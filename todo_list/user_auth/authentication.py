import re
from rest_framework.authentication import BasicAuthentication

from .tokens import get_user_for_token


class UserTokenAuthentication(BasicAuthentication):
    """
        JWT based stateless authentication.
    """

    auth_rx = re.compile(r"^Token (.+)$")

    def authenticate(self, request):
        token_rx_match = self.auth_rx.search(request.headers.get('Authorization', ''))
        if not token_rx_match:
            return None

        token = token_rx_match.group(1)
        user = get_user_for_token(token)

        return user, token

    def authenticate_header(self, request):
        return 'Token realm="api"'
