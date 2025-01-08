from django.shortcuts import redirect
from .models import Korisnik

def admin_required(function):
    def wrap(*args, **kwargs):
        if args[0].user.role == Korisnik.ADMIN:
            return function(*args, **kwargs)
        else:
            return redirect('dodaj_korisnika')
    return wrap

def profesor_required(function):
    def wrap(*args, **kwargs):
        if args[0].user.role == Korisnik.PROFESOR:
            return function(*args, **kwargs)
        else:
            return redirect('login')
    return wrap

def student_required(function):
    def wrap(*args, **kwargs):
        if args[0].user.role == Korisnik.STUDENT:
            return function(*args, **kwargs)
        else:
            return redirect('login')
    return wrap
