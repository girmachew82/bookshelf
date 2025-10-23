from rest_framework import serializers
from .models import Publisher, Book
from django.utils import timezone
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model

User = get_user_model()

class AdminUserSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Group.objects.all(),
        required=False
    )
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        # Include `groups` for admin to assign roles
        fields = ('id', 'username', 'email', 'is_staff', 'groups','password')
    # --- CRITICAL FIX: Override create method to hash password ---
    def create(self, validated_data):
        # Pop the password before creating the user object
        password = validated_data.pop('password', None)
        
        # Create the user instance without the password first
        user = User.objects.create(**validated_data)
        
        # Use set_password() which handles hashing, then save the user
        if password is not None:
            user.set_password(password)
            user.save()
            
        return user

    # Optional: Override update method to handle password changes during PATCH/PUT
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        
        # If a new password is provided, hash it
        if password is not None:
            instance.set_password(password)
            
        # Call the parent update method to handle other fields
        return super().update(instance, validated_data)

class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Permission.objects.all()
    )
    class Meta:
        model = Group
        fields = ('id', 'name', 'permissions')

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name', 'codename')

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields ='__all__'



class BookWriteSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        max_length=255,
        allow_blank=False,
        error_messages={
            "blank": "Please provide a book title.",
            "required": "Book title is required."
        }
    )    
    class Meta:
        model = Book
        fields = ['publisher','title','author','published_year','price']
    def validate_published_year(self, value):
        if value.year > timezone.now().year:
            raise serializers.ValidationError("Published year cannot be in the future.")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be a positive number.")
        return value        

class BookReadSerializer(serializers.ModelSerializer):
    publisher = serializers.StringRelatedField()
    class Meta:
        model = Book
        fields = ['id','publisher','title','author','published_year','price']