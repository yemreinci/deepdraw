from django.urls import path
from web import views

urlpatterns = [
    path('', views.index, name='index'),
    path('train/', views.train, name='train'),
    path('train/<label>/', views.train, name='train'),
    path('test/', views.test, name='test'),
    path('login/', views.Login.as_view(), name='login'),
    path('images/<id>/data/', views.image_data, name='image_data'),
    path('images/<id>/', views.image, name='image_view'),
    path('images/<id>/delete/', views.image_delete),
    path('admin/stats/', views.stats, name='stats'),
]