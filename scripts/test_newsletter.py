#!/usr/bin/env python3
"""
Test Newsletter Generation
Run this to test newsletter generation without sending
"""

import os
import sys
import json
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from news_collector import NewsCollector
from newsletter_generator import NewsletterGenerator

def main():
    """Test newsletter generation"""
    print("🧪 Testing Newsletter Generation")
    print("=" * 40)
    
    # Load environment
    if os.path.exists('.env'):
        from dotenv import load_dotenv
        load_dotenv()
    
    try:
        # Test news collection
        print("📰 Testing news collection...")
        collector = NewsCollector()
        articles = collector.collect_daily_news()
        print(f"✅ Collected {len(articles)} articles")
        
        if not articles:
            print("⚠️ No articles collected. Check your RSS sources.")
            return
        
        # Test newsletter generation
        print("\n🤖 Testing newsletter generation...")
        generator = NewsletterGenerator()
        newsletter = generator.generate_newsletter(articles)
        print(f"✅ Newsletter generated: {newsletter['subject']}")
        
        # Save test outputs
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save raw articles
        with open(f'test_articles_{timestamp}.json', 'w') as f:
            json.dump(articles, f, indent=2, default=str)
        print(f"💾 Articles saved to test_articles_{timestamp}.json")
        
        # Save newsletter HTML
        with open(f'test_newsletter_{timestamp}.html', 'w') as f:
            f.write(newsletter['html'])
        print(f"💾 Newsletter HTML saved to test_newsletter_{timestamp}.html")
        
        # Save newsletter text
        with open(f'test_newsletter_{timestamp}.txt', 'w') as f:
            f.write(newsletter['text'])
        print(f"💾 Newsletter text saved to test_newsletter_{timestamp}.txt")
        
        print("\n🎉 Newsletter generation test completed successfully!")
        print(f"\n📊 Statistics:")
        print(f"   Articles collected: {len(articles)}")
        print(f"   Newsletter length: {len(newsletter['html'])} chars")
        print(f"   Subject: {newsletter['subject']}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)