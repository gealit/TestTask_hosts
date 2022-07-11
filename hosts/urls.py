from django.contrib.auth.views import LogoutView
from django.urls import path

from hosts.views import LoginUserView, RegisterUserView, HomeView, HostCreateView, HostUpdateView, HostDeleteView, \
    HostUpdateAdminView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('host_create/', HostCreateView.as_view(), name='host-create'),
    path('host_update/<int:pk>', HostUpdateView.as_view(), name='host-update'),
    path('host_update_admin/<int:pk>', HostUpdateAdminView.as_view(), name='host-update-admin'),
    path('host_delete/<int:pk>', HostDeleteView.as_view(), name='host-delete'),
]
