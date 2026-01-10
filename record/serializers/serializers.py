from rest_framework import serializers
from record.models import Record, RecordTooth, RecordDisease, RecordMedication, Appointments
from users.models import User, StudentSubject
from medication.models import Medication
from case.models import Case, Tooth
from treatment.models import Treatment
from disease.models import Disease
from medication.models import Medication

#____________________________________________________________________________________Record_Patient_Notes
class RecordToothPatientNotesSeializer(serializers.Serializer):
    id = serializers.UUIDField(read_only = True)
    record = serializers.PrimaryKeyRelatedField(queryset = Record.objects.all(),write_only = True, required = False)
    tooth = serializers.PrimaryKeyRelatedField(queryset = Tooth.objects.all(),write_only = True)
    tooth_name = serializers.CharField(
        source = 'tooth.name',
        read_only = True
    )
    patient_notes = serializers.CharField(max_length = 1000)
    
    def create(self, validated_data):
        return RecordTooth.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.patient_notes += validated_data.get("patient_notes", instance.patient_notes) + " "
        instance.save()
        return instance

class RecordToothDoctorAddSerializer(serializers.Serializer):
    record = serializers.PrimaryKeyRelatedField(queryset = Record.objects.all(),write_only = True, required = False)
    tooth = serializers.PrimaryKeyRelatedField(queryset = Tooth.objects.all(),write_only = True)
    
    def create(self, validated_data):
        return RecordTooth.objects.create(**validated_data)

#____________________________________________________________________________________Record_Tooth
class RecordToothSerializer(serializers.Serializer):
    id = serializers.UUIDField(required = False)
    record = serializers.PrimaryKeyRelatedField(queryset = Record.objects.all(),write_only = True, required = False)
    patient_name = serializers.CharField(
        source = 'record.patient',
        read_only = True
    )
    tooth = serializers.PrimaryKeyRelatedField(queryset = Tooth.objects.all(),write_only = True, required = False)
    tooth_name = serializers.CharField(
        source = 'tooth.name',
        read_only = True
    )
    #___________________________________________________examination
    
    case = serializers.PrimaryKeyRelatedField(queryset = Case.objects.all(), write_only = True, required = False)
    case_name = serializers.CharField(
        source = 'case.name',
        read_only = True
    )
    examination_student=serializers.PrimaryKeyRelatedField(queryset = User.objects.all(),write_only = True, required = False)
    examination_student_name = serializers.CharField(
        source = 'examination_student.first_name',
        read_only = True
    )
    examination_subject = serializers.PrimaryKeyRelatedField(queryset = StudentSubject.objects.all(), write_only = True, required = False)
    examination_subject_name = serializers.CharField(
        source = 'examination_subject.subject',
        read_only = True
    )
    examination_supervisor = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), write_only = True, required = False)
    examination_supervisor_name = serializers.CharField(
        source = 'examination_supervisor.first_name',
        read_only = True
    )
    diagnosed = serializers.BooleanField(required = False)
    
    #___________________________________________________treatment
    
    treatment = serializers.PrimaryKeyRelatedField(queryset = Treatment.objects.all(), write_only = True, required = False)
    treatment_name = serializers.CharField(
        source = 'treatment.name',
        read_only = True
    )
    treatment_student=serializers.PrimaryKeyRelatedField(queryset = User.objects.all(),write_only = True, required = False)
    treatment_student_name = serializers.CharField(
        source = 'treatment_student.first_name',
        read_only = True
    )
    treatment_subject = serializers.PrimaryKeyRelatedField(queryset = StudentSubject.objects.all(), write_only = True, required = False)
    treatment_subject_name = serializers.CharField(
        source = 'treatment_subject.name',
        read_only = True
    )
    treatment_supervisor = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), write_only = True, required = False)
    treatment_supervisor_name = serializers.CharField(
        source = 'treatment_supervisor.first_name',
        read_only = True
    )
    treated = serializers.BooleanField(required = False)
    
    number_of_appointment = serializers.IntegerField(required = False)
    appointments_left = serializers.IntegerField(required = False)
    next_appointment = serializers.DateField(required = False)
    
    def update(self, instance, validated_data):
        instance.case = validated_data.get("case", instance.case)
        instance.examination_student = validated_data.get("examination_student", instance.examination_student)
        instance.examination_supervisor = validated_data.get("examination_supervisor", instance.examination_supervisor)
        instance.examination_subject = validated_data.get("examination_subject", instance.examination_subject)
        #____________________________________________________________________
        instance.treatment = validated_data.get("treatment", instance.treatment)
        instance.treatment_student = validated_data.get("treatment_student", instance.treatment_student)
        instance.treatment_supervisor = validated_data.get("treatment_supervisor", instance.treatment_supervisor)
        instance.treatment_subject = validated_data.get("treatment_subject", instance.treatment_subject)
        #____________________________________________________________________
        
        instance.save()
        return instance

