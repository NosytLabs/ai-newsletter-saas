#!/usr/bin/env python3
"""
Whop Integration for Nosyt Labs AI Newsletter
Handles subscription events and webhook integration
"""

import requests
import logging
from datetime import datetime
from typing import Dict, Optional
import hashlib
import hmac
from flask import Flask, request, jsonify
import json
from config import Config

class WhopIntegration:
    def __init__(self):
        self.api_key = Config.WHOP_API_KEY
        self.webhook_secret = Config.WHOP_WEBHOOK_SECRET
        self.base_url = 'https://api.whop.com/api/v2'
        self.logger = logging.getLogger(__name__)
        
        if not self.api_key:
            self.logger.warning('Whop API key not configured')
            return
            
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def verify_webhook_signature(self, payload, signature):
        """Verify webhook signature from Whop"""
        try:
            expected_signature = hmac.new(
                self.webhook_secret.encode('utf-8'),
                payload.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            return hmac.compare_digest(f'sha256={expected_signature}', signature)
            
        except Exception as e:
            self.logger.error(f'Error verifying webhook signature: {e}')
            return False

    def get_membership_details(self, membership_id):
        """Get membership details from Whop"""
        if not self.api_key:
            return None
            
        try:
            url = f'{self.base_url}/memberships/{membership_id}'
            response = requests.get(url, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f'Failed to get membership {membership_id}: {response.text}')
                return None
                
        except Exception as e:
            self.logger.error(f'Error getting membership details: {e}')
            return None

    def handle_membership_created(self, webhook_data, kit_email_manager):
        """Handle new membership creation"""
        try:
            membership_id = webhook_data.get('id')
            user_email = webhook_data.get('user', {}).get('email')
            user_name = webhook_data.get('user', {}).get('username', '')
            
            if not user_email:
                self.logger.error('No email found in membership creation webhook')
                return False
            
            # Add subscriber to Kit
            success = kit_email_manager.add_subscriber(
                email=user_email,
                first_name=user_name,
                tags=['whop-subscriber', 'premium-member', 'active']
            )
            
            if success:
                self.logger.info(f'Successfully added new subscriber from Whop: {user_email}')
                
                # Send welcome email
                welcome_content = self._generate_welcome_email(user_name or 'AI Enthusiast')
                kit_email_manager.send_newsletter(welcome_content)
                
            return success
            
        except Exception as e:
            self.logger.error(f'Error handling membership creation: {e}')
            return False
    
    def _generate_welcome_email(self, user_name):
        """Generate welcome email HTML"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Welcome to {Config.NEWSLETTER_NAME}!</title>
</head>
<body style="font-family: Inter, Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
    <div style="background: linear-gradient(135deg, {Config.EMAIL_TEMPLATE_SETTINGS['primary_color']} 0%, {Config.EMAIL_TEMPLATE_SETTINGS['secondary_color']} 100%); color: white; padding: 30px; text-align: center; border-radius: 12px; margin-bottom: 30px;">
        <h1 style="margin: 0; font-size: 28px;">🤖 Welcome to {Config.COMPANY_NAME}!</h1>
        <p style="margin: 10px 0 0 0; opacity: 0.9;">Your Premium AI Intelligence Subscription</p>
    </div>
    
    <h2 style="color: #1e293b;">Dear {user_name},</h2>
    
    <p>Thank you for subscribing to <strong>{Config.NEWSLETTER_NAME}</strong> - your premium source for comprehensive AI business intelligence.</p>
    
    <h3 style="color: {Config.EMAIL_TEMPLATE_SETTINGS['primary_color']};">What You'll Receive:</h3>
    <ul style="color: {Config.EMAIL_TEMPLATE_SETTINGS['light_text_color']};">
        <li><strong>📊 Daily Intelligence Briefings</strong> - Comprehensive analysis of global AI developments</li>
        <li><strong>💰 Funding & Deal Flow</strong> - Latest investment trends and startup activity</li>
        <li><strong>🔬 Research Breakthroughs</strong> - Academic discoveries that matter to business</li>
        <li><strong>🏢 Enterprise Applications</strong> - Real-world AI implementation case studies</li>
        <li><strong>⚡ Developer Tools</strong> - New APIs, frameworks, and technical releases</li>
        <li><strong>⚖️ Regulatory Updates</strong> - Policy changes affecting AI businesses globally</li>
    </ul>
    
    <div style="background: #f8fafc; padding: 20px; border-radius: 8px; border-left: 4px solid {Config.EMAIL_TEMPLATE_SETTINGS['primary_color']}; margin: 20px 0;">
        <h3 style="margin-top: 0; color: #1e293b;">Your Newsletter Schedule:</h3>
        <p style="margin-bottom: 0;"><strong>{' & '.join(Config.NEWSLETTER_DAYS[:2])} - {Config.NEWSLETTER_DAYS[-1]}:</strong> Comprehensive daily briefings at {Config.NEWSLETTER_TIME}</p>
    </div>
    
    <p>Your first newsletter will arrive tomorrow morning. We're excited to keep you at the forefront of AI developments!</p>
    
    <div style="text-align: center; margin: 30px 0;">
        <a href="{Config.SUBSCRIPTION_URL}" style="background: linear-gradient(135deg, {Config.EMAIL_TEMPLATE_SETTINGS['accent_color']} 0%, #d97706 100%); color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 600;">Manage Subscription</a>
    </div>
    
    <p style="color: #64748b; font-size: 14px; border-top: 1px solid #e2e8f0; padding-top: 20px; margin-top: 30px;">Best regards,<br><strong>The {Config.COMPANY_NAME} Team</strong><br><br>Questions? Reply to this email or contact us at {Config.COMPANY_EMAIL}</p>
</body>
</html>
        """

    def handle_membership_cancelled(self, webhook_data, kit_email_manager):
        """Handle membership cancellation"""
        try:
            user_email = webhook_data.get('user', {}).get('email')
            
            if not user_email:
                self.logger.error('No email found in membership cancellation webhook')
                return False
            
            # Remove subscriber from Kit
            success = kit_email_manager.remove_subscriber(user_email)
            
            if success:
                self.logger.info(f'Successfully removed cancelled subscriber: {user_email}')
            
            return success
            
        except Exception as e:
            self.logger.error(f'Error handling membership cancellation: {e}')
            return False

    def create_whop_product(self):
        """Create AI Newsletter product on Whop"""
        try:
            # This would typically use Whop's product creation API
            # For now, return success as manual setup is required
            self.logger.info('Whop product setup - please create manually at whop.com')
            return True
            
        except Exception as e:
            self.logger.error(f'Error creating Whop product: {e}')
            return False

def create_webhook_app(whop_integration, kit_email_manager):
    """Create Flask app for handling webhooks"""
    app = Flask(__name__)
    
    @app.route('/whop/webhook', methods=['POST'])
    def handle_webhook():
        try:
            # Get webhook signature
            signature = request.headers.get('X-Whop-Signature', '')
            payload = request.get_data(as_text=True)
            
            # Verify signature
            if not whop_integration.verify_webhook_signature(payload, signature):
                return jsonify({'error': 'Invalid signature'}), 401
            
            # Parse webhook data
            webhook_data = request.json
            event_type = webhook_data.get('type')
            
            logging.info(f'Received webhook: {event_type}')
            
            # Handle different event types
            if event_type == 'membership.created':
                success = whop_integration.handle_membership_created(webhook_data, kit_email_manager)
            elif event_type == 'membership.cancelled':
                success = whop_integration.handle_membership_cancelled(webhook_data, kit_email_manager)
            else:
                logging.info(f'Unhandled webhook type: {event_type}')
                success = True
            
            if success:
                return jsonify({'status': 'success'}), 200
            else:
                return jsonify({'status': 'error'}), 500
                
        except Exception as e:
            logging.error(f'Error handling webhook: {e}')
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy', 
            'timestamp': datetime.now().isoformat(),
            'service': Config.NEWSLETTER_NAME
        })
    
    return app

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    from kit_email_manager import KitEmailManager
    
    whop = WhopIntegration()
    kit = KitEmailManager()
    
    app = create_webhook_app(whop, kit)
    app.run(host='0.0.0.0', port=5000, debug=True)
