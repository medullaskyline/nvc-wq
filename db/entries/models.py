from datetime import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

from . import FEELINGS_DICT, NEEDS_DICT

MAIN_CATEGORY_CHOICES = tuple((feel.upper(), feel.lower()) for feel in FEELINGS_DICT.keys())
EMOTIONAL_CATEGORY_CHOICES = tuple((feel.upper(), feel.lower()) for feel in FEELINGS_DICT['emotional'].keys())
MENTAL_CATEGORY_CHOICES = tuple((feel.upper(), feel.lower()) for feel in FEELINGS_DICT['mental'].keys())
PHYSICAL_CATEGORY_CHOICES = tuple((feel.upper(), feel.lower()) for feel in FEELINGS_DICT['physical'].keys())
SUBCAT_CHOICES = EMOTIONAL_CATEGORY_CHOICES + MENTAL_CATEGORY_CHOICES + PHYSICAL_CATEGORY_CHOICES

NEED_CATEGORY_CHOICES = tuple((need.upper(), need.lower()) for need in NEEDS_DICT.keys())


def get_need_choices():
    return_tup = ()
    for need_list in NEEDS_DICT.values():
        for need in need_list:
            return_tup += ((need.upper(), need.lower()),)
    return return_tup


def get_feelings_choices(main_category):
    return_tup = ()
    for key, value_list in FEELINGS_DICT[main_category].items():
        return_tup += tuple((feel.upper(), feel.lower()) for feel in value_list)
    return return_tup

ALL_FEELING_CHOICES = get_feelings_choices('emotional') + get_feelings_choices('mental') + get_feelings_choices('physical')
All_NEED_CHOICES = get_need_choices()


class Feeling(models.Model):
    main_category = models.CharField(max_length=256, editable=False, choices=MAIN_CATEGORY_CHOICES)
    sub_category = models.CharField(max_length=256, editable=False, choices=SUBCAT_CHOICES)
    name = models.CharField(max_length=256, editable=False, choices=ALL_FEELING_CHOICES)

    # def __unicode__(self):
    #     return self.name

    def __str__(self):
        return self.name+" : "+self.sub_category+" : "+self.main_category


class Need(models.Model):
    category = models.CharField(max_length=256, choices=NEED_CATEGORY_CHOICES, editable=False)
    name = models.CharField(max_length=256, choices=All_NEED_CHOICES, editable=False)

    # def __unicode__(self):
    #     return self.name

    def __str__(self):
        return self.name+" : "+self.category


class BaseEntry(models.Model):
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class FeelingsNeedsEntry(BaseEntry):
    feeling = models.ForeignKey(Feeling)
    need = models.ForeignKey(Need)
    notes = models.TextField(blank=True)
    public = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'feelings-needs entry'
        verbose_name_plural = 'feelings-needs entries'

    def get_absolute_url(self):
        return reverse('entries:detail', kwargs={'pk': self.pk})

    def __str__(self):
        created_at = ""  if not self.created_at else " at " + datetime.strftime(self.created_at, "%y-%m-%d %H:%M:%S")
        return "f/n entered by " + self.user.username + created_at
