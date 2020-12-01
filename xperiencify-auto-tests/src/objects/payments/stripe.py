import time
from src.framework.logger import logger
from src.commons.constants import REQUEST_TIME_LIMIT
from src.framework.requests.stripe import StripeRequests

api = StripeRequests()
logger = logger.get_logger()


class Stripe:

    @staticmethod
    def get_full_balance():
        return dict(*api.get_stripe_balance().available).get("amount") + dict(*api.get_stripe_balance().pending).get("amount")

    @staticmethod
    def wait_for_payment_will_done(old_balance):
        end_time = time.time() + REQUEST_TIME_LIMIT
        new_balance = Stripe().get_full_balance()
        while old_balance >= new_balance:
            new_balance = Stripe().get_full_balance()
            if time.time() > end_time:
                logger.info(f"Stripe balance was not changed. Stripe user: {api.get_stripe_info().email}")
                raise TimeoutError(f"Stripe balance was not changed. Stripe user: {api.get_stripe_info().email}")
