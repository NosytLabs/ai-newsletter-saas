#!/usr/bin/env python3
"""
Create Whop Product
Run this script to create your AI Newsletter product on Whop
"""

import sys
import os
from src.whop_integration import WhopIntegration

def main():
    """Create Whop product"""
    try:
        # Load environment variables from .env if present
        if os.path.exists('.env'):
            from dotenv import load_dotenv
            load_dotenv()
        
        whop = WhopIntegration()
        result = whop.create_ai_newsletter_product()
        
        if result['success']:
            print('✅ Whop product created successfully!')
            return True
        else:
            print('📋 Follow manual setup instructions above')
            return False
            
    except Exception as e:
        print(f'❌ Error: {e}')
        print('\nMake sure to:')
        print('1. Set WHOP_API_KEY environment variable')
        print('2. Install requirements: pip install -r requirements.txt')
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
