from collections import namedtuple
from django.db import models


# Create your models here.
class Nippou(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True)
    owner = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NippouUser():

    def __init__(self):
        pass

    @classmethod
    def validate(cls, parameters):
        items = ["email", "password", "password_confirm"]
        UserParameters = namedtuple("UserParameters", items)
        u = UserParameters(*[parameters[i] for i in items])

        msg = ""
        if not u.email:
            msg = "メールアドレスが設定されていません"
        elif not u.password or not u.password_confirm:
            msg = "パスワードが設定されていません"
        elif not (u.password == u.password_confirm):
            msg = "パスワードが一致しません"
        elif len(u.password) < 8:
            msg = "パスワードが8桁未満です"

        if msg != "":
            raise Exception(msg)

        return u
