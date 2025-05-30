
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.http import HttpResponse

from . filters import StudentFilter
from .forms import StudentSearchForm, StudentForm
from . models import Student

class StudentListView(LoginRequiredMixin, FilterView):
    model = Student
    template_name = 'home.html'
    context_object_name = 'students'
    filterset_class = StudentFilter
    paginate_by = 2

    def get_queryset(self):
        self.filterset = self.filterset_class(self.request.GET, queryset=super().get_queryset())
        return self.filterset.qs.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter_params = self.request.GET.copy()
        filter_params.pop('page', None)

        context['filter'] = self.filterset
        context['filter_params'] = filter_params
        context['helper_search_form'] = StudentSearchForm(self.request.GET)
        return context

class GetCreateStudentsView(LoginRequiredMixin, View):
    def get(self, request):
        student_form = StudentForm
        return render(request, 'helper_create_update_form.html', {
            'student_form': student_form
        })

    def post(self, request):
        student_form = StudentForm(request.POST)
        if student_form.is_valid():
            name = student_form.cleaned_data['name']
            subject = student_form.cleaned_data['subject']
            marks = student_form.cleaned_data['marks']

            # Try to get existing object (case-insensitive)
            student_qs = Student.objects.filter(name__iexact=name, subject__iexact=subject)

            if student_qs.exists():
                student = student_qs.first()
                student.marks = int(student_qs.first().marks) + marks
                student.created_by = request.user
                student.save()
                messages.success(request, f"Student record updated for {student.name} in {student.subject}.")
            else:
                # Create new if not exists
                student = student_form.save(commit=False)
                student.created_by = request.user
                student.save()
                messages.success(request, f"New student record created for {student.name} in {student.subject}.")

            return redirect('home')

        return render(request, 'helper_create_update_form.html', {
            'student_form': student_form
        })
class UpdateStudentsView(LoginRequiredMixin, View):
    def get(self, request, pk, action):
        student = Student.objects.get(pk=pk)
        if student and action == 'delete':
            student.delete()
            messages.warning(request, 'Student Details Deleted Successfully')
            return redirect('home')
        else:
            student_form = StudentForm(instance=student)
            return render(request, 'helper_create_update_form.html', {
                'student_form': student_form
            })

    def post(self, request, pk, action):
        student = Student.objects.get(pk=pk)
        student_form = StudentForm(self.request.POST, instance=student)
        if student_form.is_valid():
            student = student_form.save(commit=False)
            student.created_by = request.user
            student.save()
            messages.success(request, f"Student record {student.name} updated in {student.subject}.")
            return redirect('home')
        return render(request, 'helper_create_update_form.html',{
            'student_form': student_form
        })