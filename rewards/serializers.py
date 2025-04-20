# from rest_framework import serializers
# from .models import App, UserAppTask, UserProfile, AppCategory, AppSubCategory
# from django.contrib.auth.models import User



# class AppCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AppCategory
#         fields = ['id', 'name']


# class AppSubCategorySerializer(serializers.ModelSerializer):
#     category = AppCategorySerializer(read_only=True)
#     category_id = serializers.PrimaryKeyRelatedField(
#         queryset=AppCategory.objects.all(), write_only=True, source='category'
#     )

#     class Meta:
#         model = AppSubCategory
#         fields = ['id', 'name', 'category', 'category_id']
        
        

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'first_name', 'last_name']

# class UserProfileSerializer(serializers.ModelSerializer):
#     user = UserSerializer()
    
#     class Meta:
#         model = UserProfile
#         fields = ['user', 'points', 'phone']

# class AppSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = App
#         fields = '__all__'



# class UserAppTaskSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserAppTask
#         fields = ['id', 'app', 'screenshot', 'status', 'created_at']
#         read_only_fields = ['status', 'created_at']

# class AdminTaskUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserAppTask
#         fields = ['status']
        
        
        

# class UserRegistrationSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#     phone = serializers.CharField(write_only=True)
    
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password', 'phone']
    
#     def create(self, validated_data):
#         phone = validated_data.pop('phone')
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             password=validated_data['password']
#         )
#         UserProfile.objects.create(user=user, phone=phone)
#         return user




from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import AppCategory, AppSubCategory, App, UserAppTask, UserProfile



#############################################
            # Login Serializer 
#############################################



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User is inactive.")
                data['user'] = user
            else:
                raise serializers.ValidationError("Invalid username or password.")
        else:
            raise serializers.ValidationError("Both username and password are required.")
        print(user)
        return data
    
    
    
    
#############################################
            # SignUp Serializer 
#############################################


class UserSignUpSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'phone']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        phone = validated_data.pop('phone', '')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, phone=phone)
        return user
    
    
    
    
#############################################
            # Profile Serializer 
#############################################

class UserProfileSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source='userprofile.phone')
    points = serializers.IntegerField(source='userprofile.points')

    class Meta:
        model = User
        fields = ['id', 'username','is_staff', 'first_name', 'last_name', 'email', 'phone', 'points']
        
        
        

        
#############################################
            # Sub Category Serializer 
#############################################


class AppSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AppSubCategory
        fields = ['id', 'name']
        
        
        
#############################################
            # Category Serializer 
#############################################  
    
class AppCategorySerializer(serializers.ModelSerializer):
    subcategories = AppSubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = AppCategory
        fields = ['id', 'name', 'subcategories']
        
        
#############################################
            # App Serializer 
#############################################

class AppSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = App
        fields = '__all__'
        
        
    def get_logo_url(self, obj):
        request = self.context.get('request', None)
        if request and obj.logo:
            return request.build_absolute_uri(obj.logo.url)
        elif obj.logo:
            return obj.logo.url  # fallback to relative path
        return None
    
    
        
#############################################
            # App Task Serializer 
#############################################
class UserAppTaskSerializer(serializers.ModelSerializer):
    app_name = serializers.CharField(source='app.name', read_only=True)
    app_points = serializers.IntegerField(source='app.points', read_only=True)

    class Meta:
        model = UserAppTask
        fields = ['id', 'user', 'app', 'app_name', 'app_points', 'screenshot', 'status', 'created_at']
        read_only_fields = ['user', 'status', 'created_at']  # 👈 user made read-only
        
    def update(self, instance, validated_data):
        """
        Override the update method to handle file upload properly
        when a screenshot is provided.
        """
        screenshot = validated_data.get('screenshot', None)
        if screenshot:
            instance.screenshot = screenshot  # Update the screenshot if it's provided
        instance.status = validated_data.get('status', instance.status)  # Optionally update status
        instance.save()
        return instance

        

