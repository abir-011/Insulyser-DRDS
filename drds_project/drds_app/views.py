from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from .utils import predict_class
import os

is_logged_in = False

# Use Django's media directory
UPLOAD_PATH = settings.MEDIA_ROOT
os.makedirs(UPLOAD_PATH, exist_ok=True)

def login_view(request):
    global is_logged_in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username == 'Insulyser' and password == 'Admin':
            is_logged_in = True
            return redirect('welcome')
        else:
            return render(request, 'login.html', {'message': 'Invalid credentials'})
    return render(request, 'login.html')

def welcome_view(request):
    return render(request, 'welcome.html') if is_logged_in else HttpResponse("Unauthorized", status=401)

def home_view(request):
    return render(request, 'home.html')

def upload_view(request):
    if request.method == 'POST' and request.FILES.get('image'):
        img = request.FILES['image']
        path = os.path.join(UPLOAD_PATH, 'input.png')
        with open(path, 'wb+') as dest:
            for chunk in img.chunks():
                dest.write(chunk)
        return redirect('wait')
    return render(request, 'home.html')

def wait_view(request):
    image_path = os.path.join(UPLOAD_PATH, 'input.png')
    prediction = predict_class(image_path)
    output_map = {
        "Mild": "output1.html",
        "Moderate": "output2.html",
        "No_DR": "output3.html",
        "Proliferate_DR": "output4.html",
        "Severe": "output5.html",
        None: "output6.html"
    }
    return render(request, output_map.get(prediction, "output6.html"))

def logout_view(request):
    global is_logged_in
    is_logged_in = False
    return redirect('login')

def about_view(request):
    return render(request, 'about.html') if is_logged_in else render(request, 'about1.html')

def contact_view(request):
    return render(request, 'contact.html') if is_logged_in else render(request, 'contact1.html')
