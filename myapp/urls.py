from django.urls import path

from .views import *

urls = [
    # Misc
    ('', home, 'home'),
    # User
    ('login', Login.as_view(), 'login'),
    ('demo', Login.as_view(guest_login=True), 'demo'),
    ('logout', Logout.as_view(), 'logout'),
    # Project
    ('projects', ProjectList.as_view(), 'project-list'),
    ('projects/create', ProjectCreate.as_view(), 'project-create'),
    ('projects/<int:p_id>/dashboard', ProjectDetail.as_view(), 'project-detail'),
    ('projects/<int:p_id>/update', ProjectUpdate.as_view(), 'project-update'),
    ('projects/<int:p_id>/delete', ProjectDelete.as_view(), 'project-delete'),
    # Sprint
    ('projects/<int:p_id>/sprints', SprintList.as_view(), 'sprint-list'),
    ('projects/<int:p_id>/sprints/create', SprintCreate.as_view(), 'sprint-create'),
    ('projects/<int:p_id>/sprints/<int:s_id>/update', SprintUpdate.as_view(), 'sprint-update'),
    ('projects/<int:p_id>/sprints/<int:s_id>/delete', SprintDelete.as_view(), 'sprint-delete'),
    # Task
    ('projects/<int:p_id>/tasks', TaskList.as_view(), 'task-list'),
    ('projects/<int:p_id>/tasks/create', TaskCreate.as_view(), 'task-create'),
    ('projects/<int:p_id>/tasks/<int:t_id>/update', TaskUpdate.as_view(), 'task-update'),
    ('projects/<int:p_id>/tasks/<int:t_id>/delete', TaskDelete.as_view(), 'task-delete'),
    # User
    ('projects/<int:p_id>/users/create', UserCreate.as_view(), 'user-create'),
    ('projects/<int:p_id>/users/<int:u_id>/update', UserUpdate.as_view(), 'user-update'),
    # Member
    ('projects/<int:p_id>/members', MemberList.as_view(), 'member-list'),
    ('projects/<int:p_id>/members/create', MemberCreate.as_view(), 'member-create'),
    ('projects/<int:p_id>/members/<int:m_id>/delete', MemberDelete.as_view(), 'member-delete'),
]

urlpatterns = [path(url[0], url[1], name=url[2]) for url in urls]
