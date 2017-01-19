# Create your models here.
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class OfficesModel(models.Model):
    named = models.CharField(max_length=30, verbose_name=u'Название', blank=True, null=True)
    location = models.CharField(max_length=255, verbose_name=u'Адрес', blank=True, null=True)
    picture = models.ImageField(upload_to="test/", blank=True, null=True, verbose_name=u'')

    def __str__(self):
        return self.named


class MembersModel(models.Model):
    office = models.ManyToManyField(OfficesModel, related_name="members")
    f_name = models.CharField(max_length=100, verbose_name=u'Name', null=True)
    l_name = models.CharField(max_length=100, verbose_name=u'L_name', null=True)
    position = models.CharField(max_length=255, verbose_name=u'Position', default='------')
    user = models.OneToOneField(User, null=True, related_name='member')

    def __str__(self):
        return self.l_name