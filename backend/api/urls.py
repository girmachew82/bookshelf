from django.urls import path
from .views import PublisherListCreateAPIView, PublisherRetriveUpdateDestroyAPIView, BookListCreateAPIView, BookRetriveUpdateDestroyAPIView, UserViewSet, PermissionListView, GroupViewSet

user_list = UserViewSet.as_view({'get': 'list', 'post': 'create'})
user_detail = UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})

group_list = GroupViewSet.as_view({'get': 'list', 'post': 'create'})
group_detail = GroupViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})

urlpatterns = [
    path('publishers/', PublisherListCreateAPIView.as_view(), name='publisher-list' ),
    path('publishers/<int:pk>/', PublisherRetriveUpdateDestroyAPIView.as_view(), name='publisher-detail'),
    path('books/',BookListCreateAPIView.as_view(), name='list-create-books'),
    path('books/<int:pk>/',BookRetriveUpdateDestroyAPIView.as_view(),name='retrive-update-destroy-book'),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail'),
    path('groups/', group_list, name='group-list'),
    path('groups/<int:pk>/',group_detail, name='group-detail'),
    path('permissions/',PermissionListView.as_view(), name='permission-list'),


]
