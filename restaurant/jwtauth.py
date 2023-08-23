import jwt, datetime

JWT_SECRET = 'This is not a secret'
JWT_ALGORITHMS = ['HS256']
ACCESS_MAX_AGE = 60 * 5
REFRESH_MAX_AGE = 60 * 60 * 24 * 7
ACCESS_TOKEN_COOKIE_KEY = 'jwtaccess'
REFRESH_TOKEN_COOKIE_KEY = 'jwtrefresh'

class JwtToken:

  def __init__(self, request) -> None:
    self.request = request
    self.access_token = request.COOKIES.get(ACCESS_TOKEN_COOKIE_KEY)
    self.refresh_token = request.COOKIES.get(REFRESH_TOKEN_COOKIE_KEY)

  def encode(self, payload, secret=JWT_SECRET, algorithm=JWT_ALGORITHMS[0]) -> object:
    return jwt.encode(payload, secret, algorithm=algorithm)

  def decode(self, token, secret=JWT_SECRET, algorithms=JWT_ALGORITHMS) -> object:
    return jwt.decode(token, secret, algorithms=algorithms, options={'verify_exp': False})

  def is_valid(self) -> bool:
    '''
    Check if the token is valid
    access: valid & refresh: valid -> True
    access: expired & refresh: valid -> refresh token & True
    refresh: expired -> False
    access: None | refresh: None -> False
    '''
    if self.access_token is None or self.refresh_token is None:
      return False
    else:
      pass

    access_token_payload = self.decode(self.access_token)
    refresh_token_payload = self.decode(self.refresh_token)
    access_token_exp = datetime.datetime.utcfromtimestamp(access_token_payload['exp'])
    refresh_token_exp = datetime.datetime.utcfromtimestamp(refresh_token_payload['exp'])
    now = datetime.datetime.utcnow()

    if refresh_token_exp < now:
      return False
    elif access_token_exp < now:
      self.refresh()
      return True
    else:
      return True

  def issue(self, user_id, username, email, is_staff) -> None:
    new_access_token_payload = {
      'user_id': user_id,
      'username': username,
      'email': email,
      'is_staff': is_staff,
      'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=ACCESS_MAX_AGE),
      'iat': datetime.datetime.utcnow(),
    }
    new_refresh_token_payload = {
      'user_id': user_id,
      'username': username,
      'email': email,
      'is_staff': is_staff,
      'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=REFRESH_MAX_AGE),
      'iat': datetime.datetime.utcnow(),
    }
    self.access_token = self.encode(new_access_token_payload)
    self.refresh_token = self.encode(new_refresh_token_payload)

  def refresh(self) -> None:
    '''Refresh token rotation'''
    current_user_id, current_username, current_email, is_staff = self.get_user()
    self.issue(current_user_id, current_username, current_email, is_staff)

  def get_user(self) -> tuple:
    '''Return user_id and username'''
    access_token_payload = self.decode(self.access_token)
    user_id = access_token_payload['user_id']
    username = access_token_payload['username']
    email = access_token_payload['email']
    is_staff = access_token_payload['is_staff']
    return user_id, username, email, is_staff
