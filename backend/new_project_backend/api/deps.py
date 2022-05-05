from fastapi.security import OAuth2PasswordBearer

oauth2_password_bearer = OAuth2PasswordBearer(tokenUrl='api/token')
