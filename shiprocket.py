from paytmchecksum import PaytmChecksum
import uuid
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
import json
from django.utils import timezone



###########     Generate Authentication Token     ########
@api_view(['GET'])
def generate_auth_token(request):
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

        return Response({'status':True, 'message':'success', 'data':json_data})
    
    except Exception as e:
        return Response({'status':False, 'message':str(e), 'data':{}})


##############   Check Domestic Courier Services Available     #########
@api_view(['POST'])
def domestic_couriers_available(request):
    token = request.data['token']
    pickup_pin = request.data['pickup_pin']
    delivery_pin = request.data['delivery_pin']
    weight = request.data['weight']
    mode = request.data['mode']
    try:
        url = "https://apiv2.shiprocket.in/v1/external/courier/serviceability/"
        payload=json.dumps(
            {
            'pickup_postcode': pickup_pin, #seller_pincode
            'delivery_postcode': delivery_pin,#buyer.postal_code,
            'weight': weight,
            'mode': mode,#Surface or Air,
            'cod': 0,
            })
        
        headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        json_data = json.loads(response.text)['data']['available_courier_companies']
        
        # try:
        #     data1 = json_data['data']['available_courier_companies']
        #     x = range(len(data1))
        #     ooo = []
        #     for i in x:
        #         if mode=='Surface':
        #             if data1[i]['air_max_weight'] == '0.00':
        #                 ooo.append({
        #                     'courier_company_id' :data1[i]['courier_company_id'],
        #                     'courier_name':data1[i]['courier_name'],
        #                     # 'quantity': int(quantity),
        #                     'delivery_boy_contact':data1[i]['delivery_boy_contact'],
        #                     'estimated_delivery_days':data1[i]['estimated_delivery_days'],
        #                     'estimated_date':data1[i]['etd'],
        #                     'rating':data1[i]['rating'],
        #                     'air_max_weight':data1[i]['air_max_weight'],
        #                     'surface_max_weight':data1[i]['surface_max_weight'],
        #                     'is_surface':data1[i]['is_surface'],
        #                     'rate':data1[i]['rate'],
        #                     'freight_charge':data1[i]['freight_charge'],
        #                     'id':data1[i]['id']
        #                 })       
        #         else:
        #             if data1[i]['air_max_weight'] != '0.00': 
        #                 ooo.append({
        #                     'courier_company_id' :data1[i]['courier_company_id'],
        #                     'courier_name':data1[i]['courier_name'],
        #                     # 'quantity': int(quantity),
        #                     'delivery_boy_contact':data1[i]['delivery_boy_contact'],
        #                     'estimated_delivery_days':data1[i]['estimated_delivery_days'],
        #                     'estimated_date':data1[i]['etd'],
        #                     'rating':data1[i]['rating'],
        #                     'air_max_weight':data1[i]['air_max_weight'],
        #                     'surface_max_weight':data1[i]['surface_max_weight'],
        #                     'is_surface':data1[i]['is_surface'],
        #                     'rate':data1[i]['rate'],
        #                     'freight_charge':data1[i]['freight_charge'],
        #                     'id':data1[i]['id']
        #                 })
                                          
        return Response({"status": True, "message": "Success",'data':json_data})
        # except:
        #     return Response({"status":False, "message": "Error", "data":json_data})
    except Exception as e:
        return Response({"status": "Error", "message": str(e), "data": {}})



@api_view(['POST'])
def international_couriers_available(request):
    try:
        # user_id = request.headers['User-id']
        # size_id = int(request.data['size_id'])
        token = request.data['token']
        country = request.data['country']
        weight = request.data['weight']
        pickup_pin = request.data['pickup_pin']
        url = "https://apiv2.shiprocket.in/v1/external/countries"

        payload={}
        headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        json_data = json.loads(response.text)['data']

        for i in json_data:
            if i['name'] == country:
                iso_code_2 = i['iso_code_2']
                break
    
        url = "https://apiv2.shiprocket.in/v1/external/courier/international/serviceability"
        payload=json.dumps(
                {
                'delivery_country': iso_code_2,
                'pickup_postcode': pickup_pin,
                'weight': weight,
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
                        # 'quantity': int(quantity),
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
    

##############  channel is for branding in communication   our channel id is  3268780  ######
@api_view(['POST'])
def get_all_channels(request):
    try:
        token = request.data['token']
        url = "https://apiv2.shiprocket.in/v1/external/channels"
        payload={}
        headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        json_data = json.loads(response.text)

        return Response({'status':True, 'message':'success', 'data':json_data})
    
    except Exception as e:
        return Response({'status':False, 'message':str(e), 'data':{}})
    

##############  create a new order  ######
@api_view(['POST'])
def create_custom_order(request):
    try:
        pay_mode = request.data['pay_mode']
        order_id = request.data['order_id']
        token = request.data['token']
        url = "https://apiv2.shiprocket.in/v1/external/orders/create/adhoc"
        payload = json.dumps({
        "order_id": order_id,
        "order_date": f'{timezone.localtime().strftime("%Y-%m-%d %H:%M")}',#"2019-07-24 11:11"
        "pickup_location": "NoidaOffice",
        "channel_id": "3268780",
        "comment": "",
        "billing_customer_name": "Kshitij",#f'{buyer.name}',
        "billing_last_name": "Joshi",
        "billing_address": "Jai kishan marg, Kotabagh, Nanital, Uttrakhand",
        "billing_address_2": "",
        "billing_city": "Nanital",
        "billing_pincode": "263159",
        "billing_state": "Uttrakhand",
        "billing_country": "India",
        "billing_email": "kshitijjoshi014@gmail.com",
        "billing_phone": "8595483567",
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
            "name": "Laptop",#f"{product.title}"
            "sku": "ACERNITRO",#f"{product.sku}"
            "units": 1,#f"{product.quantity}"
            "selling_price": "75000",#f"{product.price}"
            "discount": "",
            "tax": "",
            "hsn": ""
            }
        ],
        "payment_method": f"{pay_mode}",#"Prepaid"
        "shipping_charges": 0,
        "giftwrap_charges": 0,
        "transaction_charges": 0,
        "total_discount": 0,
        "sub_total": 75000,#order.amount
        "length": 35, #cm
        "breadth": 20, #cm
        "height": 2, #cm
        "weight": 3 #kg
        })
        headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        json_data = json.loads(response.text)

        return Response({'status':True, 'message':'success', 'data':json_data})
    
    except Exception as e:
        return Response({'status':False, 'message':str(e), 'data':{}})
    

