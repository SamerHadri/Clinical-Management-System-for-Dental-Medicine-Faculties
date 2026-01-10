from django.urls import path
from case.views import views

urlpatterns = [
    path('', view= views.case),
    path('<uuid:id>/', view= views.caseID),
    path('tooth/', view= views.tooth),
    path('tooth/<uuid:id>/', view= views.toothID),
]