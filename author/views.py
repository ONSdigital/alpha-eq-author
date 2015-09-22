from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.urlresolvers import reverse


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class WelcomeView(LoginRequiredMixin, TemplateView):
    template_name = 'welcome.html'


class LoginView(TemplateView):
    template_name = 'login.html'

    def post(self, request):

        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            # password is verified
            if user.is_active:
                login(request, user)
                if 'next' in request.GET:
                    return redirect(request.GET['next'])

                return redirect(reverse('welcome'))

        return HttpResponse('Sorry %s, your name\'s not down, you\'re not coming in.' % request.POST['username'])


class LogoutView(TemplateView):
    def get(self, request):
        logout(request)
        return redirect(reverse('welcome'))
