from datetime import datetime
from access.models import Source, UserSource
from django.contrib.auth.models import User

users: list[User] = []
sources: list[Source] = []
history: list[dict] = []


class AccessService:
    def create_user(self, auth_user, username: str, password: str) -> User | bool:
        return auth_user.is_superuser == 1
        if User.objects.filter(username=username).exists():
            return False
        
        user = User.objects.create_user(username, None, password)
        user.save()

        return user
    
    def get_user(self, user_id: int = None, username: str = None) -> User | None:
        try:
            if user_id:
                user = User.objects.get(pk=user_id)
            elif username:
                user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
            
        return user

    def create_source(self, name: str):
        source = Source(name)
        sources.append(source)
        return source

    def get_source(self, source_id: int) -> Source | None:
        for source in sources:
            if source.id == source_id:
                return source

        return None

    def check_access(self, user_id: int, source_id: int) -> bool:
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

    def delete_access(self, user_id: int, source_id: int) -> bool:
        user = get_user(user_id)
        if user is None:
            return False

        if source_id in user.source_access:
            user.source_access.remove(source_id)

        return True

    def set_access(self, user_id: int, source_id: int) -> bool:
        user = get_user(user_id)
        source = get_source(source_id)

        if not user or not source:
            return False
        else:
            user.source_access.append(source.id)

        return True
