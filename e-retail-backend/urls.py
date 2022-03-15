"""
author: varun
"""

from rest_framework import routers

from django.urls import path, include

from . import views

# routes for order app.

router = routers.DefaultRouter()
router.register(r'', views.OrderViewSet)

urlpatterns = [
    path('add/<str:id>/<str:token>/', views.add, name='order.add'),
    path('', include(router.urls)),
]
