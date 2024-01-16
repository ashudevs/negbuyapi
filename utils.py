from django.contrib.auth.tokens import PasswordResetTokenGenerator
from requests import request
import six
from yaml import serialize
from negbuy import settings
from negbuyapi import Checksum
from negbuyapi.models import userDB
import requests
from negbuyapi.serializers import UserSerializer

class TokenGenerator(PasswordResetTokenGenerator):
    
    def _make_hash_value(self,user,timestamp):
        return (six.text_type(user.user_id))+(six.text_type(user.email))+(six.text_type(timestamp))

generate_token = TokenGenerator()

# Paytm 

def VerifyPaytmResponse(response):
    response_dict = {}
    if response.method == "POST":
        data_dict = {}
        for key in response.POST:
            data_dict[key] = response.POST[key]
        MID = data_dict['MID']
        ORDERID = data_dict['ORDERID']
        print(MID)
        print(ORDERID)
        verify = Checksum.verify_checksum(data_dict, settings.PAYTM_MERCHANT_KEY, data_dict['CHECKSUMHASH'])
        if verify:
            STATUS_URL = settings.PAYTM_TRANSACTION_STATUS_URL
            data = '{"MID":"%s","ORDERID":"%s"}'%(MID, ORDERID)
            check_resp = requests.post(STATUS_URL, data=data).json()
            if check_resp['STATUS']=='TXN_SUCCESS':
                response_dict['verified'] = True
                response_dict['paytm'] = check_resp
                return (response_dict)
            else:
                response_dict['verified'] = False
                response_dict['paytm'] = check_resp
                return (response_dict)
        else:
            response_dict['verified'] = False
            return (response_dict)
    response_dict['verified'] = False
    return response_dict

