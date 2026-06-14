
from backend.models import Cart
def cart_item_count(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        total_items = sum(item.quantity for item in cart_items)
    else:
        total_items = 0
    return {'cart_item_count': total_items}