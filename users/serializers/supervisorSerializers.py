from rest_framework import serializers
from users.models import User
from subject.models import Subject, Department

class SupervisorCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 25)
    password = serializers.CharField(max_length = 50, write_only = True)
    first_name = serializers.CharField(max_length = 25)
    last_name = serializers.CharField(max_length = 25)
    is_male = serializers.BooleanField()
    date_of_birth = serializers.DateField()
    email = serializers.EmailField(max_length = 25,required = False)
    type = serializers.CharField(default = "Supervisor")
    university_number = serializers.CharField(max_length = 9 , required = False)
    department = serializers.PrimaryKeyRelatedField(queryset = Department.objects.all(), write_only = True)
    department_name = serializers.CharField(
        source = 'department.name',
        read_only = True
    )
    
    is_active= serializers.BooleanField(default= True, write_only = True)
    is_superuser= serializers.BooleanField(default= False, write_only = True)
    is_staff = serializers.BooleanField(default = True, write_only = True)
    is_deleted = serializers.BooleanField(default = False, write_only = True)
    is_dark = serializers.BooleanField(default= False, write_only = True)
    language= serializers.CharField(default= 'en', max_length=3, write_only = True)
    
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class PrivateSupervisorReadSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 25)
    first_name = serializers.CharField(max_length = 25)
    last_name = serializers.CharField(max_length = 25)
    is_male = serializers.BooleanField()
    date_of_birth = serializers.DateField()
    email = serializers.EmailField(max_length = 25)
    type = serializers.CharField(default = "Supervisor")
    university_number = serializers.CharField(max_length = 9)
    department = serializers.PrimaryKeyRelatedField(queryset = Department.objects.all(),write_only = True)
    
    is_active= serializers.BooleanField(default= True)
    is_superuser= serializers.BooleanField(default= False)
    is_staff = serializers.BooleanField(default = False)
    is_deleted = serializers.BooleanField(required = False)
    is_dark = serializers.BooleanField(default= False)
    language= serializers.CharField(default= 'en', max_length=3)

class PublicSupervisorReadSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 25)
    department = serializers.CharField(source = 'department.name')

class ChangeStudentMarksSerializer(serializers.Serializer):
    student_first_name = serializers.CharField(
        source = 'student.first_name',
        read_only = True
    )
    student_last_name = serializers.CharField(
        source = 'student.last_name',
        read_only = True
    )
    supervisor = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), write_only = True)
    supervisor_first_name = serializers.CharField(
        source = 'supervisor.first_name',
        read_only = True
    )
    supervisor_last_name = serializers.CharField(
        source = 'supervisor.last_name',
        read_only = True
    )
    subject_name = serializers.CharField(
        source = 'subject.name',
        read_only = True
    )
    mark = serializers.IntegerField()
    completed = serializers.BooleanField(required = False)
    
    def update(self, instance, validated_data):
        instance.mark = validated_data.get("mark", instance.mark)
        instance.supervisor = validated_data.get("supervisor", instance.supervisor)
        instance.completed = validated_data.get("completed", instance.completed)
        instance.save()
        return instance