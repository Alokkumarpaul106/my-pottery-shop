from ..models import Product,Category,Customer,Order
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required



# shows home page with 8 products and all categories
def home(request):
    products = Product.objects.filter(available=True)[:8]  
    categories=Category.objects.all()
    

    context = {
        'products': products,
        'categories': categories,
        
    }
    return render(request, 'shop/home.html', context)

# category

def category(request):
    categories=Category.objects.all()
    return render(request,'shop/category.html',{
        'categories': categories
        })

# new arrival

def new_arrival(request):
    products=Product.objects.filter(available="True")[:8]
    return render(request,'shop/new_arrival.html',{
        'products':products
    })




# profile and logout process

@login_required(login_url='/login/')
def profile(request):
    tab=request.GET.get('tab')
    customer,created=Customer.objects.get_or_create(user=request.user)
    orders = Order.objects.filter(user=request.user).order_by('-created_date')
    total_orders = orders.count()
    total_spent = sum(order.order_total for order in orders)
    order_history_active=(tab=='order')
    
    return render(request,'shop/profile.html',{
        "customer":customer,
        "orders":orders,
        "total_orders":total_orders,
        "total_spent":total_spent,
        "order_history_active":order_history_active,
                
    })