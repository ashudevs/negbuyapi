import razorpay, requests
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework.response import Response
from negbuy import settings
from .models import *
from .serializers import *
from rest_framework.decorators import api_view


#############     DDP     #############


@api_view(["POST"])
def ddp_click_on_pay_now(request):
    try:
        user_id = request.headers["User-id"]
        user = userDB.objects.filter(user_id=user_id)
        print(user)
        if user:
            instance_id = int(request.data["instance_id"])
            ppo = Purchase_Process_DP.objects.filter(id=instance_id)
            print(ppo)

            if ppo:
                ppo[0].status = "processing"
                ppo[0].save()
                print("aaaaaaaaa")
                client = razorpay.Client( 
                    auth=(settings.RAZORPAYKEYID, settings.RAZORPAYKEYSECRET)
                )
                print("qqqqqq")
                payment = client.order.create(
                    {
                        "amount": int(str(round(ppo[0].total_amount)) + '00'),
                        "currency": "INR",
                        "payment_capture": "1",
                    }
                )
                print("qqqq")

                ppo[0].razorpay_id = payment["id"]
                ppo[0].razorpay_currency = payment["currency"]
                ppo[0].save

                return Response(
                    {
                        "status": True,
                        "message": "Success",
                        "data": {
                            "amount": payment["amount"],
                            "razorpar_amount":str(payment["amount"]) + '00',
                            "currency": payment["currency"],
                            "order_id": payment["id"],
                            "name": ppo[0].user_id.first_name,
                            "email": ppo[0].user_id.email,
                            "phone": ppo[0].user_id.phone,
                        },
                    }
                )

            else:
                return Response(
                    {
                        "status": False,
                        "message": "You replaced your cart with some other item. Please check your cart.",
                        "data": {},
                    }
                )

        else:
            return Response(
                {"status": False, "message": "Unauthorised User", "data": {}}
            )

    except Exception as e:
        return Response({"status": "Error", "message": str(e), "data": {}})


@api_view(["POST"])
def ddp_callbackrazor(request):
    try:
        user_id = request.headers["User-id"]
        user = userDB.objects.filter(user_id=user_id)
        if user:
            instance_id = int(request.data["instance_id"])
            ppo = Purchase_Process_DP.objects.filter(id=instance_id)

            if ppo:
                razorpay_order_id = request.data["razorpay_order_id"]
                razorpay_payment_id = request.data["razorpay_payment_id"]
                razorpay_signature = request.data["razorpay_signature"]

                client = razorpay.Client(
                    auth=(settings.RAZORPAYKEYID, settings.RAZORPAYKEYSECRET)
                )

                generated_signature = client.utility.verify_payment_signature(
                    {
                        "razorpay_order_id": razorpay_order_id,
                        "razorpay_payment_id": razorpay_payment_id,
                        "razorpay_signature": razorpay_signature,
                    }
                )

                if generated_signature:
                    ppo[0].razorpay_payment_id = razorpay_payment_id
                    ppo[0].save()

                    ddo_obj = DDP_Orders_DB.objects.create(
                        ddp_buyer_id=ppo[0].user_id,
                        ddp_seller_id=ppo[
                            0
                        ].product_id.variant_id.main_product_id.seller_id,
                        product_id=ppo[0].product_id,
                        payment_id=ppo[0].razorpay_payment_id,
                        product_price=ppo[0].price,
                        quantity=ppo[0].quantity,
                        shipping_address=ppo[0].delivery_address,
                        pincode=ppo[0].pincode,
                        country=ppo[0].country,
                        state=ppo[0].state,
                        city=ppo[0].city,
                        company_courier_id=ppo[0].company_courier_id,
                        company_courier_name=ppo[0].company_courier_name,
                        expected_delivery_date=(
                            timedelta(ppo[0].estimated_delivery_days + 2)
                            + timezone.localtime(timezone.now())
                        ).strftime("%-d %B %Y"),
                        transport_mode=ppo[0].transport_mode,
                        courier_charges=ppo[0].courier_charges,
                        total_weight=ppo[0].total_weight,
                        gst=ppo[0].gst,
                        service_charge=ppo[0].service_charge,
                        total_amount=ppo[0].total_amount,
                        razorpay_order_id=ppo[0].razorpay_order_id,
                        razorpay_payment_id=ppo[0].razorpay_payment_id,
                    )
                    ddo_obj.save()
                    ppo[0].delete()

                    return Response({"status": True, "message": "Success", "data": ddo_obj.id})

                else:
                    return Response(
                        {
                            "status": False,
                            "message": "Unauthorised Signature",
                            "data": {},
                        }
                    )
            else:
                return Response(
                    {
                        "status": False,
                        "message": "You replaced your cart with some other item. Please check your cart.",
                        "data": {},
                    }
                )
        else:
            return Response(
                {"status": False, "message": "Unauthorised User", "data": {}}
            )
    except Exception as e:
        return Response({"status": "Error", "message": str(e), "data": {}})


