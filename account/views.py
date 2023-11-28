from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from users.forms import CustomUserCreationForm
from news_api.models import *
from email.message import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from users.models import CustomUser
from django.core.mail import EmailMessage



API_KEY = '981b08fa899d4d44b490545678025616'


def login_page(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            username_lower = username.lower()

            user = authenticate(request, username=username_lower, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Username or Password is incorrect')

        context = {}
        return render(request, 'accounts/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


def register_page(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False  # Deactivate the user until email confirmation

                # Check password complexity
                password = form.cleaned_data['password1']
                if (
                    not any(char.isupper() for char in password) or
                    not any(char.isdigit() for char in password) or
                    not any(char in '!@#$%^&*()_+{}:;<>,.?~' for char in password)
                ):
                    messages.error(
                        request, "Password must contain a capital letter, a number, and a special character."
                    )
                    return render(request, 'accounts/register.html', {'form': form})

                email = form.cleaned_data['email']

                user.save()

               # Send email confirmation
                current_site = get_current_site(request)
                subject = 'Activate your account'
                message = render_to_string('accounts/account_activation_email.html', {
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                to_email = email
                send_email = EmailMessage(subject, message, to=[to_email])
                send_email.send()

                # messages.success(request, 'Thank you for registering with us. Kindly check your email to activate your Account')  # noqa
                return redirect('account_activation_sent')

                # messages.success(
                # request, f'Account was created for {user.username}')
                # return redirect('login')
        else:
            form = CustomUserCreationForm()

        context = {'form': form}
        return render(request, 'accounts/register.html', context)


def account_activation_sent(request):
    return render(request, 'accounts/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # messages.success(request, 'Congratulations! your account has been activated.') #noqa
        return redirect('account_activation_complete')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('account_invalid_link')


def account_activation_complete(request):
    return render(request, 'accounts/account_activation_complete.html')


def account_invalid_link(request):
    return render(request, 'accounts/account_invalid_link.html')
