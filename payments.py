from asyncio.base_subprocess import ReadSubprocessPipeProto
from urllib import response
from .models import *
import requests
from .serializers import *
import json
from negbuy import settings
import razorpay
import pycountry
# Nilabh Sahu 
from paytmchecksum import PaytmChecksum
import uuid
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# RAZORPAY_KEY_ID = "rzp_test_Z9UTQglaPACbxX" #test
# RAZORPAY_KEY_SECRET = "qLvm96SmX8pHRTyJ5mQ42x4Y" #test
RAZORPAY_KEY_ID = "rzp_live_5ncJ5tnoDg4U7m" #live
RAZORPAY_KEY_SECRET = "P2NfnOebso1JL3H5iAozD18P" #live
m_id = settings.PAYTM_MERCHANT_ID
m_key = settings.PAYTM_MERCHANT_KEY
order_id = ""
txnToken = ""
paymentMode = ""
cardNo = ""
cvv=""
expirymonth=""
expiryyear=""
channelcode=""


@api_view(['POST','GET'])
def InitiateTransactionAPI(request):
    if request.method == "GET":
        return render(request, 'cardpay.html')
    if request.method == "POST":   
        global order_id
        global txnToken
        order_id = uuid.uuid4()
        data = request.data
        user_id = request.headers['User-id']
        productID = data['product_id']
        usr = userDB.objects.get(user_id=user_id)
        prods = product.objects.get(id=productID)
        product_name = prods.name
        amount = prods.price
        address=usr.city

        transaction = Orders_Id.objects.create(ORDER_ID = order_id, User_Id = user_id,
                                Mobile = usr.phone ,Address=address,TXNAMOUNT= str(amount),
                            Product_Name =product_name, Username = usr.username)

        paytmParams = dict()
        

        paytmParams["body"] = {
            "requestType"   : "Payment",
            "mid"           : m_id,
            "websiteName"   : settings.PAYTM_WEBSITE,
            "orderId"       : str(order_id),
            "callbackUrl"   : "http://localhost:8000/api/callback",
            "txnAmount"     : {
                "value"     : str(amount),
                "currency"  : "INR",
                },
            "userInfo"      : {
                "custId"    : str(user_id),
            },
        }

        checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), m_key)

        paytmParams["head"] = {
            "signature": checksum,
            "channelId":"WEB"
        }

        # # for Production
        # url = f"https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid={m_id}&orderId={order_id}"

        post_data = json.dumps(paytmParams)

        #for Staging
        url = f"https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid={m_id}&orderId={order_id}"

        response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()

        transaction.Checksum = response['head']['signature']
        transaction.txnToken = response['body']['txnToken']
        txnToken = response['body']['txnToken']
        transaction.save()
        # param_dict = {
        #     'mid':m_id,
        #     'txnToken': response['body']['txnToken'],
        #     'orderId': paytmParams['body']['orderId'],
        #     'company_name': settings.PAYTM_COMPANY_NAME
        # }
        return Response(response)

@api_view(['POST'])
def SendOtpAPI(request):
    phone = request.data['phone']

    # Send OTP API
    otpdict =dict()

    otpdict["body"] = {
        "mobileNumber" : phone
    }

    otpdict["head"] = {
        "channelId": "WEB",
        "txnToken" : txnToken
    }
    postal_data = json.dumps(otpdict)

    # for Staging
    sendOTPurl = f"https://securegw-stage.paytm.in/login/sendOtp?mid={m_id}&orderId={order_id}"

    resp = requests.post(sendOTPurl, data = postal_data, headers = {"Content-type": "application/json"}).json()
    #print(resp)
    return Response({"message":resp["body"]["resultInfo"]["resultMsg"]})

@api_view(['POST'])
def verifyOtpAPI(request):
    otp = request.data['otp'] #888888

    paytmParams = dict()

    paytmParams["body"] = {
    "otp"      : str(otp)
    }

    paytmParams["head"] = {
    "channelId": "WEB",
    "txnToken" : txnToken
    }

    post_data = json.dumps(paytmParams)

    # for Staging
    url = f"https://securegw-stage.paytm.in/login/validateOtp?mid={m_id}&orderId={order_id}"

    # # for Production
    # url = f"https://securegw.paytm.in/login/validateOtp?mid={m_id}&orderId={order_id}"

    response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
    param_dict = {
        "mid": m_id,
        "orderId":order_id,
        "txnToken": txnToken,
        "paymentMode": "BALANCE",
        "AUTH_MODE":"otp",
    }
    if response['body']['resultInfo']['resultStatus'] == "SUCCESS":
        return Response({"data":param_dict})
    else:
        return Response({"message": "Invalid OTP"}, status=400)

