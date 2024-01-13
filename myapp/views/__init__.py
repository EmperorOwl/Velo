from .auth import *
from .member import *
from .project import *
from .sprint import *
from .task import *
from .user import *

__all__ = (
    'home', 'settings',
    'Login', 'Logout',
    'MemberList', 'MemberCreate', 'MemberDelete',
    'ProjectList', 'ProjectCreate', 'ProjectDetail', 'ProjectUpdate', 'ProjectDelete',
    'SprintList', 'SprintCreate', 'SprintUpdate', 'SprintDelete',
    'TaskList', 'TaskCreate', 'TaskUpdate', 'TaskDelete',
    'UserList', 'UserCreate', 'UserUpdate'
)


def home(request):
    current_user: User = request.user
    # If user is logged, then redirect them.
    if current_user.is_authenticated:
        if current_user.last_visited_project:
            return redirect(reverse('project-detail',
                                    kwargs={'p_id': current_user.last_visited_project.id}))
        return redirect(reverse('project-list'))
    # Otherwise show home page.
    return render(request, 'home.html')


def settings(request):
    return render(request, 'settings.html')
