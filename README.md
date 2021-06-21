# ChatTest

# Run using docker-compose

```

cp .example.env .env
docker-compose up

```

# Run without using docker

```

# for creating virtual environment
virtualenv -p python3 env

# to activate env
source env/bin/activate

# go into app folder then run
pip install -r requirement.txt

# Create db named "groupchatdb" in PostgreSQL then run migrations
python manage.py migrate

```

## Run Django server

```
#To run server
python manage.py runserver

```

## To run test cases

```
# To run coverage 
coverage run manage.py test

# To check coverage report
coverage report -m --omit="*/env/*"

```

# Usage

## Create Superuser
```
# Create superuser using below command
python manage.py createsuperuser

```

# API Endpoints

## User App API

1. User login API - "/login/"
    - POST params used : "username", "password"
    ```
    curl --location --request POST 'http://localhost:8000/login/' \
    --header 'Authorization: Token 77c912677bf464d3ea113fca745d6911d1c6a036' \
    --form 'username="<username>"' \
    --form 'password="<password>"'
    ```

2. User logout API - "/logout/"
    - GET - No params used.
    ```
    curl --location --request GET 'http://localhost:8000/logout/' \
    --header 'Authorization: Token <Your Token>' 
    ```

3. User list API - "/user-list/"
    - GET - No params used.
    ```
    curl --location --request GET 'http://localhost:8000/user-list/' \
    --header 'Authorization: Token <Your Token>' 
    ```

4. User create API - "/user-create/"
    - POST params used : ["first_name", "username", "last_name", "email", "password"]
    ```
    curl --location --request POST 'http://localhost:8000/user-create/' \
    --header 'Authorization: Token <Your Token>' \
    --form 'first_name="user"' \
    --form 'last_name="1"' \
    --form 'email="user1@gmail.com"' \
    --form 'password="password"' \
    --form 'is_active="True"'
    ```

5. User Detail API - "/user/<int:pk>/"
    - GET - No params used.
    ```
    curl --location --request GET 'http://localhost:8000/user/<user_id>/' \
    --header 'Authorization: Token <Your Token>' 
    ```
    - PUT params used : ["first_name", "username", "last_name", "email", "password" ]
    ```
    curl --location --request PUT 'http://localhost:8000/user/<user_id>/' \
    --header 'Authorization: Token <Your Token>' \
    --form 'first_name="user"' \
    --form 'last_name="1"' \
    --form 'email="user1@gmail.com"' \
    --form 'is_active="True"'
    ```

    - DELETE - No params used.
    ```
    curl --location --request DELETE 'http://localhost:8000/user/<user_id>/' \
    --header 'Authorization: Token <Your Token>' 
    ```

## Chat App API

1. Group List API - "/chat/group-list/"
    - GET - No params used.
    ```
    curl --location --request GET 'http://localhost:8000/chat/group-list/' \
    --header 'Authorization: Token <Your Token>' 
    ```

2. Group create API - "/chat/group-create/"
    - POST params used : ["title", "is_private", "members"]
    ```
    curl --location --request POST 'http://localhost:8000/chat/group-create/' \
    --header 'Authorization: Token <Your Token>' \
    --form 'title="<Group Name>"' \
    --form 'members="<user id>"' \
    --form 'members="<user id>"' \
    --form 'is_private="False"'
    ```

3. Group Detail API - "/chat/group/<int:pk>/"
    - GET - No params used.
    ```
    curl --location --request GET 'http://localhost:8000/chat/<group_id>/' \
    --header 'Authorization: Token <Your Token>' 
    ```

    - PUT params used : ["title", "is_private", "members"]
    ```
    curl --location --request PUT 'http://localhost:8000/chat/group/<group_id>/' \
    --header 'Authorization: Token <Your Token>' \
    --form 'title="<Group Name>"' \
    --form 'members="<user id>"' \
    --form 'members="<user id>"' \
    --form 'is_private="False"'
    ```    

    - DELETE - No params used.
    ```
    curl --location --request DELETE 'http://localhost:8000/chat/group/<group_id>/' \
    --header 'Authorization: Token <Your Token>' 
    ```

4. Add/Delete Group Member API - "/chat/group/<int:pk>/member/"
    - GET - No params used.
    ```
    curl --location --request GET 'http://localhost:8000/chat/group/<group_id>/member/' \
    --header 'Authorization: Token <Your Token>' 
    ```
    - PUT params used : ["members"] = List of user ids
    ```
    curl --location --request PUT 'http://localhost:8000/chat/group/<group_id>/member/' \
    --header 'Authorization: Token <Your Token>' \
    --form 'members="<user id>"' \
    --form 'members="<user id>"'
    ```

5. Group Chat API - "/chat/group/<int:pk>/chat/"
    - GET - No params used.
    ```
    curl --location --request GET 'http://localhost:8000/chat/group/<group_id>/chat/' \
    --header 'Authorization: Token <Your Token>' 
    ```
    - POST params used : ["message"] = "Any Text as message"
    ```
    curl --location --request POST 'http://localhost:8000/chat/group/<group_id>/chat/' \
    --header 'Authorization: Token <Your Token>' \
    --form 'message="Hi I am John"'
    ```

6. Group Message Like/Dislike API - "/chat/group/<int:group_id>/message/<int:msg_id>/"   
    - GET - No params used.
    ```
    curl --location --request GET 'http://localhost:8000/chat/group/<group_id>/message/<msg_id>/' \
    --header 'Authorization: Token <Your Token>' 
    ```
    - POST - No params used. = like/Unlike operation performed
    ```
    curl --location --request POST 'http://localhost:8000/chat/group/<group_id>/message/<msg_id>/' \
    --header 'Authorization: Token <Your Token>' 
    ```


# what a:
## Superuser/Admin can do
* He can Create/Edit/Delete/Get "User" details
* He can Create/Edit/Delete/Get "Group" details
* He can Add/Remove user from a Group
* He can Like/Unlike a message in a Group

## Normal User can do
* He can Create/Edit/Delete/Get "Group" details
* He can Add/Remove user from a Group
* He can Like/Unlike a message in a Group

# What more can be done(Future Scope):
## In User App
* User can view and edit his details like first_name, last_name, password etc
* User can deactivate his account

## In Chat App
* User can create a private group chat.
* Normal User can act has group admin, can give permissions to member users to perform few actions.
* Group can have multiple admins.
* User can send other that text messages (emojis, media files, docs etc)
* Can Implement send/recieve messages using Websockets
