import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
from io import BytesIO
from fpdf import FPDF
import os
from datetime import datetime

# Load the pre-trained model
model = tf.keras.models.load_model('Final/last_model.keras')

def preprocess_image(image):
    """
    Preprocesses the uploaded image for model prediction.
    """
    image = image.resize((224, 224))  # Resize to match the model's expected input size
    img_array = np.array(image)
    img_array = tf.keras.applications.resnet.preprocess_input(img_array)  # Preprocessing for ResNet
    img_array = np.expand_dims(img_array, axis=0)  # Add a batch dimension
    return img_array

def predict_image(model, img_array, threshold=0.5):
    """
    Predicts whether an image is cancerous or not using the loaded model.
    """
    pred = model.predict(img_array)
    score = pred[0][0]  # Extract the prediction probability

    if score > threshold:
        prediction = "Normal"
        confidence = score  # Confidence for Normal class
    else:
        prediction = "Cancer"
        confidence = 1 - score  # Confidence for Cancer class
    
    return prediction, confidence

def generate_pdf_report(name, age, laterality, prediction, confidence, image, additional_notes):
    """
    Generates a visually appealing PDF report including user details, prediction results, and the image.
    """
    pdf = FPDF()
    pdf.add_page()

    # Add a title with a border
    pdf.set_font("Arial", "B", 20)
    pdf.set_text_color(0, 51, 102)  # Dark blue color
    pdf.cell(0, 10, "Breast Cancer Detection Report", ln=True, align="C", border=0)

    # Add a horizontal line
    pdf.set_draw_color(0, 51, 102)  # Dark blue color
    pdf.set_line_width(0.5)
    pdf.line(10, 20, 200, 20)

    # pdf.ln(10)  # Add some vertical space

    # Add report generation date and time
    pdf.set_font("Arial", "I", 10)
    pdf.set_text_color(128, 128, 128)  # Gray color
    report_date = datetime.now().strftime("%B %d, %Y, %I:%M %p")
    pdf.cell(0, 10, f"Report Generated On: {report_date}", ln=True, align="R")

    pdf.ln(5)  # Add some vertical space

    # Add patient details
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(0, 0, 0)  # Black color
    pdf.cell(0, 10, "Patient Details", ln=True, align="L")

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Name: {name}", ln=True)
    pdf.cell(0, 10, f"Age: {age}", ln=True)
    pdf.cell(0, 10, f"Breast Laterality: {laterality}", ln=True)

    # Add additional notes
    if additional_notes.strip():
        pdf.ln(5)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Additional Notes", ln=True, align="L")
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, additional_notes)

    pdf.ln(10)  # Add some vertical space

    # Add prediction results
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Prediction Results", ln=True, align="L")

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Prediction: {prediction}", ln=True)
    pdf.cell(0, 10, f"Confidence: {confidence * 100:.2f}%", ln=True)

    pdf.ln(10)  # Add space after the bar

    # Add the uploaded image
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Uploaded Image", ln=True, align="L")

    # Save the image to a temporary file for FPDF compatibility
    temp_img_path = "temp_image.png"
    image.save(temp_img_path, format="PNG")

    # Insert the image into the PDF
    pdf.image(temp_img_path, x=10, y=pdf.get_y(), w=100)

    # Remove the temporary image file after inserting it into the PDF
    if os.path.exists(temp_img_path):
        os.remove(temp_img_path)

    # pdf.ln(10)  # Add some vertical space after the image

    # Add a footer
    pdf.set_y(-45)
    pdf.set_font("Arial", "I", 10)
    pdf.set_text_color(128, 128, 128)  # Gray color
    pdf.cell(0, 10, "This report is generated by the Breast Cancer Detection System.", ln=True, align="C")
    pdf.cell(0, 10, "For informational purposes only. Consult a medical professional for diagnosis.", ln=True, align="C")

    # Output the PDF to a string buffer
    pdf_buffer = BytesIO()
    pdf_output = pdf.output(dest="S").encode("latin1")  # Get the PDF as a string
    pdf_buffer.write(pdf_output)
    pdf_buffer.seek(0)
    return pdf_buffer

def main():
    # Set a custom page layout
    st.set_page_config(page_title="Breast Cancer Detection", page_icon="🩺", layout="wide")

    # Add a header with a background color
    st.markdown(
        """
        <style>
        .main-header {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        .main-header h1 {
            color: #343a40;
            font-size: 2.5rem;
        }
        </style>
        <div class="main-header">
            <h1>Breast Cancer Detection</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("### Upload a mammogram image to classify it as cancerous or non-cancerous.")

    # Center-aligned upload button using columns
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    # Initialize session state to hold prediction details
    if "prediction" not in st.session_state:
        st.session_state.prediction = None
    if "confidence" not in st.session_state:
        st.session_state.confidence = None

    if uploaded_file is not None:
        image = Image.open(uploaded_file)

        # Create two columns: one for the image and one for the results/details
        st.markdown("---")
        st.write("### Results")
        image_col, details_col = st.columns([1, 1])

        with image_col:
            st.image(image, caption="Uploaded Image", use_container_width=True)

        with details_col:
            st.subheader("Prediction Results")
            img_preprocessed = preprocess_image(image)
            prediction, confidence = predict_image(model, img_preprocessed)

            st.markdown(f"<h3 style='color: #007bff;'>Prediction: {prediction}</h3>", unsafe_allow_html=True)
            st.markdown(f"<h4>Confidence: {confidence * 100:.2f}%</h4>", unsafe_allow_html=True)

            # Save the prediction details in session state for PDF generation
            st.session_state.prediction = prediction
            st.session_state.confidence = confidence

            st.markdown("---")
            st.subheader("Patient Information")
            name = st.text_input("Name:")
            age = st.text_input("Age:")
            laterality = st.selectbox("Breast Laterality:", ["Left", "Right"])  # Dropdown for laterality
            additional_info = st.text_area("Additional Information:")

            # Generate PDF report button
            if st.button("Generate PDF Report"):
                if name and age and laterality:
                    # Pass additional_info as additional_notes
                    pdf_buffer = generate_pdf_report(name, age, laterality, prediction, confidence, image, additional_info)
                    # Create a dynamic filename using the entered name
                    filename = f"{name.replace(' ', '_')}_breast_cancer_result.pdf"
                    st.download_button(
                        label="Download Report as PDF",
                        data=pdf_buffer,
                        file_name=filename,
                        mime="application/pdf",
                    )
                else:
                    st.error("Please enter your name, age, and breast laterality to generate the report.")

if __name__ == "__main__":
    main()