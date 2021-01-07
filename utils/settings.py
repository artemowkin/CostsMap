from __future__ import annotations

from typing import Union
import os

from django.core.exceptions import ImproperlyConfigured


def get_env(env_name: str, default: Any = None) -> Union[int, str]:
    """Returns environment variable value

    Parameters
    ----------
    env_name : str
        Environment variable name
    default
        Default environment variable value. If variable doesn't exist
        returns this value. By default `None`

    Raises
    ------
    ImproperlyConfigured
        Raises if environment variable doesn't exist and `default`
        is empty

    Returns
    -------
    env_value : Any[str, int]
        Environment variable value. If this value contains only digits
        returns integer else string

    """
    env_value = os.getenv(env_name, default)
    if not env_value:
        raise ImproperlyConfigured(
            f"You need to set `{env_name}` environment variable"
        )

    if isinstance(env_value, str) and env_value.isdigit():
        env_value = int(env_value)

    return env_value
