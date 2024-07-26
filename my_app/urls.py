from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('registration',views.registration),
    path('login',views.login),
    path('logout',views.logout),
    path('dashboard',views.success),
    path('add_pie',views.add_pie),
    path('pies/edit/<int:id>',views.edit_pie),
    path('delete',views.remove_pie),
    path('pies',views.show_pies),
    path('pies/<int:id>/vote',views.vote),
    path('remove_delicious/<int:id>',views.remove_delicious),
    path('add_delicious/<int:id>',views.add_delicious)
    

]