#!/usr/bin/env python3
"""
AI Newsletter System - Main Entry Point
Automated daily newsletter generation and delivery
"""

import os
import sys
import logging
from datetime import datetime
from typing import Dict, List

# Import modules
from .news_collector import NewsCollector
from .newsletter_generator import NewsletterGenerator
from .email_sender import EmailSender
from .whop_integration import WhopIntegration

def setup_logging():
    """Configure logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('newsletter.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

def load_environment():
    """Load environment variables"""
    if os.path.exists('.env'):
        from dotenv import load_dotenv
        load_dotenv()
    
    required_vars = [
        'NEWSAPI_KEY',
        'HF_TOKEN', 
        'KIT_API_KEY',
        'WHOP_API_KEY'
    ]
    
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        raise ValueError(f"Missing environment variables: {', '.join(missing)}")

def main():
    """Main newsletter generation process"""
    logger = setup_logging()
    logger.info("🚀 Starting AI Newsletter System")
    
    try:
        # Load environment
        load_environment()
        logger.info("✅ Environment loaded")
        
        # Initialize components
        news_collector = NewsCollector()
        newsletter_generator = NewsletterGenerator()
        email_sender = EmailSender()
        whop_integration = WhopIntegration()
        
        # Step 1: Collect news
        logger.info("📰 Collecting news from sources...")
        news_articles = news_collector.collect_daily_news()
        logger.info(f"✅ Collected {len(news_articles)} articles")
        
        # Step 2: Generate newsletter
        logger.info("🤖 Generating newsletter with AI...")
        newsletter_content = newsletter_generator.generate_newsletter(news_articles)
        logger.info("✅ Newsletter generated")
        
        # Step 3: Get active subscribers
        logger.info("👥 Getting active subscribers...")
        subscribers = whop_integration.get_active_subscribers()
        logger.info(f"✅ Found {len(subscribers)} active subscribers")
        
        # Step 4: Send newsletter
        if subscribers:
            logger.info("📧 Sending newsletter to subscribers...")
            result = email_sender.send_newsletter(newsletter_content, subscribers)
            logger.info(f"✅ Newsletter sent to {result['sent']} subscribers")
            
            if result['errors']:
                logger.warning(f"⚠️ {len(result['errors'])} send errors occurred")
        else:
            logger.info("ℹ️ No active subscribers found")
        
        # Step 5: Log metrics
        metrics = {
            'date': datetime.now().isoformat(),
            'articles_collected': len(news_articles),
            'subscribers_count': len(subscribers),
            'emails_sent': result.get('sent', 0) if subscribers else 0,
            'errors': len(result.get('errors', [])) if subscribers else 0
        }
        
        logger.info(f"📊 Daily metrics: {metrics}")
        
        # Save metrics for analytics
        whop_integration.log_newsletter_metrics(metrics)
        
        logger.info("🎉 Newsletter system completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Newsletter system failed: {str(e)}")
        logger.exception("Full error details:")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)