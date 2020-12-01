import stripe

stripe.api_key = ""


class StripeRequests:

    @staticmethod
    def get_stripe_balance():
        return stripe.Balance.retrieve()

    @staticmethod
    def get_stripe_info():
        return stripe.Account.retrieve()
