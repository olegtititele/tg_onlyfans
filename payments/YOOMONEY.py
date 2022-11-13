import config.config as cf
from yoomoney import Client, Quickpay
import json

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
            label=str(bill_id)
        )
        
        return quickpay.base_url
        

    def operation_info(self, bill_id):
        try:
            client = Client(self.YOOMONEY_PRIV_KEY)
            history_operations = client.operation_history(label=str(bill_id)).operations
            
            if len(history_operations) == 0:
                return "not_paid"
            else:
                for operation in history_operations:
                    return operation.status
        except:
            return "not_paid"