from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect, JsonResponse
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, REDIRECT_FIELD_NAME, login as auth_login
from django.shortcuts import redirect, resolve_url
from django.core.urlresolvers import reverse
from django.conf import settings
from survey.models import Questionnaire

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class WelcomeView(LoginRequiredMixin, TemplateView):
    template_name = 'welcome.html'

    def get(self, request, *args, **kwargs):
        return redirect(reverse("survey:index"))


class LogoutView(TemplateView):
    def get(self, request):
        print "here"
        unlock(request)
        logout(request)
        return redirect(reverse('welcome'))


def unlock(request):
    questionnaires = Questionnaire.objects.all().filter(locked_by=request.user.username)
    for questionnaire in questionnaires:
        questionnaire.locked_by = None
        questionnaire.locked_on = None
        questionnaire.save()


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())

            if request.is_ajax():
                return JsonResponse({"success":redirect_to})
            else:
                return HttpResponseRedirect(redirect_to)
        else:
            if request.is_ajax():
                return JsonResponse({'errors':form.errors})
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)

