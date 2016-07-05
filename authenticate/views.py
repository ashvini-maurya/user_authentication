from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from authenticate.forms import UserForm
from datetime import datetime



def index(request):
    reset_last_access_t = False
    response = render(request, 'authenticate/index.html', {})
    if 'last_access_t' in request.COOKIES:
        last_access = request.COOKIES['last_access_t']

    else:
        reset_last_access_t = True
        response = render(request, 'authenticate/index.html', {})


    if reset_last_access_t:
        value = datetime.now()
        print value
        response.set_cookie('last_access_t', value)

    return response



def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print user_form.errors
    else:
        user_form = UserForm()

    return render(request,
            'authenticate/register.html',
            {'user_form': user_form, 'registered': registered} )



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/authenticate/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'authenticate/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/authenticate/')