

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import HttpRequest, Request
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from users.models import User, StudentSubject
from record.models import Appointments, RecordTooth, Record
from subject.models import Subject
from users.serializers.serializers import UserSerializer
from record.serializers.serializers import AppointmentsSerializer
from users.serializers.studentSerializers import StudentCreateSerializer, PublicStudentReadSerializer, PrivateStudentReadSerializer, StudentSubjectCreateSerializer, StudentSubjectReadSerializer
import uuid

from rest_framework.authtoken.models import Token
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: PrivateStudentReadSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
)
@swagger_auto_schema(
    method= 'POST',
    responses={
        status.HTTP_200_OK: StudentCreateSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
    request_body=StudentCreateSerializer()
)
@api_view(['GET', 'POST'])
def student(request:Request|HttpRequest)->Response:
    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 10
        student = User.objects.filter(type__exact = "Student").order_by("first_name")
        if request.user.type in ['Patient', 'Student']:
            student = student.filter(is_deleted = False)
            paginated_students = paginator.paginate_queryset(student, request)
            ser = PublicStudentReadSerializer(paginated_students, many = True)
        elif request.user.type in ['Supervisor', 'CEO']:
            student = student.filter(is_deleted = False)
            paginated_students = paginator.paginate_queryset(student, request)
            ser = PrivateStudentReadSerializer(paginated_students, many = True)
        elif request.user.type in ['Developer']:
            paginated_students = paginator.paginate_queryset(student, request)
            ser = UserSerializer(paginated_students, many = True)
        return Response(data = ser.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        try:
            user = User.objects.get(username = request.data['username'])
            return Response(data="username already exists", status=status.HTTP_409_CONFLICT)
        except:
            if request.user.type in ['Patient', 'Student']:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            reqSer = StudentCreateSerializer(data = request.data)
            if reqSer.is_valid():
                reqSer.save()
                user = User.objects.get(username = request.data['username'])
                subjects = Subject.objects.filter(academic_year = 1)
                for subject in subjects:
                    reqSer = StudentSubjectCreateSerializer(data= {"student":user.id, "subject":subject.id})
                    if reqSer.is_valid():
                        reqSer.save()
                
                usertoken, created = Token.objects.get_or_create(user= user)
                return Response(data={ 
                            'token': usertoken.key,
                            'id': user.pk,
                            'type': user.type
                        }, status= status.HTTP_201_CREATED)
            return Response(reqSer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: PrivateStudentReadSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
)
@swagger_auto_schema(
    method= 'DELETE',
    responses={
        status.HTTP_204_NO_CONTENT: "Deleted",
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
)
@api_view(['GET', 'DELETE'])
def studentID(request:Request|HttpRequest, id:uuid)->Response:
    if request.method == 'GET':
        try:
            student = User.objects.get(pk = id)
            if student.is_deleted == True:
                if request.user.type in ['Developer']:
                    ser = UserSerializer(student)
                elif request.user.type in ['Patient', 'Student', 'Supervisor', 'CEO']:
                    return Response(data = "student has been deleted", status=status.HTTP_404_NOT_FOUND)
            if request.user.type in ['Patient']:
                ser = PublicStudentReadSerializer(student)
            elif request.user.type in ['Student']:
                if request.user.pk != id :
                    ser = PublicStudentReadSerializer(student)
                elif request.user.pk == id :
                    ser = PrivateStudentReadSerializer(student)
            elif request.user.type in ['Supervisor', 'CEO']:
                ser = PrivateStudentReadSerializer(student)
            elif request.user.type in ['Developer']:
                ser = UserSerializer(student)
            return Response(data= ser.data , status= status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)
    
    elif request.method == 'DELETE':
        try:
            student = User.objects.get(pk = id)
            if request.user.type in ['Patient']:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            elif request.user.type in ['Student']:
                if request.user.pk != id :
                    return Response(status= status.HTTP_401_UNAUTHORIZED)
                elif request.user.pk == id :
                    student.is_deleted = True
                    student.save()
            elif request.user.type in ['Supervisor', 'CEO']:
                    student.is_deleted = True
                    student.save()
            elif request.user.type in ['Developer']:
                student.delete()
            return Response(status= status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)

#____________________________________________________________________________________StudentAppointment
@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: AppointmentsSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    }
)
@swagger_auto_schema(
    method= 'POST',
    responses={
        status.HTTP_200_OK: AppointmentsSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
    request_body=AppointmentsSerializer()
)
@api_view(['GET', 'POST'])
def studentappointment(request:Request|HttpRequest)->Response:
    if request.method == "GET":
        appointment = Appointments.objects.filter(student__exact = request.user.id)
        ser = AppointmentsSerializer(appointment, many= True)
        return Response(data= ser.data, status= status.HTTP_200_OK)
    elif request.method == "POST":
        request.data['student'] = request.user.id
        user_id = RecordTooth.objects.filter(id=request.data['record_tooth']).values_list('record__patient_id', flat=True).get()
        request.data['patient'] = user_id
        reqSer = AppointmentsSerializer(data = request.data)
        if reqSer.is_valid():
            reqSer.save()
            return Response(data= reqSer.data, status= status.HTTP_201_CREATED)
        return Response(reqSer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: AppointmentsSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    }
)
@swagger_auto_schema(
    method= 'POST',
    responses={
        status.HTTP_200_OK: AppointmentsSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
    request_body=AppointmentsSerializer()
)
@api_view(['GET', 'POST'])
def approvedstudentappointment(request:Request|HttpRequest)->Response:
    if request.method == "GET":
        appointment = Appointments.objects.filter(student__exact = request.user.id,status = "Approved")
        ser = AppointmentsSerializer(appointment, many= True)
        return Response(data= ser.data, status= status.HTTP_200_OK)
    elif request.method == "POST":
        request.data['student'] = request.user.id
        reqSer = AppointmentsSerializer(data = request.data)
        if reqSer.is_valid():
            reqSer.save()
            return Response(data= reqSer.data, status= status.HTTP_201_CREATED)
        return Response(reqSer.errors, status=status.HTTP_400_BAD_REQUEST)

#____________________________________________________________________________________StudentSubject
@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: StudentSubjectReadSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
)
@swagger_auto_schema(
    method= 'POST',
    responses={
        status.HTTP_200_OK: StudentSubjectCreateSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
    request_body=StudentSubjectCreateSerializer()
)
@api_view(['GET', 'POST'])
def studentsubject(request:Request|HttpRequest)->Response:
    if request.method == "GET":
        studentsubject = StudentSubject.objects.filter(student = request.user.id)
        ser = StudentSubjectReadSerializer(studentsubject, many = True)
        return Response(data= ser.data, status= status.HTTP_200_OK)
    
    elif request.method == "POST":
        if request.user.type not in ['Developer','CEO','Supervisor']:
            return Response(status=status.HTTP_403_FORBIDDEN)
        students = User.objects.filter(type = "Student")
        for student in students:
            failedstudentsubjects = StudentSubject.objects.filter(student = student.id, completed = False).count()
            if failedstudentsubjects <= 4 and student.academic_year != 5:
                student.academic_year += 1 
                student.save()
                subjects = Subject.objects.filter(academic_year = student.academic_year + 1)
                for subject in subjects:
                    reqSer = StudentSubjectCreateSerializer(data= {"student":student.id, "subject":subject.id})
                    if reqSer.is_valid():
                        reqSer.save()
        return Response(status=status.HTTP_200_OK)

@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: StudentSubjectReadSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
)
@swagger_auto_schema(
    method= 'DELETE',
    responses={
        status.HTTP_204_NO_CONTENT:"Deleted",
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
)
@api_view(['GET','DELETE'])
def studentsubjectID(request:Request|HttpRequest, id:uuid)->Response:
    if request.method == "GET":
        try:
            studentsubject = StudentSubject.objects.get(pk = id)
            ser = StudentSubjectReadSerializer(studentsubject)
            return Response(data= ser.data , status= status.HTTP_200_OK)
        except StudentSubject.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == "DELETE":
        try:
            studentsubject = StudentSubject.objects.get(pk = id)
            studentsubject.is_deleted = True
            studentsubject.save()
            return Response(status= status.HTTP_204_NO_CONTENT)
        except StudentSubject.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)