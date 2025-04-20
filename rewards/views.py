# from rest_framework import viewsets, status
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated, IsAdminUser
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.authtoken.models import Token
# from django.contrib.auth.models import User
# from .models import App, UserAppTask, UserProfile,AppCategory, AppSubCategory
# from .serializers import (
#     AppSerializer,
#     UserAppTaskSerializer, 
#     AdminTaskUpdateSerializer,
#     UserRegistrationSerializer,
#     UserProfileSerializer,
#     AppCategorySerializer,
#     AppSubCategorySerializer
# )

# from rest_framework.permissions import AllowAny
# from rest_framework import generics, permissions
# from rest_framework.views import APIView



# class CustomAuthToken(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data,context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token': token.key,
#             'user_id': user.pk,
#             'username': user.username,
#             'is_staff': user.is_staff
#         })
        
        

# class UserRegistrationViewSet(viewsets.GenericViewSet):
#     permission_classes = [AllowAny]
#     serializer_class = UserRegistrationSerializer
    
#     def create(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token': token.key,
#             'user_id': user.pk,
#             'username': user.username,
#             'is_staff': user.is_staff
#         }, status=status.HTTP_201_CREATED)
        
        


# class AppViewSet(viewsets.ModelViewSet):
#     queryset = App.objects.filter(is_active=True)
#     serializer_class = AppSerializer
    
#     def get_permissions(self):
#         if self.action in ['create', 'update', 'partial_update', 'destroy']:
#             permission_classes = [IsAdminUser]
#         else:
#             permission_classes = [IsAuthenticated]
#         return [permission() for permission in permission_classes]
    
    



# # User can submit task
# class UserAppTaskList(APIView):
#     permission_classes = [IsAuthenticated]  # Only authenticated users can access

#     def get(self, request):
#         tasks = UserAppTask.objects.filter(user=request.user)
#         serializer = UserAppTaskSerializer(tasks, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = UserAppTaskSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)  # Assign current user to the task
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # Admin User
# class AdminTaskViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     Admin-only ViewSet to manage user-submitted app tasks.
#     """
#     queryset = UserAppTask.objects.all()
#     serializer_class = UserAppTaskSerializer
#     permission_classes = [permissions.IsAdminUser]

#     @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAdminUser])
#     def update_status(self, request, pk=None):
#         task = self.get_object()
#         serializer = AdminTaskUpdateSerializer(task, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'Status updated successfully'})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






# class UserProfileViewSet(viewsets.GenericViewSet):
#     serializer_class = UserProfileSerializer
#     permission_classes = [IsAuthenticated]
    
#     def retrieve(self, request):
#         profile = request.user.userprofile
#         serializer = self.get_serializer(profile)
#         return Response(serializer.data)
    
#     @action(detail=False, methods=['get'])
#     def points(self, request):
#         profile = request.user.userprofile
#         return Response({'points': profile.points})

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser


from .serializers import LoginSerializer, UserSignUpSerializer,UserProfileSerializer , AppCategorySerializer, AppSubCategorySerializer, AppSerializer, UserAppTaskSerializer
from .models import AppCategory, AppSubCategory, App,UserAppTask,UserProfile




################################################
                # User Login API
################################################

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        """
        Authenticate user and return a token if successful.
        """
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']  # Get the authenticated user
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                'user_id':user.id,
                'username':user.username,
                'is_staff':user.is_staff
                }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





################################################
                # User SignUp API
################################################


class UserSignUpAPIView(APIView):
    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
################################################
                    # Profile API
################################################


class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)



    
    
################################################
                # Admin User Check API
################################################

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
    
    
################################################
                # APP Category API
################################################

class AppCategoryListAdminOnly(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        categories = AppCategory.objects.all()
        serializer = AppCategorySerializer(categories, many=True)
        return Response(serializer.data)

    
################################################
                    # APP API
################################################


class AppAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]  # Only logged-in users can view
        return [permissions.IsAdminUser()]  # Only admin can add

    def get(self, request):
        apps = App.objects.filter(is_active=True)
        serializer = AppSerializer(apps, many=True, context={'request': request})
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AppSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    

class SingleAppAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        if request.user.is_staff:
            return Response({'error': 'Admins are not allowed to access this endpoint'}, status=status.HTTP_403_FORBIDDEN)

        try:
            app = App.objects.get(pk=pk, is_active=True)
            serializer = AppSerializer(app, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except App.DoesNotExist:
            return Response({'error': 'App not found'}, status=status.HTTP_404_NOT_FOUND)
    
    

class AppDetailAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]  # Only admin can update/delete

    def put(self, request, pk):
        app = get_object_or_404(App, pk=pk)
        serializer = AppSerializer(app, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        app = get_object_or_404(App, pk=pk)
        app.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
################################################
                    # App Task API
################################################
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError

class UserAppTaskListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # for handling screenshots

    def get(self, request):
        # Admin sees all tasks, user sees only their own
        if request.user.is_staff:
            tasks = UserAppTask.objects.all()
        else:
            tasks = UserAppTask.objects.filter(user=request.user)

        serializer = UserAppTaskSerializer(tasks, many=True)
        return Response(serializer.data)

    

    
    
    def post(self, request):
        print('POST DATA:', request.data)
        print('FILES:', request.FILES)
        
        if request.user.is_staff:
            return Response({"detail": "Admins cannot submit tasks."}, status=status.HTTP_403_FORBIDDEN)

        # Check if the user has already submitted a task for this app
        existing_task = UserAppTask.objects.filter(user=request.user, app=request.data.get('app')).first()

        if existing_task:
            # If task exists, update the screenshot if provided
            if 'screenshot' in request.FILES:
                existing_task.screenshot = request.FILES['screenshot']
                existing_task.status = 'pending'  # You may also reset the status if needed
                existing_task.save()
                return Response(UserAppTaskSerializer(existing_task).data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Screenshot must be provided for updating the task."}, status=status.HTTP_400_BAD_REQUEST)

        # If no existing task, create a new one
        serializer = UserAppTaskSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                serializer.save(user=request.user)  # Attach the authenticated user
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                raise ValidationError({"non_field_errors": ["You've already submitted a task for this app."]})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserAppTaskApproveRejectAPIView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        task = get_object_or_404(UserAppTask, pk=pk)
        new_status = request.data.get("status")

        if new_status not in ['approved', 'rejected', 'completed']:
            return Response({"detail": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        task.status = new_status
        task.save()
        return Response({"detail": f"Task status updated to {new_status}."})
    
    
    
