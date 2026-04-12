import razorpay

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings

from .models import Product, Cart, Order


# 🏠 HOME PAGE
def home(request):
    products = Product.objects.all()
    cart_count = Cart.objects.count()

    return render(request, 'home.html', {
        'products': products,
        'cart_count': cart_count
    })


# 🛒 ADD TO CART
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(product=product)

    cart_item.quantity += 1
    cart_item.save()

    return redirect('cart')


# 🛍 CART PAGE
def cart(request):
    items = Cart.objects.all()

    total = sum(item.product.price * item.quantity for item in items)

    return render(request, 'cart.html', {
        'items': items,
        'total': total
    })


# ➕ INCREASE QUANTITY
def increase_quantity(request, id):
    item = get_object_or_404(Cart, id=id)
    item.quantity += 1
    item.save()
    return redirect('cart')


# ➖ DECREASE QUANTITY
def decrease_quantity(request, id):
    item = get_object_or_404(Cart, id=id)

    item.quantity -= 1

    if item.quantity <= 0:
        item.delete()
    else:
        item.save()

    return redirect('cart')


# 💳 CHECKOUT + PAYMENT
def checkout(request):
    items = Cart.objects.all()
    total = sum(item.product.price * item.quantity for item in items)

    if request.method == "POST":

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        payment_method = request.POST.get("payment_method")

        # 🟡 CASH ON DELIVERY
        if payment_method == "COD":
            Order.objects.create(
                name=name,
                phone=phone,
                address=address,
                payment_method="COD"
            )

            Cart.objects.all().delete()
            return redirect('success')

        # 🟢 RAZORPAY PAYMENT
        client = razorpay.Client(auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        ))

        payment = client.order.create({
            "amount": int(total * 100),  # paise
            "currency": "INR",
            "payment_capture": "1"
        })

        return render(request, "payment.html", {
            "payment": payment,
            "total": total,
            "name": name,
            "phone": phone,
            "address": address,
            "RAZORPAY_KEY_ID": settings.RAZORPAY_KEY_ID
        })

    return render(request, "checkout.html", {
        "total": total
    })


# ✅ SUCCESS PAGE
def success(request):
    Cart.objects.all().delete()
    return render(request, 'success.html')