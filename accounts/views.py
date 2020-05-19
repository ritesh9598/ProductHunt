from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from clarifai.rest import ClarifaiApp
import climage



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

def search(request):
    if request.method=='POST':
        add=request.POST['submit']
        context ={
          'add':add,
          }
        return render(request,'accounts/search.html',context)

    else:
        return render(request,'accounts/search.html')


def facedetect(request):
    if request.method=='POST':
        add=request.POST['submit']
        app = ClarifaiApp()
        model = app.models.get("a403429f2ddf4b49b307e318f00e528b")
        response = model.predict_by_url('add')
        clarifaiFace = response['outputs'][0]['data']['regions'][0]['region_info']['bounding_box']
        height,width=300,500
        box={
            'leftCol':clarifaiFace['left_col'] * width,
            'topRow':clarifaiFace['top_row'] * height,
            'rightCol': width - (clarifaiFace['right_col'] * width),
            'bottomRow':height - (clarifaiFace['bottom_row'] * height)
        }
        return render(request,'accounts/search.html',box)





'''
app = ClarifaiApp()
model = app.models.get("afe83148de574efbbfa485db27dfcdfe")
image = ClImage(url='https://samples.clarifai.com/face-det.jpg')
model.predict([image])
concepts = response['outputs'][0]['data']['concepts']
for concept in concepts:
    print(concept['name'], concept['value']
)'''


'''
app = ClarifaiApp()
model = app.models.get("a403429f2ddf4b49b307e318f00e528b")
response = model.predict_by_url('https://samples.clarifai.com/face-det.jpg')
clarifaiFace = response['outputs'][0]['data']['regions'][0]['region_info']['bounding_box']
width = int(image.width)
height =int(image.height)

leftCol=clarifaiFace['left_col'] * width,
topRow=clarifaiFace['top_row'] * height,
rightCol= width - (clarifaiFace['right_col'] * width),
bottomRow=height - (clarifaiFace['bottom_row'] * height)
print(leftCol)'''
