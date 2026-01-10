from django.db import models
import uuid

from users.models import User, StudentSubject
from case.models import Case, Tooth
from treatment.models import Treatment
from disease.models import Disease
from medication.models import Medication



class Record(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="Records",
        related_query_name="Record"
    )
    register_date = models.DateField(auto_now_add=True)
    modify_date = models.DateField(auto_now=True)
    
    importance = models.IntegerField(default=0)
    notes = models.CharField(max_length=500)
    
    class Meta:
        db_table= "records"
    
    def __str__(self) -> str:
        return f"{self.patient.first_name} {self.patient.last_name} record"

class RecordTooth(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    record = models.ForeignKey(
        Record,
        on_delete=models.DO_NOTHING,
        related_name="RecordTeeth",
        related_query_name="RecordTooth"
    )
    tooth = models.ForeignKey(
        Tooth,
        on_delete=models.DO_NOTHING,
        related_name="RecordTeeth",
        related_query_name="RecordTooth"
    )
    patient_notes = models.CharField(max_length = 1000, null = True)
    
    #___________________________________________________examination
    
    case = models.ForeignKey(
        Case,
        on_delete=models.DO_NOTHING,
        related_name="RecordCases",
        related_query_name="RecordCase",
        null=True
    )
    examination_student = models.ForeignKey(
        User,
        on_delete= models.DO_NOTHING,
        related_name="ExaminationStudents",
        related_query_name="ExaminationStudent",
        null=True
    )
    examination_supervisor= models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="ExaminationSupervisors",
        related_query_name="ExaminationSupervisor",
        null= True
    )
    examination_subject = models.ForeignKey(
        StudentSubject,
        on_delete=models.DO_NOTHING,
        related_name="ExaminationSubjects",
        related_query_name="ExaminationSubject",
        null=True
    )
    diagnosed = models.BooleanField(default=False)
    
    #___________________________________________________treatment
    
    treatment = models.ForeignKey(
        Treatment,
        on_delete=models.DO_NOTHING,
        related_name="RecordTreatments",
        related_query_name="RecordTreatment",
        null=True
    )
    
    treatment_student = models.ForeignKey(
        User,
        on_delete= models.DO_NOTHING,
        related_name="TreatmentStudents",
        related_query_name="TreatmentStudent",
        null=True
    )
    treatment_supervisor = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="TreatmentSupervisors",
        related_query_name="TreatmentSupervisor",
        null= True
    )
    treatment_subject = models.ForeignKey(
        StudentSubject,
        on_delete=models.DO_NOTHING,
        related_name="TreatmentSubjects",
        related_query_name="TreatmentSubject",
        null=True
    )
    treated = models.BooleanField(default=False)
    
    number_of_appointment = models.IntegerField(null = True)
    appointments_left = models.IntegerField(null = True)
    next_appointment = models.DateField(null = True)
    
    class Meta:
        db_table= "RecordTooth"

class RecordDisease(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    record = models.ForeignKey(
        Record,
        on_delete=models.DO_NOTHING,
        related_name="RecordDiseases",
        related_query_name="RecordDisease"
    )
    disease = models.ForeignKey(
        Disease,
        on_delete=models.DO_NOTHING,
        related_name="RecordDiseases",
        related_query_name="RecordDisease"
    )
    class Meta:
        db_table= "RecordDisease"
        
        unique_together =[
            ['record', 'disease']
        ]

class RecordMedication(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    record = models.ForeignKey(
        Record,
        on_delete=models.DO_NOTHING,
        related_name="RecordMedications",
        related_query_name="RecordMedication"
    )
    medication = models.ForeignKey(
        Medication,
        on_delete=models.DO_NOTHING,
        related_name="RecordMedications",
        related_query_name="RecordMedication"
    )
    doses = models.IntegerField()
    still_active = models.BooleanField()
    date_of_last_dose = models.DateField(null = True)
    new_medication = models.BooleanField()
    class Meta:
        db_table= "RecordMedication"
        
        unique_together =[
            ['record', 'medication']
        ]





class Appointments(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="PatientAppointments",
        related_query_name="PatientAppointment"
    )
    record_tooth = models.ForeignKey(
        RecordTooth,
        on_delete=models.DO_NOTHING,
        related_name="PatientAppointments",
        related_query_name="PatientAppointment"
    )
    student = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="StudentAppointments",
        related_query_name="StudentAppointment"
    )
    type = models.CharField(max_length = 25, choices = [("E", "Examination"),("T", "Treatment")])
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length = 25, choices = [("P", "Pending"), ("A", "Approved"), ("F", "Finished"), ("C", "Cancelled")], default = "Pending")
    notes = models.CharField(max_length=500, blank= True)
    class Meta:
        db_table= "Appointments"
