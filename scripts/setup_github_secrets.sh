#!/bin/bash

# Setup GitHub Secrets for Nosyt Labs AI Newsletter SaaS
# Run this script to set up all required secrets for GitHub Actions

echo "🔐 Setting up GitHub Secrets for AI Newsletter SaaS"
echo "================================================="

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI not found. Please install it first:"
    echo "   https://cli.github.com/"
    exit 1
fi

# Check if user is logged in to GitHub CLI
if ! gh auth status &> /dev/null; then
    echo "❌ Please login to GitHub CLI first:"
    echo "   gh auth login"
    exit 1
fi

echo "✅ GitHub CLI is ready"
echo ""

# Function to set secret
set_secret() {
    local secret_name=$1
    local description=$2
    
    echo "Setting $secret_name..."
    echo "Description: $description"
    read -s -p "Enter value: " secret_value
    echo ""
    
    if [ -n "$secret_value" ]; then
        gh secret set "$secret_name" --body="$secret_value"
        echo "✅ $secret_name set successfully"
    else
        echo "❌ Empty value provided for $secret_name"
    fi
    echo ""
}

# Set all required secrets
echo "📝 Setting up API keys..."
echo ""

set_secret "NEWSAPI_KEY" "NewsAPI key from newsapi.org (free tier: 1,000 requests/day)"
set_secret "HF_TOKEN" "Hugging Face token from huggingface.co (free tier: unlimited inference)"
set_secret "KIT_API_KEY" "Kit (ConvertKit) API key from kit.com (free tier: 1,000 subscribers)"
set_secret "WHOP_API_KEY" "Whop API key from whop.com (for subscription management)"
set_secret "WHOP_WEBHOOK_SECRET" "Whop webhook secret for secure webhook verification"

echo "🎉 All secrets have been configured!"
echo ""
echo "📋 Next steps:"
echo "1. Verify secrets in GitHub: https://github.com/NosytLabs/ai-newsletter-saas/settings/secrets/actions"
echo "2. Test the system: python src/main.py test"
echo "3. Trigger manual workflow: https://github.com/NosytLabs/ai-newsletter-saas/actions"
echo "4. Set up Whop product at: https://whop.com/dashboard/start"
echo ""
echo "🚀 Your AI Newsletter SaaS is ready to launch!"
