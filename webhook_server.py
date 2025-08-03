#!/usr/bin/env python3
"""
Webhook Server for Whop Integration
Run this to handle subscription webhooks
"""

import os
import logging
from src.whop_integration import create_flask_webhook_app

def main():
    """Run webhook server"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    app = create_flask_webhook_app()
    
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    
    print(f'🚀 Starting Whop webhook server on {host}:{port}')
    print(f'🔗 Webhook endpoint: http://{host}:{port}/whop/webhook')
    print(f'❤️ Health check: http://{host}:{port}/health')
    
    app.run(host=host, port=port, debug=False)

if __name__ == '__main__':
    main()
