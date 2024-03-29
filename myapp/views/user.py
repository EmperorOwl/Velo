from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic.edit import ContextMixin, FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import BaseUserCreationForm, SetPasswordForm
from django.forms.models import modelform_factory
from django.shortcuts import get_object_or_404, reverse, redirect

from ..models import Project, User, Member
from ..utils import pretty_form


# FORMS -----------------------------------------------------------------------

class UserCreationForm(BaseUserCreationForm):
    """ Custom form """

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2',
                  'first_name', 'last_name', 'email']


ChangeRole = modelform_factory(Member, fields=['role'])


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
        return reverse('member-list', args=[self.project.id])

    def get_context_data(self, **kwargs):
        """ Appends the Project instance to the context. """
        context = super().get_context_data(**kwargs)
        context['project'] = self.project
        return context


class UserFormMixin(UserMixin, FormMixin):
    context_object_name = 'object'  # Prevents conflict with request.user
    object = None
    request = None

    def get_form(self, form_class=None):
        return pretty_form(
            form=super().get_form(form_class),
            user=self.request.user
        )

    def form_valid(self, form):
        # Add this user to the project's team (will not add duplicate).
        self.object = form.save()
        self.project.team.add(self.object, through_defaults={})
        # Role will always be valid as it is a dropdown, so skip validation.
        Member.objects.update_or_create(
            user=self.object,
            project=self.project,
            defaults={'role': self.request.POST['role']}
        )
        form3 = SetPasswordForm(self.object, self.request.POST)
        if self.request.POST['new_password1']:
            if form3.is_valid():
                form3.save()
            else:
                return super().form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Pass member instance and change role form.
        context = super().get_context_data(**kwargs)
        if self.object:
            member = Member.objects.get(project=self.project,
                                        user=self.object)
            context['member'] = member
            context['form2'] = ChangeRole(instance=member)
            context['form3'] = SetPasswordForm(user=member.user)
            for field in context['form3'].fields.values():
                field.required = False
        else:
            context['form2'] = ChangeRole()
        context['form2'] = pretty_form(
            form=context['form2'],
            user=self.request.user
        )
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
            return redirect(reverse('member-list', args=[p_id]))


class UserCreate(UserFormMixin, CreateView):
    form_class = UserCreationForm


class UserUpdate(UserFormMixin, UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
