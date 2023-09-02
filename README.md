# Little Lemon Back-End Documentation

Front-end repo: https://github.com/cyruscsc/little-lemon-frontend

## Dependency Packages

- `django`
- `djangorestframework`
- `django-cors-headers`
- `whitenoise`
- `mysqlclient`
- `pyjwt`

## Database Structure

The project utilizes the MySQL database. Besides the Django default `User` model, 3 other models, namely `Category`, `Menu`, and `Booking` are created to store and manage data.

### Entity Relationship Diagram

![Little Lemon Back-End ERD](/images/little-lemon-erd-bg.png)

## User Authentication

The app uses cookie-based JSON Web Token (JWT) for user authentication. Code file: `restaurant/jwtauth.py`.

Basic user data is stored in the payload of the token. Therefore, there is no need to authenticate the user with the database every time a request is made once a user is successfully logged in.
The JWT authentication mechanism of the restaurant app consists of an access token and a refresh token. It also implements refresh token rotation to offer more convenience to users.
The logics of registration, login, logout, and user retrieval are handled by `RegisterView`, `LoginView`, `LogoutView`, and `UserView` in `restaurant/views.py` respectively.

`jwtauth.py` is written to be reusable in other Django apps or projects.

### Quick Start

**Imports required:**

```py
# myapp/views.py

from rest_framework.response import Response
from .jwtauth import JwtToken, ACCESS_TOKEN_COOKIE_KEY, REFRESH_TOKEN_COOKIE_KEY
```

The `Response` class from DRF is used to send responses and set necessary cookies back to the client. It is interchangeable with similar classes or functions, such as `HttpResponse` from Django.
The `ACCESS_TOKEN_COOKIE_KEY` and `REFRESH_TOKEN_COOKIE_KEY` are two constants used as the keys of setting cookies.

**Validate a request:**

For any request that authentication is required, simply pass the request object as the parameter to create an instance of the `JwtToken` class.
Then, call the `is_valid()` method to validate the request user.

Example code snippet:

```py
# myapp/views.py

jwt_token = JwtToken(request)
if jwt_token.is_valid():
    print("Authenticated user")
else:
    print("Unauthenticated user")
```

`is_valid()` returns `True` if
- _access token_ and _refresh token_ are valid, or
- _access token_ is expired but _refresh token_ is valid (both tokens are refreshed automatically)

`is_valid()` returns `False` if
- _refresh token_ is expired, or
- either _access token_ or _refresh token_ is not found

Conditional statements can be used to handle the results of `is_valid()` method. For example, proceeding with the request upon `True` value, or raising exception upon `False` value.

**Issue a token:**

Same as above, an instance of `JwtToken` is required to call the `issue()` method.

Example code snippet:

```py
# myapp/views.py

user = authenticate(username=username, password=password)

jwt_token = JwtToken(request)
jwt_token.issue(user.id, user.username, user.email, user.is_staff)
```

The `issue()` method takes 4 parameters, namely `user_id`, `username`, `email`, `is_staff`. These are the user data to be stored in the payload of the tokens.
It is strongly recommanded to authenticate the user before issuing a new token. In the example above, the `authenticate()` method from `django.contrib.auth` is responsible for this job.

**Get user data**

The `get_user()` method returns all user data in the token's payload in a tuple.

Example code snippet:

```py
# myapp/views.py

jwt_token = JwtToken(request)
if jwt_token.is_valid():
    user_id, username, email, is_staff = jwt_token.get_user()
    print(f"Hi {username}!")
else:
    print("Unauthenticated user")
```

Of course, it is important to validate the request before getting any user data.

**Set cookies**

In order to get the most out of this JWT authentication, the tokens have to be set in the client's cookies. It can be done with the `set_cookie()` method of the `Response` class from DRF.
Setting cookies with `httponly=True` is a more secure approach.

Example code snippet:

```py
# myapp/views.py

jwt_token = JwtToken(request)
response = Response()

if jwt_token.is_valid():
    response.data = {
        "message": "Cookies set",
    }
    response.set_cookie(key=ACCESS_TOKEN_COOKIE_KEY, value=jwt_token.access_token, httponly=True)
    response.set_cookie(key=REFRESH_TOKEN_COOKIE_KEY, value=jwt_token.refresh_token, httponly=True)
else:
    response.data = {
        "message": "Unauthenticated user",
    }

return response
```

On the contrary, to delete the tokens stored in cookies, an easy way is to set the cookies with same key but empty value as well as a very short _max_age_.

Example code snippet:

```py
# myapp/views.py

response = Response()
response.data = {
    "message": "Cookies deleted",
}
response.set_cookie(key=ACCESS_TOKEN_COOKIE_KEY, value='', max_age=1, httponly=True)
response.set_cookie(key=REFRESH_TOKEN_COOKIE_KEY, value='', max_age=1, httponly=True)
```

## API Endpoints

### User Authentication Related Endpoints

| Method | Path               | Parameters                    | Description                               |
| ------ | ------------------ | ----------------------------- | ----------------------------------------- |
| `POST` | /api/checkusername | username                      | Check if the username is available or not |
| `POST` | /api/checkemail    | email                         | Check if the email is available or not    |
| `POST` | /api/register      | username<br>email<br>password | Register a new user                       |
| `POST` | /api/login         | username<br>password          | Log in an existing user                   |
| `POST` | /api/logout        | none                          | Log out the current user                  |
| `GET`  | /api/user          | none                          | Get the current user's data               |

### Content Related Endpoints

| Method   | Path               | Parameters                                               | Description                                   |
| -------- | ------------------ | -------------------------------------------------------- | --------------------------------------------- |
| `GET`    | /api/menu          | none                                                     | Get all menu items                            |
| `GET`    | /api/menu/{id}     | none                                                     | Get a specific menu item                      |
| `GET`    | /api/bookings      | none                                                     | Get all bookings of the current user          |
| `POST`   | /api/bookings      | email<br>num_guests<br>date (yyyy-mm-dd)<br>time (hh:mm) | Create a new booking for the current user     |
| `GET`    | /api/bookings/{id} | none                                                     | Get a specific booking of the current user    |
| `DELETE` | /api/bookings/{id} | none                                                     | Delete a specific booking of the current user |
