from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . views import StudentListView, GetCreateStudentsView, UpdateStudentsView

urlpatterns = [
    path('', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('home/', StudentListView.as_view(), name='home'),
    path('create_students/', GetCreateStudentsView.as_view(), name='student-create'),
    path('update_or_delete_student/<int:pk>/<str:action>/', UpdateStudentsView.as_view(), name='student-update-delete'),
]
