

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import HttpRequest, Request
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from users.models import User, Subject ,StudentSubject
from users.serializers.serializers import UserSerializer
from users.serializers.supervisorSerializers import SupervisorCreateSerializer, PublicSupervisorReadSerializer ,PrivateSupervisorReadSerializer, ChangeStudentMarksSerializer
import uuid

from rest_framework.authtoken.models import Token
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema



@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: PrivateSupervisorReadSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
)
@swagger_auto_schema(
    method= 'POST',
    responses={
        status.HTTP_200_OK: SupervisorCreateSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
    request_body=SupervisorCreateSerializer()
)
@api_view(['GET', 'POST'])
def supervisor(request:Request|HttpRequest)->Response:
    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 10
        supervisor = User.objects.filter(type__exact = "Supervisor")
        paginated_supervisors = paginator.paginate_queryset(supervisor, request)
        if request.user.type in ['Patient', 'Student', 'Supervisor']:
            ser = PublicSupervisorReadSerializer(paginated_supervisors, many = True)
        elif request.user.type in ['CEO']:
            ser = PrivateSupervisorReadSerializer(paginated_supervisors, many = True)
        elif request.user.type in ['Developer']:
            ser = UserSerializer(paginated_supervisors, many = True)
        return Response(data= ser.data, status= status.HTTP_200_OK)
    
    elif request.method == 'POST':
        try:
            user = User.objects.get(username = request.data['username'])
            return Response(data="username already exists", status=status.HTTP_409_CONFLICT)
        except:
            if request.user.type in ['Patient', 'Student', 'Supervisor']:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            reqSer = SupervisorCreateSerializer(data = request.data)
            if reqSer.is_valid():
                reqSer.save()
                user = User.objects.get(username = request.data['username'])
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
        status.HTTP_200_OK: PrivateSupervisorReadSerializer(),
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
@api_view(['GET', 'PUT', 'DELETE'])
def supervisorID(request:Request|HttpRequest, id:uuid)->Response:
    if request.method == 'GET':
        try:
            supervisor = User.objects.get(pk = id)
            if supervisor.is_deleted == True:
                if request.user.type in ['Developer']:
                    ser = UserSerializer(supervisor)
                elif request.user.type in ['Patient', 'Student', 'Supervisor', 'CEO']:
                    return Response(data = "supervisor has been deleted", status=status.HTTP_404_NOT_FOUND)
            if request.user.type in ['Patient', 'Student']:
                ser = PublicSupervisorReadSerializer(supervisor)
            elif request.user.type in ['Supervisor']:
                if request.user.pk != id :
                    ser = PublicSupervisorReadSerializer(supervisor)
                elif request.user.pk == id :
                    ser = PrivateSupervisorReadSerializer(supervisor)
            elif request.user.type in ['CEO']:
                ser = PrivateSupervisorReadSerializer(supervisor)
            elif request.user.type in ['Developer']:
                ser = UserSerializer(supervisor)
            return Response(data= ser.data , status= status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)
    
    elif request.method == 'DELETE':
        try:
            supervisor = User.objects.get(pk = id)
            if request.user.type in ['Patient', 'Student']:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            elif request.user.type in ['Supervisor']:
                if request.user.pk != id :
                    return Response(status= status.HTTP_401_UNAUTHORIZED)
                elif request.user.pk == id :
                    supervisor.is_deleted = True
                    supervisor.save()
            elif request.user.type in ['Supervisor', 'CEO']:
                    supervisor.is_deleted = True
                    supervisor.save()
            elif request.user.type in ['Developer']:
                supervisor.delete()
            return Response(status= status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)

#____________________________________________________________________________________SupervisorMarks
@swagger_auto_schema(
    method= 'PUT',
    responses={
        status.HTTP_200_OK: ChangeStudentMarksSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
    request_body=ChangeStudentMarksSerializer()
)
@api_view(['PUT'])
def supervisorstudentmarks(request:Request|HttpRequest, id:uuid)->Response:
    if request.method == 'PUT':
        if request.user.type in ['Supervisor']:
            
            try:
                studentsubject = StudentSubject.objects.get(pk = id)
            except:
                return Response(data="student hasn't registered to the subject yet", status=status.HTTP_404_NOT_FOUND)
            
            if studentsubject.completed == True:
                return Response(data="student has already passed", status=status.HTTP_406_NOT_ACCEPTABLE)
            
            if request.data['mark'] > 60 :
                request.data['completed'] = True
            else:
                request.data['completed'] = False
            request.data['supervisor'] = request.user.id
            reqSer = ChangeStudentMarksSerializer(data = request.data, instance = studentsubject)
            if reqSer.is_valid():
                reqSer.save()
                return Response(data= reqSer.data, status= status.HTTP_202_ACCEPTED)
            return Response(reqSer.errors, status= status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)