from django.contrib import admin
from django.urls import path
from task import views

urlpatterns = [
    path('adadmin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('current/', views.currenttasks, name='currenttasks'),
    path('important/',views.importanttasks,name='importanttasks'),
    path('completed/', views.completedtasks, name='completedtasks'),
    path('new/', views.newtask, name='newtask'),
    path('task/<int:task_pk>', views.updatetask, name='update'),
    path('task/<int:task_pk>/complete', views.completetask, name='completetask'),
    path('task/<int:task_pk>/delete', views.deletetask, name='deletetask'),
]
