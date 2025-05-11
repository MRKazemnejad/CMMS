from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from accounts.models import ActiveSession
import sweetify




# Create your views here.

def login(request):
    if request.user.is_authenticated:
        return redirect('maintenance:dashboard')
    else:
        if request.method == 'POST':
            user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:


                # active_session = ActiveSession.objects.filter(user=user).first()
                # if active_session and active_session.session_key != request.session.session_key:
                #
                #     msg = "تست"
                #     sweetify.error(request, msg, persistent='تایید', timer='3000')
                #     return render(request, 'accounts/login.html')


                auth.login(request, user)

                # ActiveSession.objects.update_or_create(user=user,defaults={'session_key': request.session.session_key})
                return redirect('maintenance:dashboard')


            else:
                return render(request, 'accounts/page-404.html', {'error': 'نام کاربری یا کلمه عبور اشتباه است.'})
        else:
            return render(request, 'accounts/login.html')


def register(request):
    return render(request, 'accounts/register.html')


def logout(request):
    # ActiveSession.objects.filter(user=request.user).delete()
    auth.logout(request)
    return render(request, 'accounts/login.html')