############ CARD PAYMENT API #################
# 1. Call Initiate transaction api
# 2. Call fetchBinDetail API
# 3. Call CardPaymentAPI
@api_view(['POST'])
def fetchBinDetail(request):
    global paymentMode

    data= request.data
    bin = data['bin']
    payParams = dict()

    payParams["body"] = {
        "bin"       :  bin #"411111",
    }

    payParams["head"] = {
        "channelId"     : "WEB",
        "tokenType" : "TXN_TOKEN",
        "token"  : txnToken
    }

    pos_data = json.dumps(payParams)

    # for Staging
    url = f"https://securegw-stage.paytm.in/fetchBinDetail?mid={m_id}&orderId={order_id}" #As soon as the first 6 digits are entered, this api will get the BIN details of the card.

    # # #for Production
    # url = f"https://securegw.paytm.in/fetchBinDetail?mid={m_id}&orderId={order_id}"

    respon = requests.post(url, data = pos_data, headers = {"Content-type": "application/json"}).json()

    paymentMode = respon['body']['binDetail']['paymentMode']
    #print(paymentMode)
    
    if respon['body']['resultInfo']['resultMsg']!="Success":
        return Response({"message":"Invalid Card Details"}, status=400)
    else:
        return Response({"paymentmode":paymentMode})
        
@api_view(['POST','GET'])
def CardPaymentAPI(request):
    global cardNo
    global cvv
    global expirymonth
    global expiryyear
    if request.method == "GET":
        return render(request, 'cardpay.html')

    data= request.data
    cardNo = data['cardNo']
    cvv = data['cvv']
    expirymonth = data['expirymonth']
    expiryyear = data['expiryyear']

    param_dict = {
        "mid": m_id,
        "orderId":str(order_id),
        "txnToken":txnToken,
        "paymentMode": paymentMode,
        "cardInfo": f"|{cardNo}|{cvv}|{expirymonth}{expiryyear}",
        "AUTH_MODE":"otp",
    }
    #return render(request, 'demo.html', {'data':param_dict})
    return Response(param_dict)

######### Net Banking ###############

# 1. Initiate transaction API
# 2. Fetch PaymentOptionsAPI
## if user not chooses these available banks from these, we will call FetchNBpayementAPI
# 3. Fetch NB Payment API

@api_view(['POST'])
def FetchPaymentOptionsAPI(request):
    paytmParams = dict()

    paytmParams["body"] = {

        "mid"           : m_id,
        "orderId"       : str(order_id),
        "returnToken"   :  "true"
    }
    paytmParams["head"] = {
        "channelId"     : "WEB",
        "tokenType"     : "TXN_TOKEN",
        "token"         : txnToken
    }
    post_data = json.dumps(paytmParams)

    # for Staging
    url = f"https://securegw-stage.paytm.in/theia/api/v2/fetchPaymentOptions?mid={m_id}&orderId={order_id}"

    # for Production
    # url = "https://securegw.paytm.in/theia/api/v2/fetchPaymentOptions?mid=YOUR_MID_HERE&orderId=ORDERID_98765"
    response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
    paymentBankDetails = response['body']['merchantPayOption']['paymentModes'][3]['payChannelOptions']
    if response['body']['resultInfo']['resultMsg']!="Success":
        return Response({"message":"Something Went Wrong !!"}, status=400)
    else:
        return Response({"BankDetails":response})

