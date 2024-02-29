from django.shortcuts import render
from .models import User
from .serializer import UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login
# Create your views here.

class RegisterAPIView(APIView):
    def post(self, request):
        phone = request.data.get("phone")
        if not phone:
            return Response({"error" : "Phone number is required"})

        if len(phone) != 13:
            return Response({"error" : "Bunday telefon raqam mavjud emas"})
        
        user = User.objects.filter(phone = phone).last()

        if user:
            return Response({"error" : "Bunday foydalanuvchi mavjud"})
        else:
            serializer = UserSerializer(data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response({'message': serializer.data})
        
class LoginAPIView(APIView):
    def get(self, request):
        phone = request.data.get("phone")
        if not phone:
            return Response({"error" : "Phone number is required"})

        if len(phone) != 13:
            return Response({"error" : "Bunday telefon raqam mavjud emas"})
        
        user = User.objects.filter(phone = phone).last()

        if not user:
            return Response({"error" : "Bunday foydalanuvchi mavjud emas"})
        else:
            login(request, user)

 
        
        return Response({'message': "Login successfull" })
        

 