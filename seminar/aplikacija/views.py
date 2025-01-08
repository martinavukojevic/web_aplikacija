from django.shortcuts import render, redirect, get_object_or_404
from .models import Korisnik, Predmet, Upisi
from .forms import KorisnikForm, PredmetiForm
from django.http import HttpResponseNotAllowed, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.db.models import Count

from django.db.models import Max
from django.contrib.auth.views import LoginView 
from .forms import PredmetProfesoruForm

from django.urls import reverse  
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from .decorators import admin_required,profesor_required,student_required

# Create your views here.

class UpdatedLoginView(LoginView):
    def get_success_url(self):
        user_id = self.request.user.id
        return f'/home/{user_id}'
    


@login_required
def dodaj_korisnika(request):
    if request.method == 'GET':
        form = KorisnikForm()
        return render(request, 'dodaj_korisnika.html', {'form': form})
    elif request.method == 'POST':
        form = KorisnikForm(request.POST)
        if form.is_valid():
            #print(form.cleaned_data.get('password'))
            form.save()
            return redirect('dodajKorisnika')
        else:
            return HttpResponseNotAllowed()
####


@login_required
def home_page(request, user_id):
    user = Korisnik.objects.get(id=user_id)
    return render(request, 'home.html', {'username': user.username, 'role': user.role, 'user_id': user_id})


########ADMIN VIEWOVI



@login_required
@admin_required
def studenti_lista(request):
    studenti = Korisnik.objects.filter(role="stu")

    user_id = request.user.id  #ovo je za link da se mozemo vratit na home page od logiranog usera
    return render(request, 'studenti_lista.html', {'studenti': studenti, 'user_id': user_id})



@login_required
@admin_required
def dodaj_studenta(request):
    if request.method == 'GET':
        form = KorisnikForm()

    elif request.method == 'POST':
        form = KorisnikForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            if role != 'stu':
                form.add_error('role', 'Samo se student moze dodati!')
                #return render(request, 'dodaj_studenta.html', {'form': form})
            else:
                form.save()
                return redirect('studentiLista')
    return render(request, 'dodaj_studenta.html', {'form': form})



@login_required
@admin_required
def edit_studenta(request, user_id):
    student = Korisnik.objects.get(pk=user_id) #uzima pravog korisnika
    if request.method == 'GET':
        form = KorisnikForm(instance=student)
        return render(request, 'edit_student.html', {'form': form})
    elif request.method == 'POST':
        form = KorisnikForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('studentiLista') #ako stisnemo submit vraca nas na listu
#########



@login_required
@admin_required
def predmeti_lista(request):
    predmeti = Predmet.objects.all()
    user_id = request.user.id
    return render(request, 'predmeti_lista.html', {'predmeti': predmeti, 'user_id': user_id})



@login_required
@admin_required
def edit_predmeta(request, predmet_id):
    predmet = Predmet.objects.get(pk=predmet_id)
    if request.method == 'GET':
        form = PredmetiForm(instance=predmet)
        return render(request, 'edit_predmeta.html', {'form': form})
    elif request.method == 'POST':
        form = PredmetiForm(request.POST, instance=predmet)
        if form.is_valid():
            form.save()
            return redirect('predmetiLista')
        


@login_required
@admin_required
def dodaj_predmet(request):
    if request.method == 'GET':
        form = PredmetiForm()
        return render(request, 'dodaj_predmet.html', {'form': form})
    elif request.method == 'POST':
        form = PredmetiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('predmetiLista')
        else:
            return HttpResponseNotAllowed
        



@login_required
@admin_required
def predmet_profesoru(request): 
    if request.method == 'GET':
        form = PredmetProfesoruForm()
        return render(request, 'predmet_profesoru.html', {'form': form})
    elif request.method == 'POST':
        form = PredmetProfesoruForm(request.POST)
        if form.is_valid():
            #form.save()
            predmet = form.cleaned_data['predmet']
            profesor = form.cleaned_data['profesor']
            

            predmet.nositelj = profesor
            predmet.save()
            return redirect('dajPredmetProfesoru')
    else:
        return HttpResponseNotAllowed