###########       EXWORK       ############


@api_view(['POST'])
def create_exwork_order(request):
    try:
        user_id = request.headers["User-id"]
        user = userDB.objects.filter(user_id=user_id)
        if user:
            instance_id = int(request.data["instance_id"])
            ppo = Purchase_Process_DP.objects.filter(id=instance_id)

            if ppo:
                ppo[0].status = "processing"
                ppo[0].save()

                order=Exwork_Orders_DB.objects.create(
                    exwork_buyer_id=ppo[0].user_id,
                    exwork_seller_id=ppo[
                        0
                    ].product_id.variant_id.main_product_id.seller_id,
                    order_id=instance_id,
                    product_id=ppo[0].product_id,
                    product_price=ppo[0].price,
                    quantity=ppo[0].quantity,
                    shipping_address=ppo[0].delivery_address, 
                    pincode=ppo[0].pincode,
                    country=ppo[0].country,
                    state=ppo[0].state,
                    city=ppo[0].city,
                    expected_delivery_date=(
                        timedelta(4)
                        + timezone.localtime(timezone.now())
                    ).strftime("%-d %B %Y"),
                    transport_mode=ppo[0].transport_mode,
                    total_weight=ppo[0].total_weight,
                    gst=ppo[0].gst,
                    service_charge=ppo[0].service_charge,
                    total_amount=ppo[0].total_amount,
                )

                ppo[0].delete()

                return Response({"status": True, "message": "Success", "data": {'id':order.id}})

            else:
                return Response(
                    {
                        "status": False,
                        "message": "You replaced your cart with some other item. Please check your cart.",
                        "data": {},
                    }
                )

        else:
            return Response(
                {"status": False, "message": "Unauthorised User", "data": {}}
            )

    except Exception as e:
        return Response({"status": "Error", "message": str(e), "data": {}})


@api_view(["POST"])
def exwork_click_on_pay_now(request):
    try:
        user_id = request.headers["User-id"]
        user = userDB.objects.filter(user_id=user_id)
        if user:
            order_id = int(request.data["order_id"])
            order = Exwork_Orders_DB.objects.get(id=order_id)

            client = razorpay.Client(
                auth=(settings.RAZORPAYKEYID, settings.RAZORPAYKEYSECRET)
            )

            payment = client.order.create(
                {
                    "amount": int(str(round(order.total_amount)) + '00'), #int(str(round(ppo[0].total_amount)) + '00')
                    "currency": "INR",
                    "payment_capture": "1",
                }
            )

            order.razorpay_order_id = payment["id"]
            order.save()

            return Response(
                {
                    "status": True,
                    "message": "Success",
                    "data": {
                        "id":order.id,
                        "amount": payment["amount"],
                        "currency": payment["currency"],
                        "order_id": payment["id"],
                        "name": order.exwork_buyer_id.first_name,
                        "email": order.exwork_buyer_id.email,
                        "phone": order.exwork_buyer_id.phone,
                        "ppo":order.order_id,
                    },
                }
            )
        else:
            return Response(
                {"status": False, "message": "Unauthorised User", "data": {}}
            )

    except Exception as e:
        return Response({"status": "Error", "message": str(e), "data": {}})


