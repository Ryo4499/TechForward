from uuid import uuid4


def generate_uuid() -> str:
    """UUIDの生成

    Returns:
        str: 自動生成されたUUID
    """
    return str(uuid4().hex)
