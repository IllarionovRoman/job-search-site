from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('employees/', employees_list, name='employees_list_url'),
    path('employee/create/', EmployeeCreate.as_view(), name='employee_create_url'),
    path('employee/<str:slug>/', EmployeeDetail.as_view(), name='employee_detail_url'),
    path('employee/<str:slug>/update/', EmployeeUpdate.as_view(), name='employee_update_url'),
    path('employee/<str:slug>/delete/', EmployeeDelete.as_view(), name='employee_delete_url'),
    path('categories/', categories_list, name='categories_list_url'),
    path('category/create/', CategoryCreate.as_view(), name='category_create_url'),
    path('category/<str:slug>/', CategoryDetail.as_view(), name='category_detail_url'),
    path('category/<str:slug>/update/', CategoryUpdate.as_view(), name='category_update_url'),
    path('category/<str:slug>/delete/', CategoryDelete.as_view(), name='category_delete_url'),
    path('registration/', RegistrationView.as_view(), name='registration_url'),
    path('login/', LoginView.as_view(), name='login_url'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout_url'),
    path('profile/<str:slug>/', ProfileView.as_view(), name='profile_url'),
    path('profile/<str:slug>/update/', ProfileUpdate.as_view(), name='profile_update_url'),
    path('profile/<str:slug>/support/', SupportView.as_view(), name='support_url'),
]