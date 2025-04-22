from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, loginforms, otp_form
from django.contrib import messages
import random
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .models import OTP, customuser, SustainabilityScore  # Added SustainabilityScore model
from .models import Community
import pandas as pd
import pickle
import os
from django.conf import settings
import pandas as pd
import numpy as np
import joblib
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SustainabilityScore  
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Get the full path to the accounts directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = settings.BASE_DIR 

# # Load the model and scaler using correct paths
# model = load_model(os.path.join(BASE_DIR, "sustainability_model.h5"))
# scaler = joblib.load(os.path.join(BASE_DIR, "scaler.pkl"))

# Load your dataset
dataset = pd.read_csv('ecostat_sample_dataset.csv')

# Redirect "Get Started" to login page
def home(request):
    return render(request, "home.html")

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            authenticated_user = authenticate(
                request, username=form.cleaned_data['username'], password=form.cleaned_data['password1']
            )
            if authenticated_user:
                login(request, authenticated_user)
                return redirect("dashboard")  # Redirect to dashboard after signup
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})

def login_view(request):
    if request.method == 'POST':
        form = loginforms(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                otp = generate_otp()
                OTP.objects.create(user=user, otp_code=otp)
                send_otp(user, otp)
                request.session['user_id'] = user.id
                return redirect('verify_otp')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = loginforms()
    
    return render(request, 'accounts/login.html', {'forms': form})

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp(user, otp):
    subject = "Ecostat Login OTP"
    message = f"Your OTP is {otp}. Do not share it with anyone."
    send_mail(subject, message, 'ecostat005@gmail.com', [user.email])

def verify_otp(request):
    if request.method == 'POST':
        otp_code = request.POST.get('otp_code')
        user_id = request.session.get('user_id')

        if user_id:
            try:
                user = customuser.objects.get(id=user_id)
                otp_entry = OTP.objects.filter(user=user).latest('created_at')

                if otp_entry.otp_code == otp_code:
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    messages.success(request, "Login successful")
                    return redirect('dashboard')  # Redirect to dashboard
                else:
                    messages.error(request, "Invalid OTP")
            except OTP.DoesNotExist:
                messages.error(request, "OTP not found for this user.")
        
    return render(request, 'accounts/verify_otp.html')

@login_required
def dashboard(request):
    # Fetch latest sustainability score
    score_entry = SustainabilityScore.objects.order_by('-id').first()
    
    # Default value if no score is available
    score = score_entry.score if score_entry else 0  

    return render(request, 'dashboard.html', {'user': request.user, 'score': score})

def logout_page(request):
    logout(request)
    return redirect('home')

def about(request):
    return render(request, 'about.html')
from django.http import JsonResponse

def sustainability_score(request):
    # data = {"score": 8.5}  # Example static data
    return render(request, 'sustainability_calculator.html')
from django.shortcuts import render



def profile(request):
    return render(request, 'accounts/profile.html')
from django.shortcuts import render

def community_insights(request):
    communities = Community.objects.all()  # ✅ Model name starts with capital C
    return render(request, 'accounts/community_insights.html', {'communities': communities})



from django.shortcuts import render

# def sustainability_calculator(request):
#     return render(request, 'sustainability_calculator.html')

# def sustainability_calculator(request):
#     prediction = None 
#     if request.method == "POST":
#         try:
#             energy_usage = float(request.POST.get('energy_usage'))
#             pollution_level = float(request.POST.get('pollution_level'))
#             recycling_rate = float(request.POST.get('recycling_rate'))
#             green_cover = float(request.POST.get('green_cover'))
#             rainwater_harvesting = int(request.POST.get('rainwater_harvesting'))  # 0 or 1

#             #input_data = np.array([[energy_usage, pollution_level, recycling_rate, green_cover, rainwater_harvesting]])
#             input_data = np.array([[3500, 70, 7000, 3000, 4000]])

#             # Load trained RandomForest model (.pkl)
#             model = joblib.load(os.path.join(BASE_DIR, "sustainability_model.pkl"))

#             score = model.predict(input_data)[0]
#             prediction = round(score, 2)
#             SustainabilityScore.objects.create(score=prediction)

#         except ValueError:
#             messages.error(request, "Invalid input. Please make sure all fields contain valid numbers.")
#             return render(request, 'sustainability_calculator.html')

#     return render(request, 'sustainability_calculator.html', {'prediction': prediction})


# def sustainability_calculator(request):
#     print(request.method)
#     if request.method == "POST":
#         try:
#             energy_usage = float(request.POST.get('energy_usage'))
#             pollution_level = float(request.POST.get('pollution_level'))
#             recycling_rate = float(request.POST.get('recycling_rate'))
#             green_cover = float(request.POST.get('green_cover'))
#             water_conservation = int(request.POST.get('water_conservation'))

#             print("Input values:", energy_usage, pollution_level, recycling_rate, green_cover, water_conservation)

#             input_data = np.array([[energy_usage, pollution_level, recycling_rate, green_cover, water_conservation]])

#             # Optional: Load and apply scaler if used
#             # scaler_path = os.path.join(BASE_DIR, 'accounts', 'ml_model', 'scaler.pkl')
#             # scaler = joblib.load(scaler_path)
#             # input_data = scaler.transform(input_data)

#             model_path = os.path.join(BASE_DIR, 'ml_model', 'sustainability_model.pkl')
#             model = joblib.load(model_path)

#             score = model.predict(input_data)[0]
#             prediction = round(score, 2)

#             print("Predicted score:", prediction)

#             # Save to DB
#             SustainabilityScore.objects.create(score=prediction)

#             return JsonResponse({
#                 'success': True,
#                 'sustainability_score': prediction
#             })

#         except Exception as e:
#             return JsonResponse({'success': False, 'error': str(e)})

#     return JsonResponse({'success': False, 'error': 'Only POST method allowed'})

@csrf_exempt
def sustainability_calculator(request):
    if request.method == "POST":
        try:
            energy_usage = float(request.POST.get('energy_usage'))
            pollution_level = float(request.POST.get('pollution_level'))
            recycling_rate = float(request.POST.get('recycling_rate'))
            green_cover = float(request.POST.get('green_cover'))
            water_conservation = float(request.POST.get('water_conservation'))

            input_data = np.array([[energy_usage, pollution_level, recycling_rate, green_cover, water_conservation]])

            model_path = os.path.join(BASE_DIR, 'accounts', 'ml_model', 'sustainability_model.pkl')
            model = joblib.load(model_path)

            score = model.predict(input_data)[0]
            prediction = round(score, 2)

            SustainabilityScore.objects.create(score=prediction)

            return JsonResponse({'success': True, 'prediction': prediction})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Only POST method allowed'})


def community_insights_all(request):
    communities = Community.objects.all()
    return render(request, 'community_insights.html', {'communities': communities})

def community_insights_detail(request, community):
    communities = Community.objects.filter(community_name=community)
    return render(request, 'community_insights.html', {'communities': communities})