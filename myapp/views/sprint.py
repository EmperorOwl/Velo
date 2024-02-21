from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.edit import ContextMixin, FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, reverse, redirect

from ..models import Project, Sprint, Task
from ..choices import TaskStatus
from ..utils import pretty_form


# MIXINS ----------------------------------------------------------------------

class SprintMixin(LoginRequiredMixin, ContextMixin):
    model = Sprint
    pk_url_kwarg = 's_id'
    kwargs = None
    project = None

    def dispatch(self, request, *args, **kwargs):
        """ Initialises the project attribute. """
        self.project = get_object_or_404(Project, id=self.kwargs['p_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        """ Returns the URL to go to after creating/editing/deleting. """
        return reverse('sprint-list', args=[self.project.id])

    def get_context_data(self, **kwargs):
        """ Appends the Project instance to the context. """
        context = super().get_context_data(**kwargs)
        context['project'] = self.project
        return context


class SprintFormMixin(SprintMixin, FormMixin):
    fields = '__all__'
    request = None

    def get_form(self, form_class=None):
        """ Removes selection of which project from form. """
        form = super().get_form(form_class)
        form.fields.pop('project')
        return pretty_form(form, self.request.user)

    def form_valid(self, form):
        """ Sets this sprint's project to the project. """
        form.instance.project = self.project
        return super().form_valid(form)


# VIEWS -----------------------------------------------------------------------

class SprintList(SprintMixin, ListView):
    context_object_name = 'sprints'

    def get_queryset(self):
        """ Returns this project's sprints. """
        sprints = self.project.sprints.order_by('status')
        search_query = self.request.GET.get('search', '')
        if search_query:
            sprints = sprints.filter(name__icontains=search_query)
        return sprints

    def get(self, request, *args, **kwargs):
        p_id = int(request.GET.get('project-id', -2))
        if p_id == -2:
            request.user.set_last_visited_project(self.project)
            return super().get(request, *args, **kwargs)
        elif p_id == -1:
            return redirect('project-list')
        else:
            return redirect(reverse('sprint-list', args=[p_id]))


class SprintDetail(SprintMixin, DetailView):
    """ Scrum Board """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('search', '')
        status_to_tasks = {}
        for status in TaskStatus:
            tasks = Task.objects.filter(sprint=self.object, status=status)
            if search_query:
                tasks = tasks.filter(name__icontains=search_query)
            key = status.name.replace('_', ' ').title()
            status_to_tasks[key] = tasks
        context['status_to_tasks'] = status_to_tasks
        self.request.session['previous_page'] = self.request.path
        return context


class SprintCreate(SprintFormMixin, CreateView):
    pass


class SprintUpdate(SprintFormMixin, UpdateView):
    pass


class SprintDelete(SprintMixin, DeleteView):

    def post(self, request, *args, **kwargs):
        """ Prevents non admins from deleting a sprint. """
        if not request.user.is_staff:
            return render(request, 'forbidden.html', status=403)
        return super().post(request, *args, **kwargs)
