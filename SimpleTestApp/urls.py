"""SimpleTestApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
import testapps.views as testapps

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', testapps.index, name="testapps_index"),
    path('html/index_test_script_detail_select_html', testapps.index_test_script_detail_select_html, name="index_test_script_detail_select_html"),
    path('html/index_test_script_detail_select_on_selected', testapps.index_test_script_detail_select_on_selected, name="index_test_script_detail_select_on_selected"),
    path('update/test_case_card_details',  testapps.update_test_case_card_details, name="update_test_case_card_details"),
    path('delete/test_case_card', testapps.delete_test_case_card, name="delete_test_case_card"),
    path('delete/test_script_detail', testapps.delete_test_script_detail, name="delete_test_script_detail"),
    path('create/test_case_card', testapps.create_test_case_card, name="create_test_case_card"),
    path('export/export_test_case_card', testapps.export_test_case_card, name="export_test_case_card")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
