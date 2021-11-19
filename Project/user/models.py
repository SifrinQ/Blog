from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import json as js


class Blog(models.Model):
    hedline = models.CharField(max_length = 100)
    rubrick = models.CharField(max_length = 50)
    text = models.CharField(max_length = 1000)

    def __str__(self):
	    return self.hedline

    @classmethod
    def __GetModelField__(instance):
        model_meta = instance._meta.fields
        fields = []
        for field in model_meta:
            fields.append(str(field).replace('user.Blog.', ''))
        return fields

    @staticmethod
    def __CleaningAndDumping__(QSlist, fields):

        CleanQSlist = []
        for QS in QSlist:
            if QS.exists():
                CleanQSlist.append(QS)

        data = []
        for QS in CleanQSlist:
            variable = {}
            for response in QS:
                for field in fields:
                    variable.update({field: getattr(response, field)})
            data.append(variable)
        json = js.dumps(data)
        return json

    @classmethod
    def Searching(instance, params):
        response = []
        for param in params:
            QS = instance.objects.filter(
                models.Q( hedline__icontains = param) |
                models.Q( rubrick__icontains = param) |
                models.Q( text__icontains = param)
             )
            response.append(QS)
        json = instance.__CleaningAndDumping__(
                response,
                instance.__GetModelField__()
            )
        return json
