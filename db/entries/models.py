from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse
# from wq.db.patterns.models import RelatedModel, Relationship, InverseRelationship, RelationshipType, InverseRelationshipType, RelatedModelManager
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
    user = models.ForeignKey(User) #, editable=False) if this is false, it wont show up in the edit form
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        abstract = True


class FeelingMainCategory(models.Model):
    feeling_main_category = models.CharField(max_length=256, editable=False, choices=MAIN_CATEGORY_CHOICES)

    def feeling_sub_categories(self):
        return FeelingSubCategory.objects.filter(feeling_main_category_id=self.pk)

    def __str__(self):
        return self.feeling_main_category

    class Meta:
        verbose_name_plural = "Feeling Main Categories"


class FeelingSubCategory(models.Model):
    feeling_main_category = models.ForeignKey(FeelingMainCategory, editable=False)
    feeling_sub_category = models.CharField(max_length=256, editable=False, choices=SUBCAT_CHOICES)

    def feeling_leaves(self):
        return FeelingLeaf.objects.filter(feeling_sub_category_id=self.pk)

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

    class Meta:
        verbose_name_plural = "Feeling Leaves"


class NeedCategory(models.Model):
    need_category = models.CharField(max_length=256, editable=False, choices=NEED_CATEGORY_CHOICES)

    def needleaves(self):
        return self.needleaf_set.all()

    def __str__(self):
        return self.need_category

    def get_absolute_url(self):
        return reverse('needleaf-for-need_category', kwargs={'need_category': self.pk})

    class Meta:
        verbose_name_plural = "Need Categories"



class NeedLeaf(models.Model):
    need_category = models.ForeignKey(NeedCategory, editable=False)
    need_leaf = models.CharField(max_length=256, editable=False, choices=All_NEED_CHOICES)

    def __str__(self):
        return self.need_leaf

    class Meta:
        verbose_name_plural = "Need Leaves"


class Entry(BaseEntry):
    feeling_main_category = models.ForeignKey(FeelingMainCategory)
    feeling_sub_category = ChainedForeignKey(FeelingSubCategory,
                                             chained_field="feeling_main_category",
                                             chained_model_field="feeling_main_category",
                                             show_all=False,
                                             auto_choose=True,
                                             sort=True)
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
    wq_label_template = "{{user.username}} on {{created_at}}"

    def __str__(self):
        return pystache.render(self.wq_label_template, self)    
    """

"""
class RelatedEntry(RelatedModel, BaseEntry):
    feeling_main_category = models.ForeignKey(FeelingMainCategory)
    feeling_sub_category = ChainedForeignKey(FeelingSubCategory,
                                             chained_field="feeling_main_category",
                                             chained_model_field="feeling_main_category",
                                             show_all=False,
                                             auto_choose=True,
                                             sort=True)
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
        qs_list = list(self.user.relatedentry_set.all())
        index = str(qs_list.index(self))
        username = self.user.username
        length = str(len(qs_list))

        return f'related entry by {username}: {index} of {length}'
"""