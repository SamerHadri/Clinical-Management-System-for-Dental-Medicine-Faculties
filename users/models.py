from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
import uuid

from subject.models import Department,Subject


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(validators=[UnicodeUsernameValidator], max_length = 25, unique=True)
    first_name = models.CharField(max_length = 25)
    last_name = models.CharField(max_length = 25)
    is_male = models.BooleanField(default=True)
    date_of_birth = models.DateField(null = True)
    type = models.CharField(max_length = 25, choices = [("P", "Patient"),("ST", "Student"), ("SU", "Supervisor"),("C", "CEO"), ("D", "Developer")],default="Developer")
    
    email= models.EmailField(max_length = 25, null = True)
    #patient data
    national_number = models.CharField(max_length = 50, null = True)
    phone_number = models.CharField(max_length = 50, null = True)
    #student data
    university_number = models.CharField(max_length = 9, null = True)
    academic_year = models.IntegerField(null = True)
    #supervisor data
    department = models.ForeignKey(Department, on_delete = models.DO_NOTHING, related_name="Users", related_query_name="User", null = True)
    
    is_active= models.BooleanField(default= True)
    is_superuser= models.BooleanField(default= False)
    is_staff = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    
    is_dark = models.BooleanField(default= False)
    language= models.CharField(default= 'en', max_length=3)
    
    objects= UserManager()
    USERNAME_FIELD= "username"
    Email_Field= "email"
    
    class Meta:
        db_table= "users"
    
    def __str__(self) -> str:
        return self.username

class StudentSubject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="StudentSubjects",
        related_query_name="StudentSubject"
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.DO_NOTHING,
        related_name="StudentSubjects",
        related_query_name="StudentSubject"
    )
    supervisor = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="SupervisortSubjects",
        related_query_name="SupervisorSubject",
        null = True
    )
    completed = models.BooleanField(default=False)
    mark = models.IntegerField(default = -1)
    notes = models.CharField(max_length=250,null = True)
    is_deleted = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
    
    class Meta:
        db_table= "studentsubject"
    
    def __str__(self) -> str:
        return self.student.first_name + " " + self.student.last_name + ":" + self.subject.name
