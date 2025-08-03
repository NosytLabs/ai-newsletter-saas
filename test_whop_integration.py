#!/usr/bin/env python3
"""
Test Whop Integration
Verify your Whop API keys and product creation
"""

import os
import sys
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

def test_whop_api():
    """Test Whop API connection"""
    load_dotenv()
    
    api_key = os.getenv('WHOP_API_KEY')
    if not api_key:
        print("❌ WHOP_API_KEY not found in .env file")
        return False
    
    print("🔧 Testing Whop API connection...")
    
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # Test API connection
        response = requests.get('https://api.whop.com/api/v5/memberships', headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Whop API connected successfully!")
            print(f"📊 Current memberships: {len(data.get('data', []))}")
            return True
        else:
            print(f"❌ Whop API error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Whop API connection failed: {e}")
        return False

def create_newsletter_product():
    """Create the AI Newsletter product on Whop"""
    load_dotenv()
    
    api_key = os.getenv('WHOP_API_KEY')
    
    print("\n🛒 Creating AI Newsletter product on Whop...")
    
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        product_data = {
            'name': 'Nosyt Labs Daily AI Intelligence',
            'description': '🤖 Get the latest AI news, insights, and analysis delivered to your inbox daily. Curated by experts, powered by AI.',
            'price': 1999,  # $19.99 in cents
            'currency': 'USD',
            'billing_period': 'monthly',
            'category': 'newsletter',
            'visibility': 'public',
            'tags': ['ai', 'newsletter', 'tech', 'intelligence', 'automation'],
            'features': [
                '📰 Daily AI news digest',
                '🔍 Expert analysis & insights',
                '🚀 Latest tech innovations',
                '💡 Startup & funding updates',
                '🎯 Curated for professionals',
                '📱 Mobile-friendly format',
                '🤖 AI-powered summaries',
                '⚡ Delivered at 8 AM EST',
                '🎨 Beautiful HTML design',
                '💬 Community access'
            ]
        }
        
        response = requests.post('https://api.whop.com/api/v5/products', 
                               headers=headers, 
                               json=product_data)
        
        if response.status_code == 201:
            product = response.json()
            product_id = product.get('id')
            print(f"✅ Product created successfully!")
            print(f"🆔 Product ID: {product_id}")
            print(f"💰 Price: $19.99/month")
            print(f"🔗 Product URL: https://whop.com/product/{product_id}")
            return product_id
        else:
            print(f"❌ Product creation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Product creation error: {e}")
        return None

def test_webhook_setup():
    """Test webhook configuration"""
    webhook_secret = os.getenv('WHOP_WEBHOOK_SECRET')
    
    print(f"\n🔗 Webhook Configuration:")
    print(f"Secret configured: {'✅' if webhook_secret else '❌'}")
    
    if webhook_secret:
        print(f"Secret: {webhook_secret[:10]}...")
        print(f"Webhook URL: https://your-domain.com/whop/webhook")
        print(f"📝 Add this webhook URL to your Whop dashboard")
    else:
        print("❌ Please set WHOP_WEBHOOK_SECRET in .env file")

def simulate_webhook_test():
    """Simulate a webhook payload for testing"""
    print(f"\n🧪 Webhook Test Payload:")
    
    test_payload = {
        "type": "membership.created",
        "data": {
            "id": "mem_test123",
            "status": "active",
            "user": {
                "email": "test@example.com",
                "username": "testuser"
            },
            "created_at": datetime.now().isoformat()
        }
    }
    
    print(json.dumps(test_payload, indent=2))
    
    # Test webhook handling
    try:
        from src.whop_integration import WhopIntegration
        whop = WhopIntegration()
        result = whop.handle_subscription_webhook(test_payload)
        print(f"Webhook handling test: {'✅ Passed' if result else '❌ Failed'}")
    except Exception as e:
        print(f"Webhook test error: {e}")

def main():
    """Main test function"""
    print("🤖 Nosyt Labs - Whop Integration Test")
    print("=" * 40)
    
    # Test Whop API
    if not test_whop_api():
        print("\n❌ Whop API test failed. Please check your API key.")
        return False
    
    # Create product
    product_id = create_newsletter_product()
    
    # Test webhook setup
    test_webhook_setup()
    
    # Simulate webhook
    simulate_webhook_test()
    
    if product_id:
        print(f"\n🎉 Whop Integration Complete!")
        print(f"\n📋 Next Steps:")
        print(f"1. Visit: https://whop.com/product/{product_id}")
        print(f"2. Customize product description and images")
        print(f"3. Set up webhook URL in Whop dashboard")
        print(f"4. Publish your product")
        print(f"5. Start marketing to get subscribers!")
        print(f"\n💰 Ready to earn $19.99/month recurring revenue!")
        return True
    else:
        print(f"\n❌ Product creation failed. Please check your Whop API key.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)