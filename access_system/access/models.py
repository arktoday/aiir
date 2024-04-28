import itertools
import bcrypt


from django.db import models

class Source(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'source'


# class User:
#     IS_ADMIN: int = 0

#     id_iter = itertools.count(1)

#     id: int
#     username: str
#     password_hash: str

#     def __init__(self, username: str, password: str):
#         self.id = next(User.id_iter)
#         self.username = username

#         salt = bcrypt.gensalt()
#         self.password_hash = bcrypt.hashpw(password, salt)

#         self.source_access = []
#         self.is_admin = 0

#     @staticmethod
#     def check_pasword(hashed_password: str, password: str) -> bool:
#         return hashed_password == bcrypt.hashpw(password, hashed_password)
