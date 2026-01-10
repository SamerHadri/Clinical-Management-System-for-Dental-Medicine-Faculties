from django.urls import path
from subject.views import views

urlpatterns = [
    path('', view=views.subject),
    path('<uuid:id>/', view=views.subjectID),
    path('department/', view=views.department),
    path('department/<uuid:id>/', view=views.departmentID)
]