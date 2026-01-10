from django.urls import path
from ..views import views

urlpatterns = [
    path('', view= views.index),
    path('<uuid:id>/', view= views.indexID),
]