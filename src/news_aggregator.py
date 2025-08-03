#!/usr/bin/env python3
"""
Enhanced News Aggregator for Nosyt Labs AI Newsletter
Supports 20+ global sources with NewsAPI integration
"""

import feedparser
import requests
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
import re
import time
from config import Config

class NewsAggregator:
    def __init__(self):
        self.newsapi_key = Config.NEWSAPI_KEY
        self.logger = logging.getLogger(__name__)
        
        # 20+ premium AI news sources
        self.rss_sources = {
            'breaking_news': {
                'TechCrunch AI': 'https://techcrunch.com/category/artificial-intelligence/feed/',
                'VentureBeat AI': 'https://venturebeat.com/category/ai/feed/',
                'The Verge AI': 'https://www.theverge.com/ai-artificial-intelligence/rss/index.xml',
                'MIT Tech Review': 'https://www.technologyreview.com/feed/',
                'Ars Technica': 'https://feeds.arstechnica.com/arstechnica/technology-lab',
                'Wired AI': 'https://www.wired.com/feed/tag/ai/latest/rss'
            },
            'research': {
                'arXiv AI': 'https://arxiv.org/rss/cs.AI',
                'arXiv ML': 'https://arxiv.org/rss/cs.LG',
                'Google AI Blog': 'http://googleaiblog.blogspot.com/atom.xml',
                'OpenAI Blog': 'https://openai.com/blog/rss/',
                'DeepMind': 'https://deepmind.com/blog/feed/basic/'
            },
            'business': {
                'AI Business': 'https://aibusiness.com/rss.xml',
                'Crunchbase News': 'https://news.crunchbase.com/feed',
                'The Information': 'https://www.theinformation.com/feed'
            },
            'enterprise': {
                'InfoQ AI': 'https://feed.infoq.com/ai-ml-data-eng/',
                'ZDNet AI': 'https://www.zdnet.com/topic/artificial-intelligence/rss.xml',
                'IEEE Spectrum': 'https://spectrum.ieee.org/feeds/topic/artificial-intelligence.rss'
            },
            'global': {
                'MarkTechPost': 'https://www.marktechpost.com/feed',
                'Unite.AI': 'https://www.unite.ai/feed/',
                'Analytics India': 'https://analyticsindiamag.com/feed/'
            }
        }

    def fetch_newsapi_stories(self, query='artificial intelligence', limit=15):
        """Fetch latest AI stories from NewsAPI"""
        if not self.newsapi_key:
            self.logger.warning('NewsAPI key not configured')
            return []
            
        try:
            url = 'https://newsapi.org/v2/everything'
            params = {
                'q': query,
                'apiKey': self.newsapi_key,
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': limit,
                'from': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            }
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            stories = []
            for article in data.get('articles', []):
                if article.get('title') and article.get('description'):
                    stories.append({
                        'title': article['title'],
                        'summary': article['description'],
                        'url': article['url'],
                        'source': article['source']['name'],
                        'published': article['publishedAt'],
                        'category': 'breaking_news'
                    })
            
            return stories
        except Exception as e:
            self.logger.error(f'NewsAPI error: {e}')
            return []

    def fetch_rss_stories(self):
        """Fetch from all RSS sources"""
        all_stories = []
        
        for category, sources in self.rss_sources.items():
            for source_name, rss_url in sources.items():
                try:
                    feed = feedparser.parse(rss_url)
                    
                    for entry in feed.entries[:3]:  # Top 3 from each
                        title = self.clean_html(entry.get('title', ''))
                        summary = self.clean_html(entry.get('summary', '') or entry.get('description', ''))
                        
                        if title and len(title) > 10:
                            story = {
                                'title': title,
                                'summary': summary[:300] + '...' if len(summary) > 300 else summary,
                                'url': entry.get('link', ''),
                                'source': source_name,
                                'published': entry.get('published', ''),
                                'category': category
                            }
                            all_stories.append(story)
                    
                    time.sleep(0.5)  # Rate limiting
                    
                except Exception as e:
                    self.logger.error(f'RSS error for {source_name}: {e}')
                    continue
        
        return all_stories

    def clean_html(self, text):
        """Remove HTML tags"""
        if not text:
            return ''
        text = re.sub(r'<[^>]+>', '', text)
        return ' '.join(text.split()).strip()

    def score_story(self, story):
        """Calculate business impact score"""
        score = 0.0
        text = f"{story['title']} {story['summary']}".lower()
        
        for keyword in Config.BUSINESS_KEYWORDS['high_impact']:
            if keyword in text:
                score += 3.0
        
        for keyword in Config.BUSINESS_KEYWORDS['medium_impact']:
            if keyword in text:
                score += 2.0
                
        for keyword in Config.BUSINESS_KEYWORDS['trending_tech']:
            if keyword in text:
                score += 1.5
        
        # Category weights
        weights = {'breaking_news': 1.2, 'business': 1.5, 'research': 1.0}
        score *= weights.get(story['category'], 1.0)
        
        return round(score, 2)

    def categorize_stories(self, stories):
        """Categorize and rank stories"""
        # Add scores
        for story in stories:
            story['score'] = self.score_story(story)
        
        # Sort by score
        stories.sort(key=lambda x: x['score'], reverse=True)
        
        # Remove duplicates
        unique_stories = self.remove_duplicates(stories)
        
        # Categorize for newsletter
        categorized = {
            'breaking_news': [],
            'funding_deals': [],
            'research': [],
            'enterprise': [],
            'developer_tools': [],
            'quick_bites': []
        }
        
        for story in unique_stories:
            text = f"{story['title']} {story['summary']}".lower()
            
            if any(word in text for word in Config.CATEGORY_KEYWORDS['funding_deals']):
                categorized['funding_deals'].append(story)
            elif any(word in text for word in Config.CATEGORY_KEYWORDS['research']):
                categorized['research'].append(story)
            elif any(word in text for word in Config.CATEGORY_KEYWORDS['enterprise']):
                categorized['enterprise'].append(story)
            elif any(word in text for word in Config.CATEGORY_KEYWORDS['developer_tools']):
                categorized['developer_tools'].append(story)
            elif story['score'] >= 4.0:
                categorized['breaking_news'].append(story)
            else:
                categorized['quick_bites'].append(story)
        
        # Limit per category using config
        for category in categorized:
            max_stories = Config.MAX_STORIES_PER_CATEGORY.get(category, 3)
            categorized[category] = categorized[category][:max_stories]
        
        return categorized

    def remove_duplicates(self, stories):
        """Remove duplicate stories"""
        unique_stories = []
        seen_titles = set()
        
        for story in stories:
            normalized = re.sub(r'[^\w\s]', '', story['title'].lower())
            if normalized not in seen_titles:
                unique_stories.append(story)
                seen_titles.add(normalized)
        
        return unique_stories

    def get_daily_stories(self):
        """Main method to get all stories"""
        self.logger.info('Collecting AI news...')
        
        # Get from all sources
        rss_stories = self.fetch_rss_stories()
        newsapi_stories = self.fetch_newsapi_stories()
        
        all_stories = rss_stories + newsapi_stories
        
        if not all_stories:
            return {}
        
        return self.categorize_stories(all_stories)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    aggregator = NewsAggregator()
    stories = aggregator.get_daily_stories()
    print(f'Collected {sum(len(v) for v in stories.values())} stories')
