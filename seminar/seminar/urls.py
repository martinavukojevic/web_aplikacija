"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from aplikacija import views
from django.contrib.auth.views import LoginView, LogoutView
from aplikacija.views import UpdatedLoginView

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('dodaj_korisnika/', views.dodaj_korisnika, name="dodajKorisnika"),
    path('login/', UpdatedLoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='login.html'), name='logout'),
    path('home/<int:user_id>', views.home_page, name='home'),
    #path('accounts/profile', views.home_page)
    path('dodaj_predmet/', views.dodaj_predmet, name="dodajPredmet"),

    path('studenti_lista/', views.studenti_lista, name="studentiLista"),
    path('edit_studenta/<int:user_id>', views.edit_studenta, name="editStudenta"),
    path('dodaj_studenta/', views.dodaj_studenta, name="dodajStudenta"),
    path('studenti_na_predmetu_adm/<int:predmet_id>', views.studenti_na_predmetu_adm, name="studentiNaPredmetu1"), 
    path('studenti_na_predmetu_prof/<int:predmet_id>', views.studenti_na_predmetu_prof, name="studentiNaPredmetu2"), 


    path('profesori_lista/', views.profesori_lista, name="profesoriLista"),
    path('edit_profesora/<int:user_id>', views.edit_profesora, name="editProfesora"),
    path('dodaj_profesora/', views.dodaj_profesora, name="dodajProfesora"),

    path('predmeti_lista/', views.predmeti_lista, name="predmetiLista"),
    path('edit_predmeta/<int:predmet_id>', views.edit_predmeta, name="editPredmeta"),
    path('dodaj_predmet/', views.dodaj_predmet, name="dodajPredmet"),
    path('predmet_profesoru/', views.predmet_profesoru, name="dajPredmetProfesoru"),
    path('predmeti_od_profesora/<int:user_id>', views.predmeti_od_profesora, name="predmetiOdProfesora"),

    path('upisni_list_adm/<int:user_id>', views.upisni_list, name="upisniList"), 
    path('upisni_list_prof/<int:user_id>', views.upisni_list2, name="upisniList2"),
    path('upisni_list_stud/<int:user_id>', views.upisni_list3, name="upisniList3"),
    path('upisi_predmet/<int:user_id>/<int:predmet_id>', views.upisi_predmet, name='upisiPredmet'),
    path('ukloni_predmet/<int:user_id>/<int:predmet_id>', views.ukloni_predmet, name="ukloniPredmet"),
    path('polozio_predmet/<int:user_id>/<int:predmet_id>', views.polozio_predmet, name="polozioPredmet"), 
    path('izgubio_predmet/<int:user_id>/<int:predmet_id>', views.izgubio_predmet, name="izgubioPredmet"),


    #path('upisni_listovi_adm/', views.upisni_listovi_adm, name="upisniListoviAdm"),

    path('stud_koji_su_upisali/<int:predmet_id>', views.stud_koji_su_upisali, name="studKojiSuUpisali"),
    path('stud_koji_su_polozili/<int:predmet_id>', views.stud_koji_su_polozili, name="studKojiSuPolozili"),
    path('stud_koji_su_izg_potp/<int:predmet_id>', views.stud_koji_su_izg_potp, name="studKojiSuIzgPotp"),

    path('upisi_predmet_adm/<int:user_id>/<int:predmet_id>/', views.upisi_predmet_adm, name='upisiPredmetAdm'),
    path('ukloni_predmet_adm/<int:user_id>/<int:predmet_id>/', views.ukloni_predmet_adm, name='ukloniPredmetAdm'),
    path('polozio_predmet_adm/<int:user_id>/<int:predmet_id>/', views.polozio_predmet_adm, name='polozioPredmetAdm'),
    path('izgubio_predmet_adm/<int:user_id>/<int:predmet_id>/', views.izgubio_predmet_adm, name='izgubioPredmetAdm'),   
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)