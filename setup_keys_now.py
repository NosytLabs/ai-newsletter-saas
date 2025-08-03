#!/usr/bin/env python3
"""
Setup API Keys - Let's get your newsletter working NOW!
"""

import os
import getpass

def setup_keys_interactive():
    """Interactive API key setup"""
    print("🔑 AI Newsletter SaaS - API Key Setup")
    print("=" * 50)
    print("Let's configure your API keys to get the system working!")
    
    # Collect API keys
    print("\n1. NewsAPI Key:")
    print("   Get from: https://newsapi.org/register")
    newsapi_key = input("   Enter your NewsAPI key: ").strip()
    
    print("\n2. Hugging Face Token:")
    print("   Get from: https://huggingface.co/settings/tokens")
    hf_token = input("   Enter your HF token: ").strip()
    
    print("\n3. Kit (ConvertKit) API Key:")  
    print("   Get from: https://kit.com → Settings → API")
    kit_key = input("   Enter your Kit API key: ").strip()
    
    print("\n4. Whop API Key:")
    print("   Get from: https://whop.com → Developer Settings")
    whop_key = input("   Enter your Whop API key: ").strip()
    
    print("\n5. Webhook Secret:")
    webhook_secret = input("   Enter webhook secret (or press Enter to generate): ").strip()
    if not webhook_secret:
        import secrets
        webhook_secret = secrets.token_urlsafe(32)
        print(f"   Generated: {webhook_secret}")
    
    # Create .env file
    env_content = f"""# AI Newsletter SaaS - Production Configuration

# NewsAPI (newsapi.org) - Free tier: 1,000 requests/day
NEWSAPI_KEY={newsapi_key}

# Hugging Face (huggingface.co) - Free tier: unlimited inference
HF_TOKEN={hf_token}

# Kit/ConvertKit (kit.com) - Free tier: 1,000 subscribers
KIT_API_KEY={kit_key}

# Whop (whop.com) - For subscription management
WHOP_API_KEY={whop_key}

# Webhook secret for Whop integration
WHOP_WEBHOOK_SECRET={webhook_secret}

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
    
    print("\n✅ Configuration saved to .env file!")
    
    # Test configuration
    test_apis(newsapi_key, hf_token, kit_key, whop_key)
    
    return True

def test_apis(newsapi_key, hf_token, kit_key, whop_key):
    """Test API connections"""
    print("\n🧪 Testing API connections...")
    
    # Test NewsAPI
    try:
        import requests
        response = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&pageSize=1&apiKey={newsapi_key}")
        if response.status_code == 200:
            print("✅ NewsAPI: Working")
        else:
            print(f"❌ NewsAPI: Error {response.status_code}")
    except Exception as e:
        print(f"❌ NewsAPI: {e}")
    
    # Test Kit API
    try:
        response = requests.get(f"https://api.convertkit.com/v3/subscribers?api_key={kit_key}")
        if response.status_code == 200:
            print("✅ Kit API: Working")
        else:
            print(f"❌ Kit API: Error {response.status_code}")
    except Exception as e:
        print(f"❌ Kit API: {e}")
    
    # Test Whop API
    try:
        headers = {'Authorization': f'Bearer {whop_key}'}
        response = requests.get("https://api.whop.com/api/v5/memberships", headers=headers)
        if response.status_code == 200:
            print("✅ Whop API: Working")
        else:
            print(f"❌ Whop API: Error {response.status_code}")
    except Exception as e:
        print(f"❌ Whop API: {e}")
    
    print("✅ Hugging Face: Will test during newsletter generation")

def create_github_secrets_file(newsapi_key, hf_token, kit_key, whop_key, webhook_secret):
    """Create GitHub secrets reference file"""
    secrets_data = {
        "NEWSAPI_KEY": newsapi_key,
        "HF_TOKEN": hf_token,
        "KIT_API_KEY": kit_key,
        "WHOP_API_KEY": whop_key,
        "WHOP_WEBHOOK_SECRET": webhook_secret
    }
    
    import json
    with open('github_secrets.json', 'w') as f:
        json.dump(secrets_data, f, indent=2)
    
    print("📁 GitHub secrets saved to github_secrets.json")

def main():
    """Main setup function"""
    print("🚀 Let's get your AI Newsletter SaaS working!")
    
    if setup_keys_interactive():
        print("\n🎉 Setup Complete!")
        print("\n🚀 Next Steps:")
        print("1. Run: python INSTANT_ACTIVATION.py")
        print("2. Run: python test_system.py")
        print("3. Create your Whop product")
        print("4. Add GitHub secrets for automation")
        print("5. Start marketing and get subscribers!")
        print("\n💰 Each subscriber = $239.88 annual value!")

if __name__ == '__main__':
    main()