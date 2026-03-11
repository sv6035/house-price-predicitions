# Quick Start Guide - House Price Prediction

Get your ML application running in 15 minutes!

---

## 🚀 Local Setup (5 minutes)

### Step 1: Clone and Install
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/house-price-prediction.git
cd house-price-prediction

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Generate Data and Train Model
```bash
# Generate sample dataset
python data/generate_data.py

# Run complete ML pipeline
python run_pipeline.py
```

Expected output:
```
✓ Dataset generated: 1000 samples
✓ Data cleaned
✓ Features engineered
✓ Models trained
✓ Best model: Gradient Boosting (R² = 0.97)
✓ Model saved
```

### Step 3: Run Web Application
```bash
# Start Flask app
cd app
python app.py
```

### Step 4: Test
Open browser: `http://localhost:5000`

Enter sample values:
- Area: 1800
- Bedrooms: 3
- Bathrooms: 2
- Age: 10
- Location Score: 7.5

Click "Predict Price" → See prediction!

---

## ☁️ AWS Deployment (10 minutes)

### Prerequisites
- AWS Account
- SSH client

### Step 1: Launch EC2 (3 minutes)
1. AWS Console → EC2 → Launch Instance
2. Choose:
   - **AMI**: Ubuntu 22.04 LTS
   - **Type**: t2.micro (Free Tier)
   - **Storage**: 8 GB
3. Security Group - Add rules:
   - SSH (22): My IP
   - Custom TCP (5000): 0.0.0.0/0
4. Create/download key pair
5. Launch!

### Step 2: Connect to EC2 (1 minute)
```bash
# Set key permissions (Mac/Linux)
chmod 400 your-key.pem

# Connect
ssh -i "your-key.pem" ubuntu@YOUR_EC2_IP
```

### Step 3: Setup Server (4 minutes)
```bash
# Update system
sudo apt-get update -y

# Install Python and Git
sudo apt-get install python3 python3-pip git -y

# Clone repository
git clone https://github.com/YOUR_USERNAME/house-price-prediction.git
cd house-price-prediction

# Install dependencies
pip3 install -r requirements.txt
```

### Step 4: Run Application (2 minutes)
```bash
# Generate data and train model
python3 data/generate_data.py
python3 run_pipeline.py

# Start Flask app
cd app
python3 app.py
```

### Step 5: Access Application
Open browser: `http://YOUR_EC2_IP:5000`

🎉 **Done!** Your ML app is live on AWS!

---

## 📝 Common Commands

### Local Development
```bash
# Activate environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Run pipeline
python run_pipeline.py

# Start app
cd app && python app.py

# Run tests
python src/evaluate_model.py
```

### AWS Management
```bash
# Connect to EC2
ssh -i "key.pem" ubuntu@EC2_IP

# Check app status
sudo systemctl status house-price-app

# View logs
sudo journalctl -u house-price-app -f

# Restart app
sudo systemctl restart house-price-app

# Stop EC2 (save costs)
aws ec2 stop-instances --instance-ids i-XXXXX
```

---

## 🔧 Troubleshooting

### Issue: "Module not found"
```bash
pip install -r requirements.txt
```

### Issue: "Port 5000 already in use"
```bash
# Find process
lsof -i :5000  # Mac/Linux
netstat -ano | findstr :5000  # Windows

# Kill process
kill -9 PID  # Mac/Linux
taskkill /PID PID /F  # Windows
```

### Issue: "Model not found"
```bash
# Ensure you ran the pipeline
python run_pipeline.py

# Check models directory
ls -la models/
```

### Issue: Can't access EC2 app
- Check security group allows port 5000
- Verify app is running: `ps aux | grep python`
- Check logs: `sudo journalctl -u house-price-app -f`

---

## 📊 Test the API

### Using curl
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "area": 1800,
    "bedrooms": 3,
    "bathrooms": 2,
    "age": 10,
    "location_score": 7.5
  }'
```

### Using Python
```python
import requests

url = "http://localhost:5000/api/predict"
data = {
    "area": 1800,
    "bedrooms": 3,
    "bathrooms": 2,
    "age": 10,
    "location_score": 7.5
}

response = requests.post(url, json=data)
print(response.json())
```

---

## 📚 Next Steps

1. ✅ **Customize Dataset**: Modify `data/generate_data.py`
2. ✅ **Add Features**: Update feature engineering
3. ✅ **Improve Model**: Try different algorithms
4. ✅ **Enhance UI**: Customize `templates/index.html`
5. ✅ **Setup S3**: Store models in cloud
6. ✅ **Add Monitoring**: CloudWatch metrics
7. ✅ **Setup Domain**: Point domain to EC2
8. ✅ **Enable HTTPS**: Use Let's Encrypt

---

## 💡 Pro Tips

1. **Save Costs**: Stop EC2 when not using
2. **Keep Updated**: `git pull` regularly
3. **Monitor Usage**: Check AWS Free Tier dashboard
4. **Backup Models**: Upload to S3 regularly
5. **Use Elastic IP**: Keep same IP address
6. **Enable Logging**: Track predictions and errors
7. **Version Models**: Save different model versions
8. **Test Locally**: Always test before deploying

---

## 📞 Need Help?

- 📖 Read full documentation: `README.md`
- 🏗️ Check architecture: `ARCHITECTURE.md`
- ☁️ AWS guide: `AWS_DEPLOYMENT_GUIDE.md`
- 🐛 Report issues: GitHub Issues
- 💬 Ask questions: GitHub Discussions

---

## ✅ Checklist

### Local Setup
- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Data generated
- [ ] Model trained
- [ ] App running locally
- [ ] Predictions working

### AWS Deployment
- [ ] AWS account created
- [ ] EC2 instance launched
- [ ] Security group configured
- [ ] Connected via SSH
- [ ] Code deployed
- [ ] Model trained on EC2
- [ ] App running on EC2
- [ ] Accessible via browser

### Optional
- [ ] S3 bucket created
- [ ] Models uploaded to S3
- [ ] Elastic IP allocated
- [ ] Domain configured
- [ ] Monitoring setup
- [ ] Billing alerts set

---

**🎊 Congratulations! You've built and deployed a complete ML system!**

Share your success:
- Tweet: "Just deployed my ML app on AWS! 🚀 #MachineLearning #AWS"
- LinkedIn: Post about your project
- GitHub: Star the repository
