from .services import AuthStore
from ..project.settings import settings


def use_auth_store() -> AuthStore:
    return AuthStore(settings.secret_key)