@api_view(['POST'])
def FetchNBpaymentAPI(request):
    paytmParams = dict()

    paytmParams["body"] = {
        "type"     : "MERCHANT",
    }

    paytmParams["head"] = {
        "channelId"     : "WEB",
        "tokenType"     : "TXN_TOKEN",
        "token"         : txnToken
    }

    post_data = json.dumps(paytmParams)

    # for Staging
    url = f"https://securegw-stage.paytm.in/theia/api/v1/fetchNBPaymentChannels?mid={m_id}&orderId={order_id}"

    # for Production
    # url = "https://securegw.paytm.in/theia/api/v1/fetchNBPaymentChannels?mid=YOUR_MID_HERE&orderId=ORDERID_98765"

    response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
    morebanks = response['body']['nbPayOption']['payChannelOptions'] # array of banks and their info
    #paymentBankDetails = response['body']['merchantPayOption']['paymentModes']
    if response['body']['resultInfo']['resultMsg']!="Success":
        return Response({"message":"Something Went Wrong !!"}, status=400)
    else:
        return Response({"data":morebanks})

@api_view(['POST','GET'])
def NetBankingAPI(request):
    if request.method == "GET":
        return render(request, 'pay.html')
    global channelcode
    channelcode = request.data['channelcode']
    param_dict = {
        "mid": m_id,
        "orderId":str(order_id),
        "txnToken": txnToken,
        "paymentMode": "NET_BANKING",
        "channelCode": str(channelcode),
        "AUTH_MODE":"otp",
    }
    return render(request, 'demo.html', {'data':param_dict})
    #return Response(param_dict)

@api_view(['POST'])
def transactionStatusAPI(request):
    paytmParams = dict()

# body parameters
    paytmParams["body"] = {

        # Find your MID in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
        "mid" : m_id,

        # Enter your order id which needs to be check status for
        "orderId" : str(order_id),
    }

    # Generate checksum by parameters we have in body
    # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys 
    checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), m_key)

    # head parameters
    paytmParams["head"] = {

        # put generated checksum value here
        "signature"	: checksum
    }

    # prepare JSON string for request
    post_data = json.dumps(paytmParams)

    # for Staging
    url = "https://securegw-stage.paytm.in/v3/order/status"

    # # for Production
    # url = "https://securegw.paytm.in/v3/order/status"

    response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
    return Response(response)

@api_view(['POST','GET'])
def UPIPayment(request):
    if request.method == "GET":
        return render(request, 'pay.html')
    vpa = request.data['vpa']
    paytmParams = dict()

    paytmParams["body"] = {
        "vpa"      : str(vpa)
    }

    paytmParams["head"] = {
        "channelId"     : "WEB",
        "tokenType"     : "TXN_TOKEN",
        "token"         : txnToken
    }

    post_data = json.dumps(paytmParams)

    # for Staging
    url = f"https://securegw-stage.paytm.in/theia/api/v1/vpa/validate?mid={m_id}&orderId={order_id}"

    # for Production
    # url = "https://securegw.paytm.in/theia/api/v1/vpa/validate?mid=YOUR_MID_HERE&orderId=ORDERID_98765"

    response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
    param_dict = {
        "mid": m_id,
        "orderId":str(order_id),
        "txnToken": txnToken,
        "paymentMode": "UPI",
        "payerAccount": vpa,
    }
    return Response(response)
    #return render(request, 'demo.html', {'data':param_dict})

@api_view(['POST'])
def CardprocessTransactionAPI(request):
    paytmParams = dict()

    paytmParams["body"] = {
        "requestType" : "NATIVE",
        "mid"         : m_id,
        "orderId"     : str(order_id),
        "paymentMode" : paymentMode,
        "cardInfo"    : f"|{cardNo}|{cvv}|{expirymonth}{expiryyear}",
        "authMode"    : "otp",
    }

    paytmParams["head"] = {
        "txnToken"    : txnToken
    }

    post_data = json.dumps(paytmParams)

    # for Staging
    url = f"https://securegw-stage.paytm.in/theia/api/v1/processTransaction?mid={m_id}&orderId={order_id}"

    # # # for Production
    # url = f"https://securegw.paytm.in/theia/api/v1/processTransaction?mid={m_id}&orderId={order_id}"

    response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
    return Response(response)

@api_view(['POST','GET'])
def WalletprocessTransactionAPI(request):
    paytmParams = dict()

    paytmParams["body"] = {
        "mid": m_id,
        "orderId":str(order_id),
        "txnToken": txnToken,
        "paymentMode": "BALANCE",
        "AUTH_MODE":"otp",
    }

    paytmParams["head"] = {
        "txnToken"    : txnToken
    }

    post_data = json.dumps(paytmParams)

    # for Stagingmi
    url = f"https://securegw-stage.paytm.in/theia/api/v1/processTransaction?mid={m_id}&orderId={order_id}"

    # # for Production
    # url = f"https://securegw.paytm.in/theia/api/v1/processTransaction?mid={m_id}&orderId={order_id}"

    response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
    return Response(response)     

