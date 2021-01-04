"""markdoc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from karm import views
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "MARK"
admin.site.site_title = "MARK Admin Panel"
admin.site.index_title = "Welcome to MARK Admin Panel"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup', views.handleSignup, name='signup'),
    path('login', views.handleLogin, name='login'),
    path('logout', views.handleLogout, name='logout'),
    path('contact', views.contact, name='contact'),
    path('appointment', views.appointment, name='appointment'),
    path('checkup', views.checkup, name='checkup'),
    path('bookAppoint/<int:pk>', views.bookAppoint, name='bookAppoint'),
    path('confirm/<int:pk>/', views.confirm_doc, name='confirm_doc'),
    path('confirmapt/<int:pk>', views.confirm_apt, name='confirm_apt'),
    path('cancel/<int:pk>', views.cancel_apt, name='cancel_apt'),
    path('test-center', views.test_center, name='test-center'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
