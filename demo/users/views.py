from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User
from .models import Fact
from django.contrib.auth.hashers import make_password, check_password
from cryptography.fernet import Fernet
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

# Create your views here.
def home(request):
    if 'user' in request.session:
        current_user = request.session['user']
        param = {'current_user': current_user}
        queryset = Fact.objects.all()
        context = {
            "object_list": queryset,
            "current_user": current_user
        }
        return render(request, 'users/base.html',context)
    else:
        queryset = Fact.objects.all()
        context = {
            "object_list": queryset
        }
        return render(request, 'users/base.html',context)

def signup(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        password = make_password(request.POST.get('pwd'))
        fernet = Fernet(settings.KEY)
        encPassword = fernet.encrypt(password.encode())
        # print(uname, pwd)
        if User.objects.filter(username=uname).count()>0:
            messages.info(request, 'Username already exists.')
            return redirect('signup')
        else:
            user = User(username=uname, password=password)
            user.save()
            return redirect('login')
    else:
        return render(request, 'users/signup.html')



def login(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        password = request.POST.get('pwd') 
        fernet = Fernet(settings.KEY)


        try:
            uid = User.objects.get(username=uname)
            decPassword = check_password(request.POST.get('pwd'),uid.password)
            print(decPassword)

            if decPassword:
                    request.session['user'] = uname
                    return redirect('home')
            else:
                messages.info(request,'Password does not match.')
                return redirect('login')
        except ObjectDoesNotExist:
                messages.info(request,'User does not exitst')
                return redirect('login')


    return render(request, 'users/login.html')


def logout(request):
    try:
        del request.session['user']
    except:
        return redirect('login')
    return redirect('login')

def add(request):

    if 'user' in request.session:
        if request.method == 'POST':
            current_user = request.session['user']
            param = User.objects.get(username=current_user)   
            if request.POST.get('blog'):
                blog=Fact()
                blog.fact= request.POST.get('blog')
                blog.user_id_id= param.id
                blog.save()            
                return redirect('home') 
        else:

            return render(request,'users/add.html')
    else:
        return redirect('login')

def like_category(request):

    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']

    likes = 0
    if cat_id:
        cat = Fact.objects.get(id=int(cat_id))
        if cat:
            if cat.like:
                likes = cat.like + 1
                cat.like =  likes
                cat.save()
            else:
                likes = likes + 1
                cat.like =  likes
                cat.save()

    return HttpResponse(likes)