@login_required
@admin_required
def profesori_lista(request):
    profesori = Korisnik.objects.filter(role='prof')

    user_id = request.user.id
    return render(request, 'profesori_lista.html', {'profesori': profesori, 'user_id': user_id})



@login_required
@admin_required
def dodaj_profesora(request):
    if request.method == 'GET':
        form = KorisnikForm()
        return render(request, 'dodaj_profesora.html', {'form': form})
    elif request.method == 'POST':
        form = KorisnikForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profesoriLista')
        


@login_required   
@admin_required
def edit_profesora(request, user_id):
    profesor = Korisnik.objects.get(pk=user_id)
    if request.method == 'GET':
        form = KorisnikForm(instance=profesor)
        return render(request, 'edit_profesora.html', {'form': form})
    elif request.method == 'POST':
        form = KorisnikForm(request.POST, instance=profesor)
        if form.is_valid():
            form.save()
            return redirect('profesoriLista')



@login_required
@admin_required
def studenti_na_predmetu_adm(request, predmet_id):
    upisi_sa_predmetom = Upisi.objects.filter(predmet=predmet_id)
    studenti_sa_predmetom = [upis.student for upis in upisi_sa_predmetom]
    predmet_objekt = Predmet.objects.get(pk=predmet_id)

    user_id = request.user.id #nacin za dohvacanje usera koji je logiran trenutno!!
    return render(request, 'studenti_na_predmetu.html', {'predmet': predmet_objekt, 'studenti_objekti': studenti_sa_predmetom, 'user_id': user_id})

@login_required
@admin_required
def upisni_list(request, user_id): #ovde je user_id korisnika 
    student = Korisnik.objects.get(pk=user_id) #trazi se student
    upisani_predmeti = Upisi.objects.filter(student=student).values_list('predmet', flat=True) #ovo koristimo samo da nademo neupisane
    neupisani_predmeti = Predmet.objects.exclude(id__in=upisani_predmeti) #id__in= ako se oce dohvatiti vise id-eva, a id= ako samo 1


    upisani_predmeti_iz_Predmeti = Predmet.objects.filter(id__in=upisani_predmeti)
    upisani_predmeti_sve = Upisi.objects.filter(student=student)

    polozeni_predmeti = Upisi.objects.filter(student=student, status="polozen").values_list('predmet_id', flat=True) 
    nepolozeni_predmeti = Upisi.objects.filter(student=student, status="izg_potpis").values_list('predmet_id', flat=True)

    user_id_logirani = request.user.id 
    user_obj_logirani = Korisnik.objects.get(id=user_id_logirani)

    return render(request, 'upisni_list.html', {'neupisani_predmeti': neupisani_predmeti, 'upisani_predmeti': upisani_predmeti_iz_Predmeti, 
    'user_id': user_id, 'student': student, 'user_obj_logirani': user_obj_logirani, 'upisani_predmeti_sve': upisani_predmeti_sve, 
    'polozeni_predmeti': polozeni_predmeti, 'nepolozeni_predmeti': nepolozeni_predmeti})



@login_required
@admin_required
def polozio_predmet_adm(request, user_id, predmet_id):
    student = Korisnik.objects.get(pk=user_id)
    predmet = Predmet.objects.get(pk=predmet_id)

    upisani = Upisi.objects.filter(student=student, predmet=predmet)
    
    if upisani.exists():
        upisani.update(status='polozen')
    else:
        
        pass
    
    return redirect('upisniList', user_id=user_id)




@login_required
@admin_required
def izgubio_predmet_adm(request, user_id, predmet_id):
    student = Korisnik.objects.get(pk=user_id)
    predmet = Predmet.objects.get(pk=predmet_id)

    upisani = Upisi.objects.filter(student=student, predmet=predmet)
    
    if upisani.exists():
        upisani.update(status='izg_potpis')
    else:
       
        pass
    
    return redirect('upisniList', user_id=user_id)



@login_required
@admin_required
def upisi_predmet_adm(request, user_id, predmet_id):
    student = Korisnik.objects.get(pk=user_id)
    predmet = Predmet.objects.get(pk=predmet_id)
    Upisi.objects.create(student=student, predmet=predmet, status="upisan")
    return redirect('upisniList', user_id=user_id)


