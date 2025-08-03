#!/usr/bin/env python3
"""
Quick Setup - Input your API keys and test the system
"""

import os
import sys
import getpass
from datetime import datetime

def collect_api_keys():
    """Collect API keys interactively"""
    print("🔑 Enter your API keys from the previous conversation:")
    print("=" * 50)
    
    keys = {}
    
    print("\n1. NewsAPI Key (from newsapi.org):")
    keys['NEWSAPI_KEY'] = input("   Enter your NewsAPI key: ").strip()
    
    print("\n2. Hugging Face Token (from huggingface.co):")  
    keys['HF_TOKEN'] = input("   Enter your HF token: ").strip()
    
    print("\n3. Kit API Key (from kit.com):")
    keys['KIT_API_KEY'] = input("   Enter your Kit API key: ").strip()
    
    print("\n4. Whop API Key (from whop.com):")
    keys['WHOP_API_KEY'] = input("   Enter your Whop API key: ").strip()
    
    print("\n5. Whop Webhook Secret (any random string):")
    webhook_secret = input("   Enter webhook secret (or press Enter for auto-generated): ").strip()
    if not webhook_secret:
        import secrets
        webhook_secret = secrets.token_urlsafe(32)
        print(f"   Generated: {webhook_secret}")
    keys['WHOP_WEBHOOK_SECRET'] = webhook_secret
    
    return keys

def create_env_file(api_keys):
    """Create .env file with API keys"""
    env_content = f"""# AI Newsletter SaaS - Production Configuration
# Generated: {datetime.now().isoformat()}

# NewsAPI (newsapi.org) - Free tier: 1,000 requests/day
NEWSAPI_KEY={api_keys['NEWSAPI_KEY']}

# Hugging Face (huggingface.co) - Free tier: unlimited inference
HF_TOKEN={api_keys['HF_TOKEN']}

# Kit/ConvertKit (kit.com) - Free tier: 1,000 subscribers
KIT_API_KEY={api_keys['KIT_API_KEY']}

# Whop (whop.com) - For subscription management
WHOP_API_KEY={api_keys['WHOP_API_KEY']}

# Webhook secret for Whop integration
WHOP_WEBHOOK_SECRET={api_keys['WHOP_WEBHOOK_SECRET']}

# Additional configuration
FLASK_ENV=production
FLASK_DEBUG=False
NEWSLETTER_FROM_EMAIL=newsletter@nosytlabs.com
NEWSLETTER_FROM_NAME=Nosyt Labs AI Intelligence
COMPANY_NAME=Nosyt Labs
COMPANY_WEBSITE=https://nosytlabs.com
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env file created successfully!")

def test_api_connections(api_keys):
    """Test API connections"""
    print("\n🧪 Testing API connections...")
    
    # Test NewsAPI
    try:
        import requests
        response = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_keys['NEWSAPI_KEY']}")
        if response.status_code == 200:
            print("✅ NewsAPI: Working")
        else:
            print(f"❌ NewsAPI: Error {response.status_code}")
    except Exception as e:
        print(f"❌ NewsAPI: {e}")
    
    # Test Hugging Face
    try:
        from transformers import pipeline
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn", use_auth_token=api_keys['HF_TOKEN'])
        print("✅ Hugging Face: Working")
    except Exception as e:
        print(f"❌ Hugging Face: {e}")
    
    # Test Kit API
    try:
        response = requests.get(f"https://api.convertkit.com/v3/subscribers?api_key={api_keys['KIT_API_KEY']}")
        if response.status_code == 200:
            print("✅ Kit API: Working")
        else:
            print(f"❌ Kit API: Error {response.status_code}")
    except Exception as e:
        print(f"❌ Kit API: {e}")
    
    # Test Whop API
    try:
        headers = {'Authorization': f'Bearer {api_keys["WHOP_API_KEY"]}'}
        response = requests.get("https://api.whop.com/api/v5/memberships", headers=headers)
        if response.status_code == 200:
            print("✅ Whop API: Working")
        else:
            print(f"❌ Whop API: Error {response.status_code}")
    except Exception as e:
        print(f"❌ Whop API: {e}")

def run_full_test():
    """Run the full system test"""
    print("\n🚀 Running full system test...")
    try:
        os.system("python test_system.py")
    except Exception as e:
        print(f"Test failed: {e}")

def main():
    """Main setup function"""
    print("🤖 Nosyt Labs AI Newsletter SaaS - Quick Setup")
    print("=" * 50)
    print("Let's get your newsletter system running with the API keys")
    print("you provided in our previous conversation!")
    
    # Install dependencies
    print("\n📦 Installing dependencies...")
    os.system("pip install -r requirements.txt > /dev/null 2>&1")
    
    # Collect API keys
    api_keys = collect_api_keys()
    
    # Create .env file
    create_env_file(api_keys)
    
    # Test connections
    test_api_connections(api_keys)
    
    # Run full test
    run_full_test()
    
    print("\n🎉 Setup Complete!")
    print("\n📋 Next Steps:")
    print("1. Run: python create_product.py (create Whop product)")
    print("2. Add GitHub secrets for automation")
    print("3. Deploy webhook server: python webhook_server.py")
    print("4. Start earning $19.99/month! 💰")
    
    print(f"\n💡 Your newsletter will run automatically Mon-Fri at 8 AM EST")
    print(f"📊 Revenue potential: 100 subscribers = $1,999/month")

if __name__ == '__main__':
    main()