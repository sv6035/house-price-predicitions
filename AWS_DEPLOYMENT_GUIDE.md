# AWS Deployment Guide - House Price Prediction System

## Complete Step-by-Step AWS Deployment (Free Tier Only)

---

## Prerequisites

- AWS Account (Free Tier eligible)
- Basic knowledge of AWS Console
- SSH client (PuTTY for Windows, Terminal for Mac/Linux)
- GitHub account (optional, for code hosting)

---

## Part 1: AWS Account Setup

### 1.1 Create AWS Account
1. Go to https://aws.amazon.com
2. Click "Create an AWS Account"
3. Follow the registration process
4. Add payment method (required but won't be charged if staying in Free Tier)

### 1.2 Set Up Billing Alerts
1. Go to AWS Console → Billing Dashboard
2. Click "Billing Preferences"
3. Enable "Receive Free Tier Usage Alerts"
4. Enter your email address
5. Set alert threshold: $5

---

## Part 2: IAM User Setup (Security Best Practice)

### 2.1 Create IAM User
1. Go to AWS Console → IAM
2. Click "Users" → "Add users"
3. Username: `house-price-admin`
4. Access type: ✅ Programmatic access, ✅ AWS Management Console access
5. Set password
6. Click "Next: Permissions"

### 2.2 Attach Policies
Attach these policies:
- `AmazonEC2FullAccess`
- `AmazonS3FullAccess`

### 2.3 Save Credentials
- Download CSV with Access Key ID and Secret Access Key
- **IMPORTANT**: Store securely, never commit to Git

---

## Part 3: S3 Bucket Setup

### 3.1 Create S3 Bucket
1. Go to AWS Console → S3
2. Click "Create bucket"
3. **Bucket name**: `house-price-prediction-models-[YOUR-NAME]`
   - Must be globally unique
   - Use lowercase, no spaces
4. **Region**: us-east-1 (N. Virginia)
5. **Block Public Access**: Keep all enabled (for security)
6. Click "Create bucket"

### 3.2 Create Folder Structure
1. Open your bucket
2. Click "Create folder"
3. Create folders:
   - `models/`
   - `data/`

### 3.3 Upload Files (After Training)
```bash
# From your local machine
aws s3 cp models/house_price_model.pkl s3://YOUR-BUCKET-NAME/models/
aws s3 cp models/scaler.pkl s3://YOUR-BUCKET-NAME/models/
aws s3 cp models/feature_names.pkl s3://YOUR-BUCKET-NAME/models/
```

---

## Part 4: EC2 Instance Setup

### 4.1 Launch EC2 Instance

1. **Go to EC2 Dashboard**
   - AWS Console → EC2 → Launch Instance

2. **Name and Tags**
   - Name: `house-price-prediction-server`

3. **Choose AMI (Amazon Machine Image)**
   - Select: **Ubuntu Server 22.04 LTS (HVM), SSD Volume Type**
   - Architecture: 64-bit (x86)
   - ✅ Free tier eligible

4. **Choose Instance Type**
   - Select: **t2.micro** (1 vCPU, 1 GB RAM)
   - ✅ Free tier eligible: 750 hours/month

5. **Key Pair (Login)**
   - Click "Create new key pair"
   - Key pair name: `house-price-key`
   - Key pair type: RSA
   - Private key format: `.pem` (Linux/Mac) or `.ppk` (Windows/PuTTY)
   - Click "Create key pair"
   - **SAVE THE FILE** - you can't download it again!

6. **Network Settings**
   - Click "Edit"
   - **Security Group Name**: `house-price-sg`
   - **Description**: Security group for house price prediction app
   
   **Inbound Rules:**
   
   | Type | Protocol | Port | Source | Description |
   |------|----------|------|--------|-------------|
   | SSH | TCP | 22 | My IP | SSH access |
   | HTTP | TCP | 80 | 0.0.0.0/0 | HTTP access |
   | Custom TCP | TCP | 5000 | 0.0.0.0/0 | Flask app |

7. **Configure Storage**
   - Size: **8 GB** (Free Tier: up to 30 GB)
   - Volume Type: General Purpose SSD (gp2)

8. **Advanced Details**
   - Leave as default

9. **Launch Instance**
   - Click "Launch instance"
   - Wait for instance state: **Running**

### 4.2 Note Your Instance Details
- **Instance ID**: i-xxxxxxxxxxxxxxxxx
- **Public IPv4 address**: XX.XX.XX.XX (changes on restart)
- **Public IPv4 DNS**: ec2-XX-XX-XX-XX.compute-1.amazonaws.com

---

## Part 5: Connect to EC2 Instance

### 5.1 Windows Users (PuTTY)

**Convert .pem to .ppk:**
1. Download PuTTYgen
2. Load your .pem file
3. Click "Save private key"
4. Save as .ppk

**Connect:**
1. Open PuTTY
2. Host Name: `ubuntu@YOUR_EC2_PUBLIC_IP`
3. Port: 22
4. Connection → SSH → Auth → Browse for .ppk file
5. Click "Open"

### 5.2 Mac/Linux Users

```bash
# Set permissions
chmod 400 house-price-key.pem

# Connect
ssh -i "house-price-key.pem" ubuntu@YOUR_EC2_PUBLIC_IP
```

---

## Part 6: Server Setup

### 6.1 Update System
```bash
sudo apt-get update -y
sudo apt-get upgrade -y
```

### 6.2 Install Python and Dependencies
```bash
# Install Python 3 and pip
sudo apt-get install python3 python3-pip python3-venv -y

# Install Git
sudo apt-get install git -y

# Verify installations
python3 --version
pip3 --version
git --version
```

### 6.3 Clone Repository

**Option A: From GitHub**
```bash
cd ~
git clone https://github.com/YOUR_USERNAME/house-price-prediction.git
cd house-price-prediction
```

**Option B: Upload via SCP**
```bash
# From your local machine
scp -i "house-price-key.pem" -r house-price-prediction ubuntu@YOUR_EC2_PUBLIC_IP:~
```

### 6.4 Install Python Packages
```bash
cd ~/house-price-prediction
pip3 install -r requirements.txt
```

### 6.5 Configure AWS CLI (for S3 access)
```bash
# Install AWS CLI
sudo apt-get install awscli -y

# Configure
aws configure
```

Enter:
- AWS Access Key ID: [Your Access Key]
- AWS Secret Access Key: [Your Secret Key]
- Default region: us-east-1
- Default output format: json

---

## Part 7: Run the Application

### 7.1 Generate Data and Train Model
```bash
cd ~/house-price-prediction

# Generate dataset
python3 data/generate_data.py

# Run complete pipeline
python3 run_pipeline.py
```

### 7.2 Upload Models to S3 (Optional)
```bash
python3 s3_integration.py upload
```

### 7.3 Start Flask Application

**Option A: Direct Run (for testing)**
```bash
cd app
python3 app.py
```

**Option B: Background Process**
```bash
cd app
nohup python3 app.py > app.log 2>&1 &
```

**Option C: Production with systemd**
```bash
# Create service file
sudo nano /etc/systemd/system/house-price-app.service
```

Paste:
```ini
[Unit]
Description=House Price Prediction Flask App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/house-price-prediction/app
ExecStart=/usr/bin/python3 /home/ubuntu/house-price-prediction/app/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Save and exit (Ctrl+X, Y, Enter)

```bash
# Start service
sudo systemctl daemon-reload
sudo systemctl start house-price-app
sudo systemctl enable house-price-app

# Check status
sudo systemctl status house-price-app

# View logs
sudo journalctl -u house-price-app -f
```

---

## Part 8: Access Your Application

### 8.1 Open in Browser
```
http://YOUR_EC2_PUBLIC_IP:5000
```

### 8.2 Test API
```bash
curl -X POST http://YOUR_EC2_PUBLIC_IP:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "area": 1800,
    "bedrooms": 3,
    "bathrooms": 2,
    "age": 10,
    "location_score": 7.5
  }'
