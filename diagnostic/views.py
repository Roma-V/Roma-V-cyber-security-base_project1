from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from diagnostic.forms import DiagnoseRecordForm
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.views.decorators.http import require_POST
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin  
from django.contrib.auth.models import User

from .models import Record, Diagnose
from .forms import DiagnoseRecordForm


# Create your views here.
def index(request):
    """View function for home page of the app"""

    # Generate counts of some of the main objects
    num_records = Record.objects.all().count()
    num_diagnoses = Diagnose.objects.all().count()

    # Available books (status = 'a')
    num_unresolver_records = Record.objects.filter(diagnose__isnull=True).count()

    context = {
        'num_diagmoses': num_diagnoses,
        'num_records': num_records,
        'num_unresolver_records': num_unresolver_records,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class RecordListView(LoginRequiredMixin, generic.ListView):
    model = Record

    def get_context_data(self, **kwargs):
        '''
        Restrict full list to Doctors and Patients are 
        allowed to see only their own records.
        '''

        # Doctors
        if self.request.user.groups.filter(name='Doctors').exists():
            return super().get_context_data(**kwargs)
        #Patients
        else:
            context = super().get_context_data(**kwargs)
            context['object_list'] = Record.objects.filter(patient=self.request.user)
            context['record_list'] = Record.objects.filter(patient=self.request.user)
            return context

class RecordDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Record
    permission_required = 'diagnostic.view_record'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DiagnoseRecordForm()
        
        # An extension for restricted access to private data
        """
        if not self.request.user.groups.filter(name='Doctors').exists():
            context['object_list'] = Record.objects.filter(patient=self.request.user)
            context['record_list'] = Record.objects.filter(patient=self.request.user)
        """
        
        return context

class RecordCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Record
    fields = ['title', 'symptoms', 'patient']
    permission_required = 'diagnostic.add_record'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user)

        # Dissalow choosing patient for a non-doctor.
        if not user.has_perm('diagnostic.change_record'):
            print(context['form'].fields['patient'])
            del context['form'].fields['patient']

        return context
    
    def post(self, *args, **kwargs):
        data = args[0].POST
        patient = data.get('patient', default=False)
        if patient:
            patient = User.objects.get(pk=patient)
        else:
            patient = User.objects.get(username=self.request.user)

        new_record = Record(title=data['title'], symptoms=data['symptoms'], patient = patient)
        new_record.save()

        return HttpResponseRedirect( reverse('record-detail', args=[new_record.id]) )

@require_POST
def diagnose_record(request, pk):
    record = get_object_or_404(Record, pk=pk)

    # Create a form instance and populate it with data from the request (binding):
    form = DiagnoseRecordForm(request.POST)

    # Check if the form is valid:
    if form.is_valid():
        # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
        record.diagnose = form.cleaned_data['diagnose']
        record.save()

        # redirect to a new URL:
        return HttpResponseRedirect(reverse('records') )

    return HttpResponseRedirect( reverse('record-detail', args=[pk]) )

class DiagnoseListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Diagnose
    permission_required = 'diagnostic.view_diagnose'

class DiagnoseCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Diagnose
    fields = ['name']
    permission_required = 'diagnostic.add_diagnose'
