from wq.db.rest.views import ModelViewSet
from django.db.models.fields import FieldDoesNotExist
from rest_framework.decorators import detail_route

from wq.db.rest.model_tools import get_by_identifier
from rest_framework.response import Response


class FeelingsNeedsEntryViewSet(ModelViewSet):
    # todo: is all this necessary?

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @detail_route
    def edit(self, request, *args, **kwargs):
        """
        Generates a context appropriate for editing a form
        """
        response = self.retrieve(request, *args, **kwargs)
        obj = self.get_object()
        if obj.user != request.user:
            return response
        serializer = self.get_serializer(obj)
        serializer.add_lookups(response.data)
        serializer.add_checked(response.data)
        return response

    def new(self, request):
        """
        new is a variant of the "edit" action, but with no existing model
        to lookup.
        """
        self.action = 'edit'
        init = request.GET.dict()
        for arg in self.ignore_kwargs:  ## todo: ignore_kwargs should include User
            init.pop(arg, None)
        for key in list(init.keys()):
            try:
                field = self.model._meta.get_field(key)
            except FieldDoesNotExist:
                del init[key]
            else:
                if field.rel:
                    fk_model = field.rel.to
                    try:
                        obj = get_by_identifier(fk_model.objects, init[key])
                    except fk_model.DoesNotExist:
                        del init[key]
                    else:
                        init[key] = obj.pk

        obj = self.model(**init)
        obj.user = request.user
        serializer = self.get_serializer(obj)
        data = serializer.data
        serializer.add_lookups(data)
        resp = Response(data)
        # resp.data['user_list'] = [{'id': request.user.id, 'label': request.user.username, 'selected': True}]
        return resp



