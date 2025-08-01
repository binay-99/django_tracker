
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('delete/<id>/',views.delete,name='delete_transaction'),
    path('edit/<id>',views.edit,name='edit_transaction')
]