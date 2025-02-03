from inventory import views
from django.urls import path

urlpatterns = [
    path('items/', views.manage_item),
    path('items/<int:id>', views.manage_item),
    
    path('customers/', views.manage_customer),
    path('customers/<int:id>', views.manage_customer),
    
    path('orders/', views.manage_order),
    path('orders/<int:id>', views.manage_order),
    
    path('suppliers/', views.manage_supplier),
    path('suppliers/<int:id>', views.manage_supplier),
]