@api_view(['POST','GET'])
def NetBankingprocessTransaction(request):
    paytmParams = dict()

    paytmParams["body"] = {
        "mid": m_id,
        "orderId":str(order_id),
        "txnToken": txnToken,
        "paymentMode": "NET_BANKING",
        "channelCode": "SBI",
        "AUTH_MODE":"otp",
    }

    paytmParams["head"] = {
        "txnToken"    : txnToken
    }

    post_data = json.dumps(paytmParams)

    # for Stagingmi
    url = f"https://securegw-stage.paytm.in/theia/api/v1/processTransaction?mid={m_id}&orderId={order_id}"

    # # for Production
    # url = f"https://securegw.paytm.in/theia/api/v1/processTransaction?mid={m_id}&orderId={order_id}"

    response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
    return Response(response)     

@api_view(['POST','GET'])
def UPIprocessTransaction(request):
    paytmParams = dict()

    paytmParams["body"] = {
        "mid": m_id,
        "orderId":str(order_id),
        "txnToken": txnToken,
        "paymentMode": "NET_BANKING",
        "channelCode": channelcode,
        "AUTH_MODE":"otp",
    }

    paytmParams["head"] = {
        "txnToken"    : txnToken
    }

    post_data = json.dumps(paytmParams)

    # for Staging
    url = f"https://securegw-stage.paytm.in/theia/api/v1/processTransaction?mid={m_id}&orderId={order_id}"

    # # for Production
    # url = f"https://securegw.paytm.in/theia/api/v1/processTransaction?mid={m_id}&orderId={order_id}"

    response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
    return Response(response)   

mail = settings.SHIPROCKETID
passwd = settings.SHIPROCKETPASSWD

############## SHIPROCKET #############
@api_view(['GET'])
def SRauth(request):
    try:
        url = "https://apiv2.shiprocket.in/v1/external/auth/login"

        payload = json.dumps({
        "email":'vinashakcoc@gmail.com',
        "password": 'Gooooo'
        })
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        json_data = json.loads(response.text)
        return Response(json_data)
    except Exception as e:
        return Response({'message': e})


@api_view(['POST'])
def SRrates(request):
    user_id = request.headers['User-id']
    size_id = int(request.data['size_id'])
    token = request.data['token']
    quantity = request.data['quantity']
    mode = request.data['mode']
    try:
        buyer = userDB.objects.get(user_id=user_id)
        prods = ProductSizeVariations.objects.get(id=size_id)
        url = "https://apiv2.shiprocket.in/v1/external/courier/serviceability/"

        payload=json.dumps(
            {
            'pickup_postcode': 201301, #seller_pincode,382475
            'delivery_postcode': 110025,#buyer.postal_code,
            'weight': int(prods.weight) * int(quantity),
            'mode': mode,#Surface or Air,
            'cod': 1,
            })
        
        headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        json_data = json.loads(response.text)
        
        try:
            data1 = json_data['data']['available_courier_companies']
            x = range(len(data1))
            ooo = []
            for i in x:
                if mode=='Surface':
                    if data1[i]['air_max_weight'] == '0.00':
                        ooo.append({
                            'courier_company_id' :data1[i]['courier_company_id'],
                            'courier_name':data1[i]['courier_name'],
                            'quantity': int(quantity),
                            'delivery_boy_contact':data1[i]['delivery_boy_contact'],
                            'estimated_delivery_days':data1[i]['estimated_delivery_days'],
                            'estimated_date':data1[i]['etd'],
                            'rate':data1[i]['rate'],
                            'rating':data1[i]['rating'],
                            'air_max_weight':data1[i]['air_max_weight'],
                            'surface_max_weight':data1[i]['surface_max_weight'],
                            'is_surface':data1[i]['is_surface']
                        })       
                else:
                    if data1[i]['air_max_weight'] != '0.00': 
                        ooo.append({
                            'courier_company_id' :data1[i]['courier_company_id'],
                            'courier_name':data1[i]['courier_name'],
                            'quantity': int(quantity),
                            'delivery_boy_contact':data1[i]['delivery_boy_contact'],
                            'estimated_delivery_days':data1[i]['estimated_delivery_days'],
                            'estimated_date':data1[i]['etd'],
                            'rate':data1[i]['rate'],
                            'rating':data1[i]['rating'],
                            'air_max_weight':data1[i]['air_max_weight'],
                            'surface_max_weight':data1[i]['surface_max_weight'],
                            'is_surface':data1[i]['is_surface']
                        })
                                          
            return Response({"status": True, "message": "Success",'data':ooo})
        except:
            return Response({"status":False, "message": "Error", "data":json_data})
    except Exception as e:
        return Response({"status": "Error", "message": str(e), "data": {}})

