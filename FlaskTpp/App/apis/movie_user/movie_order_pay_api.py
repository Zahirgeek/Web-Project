# 支付(调用支付宝接口)
from alipay import AliPay, ISVAliPay
from flask_restful import Resource

from App.apis.api_contant import HTTP_OK
from App.settings import ALIPAY_APPID, APP_PRIVATE_KEY, ALIPAY_PUBLIC_KEY


class MovieOrderPayResource(Resource):


    def get(self, order_id):

        # 构建支付的客户端  AlipayClient
        alipay_client = AliPay(
            appid=ALIPAY_APPID,
            app_notify_url=None,  # 默认回调url
            # 私钥公钥未提供
            app_private_key_string=APP_PRIVATE_KEY,
            alipay_public_key_string=ALIPAY_PUBLIC_KEY,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            sign_type="RSA",  # RSA 或者 RSA2
            debug=False  # 默认False
        )
        # 使用Alipay进行支付请求的发起

        subject = "i9 20核系列 RTX2080"

        # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        # order_string = alipay_client.api_alipay_trade_page_pay(
        #     out_trade_no="1100000",
        #     total_amount=10000,
        #     subject=subject,
        #     return_url="http://www.Zahir.com",
        #     notify_url="http://www.Zahir.com"  # 可选, 不填则使用默认notify url
        # )

        # 手机网站支付
        order_string = alipay_client.api_alipay_trade_wap_pay(
            out_trade_no="1100001",
            total_amount=100000,
            subject=subject,
            return_url="http://www.Zahir.com",
            notify_url="http://www.Zahir.com"  # 可选, 不填则使用默认notify url
        )

        # 客户端操作

        pay_url = "https://openapi.alipaydev.com/gateway.do?" + order_string

        data = {
            "msg": "ok",
            "status": HTTP_OK,
            "data": {
                "pay_url": pay_url,
                "order_id": order_id
            }
        }

        return data