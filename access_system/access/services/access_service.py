from datetime import datetime
from access.models import Source, UserSource, AccessHistory
from django.contrib.auth.models import User
from access.services.operations_service import OperationsService
from access.scheduler import scheduler, DateTrigger


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
    
    def get_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
        except:
            return False
        
        return user


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

    def get_all_sources(self):
        return Source.objects.all()
    
    def get_source(self, source_id):
        try:
            source = Source.objects.get(id=source_id)
        except:
            return False
        
        return source


class AccessService:
    operations_service = OperationsService()
    
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
    
    def export_access_history(self):
        operation_id = self.ops_service.create_operation()
        scheduler.add_job(self._access_history_to_file,
                          DateTrigger(datetime.now()), (operation_id, ))
        return operation_id

    def _access_history_to_file(self, operation_id: int):
        strings = [
            f"{app.id},{app.driver_id},{app.status.value},{(app.finished_date - app.created_date).total_seconds() if app.finished_date else ''}" for app in applications.values()]
        time.sleep(1)
        filename = f"static/reports/report_{datetime.now().isoformat(timespec='seconds').replace(':', '-')}.csv"
        with open(f"applications/{filename}", 'w')as f:
            f.write('\n'.join(strings))

        self.ops_service.finish_operation(operation_id, { 'url': filename })

