from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import DocClientForm, DocAdminForm
from client.models import Client, Log
from .models import Doc
import json
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.
def create_doc(request):
    if request.method == 'POST':
        doc = Doc()
        if request.session['token'] == 'client':
            doc_form = DocClientForm(request.POST, request.FILES)
        else:
            doc_form = DocAdminForm(request.POST, request.FILES)

        print(doc_form)

        if doc_form.is_valid():
            doc_form.save(commit=False)
            doc.title = doc_form.cleaned_data['title']
            doc.file = doc_form.cleaned_data['file']
            doc.crypth = doc_form.cleaned_data['crypth']
            doc.client = Client.objects.get(id=request.POST['client'])
            doc.save()
            if request.session['token'] == 'client':
                Log.objects.create(id_client=Client(id=request.session['id_client']), action=3)
                return redirect("client:document")
            elif request.session['token'] == 'admin':
                return redirect("adminer:document")
            else:
                return HttpResponse("ERROR URL")
        else:
            return HttpResponse('Ошибка')
    else:
        if request.session['token'] == 'client':
            return redirect('client:document_add')
        elif request.session['token'] == 'admin':
            return redirect('adminer:document_add')
        else:
            return HttpResponse("ERROR URL")

def edit_doc(request, id):
    if request.method == 'POST':
        instance = Doc.objects.get(id=id)
        if request.session['token'] == 'client':
            doc_form = DocClientForm(request.POST, request.FILES, instance=instance)
        else:
            doc_form = DocAdminForm(request.POST, request.FILES, instance=instance)

        print(doc_form)
        if doc_form.is_valid():
            doc_form.save()
            if request.session['token'] == 'client':
                Log.objects.create(id_client=Client(id=request.session['id_client']), action=4)
                return redirect("client:document")
            elif request.session['token'] == 'admin':
                return redirect("adminer:document")
            else:
                return HttpResponse("ERROR URL")
        else:
            return HttpResponse('Ошибка')
    else:
        if request.session['token'] == 'client':
            return redirect('client:document_edit')
        elif request.session['token'] == 'admin':
            return redirect('adminer:document_edit')
        else:
            return HttpResponse("ERROR URL")

def get_decrypth(request):
    if request.method == 'POST':
        id = request.POST['id']
        instance = Doc.objects.filter(id=id).update(decrypth=1)
        Log.objects.create(id_client=Client(id=request.session['id_client']), action=6)
        print(instance)
        return HttpResponse(json.dumps('true'), content_type='application/json')
    else:
        return HttpResponse(json.dumps('false'), content_type='application/json')

def search(request):
    if request.method == 'POST':
        title = request.POST['title']
        id_client = request.session['id_client']
        obj = Doc.objects.filter(title__contains=title, client=id_client, active=1).values('id',
                                                                                           'title',
                                                                                           'crypth',
                                                                                           'decrypth',
                                                                                           'date_created',
                                                                                           'date_updated')
        for item in obj:
            item['display_crypth'] = Doc.CRYPTH_METHODS[int(item['crypth'])][1]
            item['date_created'] = item['date_created'].strftime("%d.%m.%Y %H:%M")
            item['date_updated'] = item['date_updated'].strftime("%d.%m.%Y %H:%M")
        obj.get_crypt = obj
        prices_json = json.dumps(list(obj), cls=DjangoJSONEncoder)
        print(prices_json)
        return HttpResponse(prices_json, content_type='application/json')

def search_admin(request):
    if request.method == 'POST':
        title = request.POST['title']
        obj = Doc.objects.filter(title__contains=title, active=1).values('id', 'title', 'crypth', 'decrypth',
                                                                         'date_created', 'date_updated', 'client')
        for item in obj:
            item['client'] = Client.objects.get(id=item['client']).fio
            item['display_crypth'] = Doc.CRYPTH_METHODS[int(item['crypth'])][1]
            item['date_created'] = item['date_created'].strftime("%d.%m.%Y %H:%M")
            item['date_updated'] = item['date_updated'].strftime("%d.%m.%Y %H:%M")
        obj.get_crypt = obj
        prices_json = json.dumps(list(obj), cls=DjangoJSONEncoder)
        print(prices_json)
        return HttpResponse(prices_json, content_type='application/json')