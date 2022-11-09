from pyqiwip2p import AioQiwiP2P
from db.db import DB
import config.config as cf


class Qiwi(object):
    def __init__(self):
        self.db = DB()
        self.QIWI_PRIV_KEY = cf.QIWI_PRIV_KEY#self.db.get_qiwi_api()
        self.p2p = AioQiwiP2P(auth_key=self.QIWI_PRIV_KEY)
        
    async def make_bill(self, bill_id, amount, comment):
        lifetime = 30
        return await self.p2p.bill(bill_id=bill_id, amount=amount, lifetime=lifetime, comment=comment)
        
    
    async def get_pay_url(self, bill_id):
        pay_url = (await self.p2p.check(bill_id=bill_id)).pay_url

        return pay_url

    async def check_payment(self, bill_id):
        payment_status = (await self.p2p.check(bill_id=bill_id)).status
        
        return payment_status
    
    async def get_payment_amount(self, bill_id):
        payment_amount = (await self.p2p.check(bill_id=bill_id)).amount
        
        return payment_amount
    
    async def reject_payment(self, bill_id):
        try:
            await self.p2p.reject(bill_id=bill_id)
        except:
            return