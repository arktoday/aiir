import itertools
from datetime import datetime


class Source:
    id_iter = itertools.count(1)

    def __init__(self, name: str):
        self.id = next(Source.id_iter)
        self.name = name


class User:
    IS_ADMIN: int = 1

    id_iter = itertools.count(1)

    def __init__(self, username: str, password: str):
        self.id = next(User.id_iter)
        self.username = username
        self.password = password
        self.source_access = []
        self.is_admin = 0


users: list[User] = []
sources: list[Source] = []
history: list[{}] = []


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
        print(f'Попытка получения доступа к ресурсу {source_id} пользователем {user_id} неуспешна')

    history.append({'time': datetime.now(), 'user_id': user_id, 'source_id': source_id, 'hasAccess': access})

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


def get_access_log() -> list[dict]:
    curr_date = datetime.now().strftime('%Y%m%d')

    with open(f'access_log_{curr_date}.txt', 'w') as f:
        for row in history:
            f.write(f'[{row["time"]}] user: {row["user_id"]} source: {row["source_id"]} accessed: {row["hasAccess"]}\n')

    return history


print(create_user('user_1', 'pass').__dict__)
print(create_user('user_1', 'pass'))
print(create_user('user_2', 'pass').__dict__)

print(create_source('zoo.zoo').__dict__)
print(create_source('res').__dict__)
print(create_source(1).__dict__)

print(check_access(1, 1))
print(check_access(1, 2))

print(set_access(1, 1))
print(set_access(1, 2))
print(check_access(1, 1))
print(check_access(1, 2))

print(set_access(2, 2))
print(check_access(2, 2))
print(delete_access(2, 2))
print(check_access(2, 2))

print(get_access_log())

