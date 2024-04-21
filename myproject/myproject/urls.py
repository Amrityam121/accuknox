"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from users.views import friend_list,signup,login,friend_request_pending,UserListView,send_friend_request, accept_friend_request, reject_friend_request
# from users.views import signup ,login ,UserListView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/signup/', signup, name='signup'),
    path('api/login/', login, name='login'),
    path('api/search/', UserListView.as_view(), name='search'),
    path('api/send-friend-request/<int:to_user_id>/', send_friend_request, name='send_friend_request'),
    path('api/accept-friend-request/<int:friend_request_id>/', accept_friend_request, name='accept_friend_request'),
    path('api/reject-friend-request/<int:friend_request_id>/', reject_friend_request, name='reject_friend_request'),
    path('api/pending-friend-request/', friend_request_pending, name='friend_request_pending'),
    path('api/friends/', friend_list, name='friends'),


]
