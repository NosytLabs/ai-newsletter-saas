#!/usr/bin/env python3
"""
Complete System Test
Tests all APIs and functionality
"""

import os
import sys
import logging
from datetime import datetime
from src.newsletter_system import AINewsletterSystem

def test_environment():
    """Test environment variables"""
    print('🔧 Testing Environment Variables...')
    
    required_vars = ['NEWSAPI_KEY', 'HF_TOKEN', 'KIT_API_KEY', 'WHOP_API_KEY']
    results = {}
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f'  ✅ {var}: Configured ({value[:10]}...)')
            results[var] = True
        else:
            print(f'  ❌ {var}: Missing')
            results[var] = False
    
    return results

def test_news_collection(system):
    """Test news collection functionality"""
    print('\n📰 Testing News Collection...')
    
    try:
        stories = system.collect_news()
        
        if stories:
            print(f'  ✅ Collected {len(stories)} stories')
            print(f'  📄 Top story: {stories[0]["title"][:60]}...')
            print(f'  🏆 Top score: {stories[0]["score"]}/10')
            return True
        else:
            print('  ❌ No stories collected')
            return False
            
    except Exception as e:
        print(f'  💥 Error: {e}')
        return False

def test_newsletter_generation(system):
    """Test newsletter generation"""
    print('\n🎨 Testing Newsletter Generation...')
    
    try:
        # Create mock stories for testing
        mock_stories = [
            {
                'title': 'OpenAI Announces Revolutionary AI Model',
                'summary': 'New breakthrough in artificial intelligence capabilities with significant business impact.',
                'url': 'https://example.com/story1',
                'source': 'TechCrunch',
                'score': 9.2
            },
            {
                'title': 'AI Startup Raises $100M Series B',
                'summary': 'Major funding round signals continued investor confidence in AI sector.',
                'url': 'https://example.com/story2',
                'source': 'VentureBeat',
                'score': 8.7
            }
        ]
        
        newsletter_html = system.generate_newsletter(mock_stories)
        
        if newsletter_html and len(newsletter_html) > 1000:
            print(f'  ✅ Newsletter generated ({len(newsletter_html):,} characters)')
            
            # Save test newsletter
            filename = f'test_newsletter_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(newsletter_html)
            
            print(f'  💾 Saved as: {filename}')
            return True
        else:
            print('  ❌ Newsletter generation failed')
            return False
            
    except Exception as e:
        print(f'  💥 Error: {e}')
        return False

def test_subscriber_stats(system):
    """Test subscriber statistics"""
    print('\n📊 Testing Subscriber Stats...')
    
    try:
        stats = system.get_subscriber_stats()
        
        print(f'  ✅ Total subscribers: {stats["total_subscribers"]}')
        print(f'  ✅ Active subscribers: {stats["active_subscribers"]}')
        print(f'  💰 Revenue potential: ${stats["revenue_potential"]:,.2f}/month')
        
        return True
        
    except Exception as e:
        print(f'  💥 Error: {e}')
        return False

def main():
    """Run complete system test"""
    print('🚀 NOSYT LABS AI NEWSLETTER SYSTEM TEST')
    print('=' * 50)
    
    # Test environment
    env_results = test_environment()
    env_passed = all(env_results.values())
    
    if not env_passed:
        print('\n❌ Environment test failed. Please set all required API keys.')
        print('\n📝 Required environment variables:')
        for var, passed in env_results.items():
            status = '✅' if passed else '❌'
            print(f'  {status} {var}')
        return False
    
    # Initialize system
    try:
        print('\n🔧 Initializing AI Newsletter System...')
        logging.basicConfig(level=logging.WARNING)  # Reduce noise
        system = AINewsletterSystem()
        print('  ✅ System initialized successfully')
    except Exception as e:
        print(f'  💥 System initialization failed: {e}')
        return False
    
    # Run tests
    tests = [
        ('News Collection', lambda: test_news_collection(system)),
        ('Newsletter Generation', lambda: test_newsletter_generation(system)),
        ('Subscriber Stats', lambda: test_subscriber_stats(system))
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f'  💥 {test_name} failed: {e}')
    
    # Results
    print('\n' + '=' * 50)
    print(f'🎯 TEST RESULTS: {passed}/{total} PASSED')
    
    if passed == total:
        print('\n🎉 ALL TESTS PASSED! SYSTEM IS FULLY FUNCTIONAL!')
        print('\n📋 Next Steps:')
        print('1. Set GitHub secrets for automation')
        print('2. Create Whop product for subscriptions')
        print('3. Deploy webhook endpoint (optional)')
        print('4. Launch marketing campaign')
        print('5. Start earning $19.99/month recurring revenue!')
        
        return True
    else:
        print('\n⚠️  Some tests failed. Please check configuration.')
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
