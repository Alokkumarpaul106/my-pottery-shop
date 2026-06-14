from ..models import Product,Category
from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q


# shows all products with pagination and filtering options
def product_list(request):
    products=Product.objects.all()
    categories=Category.objects.all()
    category=request.GET.get('category')
    min_price=request.GET.get('min_price')
    max_price=request.GET.get('max_price')
    search=request.GET.get('search')
    sort=request.GET.get('sort')
# search query থাকলে product_name এ search করবে, না থাকলে সব product দেখাবে
    q = request.GET.get('q', '')
    if q:
        products = Product.objects.filter(
            product_name__icontains=q,
            available=True
        )
    else:
        products = Product.objects.filter(available=True)



    if category:
        products=products.filter(category__slug=category)
    if min_price:
        products=products.filter(price__gte=min_price)
    if max_price:
        products=products.filter(price__lte=max_price)
    if search:
        products=products.filter(product_name__icontains=search)
    
    if sort == 'low':
        products = products.order_by('price')

    elif sort == 'high':
        products = products.order_by('-price')

    elif sort == 'latest':
        products = products.order_by('-id')

    paginator = Paginator(products, 6) # প্রতি page এ 6টা 
    page_number = request.GET.get('page') 
    products = paginator.get_page(page_number)

    return render(request,'shop/product_list.html',{
        'products':products,
        'categories':categories,
        'q':q,
        
       })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    images = product.images.all()

    search_term =product.product_name.split()[0]

    related_products = Product.objects.filter(
        product_name__icontains=search_term,
        available=True
    ).exclude(id=product.id)[:4]

    if not related_products.exists():
        related_products = Product.objects.filter(
            category=product.category,
            available=True
        ).exclude(id=product.id)[:4]

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'images': images,
        'product_details': product.product_details,
        'related_products': related_products,
    })

#category wise product listing 
def category_products(request, slug):
    category = Category.objects.get(slug=slug)
    products = Product.objects.filter(category=category,available="True")[:6]
    
    return render(request, 'shop/category_products.html', {
        'category': category,
        'products': products,
        
    })
