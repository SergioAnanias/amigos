from django.db import models
import bcrypt
import re
from datetime import datetime, date

# Create your models here.
class UserManager(models.Manager):
    def validator(self, postData):
        errors={}

        if len(postData["name"]) < 3:
            errors["name"]="Su nombre debe contener al menos 5 caracteres"
        if len(postData["nickname"]) < 3:
            errors["nickname"]="Su alias debe contener al menos 3 caracteres"
        if len(User.objects.filter(alias=postData["nickname"]))>0:
            errors["nickname"]="El alias ya fue tomado"
# Valida si el campo esta vacio o no
        if len(postData["email"])>0:
            EMAIL_REGEX=re.compile(r'[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+')
# Valida si el email sigue una expresión regular
            if not re.match(EMAIL_REGEX, postData["email"]):
                errors["email"]="Email no valido"
# Valida si el correo existe o no
            if len(User.objects.filter(email=postData["email"])) > 0:
                errors["exists"]= "El correo ya existe"
# Valida la longitud de la contraseña
        if len(postData["password"]) == 0 or len(postData["password"]) < 5:
            errors["passwordlen"]= "La contraseña debe tener al menos 5 caracteres"
#Valida si las constraseñas coinciden
        elif postData["password"] != postData["cpassword"]:
            errors["password"] = "Las contraseñas no coinciden"
#Valida si la fecha no esta nula, es una fecha valida, y ademas si es que la fecha esta en pasado
        if len(postData["dateborn"]) == 0 or len(postData["dateborn"]) < 10 or datetime.strptime(postData["dateborn"], "%Y-%m-%d") > datetime.now(): 
            errors["age"] = "Debe ingresar una fecha de nacimiento valida"
        else:
            fechanacimiento = datetime.strptime(postData["dateborn"], "%Y-%m-%d")
            tiempoactual = datetime.now() # Fecha de registro
            edad = tiempoactual - fechanacimiento #Edad del usuario
            minedad = 16 * 365 #Minimo de edad para registrarse
            if edad.days < minedad: # Revisa si el usuario tiene cierta edad 
                errors["minage"] = "Debe tener al menos 16 años"
        return errors
# Valida la información del login
    def loginvalidator(self, postData):
        errors={}
        if len(User.objects.filter(email=postData["email"])) == 0:
            errors['notfound']= "Not valid login"
        else:
            pw1= User.objects.get(email=postData["email"]).password
            if not bcrypt.checkpw(postData['password'].encode(), pw1.encode()):
                errors['password']="Not valid login"
        return errors

class Permission(models.Model):
    CHOICES =(
        ('admin', 'Admin'),
        ('usuario', 'Usuario'),
        ('block', 'Ban')
    )
    permissionLevel = models.CharField(max_length=10, choices=CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.permissionLevel}"

class User(models.Model):
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    dateborn = models.DateField()
    friends= models.ManyToManyField("self", blank=True, null=True)
    permission = models.ForeignKey(Permission, related_name='users', blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects= UserManager()