

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import HttpRequest, Request
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from subject.models import Subject, Department
from subject.serializers.serializers import DepartmentSerializer, SubjectSerializer
import uuid


from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request, HttpRequest



@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: DepartmentSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
)
@swagger_auto_schema(
    method= 'POST',
    responses={
        status.HTTP_200_OK: DepartmentSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
    request_body=DepartmentSerializer()
)
@api_view(['GET', 'POST'])
def department(request:Request|HttpRequest)->Response:
    if request.method == "GET":
        department = Department.objects.all()
        ser = DepartmentSerializer(department, many= True, context={"request": request})
        return Response(data= ser.data, status= status.HTTP_200_OK)
    
    elif request.method == "POST":
        reqSer = DepartmentSerializer(data= request.data, context={"request": request})
        if reqSer.is_valid():
            reqSer.save()
            return Response(data= reqSer.data, status= status.HTTP_201_CREATED)
        return Response(reqSer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: DepartmentSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
)
@swagger_auto_schema(
    method= 'PUT',
    responses={
        status.HTTP_200_OK: DepartmentSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
    request_body=DepartmentSerializer()
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
def departmentID(request:Request|HttpRequest, id:uuid)->Response:
    if request.method == "GET":
        try:
            department = Department.objects.get(pk = id)
            ser = DepartmentSerializer(department, context={"request": request})
            return Response(data= ser.data , status= status.HTTP_200_OK)
        except Department.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == "PUT":
        try:
            department = Department.objects.get(pk = id)
            reqSer = DepartmentSerializer(data= request.data, instance = department, context={"request": request})
            if reqSer.is_valid():
                reqSer.save()
                return Response(data= reqSer.data, status= status.HTTP_202_ACCEPTED)
            return Response(reqSer.errors, status= status.HTTP_400_BAD_REQUEST)
        except Department.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)
    
    elif request.method == "DELETE":
        try:
            department = Department.objects.get(pk = id)
            department.delete()
            return Response(status= status.HTTP_204_NO_CONTENT)
        except Department.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: SubjectSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
)
@swagger_auto_schema(
    method= 'POST',
    responses={
        status.HTTP_200_OK: SubjectSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
    request_body=SubjectSerializer()
)
@api_view(['GET', 'POST'])
def subject(request:Request|HttpRequest)->Response:
    if request.method == "GET":
        subject = Subject.objects.all().order_by("academic_year","academic_term")
        ser = SubjectSerializer(subject, many= True, context={"request": request})
        return Response(data= ser.data, status= status.HTTP_200_OK)
    
    elif request.method == "POST":
        reqSer = SubjectSerializer(data= request.data, context={"request": request})
        if reqSer.is_valid():
            reqSer.save()
            return Response(data= reqSer.data, status= status.HTTP_201_CREATED)
        return Response(reqSer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: SubjectSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
)
@swagger_auto_schema(
    method= 'PUT',
    responses={
        status.HTTP_200_OK: SubjectSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
    request_body=SubjectSerializer()
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
def subjectID(request:Request|HttpRequest, id:uuid)->Response:
    if request.method == "GET":
        try:
            subject = Subject.objects.get(pk = id)
            ser = SubjectSerializer(subject, context={"request": request})
            return Response(data= ser.data , status= status.HTTP_200_OK)
        except Subject.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == "PUT":
        try:
            subject = Subject.objects.get(pk = id)
            reqSer = SubjectSerializer(data= request.data, instance = subject, context={"request": request})
            if reqSer.is_valid():
                reqSer.save()
                return Response(data= reqSer.data, status= status.HTTP_202_ACCEPTED)
            return Response(reqSer.errors, status= status.HTTP_400_BAD_REQUEST)
        except Subject.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)
    
    elif request.method == "DELETE":
        try:
            subject = Subject.objects.get(pk = id)
            subject.delete()
            return Response(status= status.HTTP_204_NO_CONTENT)
        except Subject.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)
