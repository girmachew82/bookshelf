from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from rest_framework import generics
from .serializers import PublisherSerializer, BookWriteSerializer, BookReadSerializer, GroupSerializer, PermissionSerializer,AdminUserSerializer
from .models import Publisher, Book
from .filters import BookFilter
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import User

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminUser]
    
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().prefetch_related('permissions')
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]

class PermissionListView(generics.ListAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAdminUser]

class PublisherListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PublisherSerializer
    queryset = Publisher.objects.all()


class PublisherRetriveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.select_related('publisher')

    filter_backends = (DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter)
    filterset_class = BookFilter
    search_fields =['publisher__name','title']
    ordering_fields =['price','published_year','publisher__name','title']

    def get_serializer_class(self):
        if self.request.method =='GET':
            return BookReadSerializer
        return BookWriteSerializer

class BookRetriveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookReadSerializer