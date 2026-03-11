# Step-by-Step Execution Guide

## Complete Walkthrough: From Zero to Deployed ML Application

---

## 🎯 What You'll Accomplish

By the end of this guide, you will have:
- ✅ A trained machine learning model
- ✅ A working web application
- ✅ Deployment on AWS Free Tier
- ✅ A complete portfolio project

**Estimated Time**: 30-45 minutes

---

## Phase 1: Local Setup (15 minutes)

### Step 1: Verify Prerequisites (2 minutes)

Check if you have Python installed:
```bash
python --version
# Should show Python 3.8 or higher
```

If not installed:
- **Windows**: Download from python.org
- **Mac**: `brew install python3`
- **Linux**: `sudo apt-get install python3`

### Step 2: Navigate to Project (1 minute)

```bash
cd c:\Users\sv340\OneDrive\Desktop\aws project\house-price-prediction
```

### Step 3: Create Virtual Environment (2 minutes)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# You should see (venv) in your terminal
```

### Step 4: Install Dependencies (3 minutes)

```bash
pip install -r requirements.txt

# This will install:
# - pandas, numpy (data processing)
# - matplotlib, seaborn (visualization)
# - scikit-learn (machine learning)
# - flask (web framework)
# - boto3 (AWS integration)
```

### Step 5: Test Setup (2 minutes)

```bash
python test_setup.py

# Expected output:
# ✅ All packages installed
# ✅ All directories exist
# ✅ All files exist
# ✅ Data generation works
# ✅ Model training works
```

If any test fails, review the error messages and fix before proceeding.

### Step 6: Generate Dataset (2 minutes)

```bash
python data/generate_data.py

# Expected output:
# ✓ Dataset generated successfully!
# ✓ Saved to: data/raw/house_data.csv
# Dataset Info:
#   Samples: 1000
#   Features: 5
```

Verify the file was created:
```bash
# Windows:
dir data\raw\house_data.csv

# Mac/Linux:
ls -lh data/raw/house_data.csv
```

### Step 7: Run ML Pipeline (3 minutes)

```bash
python run_pipeline.py

# This will:
# 1. Clean the data
# 2. Engineer features
# 3. Train 3 models
# 4. Select best model
# 5. Save model files

# Expected output:
# ==================================================
# DATA CLEANING PIPELINE
# ==================================================
# Dataset loaded: 1000 rows, 6 columns
# ...
# ==================================================
# FEATURE ENGINEERING PIPELINE
# ==================================================
# ...
# ==================================================
# MODEL TRAINING
# ==================================================
# Training Linear Regression...
# Training Random Forest...
# Training Gradient Boosting...
# 
# MODEL EVALUATION
# Linear Regression:
#   RMSE: $45,234.56
#   MAE:  $34,567.89
#   R²:   0.9234
# 
# Random Forest:
#   RMSE: $35,123.45
#   MAE:  $25,678.90
#   R²:   0.9512
# 
# Gradient Boosting:
#   RMSE: $30,456.78
#   MAE:  $22,345.67
#   R²:   0.9678
# 
# BEST MODEL: Gradient Boosting
# R² Score: 0.9678
# Model saved to: models/house_price_model.pkl
```

Verify model files were created:
```bash
# Windows:
dir models\*.pkl

