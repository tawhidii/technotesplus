from django.shortcuts import render, redirect, get_object_or_404
from .forms import (
    RegistrationForm,
    LoginForm
)
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.contrib.auth.models import User
from .models import Profile


# view for user login
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home:home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home:home')
            else:
                messages.error(request, 'Invalid login or inactive account !!')
    else:
        form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)


# view for user registration
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.is_active = False  # Deactivate User Until Email activation done
            new_user.save()
            current_site = get_current_site(request)
            subject = 'Account Activation'
            message = render_to_string('accounts/account_activation_email.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': account_activation_token.make_token(new_user)
            })
            new_user.email_user(subject, message)  ## Send Email

            messages.success(request, 'Registration Done. Please check email to confirm account')
            return redirect('accounts:register')
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, "accounts/register.html", context)


# Account activation via email view (CBV)
class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):

            profile = get_object_or_404(Profile, user=user)
            profile.email_confirmed = True
            profile.save()
            user.is_active = True
            user.save()

            messages.success(request, 'Your account have been confirmed. Now login')
            return redirect('accounts:login')
        else:
            messages.warning(request, 'The confirmation link was invalid, possibly because it has already been used.')
            return redirect('accounts:login')
