from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.views import View
from .models import Employees, Category, Person
from .utils import *
from .forms import *
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics, permissions, response
from .serializers import *


class BaseView(View):

    def get(self, request):
        employee = Employees.objects.all()
        category = Category.objects.all()
        context = {
            'employee': employee,
            'category': category
        }
        return render(request, 'website/base_template.html', context)


def employees_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        employees = Employees.objects.filter(job__icontains=search_query)
    else:
        employees = Employees.objects.all()
    employee_base = Employees.objects.all()
    category_base = Category.objects.all()
    paginator = Paginator(employees, 4)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()
    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''
    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''
    context = {
        'page_object': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url,
        'employee_base': employee_base,
        'category_base': category_base
    }
    return render(request, 'website/index.html', context)


def employee_detail(request, slug):
    employee = Employees.objects.get(slug__iexact=slug)
    return render(request, 'website/employee_detail.html', context={'employee': employee})


def categories_list(request):
    categories = Category.objects.all()
    return render(request, 'website/categories_list.html', context={'categories': categories})


def category_detail(request, slug):
    category = Category.objects.get(slug__iexact=slug)
    return render(request, 'website/category_detail.html', context={'category': category})


class EmployeeDetail(ObjectDetailMixin, View):
    model = Employees
    template = 'website/employee_detail.html'
    model_two = Category
    model_three = Person


class CategoryDetail(ObjectDetailMixin, View):
    model = Category
    template = 'website/category_detail.html'
    model_two = Employees


class CategoryCreate(LoginRequiredMixin, View, ObjectCreateMixin):
    form_model = CategoryForm
    template = 'website/category_create.html'
    raise_exception = True


class EmployeeCreate(LoginRequiredMixin, View, ObjectCreateMixin):
    form_model = EmployeeForm
    template = 'website/employee_create.html'
    raise_exception = True


class CategoryUpdate(LoginRequiredMixin, View, ObjectUpdateMixin):
    model = Category
    template = 'website/category_update.html'
    form_model = CategoryForm
    raise_exception = True


class EmployeeUpdate(LoginRequiredMixin, View, ObjectUpdateMixin):
    model = Employees
    template = 'website/employee_update.html'
    form_model = EmployeeForm
    raise_exception = True


class CategoryDelete(LoginRequiredMixin, View, ObjectDeleteMixin):
    model = Category
    template = 'website/category_delete.html'
    redirect_url = 'categories_list_url'
    raise_exception = True


class EmployeeDelete(LoginRequiredMixin, View, ObjectDeleteMixin):
    model = Employees
    template = 'website/employee_delete.html'
    redirect_url = 'employees_list_url'
    raise_exception = True


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'website/login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'website/login.html', context={'form': form})


class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        context = {
            'form': form
        }
        return render(request, 'website/registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.age = form.cleaned_data['age']
            new_user.image_user = form.cleaned_data['image_user']
            new_user.city = form.cleaned_data['city']
            new_user.country = form.cleaned_data['country']
            new_user.phone = form.cleaned_data['phone']
            new_user.description = form.cleaned_data['description']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return redirect(new_user)
        context = {
            'form': form
        }
        return render(request, 'website/registration.html', context)


class ProfileView(View):
    def get(self, request, slug):
        person = Person.objects.get(slug__iexact=slug)
        context = {
            'user': self.request.user,
            'users': person,
        }
        return render(request, 'website/profile.html', context)


class ProfileUpdate(View):
    def get(self, request, slug):
        user = Person.objects.get(slug__iexact=slug, username__iexact=request.user.username)
        form = PersonUpdateForm(instance=user)
        return render(request, 'website/profile_update.html', context={'form': form, 'user': user})

    def post(self, request, slug):
        user = Person.objects.get(slug__iexact=slug, username__iexact=request.user.username)
        form = PersonUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.age = form.cleaned_data['age']
            new_user.city = form.cleaned_data['city']
            new_user.country = form.cleaned_data['country']
            new_user.phone = form.cleaned_data['phone']
            new_user.email = form.cleaned_data['email']
            new_user.description = form.cleaned_data['description']
            new_user.image_user = form.cleaned_data['image_user']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return redirect(new_user)
        return render(request, 'website/profile_update.html', context={'form': form, 'user': user})


class SupportView(View):
    def get(self, request, slug):
        person = Person.objects.get(slug__iexact=slug, username=request.user.username)
        context = {
            'phone': person.phone
        }
        return render(request, 'website/support.html', context)


class PersonAPIView(ObjectAPIMixin, APIView):
    model_serializer = PersonSerializer
    model = Person


class EmployeeAPIView(ObjectAPIMixin, APIView):
    model_serializer = EmployeeSerializer
    model = Employees


class CategoryAPIView(ObjectAPIMixin, APIView):
    model_serializer = CategorySerializer
    model = Category


