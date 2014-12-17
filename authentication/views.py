# Create your views here.
import datetime

from django.core.urlresolvers import reverse
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from authentication.models import UserProfile
from django.http import HttpResponse
from authentication.forms import MyRegistrationForm
from django.core.context_processors import csrf



# def confirm(request, activation_key):
#     if request.user.is_authenticated():
#         return render_to_response('authentication/confirm.html', {'has_account': True})
#     user_profile = get_object_or_404(UserProfile,
#                                      activation_key=activation_key)
#     if user_profile.key_expires < datetime.datetime.today():
#         return render_to_response('authentication/confirm.html', {'expired': True})
#     user_account = user_profile.user
#     user_account.is_active = True
#     user_account.save()
#     return render_to_response('authentication/confirm.html', {'success': True})


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return HttpResponseRedirect(reverse('authentication:logout_success'))


def logout_success(request):
    return render_to_response('authentication/logout_success.html')


def profile(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('polls:index'))
    else:
        return HttpResponse("login not successfully")
        return render_to_response('authentication/logout.html',  {})

def register_user(request):
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)
        print form
        if form.is_valid():
            form.save()
            print "here"
            return HttpResponseRedirect(reverse('authentication:register_success'))
        
    else:
        form = MyRegistrationForm()
    args = {}
    args.update(csrf(request))
    
    args['form'] = form
    
    return render_to_response('authentication/register.html', args)



def register_success(request):
    return render_to_response('authentication/register_success.html')


