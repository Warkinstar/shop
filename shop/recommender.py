import redis
from django.conf import settings
from .models import Product


# connect to redis
r = redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)


class Recommender:
    def get_product_key(self, id):
        return f"product:{id}:purchased_with"

    def products_bought(self, products):
        products_ids = [p.id for p in products]
        for product_id in products_ids:
            for with_id in products_ids:
                # get the other products bought with each product
                if product_id != with_id:
                    # increment score for product purchased together
                    r.zincrby(
                        self.get_product_key(product_id), 1, with_id
                    )  # Увеличить оценку with_id на 1 в наборе данных get_product_key

    def suggest_products_for(self, products, max_results=6):
        product_ids = [p.id for p in products]
        if len(products) == 1:
            # only 1 product
            suggestions = r.zrange(
                self.get_product_key(product_ids[0]), 0, -1, desc=True
            )[:max_results]
        else:
            # generate a temporary key
            flat_ids = "".join([str(id) for id in product_ids])
            tmp_key = f"tmp_{flat_ids}"  # tmp_12321...
            # multiple products, combine scores of all products
            # store the resulting sorted set in a temporary key
            keys = [
                self.get_product_key(id) for id in product_ids
            ]  # [product:id:purchased_with, ...]
            r.zunionstore(tmp_key, keys)  # tmp_key
            # remove ids for the products the recommendation is for
            r.zrem(tmp_key, *product_ids)  # Удалить продукты рекомендации тех же продуктов
            # get the product ids by their score, descendant sort
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]
            # remove the temporary key
            r.delete(tmp_key)

        suggested_products_ids = [int(id) for id in suggestions]
        # get suggested products and sort by order of appearance
        suggested_products = list(Product.objects.filter(
            id__in=suggested_products_ids
        ))
        suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))
        return suggested_products

    def clear_purchases(self):
        for id in Product.objects.value_list("id", flat=True):
            r.delete(self.get_product_key(id))

