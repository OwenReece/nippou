# -*- coding: utf-8 -*-
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import django.contrib.auth as auth
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
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
def view(request):
    if request.method == "GET":
        nippous = models.Nippou.objects.all().order_by("-created_at")
        return render(request, "nippou_app/view.html", {"nippous": nippous})
    else:
        today = datetime.now().strftime("%Y/%m/%d")
        username = request.user.username
        n = models.Nippou(title=today, body="", owner=username)
        n.save()
        return redirect("/nippou/document/{0}/edit".format(n.id))


@login_required()
def detail(request, nippou_id):
    nippou = models.Nippou.objects.get(pk=nippou_id)
    is_own = (nippou.owner == request.user.username)
    return render(request, "nippou_app/detail.html", {"nippou": nippou, "is_own": is_own})


@login_required()
def edit(request, nippou_id):
    nippou = models.Nippou.objects.get(pk=nippou_id)
    is_own = (nippou.owner == request.user.username)
    show_nippou = lambda r, m="":  render(r, "nippou_app/edit.html", {"nippou": nippou, "is_own": is_own, "message": m})

    if not is_own:
        return redirect("/nippou/document/{0}/".format(nippou.id))

    if request.method == "GET":
        return show_nippou(request)
    elif request.method == "POST":
        class NippouForm(ModelForm):
            class Meta:
                model = models.Nippou
                fields = ["title", "body"]

        f = NippouForm(request.POST, instance=nippou)
        if f.is_valid():
            f.save()
            return redirect("/nippou/document/{0}/".format(nippou.id))
        else:
            return show_nippou(request, "入力内容に誤りがあります")

@login_required()
def delete(request, nippou_id):
    nippou = models.Nippou.objects.get(pk=nippou_id)
    is_own = (nippou.owner == request.user.username)

    if not is_own:
        return redirect("/nippou/document/{0}/".format(nippou.id))

    nippou.delete()
    return redirect("/nippou/document/")
