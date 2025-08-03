#!/usr/bin/env python3
"""
Modern Newsletter Generator with Beautiful HTML Templates
"""

import requests
import logging
from datetime import datetime
from typing import Dict, List
from config import Config

class NewsletterGenerator:
    def __init__(self):
        self.hf_token = Config.HF_TOKEN
        self.logger = logging.getLogger(__name__)
        
        self.api_url = 'https://api-inference.huggingface.co/models/'
        self.headers = {'Authorization': f'Bearer {self.hf_token}'} if self.hf_token else {}
        
        # Free HF models for content enhancement
        self.models = [
            'microsoft/DialoGPT-medium',
            'google/flan-t5-base',
            'facebook/blenderbot-400M-distill'
        ]

    def query_hf_model(self, model, prompt, max_length=300):
        """Query Hugging Face model"""
        if not self.hf_token:
            return ''
            
        try:
            url = self.api_url + model
            payload = {
                'inputs': prompt,
                'parameters': {
                    'max_length': max_length,
                    'temperature': 0.7,
                    'do_sample': True
                }
            }
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('generated_text', '').replace(prompt, '').strip()
            
            return ''
        except Exception as e:
            self.logger.error(f'HF model error: {e}')
            return ''

    def generate_executive_summary(self, top_stories):
        """Generate executive summary"""
        if not top_stories:
            return 'No major AI developments today.'
        
        stories_text = '\n'.join([f'- {story["title"]}' for story in top_stories[:3]])
        
        prompt = f"""Summarize these AI developments for business executives:

{stories_text}

Executive Summary:"""
        
        # Try AI generation
        for model in self.models:
            summary = self.query_hf_model(model, prompt, 200)
            if summary and len(summary) > 50:
                return summary
        
        # Fallback
        return f"""Today's AI landscape shows {len(top_stories)} key developments:

• **Market Leadership**: {top_stories[0]['title'][:80]}...
• **Innovation Focus**: {top_stories[1]['title'][:80] if len(top_stories) > 1 else 'Continued advancement in AI capabilities'}
• **Strategic Impact**: {'Enterprise adoption accelerating with new partnerships' if len(top_stories) > 2 else 'Competitive positioning opportunities emerging'}

These developments signal continued rapid evolution in AI market dynamics."""

    def create_beautiful_html_newsletter(self, categorized_stories):
        """Create stunning HTML newsletter"""
        current_date = datetime.now().strftime('%B %d, %Y')
        
        # Generate sections
        exec_summary = self.generate_executive_summary(categorized_stories.get('breaking_news', []))
        
        newsletter_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 {Config.NEWSLETTER_NAME} - {current_date}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: {Config.EMAIL_TEMPLATE_SETTINGS['font_family']};
            line-height: 1.6;
            color: {Config.EMAIL_TEMPLATE_SETTINGS['text_color']};
            background: {Config.EMAIL_TEMPLATE_SETTINGS['background_gradient']};
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 700px;
            margin: 0 auto;
            background: #ffffff;
            border-radius: 16px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, {Config.EMAIL_TEMPLATE_SETTINGS['primary_color']} 0%, {Config.EMAIL_TEMPLATE_SETTINGS['secondary_color']} 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }}
        
        .logo {{
            font-size: 2.5rem;
            margin-bottom: 10px;
        }}
        
        .header h1 {{
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 8px;
        }}
        
        .header .date {{
            font-size: 1rem;
            opacity: 0.9;
            font-weight: 300;
        }}
        
        .content {{
            padding: 0;
        }}
        
        .section {{
            padding: 30px;
            border-bottom: 1px solid #f1f5f9;
        }}
        
        .section:last-child {{
            border-bottom: none;
        }}
        
        .section-title {{
            font-size: 1.4rem;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .section-icon {{
            font-size: 1.5rem;
        }}
        
        .executive-summary {{
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            border-left: 4px solid {Config.EMAIL_TEMPLATE_SETTINGS['primary_color']};
            padding: 25px;
            margin-bottom: 20px;
            border-radius: 8px;
        }}
        
        .story {{
            margin-bottom: 25px;
            padding-bottom: 20px;
            border-bottom: 1px solid #f1f5f9;
        }}
        
        .story:last-child {{
            margin-bottom: 0;
            padding-bottom: 0;
            border-bottom: none;
        }}
        
        .story-title {{
            font-size: 1.1rem;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 8px;
            line-height: 1.4;
        }}
        
        .story-summary {{
            color: {Config.EMAIL_TEMPLATE_SETTINGS['light_text_color']};
            margin-bottom: 12px;
            line-height: 1.5;
        }}
        
        .story-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.85rem;
            color: #64748b;
        }}
        
        .story-source {{
            font-weight: 500;
            color: {Config.EMAIL_TEMPLATE_SETTINGS['primary_color']};
        }}
        
        .story-score {{
            background: linear-gradient(135deg, {Config.EMAIL_TEMPLATE_SETTINGS['success_color']} 0%, #059669 100%);
            color: white;
            padding: 4px 10px;
            border-radius: 12px;
            font-weight: 500;
            font-size: 0.8rem;
        }}
        
        .read-more {{
            color: {Config.EMAIL_TEMPLATE_SETTINGS['primary_color']};
            text-decoration: none;
            font-weight: 500;
            font-size: 0.9rem;
            border-bottom: 1px solid transparent;
            transition: border-color 0.2s;
        }}
        
        .read-more:hover {{
            border-color: {Config.EMAIL_TEMPLATE_SETTINGS['primary_color']};
        }}
        
        .footer {{
            background: #1e293b;
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .footer h3 {{
            margin-bottom: 15px;
            color: #f1f5f9;
        }}
        
        .footer p {{
            color: #94a3b8;
            margin-bottom: 10px;
        }}
        
        .cta-button {{
            display: inline-block;
            background: linear-gradient(135deg, {Config.EMAIL_TEMPLATE_SETTINGS['accent_color']} 0%, #d97706 100%);
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            margin: 15px 10px 5px 10px;
            transition: transform 0.2s;
        }}
        
        .cta-button:hover {{
            transform: translateY(-2px);
        }}
        
        .personas {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}
        
        .persona {{
            background: #f8fafc;
            padding: 15px;
            border-radius: 8px;
            border-left: 3px solid {Config.EMAIL_TEMPLATE_SETTINGS['primary_color']};
        }}
        
        .persona h4 {{
            color: #1e293b;
            margin-bottom: 5px;
            font-size: 0.95rem;
        }}
        
        .persona p {{
            color: #64748b;
            font-size: 0.85rem;
        }}
        
        @media (max-width: 600px) {{
            body {{
                padding: 10px;
            }}
            
            .header {{
                padding: 30px 20px;
            }}
            
            .section {{
                padding: 20px;
            }}
            
            .personas {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">🤖</div>
            <h1>{Config.NEWSLETTER_NAME}</h1>
            <div class="date">{current_date}</div>
        </div>
        
        <div class="content">
            <div class="section">
                <div class="section-title">
                    <span class="section-icon">📊</span>
                    Executive Summary
                </div>
                <div class="executive-summary">
                    {exec_summary}
                </div>
            </div>
            
            {self._generate_section_html('🔥', 'Breaking AI News', categorized_stories.get('breaking_news', []))}
            {self._generate_section_html('💰', 'Funding & Deals', categorized_stories.get('funding_deals', []))}
            {self._generate_section_html('🔬', 'Research Breakthroughs', categorized_stories.get('research', []))}
            {self._generate_section_html('🏢', 'Enterprise Focus', categorized_stories.get('enterprise', []))}
            {self._generate_section_html('⚡', 'Developer Tools', categorized_stories.get('developer_tools', []))}
            {self._generate_section_html('🎯', 'Quick Bites', categorized_stories.get('quick_bites', []))}
        </div>
        
        <div class="footer">
            <h3>🚀 For Our Subscribers</h3>
            <div class="personas">
                {self._generate_personas_html()}
            </div>
            
            <p style="margin-top: 25px; color: #f1f5f9;">{Config.COMPANY_NAME} - Connecting global business leaders with AI developments that matter</p>
            
            <a href="{Config.SUBSCRIPTION_URL}" class="cta-button">Subscribe Now - {Config.SUBSCRIPTION_PRICE}</a>
            <a href="mailto:{Config.COMPANY_EMAIL}" class="cta-button">Contact Us</a>
        </div>
    </div>
</body>
</html>
        """
        
        return newsletter_html

    def _generate_section_html(self, icon, title, stories):
        """Generate HTML for a newsletter section"""
        if not stories:
            return ''
        
        section_html = f'''
            <div class="section">
                <div class="section-title">
                    <span class="section-icon">{icon}</span>
                    {title}
                </div>
        '''
        
        for story in stories:
            section_html += f'''
                <div class="story">
                    <div class="story-title">{story['title']}</div>
                    <div class="story-summary">{story['summary']}</div>
                    <div class="story-meta">
                        <span class="story-source">{story['source']}</span>
                        <span class="story-score">Impact: {story.get('score', 0)}/10</span>
                    </div>
                    <a href="{story['url']}" class="read-more">Read Full Story →</a>
                </div>
            '''
        
        section_html += '</div>'
        return section_html
    
    def _generate_personas_html(self):
        """Generate HTML for target personas"""
        personas_html = ''
        for persona_key, persona_data in Config.TARGET_PERSONAS.items():
            personas_html += f'''
                <div class="persona">
                    <h4>{persona_data['title']}</h4>
                    <p>{persona_data['description']}</p>
                </div>
            '''
        return personas_html

    def create_newsletter(self, categorized_stories):
        """Create complete newsletter"""
        self.logger.info('Generating beautiful newsletter...')
        return self.create_beautiful_html_newsletter(categorized_stories)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    generator = NewsletterGenerator()
    
    # Test with mock data
    mock_stories = {
        'breaking_news': [{
            'title': 'OpenAI Announces Revolutionary GPT-5 Model',
            'summary': 'New model features advanced reasoning capabilities and multimodal processing.',
            'url': 'https://example.com',
            'source': 'TechCrunch',
            'score': 9.5
        }]
    }
    
    newsletter = generator.create_newsletter(mock_stories)
    print('Newsletter generated successfully!')
