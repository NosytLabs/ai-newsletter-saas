#!/usr/bin/env python3
"""
Email Sender - Handles newsletter delivery via Kit (ConvertKit)
"""

import os
import requests
import logging
from typing import List, Dict

class EmailSender:
    """Sends newsletters via Kit (ConvertKit)"""
    
    def __init__(self):
        self.kit_api_key = os.getenv('KIT_API_KEY')
        self.base_url = 'https://api.convertkit.com/v3'
        self.logger = logging.getLogger(__name__)
    
    def send_newsletter(self, newsletter: Dict, subscribers: List[Dict]) -> Dict:
        """Send newsletter to all subscribers"""
        try:
            # Create broadcast in Kit
            broadcast_id = self._create_broadcast(newsletter)
            
            if not broadcast_id:
                return {'sent': 0, 'errors': ['Failed to create broadcast']}
            
            # Send broadcast
            result = self._send_broadcast(broadcast_id)
            
            return {
                'sent': len(subscribers) if result else 0,
                'errors': [] if result else ['Failed to send broadcast'],
                'broadcast_id': broadcast_id
            }
            
        except Exception as e:
            self.logger.error(f"Newsletter sending failed: {e}")
            return {'sent': 0, 'errors': [str(e)]}
    
    def _create_broadcast(self, newsletter: Dict) -> str:
        """Create broadcast in Kit"""
        try:
            url = f"{self.base_url}/broadcasts"
            
            data = {
                'api_key': self.kit_api_key,
                'content': newsletter['html'],
                'description': newsletter['subject'],
                'subject': newsletter['subject'],
                'send_at': None  # Send immediately
            }
            
            response = requests.post(url, json=data)
            
            if response.status_code == 201:
                broadcast_data = response.json()
                return str(broadcast_data['broadcast']['id'])
            else:
                self.logger.error(f"Failed to create broadcast: {response.text}")
                return None
                
        except Exception as e:
            self.logger.error(f"Broadcast creation failed: {e}")
            return None
    
    def _send_broadcast(self, broadcast_id: str) -> bool:
        """Send broadcast to subscribers"""
        try:
            url = f"{self.base_url}/broadcasts/{broadcast_id}/send"
            
            data = {
                'api_key': self.kit_api_key
            }
            
            response = requests.post(url, json=data)
            
            if response.status_code == 204:
                self.logger.info(f"Broadcast {broadcast_id} sent successfully")
                return True
            else:
                self.logger.error(f"Failed to send broadcast: {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"Broadcast sending failed: {e}")
            return False
    
    def add_subscriber(self, email: str, first_name: str = '') -> bool:
        """Add subscriber to Kit"""
        try:
            url = f"{self.base_url}/subscribers"
            
            data = {
                'api_key': self.kit_api_key,
                'email': email,
                'first_name': first_name,
                'state': 'active'
            }
            
            response = requests.post(url, json=data)
            
            if response.status_code in [200, 201]:
                self.logger.info(f"Subscriber {email} added successfully")
                return True
            else:
                self.logger.error(f"Failed to add subscriber: {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"Subscriber addition failed: {e}")
            return False
    
    def remove_subscriber(self, email: str) -> bool:
        """Remove subscriber from Kit"""
        try:
            # First get subscriber ID
            subscriber_id = self._get_subscriber_id(email)
            if not subscriber_id:
                return False
            
            url = f"{self.base_url}/subscribers/{subscriber_id}/unsubscribe"
            
            data = {
                'api_key': self.kit_api_key
            }
            
            response = requests.put(url, json=data)
            
            if response.status_code == 200:
                self.logger.info(f"Subscriber {email} removed successfully")
                return True
            else:
                self.logger.error(f"Failed to remove subscriber: {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"Subscriber removal failed: {e}")
            return False
    
    def _get_subscriber_id(self, email: str) -> str:
        """Get Kit subscriber ID by email"""
        try:
            url = f"{self.base_url}/subscribers"
            params = {
                'api_key': self.kit_api_key,
                'email_address': email
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                subscribers = data.get('subscribers', [])
                if subscribers:
                    return str(subscribers[0]['id'])
            
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to get subscriber ID: {e}")
            return None