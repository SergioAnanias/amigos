from django.shortcuts import render, HttpResponse, redirect
from main.models import *
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
import bcrypt
from main.decorators import loginauth

# Create your views here.

def friends(request):
    context= {
        'usuario': User.objects.get(id=request.session['user']),
        'usuarios': User.objects.all().exclude(id=request.session['user']), 
        'amigos': User.objects.get(id=request.session['user']).friends.all()
    }
    return render(request, 'friends.html',context)

def profile(request, id):
    context= {
        'usuario': User.objects.get(id=request.session['user']),
        'profile': User.objects.get(id=id)
    }
    return render(request, 'profile.html', context)
    
def newfriend(request):
    userA= User.objects.get(id=request.session['user'])
    userB= User.objects.get(id=request.POST['id'])
    userA.friends.add(userB)
    userB.friends.add(userA)
    return redirect('/friends')

def delete(request):
    userA= User.objects.get(id=request.session['user'])
    userB= User.objects.get(id=request.POST['id'])
    userA.friends.remove(userB)
    return redirect('/friends')