from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import ContextMixin, FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import BaseUserCreationForm
from django.shortcuts import get_object_or_404, render, reverse, redirect

from ..models import Project, User, Member
from ..utils import process_form_for_display


# FORMS -----------------------------------------------------------------------

class UserCreationForm(BaseUserCreationForm):
    """ Custom one """

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2',
                  'first_name', 'last_name', 'email', 'role']


# MIXINS ----------------------------------------------------------------------

class UserMixin(LoginRequiredMixin, ContextMixin):
    model = User
    pk_url_kwarg = 'u_id'
    kwargs = None
    project = None

    def dispatch(self, request, *args, **kwargs):
        """ Initialises the project attribute. """
        self.project = get_object_or_404(Project, id=self.kwargs['p_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        """ Returns the URL to go to after creating/editing/deleting. """
        return reverse('user-list', args=[self.project.id])

    def get_context_data(self, **kwargs):
        """ Appends the Project instance to the context. """
        context = super().get_context_data(**kwargs)
        context['project'] = self.project
        return context


class UserFormMixin(UserMixin, FormMixin):
    object = None
    request = None

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return process_form_for_display(form, user=self.request.user)

    def form_valid(self, form):
        """ Add this user to the project's team. """
        self.object = form.save()
        self.project.team.add(self.object, through_defaults={})
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['member'] = Member.objects.get(project=self.project,
                                                   user=self.object)
        return context


# VIEWS -----------------------------------------------------------------------

class UserList(UserMixin, ListView):
    context_object_name = 'users'

    def get_queryset(self):
        """ Returns this project's users. """
        users = self.project.team.all()
        search_query = self.request.GET.get('search', '')
        if search_query:
            users = users.filter(username__contains=search_query)
        return users

    def get(self, request, *args, **kwargs):
        p_id = int(request.GET.get('project-id', -2))
        if p_id == -2:
            request.user.set_last_visited_project(self.project)
            return super().get(request, *args, **kwargs)
        elif p_id == -1:
            return redirect('project-list')
        else:
            return redirect(reverse('user-list', args=[p_id]))


class UserCreate(UserFormMixin, CreateView):
    form_class = UserCreationForm


class UserUpdate(UserFormMixin, UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'role']


class UserDelete(UserMixin, DeleteView):

    def post(self, request, *args, **kwargs):
        """ Prevents non superusers from deleting a user. """
        if not request.user.is_staff:
            return render(request, 'forbidden.html', status=403)
        return super().post(request, *args, **kwargs)
