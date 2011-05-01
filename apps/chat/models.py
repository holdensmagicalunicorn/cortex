import simplejson as json
from django.db import models
from django.contrib import admin
from django.core import serializers
import django.dispatch
from django.db.models.signals import pre_save
from django.dispatch import receiver

class CapsuleModel(models.Model):

    def xport(self):
        return {
            'id': self.id,
            'attrs': self.json_equivalent()
        }

    def json_equivalent(self):
        dictionary = {}
        for field in self._meta.get_all_field_names():
            if field != 'id':
                val = self.__getattribute__(field)
                if isinstance(val, str) or isinstance(val, int):
                    dictionary[field] = val
        return dictionary

    def mport(self,**args):
        for key, value in args.iteritems():
            self['key'] = value

        self.save()

class AppModel(CapsuleModel):
    toggler = models.BooleanField()

admin.site.register(AppModel)
