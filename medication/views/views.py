

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import HttpRequest, Request
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from medication.models import Medication
from medication.serializers.serializers import MedicationSerializer
import uuid


from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request, HttpRequest


@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: MedicationSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
)
@swagger_auto_schema(
    method= 'POST',
    responses={
        status.HTTP_200_OK: MedicationSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
    request_body=MedicationSerializer()
)
@api_view(['GET', 'POST'])
def medication(request:Request|HttpRequest)->Response:
    if request.method == "GET":
        medication = Medication.objects.all()
        ser = MedicationSerializer(medication, many= True, context={"request": request})
        return Response(data= ser.data, status= status.HTTP_200_OK)
    
    elif request.method == "POST":
        reqSer = MedicationSerializer(data= request.data, context={"request": request})
        if reqSer.is_valid():
            reqSer.save()
            return Response(data= reqSer.data, status= status.HTTP_201_CREATED)
        return Response(reqSer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: MedicationSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
)
@swagger_auto_schema(
    method= 'PUT',
    responses={
        status.HTTP_200_OK: MedicationSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
    request_body=MedicationSerializer()
)
@swagger_auto_schema(
    method= 'DELETE',
    responses={
        status.HTTP_204_NO_CONTENT: "Deleted",
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
)
@api_view(['GET', 'PUT', 'DELETE'])
def medicationID(request:Request|HttpRequest, id:uuid)->Response:
    if request.method == "GET":
        try:
            medication = Medication.objects.get(pk = id)
            ser = MedicationSerializer(medication, context={"request": request})
            return Response(data= ser.data , status= status.HTTP_200_OK)
        except Medication.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == "PUT":
        try:
            medication = Medication.objects.get(pk = id)
            reqSer = MedicationSerializer(data= request.data, instance = medication, context={"request": request})
            if reqSer.is_valid():
                reqSer.save()
                return Response(data= reqSer.data, status= status.HTTP_202_ACCEPTED)
            return Response(reqSer.errors, status= status.HTTP_400_BAD_REQUEST)
        except Medication.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)
    
    elif request.method == "DELETE":
        try:
            medication = Medication.objects.get(pk = id)
            medication.delete()
            return Response(status= status.HTTP_204_NO_CONTENT)
        except Medication.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)
