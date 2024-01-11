from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, reverse, redirect
from django.urls import reverse_lazy

from ..models import Project
from ..utils import process_form_for_display


# MIXINS ----------------------------------------------------------------------

class ProjectMixin(LoginRequiredMixin):
    model = Project
    pk_url_kwarg = 'p_id'
    success_url = reverse_lazy('project-list')


class ProjectFormMixin(ProjectMixin, FormMixin):
    fields = '__all__'
    object = None
    request = None

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields.pop('team')
        return process_form_for_display(form, self.request.user)

    def form_valid(self, form):
        """ Adds the user who created the project to their project. """
        self.object = form.save()
        self.object.team.add(self.request.user, through_defaults={})
        return super().form_valid(form)


# VIEWS -----------------------------------------------------------------------

class ProjectList(ProjectMixin, ListView):
    context_object_name = 'projects'

    def get_queryset(self):
        """ Returns the current user's projects. """
        projects = self.request.user.projects.all()
        search_query = self.request.GET.get('search', '')
        if search_query:
            projects = projects.filter(name__icontains=search_query)
        return projects

    def get(self, request, *args, **kwargs):
        """ Clears the user's last visited project. """
        request.user.set_last_visited_project(None)
        return super().get(request, *args, **kwargs)


class ProjectDetail(ProjectMixin, DetailView):

    def get(self, request, *args, **kwargs):
        p_id = int(request.GET.get('project-id', -2))
        if p_id == -2:
            project = Project.objects.get(id=self.kwargs['p_id'])
            request.user.set_last_visited_project(project)
            return super().get(request, *args, **kwargs)
        elif p_id == -1:
            return redirect('project-list')
        else:
            return redirect(reverse('project-detail', args=[p_id]))


class ProjectCreate(ProjectFormMixin, CreateView):
    pass


class ProjectUpdate(ProjectFormMixin, UpdateView):
    pass


class ProjectDelete(ProjectMixin, DeleteView):

    def post(self, request, *args, **kwargs):
        """ Prevents non superusers from deleting a project. """
        if not request.user.is_superuser:
            return render(request, 'forbidden.html', status=403)
        return super().post(request, *args, **kwargs)
