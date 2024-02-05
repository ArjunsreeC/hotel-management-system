from django.shortcuts import render, redirect
from rest_framework import generics
from .models import User, Customer
from .serializers import UserSerializer
from .forms import UserForm, CustomerSignupForm

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users')
    else:
        form = UserForm()
    return render(request, 'register.html', {'form': form})

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request):
        users = self.get_queryset()
        return render(request, 'users.html', {'users': users})

def customer_signup(request):
    if request.method == 'POST':
        form = CustomerSignupForm(request.POST)
        if form.is_valid():
            user_data = {
                'email': form.cleaned_data['email'],
                'age': form.cleaned_data['age'],
                'address': form.cleaned_data['address'],
                'contact_number': form.cleaned_data['contact_number'],
                'password': form.cleaned_data['password']
            }
            user_instance = User(**user_data)
            user_instance.save()
            customer_data = {
                'name': form.cleaned_data['name'],
                'tier': form.cleaned_data['tier'],
                'dietary_preference': form.cleaned_data['dietary_preference'],
                'user': user_instance
            }
            customer_instance = Customer(**customer_data)
            customer_instance.save()
            request.session['user_id'] = user_instance.id
            request.session['access_type'] = 'Customer'
            request.session['logged_in'] = True
            return redirect('home')
    else:
        form = CustomerSignupForm()
    print(form)
    return render(request, 'signup.html', {'form': form})