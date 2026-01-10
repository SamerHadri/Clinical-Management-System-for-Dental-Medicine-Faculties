from django.urls import path
from ..views import views

urlpatterns = [
    path('', view= views.medication),
    path('<uuid:id>/', view= views.medicationID),
]