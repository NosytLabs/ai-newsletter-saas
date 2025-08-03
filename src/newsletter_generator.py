#!/usr/bin/env python3
"""
Newsletter Generator - Creates beautiful HTML newsletters using AI
"""

import os
import logging
from typing import List, Dict
from datetime import datetime
from transformers import pipeline
import requests

class NewsletterGenerator:
    """Generates AI-powered newsletters"""
    
    def __init__(self):
        self.hf_token = os.getenv('HF_TOKEN')
        self.logger = logging.getLogger(__name__)
        
        # Initialize Hugging Face pipeline for summarization
        try:
            self.summarizer = pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                use_auth_token=self.hf_token
            )
        except Exception as e:
            self.logger.warning(f"Failed to load summarizer: {e}")
            self.summarizer = None
    
    def generate_newsletter(self, articles: List[Dict]) -> Dict:
        """Generate complete newsletter content"""
        try:
            # Group articles by category
            categorized = self._categorize_articles(articles)
            
            # Generate summaries
            summarized = self._generate_summaries(categorized)
            
            # Create newsletter structure
            newsletter = {
                'subject': f"Nosyt Labs AI Intelligence - {datetime.now().strftime('%B %d, %Y')}",
                'html': self._generate_html(summarized),
                'text': self._generate_text(summarized),
                'articles_count': len(articles)
            }
            
            return newsletter
            
        except Exception as e:
            self.logger.error(f"Newsletter generation failed: {e}")
            return self._generate_fallback_newsletter(articles)
    
    def _categorize_articles(self, articles: List[Dict]) -> Dict[str, List[Dict]]:
        """Categorize articles by topic"""
        categories = {
            'AI & Machine Learning': [],
            'Tech Innovation': [],
            'Business & Startups': [],
            'Other': []
        }
        
        for article in articles:
            title = article.get('title', '').lower()
            description = article.get('description', '').lower()
            content = f"{title} {description}"
            
            if any(keyword in content for keyword in ['ai', 'artificial intelligence', 'machine learning', 'neural', 'chatgpt']):
                categories['AI & Machine Learning'].append(article)
            elif any(keyword in content for keyword in ['startup', 'business', 'funding', 'investment']):
                categories['Business & Startups'].append(article)
            elif any(keyword in content for keyword in ['tech', 'innovation', 'digital', 'automation']):
                categories['Tech Innovation'].append(article)
            else:
                categories['Other'].append(article)
        
        # Remove empty categories
        return {k: v for k, v in categories.items() if v}
    
    def _generate_summaries(self, categorized: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
        """Generate AI summaries for articles"""
        summarized = {}
        
        for category, articles in categorized.items():
            summarized[category] = []
            
            for article in articles:
                summary = self._summarize_article(article)
                article['ai_summary'] = summary
                summarized[category].append(article)
        
        return summarized
    
    def _summarize_article(self, article: Dict) -> str:
        """Generate AI summary for single article"""
        try:
            if not self.summarizer:
                return article.get('description', '')[:200] + '...'
            
            content = article.get('content') or article.get('description', '')
            if len(content) < 50:
                return content
            
            # Limit input length for summarization
            content = content[:1000]
            
            summary = self.summarizer(content, max_length=100, min_length=30, do_sample=False)
            return summary[0]['summary_text']
            
        except Exception as e:
            self.logger.warning(f"Summarization failed for article: {e}")
            return article.get('description', '')[:200] + '...'
    
    def _generate_html(self, categorized: Dict[str, List[Dict]]) -> str:
        """Generate beautiful HTML newsletter"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Nosyt Labs AI Intelligence</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px; margin-bottom: 30px; }}
                .header h1 {{ margin: 0; font-size: 28px; }}
                .date {{ opacity: 0.9; margin-top: 10px; }}
                .category {{ margin-bottom: 40px; }}
                .category h2 {{ color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 10px; }}
                .article {{ background: #f8f9fa; border-left: 4px solid #667eea; padding: 20px; margin-bottom: 20px; border-radius: 5px; }}
                .article h3 {{ margin-top: 0; color: #333; }}
                .article p {{ color: #666; margin: 10px 0; }}
                .article a {{ color: #667eea; text-decoration: none; font-weight: 500; }}
                .article a:hover {{ text-decoration: underline; }}
                .source {{ font-size: 12px; color: #999; text-transform: uppercase; letter-spacing: 1px; }}
                .footer {{ text-align: center; margin-top: 40px; padding: 20px; border-top: 1px solid #eee; color: #666; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🤖 Nosyt Labs AI Intelligence</h1>
                <div class="date">{datetime.now().strftime('%A, %B %d, %Y')}</div>
            </div>
        """
        
        # Add categories and articles
        for category, articles in categorized.items():
            html += f'<div class="category"><h2>{category}</h2>'
            
            for article in articles:
                html += f"""
                <div class="article">
                    <div class="source">{article.get('source', 'Unknown Source')}</div>
                    <h3>{article.get('title', 'No Title')}</h3>
                    <p>{article.get('ai_summary', article.get('description', ''))}</p>
                    <a href="{article.get('url', '#')}" target="_blank">Read Full Article →</a>
                </div>
                """
            
            html += '</div>'
        
        # Add footer
        html += f"""
            <div class="footer">
                <p>🚀 Powered by <strong>Nosyt Labs</strong></p>
                <p>Daily AI intelligence delivered to your inbox</p>
                <p><a href="https://whop.com" style="color: #667eea;">Manage Subscription</a></p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _generate_text(self, categorized: Dict[str, List[Dict]]) -> str:
        """Generate plain text version"""
        text = f"Nosyt Labs AI Intelligence - {datetime.now().strftime('%B %d, %Y')}\n"
        text += "=" * 50 + "\n\n"
        
        for category, articles in categorized.items():
            text += f"{category.upper()}\n" + "-" * len(category) + "\n\n"
            
            for i, article in enumerate(articles, 1):
                text += f"{i}. {article.get('title', 'No Title')}\n"
                text += f"   Source: {article.get('source', 'Unknown')}\n"
                text += f"   {article.get('ai_summary', article.get('description', ''))}\n"
                text += f"   Read more: {article.get('url', '#')}\n\n"
        
        text += "\n" + "=" * 50 + "\n"
        text += "Powered by Nosyt Labs\n"
        text += "Daily AI intelligence delivered to your inbox\n"
        
        return text
    
    def _generate_fallback_newsletter(self, articles: List[Dict]) -> Dict:
        """Generate simple newsletter if AI processing fails"""
        return {
            'subject': f"Nosyt Labs AI Intelligence - {datetime.now().strftime('%B %d, %Y')}",
            'html': self._generate_simple_html(articles),
            'text': self._generate_simple_text(articles),
            'articles_count': len(articles)
        }
    
    def _generate_simple_html(self, articles: List[Dict]) -> str:
        """Generate simple HTML without AI processing"""
        html = f"""
        <h1>Nosyt Labs AI Intelligence</h1>
        <p>{datetime.now().strftime('%B %d, %Y')}</p>
        <hr>
        """
        
        for article in articles:
            html += f"""
            <div style="margin: 20px 0; padding: 15px; border-left: 3px solid #007cba;">
                <h3>{article.get('title', 'No Title')}</h3>
                <p>{article.get('description', '')}</p>
                <a href="{article.get('url', '#')}">Read More</a>
            </div>
            """
        
        return html
    
    def _generate_simple_text(self, articles: List[Dict]) -> str:
        """Generate simple text without AI processing"""
        text = f"Nosyt Labs AI Intelligence - {datetime.now().strftime('%B %d, %Y')}\n\n"
        
        for i, article in enumerate(articles, 1):
            text += f"{i}. {article.get('title', 'No Title')}\n"
            text += f"   {article.get('description', '')}\n"
            text += f"   {article.get('url', '#')}\n\n"
        
        return text