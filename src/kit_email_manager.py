#!/usr/bin/env python3
"""
Kit Email Manager for Nosyt Labs AI Newsletter
Handles subscriber management and email delivery using Kit API
"""

import requests
import logging
from datetime import datetime
from typing import Dict, List, Optional
import json
import time
from config import Config

class KitEmailManager:
    def __init__(self):
        self.api_key = Config.KIT_API_KEY
        self.base_url = 'https://api.kit.com'
        self.logger = logging.getLogger(__name__)
        
        if not self.api_key:
            self.logger.warning('Kit API key not configured')
            return
            
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def get_subscribers(self):
        """Get all subscribers from Kit"""
        if not self.api_key:
            return []
            
        try:
            url = f'{self.base_url}/subscribers'
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            subscribers = data.get('subscribers', [])
            
            self.logger.info(f'Retrieved {len(subscribers)} subscribers')
            return subscribers
            
        except Exception as e:
            self.logger.error(f'Error getting subscribers: {e}')
            return []

    def add_subscriber(self, email, first_name='', tags=None):
        """Add new subscriber to Kit"""
        if not self.api_key:
            return False
            
        try:
            url = f'{self.base_url}/subscribers'
            
            payload = {
                'subscriber': {
                    'email': email,
                    'first_name': first_name,
                    'tags': tags or ['ai-newsletter', 'whop-subscriber']
                }
            }
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            
            if response.status_code == 201:
                self.logger.info(f'Successfully added subscriber: {email}')
                return True
            else:
                self.logger.warning(f'Failed to add subscriber {email}: {response.text}')
                return False
                
        except Exception as e:
            self.logger.error(f'Error adding subscriber {email}: {e}')
            return False

    def remove_subscriber(self, email):
        """Remove subscriber from Kit"""
        if not self.api_key:
            return False
            
        try:
            # First find the subscriber ID
            subscribers = self.get_subscribers()
            subscriber_id = None
            
            for sub in subscribers:
                if sub.get('email') == email:
                    subscriber_id = sub.get('id')
                    break
            
            if not subscriber_id:
                self.logger.warning(f'Subscriber {email} not found')
                return False
            
            url = f'{self.base_url}/subscribers/{subscriber_id}'
            response = requests.delete(url, headers=self.headers, timeout=30)
            
            if response.status_code == 204:
                self.logger.info(f'Successfully removed subscriber: {email}')
                return True
            else:
                self.logger.warning(f'Failed to remove subscriber {email}: {response.text}')
                return False
                
        except Exception as e:
            self.logger.error(f'Error removing subscriber {email}: {e}')
            return False

    def create_broadcast(self, subject, content, description=None):
        """Create a broadcast (newsletter) in Kit"""
        if not self.api_key:
            return None
            
        try:
            url = f'{self.base_url}/broadcasts'
            
            payload = {
                'broadcast': {
                    'subject': subject,
                    'content': content,
                    'description': description or f'{Config.NEWSLETTER_NAME} - {datetime.now().strftime("%B %d, %Y")}'
                }
            }
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            
            if response.status_code == 201:
                broadcast_data = response.json()
                broadcast_id = broadcast_data.get('broadcast', {}).get('id')
                self.logger.info(f'Successfully created broadcast: {broadcast_id}')
                return broadcast_id
            else:
                self.logger.error(f'Failed to create broadcast: {response.text}')
                return None
                
        except Exception as e:
            self.logger.error(f'Error creating broadcast: {e}')
            return None

    def send_broadcast(self, broadcast_id):
        """Send a broadcast to all subscribers"""
        if not self.api_key:
            return False
            
        try:
            url = f'{self.base_url}/broadcasts/{broadcast_id}/send'
            
            response = requests.post(url, headers=self.headers, timeout=30)
            
            if response.status_code == 204:
                self.logger.info(f'Successfully sent broadcast: {broadcast_id}')
                return True
            else:
                self.logger.error(f'Failed to send broadcast {broadcast_id}: {response.text}')
                return False
                
        except Exception as e:
            self.logger.error(f'Error sending broadcast {broadcast_id}: {e}')
            return False

    def send_newsletter(self, newsletter_html):
        """Main method to send newsletter to all subscribers"""
        if not self.api_key:
            self.logger.error('Kit API key not configured - cannot send newsletter')
            return False
            
        try:
            # Generate subject line
            current_date = datetime.now().strftime('%B %d, %Y')
            subject = f'🤖 Daily AI Intelligence - {current_date}'
            
            # Create broadcast
            broadcast_id = self.create_broadcast(subject, newsletter_html)
            
            if not broadcast_id:
                return False
            
            # Wait for broadcast to be ready
            time.sleep(2)
            
            # Send broadcast
            return self.send_broadcast(broadcast_id)
            
        except Exception as e:
            self.logger.error(f'Error sending newsletter: {e}')
            return False

    def get_subscriber_stats(self):
        """Get subscriber statistics"""
        if not self.api_key:
            return {'total_subscribers': 0, 'active_subscribers': 0, 'tags': {}}
            
        try:
            subscribers = self.get_subscribers()
            
            stats = {
                'total_subscribers': len(subscribers),
                'active_subscribers': len([s for s in subscribers if s.get('state') == 'active']),
                'tags': {}
            }
            
            # Count tags
            for subscriber in subscribers:
                for tag in subscriber.get('tags', []):
                    stats['tags'][tag] = stats['tags'].get(tag, 0) + 1
            
            self.logger.info(f'Subscriber stats: {stats["total_subscribers"]} total, {stats["active_subscribers"]} active')
            return stats
            
        except Exception as e:
            self.logger.error(f'Error getting subscriber stats: {e}')
            return {'total_subscribers': 0, 'active_subscribers': 0, 'tags': {}}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    email_manager = KitEmailManager()
    
    # Test getting subscribers
    stats = email_manager.get_subscriber_stats()
    print(f'Subscriber Stats: {stats}')
