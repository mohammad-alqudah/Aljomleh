
from django.urls import path

from . import views

urlpatterns = [
    #pages
	path('404', views.p404, name="store"),
	path('', views.index, name="index"),
    path('/<str:category>', views.index, name="index"),

	path('checkout', views.checkout, name="checkout"),
    path('order-success/<str:phone>', views.order_success, name="order-success"),
    path('wishlist', views.wishlist, name="wishlist"),
    path('brand/<str:brand>', views.brand, name="brand"),
    path('contact', views.contact, name="contact"),
	path('filter_', views.filter_, name="filter_"),




    #functions
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    # path('search/', views.search, name="search"),
    path('receive_note/', views.receive_note, name="receive_note"),
    path('updateWishList/', views.updateWishList, name="updateWishList"),


    #user
    path('login/', views.login, name="login"),
    path('logoutUser/', views.logoutUser, name="logoutUser"),
    path('loginPage', views.loginPage, name="loginPage"),
    path('signupPage', views.signupPage, name="signupPage"),
    path('signup', views.signup, name="signup"),





      



]