import jwt
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.exceptions import NotAuthenticated


def get_token_for_user(user: User = None, scope: str = "authentication"):
    """
        Generate a new signed token containing for a specified user & scope
    """
    data = {
        "user_%s_id" % scope: str(user.pk),
    }
    return jwt.encode(data, settings.SECRET_KEY)


def get_user_for_token(token: str = "", scope: str = "authentication"):
    """
        Extract user for the given token & scope.
    """

    # token validation
    try:
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.DecodeError:
        raise NotAuthenticated("Invalid token")

    # returns a user instance of the user_id stored in token
    try:
        user = User.objects.get(pk=data["user_%s_id" % scope])
    except:
        raise NotAuthenticated("Invalid token")
    else:
        return user
