from django.urls import path
from django.contrib.auth import views as auth_views

from .views import \
(
GroupAdminAPIView,
CreateGroupAPIView,
UpdateGroupAdminAPIView,
CreateSavingAPIView,
UpdateSavingAPIView,
GroupMemberListAPIView,
SearchGroupAPIView,
SendInviteAPIView,
InviteCreateSavingAPIView
)

app_name='savings'

urlpatterns = [
    path('group_admin', GroupAdminAPIView.as_view(), name='is_group_admin'),
    path('update_group/<int:id>', UpdateGroupAdminAPIView.as_view(),name='update_group'),
    path('create_group', CreateGroupAPIView.as_view(), name='create_group'),
    path('create_savings', CreateSavingAPIView.as_view(),name='create_saving'),
    path('update_savings/<int:id>', UpdateSavingAPIView.as_view(),name='update_saving'),
    path('view_members/<str:group_name>', GroupMemberListAPIView.as_view(),name='view_members'),
    path('search_group', SearchGroupAPIView.as_view(),name='search_group'),
    path('send_invite', SendInviteAPIView.as_view(),name='send_invite'),
    path('invite_create_savings/<str:invite>', InviteCreateSavingAPIView.as_view(),name='invite_saving')
]