@api_view(["POST"])
def exwork_callbackrazor(request):  #currency, instance_id
    try:
        user_id = request.headers["User-id"]
        user = userDB.objects.filter(user_id=user_id)
        if user:
            order_id = int(request.data["id"])
            order = Exwork_Orders_DB.objects.get(id=order_id)
        
            razorpay_order_id = request.data["razorpay_order_id"]
            razorpay_payment_id = request.data["razorpay_payment_id"]
            razorpay_signature = request.data["razorpay_signature"]

            client = razorpay.Client(
                auth=(settings.RAZORPAYKEYID, settings.RAZORPAYKEYSECRET)
            )

            generated_signature = client.utility.verify_payment_signature(
                {
                    "razorpay_order_id": razorpay_order_id,
                    "razorpay_payment_id": razorpay_payment_id,
                    "razorpay_signature": razorpay_signature,
                }
            )

            if generated_signature:
                order.razorpay_payment_id = razorpay_payment_id
                order.razorpay_order_id = razorpay_order_id
                order.save()

                return Response({"status": True, "message": "Success", "data": order.id})

            else:
                return Response(
                    {
                        "status": False,
                        "message": "Unauthorised Signature",
                        "data": {},
                    }
                )
        else:
            return Response(
                {"status": False, "message": "Unauthorised User", "data": {}}
            )
    except Exception as e:

        return Response({"status": "Error", "message": str(e), "data": {}})
    

@api_view(["POST"])
def Payment_success(request):
    try:
        user_id = request.headers["User-id"]
        user = userDB.objects.get(user_id=user_id)
            
        if user:
            #type of order, ex-work or ddp
            order_id = int(request.data["id"])
            shipment_type = request.data["shipment_type"]
            if shipment_type == "DDP":
                order = DDP_Orders_DB.objects.get(id=order_id)

                final_response = {
                    "billing_name":user.first_name + " " + user.last_name,
                    "payment_details": order.payment_id,
                    "shipping_address":order.shipping_address,
                    "billing_address":order.billing_address,
                    "contact_details":user.phone,
                    "shipping_method":order.transport_mode,
                    "product_image":order.product_id.variant_id.main_image.url,
                    "product_title":order.product_id.variant_id.main_product_id.product_title,
                    "courier_name":order.company_courier_name,
                    "quantity":order.quantity,
                    "product_price":order.product_price,
                    "gst":order.gst,
                    "service_charge":order.service_charge,
                    "delivery_charge":order.courier_charges,
                    "total_amount":order.total_amount,
                }

                return Response({"status": True, "message": "Success", "data": final_response})

            if shipment_type == "Ex-work":
                order = Exwork_Orders_DB.objects.get(id=order_id)

                final_response = {
                    "billing_name":user.first_name + " " + user.last_name,
                    "payment_details": order.payment_id,
                    "shipping_address":order.shipping_address,
                    "billing_address":order.billing_address,
                    "contact_details":user.phone,
                    "shipping_method":order.transport_mode,
                    "product_image":order.product_id.variant_id.main_image.url,
                    "product_title":order.product_id.variant_id.main_product_id.product_title,
                    "quantity":order.quantity,
                    "product_price":order.product_price,
                    "gst":order.gst,
                    "total_amount":order.total_amount,
                }

                return Response({"status": True, "message": "Success", "data": final_response})

            #razorpay_order_id = request.data["razorpay_order_id"]
            #razorpay_payment_id = request.data["razorpay_payment_id"]
            #razorpay_signature = request.data["razorpay_signature"]

            #client = razorpay.Client(
            #    auth=(settings.RAZORPAYKEYID, settings.RAZORPAYKEYSECRET)
            #)

            #generated_signature = client.utility.verify_payment_signature(
            #    {
            #        "razorpay_order_id": razorpay_order_id,
            #        "razorpay_payment_id": razorpay_payment_id,
            #        "razorpay_signature": razorpay_signature,
            #    }
            #)

            

            else:
                return Response(
                    {
                        "status": False,
                        "message": "Unauthorised Signature",
                        "data": {},
                    }
                )
        else:
            return Response(
                {"status": False, "message": "Unauthorised User", "data": {}}
            )
    except Exception as e:

        return Response({"status": "Error", "message": str(e), "data": {}})
    



