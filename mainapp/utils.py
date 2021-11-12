from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Employees, Category, Person
from rest_framework.response import Response


class ObjectDetailMixin:
    model = None
    template = None
    model_two = None

    def get(self, request, slug, *args, **kwargs):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        obj_recommendation = self.model.objects.all()
        return render(
            request, self.template, context=
            {
                self.model.__name__.lower(): obj,
                'admin_object': obj,
                'detail': True,
                '{}_recommendation'.format(self.model.__name__.lower()): obj_recommendation,
                self.model_two.__name__.lower(): obj,
            }
        )


class ObjectCreateMixin:
    form_model = None
    template = None

    def get(self, request, *args, **kwargs):
        form = self.form_model()
        return render(request, self.template, context={'form': form})

    def post(self, request, *args, **kwargs):
        bound_form = self.form_model(request.POST, request.FILES)
        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form})


class ObjectUpdateMixin:
    model = None
    template = None
    form_model = None

    def get(self, request, slug, *args, **kwargs):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.form_model(instance=obj)
        return render(request, self.template, context={'form': bound_form, self.model.__name__.lower(): obj})

    def post(self, request, slug, *args, **kwargs):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.form_model(request.POST, instance=obj)
        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form, self.model.__name__.lower(): obj})


class ObjectDeleteMixin:
    model = None
    template = None
    redirect_url = None

    def get(self, request, slug, *args, **kwargs):
        obj = self.model.objects.get(slug__iexact=slug)
        return render(request, self.template, context={self.model.__name__.lower(): obj})

    def post(self, request, slug, *args, **kwargs):
        obj = self.model.objects.get(slug__iexact=slug)
        obj.delete()
        return redirect(reverse(self.redirect_url))


class ObjectAPIMixin:
    model_serializer = None
    model = None

    def get(self, request, *args, **kwargs):
        queryset = self.model.objects.all()
        serializer = self.model_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.model_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