```

---

## Part 9: Optional - Setup Domain Name

### 9.1 Allocate Elastic IP (to keep IP static)
1. EC2 → Elastic IPs → Allocate Elastic IP address
2. Select the new IP → Actions → Associate Elastic IP address
3. Select your instance
4. Now your IP won't change on restart

**⚠️ Warning**: Elastic IPs are free when associated with a running instance, but charged when not in use!

### 9.2 Configure Domain (if you have one)
1. Go to your domain registrar
2. Add A record pointing to your Elastic IP
3. Access via: `http://yourdomain.com:5000`

---

## Part 10: Monitoring and Maintenance

### 10.1 Check Application Status
```bash
# Check if app is running
sudo systemctl status house-price-app

# View recent logs
sudo journalctl -u house-price-app -n 50

# Follow logs in real-time
sudo journalctl -u house-price-app -f
```

### 10.2 Restart Application
```bash
sudo systemctl restart house-price-app
```

### 10.3 Update Application
```bash
cd ~/house-price-prediction
git pull origin main
sudo systemctl restart house-price-app
```

### 10.4 Monitor AWS Costs
1. AWS Console → Billing Dashboard
2. Check "Free Tier Usage"
3. Review "Cost Explorer"

---

## Part 11: Troubleshooting

### Issue: Can't connect to EC2
**Solution:**
- Check security group allows SSH (port 22) from your IP
- Verify instance is running
- Check you're using correct key file
- Verify username is `ubuntu`

