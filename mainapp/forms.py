from django import forms
from .models import Category, Employees, Person
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'slug']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Название категории'
        self.fields['slug'].label = 'ID категории'

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()
        if new_slug == 'create':
            raise ValidationError('Категория с названием create не может быть создана')
        if Category.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError('Данная категория уже есть')
        return new_slug


class EmployeeForm(forms.ModelForm):
    image_user = forms.ImageField()

    class Meta:
        model = Employees
        fields = [
            'first_name',
            'last_name',
            'age',
            'city',
            'country',
            'phone',
            'email',
            'job',
            'description',
            'image_user',
            'categories',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['age'].label = 'Возраст'
        self.fields['city'].label = 'Город'
        self.fields['country'].label = 'Страна'
        self.fields['phone'].label = 'Номер телефона'
        self.fields['email'].label = 'Email'
        self.fields['job'].label = 'Ваша должность'
        self.fields['description'].label = 'Описание'
        self.fields['image_user'].label = 'Фотография'
        self.fields['categories'].label = 'Выберите категорию вашей работы'

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()
        if new_slug == 'create':
            raise ValidationError('Категория с названием create не может быть создана')
        if Category.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError('Данный id уже есть')
        return new_slug


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User.objects.filter(username=username).first()
        if not user:
            raise forms.ValidationError(f'Пользователь с логином {username} не найден')
        if not user.check_password(password):
            raise forms.ValidationError('Неверный пароль')
        return self.cleaned_data


class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(required=False)
    city = forms.CharField(required=False)
    country = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    age = forms.IntegerField(required=False)
    description = forms.CharField(widget=forms.Textarea)
    image_user = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Подтвердите пароль'
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['age'].label = 'Возраст'
        self.fields['country'].label = 'Страна'
        self.fields['city'].label = 'Город'
        self.fields['phone'].label = 'Номер телефона'
        self.fields['email'].label = 'Электронная почта'
        self.fields['description'].label = 'Расскажите о себе'
        self.fields['image_user'].label = 'Фотография'

    def clean_email(self):
        email = self.cleaned_data['email']
        domain = email.split('.')[-1]
        if domain in ['com', 'net']:
            raise forms.ValidationError(f'Регистрация для домена {domain} невозможна')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Данная электронная почта уже занята')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Логин {username} занят')
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'confirm_password',
            'first_name',
            'last_name',
            'age',
            'country',
            'city',
            'phone',
            'email',
            'description',
            'image_user'
        ]


class PersonUpdateForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(required=False)
    city = forms.CharField(required=False)
    country = forms.CharField(required=False)
    age = forms.IntegerField(required=False)
    description = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Подтвердите пароль'
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['age'].label = 'Возраст'
        self.fields['country'].label = 'Страна'
        self.fields['city'].label = 'Город'
        self.fields['phone'].label = 'Номер телефона'
        self.fields['email'].label = 'Электронная почта'
        self.fields['description'].label = 'Расскажите о себе'
        self.fields['image_user'].label = 'Фотография'

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data

    @property
    def clean_username(self):
        username = self.cleaned_data['username']
        user = Person.is_authenticated
        if username != Person.objects.get(username__iexact=user.username).username \
                and Person.objects.filter(username=username).exists():
            raise ValidationError(f'Логин {username} занят')
        return username

    @property
    def clean_email(self):
        email = self.cleaned_data['email']
        user = Person.is_authenticated
        domain = email.split('.')[-1]
        if domain in ['com', 'net']:
            raise forms.ValidationError(f'Регистрация для домена {domain} невозможна')
        if email != Person.objects.get(email__iexact=user.email).email \
                and Person.objects.filter(email=email).exists():
            raise forms.ValidationError('Данная электронная почта уже занята')
        return email

    class Meta:
        model = Person
        fields = [
            'username',
            'password',
            'confirm_password',
            'first_name',
            'last_name',
            'age',
            'country',
            'city',
            'phone',
            'email',
            'description',
            'image_user'
        ]