# 2024_SUTD_CV_Final_Project

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/issacj-17/2024_SUTD_CV_Final_Project.git
   cd 2024_SUTD_CV_Final_Project
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. Download the Model weights & dataset

   You can download the model weights of the ViT-LSTM model [here](https://sutdapac.sharepoint.com/:u:/s/202450.035ComputerVision1DProject/EQiaelkJtfRDlL0ZNmxux5YBBrEZV2IQUL-08luC-kJ6lg?e=1XZH5C). Place the `best_model.pth` file in the `checkpoints\vit-lstm` directory in order to execute the notebooks and scripts.
   Also, download the processed dataset [here](https://sutdapac.sharepoint.com/:u:/s/202450.035ComputerVision1DProject/Ed7nOIMb9JdFnTTaXzmJ9XsBP1e0O7-0mFwAOXU0_Xv2Xg?e=GfztK4) and extract the `rgb_face` directory. Place the directory within the `processed` directory within the repository.
   
---

## Run the Application - ViT
   ```bash
   streamlit run scripts/App/app.py
   ```

## Inferencing with ViT

1. **For Livestream**
    ```bash
   python scripts/inferencing/infer.py 
   ```

---

## Training and Evaluation Scripts

### **Training and Evaluation with EnhancedDrowsinessCNN**

The `CNN.py` script provides functionality for training and evaluating the EnhancedDrowsinessCNN. 

1. **Train and Evaluate the EnhancedDrowsinessCNN Model**
   ```bash
   python CNN/CNN.py
   ```

   - This script will:
     - Train the EnhancedDrowsinessCNN model.
     - Evaluate its performance on the test dataset.
     - Save the trained model weights to `CNN/model_weight/cnn.pth`.
   - After execution, it can visualize:
     - Training and validation loss.
     - Validation accuracy and F1 score trends.

---

### **Training and Evaluation with CNN3D**

The `CNN2.py` script provides functionality for training and evaluating the CNN3D.

1. **Train and Evaluate the CNN3D Model**
   ```bash
   python CNN/CNN2.py
   ```

   - This script will:
     - Train the CNN3D model using sequence data.
     - Evaluate its performance on the test dataset.
     - Save the trained model weights to `CNN/model_weight/cnn2.pth`.
   - After execution, it can visualize:
     - Training and validation loss.
     - Validation accuracy and F1 score trends.

---

### **Streamlit Application for Driver Drowsiness Detection (CNN3D)**

   The CNN3D-based driver drowsiness detection app uses your webcam for live predictions. Follow the steps below to launch the app:

   ```bash
   streamlit run CNN/app_cnn.py
   ```

   - Ensure your webcam is connected and accessible by the system.
   - Press the "Start/Stop" button in the interface to toggle recording.
   - The app will display live predictions ("Drowsy" or "Non-Drowsy") based on the video stream.

---





