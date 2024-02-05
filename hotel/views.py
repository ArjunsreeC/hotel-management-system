from django.shortcuts import render, redirect
from django.contrib import messages

from .user.models import User
from .user.forms import CustomUserLoginForm

def custom_login(request):
    error_message = None
    
    if request.method == 'POST':
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(email=email)
                
                if user.password == password:
                    request.session['user_id'] = user.id
                    request.session['access_type'] = user.access_type
                    request.session['logged_in'] = True
                    return redirect('home')
                else:
                    error_message = 'Invalid email or password.'
            except User.DoesNotExist:
                error_message = 'Invalid email or password.'
        else:
            pass
    else:
        form = CustomUserLoginForm()

    return render(request, 'login.html', {'form': form, 'error_message': error_message})

def custom_logout(request):
    request.session['access_type'] = None
    request.session['logged_in'] = False
    return redirect('home')