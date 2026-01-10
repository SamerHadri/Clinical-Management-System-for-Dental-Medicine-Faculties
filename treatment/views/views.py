

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import HttpRequest, Request
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from treatment.models import Treatment
from treatment.serializers.serializers import TreatmentSerializer
import uuid


from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request, HttpRequest


@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: TreatmentSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
)
@swagger_auto_schema(
    method= 'POST',
    responses={
        status.HTTP_200_OK: TreatmentSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
    request_body=TreatmentSerializer()
)
@api_view(['GET', 'POST'])
def index(request:Request|HttpRequest)->Response:
    if request.method == "GET":
        treatment = Treatment.objects.all()
        ser = TreatmentSerializer(treatment, many= True, context={"request": request})
        return Response(data= ser.data, status= status.HTTP_200_OK)
    
    elif request.method == "POST":
        reqSer = TreatmentSerializer(data= request.data, context={"request": request})
        if reqSer.is_valid():
            reqSer.save()
            return Response(data= reqSer.data, status= status.HTTP_201_CREATED)
        return Response(reqSer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: TreatmentSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
)
@swagger_auto_schema(
    method= 'PUT',
    responses={
        status.HTTP_200_OK: TreatmentSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
    request_body=TreatmentSerializer()
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
def indexID(request:Request|HttpRequest, id:uuid)->Response:
    if request.method == "GET":
        try:
            treatment = Treatment.objects.get(pk = id)
            ser = TreatmentSerializer(treatment, context={"request": request})
            return Response(data= ser.data , status= status.HTTP_200_OK)
        except Treatment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == "PUT":
        try:
            treatment = Treatment.objects.get(pk = id)
            reqSer = TreatmentSerializer(data= request.data, instance = treatment, context={"request": request})
            if reqSer.is_valid():
                reqSer.save()
                return Response(data= reqSer.data, status= status.HTTP_202_ACCEPTED)
            return Response(reqSer.errors, status= status.HTTP_400_BAD_REQUEST)
        except Treatment.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)
    
    elif request.method == "DELETE":
        try:
            treatment = Treatment.objects.get(pk = id)
            treatment.delete()
            return Response(status= status.HTTP_204_NO_CONTENT)
        except Treatment.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)
