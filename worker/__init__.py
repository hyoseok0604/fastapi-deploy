from celery import Celery  # type: ignore[reportMissingTypeStubs]

from shared.settings import settings

broker_url = "amqp://{user}:{password}@{host}:{port}/".format(
    user=settings.rabbitmq.default.user,
    password=settings.rabbitmq.default.password.get_secret_value(),
    host="rabbitmq",
    port=5672,
)

backend_url = "db+postgresql://{username}:{password}@{host}:{port}/{database}".format(
    username=settings.postgres.user,
    host=settings.postgres.host,
    password=settings.postgres.password.get_secret_value(),
    port=settings.postgres.port,
    database=settings.postgres.database,
)

celery_app = Celery(
    "worker",
    broker=broker_url,
    backend=backend_url,
    broker_connection_retry_on_startup=True,
    result_extended=True,
)

celery_app.autodiscover_tasks(["worker"])  # type: ignore[reportUnknownMemberType]
