from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_default_objects(sender, **kwargs):
    from .models import Tag, User, Project, Sprint, Task
    from .choices import UserRole
    # Create default tags.
    tags = [
        'Frontend',
        'Backend',
        'API',
        'Database',
        'Framework',
        'Testing',
        'UI',
        'UX'
    ]
    for tag in tags:
        Tag.objects.get_or_create(name=tag)
    # Create admin user.
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin',
            first_name='Admin',
        )
    else:
        admin = User.objects.get(username='admin')
    # Create guest user.
    if not User.objects.filter(username='guest').exists():
        guest = User.objects.create_user(
            username='guest',
            email='guest@example.com',
            password='guest',
            first_name='Guest',
            role=UserRole.GUEST
        )
    else:
        guest = User.objects.get(username='guest')
    # Create default project, sprint and task.
    project, _ = Project.objects.get_or_create(name='Demo Project')
    project.team.add(admin, guest)
    project.save()
    sprint, _ = Sprint.objects.get_or_create(project=project, name='Test Sprint')
    task, _ = Task.objects.get_or_create(sprint=sprint, name='Test Task')


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        post_migrate.connect(create_default_objects, sender=self)
