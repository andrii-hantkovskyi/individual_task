import jwt
from jwt import InvalidSignatureError
from starlette.authentication import AuthenticationBackend, AuthenticationError

import settings
from users.services import get_user_by_email


class BearerTokenAuthBackend(AuthenticationBackend):
    """
    This is a custom auth backend class that will allow you to authenticate your request and return auth and user as
    a tuple
    """

    async def authenticate(self, request):
        if "Authorization" not in request.headers:
            return

        auth = request.headers["Authorization"]
        try:
            scheme, token = auth.split()
            if scheme.lower() != 'bearer':
                return
            decoded = jwt.decode(
                token,
                settings.SECRET_TOKEN,
                algorithms=[settings.JWT_ALGORITHM],
                options={"verify_aud": False},
            )
        except (ValueError, UnicodeDecodeError, InvalidSignatureError) as exc:
            raise AuthenticationError('Invalid JWT Token.')

        email: str = decoded.get("email")
        user = await get_user_by_email(email)
        if user is None:
            raise AuthenticationError('Invalid JWT Token.')
        return auth, user
