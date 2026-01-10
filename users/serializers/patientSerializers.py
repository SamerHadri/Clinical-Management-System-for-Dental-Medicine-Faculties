from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User


#____________________________________________________________________________________Patient_R/W
class PatientCreateSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only = True)
    username = serializers.CharField(max_length = 25, validators = [UniqueValidator(queryset= User.objects.all())])
    password = serializers.CharField(max_length = 50, write_only = True)
    first_name = serializers.CharField(max_length = 25)
    last_name = serializers.CharField(max_length = 25)
    is_male = serializers.BooleanField()
    date_of_birth = serializers.DateField()
    national_number = serializers.CharField(max_length = 50)
    phone_number = serializers.CharField(max_length = 50)
    type = serializers.CharField(default = "Patient")
    
    is_active= serializers.BooleanField(default= True, write_only = True)
    is_superuser= serializers.BooleanField(default= False, write_only = True)
    is_staff = serializers.BooleanField(default = False, write_only = True)
    is_deleted = serializers.BooleanField(required = False, write_only = True)
    is_dark = serializers.BooleanField(default= False, write_only = True)
    language= serializers.CharField(default= 'en', max_length=3, write_only = True)
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class PatientReadSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 25)
    first_name = serializers.CharField(max_length = 25)
    last_name = serializers.CharField(max_length = 25)
    is_male = serializers.BooleanField()
    date_of_birth = serializers.DateField()