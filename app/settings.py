import os


def get_env(env_name: str, default_value: str | None = None):
    """
    Return environment variable value if it exists. Else raise RuntimeError
    """
    env_value = os.getenv(env_name)
    if not env_value:
        if default_value: return default_value
        raise RuntimeError(f"You need to set {env_name} env variable")

    return env_value


DATABASE_URL = get_env('DATABASE_URL')
