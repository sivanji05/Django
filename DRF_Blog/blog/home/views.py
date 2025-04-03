from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BlogSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.core.paginator import Paginator

from .models import Blog
from django.db.models import Q



class publicView(APIView):
    def get(self,request):
        try:
          
            blogs=Blog.objects.all()

            if request.GET.get('search'):
                search=request.GET.get('search')
                blogs=blogs.filter(Q(title__icontains= search)| Q(blog_text__icontains= search))


            page_number=request.GET.get('page',1)
            paginator= Paginator(blogs,1)


            
            # serializer=BlogSerializer(paginator.page(page_number),many=True)

            try:
                paginated_blogs = paginator.page(page_number)
                serializer = BlogSerializer(paginated_blogs, many=True)  # Ensure serializer is always defined
            except:
                return Response({
                    'data': [],
                    'message': 'Invalid page number: No more pages available.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({
                    'data':serializer.data,
                    'message':'blogs fetched successfully'
                      },status=status.HTTP_200_OK)
        except:
            return Response({
                    'data':serializer.errors,
                    'message':'Invalid page'
                      },status=status.HTTP_400_BAD_REQUEST)
        


class  BlogView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]


    def get(self,request):

        try:
            # data=request.data
            # data['user']=request.user.id
            blogs=Blog.objects.filter(user=request.user)

            if request.GET.get('search'):
                search=request.GET.get('search')
                blogs=blogs.filter(Q(title__icontains= search)| Q(blog_text__icontains= search))


            serializer=BlogSerializer(blogs,many=True)
            
            return Response({
                    'data':serializer.data,
                    'message':'blogs fetched successfully'
                      },status=status.HTTP_200_OK)
        except:
            return Response({
                    'data':serializer.errors,
                    'message':'somthing went wrong'
                      },status=status.HTTP_400_BAD_REQUEST)


    def post(self,request):
        try:
            data=request.data
            data['user']=request.user.id
            serializer=BlogSerializer(data=data)

            if not serializer.is_valid():
                return Response({
                    'data':serializer.errors,
                    'message':'somthing went wrong',
                },status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            return Response({
                    'data':serializer.data,
                    'message':'blog created sucessfully',
                },status=status.HTTP_201_CREATED)


        except Exception as e:
            print(e)
            return Response({
                    'data':{},
                    'message':'somthing went wrong',
                },status=status.HTTP_400_BAD_REQUEST)
        

    def patch(self,request):
        try:
            data=request.data
            blog=Blog.objects.filter(uid=data.get('uid'))

            if not blog.exists():
                return Response({
                    'data':{},
                    'message':'Invaild blog uid'
                },status=status.HTTP_308_PERMANENT_REDIRECT)

            if request.user!=blog[0].user:
                return Response({
                    'data':{},
                    'message':'You are not authorized to this blog'
                },status=status.HTTP_401_UNAUTHORIZED)
            
            serializer=BlogSerializer(blog[0],data=data,partial=True)

            if not serializer.is_valid():
                return Response({
                    'data':serializer.errors,
                    'message':'somthing went wrong',
                },status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            return Response({
                    'data':serializer.data,
                    'message':'blog updated sucessfully',
                },status=status.HTTP_201_CREATED)
        
        except Exception as e:
            print(e)
            return Response({
                    'data':{},
                    'message':'somthing went wrong',
                },status=status.HTTP_400_BAD_REQUEST)
        


    def delete(self,request):
        try:
            data=request.data
            blog=Blog.objects.filter(uid=data.get('uid'))

            if not blog.exists():
                return Response({
                    'data':{},
                    'message':'Invaild blog uid'
                },status=status.HTTP_400_BAD_REQUEST)
            
            if request.user != blog[0].user:
                return Response({
                    'data':{},
                    'message':'You are not authorized to this blog'
                },status=status.HTTP_401_UNAUTHORIZED)
            

            blog[0].delete()

            return Response({
                'data':{},
                'message':'Blog delete sucessfully'
            },status=status.HTTP_200_OK)
        
        except:
            return Response({
                'data':{},
                'message':'somthing went wrong'
            },status=status.HTTP_400_BAD_REQUEST)



        
           
