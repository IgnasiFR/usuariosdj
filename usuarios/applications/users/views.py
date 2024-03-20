from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import UserRegisterForm,LoginForm
from .models import User
from django.urls import reverse_lazy,reverse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.http import HttpResponseRedirect

# Create your views here.
class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = "/"

    def form_valid(self, form):

        User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            nombres = form.cleaned_data['nombres'],
            apellidos = form.cleaned_data['apellidos'],
            genero = form.cleaned_data['genero'],
        )
        return super(UserRegisterView,self).form_valid(form)
    
class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home_app:panel')


    def form_valid(self, form):
            user = authenticate(
                 username = form.cleaned_data['username'],
                 password = form.cleaned_data['password'],
                )
            login(self.request,user)
            return super(FormView,self).form_valid(form)
    
class LogoutView(View):
     def get(self, request, *args, **kargs):
          logout(request)
          return HttpResponseRedirect(reverse('users_app:user-login'))
          