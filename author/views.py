from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)

class WelcomeView(LoginRequiredMixin, TemplateView):
    template_name = 'welcome.html'

class AnotherView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

class LoginView(TemplateView):
    template_name = 'login.html'

    def post(self, request):
        return HttpResponse('Hello %s' % request.POST['username'])

