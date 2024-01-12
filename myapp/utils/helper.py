from django.forms import DateTimeInput, CheckboxSelectMultiple


def process_form_for_display(form, user):
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
    # if user.is_guest():
    #     for field in form.fields.values():
    #         field.widget.attrs['disabled'] = True
    return form
