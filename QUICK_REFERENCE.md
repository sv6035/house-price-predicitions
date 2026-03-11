# ⚡ Quick Reference - Train on AWS

## 🎯 Your Situation: Can't train on laptop → Train on AWS directly!

---

## 📋 30-Minute Checklist

### ☁️ AWS Setup (10 min)
- [ ] Login to AWS Console
- [ ] Launch EC2 t2.micro (Ubuntu 22.04)
- [ ] Create key pair (save .pem file!)
- [ ] Configure security group (ports 22, 80, 5000)
- [ ] Get public IP address

### 🔌 Connect & Setup (5 min)
- [ ] SSH into EC2: `ssh -i key.pem ubuntu@YOUR_IP`
- [ ] Update system: `sudo apt-get update -y`
- [ ] Install Python: `sudo apt-get install python3 python3-pip git -y`

### 📦 Upload & Install (5 min)
- [ ] Upload project via SCP/Git
- [ ] Navigate: `cd house-price-prediction`
- [ ] Install deps: `pip3 install -r requirements.txt`

### 🤖 Train Model (5 min)
- [ ] Generate data: `python3 data/generate_data.py`
- [ ] Train model: `python3 run_pipeline.py`
- [ ] Verify: `ls -lh models/*.pkl`

### 🌐 Deploy App (5 min)
- [ ] Start app: `cd app && python3 app.py`
- [ ] Access: `http://YOUR_EC2_IP:5000`
- [ ] Test prediction
- [ ] Setup systemd (optional)

---

## 🚀 Essential Commands

### Connect to EC2
```bash
ssh -i "ml-training-key.pem" ubuntu@YOUR_EC2_IP
```

### Quick Setup
```bash
sudo apt-get update -y
sudo apt-get install python3 python3-pip git -y
cd house-price-prediction
pip3 install -r requirements.txt
```

### Train Model
```bash
python3 data/generate_data.py
python3 run_pipeline.py
```

### Start App
```bash
cd app
python3 app.py
```

### Keep App Running
```bash
nohup python3 app.py > app.log 2>&1 &
```

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Can't connect | Check security group, verify key file |
| Out of memory | Use smaller dataset (500 samples) |
| Port in use | Kill process: `pkill -f app.py` |
| Module not found | Run: `pip3 install -r requirements.txt` |

---

## 💰 Cost Check

✅ EC2 t2.micro: FREE (750 hrs/month)
✅ S3 storage: FREE (5 GB)
✅ Data transfer: FREE (15 GB/month)

**Total: $0/month** (within Free Tier)

---

## 📞 Full Guide

For detailed instructions: **TRAIN_ON_AWS.md**

---

## ✅ Success = Model trained on AWS, App live on internet!

**Your URL:** `http://YOUR_EC2_IP:5000`