@api_view(['POST'])
def SRinternationalRates(request):
    try:
        user_id = request.headers['User-id']
        size_id = int(request.data['size_id'])
        token = request.data['token']
        quantity = request.data['quantity']
        
        buyer = userDB.objects.get(user_id=user_id)
        prods = ProductSizeVariations.objects.get(id=size_id)
        country = pycountry.countries.get(name=f'{buyer.country}').alpha_2
    
        url = "https://apiv2.shiprocket.in/v1/external/courier/international/serviceability"
        payload=json.dumps(
                {
                'delivery_country': f"{pycountry.countries.get(name=f'{buyer.country}').alpha_2}",
                'pickup_postcode': 123029,
                'weight': int(prods.weight) * int(quantity),
                'cod': 0
                })
        headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
        }
   
        response = requests.request("GET", url, headers=headers, data=payload)
        json_data = json.loads(response.text)
  
        try:
            data1 = json_data['data']['available_courier_companies']
            x = range(len(data1))
            ooo = []
            for i in x:
                lola = {
                        'courier_company_id' :data1[i]['courier_company_id'],
                        'courier_name':data1[i]['courier_name'],
                        'quantity': int(quantity),
                        'delivery_boy_contact':data1[i]['delivery_boy_contact'],
                        'estimated_delivery_days':data1[i]['estimated_delivery_days'],
                        'estimated_date':data1[i]['etd'],
                        'rate':float(data1[i]['rate']['rate']),
                        'rating':data1[i]['rating'],
                    }
                ooo.append(lola)
      
            return Response({"status": True, "message": "Success",'data':ooo})
        except Exception as e:
            return Response({"status":False, "message": "Error", "data":json_data})
    except Exception as e:
        return Response({"status": "Error", "message": str(e), "data": {}})
    
from datetime import datetime

# datetime object containing current date and time
now = datetime.now()

# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M")


@api_view(['POST'])
def SRcreateorder(request): # initiate transaction api must be called before calling this api.
    user_id = request.headers['User-id']
    try:
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y %H:%M")
        token = request.data['token']
        size_id = int(request.data['size_id'])
        quantity = request.data['quantity']
        prods = ProductSizeVariations.objects.get(id=size_id)
        buyer = userDB.objects.get(user_id=user_id)
        seller = userDB.objects.get(user_id=prods.variant_id.main_product_id.seller_id.user_id)
        
        url = "https://apiv2.shiprocket.in/v1/external/orders/create/adhoc"
        
        payload = json.dumps({
        "order_id": str(order_id),
        "order_date": str(dt_string),
        "pickup_location": "Primary",
        "channel_id": "3268780",
        "comment": "Seller:" + seller.first_name,
        "billing_customer_name": buyer.first_name,
        "billing_last_name": buyer.last_name,
        "billing_address": buyer.address_line1,
        "billing_address_2": buyer.address_line2,
        "billing_city": buyer.city,
        "billing_pincode": buyer.postal_code,
        "billing_state": buyer.state,
        "billing_country": buyer.country,
        "billing_email": buyer.email,
        "billing_phone": buyer.phone,
        "shipping_is_billing": True,
        "shipping_customer_name": "",
        "shipping_last_name": "",
        "shipping_address": "",
        "shipping_address_2": "",
        "shipping_city": "",
        "shipping_pincode": "",
        "shipping_country": "",
        "shipping_state": "",
        "shipping_email": "",
        "shipping_phone": "",
        "order_items": [
        {
            "name": prods.variant_id.main_product_id.product_title,
            "sku": prods.subskuiddb.sub_sku_id,
            "units": int(quantity),
            "selling_price": str(float(prods.selling_price)),
            "discount": "",
            "tax": ""
        }
    ],
        "payment_method": "COD",
        "shipping_charges": 0,
        "giftwrap_charges": 0,
        "transaction_charges": 0,
        "total_discount": 0,
        "sub_total": int(prods.selling_price),
        "length": int(prods.dim_length),
        "breadth": int(prods.dim_width),
        "height": int(prods.dim_height),
        "weight": float(prods.weight)
        })
        headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        json_data = json.loads(response.text)
        return Response(json_data)
    except Exception as e:
        return Response({'message':e})

