import math
from backend.models import Cart,Product
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# shows cart items and total price


def cart_list(request):
    cart_items=Cart.objects.filter(user=request.user)
    cart_count=cart_items.count()
    total_items = sum(item.quantity for item in cart_items)
    total = 0
    total_weight=0
    for item in cart_items:
        item.total_price = item.product.price * item.quantity
        item.total_weight = (item.product.weight or 0) * item.quantity # weight calculation
        total += item.total_price
        total_weight += item.total_weight

# if total  in cart is 6500 or more, shipping is free otherwise 60 tk
    if total_weight <= 1:
        shipping = 70
    else:
        shipping = 70 + (math.ceil(total_weight - 1) * 20)

    # 6500+ টাকায় free shipping
    if total >= 6500:
        shipping = 0

    grand_total = total + shipping

    return render(request,'shop/cart_list.html',{
        'cart_items':cart_items,
        'cart_items_count':cart_count,
        'total':total,
        'total_items':total_items,
        'total_weight': total_weight,
        'shipping':shipping,
        'grand_total':grand_total,
        
    })


# adds product to cart or updates quantity if already in cart
@login_required(login_url='/login/')
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity') or 1)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 0}
    )   
    new_qty = cart_item.quantity + quantity

    if new_qty > product.stock:
        messages.error(request, f"স্টকে শুধুমাত্র {product.stock} টি পণ্য আছে !")
        return redirect(request.META.get('HTTP_REFERER'))

    cart_item.quantity = new_qty
    cart_item.save()

    messages.success(request, f"{product.product_name} কার্টে যোগ করা হয়েছে।")
    return redirect(request.META.get('HTTP_REFERER'))
    


# removes item from cart
@login_required(login_url='/login/')
def cart_remove(request,cart_item_id):
    cart_item=get_object_or_404(Cart,id=cart_item_id,user=request.user)
    cart_item.delete()
    messages.success(request, f"{cart_item.product.product_name} কার্ট থেকে সরিয়ে ফেলা হয়েছে।")
    return redirect('backend:cart_list')


# updates cart item quantity
@login_required(login_url='/login/')
def update_cart(request, item_id):
    item = Cart.objects.get(id=item_id, user=request.user)

    if request.method == "POST":
        qty = request.POST.get('quantity')

        if qty:
            qty = int(qty)

            # quantity change হলে তবেই update
            if item.quantity != qty:
                item.quantity = qty
                item.save()

                messages.success( request,f"{item.product.product_name} quantity updated.")
            else:
                messages.info(request,"Quantity already same")

    return redirect('backend:cart_list')
