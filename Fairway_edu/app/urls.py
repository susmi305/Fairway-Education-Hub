"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.quickstart.views import index,sign_up,login_view,course_list,dashboard,course_create,delete_course,c_delete,create_folder,upload_pictures,view_folders,view_pictures,redirect_based_on_role,user_logout,delete_folder,confirm_delete_folder,upload_services,view_services,delete_service,service_del
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('signup/', sign_up, name='sign_up'),
    path('dashboard/', dashboard, name='dashboard'),
    path('login/', login_view, name='login'),
    path('course/course_list/', course_list, name='course_list'),
    path('course/course_form/', course_create, name='course_create'),
    path('course/c_delete/', c_delete, name='c_delete'),
    path('course/course_delete/<int:id>/', delete_course, name='delete_course'),
    path('gallery/create_folder/', create_folder, name='create_folder'),
    path('gallery/upload_picture/<int:folder_id>/', upload_pictures, name='upload_picture'),
    path('gallery/view_folder/', view_folders, name='view_folder'),
    path('gallery/picture/<int:folder_id>/', view_pictures, name='view_picture'),
    path('redirect/', redirect_based_on_role, name='redirect_based_on_role'),
    path('folders/<int:folder_id>/delete/', delete_folder, name='delete_folder'),
    path('gallery/confirm_delete_folder',confirm_delete_folder, name='confirm_delete_folder'),
    path('Services/upload_services/',upload_services,name='upload_services'),
    path('Service/view_services',view_services,name='view_services'),
    path('logout/', user_logout, name='logout'),
    path('services/delete/<int:id>/', delete_service, name='delete_service'),
    path('services/delete/', service_del, name='service_del'),
   
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
