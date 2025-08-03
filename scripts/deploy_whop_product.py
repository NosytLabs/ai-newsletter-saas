#!/usr/bin/env python3
"""
Whop Product Deployment Script
Creates the AI Newsletter product on Whop marketplace
"""

import requests
import json
import sys
import os
from datetime import datetime

class WhopProductDeployer:
    def __init__(self):
        self.api_key = os.getenv('WHOP_API_KEY')
        self.base_url = 'https://api.whop.com/api/v2'
        
        if not self.api_key:
            print('❌ WHOP_API_KEY environment variable not set')
            sys.exit(1)
            
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        # Product configuration
        self.product_config = {
            'name': 'Nosyt Labs Daily AI Intelligence',
            'description': '''🤖 **Premium AI Newsletter for Business Leaders**

Get comprehensive daily AI intelligence delivered to your inbox every weekday morning.

**What You'll Receive:**
• 📊 Executive Summary - AI-generated insights for strategic decision making
• 🔥 Breaking AI News - Top 4 most impactful developments  
• 💰 Funding & Deals - Latest investment trends and startup activity
• 🔬 Research Breakthroughs - Academic discoveries that matter to business
• 🏢 Enterprise Focus - Real-world AI implementation case studies
• ⚡ Developer Tools - New APIs, frameworks, and technical releases
• 🎯 Quick Bites - Additional noteworthy developments

**Why Choose Nosyt Labs:**
✅ **20+ Premium Sources** - From TechCrunch to MIT Tech Review
✅ **Global Business Focus** - International perspective on AI developments
✅ **Professional Analysis** - Business impact scoring for every story
✅ **Beautiful Design** - Modern, responsive email templates
✅ **Multiple Personas** - Content for executives, developers, investors, researchers

**Delivery Schedule:** Monday-Friday at 8:00 AM EST

**Target Audience:**
• Business Executives seeking competitive intelligence
• Developers tracking latest tools and breakthroughs  
• Investors monitoring market trends and opportunities
• Researchers following academic developments

*Join hundreds of business leaders staying ahead of the AI revolution.*''',
            'price': 19.99,
            'currency': 'USD',
            'billing_period': 'monthly',
            'category': 'newsletters',
            'tags': ['AI', 'Newsletter', 'Business Intelligence', 'Technology', 'Startups'],
            'features': [
                'Daily AI newsletter (Monday-Friday)',
                '20+ premium news sources',
                'Executive summaries and business insights',
                'Breaking news, funding deals, research updates',
                'Enterprise focus and developer tools coverage',
                'Beautiful HTML email design',
                'Business impact scoring',
                'Global AI market intelligence'
            ]
        }
    
    def create_product(self):
        """Create the AI Newsletter product on Whop"""
        print('🚀 Creating Nosyt Labs AI Newsletter product on Whop...')
        
        try:
            # Note: Whop's actual API endpoints may differ
            # This is a conceptual implementation
            url = f'{self.base_url}/products'
            
            payload = {
                'name': self.product_config['name'],
                'description': self.product_config['description'],
                'pricing': {
                    'type': 'recurring',
                    'amount': int(self.product_config['price'] * 100),  # cents
                    'currency': self.product_config['currency'],
                    'interval': 'month'
                },
                'category': self.product_config['category'],
                'tags': self.product_config['tags']
            }
            
            print(f'📡 Sending request to Whop API...')
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            
            if response.status_code in [200, 201]:
                product_data = response.json()
                product_id = product_data.get('id')
                
                print(f'✅ Product created successfully!')
                print(f'📦 Product ID: {product_id}')
                print(f'💰 Price: ${self.product_config["price"]}/month')
                print(f'🔗 Whop URL: https://whop.com/product/{product_id}')
                
                # Save product info
                self.save_product_info(product_data)
                
                return product_data
            else:
                print(f'❌ Failed to create product: {response.status_code}')
                print(f'Response: {response.text}')
                return None
                
        except Exception as e:
            print(f'💥 Error creating product: {e}')
            return None
    
    def save_product_info(self, product_data):
        """Save product information to file"""
        filename = f'whop_product_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        
        with open(filename, 'w') as f:
            json.dump(product_data, f, indent=2)
            
        print(f'💾 Product info saved to: {filename}')
    
    def setup_webhooks(self, product_id):
        """Setup webhooks for subscription events"""
        print('🔗 Setting up webhooks...')
        
        webhook_url = 'https://your-domain.com/whop/webhook'  # Update with actual URL
        
        webhook_config = {
            'url': webhook_url,
            'events': [
                'membership.created',
                'membership.cancelled',
                'membership.renewed'
            ]
        }
        
        try:
            url = f'{self.base_url}/webhooks'
            response = requests.post(url, headers=self.headers, json=webhook_config, timeout=30)
            
            if response.status_code in [200, 201]:
                webhook_data = response.json()
                print(f'✅ Webhooks configured successfully!')
                print(f'🔗 Webhook URL: {webhook_url}')
                return webhook_data
            else:
                print(f'❌ Failed to setup webhooks: {response.status_code}')
                return None
                
        except Exception as e:
            print(f'💥 Error setting up webhooks: {e}')
            return None
    
    def display_launch_checklist(self):
        """Display post-deployment checklist"""
        print('\n' + '='*60)
        print('🎯 WHOP PRODUCT LAUNCH CHECKLIST')
        print('='*60)
        print('\n📋 Manual Steps Required:')
        print('\n1. 🖼️  Upload Product Images:')
        print('   • Logo/icon for the product')
        print('   • Screenshot of newsletter design')
        print('   • Banner image for marketplace')
        print('\n2. 📝 Complete Product Details:')
        print('   • Add detailed FAQ section')
        print('   • Upload sample newsletter screenshots')
        print('   • Set up product categories and tags')
        print('\n3. 🔗 Configure Webhooks:')
        print('   • Set webhook URL to your deployed endpoint')
        print('   • Test webhook delivery')
        print('   • Verify subscription events')
        print('\n4. 💳 Payment Setup:')
        print('   • Connect Stripe account')
        print('   • Test payment flow')
        print('   • Configure tax settings')
        print('\n5. 📧 Email Integration:')
        print('   • Verify Kit API connection')
        print('   • Test welcome email flow')
        print('   • Set up subscriber management')
        print('\n6. 🚀 Launch Preparation:')
        print('   • Test end-to-end subscription flow')
        print('   • Verify newsletter delivery')
        print('   • Monitor system health')
        print('\n' + '='*60)
        print('🎉 Ready to launch your AI Newsletter SaaS!')
        print('='*60)
    
def main():
    """Main deployment function"""
    print('🤖 Nosyt Labs AI Newsletter - Whop Product Deployment')
    print('=' * 55)
    
    deployer = WhopProductDeployer()
    
    # Create product
    product_data = deployer.create_product()
    
    if product_data:
        product_id = product_data.get('id')
        
        # Setup webhooks
        if product_id:
            deployer.setup_webhooks(product_id)
        
        # Display checklist
        deployer.display_launch_checklist()
        
        print('\n🎯 Next Steps:')
        print('1. Complete manual setup steps above')
        print('2. Test the complete system')
        print('3. Launch marketing campaign')
        print('4. Monitor subscriber growth')
        
    else:
        print('❌ Product creation failed. Please check your API key and try again.')
        print('\n💡 Alternative: Create product manually at https://whop.com/dashboard/start')

if __name__ == '__main__':
    main()
