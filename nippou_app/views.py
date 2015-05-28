# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
import django.contrib.auth as auth
from django.contrib.auth.decorators import login_required
from .logic import authorization
from .logic import nippou_api


class Path():
    index = "/nippou/"
    view = "/nippou/document/"
    detail = lambda nid: "/nippou/document/{0}/".format(nid)
    edit = lambda nid: "/nippou/document/{0}/edit".format(nid)


def is_own(nippou_id, request):
    n = nippou_api.pickup(nippou_id)
    if n.owner == request.user.username:
        return True
    else:
        return False


# Create your views here.
def index(request):
    return render(request, "nippou_app/index.html")


def login(request):
    def _get():
        if request.user.is_authenticated():
            if "next" in request.GET:
                return redirect(request.GET["next"])
            else:
                return redirect(Path.view)
        else:
            return render(request, "registration/login.html", {"message": ""})

    def _post():
        params = request.POST
        is_signup = True if params["is_signup"] == "1" else False
        user = None
        if is_signup:
            user = authorization.signup(params)
        else:
            user = authorization.authorize(params)

        if user and user.is_active:
            auth.login(request, user)
            return redirect(Path.view)
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
        nippous = nippou_api.listup()
        return render(request, "nippou_app/view.html", {"nippous": nippous})
    else:
        n = nippou_api.create(request.user.username)
        return redirect(Path.edit(n.id))


@login_required()
def detail(request, nippou_id):
    n = nippou_api.pickup(nippou_id)
    return render(request, "nippou_app/detail.html", {"nippou": n, "is_own": is_own(n.id, request)})


@login_required()
def edit(request, nippou_id):
    _is_own = is_own(nippou_id, request)
    show_nippou = lambda m="":  render(request, "nippou_app/edit.html",
                                       {"nippou": nippou_api.pickup(nippou_id), "is_own": _is_own, "message": m})

    if not _is_own:
        return redirect(Path.detail(nippou_id))

    if request.method == "GET":
        return show_nippou()
    elif request.method == "POST":
        try:
            n = nippou_api.edit(nippou_id, request.POST)
            return redirect(Path.detail(n.id))
        except Exception as ex:
            return show_nippou(str(ex))

@login_required()
def delete(request, nippou_id):
    if is_own(nippou_id, request):
        nippou_api.delete(nippou_id)
        return redirect(Path.view)
    else:
        return redirect(Path.detail(n.id))
