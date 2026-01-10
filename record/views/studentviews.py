from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import HttpRequest, Request
from rest_framework import status
from django.db.models import Q
from record.models import Record, RecordTooth
from users.models import User
from record.serializers.serializers import RecordExaminationUpdateSerializer, RecordTreatmentUpdateSerializer, RecordReadSerializer, RecordTreatmentNextAppointmentSerializer, RecordToothSerializer
import uuid

from django.db import IntegrityError

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request, HttpRequest




@swagger_auto_schema(
    method= 'PUT',
    responses={
        status.HTTP_200_OK: RecordReadSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
    request_body=RecordExaminationUpdateSerializer()
)
@api_view(['PUT'])
def examin(request:Request|HttpRequest, id:uuid)->Response:
    if request.method == "PUT":
        print(request.data)
        print("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
        if request.user.type not in ['Student']:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        try:
            record_id = RecordTooth.objects.filter(id=id).values_list('record_id', flat=True).get()
            record = Record.objects.get(pk = record_id)
            student = User.objects.get(pk = request.user.id)
            try:
                for tooth in request.data['teeth']:
                    tooth['examination_student']=student.id
            except:
                pass
            reqSer = RecordExaminationUpdateSerializer(data= request.data, instance = record)
            if reqSer.is_valid():
                reqSer.save()
                return Response(data= reqSer.data, status= status.HTTP_202_ACCEPTED)
            return Response(reqSer.errors, status= status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response(data="Error: A duplicate entry already exists for this unique field.", status=status.HTTP_409_CONFLICT)
        except Record.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method= 'PUT',
    responses={
        status.HTTP_200_OK: RecordReadSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
    request_body=RecordTreatmentUpdateSerializer()
)
@api_view(['PUT'])
def treatment(request:Request|HttpRequest, id:uuid)->Response:
    if request.method == "PUT":
        print("hello")
        if request.user.type not in ['Student']:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        try:
            record_id = RecordTooth.objects.filter(id=id).values_list('record_id', flat=True).get()
            record = Record.objects.get(pk = record_id)
            student = User.objects.get(pk = request.user.id)
            try:
                for tooth in request.data['teeth']:
                    tooth['treatment_student']=student.id
            except:
                pass
            reqSer = RecordTreatmentUpdateSerializer(data= request.data, instance = record)
            if reqSer.is_valid():
                reqSer.save()
                return Response(data= reqSer.data, status= status.HTTP_202_ACCEPTED)
            return Response(reqSer.errors, status= status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response(data="Error: A duplicate entry already exists for this unique field.", status=status.HTTP_409_CONFLICT)
        except Record.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method= 'PUT',
    responses={
        status.HTTP_200_OK: RecordReadSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
    request_body=RecordTreatmentNextAppointmentSerializer()
)
@api_view(['PUT'])
def nextappointment(request:Request|HttpRequest, id:uuid)->Response:
    if request.method == 'PUT':
        try:
            record_treatment = RecordTooth.objects.get(pk = id)
            if request.user.id == record_treatment.student :
                return Response(data = {"message":"this is not your case"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            reqSer = RecordTreatmentNextAppointmentSerializer(data = request.data, instance = record_treatment)
            if reqSer.is_valid():
                reqSer.save()
                return Response(data= reqSer.data, status= status.HTTP_202_ACCEPTED)
            return Response(reqSer.errors, status= status.HTTP_400_BAD_REQUEST)
        except Record.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: RecordReadSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
)
@api_view(['GET'])
def studentrecordtooth(request:Request|HttpRequest)->Response:
    if request.method == 'GET':
        record_tooth = RecordTooth.objects.filter(Q(examination_student_id=request.user.id) | Q(treatment_student_id=request.user.id))
        ser = RecordToothSerializer(record_tooth, many = True)
        return Response(ser.data, status=status.HTTP_200_OK)