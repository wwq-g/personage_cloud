from django.urls import path
from . import views

app_name='templates'
urlpatterns = [
    path("login/",views.login_cloud,name='login_cloud'),
    path("", views.home,name='home'),
    path("logout/",views.logout_cloud,name="logout_cloud"),
    path('register/',views.register_cloud,name="register_cloud"),
    path('user_center/',views.center,name='center'),
    path('user_center/edit_profile',views.edit_profile,name='edit_profile'),
    path('user_center/change_password',views.change_password,name='change_password'),
    path('upload/',views.upload,name='upload'),
    path("del/<foo_0>", views.del_file, name='del_file'),
    path('download/<foo_1>', views.download, name='download'),
    ]