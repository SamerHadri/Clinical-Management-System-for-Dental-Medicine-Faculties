from django.urls import path
from users.views import views, patientView, studentView, supervisorView

urlpatterns = [
    path('', view=views.index),
    path('<uuid:id>/', view=views.indexID),
    path('userlogin/', view=views.userlogin),
    path('ceo/', view=views.ceo),
    path('ceo/<uuid:id>/', view=views.ceoID)
]

urlpatterns +=[
    path('patient/', view=patientView.patient),
    path('patient/create/', view=patientView.createpatient),
    path('patient/<uuid:id>/', view=patientView.patientID),
    path('patient/appointment/', view=patientView.patientappointment),
    path('patient/appointment/pending/', view=patientView.patientpendingappointment),
    path('patient/appointment/<uuid:id>/', view=patientView.patientappointmentID)
]

urlpatterns += [
    path('student/', view=studentView.student),
    path('student/<uuid:id>/', view=studentView.studentID),
    path('studentsubject/', view=studentView.studentsubject),
    path('studentsubject/<uuid:id>/', view=studentView.studentsubjectID),
    path('student/appointment/', view=studentView.studentappointment),
    path('student/appointment/approved/', view=studentView.approvedstudentappointment)
]

urlpatterns +=[
    path('supervisor/', view=supervisorView.supervisor),
    path('supervisor/<uuid:id>/', view=supervisorView.supervisorID),
    path('supervisor/changemarks/<uuid:id>/', view=supervisorView.supervisorstudentmarks)
]

