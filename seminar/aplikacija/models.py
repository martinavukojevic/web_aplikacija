from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Korisnik(AbstractUser):
    STUDENT = 'stu'
    ADMIN = 'admin'
    PROFESOR = 'prof'
    ROLES = (('stu','student'),('admin','administrator'),('prof','profesor'))
    STATUS = (('None','None'),('red','redovni'),('izv','izvanredni'))
    role=models.CharField(max_length=50,choices=ROLES)
    status=models.CharField(max_length=50,choices=STATUS)

class Predmet(models.Model):
    IZBOR=(('da','da'),('ne','ne'))
    name=models.CharField(max_length=50)
    kod=models.CharField(max_length=50)
    program=models.CharField(max_length=50)
    ects=models.IntegerField()
    sem_red=models.IntegerField()
    sem_izv=models.IntegerField()
    izborni=models.CharField(max_length=50,choices=IZBOR)
    nositelj=models.ForeignKey(Korisnik,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.name
    
class Upisi(models.Model):
    STATUS=(('pass','passed'),('enr','enrolled'),('not','not selected'),('fail','failed'))
    student=models.ForeignKey(Korisnik,on_delete=models.CASCADE)
    predmet=models.ForeignKey(Predmet,on_delete=models.CASCADE)
    status=models.CharField(max_length=50,choices=STATUS)