#____________________________________________________________________________________Record_Disease/Record_Medication(Read)
class RecordDiseaseSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only = True)
    record = serializers.PrimaryKeyRelatedField(queryset = Record.objects.all(), write_only = True, required = False)
    disease = serializers.PrimaryKeyRelatedField(queryset = Disease.objects.all(), write_only = True)
    disease_name = serializers.CharField(
        source = 'disease.name',
        read_only = True
    )
    
    def create(self, validated_data):
        return RecordDisease.objects.create(**validated_data)

class RecordMedicationReadSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only = True)
    record = serializers.PrimaryKeyRelatedField(queryset = Record.objects.all(), write_only = True, required = False)
    medication = serializers.PrimaryKeyRelatedField(queryset = Medication.objects.all(), write_only = True)
    medication_name = serializers.CharField(
        source = 'medication.name',
        read_only = True
    )
    doses = serializers.IntegerField()
    still_active = serializers.BooleanField()
    date_of_last_dose = serializers.DateField()
    new_medication = serializers.BooleanField()

#____________________________________________________________________________________Record_Medication
class RecordMedicationExaminationSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only = True)
    record = serializers.PrimaryKeyRelatedField(queryset = Record.objects.all(),write_only = True, required = False)
    medication = serializers.PrimaryKeyRelatedField(queryset = Medication.objects.all(), write_only = True)
    medication_name = serializers.CharField(
        source = 'medication.name',
        read_only = True
    )
    doses = serializers.IntegerField()
    still_active = serializers.BooleanField()
    date_of_last_dose = serializers.DateField()
    new_medication = serializers.BooleanField(default = False)
    
    def create(self, validated_data):
        return RecordMedication.objects.create(**validated_data)

class RecordMedicationTreatmentSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only = True)
    record = serializers.PrimaryKeyRelatedField(queryset = Record.objects.all(),write_only = True, required = False)
    medication = serializers.PrimaryKeyRelatedField(queryset = Medication.objects.all(), write_only = True)
    medication_name = serializers.CharField(
        source = 'medication.name',
        read_only = True
    )
    doses = serializers.IntegerField()
    still_active = serializers.BooleanField(default = True)
    date_of_last_dose = serializers.DateField(default = None)
    new_medication = serializers.BooleanField(default = True)
    
    def create(self, validated_data):
        return RecordMedication.objects.create(**validated_data)


#____________________________________________________________________________________Appointment
class AppointmentsSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only = True)
    record_tooth = serializers.PrimaryKeyRelatedField(queryset = RecordTooth.objects.all())
    patient = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), required = False, write_only = True)
    patient_name = serializers.CharField(
        source = 'patient.first_name',
        read_only = True
    )
    patient_notes = serializers.CharField(
        source = 'record_tooth.patient_notes',
        read_only = True
    )
    student = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), write_only = True)
    student_name = serializers.CharField(
        source = 'student.first_name',
        read_only = True
    )
    type = serializers.CharField(max_length = 25)
    date = serializers.DateField()
    time = serializers.TimeField()
    status = serializers.CharField(max_length = 25, required = False)
    
    def create(self, validated_data):
        return Appointments.objects.create(**validated_data)

class AppointmentsStatusSerializer(serializers.Serializer):
    status = serializers.CharField(max_length = 25)
    notes = serializers.CharField(max_length = 500 , required =False)
    
    def update(self, instance, validated_data):
        instance.status = validated_data.get("status", instance.status)
        instance.notes = validated_data.get("notes", instance.notes)
        instance.save()
        return instance




