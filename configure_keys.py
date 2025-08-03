#!/usr/bin/env python3
"""
Configure API Keys for AI Newsletter SaaS
Use the keys from your previous conversation
"""

import os

def configure_api_keys():
    """Configure your API keys from previous conversation"""
    print("🔑 Configuring API Keys for AI Newsletter SaaS")
    print("=" * 50)
    
    # Since you mentioned you already provided keys in previous conversation,
    # please update these with your actual values:
    
    api_keys = {
        'NEWSAPI_KEY': input("Enter your NewsAPI key: ").strip(),
        'HF_TOKEN': input("Enter your Hugging Face token: ").strip(),
        'KIT_API_KEY': input("Enter your Kit API key: ").strip(),
        'WHOP_API_KEY': input("Enter your Whop API key: ").strip(),
    }
    
    # Generate webhook secret if not provided
    webhook_secret = input("Enter webhook secret (or press Enter to auto-generate): ").strip()
    if not webhook_secret:
        import secrets
        webhook_secret = secrets.token_urlsafe(32)
        print(f"Generated webhook secret: {webhook_secret}")
    
    api_keys['WHOP_WEBHOOK_SECRET'] = webhook_secret
    
    # Create .env file
    env_content = f"""# AI Newsletter SaaS - Production Configuration
# Generated on: {os.popen('date').read().strip()}

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
    
    print("\n✅ .env file created successfully!")
    print("📁 Configuration saved to .env")
    
    # Create GitHub secrets reference
    print("\n📋 GitHub Secrets to Add:")
    print("Go to GitHub repository → Settings → Secrets and variables → Actions")
    print("Add these secrets:")
    
    for key, value in api_keys.items():
        print(f"   {key}: {value[:8]}...")
    
    return True

def test_configuration():
    """Test the API configuration"""
    print("\n🧪 Testing API Configuration...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        # Check all keys are present
        required_keys = ['NEWSAPI_KEY', 'HF_TOKEN', 'KIT_API_KEY', 'WHOP_API_KEY', 'WHOP_WEBHOOK_SECRET']
        missing = []
        
        for key in required_keys:
            if not os.getenv(key):
                missing.append(key)
        
        if missing:
            print(f"❌ Missing keys: {', '.join(missing)}")
            return False
        else:
            print("✅ All API keys configured!")
            print("✅ Ready to run: python INSTANT_ACTIVATION.py")
            return True
            
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def main():
    """Main configuration function"""
    print("🤖 AI Newsletter SaaS - API Key Configuration")
    print("=" * 50)
    
    # Configure keys
    if configure_api_keys():
        # Test configuration
        if test_configuration():
            print("\n🎉 Configuration Complete!")
            print("\n🚀 Next Steps:")
            print("1. Run: python INSTANT_ACTIVATION.py")
            print("2. Create your Whop product")
            print("3. Add GitHub secrets for automation")
            print("4. Start marketing and get subscribers!")
            print("\n💰 Each subscriber = $239.88 annual value!")
            return True
    
    print("\n❌ Configuration incomplete")
    return False

if __name__ == '__main__':
    main()