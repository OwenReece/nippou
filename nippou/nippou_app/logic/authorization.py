import re
from collections import namedtuple
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import django.contrib.auth as auth


class UserParameters(namedtuple("User", ["email", "password", "password_confirm"])):
    def username(self):
        return self.email.split("@")[0]

    @classmethod
    def create(cls, params):
        p = [params[f] for f in cls._fields]
        return UserParameters(*p)


class PasswordValidator():
    PASSWORD_LENGTH = 8
    PASSWORD_PATTERNS = ["[a-zA-Z]", "[0-9]"]

    @classmethod
    def validate_length(cls, value):
        if len(value) < cls.PASSWORD_LENGTH:
            raise ValidationError(("パスワードの長さは%(len)s文字以上にしてください)"),
                                  params={"len": cls.PASSWORD_LENGTH})

    @classmethod
    def validate_variety(cls, value):
        is_match = lambda p, s: 1 if re.match(".*{0}+.*".format(p), s) is not None else 0
        include_patterns = sum([is_match(p, value) for p in cls.PASSWORD_PATTERNS])
        if include_patterns < len(cls.PASSWORD_PATTERNS):
            raise ValidationError(("パスワードは英数字を含む必要があります"),
                                  code="variety")


class PasswordField(forms.CharField):
    default_validators = [PasswordValidator.validate_length, PasswordValidator.validate_variety]


class UserForm(forms.Form):
    email = forms.EmailField(required=True, error_messages={"invalid": "メールアドレスの書式が正しくありません"})
    password = PasswordField(required=True)
    password_confirm = PasswordField(required=True)

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        p1 = cleaned_data.get("password")
        p2 = cleaned_data.get("password_confirm")

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError(
                self.error_messages["入力されたパスワードが一致しません"],
                code="password_mismatch",
            )


def signup(params):
    up = UserParameters.create(params)
    uf = UserForm(params)
    uf.full_clean()
    user = None
    if uf.is_valid():
        user = User.objects.create_user(up.username(), up.email, up.password)
        user = auth.authenticate(username=up.username(), password=up.password)
    else:
        errors = uf.errors.as_data()
        msg = ""
        for k in errors:
            msg = errors[k][0].messages[0]
            break
        raise Exception(msg)

    return user


def authorize(params):
    up = UserParameters.create(params)
    user = auth.authenticate(username=up.username(), password=up.password)
    if not user:
        raise Exception("ユーザー名かパスワードが間違っています")
    return user

