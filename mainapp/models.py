from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.shortcuts import reverse

from PIL import Image
from io import BytesIO
from time import time

import sys
import uuid


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


def cropping_photo_employee(self):
    image = self.image_user
    img = Image.open(image)
    new_img = img.convert('RGB')
    resized_new_img = new_img.resize((700, 350), Image.ANTIALIAS)
    filestream = BytesIO()
    resized_new_img.save(filestream, 'JPEG', quality=90)
    filestream.seek(0)
    name = '{}.{}'.format(*self.image_user.name.split('.'))
    self.image_user = InMemoryUploadedFile(
        filestream, 'ImageField', name, 'jpeg/image', sys.getsizeof(filestream), None
    )
    return self.image_user


def cropping_photo_person(self):
    image = self.image_user
    img = Image.open(image)
    new_img = img.convert('RGB')
    resized_new_img = new_img.resize((400, 350), Image.ANTIALIAS)
    filestream = BytesIO()
    resized_new_img.save(filestream, 'JPEG', quality=90)
    filestream.seek(0)
    name = '{}.{}'.format(*self.image_user.name.split('.'))
    self.image_user = InMemoryUploadedFile(
        filestream, 'ImageField', name, 'jpeg/image', sys.getsizeof(filestream), None
    )
    return self.image_user


class Employees(models.Model):
    first_name = models.CharField(max_length=255, db_index=True)
    last_name = models.CharField(max_length=255, db_index=True)
    age = models.IntegerField(default=100, db_index=True)
    city = models.CharField(max_length=255, db_index=True)
    country = models.CharField(max_length=255, db_index=True)
    phone = models.CharField(max_length=255, db_index=True)
    email = models.EmailField(max_length=255, db_index=True)
    job = models.CharField(max_length=255, db_index=True)
    description = models.TextField(max_length=255, db_index=True)
    image_user = models.ImageField(db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    date_pub = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField('Category', related_name='employees')

    def get_absolute_url(self):
        return reverse('employee_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('employee_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('employee_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        self.image_user = cropping_photo_employee(self)
        if not self.id:
            self.slug = gen_slug(self.job)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date_pub']


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    def get_absolute_url(self):
        return reverse('category_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('category_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('category_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Person(AbstractUser):
    age = models.IntegerField(default=100, db_index=True)
    city = models.CharField(max_length=255, db_index=True)
    country = models.CharField(max_length=255, db_index=True)
    phone = models.CharField(max_length=255, db_index=True)
    description = models.TextField(max_length=255, db_index=True)
    image_user = models.ImageField(db_index=True)
    slug = models.SlugField(unique=True, default=uuid.uuid1)

    def get_absolute_url(self):
        return reverse('profile_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('profile_update_url', kwargs={'slug': self.slug})

    def get_support_url(self):
        return reverse('support_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.image_user = cropping_photo_person(self)
        if not self.id:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)