### Issue: Can't access web app
**Solution:**
- Check security group allows port 5000
- Verify Flask app is running: `sudo systemctl status house-price-app`
- Check logs: `sudo journalctl -u house-price-app -f`
- Test locally: `curl http://localhost:5000`

### Issue: Model not found
**Solution:**
- Ensure you ran `python3 run_pipeline.py`
- Check models directory: `ls -la ~/house-price-prediction/models/`
- Verify file paths in app.py

### Issue: S3 access denied
**Solution:**
- Check AWS credentials: `aws configure list`
- Verify IAM user has S3 permissions
- Check bucket name is correct

---

## Part 12: Cost Optimization

### Free Tier Limits (12 months)
- **EC2**: 750 hours/month of t2.micro
- **S3**: 5 GB storage, 20,000 GET, 2,000 PUT requests
- **Data Transfer**: 15 GB/month outbound

### Tips to Stay Free
1. ✅ Use only t2.micro instances
2. ✅ Stop instance when not in use (doesn't count toward 750 hours)
3. ✅ Keep S3 storage under 5 GB
4. ✅ Delete old snapshots and AMIs
5. ✅ Set up billing alerts
6. ⚠️ Release Elastic IPs if not using

### Stop Instance (when not needed)
```bash
# From AWS Console
EC2 → Instances → Select instance → Instance state → Stop

# Or via CLI
aws ec2 stop-instances --instance-ids i-XXXXXXXXXXXXXXXXX
```

### Start Instance
```bash
# From AWS Console
EC2 → Instances → Select instance → Instance state → Start

# Note: Public IP will change (unless using Elastic IP)
```

---

## Part 13: Cleanup (When Done)

### 13.1 Terminate EC2 Instance
1. EC2 → Instances
2. Select instance
3. Instance state → Terminate instance

### 13.2 Delete S3 Bucket
1. S3 → Select bucket
2. Empty bucket (delete all files)
3. Delete bucket

### 13.3 Release Elastic IP (if allocated)
1. EC2 → Elastic IPs
2. Select IP → Actions → Release Elastic IP address

### 13.4 Delete Security Group
1. EC2 → Security Groups
2. Select `house-price-sg`
3. Actions → Delete security group

---

## Summary Checklist

- [ ] AWS account created with billing alerts
- [ ] IAM user created with proper permissions
- [ ] S3 bucket created
- [ ] EC2 instance launched (t2.micro)
- [ ] Security group configured (ports 22, 80, 5000)
- [ ] Connected to EC2 via SSH
- [ ] Python and dependencies installed
- [ ] Code deployed to EC2
- [ ] AWS CLI configured
- [ ] Model trained and saved
- [ ] Flask app running
- [ ] Application accessible via browser
- [ ] Monitoring setup

---

## Support

If you encounter issues:
1. Check AWS documentation: https://docs.aws.amazon.com
2. Review application logs
3. Verify Free Tier usage
4. Open GitHub issue

---

**🎉 Congratulations! Your ML application is now live on AWS!**
