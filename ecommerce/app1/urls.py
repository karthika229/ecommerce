from django.urls import path
from . import views


urlpatterns = [
   
     path('',views.guest,name="guest"),
     path('loginpage',views.loginpage,name="loginpage"),
     path('customerreg',views.customerreg,name="customerreg"),
     path('custregdetails',views.custregdetails,name="custregdetails"),
     path('adminhome',views.adminhome,name="adminhome"),
     path('userlog',views.userlog,name="userlog"),
     path('home',views.home,name="home"),
     path('addcat',views.addcat,name="addcat"),
     path('catdetails',views.catdetails,name="catdetails"),
     path('addpro',views.addpro,name="addpro"),
     path('prodetails',views.prodetails,name="prodetails"),
     path('viewproduct',views.viewproduct,name="viewproduct"),
     path('editproduct/<int:pk>/', views.editproduct, name='editproduct'),
     path('editprodetails/<int:pk>/', views.editprodetails, name='editprodetails'),
     path('viewcat',views.viewcat,name="viewcat"),
     path('editcat/<int:pk>/', views.editcat, name='editcat'),
     path('editcatdetails/<int:pk>/', views.editcatdetails, name='editcatdetails'),
     path('manageuser',views.manageuser,name="manageuser"),
     path('category_product/<int:category_id>/',views.category_product, name='category_product'),
     path('add-to-cart/<int:id>', views.add_to_cart, name='add_to_cart'),
     path('view_cart', views.view_cart, name='view_cart'),
     path('remove-cart-item/<int:item_id>', views.remove_cart_item, name='remove_cart_item'),
     path('update-cart-item/<int:item_id>', views.update_cart_item, name='update_cart_item'),
     path('card',views.card,name="card"),
     path('edituser',views.edituser,name="edituser"),
     path('update_user/<int:pk>',views.update_user,name="update_user"),
     # path('cartcount',views.cartcount,name="cartcount"),
     path('about',views.about,name="about"),
     path('deleteproduct/<int:pk>',views.deleteproduct,name="deleteproduct"),
      path('deletecat/<int:pk>',views.deletecat,name="deletecat"),
     path('deleteuser/<int:pk>',views.deleteuser,name="deleteuser"),
     path('logout',views.logout,name="logout"),
     

]