#!/usr/bin/env python3
"""
News Collector - Gathers AI news from multiple sources
"""

import os
import requests
import logging
from datetime import datetime, timedelta
from typing import List, Dict
import feedparser

class NewsCollector:
    """Collects news from various AI and tech sources"""
    
    def __init__(self):
        self.newsapi_key = os.getenv('NEWSAPI_KEY')
        self.logger = logging.getLogger(__name__)
        
        # RSS Sources for AI news
        self.rss_sources = [
            'https://feeds.feedburner.com/venturebeat/SZYF',  # VentureBeat AI
            'https://rss.cnn.com/rss/edition.rss',  # CNN
            'https://techcrunch.com/feed/',  # TechCrunch
            'https://www.wired.com/feed/rss',  # Wired
            'https://www.theverge.com/rss/index.xml',  # The Verge
            'https://feeds.arstechnica.com/arstechnica/index',  # Ars Technica
            'https://rss.slashdot.org/Slashdot/slashdotMain',  # Slashdot
            'https://feeds.feedburner.com/AINews',  # AI News
        ]
    
    def collect_daily_news(self) -> List[Dict]:
        """Collect news from all sources"""
        all_articles = []
        
        # Collect from RSS feeds
        rss_articles = self._collect_from_rss()
        all_articles.extend(rss_articles)
        
        # Collect from NewsAPI if available
        if self.newsapi_key:
            newsapi_articles = self._collect_from_newsapi()
            all_articles.extend(newsapi_articles)
        
        # Deduplicate and filter
        unique_articles = self._deduplicate_articles(all_articles)
        filtered_articles = self._filter_ai_content(unique_articles)
        
        self.logger.info(f"Collected {len(filtered_articles)} unique AI articles")
        return filtered_articles[:20]  # Top 20 articles
    
    def _collect_from_rss(self) -> List[Dict]:
        """Collect articles from RSS feeds"""
        articles = []
        
        for rss_url in self.rss_sources:
            try:
                feed = feedparser.parse(rss_url)
                
                for entry in feed.entries[:5]:  # Top 5 from each source
                    articles.append({
                        'title': entry.get('title', ''),
                        'description': entry.get('summary', ''),
                        'url': entry.get('link', ''),
                        'published_at': entry.get('published', ''),
                        'source': feed.feed.get('title', rss_url),
                        'content': entry.get('summary', '')
                    })
                    
            except Exception as e:
                self.logger.warning(f"Failed to fetch from {rss_url}: {e}")
        
        return articles
    
    def _collect_from_newsapi(self) -> List[Dict]:
        """Collect articles from NewsAPI"""
        try:
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            
            url = 'https://newsapi.org/v2/everything'
            params = {
                'q': 'artificial intelligence OR machine learning OR AI OR tech',
                'from': yesterday,
                'sortBy': 'popularity',
                'language': 'en',
                'pageSize': 20,
                'apiKey': self.newsapi_key
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            articles = []
            for article in data.get('articles', []):
                articles.append({
                    'title': article.get('title', ''),
                    'description': article.get('description', ''),
                    'url': article.get('url', ''),
                    'published_at': article.get('publishedAt', ''),
                    'source': article.get('source', {}).get('name', ''),
                    'content': article.get('content', '')
                })
            
            return articles
            
        except Exception as e:
            self.logger.warning(f"NewsAPI collection failed: {e}")
            return []
    
    def _deduplicate_articles(self, articles: List[Dict]) -> List[Dict]:
        """Remove duplicate articles based on title similarity"""
        seen_titles = set()
        unique_articles = []
        
        for article in articles:
            title = article.get('title', '').lower().strip()
            if title and title not in seen_titles:
                seen_titles.add(title)
                unique_articles.append(article)
        
        return unique_articles
    
    def _filter_ai_content(self, articles: List[Dict]) -> List[Dict]:
        """Filter articles for AI/tech relevance"""
        ai_keywords = [
            'artificial intelligence', 'machine learning', 'deep learning',
            'neural network', 'ai', 'ml', 'chatgpt', 'openai', 'tech',
            'technology', 'startup', 'innovation', 'digital', 'automation',
            'robotics', 'algorithm', 'data science', 'blockchain', 'crypto'
        ]
        
        filtered = []
        for article in articles:
            title = article.get('title', '').lower()
            description = article.get('description', '').lower()
            content = f"{title} {description}"
            
            # Check if article contains AI/tech keywords
            if any(keyword in content for keyword in ai_keywords):
                filtered.append(article)
        
        return filtered