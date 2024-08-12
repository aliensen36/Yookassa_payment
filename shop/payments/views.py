from django.shortcuts import render, redirect
from .models import Order
from yookassa import Payment, Configuration
from decouple import config, Csv
import uuid

Configuration.account_id = config('YOOKASSA_SHOP_ID')
Configuration.secret_key = config('YOOKASSA_SECRET_KEY')


def create_order(request):
    if request.method == 'POST':
        product_name = request.POST['product_name']
        amount = request.POST['amount']

        order = Order.objects.create(product_name=product_name, amount=amount)

        base_url = config('BASE_URL')
        return_url = f"{base_url}/payment_success/"

        payment = Payment.create({
            "amount": {
                "value": str(amount),
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": return_url
            },
            "capture": True,
            "description": f"Order {order.id} - {product_name}"
        }, uuid.uuid4())

        order.payment_status = 'created'
        order.save()

        return redirect(payment.confirmation.confirmation_url)

    return render(request, 'payments/create_order.html')


def payment_success(request):
    return render(request, 'payments/success.html')
