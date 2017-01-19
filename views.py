from django.shortcuts import render, get_object_or_404, redirect, render_to_response, reverse
from rip_app.models import OfficesModel, MembersModel
from django.views.generic import TemplateView, DetailView, ListView
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from rip_app.forms import LoginForm, SignupForm, OfficeForm, MemberForm, CreateForm, Create
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




class OfficesListView(ListView):
    template_name = 'include/office.html'
    model = OfficesModel
    context_object_name = 'Offices'
    paginate_by = 10


class Offices(OfficesListView):
    template_name = 'index.html'



class OneOffice(DetailView):
    template_name = 'include/one_office.html'
    model = OfficesModel
    context_object_name = 'Offices'

    def get_object(self):
        object = super(OneOffice, self).get_object()
        if not self.request.user.is_authenticated():
            raise Http404
        return object

    def get_members(request, office_id):
        members = get_object_or_404(MembersModel, pk=office_id)
        return render(request,'/office/' + str(office_id)+'/', {'members': members})



def index(request):
    return render(request, 'index.html')


def login(request):
    redirect_to = request.GET.get('next')
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            auth.login(request, form.cleaned_data['user'])
            if redirect_to:
                return redirect(redirect_to)
            return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            u = form.save()
            auth.login(request, u)
            return redirect('/')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def logout(request):
    redirect_to = request.GET.get('next')
    auth.logout(request)
    if redirect_to:
        return redirect(redirect_to)
    return redirect('/')

'''
def office_new(request):
    if request.method == 'POST':
        form = CreateForm(request.POST, request.FILES)
        if form.is_valid():
            office = OfficesModel()
            office.named = request.POST.get('Название')
            office.location = request.POST.get('Адрес')
            office.picture = request.FILES.get('Логотип')
            office.save()
            return redirect('Offices')
    else:
        form = CreateForm()
    return render(request, 'newOffice.html', {'form': form})
'''

def office_new(request):
    if request.method == 'POST':
        form = Create(request.POST, request.FILES)
        if form.is_valid():
            office = form.save()
            return HttpResponseRedirect('/office/' + str(office.pk)+'/')

    else:
        form = Create()
    return render(request, 'newOffice.html', {'form': form})


def member_new(request):
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=True)
            post.save()
            return redirect('Offices')
    else:
        form = MemberForm()
    return render(request, 'new_member.html', {'form': form})


def sub(request):
    member = request.user.member
    office = OfficesModel.objects.get(pk=request.POST.get("id"))
    office.members.add(member)
    return redirect('/office/' + str(office.pk)+'/')

#def sub(request):
 #   luser = request.user.id
 #   course = Course.objects.get(pk=request.POST.get("id"))
 #   course.lusers.add(luser)
 #   return redirect('/')