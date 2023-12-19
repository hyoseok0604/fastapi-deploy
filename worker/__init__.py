from celery import Celery  # type: ignore[reportMissingTypeStubs]

from shared.settings import settings

celery_app = Celery(
    "worker",
    broker=settings.rabbitmq_uri,
    broker_connection_retry_on_startup=True,
    result_extended=True,
)

celery_app.autodiscover_tasks(["worker"])  # type: ignore[reportUnknownMemberType]
