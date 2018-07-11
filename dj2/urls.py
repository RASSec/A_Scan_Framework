"""dj2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url,include
from main import views as main_view


urlpatterns = [
    path('accounts/',include('users.urls')),
    path('accounts/profile/',main_view.accounts_profile),
    path('buglist/',main_view.projectdetail,name='projectdetail'),
    url(r'^projectdetailshow/(\d+)/$', main_view.projectdetailshow,name="projectdetailshow"),
    url(r'^listing/$', main_view.listing,name="listing"),
    url(r'^assetlist/$', main_view.assetlist,name="assetlist"),
    url(r'^scan/$', main_view.scan,name="scan"),
    path('addasset/', main_view.addasset,name="addasset"),
    path('delbug/',main_view.delbug,name="delbug"),
    path('poc_list/',main_view.poc_list,name="poc_list"),
    path('addbug/',main_view.addbug,name="addbug"),
    path('results/',main_view.results,name="results"),
    path('savetodo/',main_view.savetodo,name="savetodo"),
    path('upload_ajax/',main_view.upload_ajax,name="upload_ajax"),
    path('excel_export/',main_view.excel_export,name="excel_export"),
    path('',main_view.index),
    path('admin/', admin.site.urls),

]

