from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import HttpRequest, Request
from rest_framework import status
from record.models import RecordTooth
from users.models import StudentSubject
from subject.models import Subject
from record.serializers.serializers import RecordReadSerializer, ExaminApproveSerializer, TreatmentApproveSerializer
import uuid

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
    request_body=ExaminApproveSerializer()
)
@api_view(['PUT'])
def examinapprove(request:Request|HttpRequest, id:uuid)->Response:
    if request.method == 'PUT':
        if request.user.type not in ['Supervisor']:
            return Response(data = {"message":"action not allowd"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        try:
            record_case = RecordTooth.objects.get(pk = id)
            if record_case.examination_subject != None:
                try:
                    subject = Subject.objects.get(pk = record_case.examination_subject.subject_id)
                    if request.user.department != subject.department:
                        return Response(data="Error: You are not from the same department", status=status.HTTP_405_METHOD_NOT_ALLOWED)
                except StudentSubject.DoesNotExist:
                    return Response(status= status.HTTP_404_NOT_FOUND)
            if record_case.case is None :
                return Response(data={"This is not diagnosed yet"}, status=status.HTTP_401_UNAUTHORIZED)
            request.data['examination_supervisor'] = request.user.id
            reqSer = ExaminApproveSerializer(data = request.data, instance = record_case)
            if reqSer.is_valid():
                reqSer.save()
                return Response(data= reqSer.data, status= status.HTTP_202_ACCEPTED)
            return Response(reqSer.errors, status= status.HTTP_400_BAD_REQUEST)
        except RecordTooth.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)

@swagger_auto_schema(
    method= 'PUT',
    responses={
        status.HTTP_200_OK: RecordReadSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
    request_body=TreatmentApproveSerializer()
)
@api_view(['PUT'])
def treatmentapprove(request:Request|HttpRequest, id:uuid)->Response:
    if request.method == 'PUT':
        if request.user.type not in ['Supervisor']:
            return Response(data = {"message":"action not allowd"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        try:
            record_treatment = RecordTooth.objects.get(pk = id)
            if record_treatment.treatment_subject != None:
                try:
                    subject = Subject.objects.get(pk = record_treatment.treatment_subject.subject_id)
                    if request.user.department != subject.department:
                        return Response(data="Error: You are not from the same department", status=status.HTTP_405_METHOD_NOT_ALLOWED)
                except StudentSubject.DoesNotExist:
                    return Response(status= status.HTTP_404_NOT_FOUND)
            if record_treatment.treatment is None :
                return Response(data={"This is not treated yet"}, status=status.HTTP_401_UNAUTHORIZED)
            request.data['treatment_supervisor'] = request.user.id
            reqSer = TreatmentApproveSerializer(data = request.data, instance = record_treatment)
            if reqSer.is_valid():
                reqSer.save()
                return Response(data= reqSer.data, status= status.HTTP_202_ACCEPTED)
            return Response(reqSer.errors, status= status.HTTP_400_BAD_REQUEST)
        except RecordTooth.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)
