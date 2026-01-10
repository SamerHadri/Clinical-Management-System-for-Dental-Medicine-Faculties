

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import HttpRequest, Request
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from record.models import Record, RecordTooth
from record.serializers.serializers import RecordCreateSerializer, RecordReadSerializer, RecordToothSerializer
import uuid


from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request, HttpRequest


@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: RecordReadSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
)
@swagger_auto_schema(
    method= 'POST',
    responses={
        status.HTTP_200_OK: RecordCreateSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
    request_body=RecordCreateSerializer()
)
@api_view(['GET', 'POST'])
def record(request:Request|HttpRequest)->Response:
    if request.method == "GET":
        paginator = PageNumberPagination()
        paginator.page_size = 10
        record = Record.objects.all()
        paginated_record = paginator.paginate_queryset(record, request)
        ser = RecordReadSerializer(paginated_record, many= True)
        return Response(data= ser.data, status= status.HTTP_200_OK)
    
    elif request.method == "POST":
        reqSer = RecordCreateSerializer(data= request.data)
        if reqSer.is_valid():
            reqSer.save()
            return Response(data= reqSer.data, status= status.HTTP_201_CREATED)
        return Response(reqSer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: RecordReadSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
)
@swagger_auto_schema(
    method= 'DELETE',
    responses={
        status.HTTP_100_CONTINUE: "Deleted",
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
)
@api_view(['GET', 'DELETE'])
def recordID(request:Request|HttpRequest, id:uuid)->Response:
    if request.method == "GET":
        try:
            record = Record.objects.get(pk = id)
            ser = RecordReadSerializer(record)
            return Response(data= ser.data , status= status.HTTP_200_OK)
        except Record.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == "DELETE":
        try:
            record = Record.objects.get(pk = id)
            record.delete()
            return Response(status= status.HTTP_204_NO_CONTENT)
        except Record.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)


#____________________________________________________________________________________recordtooth
@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: RecordToothSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
)
@api_view(['GET'])
def recordtooth(request:Request|HttpRequest)->Response:
    if request.method == "GET":
        record = RecordTooth.objects.all()
        ser = RecordToothSerializer(record, many= True)
        return Response(data= ser.data, status= status.HTTP_200_OK)


#____________________________________________________________________________________recordtooth_filters
@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: RecordToothSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
)
@api_view(['GET'])
def notexamined(request:Request|HttpRequest)->Response:
    if request.method == "GET":
        record = RecordTooth.objects.filter(
            examination_student__isnull=True,
            examination_supervisor__isnull=True,
            treatment_student__isnull=True,
            treatment_supervisor__isnull=True,)
        ser = RecordToothSerializer(record, many= True)
        return Response(data= ser.data, status= status.HTTP_200_OK)

@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: RecordToothSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    }
)
@api_view(['GET'])
def examined(request:Request|HttpRequest)->Response:
    if request.method == "GET":
        
        record = RecordTooth.objects.filter(
            examination_student__isnull=False,
            examination_supervisor__isnull=True,
            treatment_student__isnull=True,
            treatment_supervisor__isnull=True)
        ser = RecordToothSerializer(record, many= True)
        return Response(data= ser.data, status= status.HTTP_200_OK)

@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: RecordToothSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
    operation_description="query parametes to look for the case"
)
@api_view(['GET'])
def examinedapproved(request:Request|HttpRequest)->Response:
    if request.method == "GET":
        case_pk = request.query_params.get("case")
        record = RecordTooth.objects.filter(
                examination_student__isnull=False,
                examination_supervisor__isnull=False,
                treatment_student__isnull=True,
                treatment_supervisor__isnull=True)
        if case_pk:
            record = record.filter(case=case_pk)
        ser = RecordToothSerializer(record, many= True)
        return Response(data= ser.data, status= status.HTTP_200_OK)

@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: RecordToothSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
)
@api_view(['GET'])
def treated(request:Request|HttpRequest)->Response:
    if request.method == "GET":
        record = RecordTooth.objects.filter(
            examination_student__isnull=False,
            examination_supervisor__isnull=False,
            treatment_student__isnull=False,
            treatment_supervisor__isnull=True,)
        ser = RecordToothSerializer(record, many= True)
        return Response(data= ser.data, status= status.HTTP_200_OK)

@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: RecordToothSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
)
@api_view(['GET'])
def treatedapproved(request:Request|HttpRequest)->Response:
    if request.method == "GET":
        record = RecordTooth.objects.filter(
            examination_student__isnull=False,
            examination_supervisor__isnull=False,
            treatment_student__isnull=False,
            treatment_supervisor__isnull=False,)
        ser = RecordToothSerializer(record, many= True)
        return Response(data= ser.data, status= status.HTTP_200_OK)