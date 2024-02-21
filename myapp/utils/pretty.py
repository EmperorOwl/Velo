from django.forms import DateTimeInput, CheckboxSelectMultiple
from django.utils import timezone as tmz


def pretty_form(form, user):
    # Update some fields.
    for field_name, field in form.fields.items():
        # User should only be able to assign a task to a team member
        # in that project.
        if field_name == 'assignees':
            field.queryset = user.last_visited_project.team.all()
        if field_name in ['team', 'tags', 'assignees']:
            field.widget = CheckboxSelectMultiple(choices=field.choices)
        if 'date' in field_name:
            field.widget = DateTimeInput(attrs={'type': 'datetime-local'})
    # Set all fields to read-only if user is a guest.
    if user.is_guest:
        for field in form.fields.values():
            field.widget.attrs['disabled'] = True
    return form


def pretty_hour(t: float):
    """ Converts 2.1 to 2.1 hours or 1.0 to 1 hour """
    if not t:
        return ''
    return str(t).replace('.0', '') + ' hour' + ('s' if t != 1 else '')


def pretty_date(d):
    """ Converts datetime to day and month and year if different year. """
    if not d:
        return ''
    return d.strftime('%b %d' + (', %Y' if d.year != tmz.now().year else ''))
