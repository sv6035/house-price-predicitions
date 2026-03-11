# 🏠 House Price Prediction System

A complete end-to-end machine learning project that predicts house prices based on features like area, bedrooms, bathrooms, age, and location score. Deployed on AWS using Free Tier services.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3.0-orange.svg)
![AWS](https://img.shields.io/badge/AWS-Free%20Tier-yellow.svg)

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Dataset Description](#dataset-description)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [AWS Deployment](#aws-deployment)
- [Architecture](#architecture)
- [Model Performance](#model-performance)
- [Technologies Used](#technologies-used)

---

## 🎯 Project Overview

This project implements a complete data science pipeline:

1. **Data Collection**: Synthetic dataset generation
2. **Data Cleaning**: Handle missing values, duplicates, outliers
3. **EDA**: Comprehensive exploratory data analysis
4. **Feature Engineering**: Create and transform features
5. **Model Training**: Train multiple ML models (Linear Regression, Random Forest, Gradient Boosting)
6. **Model Evaluation**: Compare models using RMSE, MAE, R² metrics
7. **Deployment**: Flask web application on AWS EC2
8. **Storage**: Model artifacts stored on AWS S3

---

## ✨ Features

- 🤖 Multiple ML models with automatic best model selection
- 📊 Interactive web interface for predictions
- 🔄 Complete data preprocessing pipeline
- 📈 Comprehensive EDA with visualizations
- ☁️ AWS deployment with Free Tier services
- 🔐 Secure S3 integration for model storage
- 📱 Responsive web design
- 🚀 RESTful API endpoint for predictions

---

## 📊 Dataset Description

The dataset contains 1000 house records with the following features:

| Feature | Description | Range |
|---------|-------------|-------|
| **area** | House area in square feet | 500 - 5000 sq ft |
| **bedrooms** | Number of bedrooms | 1 - 5 |
| **bathrooms** | Number of bathrooms | 1 - 4 |
| **age** | Age of the house in years | 0 - 100 years |
| **location_score** | Location quality score | 1 - 10 |
| **price** | House price (target variable) | $50,000 - $2,000,000 |

### Feature Correlations with Price:
- **Area**: Strong positive correlation (~0.85)
- **Location Score**: Strong positive correlation (~0.75)
- **Bathrooms**: Moderate positive correlation (~0.60)
- **Bedrooms**: Moderate positive correlation (~0.55)
- **Age**: Negative correlation (~-0.40)

---

## 📁 Project Structure

```
house-price-prediction/
│
├── data/
│   ├── raw/                      # Raw dataset
│   │   └── house_data.csv
│   ├── processed/                # Processed datasets
│   │   ├── cleaned_data.csv
│   │   └── engineered_data.csv
│   └── generate_data.py          # Dataset generator
│
├── notebooks/
│   └── eda.ipynb                 # Exploratory Data Analysis
│
├── src/
│   ├── data_cleaning.py          # Data cleaning module
│   ├── feature_engineering.py    # Feature engineering module
│   ├── train_model.py            # Model training module
│   └── evaluate_model.py         # Model evaluation module
│
├── models/
│   ├── house_price_model.pkl     # Trained model
│   ├── scaler.pkl                # Feature scaler
│   ├── feature_names.pkl         # Feature names
│   └── encoders.pkl              # Label encoders
│
├── app/
│   ├── app.py                    # Flask application
│   └── templates/
│       └── index.html            # Web interface
│
├── run_pipeline.py               # Main pipeline script
├── s3_integration.py             # AWS S3 integration
├── deploy_aws.sh                 # AWS deployment script
├── requirements.txt              # Python dependencies
└── README.md                     # Documentation
```

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git

### Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/house-price-prediction.git
cd house-price-prediction
```

2. **Create virtual environment** (recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Generate sample dataset**
```bash
python data/generate_data.py
```

---

## 💻 Usage

### Run Complete Pipeline

Execute the entire ML pipeline (data cleaning → feature engineering → model training):

```bash
python run_pipeline.py
```

### Run Individual Steps

**Data Cleaning:**
```bash
python src/data_cleaning.py
```

**Feature Engineering:**
```bash
python src/feature_engineering.py
```

**Model Training:**
```bash
python src/train_model.py
```

**Model Evaluation:**
```bash
python src/evaluate_model.py
```

### Start Web Application

```bash
cd app
python app.py
```

Access the application at: `http://localhost:5000`

### API Usage

**Endpoint:** `POST /api/predict`

**Request:**
```json
{
  "area": 1800,
  "bedrooms": 3,
  "bathrooms": 2,
  "age": 10,
  "location_score": 7.5
}
```

**Response:**
```json
{
  "success": true,
  "prediction": 425000.50,
  "formatted": "$425,000.50"
}
```

---

## ☁️ AWS Deployment

### Architecture

```
User Browser
     ↓
  Internet
     ↓
AWS EC2 (t2.micro)
  - Flask App
  - ML Model
     ↓
AWS S3
  - Model Storage
  - Data Storage
```

### Step-by-Step Deployment

#### 1. Launch EC2 Instance

1. Go to AWS Console → EC2
2. Click "Launch Instance"
3. **Configuration:**
   - **AMI**: Ubuntu Server 22.04 LTS (Free Tier)
   - **Instance Type**: t2.micro (Free Tier)
   - **Storage**: 8 GB (Free Tier)
4. **Security Group:**
   - SSH (Port 22): Your IP
   - HTTP (Port 80): 0.0.0.0/0
   - Custom TCP (Port 5000): 0.0.0.0/0
5. Create/download key pair
6. Launch instance

#### 2. Connect to EC2

```bash
# Windows (use PuTTY or WSL)
ssh -i "your-key.pem" ubuntu@YOUR_EC2_PUBLIC_IP

# Linux/Mac
chmod 400 your-key.pem
ssh -i "your-key.pem" ubuntu@YOUR_EC2_PUBLIC_IP
```

#### 3. Setup Application

```bash
# Update system
sudo apt-get update -y
sudo apt-get upgrade -y

# Install Python and dependencies
sudo apt-get install python3 python3-pip git -y

# Clone repository
git clone https://github.com/YOUR_USERNAME/house-price-prediction.git
cd house-price-prediction

# Install Python packages
pip3 install -r requirements.txt

# Generate data and train model
python3 data/generate_data.py
python3 run_pipeline.py
```

#### 4. Configure AWS S3 (Optional)

```bash
# Install AWS CLI
sudo apt-get install awscli -y

# Configure AWS credentials
aws configure
# Enter: Access Key ID, Secret Access Key, Region (us-east-1), Format (json)

# Upload models to S3
python3 s3_integration.py upload

# Download models from S3 (on new instances)
python3 s3_integration.py download
```

#### 5. Run Application

**Option A: Direct Run (for testing)**
```bash
cd app
python3 app.py
```

**Option B: Production with systemd**
```bash
# Run deployment script
chmod +x deploy_aws.sh
./deploy_aws.sh

# Check status
sudo systemctl status house-price-app

# View logs
sudo journalctl -u house-price-app -f
```

#### 6. Access Application

Open browser: `http://YOUR_EC2_PUBLIC_IP:5000`

### AWS Free Tier Limits

✅ **Stays within Free Tier:**
- EC2: t2.micro (750 hours/month)
- S3: 5 GB storage, 20,000 GET requests, 2,000 PUT requests
- Data Transfer: 15 GB/month

⚠️ **Monitor Usage:**
- Set up billing alerts in AWS Console
- Check usage regularly in Cost Explorer

---

## 🏗️ Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                     USER INTERFACE                       │
│                   (Web Browser)                          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   FLASK WEB APP                          │
│                  (AWS EC2 t2.micro)                      │
│  ┌──────────────────────────────────────────────────┐   │
│  │  • Route Handling                                 │   │
│  │  • Input Validation                               │   │
│  │  • Prediction Logic                               │   │
│  └──────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                ML MODEL PIPELINE                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │  1. Feature Scaling (StandardScaler)             │   │
│  │  2. Model Prediction (Random Forest/GB)          │   │
│  │  3. Output Formatting                            │   │
│  └──────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                    AWS S3 BUCKET                         │
│  • Model Artifacts (house_price_model.pkl)               │
│  • Preprocessing Objects (scaler.pkl)                    │
│  • Training Data (engineered_data.csv)                   │
└─────────────────────────────────────────────────────────┘
```

---

## 📈 Model Performance

### Models Trained

1. **Linear Regression**
   - Simple baseline model
   - Fast training and prediction
   - Assumes linear relationships

2. **Random Forest Regressor**
   - Ensemble of decision trees
   - Handles non-linear relationships
   - Robust to outliers

3. **Gradient Boosting Regressor**
   - Sequential ensemble method
   - High accuracy
   - Best performance on test set

### Expected Performance Metrics

| Model | RMSE | MAE | R² Score |
|-------|------|-----|----------|
| Linear Regression | ~$45,000 | ~$35,000 | 0.92 |
| Random Forest | ~$35,000 | ~$25,000 | 0.95 |
| Gradient Boosting | ~$30,000 | ~$22,000 | 0.97 |

*Note: Actual metrics may vary based on the generated dataset*

---

## 🛠️ Technologies Used

### Machine Learning & Data Science
- **Python 3.8+**: Core programming language
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Scikit-learn**: Machine learning algorithms
- **Matplotlib & Seaborn**: Data visualization

### Web Development
- **Flask**: Web framework
- **HTML/CSS**: Frontend interface
- **Jinja2**: Template engine

### Cloud & DevOps
- **AWS EC2**: Application hosting
- **AWS S3**: Model and data storage
- **AWS IAM**: Access management
- **Boto3**: AWS SDK for Python

### Development Tools
- **Git**: Version control
- **Jupyter Notebook**: Interactive analysis
- **Joblib**: Model serialization

---

## 📝 Future Enhancements

- [ ] Add more features (garage, pool, etc.)
- [ ] Implement real-time data updates
- [ ] Add user authentication
- [ ] Deploy with Docker containers
- [ ] Add CI/CD pipeline with GitHub Actions
- [ ] Implement A/B testing for models
- [ ] Add model monitoring and retraining
- [ ] Create mobile app interface
- [ ] Add geolocation-based predictions
- [ ] Implement explainable AI (SHAP values)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👤 Author

**Your Name**
- GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- LinkedIn: [Your Profile](https://linkedin.com/in/YOUR_PROFILE)

---

## 🙏 Acknowledgments

- Dataset inspired by Kaggle House Prices competition
- AWS Free Tier documentation
- Scikit-learn community
- Flask documentation

---

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Email: your.email@example.com

---

**⭐ If you find this project helpful, please give it a star!**
