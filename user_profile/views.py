import random
from django.shortcuts import render, redirect
from . import forms
from .forms import ChangeUserForm
from django.contrib.auth.forms import  AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login , update_session_auth_hash, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.conf import settings
from user_profile.models import Profile
from django.views.generic import FormView
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.generic import View
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.contrib.auth.models import User
from .forms import RegistrationForm
from django import forms
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import login
from django.contrib.auth import get_user_model



class UserLoginView(LoginView):
    template_name = 'user_login.html'
    def get_success_url(self):
        return reverse_lazy('homepage')

class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('homepage')


class UserRegistrationView(FormView):
    template_name = 'register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        user = form.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your account.'
        message = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

        messages.success(self.request, 'Please confirm your email address to complete the registration')
        return super().form_valid(form)
        
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Your account has been activated successfully')
        return redirect('homepage')
    else:
        messages.warning(request, 'Activation link is invalid!')
        return redirect('register')



class UserProfileUpdateView(View):
    template_name = 'edit_profile.html'

    def get(self, request):
        user = request.user
        profile = user.profile
        form = ChangeUserForm(instance=user, initial={
            'address': profile.address,
            'contact_number': profile.contact_number,
        })
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        user = request.user
        profile = user.profile
        form = ChangeUserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            profile.address = form.cleaned_data['address']
            profile.contact_number = form.cleaned_data['contact_number']
            profile.save()
            messages.success(request, 'Profile Updated Successfully')
            return redirect('homepage')
        return render(request, self.template_name, {'form': form})


class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('homepage')

from posts.models import Post

@login_required
def profile(request):
    data = Post.objects.filter(buyers=request.user)
    data2 = Post.objects.filter(author=request.user)
    return render(request, "profile.html", {'data': data, 'data2':data2})

 

@login_required
def pass_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password Updated Successfully')
            update_session_auth_hash(request, form.user)
            return redirect('profile')
        
    
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'pass_change.html', {'form' : form})