@login_required
@admin_required
def ukloni_predmet_adm(request, user_id, predmet_id):
    student = Korisnik.objects.get(pk=user_id)
    predmet = Predmet.objects.get(pk=predmet_id)

    upisani = Upisi.objects.filter(student=student, predmet=predmet)
    
    if upisani.exists():
        upisani.delete()
    else:
      
        pass
    
    return redirect('upisniList', user_id=user_id)

########PROFESOR VIEWOVI
@login_required
@profesor_required
def upisni_list2(request, user_id):
    profesor = request.user
    profesorovi_predmeti = Predmet.objects.filter(nositelj=profesor)
    #print(f"Profesorovi predmeti: {profesorovi_predmeti}")
    student = Korisnik.objects.get(pk=user_id)
    upisani_predmeti = Upisi.objects.filter(student=student, predmet__in=profesorovi_predmeti).values_list('predmet', flat=True)
    neupisani_predmeti = profesorovi_predmeti.exclude(id__in=upisani_predmeti)

    upisani_predmeti_iz_Predmeti = profesorovi_predmeti.filter(id__in=upisani_predmeti)
    upisani_predmeti_sve = Upisi.objects.filter(student=student, predmet__in=profesorovi_predmeti)

    polozeni_predmeti = Upisi.objects.filter(student=student, predmet__in=profesorovi_predmeti, status="polozen").values_list('predmet_id', flat=True)
    nepolozeni_predmeti = Upisi.objects.filter(student=student, predmet__in=profesorovi_predmeti, status="izg_potpis").values_list('predmet_id', flat=True)

    user_id_logirani = request.user.id
    user_obj_logirani = Korisnik.objects.get(id=user_id_logirani)

    return render(request, 'upisni_list_prof.html', {
        'neupisani_predmeti': neupisani_predmeti,
        'upisani_predmeti': upisani_predmeti_iz_Predmeti,
        'user_id': user_id,
        'student': student,
        'user_obj_logirani': user_obj_logirani,
        'upisani_predmeti_sve': upisani_predmeti_sve,
        'polozeni_predmeti': polozeni_predmeti,
        'nepolozeni_predmeti': nepolozeni_predmeti,
        'profesorovi_predmeti': profesorovi_predmeti  
    })




@login_required
@profesor_required
def studenti_na_predmetu_prof(request, predmet_id):
    upisi_sa_predmetom = Upisi.objects.filter(predmet=predmet_id)
    studenti_sa_predmetom = [upis.student for upis in upisi_sa_predmetom]
    predmet_objekt = Predmet.objects.get(pk=predmet_id) 

    user_id = request.user.id #nacin za dohvacanje usera koji je logiran trenutno!!
    return render(request, 'studenti_na_predmetu.html', {'predmet': predmet_objekt, 'studenti_objekti': studenti_sa_predmetom, 'user_id': user_id})





@login_required
@profesor_required
def predmeti_od_profesora(request, user_id):
    profesorovi_predmeti = Predmet.objects.filter(nositelj_id=user_id)
    return render(request, 'predmeti_od_profesora.html', {'predmeti': profesorovi_predmeti, 'user_id': user_id})

##!ne mozemo putem get zahtjeva promijenit status ako je vec odreden-mozemo mijenjati
##samo predmete koji su upisani,ali ne i polozeni/izgubljneni

@login_required
@profesor_required
def polozio_predmet(request, user_id, predmet_id):
    student = Korisnik.objects.get(pk=user_id)
    predmet = Predmet.objects.get(pk=predmet_id)

    upisani = Upisi.objects.get(student=student, predmet=predmet)
    upisani.status = 'polozen'
    upisani.save()
    return redirect('upisniList2', user_id=user_id)




@login_required
@profesor_required
def izgubio_predmet(request, user_id, predmet_id):
    student = Korisnik.objects.get(pk=user_id)
    predmet = Predmet.objects.get(pk=predmet_id)

    upisani = Upisi.objects.get(student=student, predmet=predmet)
    upisani.status = 'izg_potpis'
    upisani.save()
    return redirect('upisniList2', user_id=user_id)