# Mac/Linux:
ls -lh models/*.pkl

# You should see:
# - house_price_model.pkl
# - scaler.pkl
# - feature_names.pkl
```

---

## Phase 2: Test Locally (5 minutes)

### Step 8: Start Flask Application (1 minute)

```bash
cd app
python app.py

# Expected output:
# ✓ Model loaded successfully
# ✓ Scaler loaded successfully
# ✓ Feature names loaded successfully
#  * Running on http://0.0.0.0:5000
#  * Running on http://127.0.0.1:5000
```

**Keep this terminal open!** The app is now running.

### Step 9: Test Web Interface (2 minutes)

1. Open your web browser
2. Go to: `http://localhost:5000`
3. You should see the House Price Predictor interface

**Test with sample data:**
- Area: 1800
- Bedrooms: 3
- Bathrooms: 2
- Age: 10
- Location Score: 7.5

Click "Predict Price"

**Expected Result**: You should see a predicted price (e.g., "$425,000.50")

### Step 10: Test API Endpoint (2 minutes)

Open a NEW terminal (keep the Flask app running):

```bash
# Test API with curl
curl -X POST http://localhost:5000/api/predict -H "Content-Type: application/json" -d "{\"area\": 1800, \"bedrooms\": 3, \"bathrooms\": 2, \"age\": 10, \"location_score\": 7.5}"

# Expected response:
# {
#   "success": true,
#   "prediction": 425000.50,
#   "formatted": "$425,000.50"
# }
```

**✅ If you see the prediction, your local setup is complete!**

Stop the Flask app (Ctrl+C in the terminal where it's running).

---

## Phase 3: AWS Deployment (20 minutes)

### Step 11: AWS Account Setup (5 minutes)

1. **Create AWS Account** (if you don't have one)
   - Go to https://aws.amazon.com
   - Click "Create an AWS Account"
   - Follow the registration process
   - **Note**: Credit card required but won't be charged in Free Tier

2. **Set Billing Alert**
   - AWS Console → Billing Dashboard
   - Click "Billing Preferences"
   - Enable "Receive Free Tier Usage Alerts"
   - Enter your email
   - Set threshold: $5

3. **Create IAM User** (Security Best Practice)
   - AWS Console → IAM → Users → Add users
   - Username: `house-price-admin`
   - Access type: ✅ Programmatic + ✅ Console
   - Attach policies: `AmazonEC2FullAccess`, `AmazonS3FullAccess`
   - Download credentials CSV
   - **IMPORTANT**: Save this file securely!

### Step 12: Launch EC2 Instance (5 minutes)

1. **Go to EC2 Dashboard**
   - AWS Console → EC2 → Launch Instance

2. **Configure Instance**
   - **Name**: `house-price-prediction-server`
   - **AMI**: Ubuntu Server 22.04 LTS (Free Tier eligible)
   - **Instance Type**: t2.micro (Free Tier eligible)
   - **Key Pair**: Create new → Name: `house-price-key` → Download .pem file
   - **SAVE THE .pem FILE** - You can't download it again!

3. **Configure Security Group**
   - Click "Edit" under Network Settings
   - **Add rules**:
     - SSH (22): My IP
     - HTTP (80): 0.0.0.0/0
     - Custom TCP (5000): 0.0.0.0/0

4. **Storage**: 8 GB (default is fine)

5. **Launch Instance**

6. **Note Your Instance Details**
   - Wait for "Instance State" to show "Running"
   - Copy the "Public IPv4 address" (e.g., 54.123.45.67)

### Step 13: Connect to EC2 (3 minutes)

**Windows Users:**
```bash
# If using WSL or Git Bash:
chmod 400 house-price-key.pem
ssh -i "house-price-key.pem" ubuntu@YOUR_EC2_IP

# If using PuTTY:
# 1. Convert .pem to .ppk using PuTTYgen
# 2. Use PuTTY to connect with the .ppk file
```

**Mac/Linux Users:**
```bash
chmod 400 house-price-key.pem
ssh -i "house-price-key.pem" ubuntu@YOUR_EC2_IP
```

**Expected**: You should now be connected to your EC2 instance!

### Step 14: Setup Server (5 minutes)

**Run these commands on your EC2 instance:**

```bash
# Update system
sudo apt-get update -y
sudo apt-get upgrade -y

# Install Python and dependencies
sudo apt-get install python3 python3-pip git -y

# Verify installations
python3 --version
pip3 --version

# Clone repository (replace with your GitHub URL)
# Option A: If you pushed to GitHub
git clone https://github.com/YOUR_USERNAME/house-price-prediction.git

# Option B: If not on GitHub, upload via SCP from your local machine
# (Run this from your LOCAL machine, not EC2)
# scp -i "house-price-key.pem" -r house-price-prediction ubuntu@YOUR_EC2_IP:~

# Navigate to project
cd house-price-prediction

# Install Python packages
pip3 install -r requirements.txt
```

### Step 15: Generate Data and Train Model (2 minutes)

**On EC2:**
```bash
# Generate dataset
python3 data/generate_data.py

# Run pipeline
python3 run_pipeline.py

# This will take 1-2 minutes
# You should see the same output as local training
```

### Step 16: Start Application (2 minutes)

**Option A: Quick Test (Foreground)**
```bash
cd app
python3 app.py

# App will run in foreground
# Access at: http://YOUR_EC2_IP:5000
```

**Option B: Production (Background with systemd)**
```bash
# Create service file
sudo nano /etc/systemd/system/house-price-app.service

# Paste this content:
[Unit]
Description=House Price Prediction Flask App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/house-price-prediction/app
ExecStart=/usr/bin/python3 /home/ubuntu/house-price-prediction/app/app.py
Restart=always

[Install]
WantedBy=multi-user.target

# Save: Ctrl+X, then Y, then Enter

# Start service
sudo systemctl daemon-reload
sudo systemctl start house-price-app
sudo systemctl enable house-price-app

# Check status
sudo systemctl status house-price-app

# Should show: Active: active (running)
```

### Step 17: Access Your Application (1 minute)

1. Open your web browser
2. Go to: `http://YOUR_EC2_PUBLIC_IP:5000`
3. You should see your House Price Predictor!

**Test it:**
- Enter house details
- Click "Predict Price"
- See the prediction!

**🎉 Congratulations! Your ML app is live on AWS!**

---

## Phase 4: Optional Enhancements (10 minutes)

### Step 18: Setup S3 Storage (Optional)

**On EC2:**
```bash
# Configure AWS CLI
aws configure
# Enter your Access Key ID
# Enter your Secret Access Key
# Region: us-east-1
# Format: json

# Upload models to S3
python3 s3_integration.py upload

# Models are now backed up in S3!
```

### Step 19: Allocate Elastic IP (Optional)

**Why?** Your EC2 public IP changes when you stop/start the instance.

1. AWS Console → EC2 → Elastic IPs
2. Click "Allocate Elastic IP address"
3. Click "Allocate"
4. Select the new IP → Actions → Associate Elastic IP address
5. Select your instance → Associate

**Now your IP is permanent!**

⚠️ **Warning**: Elastic IPs are free when associated with a running instance, but cost money when not in use!

---

## Phase 5: Verification Checklist

### ✅ Local Setup Checklist
- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] All dependencies installed
- [ ] Test setup passed
- [ ] Dataset generated (1000 samples)
- [ ] Model trained successfully
- [ ] Model files created (.pkl files)
- [ ] Flask app runs locally
- [ ] Web interface accessible at localhost:5000
- [ ] Predictions working
- [ ] API endpoint working

### ✅ AWS Deployment Checklist
- [ ] AWS account created
- [ ] Billing alerts configured
- [ ] IAM user created
- [ ] EC2 instance launched (t2.micro)
- [ ] Security group configured (ports 22, 80, 5000)
- [ ] Key pair downloaded and saved
- [ ] Connected to EC2 via SSH
- [ ] Python and dependencies installed on EC2
- [ ] Code deployed to EC2
- [ ] Dataset generated on EC2
- [ ] Model trained on EC2
- [ ] Flask app running on EC2
- [ ] Application accessible via EC2 public IP
- [ ] Predictions working on live server

### ✅ Optional Enhancements Checklist
- [ ] S3 bucket created
- [ ] AWS CLI configured
- [ ] Models uploaded to S3
- [ ] Elastic IP allocated (optional)
- [ ] Domain configured (optional)

---

## Common Issues and Solutions

### Issue 1: "Module not found" error
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue 2: Can't connect to EC2
**Solutions:**
- Check security group allows SSH (port 22) from your IP
- Verify instance is running
- Check you're using the correct .pem file
- Ensure username is `ubuntu`

### Issue 3: Can't access web app on EC2
**Solutions:**
- Check security group allows port 5000
- Verify Flask app is running: `sudo systemctl status house-price-app`
- Check logs: `sudo journalctl -u house-price-app -f`
- Test locally on EC2: `curl http://localhost:5000`

### Issue 4: Model not found
**Solution:**
```bash
# Ensure you ran the pipeline
python3 run_pipeline.py

# Check if models exist
ls -la models/
```

### Issue 5: Out of memory on EC2
**Solution:**
- t2.micro has only 1GB RAM
- Reduce dataset size if needed
- Use simpler models (Linear Regression instead of Random Forest)

---

## Monitoring and Maintenance

### Check Application Status
```bash
# SSH into EC2
ssh -i "house-price-key.pem" ubuntu@YOUR_EC2_IP

# Check if app is running
sudo systemctl status house-price-app

# View logs
sudo journalctl -u house-price-app -n 50

# Follow logs in real-time
sudo journalctl -u house-price-app -f
```

### Restart Application
```bash
sudo systemctl restart house-price-app
```

### Update Application
```bash
cd ~/house-price-prediction
git pull origin main
sudo systemctl restart house-price-app
```

### Monitor AWS Costs
1. AWS Console → Billing Dashboard
2. Check "Free Tier Usage"
3. Review "Cost Explorer"

### Stop EC2 (Save Costs)
```bash
# From AWS Console
EC2 → Instances → Select instance → Instance state → Stop

# Or via CLI
aws ec2 stop-instances --instance-ids i-XXXXXXXXXXXXXXXXX
```

**Note**: Stopping the instance doesn't count toward your 750 free hours!

---

## Next Steps

### Immediate (Today)
1. ✅ Test your application thoroughly
2. ✅ Share with friends/family for feedback
3. ✅ Take screenshots for your portfolio

### Short Term (This Week)
1. 📝 Add to your resume/portfolio
2. 🐙 Push code to GitHub
3. 💼 Update LinkedIn with project
4. 📸 Create a demo video

### Medium Term (This Month)
1. 🎨 Customize the UI
2. 📊 Add more features to the model
3. 📈 Implement logging and monitoring
4. 🧪 Add unit tests

### Long Term (Next 3 Months)
1. 🐳 Dockerize the application
2. 🔄 Setup CI/CD pipeline
3. 🔐 Add user authentication
4. 📱 Create mobile app version

---

## Resources

### Documentation
- 📚 [README.md](README.md) - Complete project documentation
- 🏗️ [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- ☁️ [AWS_DEPLOYMENT_GUIDE.md](AWS_DEPLOYMENT_GUIDE.md) - Detailed AWS guide
- 🚀 [QUICKSTART.md](QUICKSTART.md) - Quick setup guide
- 📊 [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Project overview

### Learning Resources
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [AWS Free Tier](https://aws.amazon.com/free/)
- [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/)

### Community
- GitHub Issues: Report bugs
- GitHub Discussions: Ask questions
- Stack Overflow: Technical help
- AWS Forums: Cloud questions

---

## Congratulations! 🎉

You've successfully:
- ✅ Built a complete ML pipeline
- ✅ Created a web application
- ✅ Deployed to AWS Free Tier
- ✅ Gained hands-on experience with:
  - Python programming
  - Machine learning
  - Web development
  - Cloud computing
  - DevOps practices

**This is a production-ready project you can showcase in your portfolio!**

---

## Share Your Success

- 🐦 Tweet: "Just deployed my ML app on AWS! 🚀 #MachineLearning #AWS #DataScience"
- 💼 LinkedIn: Write a post about your project
- 🎥 YouTube: Create a demo video
- 📝 Blog: Write about your experience
- ⭐ GitHub: Star the repository

---

## Need Help?

- 📧 Email: your.email@example.com
- 🐙 GitHub Issues: Report problems
- 💬 GitHub Discussions: Ask questions
- 📚 Documentation: Read the guides

---

**Thank you for building this project! Happy coding! 🚀**
