from django.shortcuts import render, HttpResponse, redirect
def loginauth(func):
    def wrapper(request):
        if not 'user' in request.session or not request.session['user']:
            return redirect("/login")
        return func(request)
    return wrapper