@api_view(['POST'])
def generateAwbSR(request):
    user_id = request.headers['User-id']
    try:
        url = "https://apiv2.shiprocket.in/v1/external/courier/assign/awb"
        shipment_id = request.data['shipment_id']
        courier_company_id = request.data['courier_company_id']
        token = request.data['token']

        payload = json.dumps({
        "shipment_id": shipment_id,
        "courier_id": courier_company_id
                })
        headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        json_data = json.loads(response.text)
        return Response(json_data)
    except Exception as e:
        return Response({'message':e})

from django.http import HttpResponse, JsonResponse

@api_view(['POST'])
def courierAPI(request):
    user_id = request.headers['User-id']
    product_id = request.data['product_id']
    courier_company_id = request.data['courier_company_id']
    courier_company_name = request.data['courier_company_name']
    delivery_charge = request.data['delivery_charge']
    quantity = request.data['quantity']
    usr = userDB.objects.get(user_id= user_id)
    prods = product.objects.get(id = product_id)
    try:
        if Courierdb.objects.filter(user=usr).exists():
            if Courierdb.objects.filter(prod =prods).exists():
                tt = Courierdb.objects.get(prod=product_id)
                if Courierdb.objects.filter(courierid= courier_company_id).exists():
                    if tt:
                        return Response({'id':tt.uniqueid}, status=200)
                else:
                    if Courierdb.objects.filter(user=usr).exists() and Courierdb.objects.filter(prod =prods).exists():
                        tt.courierid = courier_company_id
                        tt.couriername = courier_company_name
                        tt.deliveryCharge= delivery_charge
                        tt.quantity=quantity
                        tt.save()
                        return Response({'id':str(tt.uniqueid)}, status=200)
            else:
                uniqueid = uuid.uuid4()            
                courierobj = Courierdb.objects.create(uniqueid=uniqueid, user=usr, prod=prods) 
                courierobj.courierid = courier_company_id
                courierobj.couriername = courier_company_name
                courierobj.deliveryCharge= delivery_charge
                courierobj.quantity=quantity
                courierobj.save()
                return Response({'id':uniqueid,
                }, status =200)
        else:
            uniqueid = uuid.uuid4()            
            courierobj = Courierdb.objects.create(uniqueid=uniqueid, user=usr, prod=prods) 
            courierobj.courierid = courier_company_id
            courierobj.couriername = courier_company_name
            courierobj.deliveryCharge= delivery_charge
            courierobj.quantity=quantity
            courierobj.save()
            return Response({'id':uniqueid,
            }, status =200)
    except Exception as e:
        return JsonResponse({'message':e})

