#!/bin/bash

# AWS EC2 Deployment Script for House Price Prediction
# This script sets up the Flask application on an EC2 instance

echo "=========================================="
echo "House Price Prediction - AWS Deployment"
echo "=========================================="

# Update system
echo "Updating system packages..."
sudo apt-get update -y
sudo apt-get upgrade -y

# Install Python and pip
echo "Installing Python 3 and pip..."
sudo apt-get install python3 python3-pip -y

# Install git
echo "Installing Git..."
sudo apt-get install git -y

# Clone repository (replace with your GitHub repo URL)
echo "Cloning repository..."
# git clone https://github.com/YOUR_USERNAME/house-price-prediction.git
# cd house-price-prediction

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Generate sample data
echo "Generating sample dataset..."
python3 data/generate_data.py

# Run the ML pipeline
echo "Running ML pipeline..."
python3 run_pipeline.py

# Install and configure nginx (optional, for production)
echo "Installing nginx..."
sudo apt-get install nginx -y

# Create systemd service for Flask app
echo "Creating systemd service..."
sudo tee /etc/systemd/system/house-price-app.service > /dev/null <<EOF
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
EOF

# Start the service
echo "Starting Flask application service..."
sudo systemctl daemon-reload
sudo systemctl start house-price-app
sudo systemctl enable house-price-app

echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
echo "Access your app at: http://YOUR_EC2_PUBLIC_IP:5000"
echo ""
echo "To check service status: sudo systemctl status house-price-app"
echo "To view logs: sudo journalctl -u house-price-app -f"
