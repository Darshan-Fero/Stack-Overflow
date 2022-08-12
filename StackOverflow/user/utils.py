import json
from pydantic import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

def pydantic_validation(Model, data):
    try:
        Model.parse_obj(data)
        return True, ''
    except ValidationError as e:
        list = json.loads(e.json())
        for error in list:
            for loc in (error.get('loc')):
                return False, {str(loc) : str(error.get('msg'))}
            
def generate_token(user):
    token = RefreshToken.for_user(user)
    token = str(token.access_token)
    return token