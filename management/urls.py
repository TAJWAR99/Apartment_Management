from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('login/',views.loginPage,name="login"),
    path('logOut',views.logOut,name="logOut"),
    path('register/',views.register,name="register"),
    path('bills/',views.bills,name="bills"),
    path('update/<str:pk>/',views.update,name="update"),
    path('delete/<str:pk>/',views.deleteOwner,name="delete"),
    path('bill-info/<str:key>/',views.bill_info,name="bill-info"),
    path('payment/',views.payment,name="payment"),
    path('update_payment/<str:pk>/',views.update_payment,name="update_payment"),
    path('delete_payment/<str:pk>/',views.delete_payment,name="delete_payment"),
    path('view/<str:pk>/',views.view,name="view"),
    
]
