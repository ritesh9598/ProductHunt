from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from clarifai.rest import ClarifaiApp
from PIL import Image
from requests import get
from io import BytesIO
from django.contrib.auth.decorators import login_required



# Create your views here.

def signup(request):
    if request.method == 'POST':
        #user has info and wants accounts
        if request.POST['password1']== request.POST['password2']:
            try:
                user=User.objects.get(username=request.POST['username'])
                return render(request,'accounts/signup.html', {'error': 'Username is already taken'})

            except User.DoesNotExist:
                user=User.objects.create_user(request.POST['username'],request.POST['email'],request.POST['password1'])
                auth.login(request,user)
                return redirect('home')

        else:
            return render(request,'accounts/signup.html', {'error': 'Password mismatch'})
    else:
        #users have i'login enfo
        return render(request,'accounts/signup.html')


def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')

        else:
            return render(request, 'accounts/login.html',{'error':'username or password is incorrect.'})
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method=='POST':
        auth.logout(request)
        return redirect('home')

@login_required(login_url="/accounts/login")
def search(request):
    if request.method=='POST':
        add=request.POST['imgurl']
        app = ClarifaiApp()
        model = app.models.get("a403429f2ddf4b49b307e318f00e528b")
        response = model.predict_by_url(add)
        clarifaiFace = response['outputs'][0]['data']['regions']
        c=[]
        image_raw = get(add)
        image = Image.open(BytesIO(image_raw.content))
        width, height = image.size
        for i in clarifaiFace:
            c.append(i['region_info'][ "bounding_box"])
        d=[]
        e={}
        for j in c:
            e['left']=j['left_col']*width
            e['top']=j['top_row']*height
            e['right']=width-(j['right_col']*width)
            e['bottom']=height-(j['bottom_row']*height)
            e2=e.copy()
            d.append(e2)
            del(e2)
        FaceNumber=len(d)
        box={
            'add':add,
            'd':d,
            'FaceNumber':FaceNumber,
        }
        return render(request,'accounts/search.html',box)
    else:
        return render(request,'accounts/search.html')
