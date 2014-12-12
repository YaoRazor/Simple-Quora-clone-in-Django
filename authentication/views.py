from django.shortcuts import render
# Create your views here.
import hashlib
import datetime

from django.contrib import auth
from django.contrib.auth import authenticate
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from authentication.models import UserProfile
from authentication.forms import RegistrationForm, LoginForm
from django.http import HttpResponse

def register(request):
    return HttpResponse("Hello register")
#if request.user.is_authenticated():
# They already have an account; don't let them register again
    #    return render_to_response('core/register.html', {'has_account': True})
    if request.method == 'GET':
        c = {}
        c.update(csrf(request))
        c['form'] = RegistrationForm()
        return render_to_response('authentication/register.html', c)

    if not request.method == 'POST': return HttpResponseRedirect('/')
    registrationForm = RegistrationForm(request.POST)
    if registrationForm.is_valid():
        user = registrationForm.save(commit=False)
        user.is_active = False
        user.save()
        profile = UserProfile(user=user,
                              activation_key=hashlib.sha224(user.username).hexdigest()[:40],
                              key_expires=datetime.datetime.today() + datetime.timedelta(days=2)
        )
        profile.save()


        #host = request.META['SERVER_NAME']
        #email_subject = 'Welcome!'
        #email_body = """Thanks for signing up.  To activate your account, follow this link: http://%(host)s/accounts/confirm/%(hash)s"""
        #email_body = email_body % {'host': host, 'hash':profile.activation_key}

        #send_mail(email_subject, email_body, 'account_creator@' + host, [user.email])
        return render_to_response('authentication/register.html', {'created': True})
    c = {}
    c.update(csrf(request))
    c['form'] = registrationForm
    return render_to_response('authentication/register.html', c)


def confirm(request, activation_key):
    if request.user.is_authenticated():
        return render_to_response('authentication/confirm.html', {'has_account': True})
    user_profile = get_object_or_404(UserProfile,
                                     activation_key=activation_key)
    if user_profile.key_expires < datetime.datetime.today():
        return render_to_response('authentication/confirm.html', {'expired': True})
    user_account = user_profile.user
    user_account.is_active = True
    user_account.save()
    return render_to_response('authentication/confirm.html', {'success': True})

def login(request):
    if request.user.is_authenticated():
        redirect_to = request.REQUEST.get('next') or '/'
        #return HttpResponse("redirect")
        return HttpResponseRedirect(redirect_to)
    if request.method == 'GET':
        c = {}
        c.update(csrf(request))
        c['form'] = LoginForm()
        return render_to_response('authentication/login.html', c)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.clean()
            user = authenticate(username=data['username'], password=data['password'])
            if user and user.is_active:
                auth.login(request, user)
                redirect_to = request.REQUEST.get('next') or '/'
                return HttpResponseRedirect(redirect_to)
            else:
                c = {}
                c.update(csrf(request))
                c['error'] = 'this username could not be authenticated.  Please ensure this user exists and has been activated before logging in'
                c['form'] = form
                return render_to_response('authentication/login.html', c)
        c = {}
        c.update(csrf(request))
        c['form'] = form
        c['error'] = 'the username and/or password is incorrect'
        return render_to_response('authentication/login.html', c)
    return HttpResponseRedirect('/')

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return render_to_response('authentication/logout.html',  {})



# Create your views here.
