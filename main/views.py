from django.shortcuts import render, HttpResponse, redirect
from main.models import *
from django.contrib import messages
from django.http import JsonResponse
import bcrypt
from .decorators import loginauth

# Decorador de login
@loginauth
def index(request):
#Primero verifica si el usuario esta en la sesión, si no está lo manda al login, y si esta renderiza el index
    context={
        "usuario": User.objects.get(id=request.session['user']),
    }
    return render(request, 'index.html',context)

def login(request):
#Render pantalla de login
    if not 'user' in request.session or not request.session['user']:
        return render(request, "login.html")
    return redirect("/")

def registerForm(request):
    if not 'user' in request.session or not request.session['user']:
        return render(request, "register.html")
#Render formulario de registro
    return redirect("/")

def register(request):
    if not 'user' in request.session or not request.session['user']:
        if request.method == "POST":
            errors = User.objects.validator(request.POST)
        # En caso de que se devuelvan errores del validador, se guardan con messages y se redirecciona al formulario de registro para mostrarlos
            if len(errors) > 0:
                for k, v in errors.items():
                    messages.error(request, v)
                return redirect("/register")
        #hashea la pw
            pwhash = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()
        #Crea un nuevo registro
            permission = 'usuario'
            if len(User.objects.all()) == 0:
                permission = 'admin'
        # Se intenta obtener el permiso, si no existe se crea
            try:
                permissionlevel= Permission.objects.get(permissionLevel=permission)
            except:
                permissionlevel= Permission.objects.create(permissionLevel=permission)
        # Se crea el usuario
            nuevo_usuario = User.objects.create(
                name=request.POST["name"],
                alias=request.POST["nickname"],
                email=request.POST["email"],
                password=pwhash,
                dateborn=request.POST["dateborn"],
                permission= permissionlevel
            )
        # Se logea el usuario
            request.session['user'] = nuevo_usuario.id
            if permission == 'admin':
                request.session['admin'] = True
            messages.success(request, "Registered in successfully")
        # Luego de crear el registro redirecciona al index
            return redirect("/")
    else:
        return redirect("/")

@loginauth
# Limpia el request.session borrando todo lo de la session y redireccionando al login
def logout(request):
    request.session.flush()
    return redirect("/login")

def logged(request):
    errors = User.objects.loginvalidator(request.POST)
    if len(errors)> 0:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect("/login")
    request.session['user'] = User.objects.get(email=request.POST["email"]).id
    request.session['permission'] = User.objects.get(email=request.POST["email"]).permission.permissionLevel
    if request.session['permission'] == 'admin':
        request.session['admin'] = True
    messages.success(request, "Logged in successfully")
    return redirect("/")


