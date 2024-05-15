from datetime import datetime
from access.models import Source, UserSource, AccessHistory
from django.contrib.auth.models import User


class UserService:
    def create_user(self, auth_user, username: str, password: str) -> User | bool:
        if User.objects.filter(username=username).exists():
            return False

        try:
            user = User.objects.create_user(username, None, password)
            user.save()
        except:
            return False

        return user

    def get_all_users(self, auth_user):
        return User.objects.all()


class SourceService:
    def create_source(self, auth_user, name: str):
        try:
            if Source.objects.filter(name=name).exists():
                source = Source.objects.get(name=name)
            else:
                source = Source(name=name)
                source.save()
        except:
            return False

        return source

    def get_all_sources(self, auth_user):
        return Source.objects.all()


class AccessService:
    def set_access(self, auth_user, user_id: int, source_id: int) -> bool:
        user = User.objects.get(id=user_id)
        source = Source.objects.get(id=source_id)

        if not user or not source:
            return False

        if UserSource.objects.filter(source=source, user=user).exists():
            return True

        try:
            new_access = UserSource(source=source, user=user)
            new_access.save()
        except:
            return False

        return True

    def delete_access(self, auth_user, user_id: int, source_id: int) -> bool:
        user = User.objects.get(id=user_id)
        source = Source.objects.get(id=source_id)

        if not UserSource.objects.filter(source=source, user=user).exists():
            return False

        try:
            UserSource.objects.filter(source=source, user=user).delete()
        except:
            return False

        return True

    def check_access(self, auth_user, source_id: int) -> bool:
        user = User.objects.get(id=auth_user.id)
        source = Source.objects.get(id=source_id)

        if auth_user.is_superuser == 1:
            access_status = True
        else:
            access_status = UserSource.objects.filter(source=source, user=user).exists()
            
        history = AccessHistory(
            source=source,
            user=user,
            hasAccess=access_status
        )
        history.save()

        return access_status
