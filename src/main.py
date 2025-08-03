#!/usr/bin/env python3
"""
Main orchestrator for Nosyt Labs AI Newsletter
Combines news aggregation, newsletter generation, and email delivery
"""

import logging
import sys
import os
from datetime import datetime

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from news_aggregator import NewsAggregator
from newsletter_generator import NewsletterGenerator
from kit_email_manager import KitEmailManager
from whop_integration import WhopIntegration
from config import Config

class NewsletterOrchestrator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Validate configuration
        missing_config = Config.get_missing_config()
        if missing_config:
            self.logger.warning(f'Missing configuration: {", ".join(missing_config)}')
        
        # Initialize components
        self.news_aggregator = NewsAggregator()
        self.newsletter_generator = NewsletterGenerator()
        self.email_manager = KitEmailManager()
        self.whop_integration = WhopIntegration()
        
    def run_daily_newsletter(self):
        """Main function to generate and send daily newsletter"""
        try:
            self.logger.info(f'🤖 Starting {Config.NEWSLETTER_NAME} generation...')
            
            # Step 1: Collect news from all sources
            self.logger.info('📰 Collecting news from 20+ sources...')
            categorized_stories = self.news_aggregator.get_daily_stories()
            
            if not categorized_stories:
                self.logger.warning('❌ No stories collected. Skipping newsletter.')
                return False
            
            total_stories = sum(len(stories) for stories in categorized_stories.values())
            self.logger.info(f'✅ Collected {total_stories} stories across all categories')
            
            # Log story breakdown
            for category, stories in categorized_stories.items():
                if stories:
                    self.logger.info(f'  📊 {category}: {len(stories)} stories')
            
            # Step 2: Generate beautiful newsletter
            self.logger.info('🎨 Generating beautiful HTML newsletter...')
            newsletter_html = self.newsletter_generator.create_newsletter(categorized_stories)
            
            if not newsletter_html:
                self.logger.error('❌ Failed to generate newsletter HTML')
                return False
            
            # Step 3: Send to subscribers via Kit
            self.logger.info('📧 Sending newsletter to subscribers...')
            success = self.email_manager.send_newsletter(newsletter_html)
            
            if success:
                self.logger.info('✅ Newsletter sent successfully!')
                
                # Get stats
                stats = self.email_manager.get_subscriber_stats()
                self.logger.info(f'📊 Delivered to {stats["active_subscribers"]} active subscribers')
                
                return True
            else:
                self.logger.error('❌ Failed to send newsletter')
                return False
                
        except Exception as e:
            self.logger.error(f'💥 Error in newsletter generation: {e}')
            return False
    
    def test_system(self):
        """Test all system components"""
        self.logger.info(f'🧪 Testing {Config.NEWSLETTER_NAME} System...')
        
        # Test configuration
        self.logger.info('🔧 Testing configuration...')
        config_validation = Config.validate_config()
        for key, valid in config_validation.items():
            status = "✅" if valid else "❌"
            self.logger.info(f'  {status} {key}: {"configured" if valid else "missing"}')
        
        # Test news aggregation
        self.logger.info('📰 Testing news aggregation...')
        stories = self.news_aggregator.get_daily_stories()
        news_success = bool(stories)
        self.logger.info(f'  {"✅" if news_success else "❌"} News aggregation: {"working" if news_success else "failed"}')
        if news_success:
            total_stories = sum(len(v) for v in stories.values())
            self.logger.info(f'    📊 Collected {total_stories} stories')
        
        # Test newsletter generation
        newsletter_success = False
        if stories:
            self.logger.info('🎨 Testing newsletter generation...')
            newsletter = self.newsletter_generator.create_newsletter(stories)
            newsletter_success = bool(newsletter)
            self.logger.info(f'  {"✅" if newsletter_success else "❌"} Newsletter generation: {"working" if newsletter_success else "failed"}')
        
        # Test Kit integration
        self.logger.info('📧 Testing Kit email integration...')
        stats = self.email_manager.get_subscriber_stats()
        kit_success = bool(stats)
        self.logger.info(f'  {"✅" if kit_success else "❌"} Kit integration: {"working" if kit_success else "failed"}')
        if kit_success:
            self.logger.info(f'    👥 Current subscribers: {stats.get("total_subscribers", 0)}')
        
        # Test Whop integration
        self.logger.info('💰 Testing Whop integration...')
        whop_ready = self.whop_integration.create_whop_product()
        self.logger.info(f'  {"✅" if whop_ready else "❌"} Whop integration: {"ready" if whop_ready else "needs setup"}')
        
        # Overall system status
        overall_success = news_success and newsletter_success and kit_success
        self.logger.info(f'\n🎯 System test completed: {"✅ ALL SYSTEMS GO!" if overall_success else "❌ Some components need attention"}')
        
        return overall_success
    
    def preview_newsletter(self):
        """Generate and save newsletter preview without sending"""
        try:
            self.logger.info('👀 Generating newsletter preview...')
            
            # Collect news
            categorized_stories = self.news_aggregator.get_daily_stories()
            
            if not categorized_stories:
                self.logger.warning('No stories for preview')
                return False
            
            # Generate newsletter
            newsletter_html = self.newsletter_generator.create_newsletter(categorized_stories)
            
            # Save preview
            preview_filename = f'newsletter_preview_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
            with open(preview_filename, 'w', encoding='utf-8') as f:
                f.write(newsletter_html)
            
            self.logger.info(f'✅ Preview saved as: {preview_filename}')
            return True
            
        except Exception as e:
            self.logger.error(f'Error generating preview: {e}')
            return False

def main():
    """Main entry point"""
    # Setup logging
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL.upper()),
        format=Config.LOG_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('newsletter.log')
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f'🚀 {Config.NEWSLETTER_NAME} System Starting...')
    
    # Initialize orchestrator
    orchestrator = NewsletterOrchestrator()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'test':
            # Run system test
            success = orchestrator.test_system()
            sys.exit(0 if success else 1)
        elif command == 'preview':
            # Generate preview
            success = orchestrator.preview_newsletter()
            sys.exit(0 if success else 1)
        else:
            logger.error(f'Unknown command: {command}')
            logger.info('Available commands: test, preview')
            sys.exit(1)
    else:
        # Run daily newsletter
        success = orchestrator.run_daily_newsletter()
        sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
