from datetime import datetime
from django.forms import ModelForm
from django.core.exceptions import ObjectDoesNotExist
from .. import models


class NippouForm(ModelForm):
    class Meta:
        model = models.Nippou
        fields = ["title", "body"]


def listup():
    nippous = models.Nippou.objects.all().order_by("-created_at")
    return nippous


def pickup(n_id):
    try:
        nippou = models.Nippou.objects.get(id=n_id)
        return nippou
    except ObjectDoesNotExist as ex:
        return None


def create(username):
    today = datetime.now().strftime("%Y/%m/%d")
    n = models.Nippou(title=today, body="", owner=username)
    n.save()
    return n


def edit(n_id, params):
    n = pickup(n_id)
    f = NippouForm(params, instance=n)
    if f.is_valid():
        f.save()
    else:
        raise Exception("入力内容に誤りがあります")

    return n


def delete(n_id):
    n = pickup(n_id)
    n.delete()
