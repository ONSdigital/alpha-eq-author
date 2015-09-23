from django.views.generic import TemplateView, FormView
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


# class LoginView(FormView):
#     template_name = 'login.html'
#
#     def def_valid(self, form):
#         next = reverse('welcome')
#         if 'next' in self.request.GET:
#             next = self.request.GET['next']
#
#         username = form.cleaned_data['username']
#         password = form.cleaned_data['password']
#
#         user = authenticate(username=username, password=password)
#         if user is not None and user.is_active:
#             login(self.request, user)
#
#             return redirect(next)
#
#         form.errors.append('Invalid username and password')
#         return self.form_invalid(form)


class LogoutView(TemplateView):
    def get(self, request):
        logout(request)
        return redirect(reverse('welcome'))