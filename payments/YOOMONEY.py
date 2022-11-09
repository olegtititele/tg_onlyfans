import config.config as cf
from yoomoney import Client, Quickpay


class YooMoney(object):
    def __init__(self):
        self.card = cf.YOOMONEY_CARD
        self.YOOMONEY_PRIV_KEY = cf.YOOMONEY_PRIV_KEY
        
    def make_bill(self, bill_id, amount, comment):
        quickpay = Quickpay(
            receiver=self.card,
            quickpay_form="shop",
            targets=comment,
            paymentType="SB",
            sum=amount,
            label=bill_id
        )
        
        return quickpay.base_url
        

    def check_payment(self, bill_id):
        client = Client(self.YOOMONEY_PRIV_KEY)
        history = client.operation_history(label=bill_id)
    
        for operation in history.operations:
            return operation.status