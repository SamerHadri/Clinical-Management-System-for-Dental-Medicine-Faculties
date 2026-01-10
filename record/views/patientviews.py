from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import HttpRequest, Request
from rest_framework import status
from record.models import Record, RecordTooth
from record.serializers.serializers import  RecordReadSerializer, RecordToothPatientNotesSeializer
import uuid

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request, HttpRequest


#check uuid


@swagger_auto_schema(
    method= 'POST',
    responses={
        status.HTTP_200_OK: RecordReadSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
    request_body=RecordToothPatientNotesSeializer()
)
@api_view(['POST'])
def patientnotes(request:Request|HttpRequest)->Response:
    if request.method == "POST":
        try:
            record = Record.objects.get(patient_id = request.user.id)
            request.data['record'] = record.id
            record_tooth = RecordTooth.objects.filter(record_id = record, tooth_id = request.data['tooth'])
            try:
                if record_tooth.first().patient_notes == None:
                    reqSer = RecordToothPatientNotesSeializer(data= request.data)
                else:
                    reqSer = RecordToothPatientNotesSeializer(data = request.data, instance = record_tooth.first())
            except:
                reqSer = RecordToothPatientNotesSeializer(data = request.data, instance = record_tooth.first())
            if reqSer.is_valid():
                reqSer.save()
                return Response(data= reqSer.data, status= status.HTTP_202_ACCEPTED)
            return Response(reqSer.errors, status= status.HTTP_400_BAD_REQUEST)
        except Record.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)
