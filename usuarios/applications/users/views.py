from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import UserRegisterForm,LoginForm,UpdatePasswordForm
from .models import User
from django.urls import reverse_lazy,reverse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import forms
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
          

class UpdatePassword(LoginRequiredMixin,FormView):
    template_name = 'users/update.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:user-login')
    login_url = reverse_lazy('users_app:user-login')


    def form_valid(self, form):
        usuario = self.request.user
        user = authenticate(
            username=usuario.username,
            password=form.cleaned_data['password1']
        )

        if user:
            new_password = form.cleaned_data['password2']
            usuario.set_password(new_password)
            usuario.save()
            logout(self.request)
            return super(UpdatePassword, self).form_valid(form)
        else:
            # Aquí agregamos el mensaje de error al formulario y luego renderizamos el template
            # con el formulario que contiene los errores.
            form.add_error(None, 'La contraseña actual no es la correcta')
            # Renderizar el mismo formulario con errores
            return self.form_invalid(form)

    def form_invalid(self, form):
        # Asegúrate de manejar adecuadamente la renderización para formularios inválidos.
        return render(self.request, self.template_name, {'form': form})
    
