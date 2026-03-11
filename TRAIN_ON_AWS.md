# 🚀 Train on AWS Directly - No Laptop Training Needed

## Perfect for: Users who want to train models directly on AWS Free Tier

---

## ⚡ Quick Overview

**What this guide does:**
- Skip local training completely
- Do everything on AWS EC2 (Free Tier)
- Train model on cloud
- Deploy immediately

**Time Required:** 30 minutes
**Cost:** $0 (Free Tier)

---

## 📋 Step-by-Step Guide

### Step 1: Launch EC2 Instance (5 minutes)

1. **Login to AWS Console**
   - Go to https://aws.amazon.com/console/
   - Sign in to your account

2. **Go to EC2**
   - Search for "EC2" in the top search bar
   - Click "EC2"

3. **Launch Instance**
   - Click orange "Launch Instance" button

4. **Configure Instance:**

   **Name:** `house-price-ml-server`

   **Application and OS Images (AMI):**
   - Select: **Ubuntu Server 22.04 LTS (HVM), SSD Volume Type**
   - Make sure it says "Free tier eligible"

   **Instance Type:**
   - Select: **t2.micro** (Free tier eligible)
   - 1 vCPU, 1 GB RAM

   **Key Pair:**
   - Click "Create new key pair"
   - Name: `ml-training-key`
   - Type: RSA
   - Format: `.pem` (for Mac/Linux) or `.ppk` (for Windows/PuTTY)
   - Click "Create key pair"
   - **SAVE THE FILE** - You can't download it again!

   **Network Settings:**
   - Click "Edit"
   - Add these rules:
     - SSH (Port 22): My IP
     - HTTP (Port 80): 0.0.0.0/0
     - Custom TCP (Port 5000): 0.0.0.0/0

   **Storage:**
   - 8 GB (default is fine)

5. **Launch Instance**
   - Click "Launch instance"
   - Wait for "Instance state" to show "Running" (1-2 minutes)

6. **Get Public IP**
   - Click on your instance
   - Copy the "Public IPv4 address" (e.g., 54.123.45.67)

---

### Step 2: Connect to EC2 (2 minutes)

**For Windows (using PuTTY):**
```
1. Download PuTTY from putty.org
2. Convert .pem to .ppk using PuTTYgen
3. Open PuTTY
4. Host: ubuntu@YOUR_EC2_IP
5. Port: 22
6. Load your .ppk file in SSH > Auth
7. Click Open
```

**For Mac/Linux/Windows WSL:**
```bash
# Set permissions
chmod 400 ml-training-key.pem

# Connect
ssh -i "ml-training-key.pem" ubuntu@YOUR_EC2_IP
```

**Expected:** You should see Ubuntu welcome message!

---

### Step 3: Setup Environment (3 minutes)

**Copy and paste these commands one by one:**

```bash
# Update system
sudo apt-get update -y

# Install Python and tools
sudo apt-get install python3 python3-pip python3-venv git -y

# Verify installation
python3 --version
```

---

### Step 4: Upload Project to EC2 (5 minutes)

**Option A: Using Git (Recommended)**

If you've pushed your code to GitHub:
```bash
git clone https://github.com/YOUR_USERNAME/house-price-prediction.git
cd house-price-prediction
```

**Option B: Using SCP (From your local machine)**

Open a NEW terminal on your LOCAL machine (not EC2):

```bash
# Windows (use Git Bash or WSL)
scp -i "ml-training-key.pem" -r "c:\Users\sv340\OneDrive\Desktop\aws project\house-price-prediction" ubuntu@YOUR_EC2_IP:~

# Mac/Linux
scp -i "ml-training-key.pem" -r "/path/to/house-price-prediction" ubuntu@YOUR_EC2_IP:~
```

Then back on EC2:
```bash
cd house-price-prediction
```

**Option C: Manual Upload (Easiest for beginners)**

1. Zip your project folder on your laptop
2. Use FileZilla or WinSCP to upload
3. Unzip on EC2:
```bash
sudo apt-get install unzip -y
unzip house-price-prediction.zip
cd house-price-prediction
```

---

### Step 5: Install Dependencies (3 minutes)

```bash
# Install Python packages
pip3 install -r requirements.txt

# This will take 2-3 minutes
# You'll see packages being installed
```

---

### Step 6: Generate Data on AWS (1 minute)

```bash
# Generate synthetic dataset
python3 data/generate_data.py
```

**Expected Output:**
```
✓ Dataset generated successfully!
✓ Saved to: data/raw/house_data.csv
Dataset Info:
  Samples: 1000
  Features: 5
```

---

### Step 7: Train Model on AWS (5 minutes)

```bash
# Run the complete ML pipeline
python3 run_pipeline.py
```

**Expected Output:**
```
==================================================
DATA CLEANING PIPELINE
==================================================
Dataset loaded: 1000 rows, 6 columns
...

==================================================
FEATURE ENGINEERING PIPELINE
==================================================
...

==================================================
MODEL TRAINING
==================================================
Training Linear Regression...
✓ Linear Regression trained successfully

Training Random Forest...
✓ Random Forest trained successfully

Training Gradient Boosting...
✓ Gradient Boosting trained successfully

==================================================
MODEL EVALUATION
==================================================

Linear Regression:
  RMSE: $45,234.56
  MAE:  $34,567.89
  R²:   0.9234

Random Forest:
  RMSE: $35,123.45
  MAE:  $25,678.90
  R²:   0.9512

Gradient Boosting:
  RMSE: $30,456.78
  MAE:  $22,345.67
  R²:   0.9678

==================================================
BEST MODEL: Gradient Boosting
R² Score: 0.9678
==================================================

Model saved to: models/house_price_model.pkl
```

**🎉 Your model is now trained on AWS!**

---

### Step 8: Start Web Application (2 minutes)

```bash
# Navigate to app directory
cd app

# Start Flask app
python3 app.py
```

**Expected Output:**
```
✓ Model loaded successfully
✓ Scaler loaded successfully
✓ Feature names loaded successfully
 * Running on http://0.0.0.0:5000
```

---

### Step 9: Access Your Application (1 minute)

1. Open your web browser
2. Go to: `http://YOUR_EC2_PUBLIC_IP:5000`
3. You should see the House Price Predictor!

**Test it:**
- Area: 1800
- Bedrooms: 3
- Bathrooms: 2
- Age: 10
- Location Score: 7.5

Click "Predict Price" → See the result!

**🎊 Congratulations! You've trained and deployed on AWS!**

---

## 🔧 Keep App Running (Production Setup)

The app stops when you close the terminal. To keep it running:

### Option 1: Background Process (Quick)

```bash
# Stop current app (Ctrl+C)

# Run in background
cd ~/house-price-prediction/app
nohup python3 app.py > app.log 2>&1 &

# Check if running
ps aux | grep app.py

# View logs
tail -f app.log
```

### Option 2: Systemd Service (Professional)

```bash
# Create service file
sudo nano /etc/systemd/system/house-price-app.service
```

**Paste this content:**
```ini
[Unit]
Description=House Price Prediction Flask App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/house-price-prediction/app
ExecStart=/usr/bin/python3 app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

**Save:** Press `Ctrl+X`, then `Y`, then `Enter`

**Start the service:**
```bash
sudo systemctl daemon-reload
sudo systemctl start house-price-app
sudo systemctl enable house-price-app

# Check status
sudo systemctl status house-price-app

# View logs
sudo journalctl -u house-price-app -f
```

**Now your app runs automatically even after reboot!**

---

## 💾 Optional: Backup Models to S3

```bash
# Configure AWS CLI
aws configure
# Enter your Access Key ID
# Enter your Secret Access Key
# Region: us-east-1
# Format: json

# Upload models to S3
python3 s3_integration.py upload
```

---

## 🎯 Complete Workflow Summary

```
1. Launch EC2 (t2.micro) ✅
2. Connect via SSH ✅
3. Install Python & dependencies ✅
4. Upload project code ✅
5. Generate dataset on AWS ✅
6. Train model on AWS ✅
7. Start Flask app ✅
8. Access via browser ✅
```

**Total Time:** 30 minutes
**Total Cost:** $0 (Free Tier)

---

## 📊 What You've Accomplished

✅ Trained ML model on AWS (not on laptop)
✅ Deployed web application on cloud
✅ Accessible from anywhere via internet
✅ Running 24/7 (if using systemd)
✅ All within Free Tier limits

---

## 🔍 Verify Everything Works

### Check Model Files
```bash
ls -lh ~/house-price-prediction/models/
# Should show:
# - house_price_model.pkl
# - scaler.pkl
# - feature_names.pkl
```

### Check App Status
```bash
sudo systemctl status house-price-app
# Should show: Active: active (running)
```

### Test API
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"area": 1800, "bedrooms": 3, "bathrooms": 2, "age": 10, "location_score": 7.5}'
```

