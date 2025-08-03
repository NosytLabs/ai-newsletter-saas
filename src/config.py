#!/usr/bin/env python3
"""
Configuration settings for Nosyt Labs AI Newsletter
"""

import os
from typing import Dict, List

class Config:
    """Configuration class for the newsletter system"""
    
    # API Keys (from environment variables)
    NEWSAPI_KEY = os.getenv('NEWSAPI_KEY')
    HF_TOKEN = os.getenv('HF_TOKEN')
    KIT_API_KEY = os.getenv('KIT_API_KEY')
    WHOP_API_KEY = os.getenv('WHOP_API_KEY')
    WHOP_WEBHOOK_SECRET = os.getenv('WHOP_WEBHOOK_SECRET', 'default_secret')
    
    # Newsletter Settings
    NEWSLETTER_NAME = 'Nosyt Labs Daily AI Intelligence'
    COMPANY_NAME = 'Nosyt Labs'
    COMPANY_EMAIL = 'hello@nosytlabs.com'
    COMPANY_URL = 'https://nosytlabs.com'
    SUBSCRIPTION_URL = 'https://whop.com/nosytlabs'
    SUBSCRIPTION_PRICE = '$19.99/month'
    
    # Scheduling
    NEWSLETTER_TIME = '8:00 AM EST'
    NEWSLETTER_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    
    # Content Limits
    MAX_STORIES_PER_CATEGORY = {
        'breaking_news': 4,
        'funding_deals': 3,
        'research': 3,
        'enterprise': 3,
        'developer_tools': 3,
        'quick_bites': 6
    }
    
    # Business Impact Keywords
    BUSINESS_KEYWORDS = {
        'high_impact': [
            'funding', 'investment', 'acquisition', 'IPO', 'valuation', 'revenue',
            'enterprise', 'partnership', 'deal', 'contract', 'market', 'competition',
            'regulation', 'policy', 'breakthrough', 'launch', 'release'
        ],
        'medium_impact': [
            'research', 'study', 'development', 'tool', 'platform', 'service',
            'innovation', 'technology', 'application', 'implementation', 'adoption'
        ],
        'trending_tech': [
            'GPT', 'LLM', 'ChatGPT', 'Claude', 'Gemini', 'OpenAI', 'Anthropic',
            'machine learning', 'deep learning', 'neural network', 'transformer',
            'generative AI', 'AGI', 'automation', 'robotics', 'computer vision'
        ]
    }
    
    # Categorization Keywords
    CATEGORY_KEYWORDS = {
        'funding_deals': ['funding', 'investment', 'deal', 'acquisition', 'venture', 'seed', 'series'],
        'research': ['research', 'paper', 'study', 'arxiv', 'academic', 'university', 'breakthrough'],
        'enterprise': ['enterprise', 'business', 'corporate', 'company', 'industry', 'commercial'],
        'developer_tools': ['API', 'tool', 'framework', 'developer', 'code', 'open source', 'SDK'],
        'regulatory': ['regulation', 'policy', 'law', 'government', 'compliance', 'ethics']
    }
    
    # Email Template Settings
    EMAIL_TEMPLATE_SETTINGS = {
        'primary_color': '#2563eb',
        'secondary_color': '#7c3aed',
        'accent_color': '#f59e0b',
        'success_color': '#10b981',
        'text_color': '#1a1a1a',
        'light_text_color': '#475569',
        'background_gradient': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'font_family': 'Inter, -apple-system, BlinkMacSystemFont, sans-serif'
    }
    
    # Target Personas
    TARGET_PERSONAS = {
        'executives': {
            'title': 'Business Executives',
            'description': 'Strategic insights for competitive positioning and technology adoption decisions'
        },
        'developers': {
            'title': 'Developers',
            'description': 'Latest tools, frameworks, and technical breakthroughs to enhance projects'
        },
        'investors': {
            'title': 'Investors',
            'description': 'Market trends, funding activity, and emerging opportunities in AI space'
        },
        'researchers': {
            'title': 'Researchers',
            'description': 'Cutting-edge academic developments and methodology advances'
        }
    }
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    @classmethod
    def validate_config(cls) -> Dict[str, bool]:
        """Validate that all required configuration is present"""
        return {
            'newsapi_key': bool(cls.NEWSAPI_KEY),
            'hf_token': bool(cls.HF_TOKEN),
            'kit_api_key': bool(cls.KIT_API_KEY),
            'whop_api_key': bool(cls.WHOP_API_KEY)
        }
    
    @classmethod
    def get_missing_config(cls) -> List[str]:
        """Get list of missing configuration items"""
        validation = cls.validate_config()
        return [key for key, valid in validation.items() if not valid]

if __name__ == '__main__':
    # Test configuration validation
    missing = Config.get_missing_config()
    if missing:
        print(f'Missing configuration: {", ".join(missing)}')
    else:
        print('All configuration items present!')
