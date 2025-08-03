#!/bin/bash

# AI Newsletter SaaS - Deployment Script
# Run this to deploy the system

set -e

echo "🚀 Deploying AI Newsletter SaaS..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please copy .env.example to .env and configure your API keys."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Test system
echo "🧪 Testing system..."
python test_system.py

if [ $? -ne 0 ]; then
    echo "❌ System test failed. Please check your configuration."
    exit 1
fi

# Create Whop product (optional)
echo "🛒 Creating Whop product..."
python create_product.py

# Start webhook server (if deploying)
if [ "$1" == "--webhook" ]; then
    echo "🔗 Starting webhook server..."
    python webhook_server.py &
    WEBHOOK_PID=$!
    echo "Webhook server started with PID: $WEBHOOK_PID"
fi

echo "✅ Deployment completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Set up GitHub secrets with your API keys"
echo "2. Publish your Whop product"
echo "3. Configure webhook URL in Whop dashboard"
echo "4. Monitor GitHub Actions for daily newsletter runs"
echo ""
echo "💰 Start earning $19.99/month recurring revenue!"

# Keep webhook server running if started
if [ "$1" == "--webhook" ]; then
    echo "Press Ctrl+C to stop webhook server"
    wait $WEBHOOK_PID
fi