from rest_framework_simplejwt.tokens import AccessToken

class CustomAccessToken(AccessToken):
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        token['username'] = user.username
        token['email'] = user.email
        return token
