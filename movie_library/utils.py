from functools import wraps
import bcrypt
from django.http import JsonResponse
import jwt
from users.models import Users
import datetime
from pytz import timezone
from movie_library.settings import JWT_SECRET_KEY


def hash_pw(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def check_pw(password: str, hash_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hash_password.encode("utf-8"))


def create_access_token(user: Users):
    ist = timezone("Asia/Kolkata")
    iat = datetime.datetime.now(ist)
    return jwt.encode(
        payload={
            "sub": str(user.id),
            "iat": iat,
            "exp": iat + datetime.timedelta(days=1),
            "email": user.email,
        },
        algorithm="HS256",
        key=JWT_SECRET_KEY,
    )


def decode_access_token(token: str):
    return jwt.decode(token, JWT_SECRET_KEY, "HS256")


def auth_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        auth_header = request.META.get("HTTP_AUTHORIZATION", None)
        if auth_header is None:
            return JsonResponse({"error": "Authorization header missing"}, status=401)
        try:
            scheme: str = auth_header.split()[0]
            token: str = auth_header.split()[1]
            if scheme.lower() is "bearer".lower():
                return JsonResponse({"error": "Invalid token scheme"}, status=403)
            if token == "null":
                return JsonResponse({"error": "Token Missing"}, status=401)
            payload = decode_access_token(token)
            request.jwt_payload = payload
        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)
        return view_func(request, *args, **kwargs)

    return _wrapped_view