---

## 🛠️ Troubleshooting

### Issue: Can't connect to EC2
**Solution:**
- Check security group allows SSH (port 22)
- Verify instance is running
- Use correct key file
- Username must be `ubuntu`

### Issue: Out of memory during training
**Solution:**
```bash
# Use smaller dataset
# Edit data/generate_data.py
nano data/generate_data.py
# Change n_samples=1000 to n_samples=500
```

### Issue: App not accessible
**Solution:**
- Check security group allows port 5000
- Verify app is running: `ps aux | grep app.py`
- Check logs: `tail -f app.log`

### Issue: Dependencies fail to install
**Solution:**
```bash
# Update pip
pip3 install --upgrade pip

# Install one by one
pip3 install pandas numpy scikit-learn flask
```

---

## 💰 Cost Monitoring

### Check Free Tier Usage
1. AWS Console → Billing Dashboard
2. Click "Free Tier"
3. Monitor EC2 hours (750/month free)

### Set Billing Alert
1. Billing Dashboard → Billing Preferences
2. Enable "Receive Free Tier Usage Alerts"
3. Set threshold: $5

### Stop Instance When Not Using
```bash
# From AWS Console
EC2 → Instances → Select → Instance State → Stop

# Stopped instances don't count toward 750 hours!
```

---

## 🎓 What You Learned

✅ AWS EC2 instance management
✅ Linux server administration
✅ Remote ML model training
✅ Cloud deployment
✅ Service management
✅ Cost optimization

---

## 📝 Next Steps

### Immediate
- ✅ Test predictions thoroughly
- ✅ Share your live URL with friends
- ✅ Take screenshots for portfolio

### This Week
- 📝 Document your process
- 🐙 Push code to GitHub
- 💼 Add to resume/LinkedIn

### This Month
- 🎨 Customize the UI
- 📊 Add more features
- 🔐 Add authentication

---

## 🚀 Quick Commands Reference

```bash
# Connect to EC2
ssh -i "ml-training-key.pem" ubuntu@YOUR_EC2_IP

# Check app status
sudo systemctl status house-price-app

# Restart app
sudo systemctl restart house-price-app

# View logs
sudo journalctl -u house-price-app -f

# Stop EC2 (save costs)
# Do this from AWS Console

# Start EC2
# Do this from AWS Console
```

---

## ✅ Success Checklist

- [ ] EC2 instance launched (t2.micro)
- [ ] Connected via SSH
- [ ] Python and dependencies installed
- [ ] Project code uploaded
- [ ] Dataset generated on AWS
- [ ] Model trained on AWS (not laptop!)
- [ ] Flask app running
- [ ] Accessible via browser
- [ ] Predictions working
- [ ] App running as service (optional)
- [ ] Billing alerts set

---

## 🎉 Congratulations!

You've successfully:
- ✅ Trained ML model on AWS (no laptop training!)
- ✅ Deployed web application on cloud
- ✅ Made it accessible from anywhere
- ✅ Stayed within Free Tier ($0 cost)

**Your ML application is now live on the internet! 🌐**

---

## 📞 Need Help?

- Check logs: `sudo journalctl -u house-price-app -f`
- Review security groups in AWS Console
- Verify instance is running
- Check Free Tier usage

---

**🎊 You did it! Your ML model is trained and deployed on AWS! 🎊**

**Share your success:**
- Tweet: "Just trained my ML model on AWS! 🚀"
- LinkedIn: Post about your cloud ML project
- Portfolio: Add this project with live URL

**Your live app:** `http://YOUR_EC2_IP:5000`

---

**Time taken:** 30 minutes
**Cost:** $0
**Skills gained:** Cloud ML, AWS, Deployment
**Portfolio value:** High

**Happy cloud computing! ☁️🚀**
