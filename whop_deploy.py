import os
import json
import logging
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from threading import Thread
import schedule
import time
from ai_newsletter_2025 import AIWhopNewsletter2025

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class WHOPWebhookServer:
    def __init__(self):
        self.newsletter_system = AIWhopNewsletter2025()
        self.setup_routes()
        
    def setup_routes(self):
        @app.route('/webhook/whop', methods=['POST'])
        def whop_webhook():
            """Handle WHOP webhook events"""
            try:
                data = request.get_json()
                event_type = data.get('type')
                
                if event_type == 'subscription.created':
                    self.handle_new_subscription(data)
                elif event_type == 'subscription.cancelled':
                    self.handle_subscription_cancelled(data)
                elif event_type == 'payment.success':
                    self.handle_payment_success(data)
                    
                return jsonify({'status': 'success'})
                
            except Exception as e:
                logger.error(f"Webhook error: {e}")
                return jsonify({'error': str(e)}), 500

        @app.route('/generate-newsletter', methods=['POST'])
        def generate_newsletter():
            """Manual newsletter generation endpoint"""
            try:
                result = self.newsletter_system.run_complete_setup()
                return jsonify(result)
            except Exception as e:
                logger.error(f"Newsletter generation error: {e}")
                return jsonify({'error': str(e)}), 500

        @app.route('/health', methods=['GET'])
        def health_check():
            """Health check endpoint"""
            return jsonify({
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'version': '2025.1.0'
            })

        @app.route('/daily-schedule', methods=['GET'])
        def daily_schedule():
            """Get daily schedule status"""
            return jsonify({
                'next_run': self.get_next_run_time(),
                'last_run': self.get_last_run_time(),
                'schedule_active': True
            })

    def handle_new_subscription(self, data):
        """Handle new WHOP subscription"""
        user_email = data.get('user', {}).get('email')
        subscription_id = data.get('subscription', {}).get('id')
        
        logger.info(f"New subscription: {user_email} - {subscription_id}")
        
        # Add to Kit email list
        # TODO: Implement Kit API integration
        
    def handle_subscription_cancelled(self, data):
        """Handle cancelled subscription"""
        user_email = data.get('user', {}).get('email')
        logger.info(f"Subscription cancelled: {user_email}")
        
    def handle_payment_success(self, data):
        """Handle successful payment"""
        user_email = data.get('user', {}).get('email')
        amount = data.get('payment', {}).get('amount')
        logger.info(f"Payment success: {user_email} - ${amount/100}")

    def get_next_run_time(self):
        """Calculate next daily run time"""
        now = datetime.now()
        next_run = now.replace(hour=8, minute=0, second=0, microsecond=0)
        if next_run <= now:
            next_run += timedelta(days=1)
        return next_run.isoformat()

    def get_last_run_time(self):
        """Get last run time from file"""
        try:
            with open('last_run.json', 'r') as f:
                data = json.load(f)
                return data.get('last_run')
        except:
            return None

    def save_last_run(self):
        """Save last run time"""
        with open('last_run.json', 'w') as f:
            json.dump({'last_run': datetime.now().isoformat()}, f)

    def run_daily_newsletter(self):
        """Run daily newsletter generation"""
        try:
            logger.info("🌅 Starting daily newsletter generation...")
            result = self.newsletter_system.run_complete_setup()
            
            # Save results
            self.save_last_run()
            
            logger.info(f"✅ Daily newsletter completed: {result.get('newsletter_file')}")
            
        except Exception as e:
            logger.error(f"Daily newsletter error: {e}")

    def start_scheduler(self):
        """Start daily scheduler"""
        schedule.every().day.at("08:00").do(self.run_daily_newsletter)
        
        while True:
            schedule.run_pending()
            time.sleep(60)

    def run(self):
        """Start the webhook server"""
        # Start scheduler in background
        scheduler_thread = Thread(target=self.start_scheduler, daemon=True)
        scheduler_thread.start()
        
        # Start Flask app
        app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    server = WHOPWebhookServer()
    server.run()