#____________________________________________________________________________________Examin
class RecordExaminationUpdateSerializer(serializers.Serializer):
    importnace = serializers.IntegerField(required = False)
    notes = serializers.CharField(max_length = 500, required = False)
    
    diseases = RecordDiseaseSerializer(many = True, source = "RecordDiseases")
    medications = RecordMedicationExaminationSerializer(many = True, source = "RecordMedications")
    teeth = RecordToothSerializer(many = True, source = "RecordTeeth")
    
    def update(self, instance, validated_data):
        diseases:list = validated_data.pop('RecordDiseases')
        medications:list = validated_data.pop("RecordMedications")
        teeth:list = validated_data.pop("RecordTeeth")
        for disease in diseases:
            RecordDisease.objects.update_or_create(**disease, record = instance)
        for medication in medications:
            medication['new_medication'] = False
            med_id = medication['medication'].id
            if len(RecordMedication.objects.filter(medication_id =med_id)) == 0 :
                RecordMedication.objects.update_or_create(**medication, record = instance)
        for tooth in teeth:
            #there should be a better version of this
            if False: #'id' in tooth:
                print("please dont")
                record_tooth_id = tooth.get('id')
                RecordTooth.objects.update_or_create(
                id = record_tooth_id,
                defaults= tooth
                )
            else:
                tooth_id = tooth['tooth']
                tooth['record_id'] = instance.id
                case_id = tooth['case'].id
                if len(RecordTooth.objects.filter(case_id = case_id ,tooth_id = tooth_id)) == 0:
                    RecordTooth.objects.create(**tooth)
        instance.importance = validated_data.get("importance", instance.importance)
        instance.notes = validated_data.get("notes", instance.notes)
        instance.diagnosed = True
        instance.save()
        return instance

class ExaminApproveSerializer(serializers.Serializer):
    diagnosed = serializers.BooleanField(default = True, required = False)
    examination_supervisor = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), write_only = True)
    examination_supervisor_name = serializers.CharField(
        source = 'supervisor.name',
        read_only = True
    )
    def update(self, instance, validated_data):
        instance.diagnosed = validated_data.get("diagnosed", instance.diagnosed)
        instance.examination_supervisor = validated_data.get("examination_supervisor", instance.examination_supervisor)
        instance.save()
        return instance

#____________________________________________________________________________________Treatment
class RecordTreatmentUpdateSerializer(serializers.Serializer):
    importance = serializers.IntegerField(required = False)
    notes = serializers.CharField(max_length = 500, required = False)
    
    medications = RecordMedicationTreatmentSerializer(many = True, source = "RecordMedications")
    teeth = RecordToothSerializer(many = True, source = "RecordTeeth")
    def update(self, instance, validated_data):
        medications:list = validated_data.pop('RecordMedications')
        teeth:list = validated_data.pop("RecordTeeth")
        for medication in medications:
            medication['new_medication'] = True
            medication['still_active'] = True
            medication['date_of_last_dose'] = None
            med_id = medication['medication'].id
            print(med_id)
            if len(RecordMedication.objects.filter(medication_id =med_id)) == 0 :
                RecordMedication.objects.update_or_create(**medication, record = instance)
        for tooth in teeth:
            #there should be a better version of this
            record_tooth_id = tooth['id']
            tooth['appointments_left'] = tooth['number_of_appointment'] 
            RecordTooth.objects.filter(id = record_tooth_id).update(**tooth)
        instance.importance = validated_data.get("importance", instance.importance)
        instance.notes = validated_data.get("notes", instance.notes)
        instance.save()
        return instance

class TreatmentApproveSerializer(serializers.Serializer):
    treated = serializers.BooleanField(default = True, required = False)
    treatment_supervisor = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), write_only = True)
    treatment_supervisor_name = serializers.CharField(
        source = 'supervisor.name',
        read_only = True
    )
    def update(self, instance, validated_data):
        instance.treated = validated_data.get("treated", instance.treated)
        instance.treatment_supervisor = validated_data.get("treatment_supervisor", instance.treatment_supervisor)
        instance.save()
        return instance

class RecordTreatmentNextAppointmentSerializer(serializers.Serializer):
    next_appointment = serializers.DateField()
    appointments_left = serializers.IntegerField(required = False)
    
    def update(self, instance, validated_data):
        instance.next_appointment = validated_data.get("next_appointment", instance.next_appointment)
        instance.appointments_left -= 1
        instance.save()
        return instance

#____________________________________________________________________________________Record R/W
class RecordReadSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only = True)
    patient = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), write_only = True)
    patient_name = serializers.CharField(
        source = 'patient.first_name',
        read_only = True
    )
    importance = serializers.IntegerField()
    notes = serializers.CharField(max_length = 500)
    
    diseases = RecordDiseaseSerializer(many = True, source = "RecordDiseases")
    medications = RecordMedicationReadSerializer(many = True, source = "RecordMedications")
    teeth = RecordToothSerializer(many = True, source = "RecordTeeth")

class RecordCreateSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only = True)
    patient = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), write_only = True)
    patient_name = serializers.CharField(
        source = 'patient.first_name',
        read_only = True
    )
    importance = serializers.IntegerField(default = 0)
    notes = serializers.CharField(required = False)
    
    def create(self, validated_data):
        return Record.objects.create(**validated_data)
