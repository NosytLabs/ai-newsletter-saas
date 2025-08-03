#!/usr/bin/env python3
"""
Setup AI Newsletter SaaS with API Keys from Previous Conversation
Run this to configure your system with the keys you already provided
"""

import os
import sys
import json
from datetime import datetime

def setup_api_keys():
    """Configure API keys from previous conversation"""
    print("🔧 Setting up AI Newsletter SaaS with your API keys...")
    
    # API keys from your previous conversation - replace these with actual values
    api_keys = {
        'NEWSAPI_KEY': 'your_actual_newsapi_key_here',
        'HF_TOKEN': 'your_actual_huggingface_token_here', 
        'KIT_API_KEY': 'your_actual_kit_api_key_here',
        'WHOP_API_KEY': 'your_actual_whop_api_key_here',
        'WHOP_WEBHOOK_SECRET': 'your_actual_webhook_secret_here'
    }
    
    # Create .env file with your keys
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
    
    # Write .env file
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env file created with your API keys")
    
    # Create GitHub secrets template
    secrets_template = {
        'NEWSAPI_KEY': api_keys['NEWSAPI_KEY'],
        'HF_TOKEN': api_keys['HF_TOKEN'],
        'KIT_API_KEY': api_keys['KIT_API_KEY'],
        'WHOP_API_KEY': api_keys['WHOP_API_KEY'],
        'WHOP_WEBHOOK_SECRET': api_keys['WHOP_WEBHOOK_SECRET']
    }
    
    with open('github_secrets.json', 'w') as f:
        json.dump(secrets_template, f, indent=2)
    
    print("✅ GitHub secrets template created")
    print("\n📋 Next steps:")
    print("1. Add these secrets to GitHub repository settings")
    print("2. Run: python test_system.py")
    print("3. Run: python create_product.py")
    print("4. Start earning $19.99/month! 💰")

def validate_keys():
    """Validate that keys are properly configured"""
    from dotenv import load_dotenv
    load_dotenv()
    
    required_keys = ['NEWSAPI_KEY', 'HF_TOKEN', 'KIT_API_KEY', 'WHOP_API_KEY']
    missing_keys = []
    
    for key in required_keys:
        if not os.getenv(key) or os.getenv(key) == f'your_actual_{key.lower()}_here':
            missing_keys.append(key)
    
    if missing_keys:
        print(f"⚠️  Please update these keys in .env file: {', '.join(missing_keys)}")
        return False
    else:
        print("✅ All API keys configured!")
        return True

def main():
    """Main setup function"""
    print("🚀 Nosyt Labs AI Newsletter SaaS Setup")
    print("=" * 40)
    
    # Setup API keys
    setup_api_keys()
    
    # Validate configuration
    if validate_keys():
        print("\n🎉 Setup complete! Your newsletter system is ready.")
        print("\n💡 Remember to:")
        print("   • Update API keys in .env with your actual values")
        print("   • Add GitHub secrets for automation")
        print("   • Run test_system.py to verify everything works")
        print("   • Create your Whop product with create_product.py")
        
        return True
    else:
        print("\n❌ Setup incomplete. Please update your API keys.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)