from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, reverse, resolve_url

from ..models import User
from ..utils import pretty_form


class Login(LoginView):
    template_name = 'login.html'
    guest_login = False

    def get(self, request, *args, **kwargs):
        # If user is already logged in, then redirect them.
        if request.user.is_authenticated:
            return redirect(self.get_default_redirect_url())
        # If user clicks on View Demo button, then log them in under Guest.
        elif self.guest_login:
            user = authenticate(request, username='guest', password='guest')
            login(request, user)
            return redirect(self.get_default_redirect_url())
        # Otherwise show them the login page.
        else:
            return super().get(request, *args, **kwargs)

    def get_default_redirect_url(self):
        # Return URL user requested but was logged out so couldn't see
        if self.next_page:
            return resolve_url(self.next_page)
        user: User = self.request.user
        # Return URL of user's dashboard of their last visited project
        if user.last_visited_project:
            return reverse('project-detail',
                           kwargs={'p_id': user.last_visited_project.id})
        # Return URL of user's list of projects
        else:
            return reverse('project-list')


class Logout(LogoutView):
    template_name = 'logout.html'


class PasswordChange(PasswordChangeView):
    template_name = 'settings.html'
    success_url = 'settings'
    success_message = "Password successfully changed!"
    fail_message = "Password could not be updated. Please try again."

    def get_form(self, form_class=None):
        return pretty_form(
            form=super().get_form(form_class),
            user=self.request.user
        )

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            self.success_message,
            extra_tags='text-success'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(
            self.request,
            messages.WARNING,
            self.fail_message,
            extra_tags='text-danger'
        )
        return super().form_invalid(form)
