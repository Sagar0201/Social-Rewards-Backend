from django.urls import path
from .views import LoginAPIView,UserSignUpAPIView,UserProfileAPIView , AppCategoryListAdminOnly, AppAPIView,UserAppTaskListCreateAPIView,UserAppTaskApproveRejectAPIView,SingleAppAPIView

urlpatterns = [
    
    # ✅ Auth APIs
    path('auth/login/', LoginAPIView.as_view(), name='login'),              # POST: Login and get token
    path('auth/signup/', UserSignUpAPIView.as_view(), name='signup'),              # POST: Register new user
    path('auth/profile/', UserProfileAPIView.as_view(), name='user-profile'), # POST : Update user profile

    # ✅ App Category (Admin Only)
    path('categories/', AppCategoryListAdminOnly.as_view(), name='categories'), # GET
    
    
    # ✅ Apps
    path('apps/', AppAPIView.as_view(), name='app-list-create'),            # GET: Authenticated users | POST: Admin only
    path('apps/<int:pk>/', SingleAppAPIView.as_view(), name='single-app'), # Get APP Data 
    
    # ✅ App Task
    path('tasks/', UserAppTaskListCreateAPIView.as_view(), name='task-list-create'),  # POST for user | user get thier own tasks | admin user get all tasks
    path('tasks/<int:pk>/update-status/', UserAppTaskApproveRejectAPIView.as_view(), name='task-status-update'), # admin user Approve Tasks
        
    
]
