# 🧠 Breast Cancer Detection Using Deep Learning

An end-to-end AI-driven system for early detection and diagnosis of breast cancer from mammogram images using Convolutional Neural Networks (CNNs).

## 📌 Project Overview

This project uses grayscale mammogram images to classify whether the tissue is **cancerous** or **non-cancerous**. The pipeline includes preprocessing, deep learning-based feature extraction, and final classification. Augmentation techniques have been used to balance the dataset and enhance model generalization.

> ✅ Final Year Project | 🎓 Christ University | 💼 Internship @ SkynetClouds

---

## 🧪 Technologies Used

- **Python**
- **TensorFlow / Keras**
- **OpenCV**
- **Scikit-learn**
- **Matplotlib / Seaborn**
- **Streamlit** *(for demo UI)*
- **DICOM handling with pydicom*

---

## 📁 Dataset Description

The dataset is composed of original and augmented grayscale mammogram images.

### 🧬 Dataset Summary

| Dataset Type | Cancer Images | Non-Cancer Images |
|--------------|----------------|-------------------|
| Original     | 125            | 620               |
| Augmented    | 1625           | 8060              |

---

## 🧰 Project Pipeline

1. **Data Preprocessing**
   - Resizing to (224, 224)
   - Grayscale normalization
   - Augmentation (flip, rotation, blur, etc.)

2. **Dataset Splitting**
   - Train / Validation / Test
   - Organized into `cancer/` and `non-cancer/` folders

3. **Model Development**
   - Custom CNN architecture
   - Trained on augmented dataset
   - Evaluation on original test images

4. **Classification**
   - Binary classification (Cancer / Non-Cancer)
   - Accuracy, Precision, Recall, F1-Score

5. **Streamlit UI**
   - Upload an image
   - Get prediction with confidence score
   - Generate Diagnosis Report

---

## 📊 Results

- **Accuracy:** ~98%  
- **Precision:** 99%  
- **Recall:** 97%  

---

## 📽️ Demo Video

Watch the live demo of the breast cancer detection system in action:  
👉 [Click here to watch on YouTube](https://youtu.be/bAw29_oJn48)

### Installation

```bash
pip install -r requirements.txt
```

🧬 Future Work

- Incorporate more advanced architectures (e.g., ResNet, EfficientNet)
- Improve explainability using Grad-CAM
- Explore federated learning for privacy preservation
- Deploy as a web app with a medical-grade interface

👨‍💻 Author

Abhilash Antony🎓 
MSc Data Analytics
Christ University
💼 Intern @ SkynetClouds
