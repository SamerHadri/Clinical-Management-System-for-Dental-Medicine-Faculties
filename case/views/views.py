from django.utils.translation import gettext_lazy as _
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import HttpRequest, Request
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from case.models import Case, Tooth
from case.serializers.serializers import CaseSerializer, ToothSerializer
import uuid


from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request, HttpRequest


@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: CaseSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
)
@swagger_auto_schema(
    method= 'POST',
    responses={
        status.HTTP_200_OK: CaseSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
    request_body=CaseSerializer()
)
@api_view(['GET', 'POST'])
def case(request:Request|HttpRequest)->Response:
    if request.method == "GET":
        case = Case.objects.all()
        ser = CaseSerializer(case, many= True, context={"request": request})
        return Response(data= ser.data, status= status.HTTP_200_OK)
    
    elif request.method == "POST":
        reqSer = CaseSerializer(data= request.data, context={"request": request})
        if reqSer.is_valid():
            reqSer.save()
            return Response(data= reqSer.data, status= status.HTTP_201_CREATED)
        return Response(reqSer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: CaseSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
)
@swagger_auto_schema(
    method= 'PUT',
    responses={
        status.HTTP_200_OK: CaseSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
    request_body=CaseSerializer()
)
@swagger_auto_schema(
    method= 'DELETE',
    responses={
        status.HTTP_204_NO_CONTENT:"Deleted",
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
)
@api_view(['GET', 'PUT', 'DELETE'])
def caseID(request:Request|HttpRequest, id:uuid)->Response:
    if request.method == "GET":
        try:
            case = Case.objects.get(pk = id)
            ser = CaseSerializer(case, context={"request": request})
            return Response(data= ser.data , status= status.HTTP_200_OK)
        except Case.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == "PUT":
        try:
            case = Case.objects.get(pk = id)
            reqSer = CaseSerializer(data= request.data, instance = case, context={"request": request})
            if reqSer.is_valid():
                reqSer.save()
                return Response(data= reqSer.data, status= status.HTTP_202_ACCEPTED)
            return Response(reqSer.errors, status= status.HTTP_400_BAD_REQUEST)
        except Case.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)
    
    elif request.method == "DELETE":
        try:
            case = Case.objects.get(pk = id)
            case.delete()
            return Response(status= status.HTTP_204_NO_CONTENT)
        except Case.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)

@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: ToothSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
)
@swagger_auto_schema(
    method= 'POST',
    responses={
        status.HTTP_200_OK: ToothSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
    request_body=ToothSerializer()
)
@api_view(['GET', 'POST'])
def tooth(request:Request|HttpRequest)->Response:
    if request.method == "GET":
        tooth = Tooth.objects.all()
        ser = ToothSerializer(tooth, many= True, context={"request": request})
        return Response(data= ser.data, status= status.HTTP_200_OK)
    
    elif request.method == "POST":
        reqSer = ToothSerializer(data= request.data, context={"request": request})
        if reqSer.is_valid():
            reqSer.save()
            return Response(data= reqSer.data, status= status.HTTP_201_CREATED)
        return Response(reqSer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: ToothSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
)
@swagger_auto_schema(
    method= 'PUT',
    responses={
        status.HTTP_200_OK: ToothSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
    request_body=ToothSerializer()
)
@swagger_auto_schema(
    method= 'DELETE',
    responses={
        status.HTTP_204_NO_CONTENT:"Deleted",
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
)
@api_view(['GET', 'PUT', 'DELETE'])
def toothID(request:Request|HttpRequest, id:uuid)->Response:
    if request.method == "GET":
        try:
            case = Tooth.objects.get(pk = id)
            ser = ToothSerializer(case, context={"request": request})
            return Response(data= ser.data , status= status.HTTP_200_OK)
        except Tooth.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == "PUT":
        try:
            case = Tooth.objects.get(pk = id)
            reqSer = ToothSerializer(data= request.data, instance = case, context={"request": request})
            if reqSer.is_valid():
                reqSer.save()
                return Response(data= reqSer.data, status= status.HTTP_202_ACCEPTED)
            return Response(reqSer.errors, status= status.HTTP_400_BAD_REQUEST)
        except Tooth.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)
    
    elif request.method == "DELETE":
        try:
            case = Tooth.objects.get(pk = id)
            case.delete()
            return Response(status= status.HTTP_204_NO_CONTENT)
        except Tooth.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)
