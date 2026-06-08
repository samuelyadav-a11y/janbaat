from jose import JWTError, jwt

from app.config import settings


def verify_supabase_token(token: str) -> dict:
    """
    Verify a JWT issued by Supabase Auth.
    Returns the decoded payload (includes sub = user UUID).
    Raises JWTError if invalid or expired.
    """
    payload = jwt.decode(
        token,
        settings.supabase_jwt_secret,
        algorithms=["HS256"],
        audience="authenticated",
    )
    return payload


def get_user_id_from_token(token: str) -> str:
    payload = verify_supabase_token(token)
    user_id: str = payload.get("sub")
    if not user_id:
        raise JWTError("No subject in token")
    return user_id
