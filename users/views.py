# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import get_authorization_header
from .serializers import UserSerializer
from .models import User
from .authentication import create_access_token, create_refresh_token, decode_access_token, decode_refresh_token
# from django.contrib.auth import authenticate
from rest_framework import exceptions
# from rest_framework_simplejwt.tokens import RefreshToken
import jwt, datetime

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

# class LoginView(APIView):
#     def post(self, request):
#         email = request.data['email']
#         password = request.data['password']

#         user = User.objects.filter(email=email).first()
#         if user is None:
#             raise AuthenticationFailed("User NOT FOUND !!")
               
#         if not user.check_password(password):
#             raise AuthenticationFailed("Incorrect password")
        
#         #payload = {
#         #    'id': user.id,
#         #    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
#         #    'iat': datetime.datetime.utcnow()            
#         #}
        

#         #token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
#         return Response({
#             'message':'Successfully logged in ..'
#           #  'token' : token
#         })


# class LoginView(APIView):
#     def post(self, request):
#         try:
#             serializer = UserSerializer(data=request.data)
#             if serializer.is_valid():
#                 email = serializer.data['email']
#                 password = serializer.data['password']

#                 userCreds = authenticate(email = email, password = password)
#                 if userCreds is None:
#                     return Response({
#                     'message':'Something went wrong. no user creds found OR invalid creds !!..',
#                     'data': {}
#                     })
                
#                 refresh = RefreshToken.for_user(userCreds)
#                 return Response({
#                     'refresh': str(refresh),
#                     'access': str(refresh.access_token),
#                 })

#             return Response({
#                 'message':'Something went wrong !!..',
#                 'data': serializer.errors
#             #  'token' : token
#             })
    
#         except Exception as e:
#             print(e)
#             return Response({
#                 'message': 'Something went wrong.',
#                 'data' : e
                
#             })
    


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed("User NOT FOUND !!")
               
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")
        
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        # refreshtoken = RefreshToken.for_user(user)
        response = Response()
        response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
        response.data = {
            'access_token': access_token
        }
        # return Response({
        #     'refresh': str(refreshtoken),
        #     'access': str(refreshtoken.access_token),
        # })
        return response
    

class GetUserDataFromToken(APIView):
    def get(self, request):
        try:             
            # get access token from the header
            auth = get_authorization_header(request).split()
            if auth and len(auth) == 2:
                access_token = auth[1].decode('utf-8')
                id = decode_access_token(access_token)
                user = User.objects.filter(pk=id).first()
                return Response(UserSerializer(user).data)
        except:
            raise exceptions.AuthenticationFailed('unauthenticated')

   
class CreateNewAccessToken(APIView):
    def post(self, request):
        getRefreshToken = request.COOKIES.get('refreshtoken')
        id = decode_refresh_token(getRefreshToken)
        access_token = create_access_token(id)
        return Response ({
            'access_token': access_token
        })