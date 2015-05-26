# -*- coding: utf-8 -*-
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import django.contrib.auth as auth
from django.contrib.auth.decorators import login_required
from . import models


# Create your views here.
def index(request):
    return render(request, "nippou_app/index.html")


def login(request):
    user_home = redirect("/nippou/document/")

    def _get():
        if request.user.is_authenticated():
            if "next" in request.GET:
                return redirect(request.GET["next"])
            else:
                return user_home
        else:
            return render(request, "registration/login.html", {"message": ""})

    def _post():
        params = request.POST
        username = params["email"].split("@")[0]
        user = None
        if params["is_signup"] == "1":
            up = models.NippouUser.validate(params)
            try:
                user = User.objects.create_user(username, up.email, up.password)
                user = auth.authenticate(username=username, password=up.password)
            except Exception as ex:
                raise Exception("新規登録できませんでした。入力値を確認してください。")
        else:
            user = auth.authenticate(username=username, password=params["password"])
            if not user:
                raise Exception("ユーザー名かパスワードが間違っています")

        if user and user.is_active:
            auth.login(request, user)
            return user_home
        else:
            raise Exception("アクティブなユーザーではありません")

    try:
        if request.method == "GET":
            return _get()
        else:
            return _post()
    except Exception as ex:
        return render(request, "registration/login.html", {"message": str(ex)})


def logout(request):
    auth.logout(request)
    return index(request)

@login_required()
def viewer(request):
    if request.method == "GET":
        nippous = models.Nippou.objects.all()
        return render(request, "nippou_app/viewer.html", {"nippous": nippous})
    else:
        today = datetime.now().strftime("%Y/%m/%d")
        username = request.user.username
        n = models.Nippou(title=today, body="", owner=username)
        n.save()
        return redirect("/nippou/document/{0}/".format(n.id))

@login_required()
def editor(request, nippou_id):
    nippou = models.Nippou.objects.get(pk=nippou_id)
    return render(request, "nippou_app/editor.html", {"nippou": nippou})
