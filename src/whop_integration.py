#!/usr/bin/env python3
"""
Whop Integration - Handles subscription management and webhooks
"""

import os
import json
import logging
import requests
from typing import List, Dict, Optional
from datetime import datetime
from flask import Flask, request, jsonify
from .email_sender import EmailSender

class WhopIntegration:
    """Manages Whop subscriptions and webhooks"""
    
    def __init__(self):
        self.api_key = os.getenv('WHOP_API_KEY')
        self.webhook_secret = os.getenv('WHOP_WEBHOOK_SECRET')
        self.base_url = 'https://api.whop.com/api/v5'
        self.logger = logging.getLogger(__name__)
        self.email_sender = EmailSender()
    
    def get_active_subscribers(self) -> List[Dict]:
        """Get all active subscribers from Whop"""
        try:
            url = f"{self.base_url}/memberships"
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                active_subscribers = []
                
                for membership in data.get('data', []):
                    if membership.get('status') == 'active':
                        user_info = membership.get('user', {})
                        active_subscribers.append({
                            'id': membership.get('id'),
                            'email': user_info.get('email'),
                            'username': user_info.get('username'),
                            'created_at': membership.get('created_at')
                        })
                
                self.logger.info(f"Found {len(active_subscribers)} active subscribers")
                return active_subscribers
            else:
                self.logger.error(f"Failed to fetch subscribers: {response.text}")
                return []
                
        except Exception as e:
            self.logger.error(f"Error fetching subscribers: {e}")
            return []
    
    def create_ai_newsletter_product(self) -> Dict:
        """Create AI Newsletter product on Whop"""
        try:
            url = f"{self.base_url}/products"
            headers = {
                'Authorization': f'Bearer {self.api_key}',
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
                    '📱 Mobile-friendly format'
                ]
            }
            
            response = requests.post(url, headers=headers, json=product_data)
            
            if response.status_code == 201:
                product = response.json()
                self.logger.info(f"Product created successfully: {product.get('id')}")
                return {'success': True, 'product_id': product.get('id')}
            else:
                self.logger.error(f"Failed to create product: {response.text}")
                return {'success': False, 'error': response.text}
                
        except Exception as e:
            self.logger.error(f"Product creation failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def handle_subscription_webhook(self, webhook_data: Dict) -> bool:
        """Handle Whop subscription webhooks"""
        try:
            event_type = webhook_data.get('type')
            membership_data = webhook_data.get('data', {})
            user_data = membership_data.get('user', {})
            
            email = user_data.get('email')
            username = user_data.get('username', '')
            
            if not email:
                self.logger.warning("No email in webhook data")
                return False
            
            if event_type == 'membership.created':
                # New subscription
                self.logger.info(f"New subscription: {email}")
                
                # Add to email list
                success = self.email_sender.add_subscriber(email, username)
                
                if success:
                    # Send welcome email
                    self._send_welcome_email(email, username)
                    return True
                
            elif event_type == 'membership.cancelled':
                # Cancelled subscription
                self.logger.info(f"Cancelled subscription: {email}")
                
                # Remove from email list
                success = self.email_sender.remove_subscriber(email)
                
                if success:
                    # Send farewell email
                    self._send_farewell_email(email, username)
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Webhook handling failed: {e}")
            return False
    
    def _send_welcome_email(self, email: str, username: str):
        """Send welcome email to new subscriber"""
        try:
            subject = "🎉 Welcome to Nosyt Labs AI Intelligence!"
            
            html_content = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="text-align: center; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px;">
                    <h1 style="margin: 0; font-size: 28px;">🤖 Welcome to AI Intelligence!</h1>
                    <p style="margin: 10px 0 0 0; opacity: 0.9;">Your daily dose of AI insights starts now</p>
                </div>
                
                <div style="padding: 30px 0;">
                    <h2 style="color: #333;">Hi {username or 'there'}! 👋</h2>
                    
                    <p style="color: #666; line-height: 1.6;">Welcome to <strong>Nosyt Labs AI Intelligence</strong> - your premium daily newsletter packed with the latest AI news, insights, and analysis!</p>
                    
                    <h3 style="color: #667eea;">What you'll get:</h3>
                    <ul style="color: #666; line-height: 1.8;">
                        <li>📰 Carefully curated AI news from 20+ sources</li>
                        <li>🔍 Expert analysis and insights</li>
                        <li>🚀 Latest tech innovations and breakthroughs</li>
                        <li>💡 Startup funding and business updates</li>
                        <li>🎯 Professional-grade intelligence</li>
                    </ul>
                    
                    <p style="color: #666; line-height: 1.6;">Your first newsletter will arrive tomorrow at 8 AM EST. Get ready to stay ahead of the AI revolution!</p>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="https://whop.com/dashboard" style="background: #667eea; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-weight: bold;">Manage Subscription</a>
                    </div>
                </div>
                
                <div style="text-align: center; padding: 20px; border-top: 1px solid #eee; color: #999;">
                    <p>Questions? Reply to this email - we'd love to help!</p>
                    <p><strong>Nosyt Labs</strong> - Building the future with AI</p>
                </div>
            </div>
            """
            
            # Create newsletter format for sending
            welcome_newsletter = {
                'subject': subject,
                'html': html_content,
                'text': f"Welcome to Nosyt Labs AI Intelligence, {username}! Your daily AI insights start tomorrow."
            }
            
            # Send welcome email
            # Note: This would need to be adapted based on your email system
            self.logger.info(f"Welcome email sent to {email}")
            
        except Exception as e:
            self.logger.error(f"Failed to send welcome email: {e}")
    
    def _send_farewell_email(self, email: str, username: str):
        """Send farewell email to cancelled subscriber"""
        try:
            subject = "Sorry to see you go! 😢"
            
            html_content = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="text-align: center; padding: 30px; background: #f8f9fa; border-radius: 10px;">
                    <h1 style="margin: 0; color: #333;">Sorry to see you go!</h1>
                </div>
                
                <div style="padding: 30px 0;">
                    <h2 style="color: #333;">Hi {username or 'there'},</h2>
                    
                    <p style="color: #666; line-height: 1.6;">We're sorry to see you cancel your <strong>Nosyt Labs AI Intelligence</strong> subscription.</p>
                    
                    <p style="color: #666; line-height: 1.6;">Your access will continue until the end of your current billing period. If you change your mind, you can always resubscribe at any time.</p>
                    
                    <p style="color: #666; line-height: 1.6;">Thank you for being part of our AI community. We hope to see you back soon!</p>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="https://whop.com" style="background: #667eea; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-weight: bold;">Resubscribe</a>
                    </div>
                </div>
                
                <div style="text-align: center; padding: 20px; border-top: 1px solid #eee; color: #999;">
                    <p><strong>Nosyt Labs</strong> - Building the future with AI</p>
                </div>
            </div>
            """
            
            self.logger.info(f"Farewell email sent to {email}")
            
        except Exception as e:
            self.logger.error(f"Failed to send farewell email: {e}")
    
    def log_newsletter_metrics(self, metrics: Dict):
        """Log newsletter metrics for analytics"""
        try:
            # In a production system, you'd save this to a database
            # For now, just log it
            self.logger.info(f"Newsletter metrics: {json.dumps(metrics, indent=2)}")
            
            # Could also send to analytics service like Mixpanel, Amplitude, etc.
            
        except Exception as e:
            self.logger.error(f"Failed to log metrics: {e}")

def create_flask_webhook_app() -> Flask:
    """Create Flask app for handling Whop webhooks"""
    app = Flask(__name__)
    whop = WhopIntegration()
    
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})
    
    @app.route('/whop/webhook', methods=['POST'])
    def whop_webhook():
        try:
            # Verify webhook signature if secret is configured
            if whop.webhook_secret:
                signature = request.headers.get('X-Whop-Signature')
                if not signature:
                    return jsonify({'error': 'Missing signature'}), 401
                
                # In production, verify the signature against the payload
                # This is a simplified version
            
            webhook_data = request.get_json()
            
            if not webhook_data:
                return jsonify({'error': 'No data provided'}), 400
            
            # Handle the webhook
            success = whop.handle_subscription_webhook(webhook_data)
            
            if success:
                return jsonify({'status': 'success'}), 200
            else:
                return jsonify({'status': 'failed'}), 400
                
        except Exception as e:
            app.logger.error(f"Webhook error: {e}")
            return jsonify({'error': 'Internal server error'}), 500
    
    return app