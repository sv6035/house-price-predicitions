# System Architecture - House Price Prediction

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                       │
│                          END USER                                     │
│                      (Web Browser)                                    │
│                                                                       │
└───────────────────────────┬───────────────────────────────────────┘
                            │
                            │ HTTP Request
                            │ (House Features)
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                                                                       │
│                      AWS CLOUD (Free Tier)                            │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                               │   │
│  │              AWS EC2 Instance (t2.micro)                      │   │
│  │                                                               │   │
│  │  ┌─────────────────────────────────────────────────────┐    │   │
│  │  │                                                       │    │   │
│  │  │           Flask Web Application                      │    │   │
│  │  │                                                       │    │   │
│  │  │  • Route Handlers (/predict, /api/predict)          │    │   │
│  │  │  • Input Validation                                  │    │   │
│  │  │  • HTML Template Rendering                           │    │   │
│  │  │                                                       │    │   │
│  │  └───────────────────┬───────────────────────────────────┘    │   │
│  │                      │                                         │   │
│  │                      ▼                                         │   │
│  │  ┌─────────────────────────────────────────────────────┐    │   │
│  │  │                                                       │    │   │
│  │  │         ML Prediction Pipeline                        │    │   │
│  │  │                                                       │    │   │
│  │  │  1. Load Model (house_price_model.pkl)              │    │   │
│  │  │  2. Load Scaler (scaler.pkl)                        │    │   │
│  │  │  3. Scale Input Features                             │    │   │
│  │  │  4. Make Prediction                                  │    │   │
│  │  │  5. Format Output                                    │    │   │
│  │  │                                                       │    │   │
│  │  └───────────────────┬───────────────────────────────────┘    │   │
│  │                      │                                         │   │
│  │                      │ Read/Write                              │   │
│  │                      ▼                                         │   │
│  │  ┌─────────────────────────────────────────────────────┐    │   │
│  │  │                                                       │    │   │
│  │  │          Local File System                            │    │   │
│  │  │                                                       │    │   │
│  │  │  • models/house_price_model.pkl                      │    │   │
│  │  │  • models/scaler.pkl                                 │    │   │
│  │  │  • models/feature_names.pkl                          │    │   │
│  │  │                                                       │    │   │
│  │  └───────────────────────────────────────────────────────┘    │   │
│  │                                                               │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                            │                                         │
│                            │ Boto3 SDK                               │
│                            │ (Optional)                              │
│                            ▼                                         │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                               │   │
│  │                  AWS S3 Bucket                                │   │
│  │          (house-price-prediction-models)                      │   │
│  │                                                               │   │
│  │  • models/house_price_model.pkl                              │   │
│  │  • models/scaler.pkl                                         │   │
│  │  • models/feature_names.pkl                                  │   │
│  │  • data/engineered_data.csv                                  │   │
│  │                                                               │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
┌──────────────┐
│   User Input │
│              │
│ • Area       │
│ • Bedrooms   │
│ • Bathrooms  │
│ • Age        │
│ • Location   │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│  Flask Backend   │
│                  │
│ 1. Receive POST  │
│ 2. Parse JSON    │
│ 3. Validate      │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Feature Scaling  │
│                  │
│ StandardScaler   │
│ Transform        │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  ML Model        │
│                  │
│ Random Forest/   │
│ Gradient Boost   │
│ Predict()        │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Format Output    │
│                  │
│ $XXX,XXX.XX      │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  Return to User  │
│                  │
│ JSON/HTML        │
└──────────────────┘
```

## ML Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   DATA SCIENCE PIPELINE                      │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐
│  Raw Data    │
│              │
│ house_data   │
│   .csv       │
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│  Data Cleaning       │
│                      │
│ • Handle Missing     │
│ • Remove Duplicates  │
│ • Remove Outliers    │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Feature Engineering  │
│                      │
│ • Create Features    │
│ • Encode Categorical │
│ • Scale Numerical    │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Train/Test Split    │
│                      │
│ 80% Train            │
│ 20% Test             │
└──────┬───────────────┘
       │
       ├─────────────────────────────────┐
       │                                 │
       ▼                                 ▼
┌──────────────┐              ┌──────────────────┐
│ Linear Reg   │              │  Random Forest   │
│              │              │                  │
│ Train        │              │  Train           │
│ Evaluate     │              │  Evaluate        │
└──────┬───────┘              └────────┬─────────┘
       │                               │
       │         ┌──────────────────┐  │
       │         │ Gradient Boost   │  │
       │         │                  │  │
       └────────▶│  Train           │◀─┘
                 │  Evaluate        │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Model Selection  │
                 │                  │
                 │ Best R² Score    │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │  Save Model      │
                 │                  │
                 │ .pkl files       │
                 └──────────────────┘
```

