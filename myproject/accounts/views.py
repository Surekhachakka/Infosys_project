from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import keras
from django.conf import settings
import numpy as np
from PIL import Image
import os
from .forms import RegistrationForm, LoginForm

# Load your trained models (update the path accordingly)
model1_path = r"C:\Users\venka\OneDrive\Desktop\Project\bi_rnn_signature_verification_model.h5"
model1 = keras.models.load_model(model1_path)

model2_path = r"C:\Users\venka\OneDrive\Desktop\Project\crnn_signature_verification_model.keras"
model2 = keras.models.load_model(model2_path)

# Define desired width and height for image input
your_desired_width = 128
your_desired_height = 128

def process_signature_model1(image_path):
    # Load and resize the image to match expected input shape
    display_image = Image.open(image_path).convert('RGB')
    display_image = display_image.resize((128, 128))  # Resize to (128, 128)

    # Convert to a numpy array and normalize
    image_array = np.array(display_image) / 255.0  # Normalize to [0, 1]

    # Flatten the image to create a single vector
    image_array = image_array.flatten()  # Shape: (49152,)

    try:
        # Adjusting to use exactly 16384 features
        image_array = image_array[:16384]  # Cut off to get exactly 16384
        image_array = image_array.reshape(1, 1, 16384)  # Shape: (1, 1, 16384)

        # Predict using the model
        predictions = model1.predict(image_array)
        accuracy_score = predictions[0][0]  # Assuming accuracy is the first output
        is_real = predictions[0][1]         # Assuming is_real is the second output

        # Interpret predictions
        status = "Real" if is_real >= 0.5 else "Forged"
        return accuracy_score, status
    except ValueError as e:
        print("Error reshaping the array:", e)
        return None, "Error in processing Model 1"

def process_signature_model2(image_path):
    # Load and preprocess the image
    display_image = Image.open(image_path)
    image_for_model = display_image.resize((your_desired_width, your_desired_height)).convert('RGB')
    image_array = np.array(image_for_model) / 255.0  # Normalize the image

    # Reshape to match the model's input shape
    image_array = image_array.reshape(1, your_desired_width, your_desired_height, 3)

    # Predict using the model
    predictions = model2.predict(image_array)

    # Check the structure of the predictions
    if predictions.shape[-1] == 1:  # Single output node (binary classification)
        accuracy_score = predictions[0][0]
        threshold = 0.6  # Adjust this value
        status = "Real" if accuracy_score >= threshold else "Forged"

    else:  # Two output nodes (softmax or similar)
        real_probability = predictions[0][0]  # Probability for 'Real'
        forged_probability = predictions[0][1]  # Probability for 'Forged'
        status = "Real" if real_probability >= forged_probability else "Forged"
        accuracy_score = max(real_probability, forged_probability)

    return accuracy_score, status

@login_required
def home_view(request):
    accuracy_score_model1 = "N/A"
    status_model1 = "N/A"
    accuracy_score_model2 = "N/A"
    status_model2 = "N/A"
    uploaded_file_url = None

    if request.method == 'POST' and request.FILES.get('signature_image'):
        uploaded_file = request.FILES['signature_image']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        uploaded_file_path = os.path.join(fs.base_location, filename)
        uploaded_file_url = fs.url(filename)

        # Process the image for both models and get the accuracy score and status
        accuracy_score_model1, status_model1 = process_signature_model1(uploaded_file_path)
        accuracy_score_model2, status_model2 = process_signature_model2(uploaded_file_path)

    return render(request, 'accounts/home.html', {
        'accuracy_score_model1': accuracy_score_model1,
        'status_model1': status_model1,
        'accuracy_score_model2': accuracy_score_model2,
        'status_model2': status_model2,
        'uploaded_file_url': uploaded_file_url
    })

@login_required
def upload_signature(request):
    # Initialize variables for results
    model1_accuracy = None
    model1_status = None
    model2_accuracy = None
    model2_status = None
    uploaded_file_url = None

    if request.method == 'POST' and 'signature_image' in request.FILES:
        # Get the uploaded image file
        signature_image = request.FILES['signature_image']
        
        # Save the file using Django's FileSystemStorage
        fs = FileSystemStorage()
        filename = fs.save(signature_image.name, signature_image)
        uploaded_file_url = fs.url(filename)
        image_path = os.path.join(settings.MEDIA_ROOT, filename)

        # Process the image with both models
        model1_accuracy, model1_status = process_signature_model1(image_path)
        model2_accuracy, model2_status = process_signature_model2(image_path)

    # Context to send to the template
    context = {
        'uploaded_file_url': uploaded_file_url,
        'model1': {
            'name': 'Model 1 - Bi-directional RNN',
            'accuracy': model1_accuracy,
            'status': model1_status,
        },
        'model2': {
            'name': 'Model 2 - Convolutional RNN',
            'accuracy': model2_accuracy,
            'status': model2_status,
        },
    }

    return render(request, 'home.html', context)

# Registration and Login views remain unchanged

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect already logged-in users
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect already logged-in users
    
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            print("Form is invalid")
            print(form.errors)  # Display validation errors in the console
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to homepage after logout
