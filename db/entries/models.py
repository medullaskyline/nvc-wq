from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

from smart_selects.db_fields import ChainedForeignKey

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


ALL_FEELING_CHOICES = get_feelings_choices('emotional') + get_feelings_choices('mental') + get_feelings_choices(
    'physical')
All_NEED_CHOICES = get_need_choices()


class BaseEntry(models.Model):
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        abstract = True


class FeelingMainCategory(models.Model):
    feeling_main_category = models.CharField(max_length=256, editable=False, choices=MAIN_CATEGORY_CHOICES)

    def __str__(self):
        return self.feeling_main_category

    class Meta:
        verbose_name_plural = "Feeling Categories"


class FeelingSubCategory(models.Model):
    feeling_main_category = models.ForeignKey(FeelingMainCategory, editable=False)
    feeling_sub_category = models.CharField(max_length=256, editable=False, choices=SUBCAT_CHOICES)

    def __str__(self):
        return self.feeling_sub_category

    class Meta:
        verbose_name_plural = "Feeling Subcategories"


class FeelingLeaf(models.Model):
    feeling_main_category = models.ForeignKey(FeelingMainCategory, editable=False)
    feeling_sub_category = models.ForeignKey(FeelingSubCategory, editable=False)
    feeling_leaf = models.CharField(max_length=256, editable=False, choices=ALL_FEELING_CHOICES)

    def __str__(self):
        return self.feeling_leaf

    # class Meta:
        # verbose_name_plural = ""


class NeedCategory(models.Model):
    need_category = models.CharField(max_length=256, editable=False, choices=NEED_CATEGORY_CHOICES)

    def __str__(self):
        return self.need_category

    class Meta:
        verbose_name_plural = "Need Categories"


class NeedLeaf(models.Model):
    need_category = models.ForeignKey(NeedCategory, editable=False)
    need_leaf = models.CharField(max_length=256, editable=False, choices=All_NEED_CHOICES)

    def __str__(self):
        return self.need_leaf


class Entry(BaseEntry):
    feeling_main_category = models.ForeignKey(FeelingMainCategory)
    feeling_sub_category = models.ForeignKey(FeelingSubCategory)
    feeling = ChainedForeignKey(FeelingLeaf,
                                chained_field="feeling_sub_category",
                                chained_model_field="feeling_sub_category",
                                show_all=False,
                                auto_choose=True,
                                sort=True)
    need_category = models.ForeignKey(NeedCategory)
    need = ChainedForeignKey(NeedLeaf,
                             chained_field="need_category",
                             chained_model_field='need_category',
                             show_all=False,
                             auto_choose=True,
                             sort=True)
    notes = models.TextField(blank=True)
    public = models.CharField(default='FALSE', choices=(
        ('FALSE', 'false'), ('TRUE', 'true')
    ), max_length=5)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        created_at = "" if not self.created_at else " at " + datetime.strftime(self.created_at, "%y-%m-%d %H:%M:%S")
        return "entry by " + self.user.username + created_at


"""
older models
"""


class Feeling(models.Model):
    main_category = models.CharField(max_length=256, editable=False, choices=MAIN_CATEGORY_CHOICES)
    sub_category = models.CharField(max_length=256, editable=False, choices=SUBCAT_CHOICES)
    name = models.CharField(max_length=256, editable=False, choices=ALL_FEELING_CHOICES)

    def __str__(self):
        return self.name + " : " + self.sub_category + " : " + self.main_category


class Need(models.Model):
    category = models.CharField(max_length=256, choices=NEED_CATEGORY_CHOICES, editable=False)
    name = models.CharField(max_length=256, choices=All_NEED_CHOICES, editable=False)

    def __str__(self):
        return self.name + " : " + self.category


class FeelingsNeedsEntry(BaseEntry):
    feeling = models.ForeignKey(Feeling)
    need = models.ForeignKey(Need)
    notes = models.TextField(blank=True)
    public = models.CharField(default='FALSE', choices=(
        ('FALSE', 'false'), ('TRUE', 'true')
    ), max_length=5)

    class Meta:
        verbose_name = 'feelings-needs entry'
        verbose_name_plural = 'feelings-needs entries'

    def __str__(self):
        created_at = "" if not self.created_at else " at " + datetime.strftime(self.created_at, "%y-%m-%d %H:%M:%S")
        return "f/n entered by " + self.user.username + created_at
