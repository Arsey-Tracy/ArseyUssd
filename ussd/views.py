from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Vendor, Transporter, Order, Role


# Create your views here.
@csrf_exempt
def ussd_callback(request):
    session_id = request.POST.get('sessionId', None)
    service_code = request.POST.get('serviceCode', None)
    phone_number = request.POST.get('phoneNumber', None)
    text = request.POST.get('text', '')

    response = ""

    # check user role
    role = Role.objects.filter(phone_number=phone_number).first()
    vendor = Vendor.objects.filter(phone_number=phone_number).first()
    transporter = Transporter.objects.filter(phone_number=phone_number).first()

    if role:
        if role.role == 'vendor':
            if text == "":
                response = "CON Welcome back, Vendor!\n"
                response += "1. place a new order\n"
                response += "2. view your orders\n"
                response += "3. Search for transporters\n"
            elif text == "1":
                response = "Enter details for the new order:"
            elif text.startswith("1*"):
                order_details = text.split('*', 1)[1]
                Order.objects.create(vendor=vendor, details=order_details)
                response = "END Your order has been placed."

            elif text == "2":
                orders = Order.objects.filter(vendor=vendor)
                if orders.exists():
                    response = "CON Your orders:\n"
                    for order in orders:
                        response += f"{order.id}. {order.details}-{order.status}\n"
                else:
                    response = "END your have no orders."
            elif text == "3":
                transporters = Transporter.objects.all()
                if transporters.exists():
                    response = "CON Available transporters:\n"
                    for transporter in transporters:
                        response += f"{transporter.id}. {transporter.name}\n"
                else:
                    response = "END No Available transporters."
        elif role.role == 'transporter':
            if text == "":
                response = "CON Welcome back, Transporter!\n"
                response += "1. View available orders\n"
                response += "2. Update order status\n"
            elif text == "1":
                orders = Order.objects.filter(vendor=vendor)
                if orders.exists():
                    response = "CON Available orders:\n"
                    for order in orders:
                        response += f"{order.id}. {order.details} (Vendor: {order.vendor.name})\n"
                else:
                    response = "END No Available orders."
    else:

        if text == "":
            response = "CON Welcome to tranlink\n"
            response += "1. Register as vendor\n"
            response += "2. Register as transporter\n"
        elif text == "1":
            response = "CON Enter your name to register as vendor:"
        elif text.startswith("1*"):
            name = text.split('*')[1]
            Vendor.objects.create(name=name, phone_number=phone_number)
            Role.objects.create(phone_number=phone_number, role='vendor')
            response = "END you have been registered as a vendor."

        elif text == "2":
            response = "CON Enter your name to register as Transporter:."
        elif text.startswith("2*"):
            name = text.split('*')[1]
            Transporter.objects.create(name=name, phone_number=phone_number)
            Role.objects.create(phone_number=phone_number, role='transporter')
            response = "END you have been registered as a Transporter."
        else:
            response = "END Invalid choice."
    return HttpResponse(response, content_type='text/plain')
from django.shortcuts import render

# Create your views here.
