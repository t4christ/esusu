from django.urls import path
from django.contrib.auth import views as auth_views



from .views import \
(
RegistrationAPIView,
InviteRegistrationAPIView,
UserRetrieveUpdateDeleteAPIView,
LoginAPIView
)
app_name='account'

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='register_user'),
    path('register/<str:invite>', InviteRegistrationAPIView.as_view(), name='register_invite'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('get_users', UserRetrieveUpdateDeleteAPIView.as_view(),name='get_users'),
    path('update_user', UserRetrieveUpdateDeleteAPIView.as_view(),name='update_user'),
    path('delete_account/<int:pk>', UserRetrieveUpdateDeleteAPIView.as_view(),name='delete_user')
]
 
    