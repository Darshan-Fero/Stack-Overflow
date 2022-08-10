from rest_framework_simplejwt.tokens import RefreshToken

def generate_token(user):
    token = RefreshToken.for_user(user)
    token = str(token.access_token)
    return token