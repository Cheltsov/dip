from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from client.models import Client, Log
from client.forms import ClientForm
from document.models import Doc
from document.forms import DocClientForm
from dip.settings import MEDIA_FACE, MEDIA_ROOT
from django.core.files.storage import FileSystemStorage
import json, base64, datetime
from cypher.views import get_evklid
from django.core.files.base import ContentFile
from django.core.serializers.json import DjangoJSONEncoder
import os
import shutil

# Create your views here.
def index(request):
    if 'id_client' in request.session:
        id_client = request.session['id_client']
        client = Client.get_client_id(id_client)
        if client.status == 1:
            return render(request, 'client/check_face.html', {})
        else:
            return redirect('client:home')
    else:
        return redirect("auth:auth")


def home(request):
    if 'id_client' in request.session:
        id_client = request.session['id_client']
        client = Client.get_client_id(id_client)
        last_time = Log.objects.filter(id_client=Client(id=id_client)).order_by('-date_created')[0]
        print(last_time)
        content = {
            "client": client,
            "last_time": last_time
        }
        return render(request, 'client/index.html', content)
    else:
        return redirect('auth:auth')

def document(request):
    if 'id_client' in request.session:
        id_client = request.session['id_client']
        documents = Doc.objects.filter(client_id=id_client)
        print(documents)
        content = {
            "documents": documents
        }
        return render(request, 'client/document.html', content)
    else:
        return redirect('auth:auth')

def document_add(request):
    if 'id_client' in request.session:
        id_client = request.session['id_client']
        form = DocClientForm(request.POST or None, initial={'client': id_client})
        content = {
            'id_client': id_client,
            'base': 'client/base.html',
            'form_client': form
        }
        return render(request, 'document/create.html', content)
    else:
        return redirect('auth:auth')

def document_edit(request, id):
    if 'id_client' in request.session:
        id_client = request.session['id_client']
        instance = get_object_or_404(Doc, id=id)
        form = DocClientForm(request.POST or None, instance=instance, initial={'client': id_client})
        content = {
            'id_client': id_client,
            'base': 'client/base.html',
            'form_client': form,
            'id_doc': id
        }
        return render(request, 'document/edit.html', content)
    else:
        return redirect('auth:auth')

def document_del(request, id):
    if 'id_client' in request.session:
        Doc.objects.get(pk=id).delete()
        Log.objects.create(id_client=Client(id=request.session['id_client']), action=5)
        return redirect("client:document")
    else:
        return redirect('auth:auth')

def check_face(request):
    if request.method == 'POST':
        data = request.POST.get('img', False)
        if data:
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            data = ContentFile(base64.b64decode(imgstr), name='photo_new_' + now + '.' + ext)
            photo_new = uploaded_file(data)
            if 'id_client' in request.session:
                id_client = request.session['id_client']
                client = Client.objects.get(id=id_client)
                if client.photo:
                    photo_old = client.photo.path
                    num_evd_res = get_evklid(photo_old, photo_new)
                    if num_evd_res < 0.55:
                        Log.objects.create(id_client=Client(id=request.session['id_client']), action=10,
                                           photo="face/00_"+os.path.basename(photo_new))
                        return HttpResponse("ok")
                    else:
                        return HttpResponse("Вы не прошли автризацию. <a href='/client/'>Назад</a>")
                else:
                    return redirect('client:home')
        else:
            return HttpResponse("Error data img")
    else:
        payload = {'success': False}
        return HttpResponse(json.dumps(payload), content_type='application/json')

def uploaded_file(myfile):
    fs = FileSystemStorage(location=MEDIA_FACE)
    filename = fs.save(myfile.name, myfile)
    uploaded_file_url = fs.path(filename)
    print(uploaded_file_url)
    shutil.copyfile(uploaded_file_url, MEDIA_FACE+'/00_'+filename)
    return uploaded_file_url

def exit(request):
    if 'id_client' in request.session:
        Log.objects.create(id_client=Client(id=request.session['id_client']), action=2)
        del request.session['token']
        del request.session['id_client']
        return redirect('auth:auth')
    else:
        return redirect('auth:auth')

def add_client(request):
    if request.method == 'POST':
        cl_form = ClientForm(request.POST, request.FILES)
        if cl_form.is_valid():
            tmp = cl_form.save()
            Log.objects.create(id_client=Client(id=tmp.id), action=9)
            return redirect("adminer:client")
        else:
            return HttpResponse('Ошибка')
    else:
        return redirect("adminer:client_add")

def edit_client(request, id):
    if request.method == 'POST':
        instance = Client.objects.get(id=id)
        cl_form = ClientForm(request.POST, request.FILES, instance=instance)
        if cl_form.is_valid():
            cl_form.save()
            return redirect("adminer:client")
        else:
            return HttpResponse('Ошибка')
    else:
        return redirect("adminer:client_edit")

def search(request):
    if request.method == 'POST':
        fio = request.POST['fio']
        obj = Client.objects.filter(fio__contains=fio, active=1).values('id', 'fio', 'email', 'active', 'status')
        for item in obj:
            item['active'] = "Да" if item['active'] else "Нет"
            item['status'] = "Да" if item['status'] else "Нет"
        prices_json = json.dumps(list(obj), cls=DjangoJSONEncoder)
        print(prices_json)
        return HttpResponse(prices_json, content_type='application/json')
