from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.shop, name = 'shop'),
    #Category views
    path('category/<cid>/', views.category_product_list_category_view, name='category-product-list'),

    #Vendor views
    path('vendors/<vid>/', views.vendor_detail_view, name='vendor-detail'),


    #Cart-related links
    path('cart/', views.cart, name = 'cart'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('delete_from_cart/', views.delete_item_from_cart, name='delete-from-cart'),
    path('update_cart/', views.update_cart, name='update-product-cart'),

    #Product view
    path('products/<pid>/', views.product_detailed_view, name = 'product-view'),

    #Searching and filtering
    path('tag/<tag_slug>/', views.tag_list, name='tags'),
    path('search/', views.search_view, name = 'search'),

    #Not yet
    path('checkout/<oid>/', views.checkout, name='checkout'),

    #PayPal Integration
    path('payment-completed/<oid>/', views.payment_completed, name='payment_completed'),
    path('payment-failed/', views.payment_failed, name='payment_failed'),
    path('paypal/', include('paypal.standard.ipn.urls'), name='paypal-ipn'),


    #New Routes
    path('save_checkout_info/', views.save_checkout_info, name='save_checkout_info'),
    path('api/create_checkout_session/<oid>/', views.create_checkout_session, name='create_checkout_session' )
]