@api_view(['POST'])
def courierAPIv2(request):
    user_id = request.headers['User-id']
    uniqueid = request.data['uniqueid']
    usr = userDB.objects.get(user_id = user_id)
    try:
        if Courierdb.objects.filter(user=usr).exists():
            tt = Courierdb.objects.get(uniqueid=uniqueid)
            product_price = tt.prod.price
            price_according_to_quantity = product_price * int(tt.quantity)
            gst_charges = ((0.18)*(float(price_according_to_quantity)))
            negbuy_charges = ((0.02)*(float(price_according_to_quantity)))
            if tt.user == usr:
                return Response({
                    'product_id': tt.prod.id,
                    'product_name': tt.prod.name,
                    'courier_company_id':int(tt.courierid),
                    'courier_company_name':tt.couriername,
                    'main_image':tt.prod.main_image.url,
                    'quantity': int(tt.quantity),
                    'original_price':price_according_to_quantity,
                    'gst_charges':gst_charges,
                    'negbuy_charges': negbuy_charges,
                    'delivery_charges': (tt.deliveryCharge),
                    'total': float(price_according_to_quantity)+ float(gst_charges) + float(negbuy_charges) + float(tt.deliveryCharge)
                            })
        else:
            return Response({'message':'Authentication Forbidden'},status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        return Response({'message':str(e)}, status= status.HTTP_400_BAD_REQUEST)

# def cancelOrderSR(request):

#     url = "https://apiv2.shiprocket.in/v1/external/orders/cancel"

#     payload = json.dumps({
#     "ids": []
#     })
#     headers = {
#     'Content-Type': 'application/json',
#     'Authorization': 'Bearer {{token}}'
#     }

#     response = requests.request("POST", url, headers=headers, data=payload)

#     json_data = json.loads(response.text)
#     return Response(json_data)



# def shipmentDetailsSR(request):

#     url = "https://apiv2.shiprocket.in/v1/external/shipments"

#     payload={}
#     headers = {
#     'Content-Type': 'application/json',
#     'Authorization': 'Bearer {{token}}'
#     }

#     response = requests.request("GET", url, headers=headers, data=payload)
#     json_data = json.loads(response.text)
#     return Response(json_data)

@api_view(['GET','POST'])
def razorpayment(request):
    if request.method == "GET":
        return render(request, 'pay.html')
    data = request.data
    user_id = request.headers['User-id']
    productID = data['product_id']
    price = data['price']
    unique_id = data['unique_id']
    usr = userDB.objects.get(user_id=user_id)
    prods = product.objects.get(id=productID)
    amount = float(price)*100

    client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
    try:
        

        payment = client.order.create({'amount': amount, 'currency': 'INR',
                                        'payment_capture': '1'})
        transaction = Razorpay.objects.create(order_id = payment['id'], user = usr,
                                        prod = prods, unique_id = unique_id,
                                currency = payment['currency'],amount = price)

        param_dict = {
            'amount':float(price),
            'currency': payment['currency'],
            'order_id': payment['id'],
            'name':usr.first_name,
            'email':usr.email,
            'phone':usr.phone
        }
        return Response(param_dict)
        #return render(request,'demo.html', payment)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST','GET'])
def callbackrazor(request):
    if request.method == "POST":
        response = request.POST
        params_dict = {
            'razorpay_order_id': response['razorpay_order_id'],
            'razorpay_payment_id': response['razorpay_payment_id'],
            'razorpay_signature':response['razorpay_signature']
        }
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        try:
            statu = client.utility.verify_payment_signature(params_dict)
            user = Razorpay.objects.get(order_id = response['razorpay_order_id'])
            user.signature = response['razorpay_signature']
            user.payment_id = response['razorpay_payment_id']
            user.paid = True
            user.save()
            #return render(request, 'success.html')
            return redirect('https://negbuy.com/transaction/'+response['razorpay_payment_id'])
        except Exception as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def razorpay_transaction(request):
    payment_id = request.data['payment_id']
    razor = Razorpay.objects.get(payment_id=payment_id)
    razor_unique_id = razor.unique_id
    curr_date = datetime.today().strftime('%d-%m-%Y')
    razor2 = Courierdb.objects.get(uniqueid=razor_unique_id)
    product_price = razor2.prod.price
    price_according_to_quantity = product_price * int(razor2.quantity)
    gst_charges = ((0.18)*(float(price_according_to_quantity)))
    negbuy_charges = ((0.02)*(float(price_according_to_quantity)))
    response_dict = {
        'currency':razor.currency,
        'order_id':razor.order_id,
        'name': razor.user.first_name,
        'email':razor.user.email,
        'phone':razor.user.phone,
        'status': razor.paid,
        'payment_date':curr_date,
        'product_name': razor2.prod.name,
        'courier_company_name':razor2.couriername,
        'main_image': razor2.prod.main_image.url,
        'quantity':razor2.quantity,
        'original_price':float(product_price)*int(razor2.quantity),
        'gst_charges': gst_charges,
        'negbuy_charges':negbuy_charges,
        'delivery_charges':razor2.deliveryCharge,
        'total': float(price_according_to_quantity)+ float(gst_charges) + float(negbuy_charges) + float(razor2.deliveryCharge)
    }
    return Response(response_dict)
