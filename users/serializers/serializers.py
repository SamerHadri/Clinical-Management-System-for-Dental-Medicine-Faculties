from rest_framework import serializers
from users.models import User
from subject.models import Department

#____________________________________________________________________________________Token
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 25)
    password = serializers.CharField(max_length = 50)

class UserInfoSerializer(serializers.Serializer):
    token = serializers.CharField(max_length = 50)
    id = serializers.CharField(max_length = 25)
    type = serializers.CharField(max_length = 10)



#____________________________________________________________________________________CEO
class CEOCreateSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only = True)
    username = serializers.CharField(max_length = 25)
    password = serializers.CharField(max_length = 50, write_only = True)
    first_name = serializers.CharField(max_length = 25)
    last_name = serializers.CharField(max_length = 25)
    is_male = serializers.BooleanField(required = False)
    date_of_birth = serializers.DateField(required = False)
    email = serializers.EmailField(max_length = 25,required = False)
    type = serializers.CharField(default = "CEO")
    
    is_active= serializers.BooleanField(default= True, write_only = True)
    is_superuser= serializers.BooleanField(default= False, write_only = True)
    is_staff = serializers.BooleanField(default = True, write_only = True)
    is_dark = serializers.BooleanField(default= False, write_only = True)
    language= serializers.CharField(default= 'en', max_length=3, write_only = True)
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class PrivateCEOReadSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 25)
    first_name = serializers.CharField(max_length = 25)
    last_name = serializers.CharField(max_length = 25)
    is_male = serializers.BooleanField(required = False)
    date_of_birth = serializers.DateField(required = False)
    email = serializers.EmailField(max_length = 25,required = False)
    type = serializers.CharField(default = "CEO")
    
    is_active= serializers.BooleanField(default= True)
    is_superuser= serializers.BooleanField(default= False)
    is_staff = serializers.BooleanField(default = True)
    is_dark = serializers.BooleanField(default= False)
    language= serializers.CharField(default= 'en', max_length=3)

class PublicCEOReadSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 25)


#____________________________________________________________________________________User
class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only = True)
    username = serializers.CharField(max_length = 25)
    password = serializers.CharField(max_length = 50, write_only = True)
    first_name = serializers.CharField(max_length = 25)
    last_name = serializers.CharField(max_length = 25)
    is_male = serializers.BooleanField(required = False)
    date_of_birth = serializers.DateField(required = False)
    email = serializers.EmailField(max_length = 25,required = False)
    type = serializers.CharField(required = False)
    national_number = serializers.CharField(max_length= 50, required = False)
    phone_number = serializers.CharField(max_length = 50, required = False)
    university_number = serializers.CharField(max_length = 9, required = False)
    academic_year = serializers.IntegerField(required = False)
    department = serializers.PrimaryKeyRelatedField(queryset = Department.objects.all(), required = False)
    department_name = serializers.CharField(
        source = 'department.name',
        read_only = True
    )
    is_active= serializers.BooleanField(default= True)
    is_superuser= serializers.BooleanField(default= False)
    is_staff = serializers.BooleanField(default = False)
    is_deleted = serializers.BooleanField(required = False)
    is_dark = serializers.BooleanField(default= False)
    language= serializers.CharField(default= 'en', max_length=3)
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class ChangePasswordSerializer(serializers.Serializer):
    old_password= serializers.CharField(
        max_length= 250
    )
    new_password= serializers.CharField(
        max_length= 250
    )
    confirm_new_password= serializers.CharField(
        max_length= 250
    )
