Django Shop Project
Это pet проект магазина. Он представляет собой пример реализации функционала интернет-магазина с использованием Django.

Установка и настройка
Клонируйте репозиторий с помощью команды:

```git clone https://github.com/warkinstar/shop.git```

Перейдите в каталог проекта:

```cd shop```

Создайте виртуальную среду и активируйте её:

```
python -m venv .venv
.venv/scripts/activate
```

Установите зависимости, указанные в файле requirements.txt:

```pip install -r requirements.txt```

Установить зависимости для WeasyPrint для вашей операционной системы https://doc.courtbouillon.org/weasyprint/stable/first_steps.html. Это необходимо для генерации pdf чеков, которые генерируются из html шаблона.

Примените миграции базы данных:

```python manage.py migrate```

Создайте суперпользователя:

```python manage.py createsuperuser```

Для функционала оплаты проведите ключи платежной системы Stripe. Создайте файл .env и добавьте
```env
STRIPE_PUBLISHABLE_KEY = "pk_test_your_key"
STRIPE_SECRET_KEY = "sk_test_your_key"
STRIPE_WEBHOOK_SECRET = "whsec_yourWebhookKey"
``` 
Так же необходимо запустить в контейнере Docker rabbitmq и redis:

```cmd
docker pull rabbitmq
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management

docker pull redis
docker run -it --rm --name redis -p 6379:6379 redis
```

Запустите celery worker
```cmd
celery -A myshop worker -l info
```

Если worker не выполняет задачи запуск воркера через gevent:

```celery -A myshop worker -l info -P gevent```

Мониторинг Celery при помощи Flower:
```celery -A myshop flower```

Запуск прослушки события оплаты вебхуков для тестирования уведомлений:
```stripe listen --forward-to localhost:8000/payment/webhook/```

Запустите сервер разработки:

```python manage.py runserver```

Теперь вы можете открыть приложение в браузере по адресу http://localhost:8000.

Функциональность
Проект магазина включает в себя следующие функции:

Просмотр списка категорий и продуктов.
Добаваление товаров в корзину.
Добавление продуктов в корзину.
Оформление заказов.
Оплата через сервис Stripe.
Интернационализация ru-en.
Административный интерфейс для управления продуктами, категориями и заказами.
Дополнительные настройки
В файле settings.py вы можете настроить дополнительные параметры проекта, такие как база данных, статические файлы, международные настройки и другие.

Для использования функционала отправки электронной почты, установите соответствующие параметры в файле settings.py. По умолчанию, проект настроен на использование консольного бэкенда отправки почты.

Contributing
Если вы обнаружили ошибки или у вас есть предложения по улучшению проекта, пожалуйста, создайте новый Issue или отправьте Pull Request.

## Лицензия

Этот проект лицензирован в соответствии с лицензией MIT. Подробности можно найти в файле [LICENSE](LICENSE).

