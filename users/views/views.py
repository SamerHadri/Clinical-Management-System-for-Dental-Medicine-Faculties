from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import HttpRequest, Request
from rest_framework import status
from record.models import Record
from users.models import User
from users.serializers.serializers import UserSerializer, ChangePasswordSerializer , UserInfoSerializer, LoginSerializer
from users.serializers.serializers import CEOCreateSerializer, PublicCEOReadSerializer, PrivateCEOReadSerializer
import uuid
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token





@swagger_auto_schema(
    method= 'POST',
    responses={
        status.HTTP_200_OK: UserInfoSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
    request_body=LoginSerializer()
)
@api_view(['POST'])
@permission_classes([AllowAny])
def userlogin(request:Request|HttpRequest)->Response:
    user = authenticate(request, username = request.data['username'], password = request.data['password'])
    if user is None:
        return Response(data='user not found', status=status.HTTP_404_NOT_FOUND)
    usertoken, created = Token.objects.get_or_create(user= user)
    if user.type == "Patient":
        record = Record.objects.get(patient = user.pk)
        return Response(data={
                'token': usertoken.key,
                'id': user.pk,
                'type': user.type,
                'record' : record.id
            } ,status=status.HTTP_200_OK)
    else:
        return Response(data={
                'token': usertoken.key,
                'id': user.pk,
                'type': user.type
            } ,status=status.HTTP_200_OK)


@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: PrivateCEOReadSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
)
@swagger_auto_schema(
    method= 'POST',
    responses={
        status.HTTP_200_OK: CEOCreateSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
    request_body=CEOCreateSerializer()
)
@api_view(['GET', 'POST'])
def ceo(request:Request|HttpRequest)->Response:
    if request.method == 'GET':
        ceo = User.objects.filter(type__exact = "CEO")
        if request.user.type in ['Patient', 'Student', 'Supervisor']:
            ser = PublicCEOReadSerializer(ceo, many = True)
        elif request.user.type in ['CEO']:
            ser = PrivateCEOReadSerializer(ceo, many = True)
        elif request.user.type in ['Developer']:
            ser = UserSerializer(ceo, many = True)
        return Response(data= ser.data, status= status.HTTP_200_OK)
    
    elif request.method == 'POST':
        try:
            user = User.objects.get(username = request.data['username'])
            return Response(data="username already exists", status=status.HTTP_409_CONFLICT)
        except:
            if request.user.type in ['Patient', 'Student', 'Supervisor']:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            reqSer = CEOCreateSerializer(data = request.data)
            if reqSer.is_valid():
                reqSer.save()
                return Response(data= reqSer.data, status= status.HTTP_201_CREATED)
            return Response(reqSer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: PrivateCEOReadSerializer(),
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
def ceoID(request:Request|HttpRequest, id:uuid)->Response:
    if request.method == 'GET':
        try:
            ceo = User.objects.get(pk = id)
            if ceo.is_deleted == True:
                if request.user.type in ['Developer']:
                    ser = UserSerializer(ceo)
                elif request.user.type in ['Patient', 'Student', 'Supervisor', 'CEO']:
                    return Response(data = "CEO has been deleted", status=status.HTTP_404_NOT_FOUND)
            if request.user.type in ['Patient', 'Student', 'Supervisor']:
                ser = PublicCEOReadSerializer(ceo)
            elif request.user.type in ['CEO']:
                if request.user.pk != id :
                    ser = PublicCEOReadSerializer(ceo)
                elif request.user.pk == id :
                    ser = PrivateCEOReadSerializer(ceo)
            elif request.user.type in ['Developer']:
                ser = UserSerializer(ceo)
            return Response(data= ser.data , status= status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)
        
    elif request.method == 'PUT':
        # to be continued
        pass
    
    elif request.method == 'DELETE':
        try:
            ceo = User.objects.get(pk = id)
            if request.user.type in ['Patient', 'Student', 'Supervisor']:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            elif request.user.type in ['CEO']:
                if request.user.pk != id :
                    return Response(status= status.HTTP_401_UNAUTHORIZED)
                elif request.user.pk == id :
                    ceo.is_deleted = True
                    ceo.save()
            elif request.user.type in ['Developer']:
                ceo.delete()
            return Response(status= status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: UserSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
)
@swagger_auto_schema(
    method= 'POST',
    responses={
        status.HTTP_200_OK: UserSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
    request_body=UserSerializer()
)
@api_view(['GET', 'POST'])
def index(request:Request|HttpRequest)->Response:
    if request.method == "GET":
        user = User.objects.all()
        ser = UserSerializer(user, many = True)
        return Response(data= ser.data, status= status.HTTP_200_OK)
    
    elif request.method == "POST":
        try:
            user = User.objects.get(username = request.data['username'])
            return Response(data="username already exists", status=status.HTTP_409_CONFLICT)
        except:
            reqSer = UserSerializer(data= request.data)
            if reqSer.is_valid():
                reqSer.save()
                return Response(data= reqSer.data, status= status.HTTP_201_CREATED)
            return Response(reqSer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method= 'GET',
    responses={
        status.HTTP_200_OK: UserSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
)
@swagger_auto_schema(
    method= 'PUT',
    responses={
        status.HTTP_200_OK: UserSerializer(),
        status.HTTP_401_UNAUTHORIZED: "UnAuthorized",
        status.HTTP_400_BAD_REQUEST: "BadRequest"
    },
    request_body=UserSerializer()
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
            user = User.objects.get(pk = id)
            ser = UserSerializer(user)
            return Response(data= ser.data , status= status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == "PUT":
        try:
            user = User.objects.get(pk = id)
            reqSer = ChangePasswordSerializer(data= request.data, instance=user)
            if reqSer.is_valid():
                reqSer.save()
                return Response(data= reqSer.data, status= status.HTTP_200_OK)
            return Response(reqSer.errors, status= status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)
    
    elif request.method == "DELETE":
        try:
            user = User.objects.get(pk = id)
            if request.user.type in ["Developer"]:
                user.delete()
                return Response(status= status.HTTP_204_NO_CONTENT)
            user.is_deleted = True
            user.save()
            return Response(status= status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)