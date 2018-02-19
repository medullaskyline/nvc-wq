from wq.db.rest.views import ModelViewSet
from django.db.models.fields import FieldDoesNotExist
from rest_framework.decorators import detail_route

from wq.db.rest.model_tools import get_by_identifier
from rest_framework.response import Response


from rest_framework.routers import Route
from wq.db.rest.views import ModelViewSet
from wq.db.rest.models import get_ct
from wq.db.patterns.relate.models import get_related_parents, get_related_children


"""
todo override ModelViewSet for listing
Feeling SubCategories, NeedLeafs, FeelingLeafs

    def retrieve(self, request, *args, **kwargs):
        '''
        Custom retrieve watches for "new" lookup value and switches modes
        accordingly
        '''
        if hasattr(self, 'lookup_url_kwarg'):
            # New in DRF 2.4?
            lookup = self.lookup_url_kwarg or self.lookup_field
        else:
            lookup = self.lookup_field

        if self.kwargs.get(lookup, "") == "new":
            # new/edit mode
            return self.new(request)
        else:
            # Normal detail view
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
                   
    def list(self, request, *args, **kwargs):
    
        1. modification 1: add {'<parent content type name>': <parent instance>}
        to kwargs so that it will correctly retrieve it from self.get_parent
        kwargs.extend({'FeelingMainCategory': [1] })  or 'FeelingSubCategory', 'NeedCategory', etc
        response = super().list(
            request, *args, **kwargs
        )
        if not isinstance(response.data, dict):
            return response

        if self.target:
            response.data['target'] = self.target
        ct = get_ct(self.model)
        
        # todo: modify this for the needleafs-for-needcategory so it doesn't go back to the needcategory
        # view so needcategory detail is never accessed
        for pct, fields in ct.get_foreign_keys().items():
            if len(fields) == 1:
                self.get_parent(pct, fields[0], response)
        return response
"""

