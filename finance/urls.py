from django.contrib import admin
from django.urls import path
from app1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.dashboard,name = 'home'),
    path('transactions/',views.all_transaction,name = 'transactions'),
     path('auth/', views.signup_view, name='auth'),
    path('add_transaction/',views.add_Transaction,name = 'addTransaction'),
]
