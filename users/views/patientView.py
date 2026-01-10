

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import HttpRequest, Request
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from record.models import Record, Appointments
from users.models import User
from users.serializers.serializers import UserSerializer
from users.serializers.patientSerializers import PatientCreateSerializer, PatientReadSerializer
from record.serializers.serializers import RecordCreateSerializer, AppointmentsSerializer, AppointmentsStatusSerializer
import uuid

from rest_framework.authtoken.models import Token
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema




@swagger_auto_schema(
    method= 'POST',
    responses={
        status.HTTP_200_OK: PatientCreateSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
    request_body=PatientCreateSerializer()
)
@api_view(['POST'])
@permission_classes([AllowAny])
def createpatient(request:Request|HttpRequest)->Response:
    #try:
    #    user = User.objects.get(username = request.data['username'])
    #    return Response(data="username already exists", status=status.HTTP_409_CONFLICT)
    #except:
    if True:
        #if request.data['password'] != request.data['rewrite_password']:
        #    return Response(data='passwords does not match', status=status.HTTP_409_CONFLICT)
        reqSer = PatientCreateSerializer(data = request.data)
        if reqSer.is_valid():
            reqSer.save()
            record = RecordCreateSerializer(data= {'patient':reqSer.data['id']})
            user = User.objects.get(username = request.data['username'])
            usertoken, created = Token.objects.get_or_create(user= user)
            if record.is_valid():
                record.save()
                patient_record = Record.objects.get(patient = reqSer.data['id'])
                return Response(data={ 
                        'token': usertoken.key,
                        'id': user.pk,
                        'type': user.type,
                        'record' :patient_record.id
                    }, status= status.HTTP_201_CREATED)
            return Response(reqSer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(reqSer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: PatientReadSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
)
@api_view(['GET'])
def patient(request:Request|HttpRequest)->Response:
    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 10
        patient = User.objects.filter(type__exact = "Patient")
        if request.user.type in ['Patient']:
            patient = patient.filter(pk = request.user.id, is_deleted = False)
            paginated_patient = paginator.paginate_queryset(patient, request)
            ser = PatientReadSerializer(paginated_patient, many = True)
        elif request.user.type in ['Student', 'Supervisor', 'CEO']:
            patient = patient.filter(is_deleted = False)
            paginated_patient = paginator.paginate_queryset(patient, request)
            ser = PatientReadSerializer(paginated_patient, many = True)
        elif request.user.type in ['Developer']:
            paginated_patient = paginator.paginate_queryset(patient, request)
            ser = UserSerializer(paginated_patient, many = True)
        return Response(data= ser.data, status= status.HTTP_200_OK)

@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: PatientReadSerializer(),
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
def patientID(request:Request|HttpRequest, id:uuid)->Response:
    if request.method == 'GET':
        try:
            patient = User.objects.get(pk = id)
            if patient.is_deleted == True:
                if request.user.type in ['Developer']:
                    ser = UserSerializer(patient)
                elif request.user.type in ['Patient', 'Student', 'Supervisor', 'CEO']:
                    return Response(data = "patient has been deleted", status=status.HTTP_404_NOT_FOUND)
            if request.user.type in ['Patient']:
                if request.user.pk != id :
                    ser = PatientReadSerializer(patient)
                elif request.user.pk == id :
                    ser = PatientReadSerializer(patient)
            elif request.user.type in ['Student', 'Supervisor', 'CEO']:
                ser = PatientReadSerializer(patient)
            elif request.user.type in ['Developer']:
                ser = UserSerializer(patient)
            return Response(data= ser.data , status= status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)
    
    elif request.method == 'DELETE':
        try:
            patient = User.objects.get(pk = id)
            if request.user.type in ['Patient']:
                if request.user.pk != id :
                    return Response(status= status.HTTP_401_UNAUTHORIZED)
                elif request.user.pk == id :
                    patient.is_deleted = True
                    patient.save()
                    return Response(status= status.HTTP_204_NO_CONTENT)
            elif request.user.type in ['Student', 'Supervisor', 'CEO']:
                patient.is_deleted = True
                patient.save()
            elif request.user.type in ['Developer']:
                patient.delete()
            return Response(status= status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)

#____________________________________________________________________________________PatientAppointment
@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: AppointmentsSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    }
)
@api_view(['GET'])
def patientappointment(request:Request|HttpRequest)->Response:
    if request.method == "GET":
        appointment = Appointments.objects.filter(patient__exact = request.user.id)
        ser = AppointmentsSerializer(appointment, many= True)
        return Response(data= ser.data, status= status.HTTP_200_OK)


@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: AppointmentsSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    }
)
@api_view(['GET'])
def patientpendingappointment(request:Request|HttpRequest)->Response:
    if request.method == "GET":
        appointment = Appointments.objects.filter(patient__exact = request.user.id,status__exact = "Pending")
        ser = AppointmentsSerializer(appointment, many= True)
        return Response(data= ser.data, status= status.HTTP_200_OK)


@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: AppointmentsSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    }
)
@swagger_auto_schema(
    method= 'PUT',
    responses={
        status.HTTP_200_OK: AppointmentsSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
    request_body=AppointmentsStatusSerializer()
)
@api_view(['GET','PUT'])
def patientappointmentID(request:Request|HttpRequest, id:uuid)->Response:
    if request.method == 'GET':
        try:
            appointment = Appointments.objects.get(pk = id)
            ser = AppointmentsSerializer(appointment)
            return Response(data= ser.data, status= status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)
    elif request.method == 'PUT':
        try:
            appointment = Appointments.objects.get(pk = id)
            reqSer = AppointmentsStatusSerializer(data= request.data, instance = appointment)
            if reqSer.is_valid():
                reqSer.save()
                return Response(data= reqSer.data, status= status.HTTP_202_ACCEPTED)
            return Response(reqSer.errors, status= status.HTTP_400_BAD_REQUEST)
        except Appointments.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)