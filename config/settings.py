#!/usr/bin/env python3
"""
Configuration settings for AI Newsletter SaaS
"""

import os
from typing import Dict, List

class Config:
    """Application configuration"""
    
    # API Keys
    NEWSAPI_KEY = os.getenv('NEWSAPI_KEY')
    HF_TOKEN = os.getenv('HF_TOKEN')
    KIT_API_KEY = os.getenv('KIT_API_KEY')
    WHOP_API_KEY = os.getenv('WHOP_API_KEY')
    WHOP_WEBHOOK_SECRET = os.getenv('WHOP_WEBHOOK_SECRET')
    
    # Newsletter Configuration
    NEWSLETTER_SUBJECT_TEMPLATE = "Nosyt Labs AI Intelligence - {date}"
    MAX_ARTICLES_PER_NEWSLETTER = 20
    NEWSLETTER_SEND_TIME = "08:00"  # 8 AM EST
    
    # RSS Sources
    RSS_SOURCES = [
        'https://feeds.feedburner.com/venturebeat/SZYF',  # VentureBeat AI
        'https://rss.cnn.com/rss/edition.rss',  # CNN
        'https://techcrunch.com/feed/',  # TechCrunch
        'https://www.wired.com/feed/rss',  # Wired
        'https://www.theverge.com/rss/index.xml',  # The Verge
        'https://feeds.arstechnica.com/arstechnica/index',  # Ars Technica
        'https://rss.slashdot.org/Slashdot/slashdotMain',  # Slashdot
        'https://feeds.feedburner.com/AINews',  # AI News
        'https://blog.openai.com/rss/',  # OpenAI Blog
        'https://ai.googleblog.com/feeds/posts/default',  # Google AI Blog
        'https://blogs.microsoft.com/ai/feed/',  # Microsoft AI Blog
        'https://www.deepmind.com/blog/rss.xml',  # DeepMind
        'https://blog.anthropic.com/rss/',  # Anthropic
        'https://huggingface.co/blog/feed.xml',  # Hugging Face
        'https://openai.com/blog/rss/',  # OpenAI
        'https://stability.ai/blog/feed',  # Stability AI
        'https://www.nvidia.com/en-us/about-nvidia/ai-computing/rss/',  # NVIDIA AI
        'https://blog.tensorflow.org/feeds/posts/default',  # TensorFlow
        'https://pytorch.org/blog/feed.xml',  # PyTorch
        'https://machinelearningmastery.com/feed/'  # ML Mastery
    ]
    
    # AI Keywords for filtering
    AI_KEYWORDS = [
        'artificial intelligence', 'machine learning', 'deep learning',
        'neural network', 'ai', 'ml', 'chatgpt', 'openai', 'tech',
        'technology', 'startup', 'innovation', 'digital', 'automation',
        'robotics', 'algorithm', 'data science', 'blockchain', 'crypto',
        'gpt', 'llm', 'transformer', 'nlp', 'computer vision',
        'reinforcement learning', 'generative ai', 'anthropic',
        'claude', 'bard', 'copilot', 'midjourney', 'stable diffusion'
    ]
    
    # Email Templates
    EMAIL_TEMPLATES = {
        'welcome': {
            'subject': '🎉 Welcome to Nosyt Labs AI Intelligence!',
            'preview': 'Your daily AI insights start now'
        },
        'newsletter': {
            'subject_template': 'Nosyt Labs AI Intelligence - {date}',
            'preview_template': '{article_count} AI stories curated for you'
        },
        'farewell': {
            'subject': 'Sorry to see you go! 😢',
            'preview': 'Thanks for being part of our AI community'
        }
    }
    
    # Pricing
    SUBSCRIPTION_PRICE = 1999  # $19.99 in cents
    CURRENCY = 'USD'
    
    # Features
    PRODUCT_FEATURES = [
        '📰 Daily AI news digest',
        '🔍 Expert analysis & insights', 
        '🚀 Latest tech innovations',
        '💡 Startup & funding updates',
        '🎯 Curated for professionals',
        '📱 Mobile-friendly format',
        '🤖 AI-powered summaries',
        '⚡ Delivered at 8 AM EST',
        '🎨 Beautiful HTML design',
        '💬 Community access'
    ]
    
    @classmethod
    def validate_config(cls) -> Dict[str, bool]:
        """Validate configuration"""
        return {
            'newsapi_key': bool(cls.NEWSAPI_KEY),
            'hf_token': bool(cls.HF_TOKEN),
            'kit_api_key': bool(cls.KIT_API_KEY),
            'whop_api_key': bool(cls.WHOP_API_KEY),
            'rss_sources': len(cls.RSS_SOURCES) > 0,
            'ai_keywords': len(cls.AI_KEYWORDS) > 0
        }