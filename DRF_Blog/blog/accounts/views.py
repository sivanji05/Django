
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status




from .serializer import RegisterSerializer,LoginSerializer

class RegisterView(APIView):

    def post(self,request):
        try:
            data=request.data
            serializer=RegisterSerializer(data=data)

            if not serializer.is_valid():
                return Response({
                    'data':serializer.errors,
                    'message':'something went wrong'
                },status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            return Response({
                'data':{},
                'message':"Your account is created Successfully"
            },status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'data':{},
                'message':"An error occurred"
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class LoginView(APIView):
    def post(self,request):
        try:
            data=request.data
            serializer=LoginSerializer(data=data)

            if not serializer.is_valid():
                return Response({
                    'data':serializer.errors,
                    'message':'somthing went wrong'
                },status=status.HTTP_400_BAD_REQUEST)
            
            response=serializer.get_jwt_token(serializer.validated_data)
            
            return Response(response,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({
                    'data':{},
                    'message':'somthing went wrong'
                },status=status.HTTP_400_BAD_REQUEST)

