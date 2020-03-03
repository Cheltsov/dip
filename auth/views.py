from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import AuthForm
from adminer.models import Adminer
from client.models import Client, Log

# Create your views here.
def auth(request):
    form = AuthForm()
    content = {
        'form': form
    }
    if request.method == 'POST':

        email = request.POST['email']
        password = request.POST['password']
        admin = Adminer(email=email, password=password)
        client = Client(email=email, password=password)

        if admin.check_admin():
            request.session['token'] = 'admin'
            request.session['admin'] = 'admin'
            return redirect('adminer:home')
        elif client.check_client():
            request.session['token'] = 'client'
            id_client = client.check_client()
            request.session['id_client'] = id_client
            Log.objects.create(id_client=Client(id=id_client), action=1)
            return redirect('client:index')
        else:
            content['error'] = "Такого пользователя нет"

    return render(request, 'auth/auth.html', content)