############   Generate AWB for shipment   ############
@api_view(['POST'])
def generate_AWB(request):
    try:
        shipment_id = request.data['shipment_id']
        courier_id = request.data['courier_id']
        token = request.data['token']
        url = "https://apiv2.shiprocket.in/v1/external/courier/assign/awb"
        payload = json.dumps({
        "shipment_id": shipment_id,
        "courier_id": courier_id,
        "status":'reassign'
        })
        headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        json_data = json.loads(response.text)

        return Response({'status':True, 'message':'success', 'data':json_data})
    
    except Exception as e:
        return Response({'status':False, 'message':str(e), 'data':{}})


############   Generate Pick Up for shipment   ############
@api_view(['POST'])
def generate_pickup(request):
    try:
        shipment_id = request.data['shipment_id']
        token = request.data['token']
        url = "https://apiv2.shiprocket.in/v1/external/courier/generate/pickup"
        payload = json.dumps({
        "shipment_id": [
            shipment_id
        ],
        "pickup_date":[]
        })
        headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        json_data = json.loads(response.text)

        return Response({'status':True, 'message':'success', 'data':json_data})
    
    except Exception as e:
        return Response({'status':False, 'message':str(e), 'data':{}})


############   Generate Manifest   ############
@api_view(['POST'])
def generate_manifest(request):
    try:
        shipment_id = request.data['shipment_id']
        token = request.data['token']
        url = "https://apiv2.shiprocket.in/v1/external/manifests/generate"
        payload = json.dumps({
        "shipment_id": [
            shipment_id
        ]
        })
        headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        json_data = json.loads(response.text)

        return Response({'status':True, 'message':'success', 'data':json_data})
    
    except Exception as e:
        return Response({'status':False, 'message':str(e), 'data':{}})
    

############   Print Manifest   ############
@api_view(['POST'])
def print_manifest(request):
    try:
        order_id = request.data['order_id']
        token = request.data['token']
        url = "https://apiv2.shiprocket.in/v1/external/manifests/print"
        payload = json.dumps({
        "order_ids": [
            order_id
        ]
        })
        headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        json_data = json.loads(response.text)

        return Response({'status':True, 'message':'success', 'data':json_data})
    
    except Exception as e:
        return Response({'status':False, 'message':str(e), 'data':{}})
    

############   Generate Label   ############
@api_view(['POST'])
def generate_label(request):
    try:
        shipment_id = request.data['shipment_id']
        token = request.data['token']
        url = "https://apiv2.shiprocket.in/v1/external/courier/generate/label"
        payload = json.dumps({
        "shipment_id": [
            shipment_id
        ]
        })
        headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        json_data = json.loads(response.text)

        return Response({'status':True, 'message':'success', 'data':json_data})
    
    except Exception as e:
        return Response({'status':False, 'message':str(e), 'data':{}})
    

############   Generate Invoice   ############
@api_view(['POST'])
def generate_invoice(request):
    try:
        order_id = request.data['order_id']
        token = request.data['token']
        url = "https://apiv2.shiprocket.in/v1/external/orders/print/invoice"
        payload = json.dumps({
        "ids": [
            order_id
        ]
        })
        headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        json_data = json.loads(response.text)

        return Response({'status':True, 'message':'success', 'data':json_data})
    
    except Exception as e:
        return Response({'status':False, 'message':str(e), 'data':{}})
    

############   Courier Tracking with AWB Number   ############
@api_view(['POST'])
def tracking_via_AWB(request):
    try:
        awb_no = request.data['awb_no']
        token = request.data['token']
        url = f"https://apiv2.shiprocket.in/v1/external/courier/track/awb/{awb_no}"
        payload={}
        headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        json_data = json.loads(response.text)

        return Response({'status':True, 'message':'success', 'data':json_data})
    
    except Exception as e:
        return Response({'status':False, 'message':str(e), 'data':{}})