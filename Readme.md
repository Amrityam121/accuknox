# Run  docker-compose build -> docker_compose up -d -> docker exec -it container_id bash -> Run python manage.py migrate

#when signup or login Authorization should be -> no-auth 



# signup users
#example : { "email": "sachin@example.com","password": "securepassword123","first_name" : "sachin",  "last_name" : "gandhi"}

  
  
  



#Note: Do not add token directly in Authorization -> berear token as it send  "berear Token 32a95236c090b2d2e11e089914fca8c112219efc"  
#where bearer is non editable to avoid this do below steps:

#put the token in  - Authorization -> select API key -> add key = Authorization , value = Token 32a95236c090b2d2e11e089914fca8c112219efc (its example)

#login with email and password to get get token  example: { "email": "sachin@example.com","password": "securepassword123"}






#search api :
#pass search query in request in url example - http://0.0.0.0:8000/api/search?search=rajat


#friend request api's

#after you login as any dummy user friendships will be created between him and other users by following api's :

# api/send-friend-request/<int:to_user_id>/   -> api is used to send example api/send-friend-request/1/ -> where 1 is id of my user you created earlier

#in above api's response you will recieve friendship relation key named friends_request_ids use these ids to accept or reject requests 
#for bellow api's:

#api/accept-friend-request/<int:friend_request_id>/
# api/reject-friend-request/<int:friend_request_id>/



#pending friend request api can be used to get pending request for the user to take action on :

#api/pending-friend-request/












