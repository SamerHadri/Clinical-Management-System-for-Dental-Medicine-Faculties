from rest_framework import serializers
from users.models import User, StudentSubject
from subject.models import Subject
from subject.serializers.serializers import SubjectSerializer
from record.serializers.serializers import RecordReadSerializer

#____________________________________________________________________________________Student_R/W
class StudentCreateSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only = True)
    username = serializers.CharField(max_length = 25)
    password = serializers.CharField(max_length = 50, write_only = True)
    first_name = serializers.CharField(max_length = 25)
    last_name = serializers.CharField(max_length = 25)
    is_male = serializers.BooleanField()
    date_of_birth = serializers.DateField()
    email = serializers.EmailField(max_length = 25)
    type = serializers.CharField(default = "Student")
    
    university_number = serializers.CharField(max_length = 9)
    academic_year = serializers.IntegerField(default = 1)
    
    national_number = serializers.CharField(max_length = 50, required = False)
    phone_number = serializers.CharField(max_length = 50, required = False)
    
    is_active= serializers.BooleanField(default= True, write_only = True)
    is_superuser= serializers.BooleanField(default= False, write_only = True)
    is_staff = serializers.BooleanField(default = False, write_only = True)
    is_dark = serializers.BooleanField(default= False, write_only = True)
    language= serializers.CharField(default= 'en', max_length=3, write_only = True)
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class PrivateStudentReadSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 25)
    first_name = serializers.CharField(max_length = 25)
    last_name = serializers.CharField(max_length = 25)
    is_male = serializers.BooleanField()
    date_of_birth = serializers.DateField()
    academic_year = serializers.IntegerField()
    email = serializers.EmailField(max_length = 25)
    university_number = serializers.CharField(max_length = 9)
    
    national_number = serializers.CharField(max_length = 50)
    phone_number = serializers.CharField(max_length = 50)


class PublicStudentReadSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 25)
    first_name = serializers.CharField(max_length = 25)
    last_name = serializers.CharField(max_length = 25)
    is_male = serializers.BooleanField()
    academic_year = serializers.IntegerField()
    type = serializers.CharField()



#____________________________________________________________________________________StudentSubject_R/W
class StudentSubjectCreateSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only = True)
    student = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), write_only = True)
    student_name = serializers.CharField(
        source = 'student.name',
        read_only = True
    )
    subject = serializers.PrimaryKeyRelatedField(queryset = Subject.objects.all(),write_only = True)
    subject_name = serializers.CharField(
        source = 'subject.name',
        read_only = True
    )
    completed = serializers.BooleanField(default = False)
    mark = serializers.IntegerField(default = -1)
    notes = serializers.CharField(max_length = 250, required = False)
    
    def create(self, validated_data):
        return StudentSubject.objects.create(**validated_data)

class StudentSubjectReadSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only = True)
    student = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), write_only = True)
    student_name = serializers.CharField(
        source = 'student.first_name',
        read_only = True
    )
    subject = serializers.PrimaryKeyRelatedField(queryset = Subject.objects.all(),write_only = True)
    subject_name = serializers.CharField(
        source = 'subject.name',
        read_only = True
    )
    subject_academic_year = serializers.CharField(
        source = 'subject.academic_year',
        read_only = True
    )
    subject_academic_term = serializers.CharField(
        source = 'subject.academic_term',
        read_only = True
    )
    completed = serializers.BooleanField()
    mark = serializers.IntegerField()
    notes = serializers.CharField(max_length = 250)