## Security Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS                       │
└─────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│  Layer 1: Network Security                               │
│                                                          │
│  • AWS Security Group                                    │
│    - Port 22 (SSH): Restricted to Admin IP              │
│    - Port 5000 (Flask): Open to 0.0.0.0/0               │
│    - Port 80 (HTTP): Open to 0.0.0.0/0                  │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│  Layer 2: Authentication & Authorization                 │
│                                                          │
│  • AWS IAM                                               │
│    - Separate IAM user (not root)                       │
│    - Minimal required permissions                        │
│    - Access keys for programmatic access                │
│                                                          │
│  • SSH Key Pair                                          │
│    - Private key authentication                          │
│    - No password login                                   │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│  Layer 3: Application Security                           │
│                                                          │
│  • Input Validation                                      │
│    - Type checking                                       │
│    - Range validation                                    │
│    - Error handling                                      │
│                                                          │
│  • No Sensitive Data Exposure                            │
│    - No credentials in code                              │
│    - Environment variables for secrets                   │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│  Layer 4: Data Security                                  │
│                                                          │
│  • S3 Bucket                                             │
│    - Private by default                                  │
│    - Block public access enabled                         │
│    - IAM-based access control                            │
└──────────────────────────────────────────────────────────┘
```

## Deployment Workflow

```
┌─────────────┐
│ Developer   │
│ Machine     │
└──────┬──────┘
       │
       │ 1. Code Development
       │
       ▼
┌─────────────┐
│   GitHub    │
│ Repository  │
└──────┬──────┘
       │
       │ 2. git push
       │
       ▼
┌─────────────────────────────────────┐
│        AWS EC2 Instance             │
│                                     │
│  3. git pull / scp                  │
│  4. pip install -r requirements.txt │
│  5. python run_pipeline.py          │
│  6. systemctl restart app           │
└─────────────────────────────────────┘
       │
       │ 7. Upload to S3 (optional)
       │
       ▼
┌─────────────┐
│  AWS S3     │
│  Bucket     │
└─────────────┘
```

## Cost Optimization Strategy

```
┌─────────────────────────────────────────────────────────┐
│              FREE TIER OPTIMIZATION                      │
└─────────────────────────────────────────────────────────┘

EC2 Instance (t2.micro)
├─ 750 hours/month FREE
├─ 1 vCPU, 1 GB RAM
└─ Strategy: Stop when not in use

S3 Storage
├─ 5 GB storage FREE
├─ 20,000 GET requests FREE
├─ 2,000 PUT requests FREE
└─ Strategy: Store only essential files

Data Transfer
├─ 15 GB outbound FREE
└─ Strategy: Optimize response sizes

Monitoring
├─ CloudWatch basic metrics FREE
└─ Set billing alerts at $5
```

## Scalability Considerations (Future)

```
Current (Free Tier)          Future (Paid)
─────────────────────        ──────────────────

Single EC2 Instance    →     Auto Scaling Group
                             (Multiple instances)

Local File Storage     →     EFS/S3 for shared storage

Manual Deployment      →     CI/CD Pipeline
                             (CodePipeline)

No Load Balancer       →     Application Load Balancer

HTTP                   →     HTTPS (ACM Certificate)

Single Region          →     Multi-Region Deployment
```

---

## Component Details

### EC2 Instance Specifications
- **Type**: t2.micro
- **vCPUs**: 1
- **Memory**: 1 GB
- **Storage**: 8 GB EBS (gp2)
- **Network**: Low to Moderate
- **Cost**: FREE (750 hours/month for 12 months)

### S3 Bucket Configuration
- **Storage Class**: Standard
- **Versioning**: Disabled (to save space)
- **Encryption**: Server-side (AES-256)
- **Public Access**: Blocked
- **Cost**: FREE (up to 5 GB)

### Flask Application
- **Framework**: Flask 2.3.3
- **Port**: 5000
- **Workers**: 1 (single-threaded)
- **Max Requests**: Unlimited
- **Timeout**: 30 seconds

### ML Model
- **Algorithm**: Random Forest / Gradient Boosting
- **Input Features**: 5 (area, bedrooms, bathrooms, age, location_score)
- **Output**: Single value (price prediction)
- **Model Size**: ~5-10 MB
- **Inference Time**: <100ms

---

This architecture is designed to:
✅ Stay within AWS Free Tier limits
✅ Provide reliable predictions
✅ Be easy to deploy and maintain
✅ Scale when needed (with paid services)
