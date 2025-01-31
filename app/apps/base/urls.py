from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
    path('', views.load_form, name='app_base'),
    path('grafico/', views.plot_view, name='grafico'),

]