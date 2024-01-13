from django.views.generic import ListView, CreateView, DeleteView
from django.views.generic.edit import ContextMixin, FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, reverse, redirect
from django.db import IntegrityError

from ..models import Project, Member
from ..utils import process_form_for_display


class MemberMixin(LoginRequiredMixin, ContextMixin):
    model = Member
    pk_url_kwarg = 'm_id'
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


class MemberFormMixin(MemberMixin, FormMixin):
    fields = '__all__'
    request = None

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields.pop('project')
        return process_form_for_display(form, user=self.request.user)

    def form_valid(self, form):
        """ Sets this member's project to the project. """
        form.instance.project = self.project
        try:
            return super().form_valid(form)
        except IntegrityError:
            form.add_error('user', "This user is already a member of this project.")
            return self.form_invalid(form)


# VIEWS -----------------------------------------------------------------------

class MemberList(MemberMixin, ListView):
    context_object_name = 'members'

    def get_queryset(self):
        """ Returns this project's users. """
        members = self.project.members.all()
        search_query = self.request.GET.get('search', '')
        if search_query:
            members = members.filter(user__username__contains=search_query)
        return members

    def get(self, request, *args, **kwargs):
        p_id = int(request.GET.get('project-id', -2))
        if p_id == -2:
            request.user.set_last_visited_project(self.project)
            return super().get(request, *args, **kwargs)
        elif p_id == -1:
            return redirect('project-list')
        else:
            return redirect(reverse('member-list', args=[p_id]))


class MemberCreate(MemberFormMixin, CreateView):
    pass


class MemberDelete(MemberMixin, DeleteView):

    def post(self, request, *args, **kwargs):
        """ Prevents non guests from deleting a member. """
        if not request.user.is_staff:
            return render(request, 'forbidden.html', status=403)
        return super().post(request, *args, **kwargs)
