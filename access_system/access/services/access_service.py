from datetime import datetime
from access_system.access.models import Source, User


users: list[User] = []
sources: list[Source] = []
history: list[dict] = []


class AccessService:
    def create_user(username: str, password: str) -> User | bool:
        if get_user(username=username) is None:
            user = User(username, password)
            users.append(user)
            return user

        return False

    def create_source(name: str):
        source = Source(name)
        sources.append(source)
        return source

    def get_user(user_id: int = None, username: str = None) -> User | None:
        if user_id is not None or username is not None:
            for user in users:
                if user.id == user_id or user.username == username:
                    return user

        return None

    def get_source(source_id: int) -> Source | None:
        for source in sources:
            if source.id == source_id:
                return source

        return None

    def check_access(user_id: int, source_id: int) -> bool:
        user = get_user(user_id)
        if user is None:
            return False

        access = source_id in user.source_access
        if not access:
            print(
                f"Попытка получения доступа к ресурсу {source_id} пользователем {user_id} неуспешна"
            )

        history.append(
            {
                "time": datetime.now(),
                "user_id": user_id,
                "source_id": source_id,
                "hasAccess": access,
            }
        )

        return access

    def delete_access(user_id: int, source_id: int) -> bool:
        user = get_user(user_id)
        if user is None:
            return False

        if source_id in user.source_access:
            user.source_access.remove(source_id)

        return True

    def set_access(user_id: int, source_id: int) -> bool:
        user = get_user(user_id)
        source = get_source(source_id)

        if not user or not source:
            return False
        else:
            user.source_access.append(source.id)

        return True
