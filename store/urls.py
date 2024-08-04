from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, DiscountViewSet, OrderViewSet, OrderDetailView, OrderItemViewSet, ProductDetailView, ProductViewSet

# Create routers for Order and Product ViewSets
routerOrder = DefaultRouter()
routerOrder.register(r'', OrderViewSet)

routerProduct = DefaultRouter()
routerProduct.register(r'', ProductViewSet)

routerOrderItem = DefaultRouter()
routerOrderItem.register(r'orderitems', OrderItemViewSet)

routerDiscount = DefaultRouter()
routerDiscount.register(r'discounts', DiscountViewSet)

routerCategory = DefaultRouter()
routerCategory.register(r'categories', CategoryViewSet)


urlpatterns = [
    path('orders/', include(routerOrder.urls)),
    path('orders/<int:order_id>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:order_id>/items/', OrderItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='orderitem-list'),
    path('', include(routerOrderItem.urls)),
    path('', include(routerDiscount.urls)),
    path('', include(routerCategory.urls)),
    path('products/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/', include(routerProduct.urls)),
]
