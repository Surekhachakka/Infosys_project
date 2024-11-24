from tensorflow.keras.models import load_model
import numpy as np

def get_model_accuracy_and_status(image, model_name):
    # Load the model based on the model_name
    if model_name == 'model1':
        model_path = r"C:\Users\venka\OneDrive\Desktop\Project\bi_rnn_signature_verification_model.h5"
    elif model_name == 'model2':
        model_path = r"C:\Users\venka\OneDrive\Desktop\Project\crnn_signature_verification_model.keras"
    else:
        raise ValueError("Unknown model name: {}".format(model_name))
    
    # Load the model
    model = load_model(model_path)
    
    # Assuming the model expects images to be normalized, we can normalize the image
    image = image.astype('float32') / 255.0  # Normalize the image to the range [0, 1]
    
    # Get model predictions
    prediction = model.predict(image)  # Predict using the model
    
    # Assuming the model gives a score, adjust this according to your model's output
    accuracy = prediction[0][0]  # Example, adjust this based on your model's output
    status = "Verified" if accuracy > 0.9 else "Not Verified"
    
    return accuracy, status
