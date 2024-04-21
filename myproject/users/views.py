# users/views.py
from rest_framework import status ,filters,generics
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth import authenticate,get_user_model

from rest_framework.authentication import TokenAuthentication
from django.shortcuts import HttpResponse
from .models import FriendRequest, Friendship

from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token

from rest_framework.views import APIView

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from django_ratelimit.decorators import ratelimit
from django.http import JsonResponse
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    if request.method == 'POST':

        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            token  = Token.objects.get_or_create(user=user)
            return Response({'token': token[0].key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



class UserListView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['email','first_name','last_name']


    

@csrf_exempt
@api_view(['POST'])
@ratelimit(key='ip', rate='3/m', method='POST', block=True)
def send_friend_request(request, to_user_id):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    token = request.headers.get('Authorization').split(" ")[1] 
    Token_obj  = Token.objects.get(key=token)
    to_user = get_user_model().objects.get(id=to_user_id)
    from_user = get_user_model().objects.get(id=Token_obj.user_id)
    old_request =FriendRequest.objects.filter(from_user=from_user, to_user=to_user)
    friends_request_ids = ""
    if not old_request:
        friend_request = FriendRequest.objects.create(from_user=from_user, to_user=to_user)
        friends_request_ids = list(FriendRequest.objects.filter(from_user=Token_obj.user_id,accepted = False,rejected =False).values("id"))
        # print(friends_request_ids,"friend reuest idssssssssssssss")
        response_data = {"status" : "Friend request sent successfully!" , "msg" : "pass friend_request_ids in url in order to accept/reject request", "friend_request_ids" : friends_request_ids }
        return JsonResponse(response_data)
    return HttpResponse({"<h1>Friend request already sent before</h1>"})



@csrf_exempt
@api_view(['POST'])
def accept_friend_request(request, friend_request_id):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    friend_request = FriendRequest.objects.get(id=friend_request_id)
    if friend_request.rejected != True :
        friend_request.accepted = True
        friend_request.save()
        Friendship.objects.create(user1=friend_request.from_user, user2=friend_request.to_user)
        return HttpResponse("<h1>Friend request Accepted</h1>")
    return HttpResponse("<h1>Friend request Already Rejected</h1>")


@csrf_exempt
@api_view(['POST'])
def reject_friend_request(request, friend_request_id):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    friend_request = FriendRequest.objects.get(id=friend_request_id)
    if friend_request.accepted != True:
        friend_request.rejected = True
        friend_request.save()
        return HttpResponse("<h1>Friend request Rejected</h1>")
    return HttpResponse("<h1>Friend request Already Accepted</h1>")
    


@csrf_exempt
@api_view(['POST'])    
@ratelimit(key='ip', rate='3/m')
def friend_request_pending(request):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    token = request.headers.get('Authorization').split(" ")[1] 
    Token_obj  = Token.objects.get(key=token)
    pending_request = FriendRequest.objects.filter(from_user_id=Token_obj.user_id,accepted = False ,rejected = False).values("to_user_id")

    return Response({'msg': pending_request}, status=status.HTTP_200_OK)





@csrf_exempt
@api_view(['POST'])    
@ratelimit(key='ip', rate='3/m')
def friend_list(request):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    token = request.headers.get('Authorization').split(" ")[1] 
    Token_obj  = Token.objects.get(key=token)
    friends = FriendRequest.objects.filter(from_user_id=Token_obj.user_id,accepted = True ,rejected = False).values("to_user_id")

    return Response({'msg': friends}, status=status.HTTP_200_OK)

