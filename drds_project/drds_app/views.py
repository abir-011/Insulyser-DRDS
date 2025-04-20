from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from .utils import predict_class, print_patient_vitals
import os
from .utils import predict_class, print_patient_vitals, get_gemini_assessment

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


def wait_view(request):
    final_class = request.session.get('final_class')

    output_map = {
        "Mild": "output1.html",
        "Moderate": "output2.html",
        "No_DR": "output3.html",
        "Proliferate_DR": "output4.html",
        "Severe": "output5.html",
        None: "output6.html"
    }
    return render(request, output_map.get(final_class, "output6.html"))


def logout_view(request):
    global is_logged_in
    is_logged_in = False
    return redirect('login')

def about_view(request):
    return render(request, 'about.html') if is_logged_in else render(request, 'about1.html')

def contact_view(request):
    return render(request, 'contact.html') if is_logged_in else render(request, 'contact1.html')

def upload_view(request):
    if request.method == 'POST' and request.FILES.get('image'):
        # Extract form data
        hba1c = request.POST.get('hba1c')
        blood_pressure = request.POST.get('blood_pressure')
        duration = request.POST.get('duration')
        serum_creatinine = request.POST.get('serum_creatinine')
        lipid_profile = request.POST.get('lipid_profile')
        img = request.FILES['image']

        # Save uploaded image
        path = os.path.join(UPLOAD_PATH, 'input.png')
        with open(path, 'wb+') as dest:
            for chunk in img.chunks():
                dest.write(chunk)

        # Predict using image model
        predicted_class = predict_class(path)

        # Get severity and final class from Gemini
        gemini_data = get_gemini_assessment(hba1c, blood_pressure, duration, serum_creatinine, lipid_profile, predicted_class)
        severity_score = gemini_data.get('severity_score')
        final_class = gemini_data.get('final_class')
        reason = gemini_data.get('reason')

        # Store everything in session
        request.session['hba1c'] = hba1c
        request.session['blood_pressure'] = blood_pressure
        request.session['duration'] = duration
        request.session['serum_creatinine'] = serum_creatinine
        request.session['lipid_profile'] = lipid_profile
        request.session['predicted_class'] = predicted_class
        request.session['severity_score'] = severity_score
        request.session['final_class'] = final_class
        request.session['reason'] = reason

        # Log
        print_patient_vitals(hba1c, blood_pressure, duration, serum_creatinine, lipid_profile, predicted_class, {
            "severity_score": severity_score,
            "reason": reason
        })
        print("Final DR Class:", final_class)

        return redirect('wait')
    return render(request, 'home.html')