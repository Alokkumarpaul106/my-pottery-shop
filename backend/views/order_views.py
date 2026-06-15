from ..models import Order,OrderItem, Product,Cart
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
import math



# shows checkout page with order summary and form to place order

import math

def checkout(request):
    # Guest user — URL থেকে product নিন
    if not request.user.is_authenticated:
        product_id = request.GET.get('product_id')
        quantity = int(request.GET.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)
        
        cart_items = [{
            'product': product,
            'quantity': quantity,
            'total_price': product.price * quantity,
        }]
        total = product.price * quantity
        total_items = quantity
        total_weight = (product.weight or 0) * quantity

    else:
        # Login user — database থেকে cart নিন
        cart_items = Cart.objects.filter(user=request.user)
        total = 0
        total_items = 0
        total_weight = 0
        for item in cart_items:
            total += item.product.price * item.quantity
            total_items += item.quantity
            item.total_price = item.product.price * item.quantity
            total_weight += (item.product.weight or 0) * item.quantity

    # Shipping rate table
    base  = {'dhaka': 70, 'sub_dhaka': 100, 'outside_dhaka': 130}
    extra = {'dhaka': 20, 'sub_dhaka': 20,  'outside_dhaka': 20}

    # Default GET এ Dhaka charge
    location = ''
    loc = 'dhaka'
    shipping = base[loc] + (math.ceil(total_weight - 1) * extra[loc] if total_weight > 1 else 0)
    grand_total = total + shipping

    if request.method == "POST":
        full_name = request.POST.get('full_name')
        phone     = request.POST.get('phone')
        address   = request.POST.get('address')
        location  = request.POST.get('location')

        # Weight + Location দিয়ে shipping
        loc      = location if location in base else 'dhaka'
        shipping = base[loc] + (math.ceil(total_weight - 1) * extra[loc] if total_weight > 1 else 0)

        # 6500+ টাকায় free shipping
        if total >= 6500:
            shipping = 0

        grand_total = total + shipping

        order_user = request.user if request.user.is_authenticated else None

        order = Order.objects.create(
            user=order_user,
            full_name=full_name,
            phone=phone,
            address=address,
            order_total=grand_total,
            location=location,
            order_status='Pending',
            payment_type="cash on delivery",
        )

        if request.user.is_authenticated:
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                )
        else:
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price,
            )

        return redirect('backend:order_process', order_id=order.id)

    context = {
        'cart_items': cart_items,
        'total': total,
        'total_items': total_items,
        'total_weight': total_weight,
        'shipping': shipping,
        'grand_total': grand_total,
        'location': location,
        'product_id': request.GET.get('product_id', ''),
        'quantity': request.GET.get('quantity', 1),
    }

    return render(request, 'shop/checkout.html', context)

# order process
def order_process(request, order_id):

    if request.user.is_authenticated:
        order = Order.objects.get(id=order_id, user=request.user)
        # OrderItem আর create করব না — checkout এ হয়ে গেছে
        order_items = OrderItem.objects.filter(order=order)
        total = sum(item.price * item.quantity for item in order_items)

        # Cart clear করুন
        Cart.objects.filter(user=request.user).delete()

        items_details = ""
        for item in order_items:
            items_details += f"-{item.product.product_name} x {item.quantity} = {item.price * item.quantity}টাকা\n"

    else:
        order = Order.objects.get(id=order_id, user=None)
        order_items = OrderItem.objects.filter(order=order)
        total = sum(item.price * item.quantity for item in order_items)

        items_details = ""
        for item in order_items:
            items_details += f"-{item.product.product_name} x {item.quantity} = {item.price * item.quantity}টাকা\n"

    order.order_status = "Confirmed"
    order.save()
    try:
        send_mail(
            subject=f"নতুন অর্ডার #{order.id} - {order.full_name}",
            message=f"""নতুন অর্ডার এসেছে!
অর্ডার আইডি: {order.id}
গ্রাহক: {order.full_name}
ঠিকানা: {order.address}
 ফোন: {order.phone}

আইটেমস:
{items_details}
সাবটোটাল: {total}টাকা
শিপিং চার্জ: {order.order_total - total}টাকা
_____________
সর্বমোট: {order.order_total}টাকা
    """,
        from_email='alokkumarpaul22076@gmail.com',
        recipient_list=['alokkumarpaul22076@gmail.com'],
        fail_silently=True,
        )
    except Exception:
        pass

    
    messages.success(request, "আপনার অর্ডারটি সফলভাবে সম্পন্ন হয়েছে!")

    return render(request, 'shop/order_process.html', {
        'total': total,
        'order': order,
        'order_id': order_id,
    })


# payment processing 

# def payment_process(request, order_id):

#     order = Order.objects.get(id=order_id,user=request.user)

#     cart_items = Cart.objects.filter(user=request.user)

#     if not cart_items.exists():
#         messages.warning(request, "Your cart is empty.")
#         return redirect('backend:cart_list')

#     for item in cart_items:
#         OrderItem.objects.create(
#             order=order,
#             product=item.product,
#             quantity=item.quantity,
#             price=item.product.price,
#         )

#     cart_items.delete()

#     order.order_status = "Confirmed"
#     order.save()

#     messages.success(request, "Your order has been placed successfully!")
#     return redirect('backend:home')
    
# def payment_success(request):
#     messages.success(request, "Your payment was successful!")
#     return redirect('backend:home')
