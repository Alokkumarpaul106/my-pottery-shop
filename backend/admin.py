from django.contrib import admin
from .models import Category,Cart,Customer,Payment,Product,Product_image,Order,OrderItem,Review


class ProductImageInline(admin.TabularInline):
    model = Product_image
    extra = 4  # Admin এ 4টা empty slot দেখাবে


#Product Admin এ Inline যোগ
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ['product_name', 'order']
    list_editable = ['order']  # Admin এ order field কে editable করবে

admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Payment)
admin.site.register(Product_image)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_username', 'full_name', 'phone', 'order_status', 'order_total']

    def get_username(self, obj):
        if obj.user:
            return obj.user.username
        return 'Guest'  # ✅ user None হলে Guest দেখাবে
    
    get_username.short_description = 'User'
    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity', 'price']

admin.site.register(Review)

