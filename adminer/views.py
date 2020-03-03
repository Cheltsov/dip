from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from client.models import Client, Log
from client.forms import ClientForm
from document.models import Doc
from document.forms import DocAdminForm
from .forms import AdminerForm
from .models import Adminer

def home(request):
    if 'admin' in request.session:
        content = {
            "client": 1
        }
        return render(request, 'adminer/index.html', content)
    else:
        return redirect('auth:auth')

def settings(request):
    if 'admin' in request.session:
        instance = get_object_or_404(Adminer, id=1)
        form_set = AdminerForm(request.POST or None, instance=instance)
        print(form_set)
        if request.method == "POST":
            set_admin = AdminerForm(request.POST, instance=instance)
            if set_admin.is_valid():
                set_admin.save()
                return redirect('adminer:home')
            else:
                return HttpResponse("ER")
        content = {
            'form': form_set
        }
        return render(request, 'adminer/setting.html', content)
    else:
        return redirect('auth:auth')

def client(request):
    if 'admin' in request.session:
        clients = Client.objects.all()
        content = {
            "clients": clients
        }
        return render(request, 'adminer/client.html', content)
    else:
        return redirect('auth:auth')

def client_add(request):
    if 'admin' in request.session:
        form = ClientForm(request.POST or None)
        content = {
            'form_client': form
        }
        return render(request, 'client/create.html', content)
    else:
        return redirect('auth:auth')

def client_edit(request, id):
    if 'admin' in request.session:
        instance = get_object_or_404(Client, id=id)
        form = ClientForm(request.POST or None, instance=instance)
        content = {
            'form_client': form,
            'id_cl': id,
        }
        return render(request, 'client/edit.html', content)
    else:
        return redirect('auth:auth')

def client_del(request, id):
    if 'admin' in request.session:
        Client.objects.get(pk=id).delete()
        return redirect("adminer:client")
    else:
        return redirect('auth:auth')

def document(request):
    if 'admin' in request.session:
        documents = Doc.objects.all()
        content = {
            "documents": documents,
        }
        return render(request, 'adminer/document.html', content)
    else:
        return redirect('auth:auth')

def document_add(request):
    if 'admin' in request.session:
        form = DocAdminForm(request.POST or None)
        content = {
            'base': 'adminer/base.html',
            'form_client': form,
            "admin": 1
        }
        return render(request, 'document/create.html', content)
    else:
        return redirect('auth:auth')

def document_edit(request, id):
    if 'admin' in request.session:
        instance = get_object_or_404(Doc, id=id)
        form = DocAdminForm(request.POST or None, instance=instance)
        content = {
            'base': 'adminer/base.html',
            'form_client': form,
            'id_doc': id,
            'admin': 1
        }
        return render(request, 'document/edit.html', content)
    else:
        return redirect('auth:auth')

def document_del(request, id):
    if 'admin' in request.session:
        Doc.objects.get(pk=id).delete()
        return redirect("adminer:document")
    else:
        return redirect('auth:auth')

def exit(request):
    if 'admin' in request.session:
        del request.session['token']
        del request.session['admin']
        return redirect('auth:auth')
    else:
        return redirect('auth:auth')

def log(request):
    if 'admin' in request.session:
        content = {
            'log_client': Log.objects.all().order_by('-date_created')
        }
        return render(request, 'adminer/log.html', content)
    else:
        return redirect('auth:auth')

def log_del(request, id):
    if 'admin' in request.session:
        Log.objects.get(pk=id).delete()
        return redirect('adminer:log')
    else:
        return redirect('auth:auth')