@login_required
@profesor_required
def stud_koji_su_upisali(request, predmet_id):
    studenti_id = Upisi.objects.filter(predmet=predmet_id).values('student_id') #id-evi studenata
    studenti_koji_su_upisali = Korisnik.objects.filter(id__in=studenti_id)
    return render(request, 'stud_koji_su_upisali.html', {'studenti': studenti_koji_su_upisali})




@login_required
@profesor_required
def stud_koji_su_polozili(request, predmet_id):
    studenti_id = Upisi.objects.filter(predmet=predmet_id, status="polozen").values('student_id')
    studenti_koji_su_polozili = Korisnik.objects.filter(id__in=studenti_id)
    return render(request, 'stud_koji_su_polozili.html', {'studenti': studenti_koji_su_polozili})




@login_required
@profesor_required
def stud_koji_su_izg_potp(request, predmet_id):
    studenti_id = Upisi.objects.filter(predmet=predmet_id, status="izg_potpis").values('student_id')
    stud_koji_su_izg_potp = Korisnik.objects.filter(id__in=studenti_id)
    return render(request, 'stu_koji_su_izg_potp.html', {'studenti': stud_koji_su_izg_potp})


##########STUDENT VIEWOVI




@login_required
@student_required
def upisni_list3(request, user_id):  
    student = Korisnik.objects.get(pk=user_id) 
    upisani_predmeti = Upisi.objects.filter(student=student).values_list('predmet', flat=True) #ovo koristimo samo da nademo neupisane
    neupisani_predmeti = Predmet.objects.exclude(id__in=upisani_predmeti) #id__in= ako se oce dohvatiti vise id-eva, a id= ako samo 1
    

    upisani_predmeti_iz_Predmeti = Predmet.objects.filter(id__in=upisani_predmeti)
    upisani_predmeti_sve = Upisi.objects.filter(student=student)

    polozeni_predmeti = Upisi.objects.filter(student=student, status="polozen").values_list('predmet_id', flat=True) 
    nepolozeni_predmeti = Upisi.objects.filter(student=student, status="izg_potpis").values_list('predmet_id', flat=True)

    user_id_logirani = request.user.id 
    user_obj_logirani = Korisnik.objects.get(id=user_id_logirani) 

    return render(request, 'upisni_list_stud.html', {'neupisani_predmeti': neupisani_predmeti, 'upisani_predmeti': upisani_predmeti_iz_Predmeti, 
    'user_id': user_id, 'student': student, 'user_obj_logirani': user_obj_logirani, 'upisani_predmeti_sve': upisani_predmeti_sve, 
    'polozeni_predmeti': polozeni_predmeti, 'nepolozeni_predmeti': nepolozeni_predmeti})



@login_required
@student_required
def upisi_predmet(request, user_id, predmet_id):
    student = Korisnik.objects.get(pk=user_id)
    predmet = Predmet.objects.get(pk=predmet_id)
    #if Upisi.objects.filter(student=user_id, predmet=predmet_id).exists():


    Upisi.objects.create(student=student, predmet=predmet, status="upisan")
    #return redirect(reverse('upisniList', args=[user_id])) #ide na path upisni_list/<user_id>
    return redirect('upisniList3', user_id=user_id)
    #return render(request, 'upisni_list.html', {'user_id': user_id, 'predmet_id': predmet_id})




@login_required
@student_required
def ukloni_predmet(request, user_id, predmet_id):
    student = Korisnik.objects.get(pk=user_id)
    predmet = Predmet.objects.get(pk=predmet_id)

    upisani = Upisi.objects.get(student=student, predmet=predmet)
    upisani.delete()
    return redirect('upisniList3', user_id=user_id)


##############

@login_required
def upisni_listovi_adm(request):
    studenti = Korisnik.objects.filter(role='stu')

    user_id = request.user.id #id logiranog usera kako bi se moga vratit u home, ovo saljemo u context
    return render(request, 'upisni_listovi_adm.html', {'studenti': studenti, 'user_id': user_id})

@login_required
def upisni_listovi_prof(request):
    studenti = Korisnik.objects.filter(role='stu')

    user_id = request.user.id
    return render(request, 'upisni_listovi_prof.html', {'studenti': studenti, 'user_id': user_id})



  