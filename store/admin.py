from django.contrib import admin
from .models import Category, Discount, Product, ProductImage, Order, OrderItem

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3  # Number of empty forms to display

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ['name', 'price', 'created_at', 'updated_at']
    search_fields = ['name', 'description']
    filter_horizontal = ('categories',) 

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Number of empty forms to display
    readonly_fields = ['product', 'quantity', 'price', 'customization_details']

    def get_fields(self, request, obj=None):
        return ['product', 'quantity', 'price', 'customization_details']

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields
    
class DiscountInline(admin.TabularInline):
    model = Discount
    extra = 1  # Number of empty forms to display
    readonly_fields = ['code', 'description', 'discount_amount', 'discount_percentage', 'start_date', 'end_date', 'is_active']

    def get_fields(self, request, obj=None):
        return ['code', 'description', 'discount_amount', 'discount_percentage', 'start_date', 'end_date', 'is_active']

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields
    
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ['id', 'customer', 'created_at', 'status', 'total_amount', 'currency']
    search_fields = ['customer__user__username', 'status']
    list_filter = ['status', 'created_at']

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity', 'price', 'customization_details']
    search_fields = ['order__id', 'product__name']
    list_filter = ['order', 'product']

class DiscountAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'order_item', 'code', 'description', 'discount_amount', 'discount_percentage', 'start_date', 'end_date', 'is_active']
    search_fields = ['order__id', 'code', 'description']
    list_filter = ['start_date', 'end_date', 'is_active']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'created_at', 'updated_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at', 'updated_at']

# Register models with admin
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)  # Register ProductImage for standalone access if needed
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)  # Register OrderItem for standalone access if needed
admin.site.register(Discount, DiscountAdmin) 
