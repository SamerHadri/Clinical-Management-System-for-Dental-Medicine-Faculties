from django.urls import path
from record.views import views, patientviews, studentviews, supervisorviews

urlpatterns = [
    path('', view=views.record),
    path('<uuid:id>/', view=views.recordID),
    path('tooth/', view=views.recordtooth),
    path('notexamined/', view=views.notexamined),
    path('examined/', view=views.examined),
    path('examined/approved/', view=views.examinedapproved),
    path('treated/', view=views.treated),
    path('treated/approved/', view=views.treatedapproved),
]

#patient urls
urlpatterns +=[
    path('Pnotes/', view=patientviews.patientnotes)#save the patient ideas and troubles
]

#student urls
urlpatterns +=[
    path('student/', view= studentviews.studentrecordtooth), #record tooth
    path('examin/<uuid:id>/', view= studentviews.examin),#examin the patient
    path('treatment/<uuid:id>/', view= studentviews.treatment),#treat the patient
    path('treatment/nextappointment/<uuid:id>/', view= studentviews.nextappointment) #book the appointment
    
]

#supervisor urls
urlpatterns +=[
    path('examin/approve/<uuid:id>/', view= supervisorviews.examinapprove),#approve the examination
    path('treatment/approve/<uuid:id>/', view= supervisorviews.treatmentapprove)#approve the treatment
]