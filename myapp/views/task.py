from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import ContextMixin, FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, reverse, redirect, resolve_url
from django.forms import inlineformset_factory

from ..models import Project, Task, Assignee
from ..utils import process_form_for_display


# MIXINS ----------------------------------------------------------------------

class TaskMixin(LoginRequiredMixin, ContextMixin):
    model = Task
    pk_url_kwarg = 't_id'
    request = None
    kwargs = None
    project = None

    def dispatch(self, request, *args, **kwargs):
        """ Initialises the project attribute. """
        self.project = get_object_or_404(Project, id=self.kwargs['p_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        """ Returns the URL to go to after creating/editing/deleting. """
        if 'previous_page' in self.request.session:
            return resolve_url(self.request.session['previous_page'])
        return reverse('task-list', args=[self.project.id])

    def get_context_data(self, **kwargs):
        """ Appends the Project instance to the context. """
        context = super().get_context_data(**kwargs)
        context['project'] = self.project
        return context


AssigneeFormset = inlineformset_factory(Task, Assignee,
                                        fields=['user', 'hours_worked'],
                                        extra=1)


class TaskFormMixin(TaskMixin, FormMixin):
    fields = '__all__'
    object = None

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields.pop('assignees')
        # Dropdown should only show sprints in this project.
        form.fields['sprint'].queryset = self.project.sprints
        return process_form_for_display(form, user=self.request.user)

    def form_valid(self, form):
        self.object = form.save()
        formset = AssigneeFormset(self.request.POST, instance=self.object)
        if formset.is_valid():
            formset.save()
        else:
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """ Adds the assignee formset to the context. """
        context = super().get_context_data(**kwargs)
        formset = AssigneeFormset(instance=self.object)
        for form in formset:
            # Dropdown should only show users in this project
            form.fields['user'].queryset = self.project.team
            # Remove labels from all fields
            for field in form.fields.values():
                field.label = ""
        context['formset'] = formset
        return context


# VIEWS -----------------------------------------------------------------------

class TaskList(TaskMixin, ListView):
    context_object_name = 'tasks'

    def get_queryset(self):
        """ Returns this project's Tasks. """
        tasks = Task.objects.filter(sprint__in=self.project.sprints.all())
        tasks = tasks.order_by('-due_date')
        search_query = self.request.GET.get('search', '')
        if search_query:
            tasks = tasks.filter(name__icontains=search_query)
        return tasks

    def get(self, request, *args, **kwargs):
        p_id = int(request.GET.get('project-id', -2))
        self.request.session['previous_page'] = self.request.path
        if p_id == -2:
            request.user.set_last_visited_project(self.project)
            return super().get(request, *args, **kwargs)
        elif p_id == -1:
            return redirect('project-list')
        else:
            return redirect(reverse('task-list', args=[p_id]))


class TaskCreate(TaskFormMixin, CreateView):
    pass


class TaskUpdate(TaskFormMixin, UpdateView):
    pass


class TaskDelete(TaskMixin, DeleteView):

    def post(self, request, *args, **kwargs):
        """ Prevents non guests from deleting a task. """
        if not request.user.is_staff:
            return render(request, 'forbidden.html', status=403)
        return super().post(request, *args, **kwargs)
