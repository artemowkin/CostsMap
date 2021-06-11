from __future__ import annotations

from django.db import connection


def execute_sql_command(command: str, args: list) -> list[tuple]:
    """Execute sql command and return `fetchall()` result"""
    with connection.cursor() as cursor:
        cursor.execute(command, args)
        result = cursor.fetchall()

    return result
