from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.core.urlresolvers import reverse


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
        logout(request)
        return redirect(reverse('welcome'))
