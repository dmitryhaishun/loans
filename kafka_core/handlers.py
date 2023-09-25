import logging
from typing import Any

from app.celery_loans.worker import app

logger = logging.getLogger(__name__)


def api_gateway_handler(message: Any):
    pass


def accounts_handler(message: Any):
    pass


def deposits_handler(message: Any):
    pass


def cards_handler(message: Any):
    pass


def loans_handler(message: Any):
    pass


@app.task(name="user_registration_handler")
def user_registration_handler(message: Any):
    logger.info(f" message - {message}")
