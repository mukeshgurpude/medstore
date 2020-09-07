from django.shortcuts import render, redirect
from .forms import BillingForm
from cart.models import CartItem, Order
from .models import BillingAddress
from django.contrib import messages
from django.conf import settings
import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import re
from django.http import HttpResponse
from django.utils.crypto import get_random_string
# from allauth.account.decorators import verified_email_required
# Create your views here.


# @verified_email_required
def checkout_view(request):
    form = BillingForm
    order = Order.objects.filter(user=request.user, ordered=False)[0]
    order_items = order.items.all()
    order_total = order.get_order_total()
    item_count = sum([item.quantity for item in order_items])
    ctx = {'form': form, 'order_items': order_items, 'item_count': item_count, 'total_amount': order_total}
    saved_Address = BillingAddress.objects.filter(user=request.user)
    if saved_Address.exists():
        savedAddress = saved_Address.first()
        ctx['savedAddress'] = savedAddress

    if request.method == "POST":
        saved_Address = BillingAddress.objects.filter(user=request.user)
        if saved_Address.exists():
            form = BillingForm(request.POST, instance=saved_Address.first())
        else:
            form = BillingForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            ctx["savedAddress"] = address
        else:
            messages.error(request, "Unable to process form.. Check for errors at your side")

    return render(request, "checkout/view.html", ctx)


def payment(request, web=True):
    key = settings.STR_PUB
    order = Order.objects.filter(user=request.user, ordered=False)[0]
    order_total = order.get_order_total()
    pay_amount = round(order_total*100, 2)
    if web:
        return render(request, "checkout/payment.html", {'key': key, 'pay': pay_amount})
    else:
        return order, pay_amount


# Testing new stripe


@csrf_exempt
def stripe_conf(request):
    if request.method == "GET":
        stripe_conf = {'publicKey': settings.STR_PUB}
        return JsonResponse(stripe_conf, safe=False)


@csrf_exempt
def create_checkout_session(request):
    order, amount = payment(request, web=False)
    items = []
    for item in order.items.all():
        items.append({'name': item.item, 'quantity': item.quantity, 'currency': 'INR', 'amount': int(item.item.price*100)})
    if request.method == "GET":
        url = request.build_absolute_uri()
        url = re.findall(r"^(http[s]?://[^\/]+)(/.)?", url)[0][0]
        print(url)
        stripe.api_key = settings.STR_SEC
        try:
            session = stripe.checkout.Session.create(
                client_reference_id=request.user.id,
                success_url=url+'/success/?sessionID=CHECKOUT_SESSION_ID',
                cancel_url=url+'/cancelled/',
                payment_method_types=["card", ],
                mode='payment',
                line_items=items
            )
            return JsonResponse({'sessionId': session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STR_SEC
    endpoint_secret = settings.STRIPE_ENDPOINT_KEY
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid Payment
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        print(event)
        user_id = int(event["data"]["object"]["client_reference_id"])
        order = Order.objects.filter(user__id=user_id, ordered=False)[0]
        cart_items = CartItem.objects.filter(user__id=user_id)
        order.orderID = "or_" + get_random_string(16)
        order.paymentID = event["data"]["object"]["payment_intent"]
        order.ordered = True
        order.total = order.get_order_total()
        order.save()
        print(cart_items)
        for cart_item in cart_items:
            print(cart_item)
            cart_item.purchased = True
            cart_item.item.quantity -= cart_item.quantity
            cart_item.item.save()
            cart_item.delete()
            print(cart_item.purchased)
            print(cart_item.item.quantity)
        cart_items.delete()
        print("Payment was successful.")

    return HttpResponse(status=200)


def success(request):
    user_id = request.user.id
    order = Order.objects.filter(user__id=user_id, ordered=False)[0]
    cart_items = CartItem.objects.filter(user__id=user_id)
    order.orderID = "or_" + get_random_string(16)
    order.paymentID = "pi_" + get_random_string(16)
    order.ordered = True
    order.total = order.get_order_total()
    order.save()
    print(cart_items)
    for cart_item in cart_items:
        print(cart_item)
        cart_item.purchased = True
        cart_item.item.quantity -= cart_item.quantity
        cart_item.item.save()
        cart_item.delete()
        print(cart_item.purchased)
        print(cart_item.item.quantity)
    cart_items.delete()
    return render(request, "handle/success.html")


def fail(request):
    return render(request, "handle/fail.html")
