from django.urls import path
from . import views
 

urlpatterns = [
    path('', views.home, name='home'),
    path('historia/', views.historia, name='historia'),
    path('servicios/', views.servicios, name='servicios'),
    path('destinos/', views.destinos, name='destinos'),
    path('preguntas/', views.preguntas, name='preguntas'),
    path('cotizacion/', views.cotizacion, name='cotizacion'),
    path('operaciones/', views.operaciones_dashboard, name='operaciones_dashboard'),
]