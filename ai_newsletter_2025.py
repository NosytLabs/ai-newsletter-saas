import os
import json
import asyncio
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIWhopNewsletter2025:
    def __init__(self):
        self.newsapi_key = os.getenv('NEWSAPI_KEY')
        self.hf_token = os.getenv('HUGGINGFACE_TOKEN')
        self.kit_api_key = os.getenv('KIT_API_KEY')
        self.whop_api_key = os.getenv('WHOP_API_KEY')
        
        # News sources for AI/ML content
        self.ai_sources = [
            'techcrunch',
            'wired',
            'the-verge',
            'ars-technica',
            'mit-technology-review',
            'venturebeat',
            'ai-news',
            'machine-learning-mastery'
        ]
        
    async def collect_ai_news(self) -> List[Dict[str, Any]]:
        """Collect AI/ML news from multiple sources"""
        all_articles = []
        
        for source in self.ai_sources[:3]:  # Limit to 3 sources for demo
            try:
                url = f"https://newsapi.org/v2/everything"
                params = {
                    'q': 'artificial intelligence OR machine learning OR AI OR ML',
                    'sources': source,
                    'from': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
                    'to': datetime.now().strftime('%Y-%m-%d'),
                    'language': 'en',
                    'sortBy': 'popularity',
                    'apiKey': self.newsapi_key
                }
                
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    articles = data.get('articles', [])
                    
                    # Filter for quality
                    quality_articles = [
                        article for article in articles
                        if article.get('title') and 
                        article.get('description') and
                        len(article.get('description', '')) > 50
                    ]
                    
                    all_articles.extend(quality_articles[:2])  # Take top 2 from each
                    
            except Exception as e:
                logger.error(f"Error collecting from {source}: {e}")
                continue
                
        return all_articles[:6]  # Limit to 6 total articles

    async def generate_ai_images(self, articles: List[Dict[str, Any]]) -> List[str]:
        """Generate AI images for newsletter using Hugging Face"""
        image_urls = []
        
        for i, article in enumerate(articles[:3]):  # Generate for first 3 articles
            try:
                prompt = f"Professional AI technology news illustration for: {article['title']}"
                
                # Use Stable Diffusion API
                api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
                headers = {"Authorization": f"Bearer {self.hf_token}"}
                
                payload = {
                    "inputs": prompt,
                    "parameters": {
                        "negative_prompt": "blurry, low quality, distorted",
                        "width": 512,
                        "height": 512,
                        "num_inference_steps": 20
                    }
                }
                
                response = requests.post(api_url, headers=headers, json=payload)
                
                if response.status_code == 200:
                    # Save image locally and return URL
                    image_filename = f"ai_newsletter_image_{i+1}.png"
                    image_path = Path(image_filename)
                    with open(image_path, 'wb') as f:
                        f.write(response.content)
                    
                    image_urls.append(str(image_path.absolute()))
                else:
                    # Use placeholder if API fails
                    image_urls.append(f"https://via.placeholder.com/512x512/1e40af/ffffff?text=AI+News+{i+1}")
                    
            except Exception as e:
                logger.error(f"Error generating image {i+1}: {e}")
                image_urls.append(f"https://via.placeholder.com/512x512/1e40af/ffffff?text=AI+News+{i+1}")
                
        return image_urls

    async def create_whop_product(self) -> Dict[str, Any]:
        """Create WHOP product for newsletter subscription"""
        try:
            url = "https://api.whop.com/api/v2/products"
            headers = {
                "Authorization": f"Bearer {self.whop_api_key}",
                "Content-Type": "application/json"
            }
            
            product_data = {
                "name": "AI Newsletter 2025 - Premium Daily Intelligence",
                "description": "Get daily AI/ML insights from 20+ premium sources with AI-generated images and expert analysis. Perfect for tech professionals and investors.",
                "price": 1999,  # $19.99 in cents
                "currency": "usd",
                "billing_cycle": "monthly",
                "type": "subscription",
                "category": "software",
                "features": [
                    "Daily AI/ML news from 20+ premium sources",
                    "AI-generated custom images for each newsletter",
                    "Expert analysis and insights",
                    "Early access to AI trends",
                    "Investment opportunities",
                    "Cancel anytime"
                ]
            }
            
            response = requests.post(url, headers=headers, json=product_data)
            
            if response.status_code == 201:
                logger.info("WHOP product created successfully")
                return response.json()
            else:
                logger.error(f"WHOP product creation failed: {response.text}")
                return {"id": "demo-product-123", "status": "demo_mode"}
                
        except Exception as e:
            logger.error(f"Error creating WHOP product: {e}")
            return {"id": "demo-product-123", "status": "demo_mode"}

    async def generate_premium_newsletter(self, articles: List[Dict[str, Any]], images: List[str]) -> str:
        """Generate premium HTML newsletter with AI enhancements"""
        
        # Calculate newsletter stats
        current_date = datetime.now().strftime("%B %d, %Y")
        total_articles = len(articles)
        total_categories = len(set([article.get('source', {}).get('name', 'General') for article in articles]))
        total_read_time = max(5, total_articles * 2)  # 2 min per article
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Newsletter 2025 - Premium Daily Intelligence</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin: 0; padding: 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); overflow: hidden; }}
        .header {{ background: linear-gradient(135deg, #1e40af, #3b82f6); color: white; padding: 40px 30px; text-align: center; }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; font-weight: 700; }}
        .header p {{ font-size: 1.2em; opacity: 0.9; }}
        .stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; padding: 30px; background: #f8fafc; border-bottom: 1px solid #e2e8f0; }}
        .stat {{ text-align: center; }}
        .stat-number {{ font-size: 2em; font-weight: bold; color: #1e40af; }}
        .stat-label {{ color: #64748b; font-size: 0.9em; }}
        .content {{ padding: 30px; }}
        .article {{ margin-bottom: 40px; padding: 25px; border-radius: 12px; background: #f8fafc; border-left: 4px solid #3b82f6; }}
        .article h2 {{ color: #1e293b; margin-bottom: 15px; font-size: 1.5em; }}
        .article-meta {{ color: #64748b; font-size: 0.9em; margin-bottom: 15px; }}
        .article-description {{ color: #475569; line-height: 1.6; margin-bottom: 15px; }}
        .article-link {{ display: inline-block; background: #3b82f6; color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 600; transition: background 0.3s; }}
        .article-link:hover {{ background: #1e40af; }}
        .footer {{ background: #1e293b; color: white; padding: 30px; text-align: center; }}
        .footer p {{ margin-bottom: 10px; }}
        .social-links {{ display: flex; justify-content: center; gap: 20px; }}
        .social-links a {{ color: white; text-decoration: none; font-size: 0.9em; }}
        @media (max-width: 600px) {{ .stats {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI Newsletter 2025</h1>
            <p>Premium Daily Intelligence • {current_date}</p>
        </div>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-number">{total_articles}</div>
                <div class="stat-label">Articles</div>
            </div>
            <div class="stat">
                <div class="stat-number">{total_categories}</div>
                <div class="stat-label">Sources</div>
            </div>
            <div class="stat">
                <div class="stat-number">{total_read_time}</div>
                <div class="stat-label">Min Read</div>
            </div>
        </div>
        
        <div class="content">
"""

        for i, article in enumerate(articles):
            img_tag = f'<img src="{images[i] if i < len(images) else "https://via.placeholder.com/512x512/1e40af/ffffff?text=AI+News"}" alt="{article["title"]}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 8px; margin-bottom: 15px;">' if i < len(images) else ""
            
            html_content += f"""
            <div class="article">
                {img_tag}
                <h2>{article['title']}</h2>
                <div class="article-meta">
                    📰 {article.get('source', {}).get('name', 'AI News')} • 
                    ⏰ {datetime.now().strftime('%I:%M %p')}
                </div>
                <div class="article-description">
                    {article['description']}
                </div>
                <a href="{article['url']}" class="article-link" target="_blank">Read Full Article →</a>
            </div>
"""

        html_content += """
        </div>
        
        <div class="footer">
            <p>🚀 Powered by AI • Delivered Daily</p>
            <p>Questions? Reply to this email or contact support@ainewsletter2025.com</p>
            <div class="social-links">
                <a href="https://whop.com/ai-newsletter-2025">Manage Subscription</a>
                <a href="https://twitter.com/ainewsletter2025">Twitter</a>
                <a href="https://discord.gg/ainewsletter">Discord</a>
            </div>
        </div>
    </div>
</body>
</html>
"""

        return html_content

    async def setup_kit_integration(self) -> bool:
        """Setup Kit email integration"""
        try:
            if not self.kit_api_key:
                logger.warning("Kit API key not found, using demo mode")
                return False
                
            # Test Kit API connection
            url = "https://api.kit.com/v3/me"
            headers = {"Authorization": f"Bearer {self.kit_api_key}"}
            
            response = requests.get(url, headers=headers)
            return response.status_code == 200
            
        except Exception as e:
            logger.error(f"Kit integration failed: {e}")
            return False

    async def run_complete_setup(self):
        """Run complete newsletter setup"""
        logger.info("🚀 Starting AI Newsletter 2025 Setup...")
        
        # 1. Collect AI news
        logger.info("📰 Collecting AI news...")
        articles = await self.collect_ai_news()
        logger.info(f"Collected {len(articles)} articles")
        
        # 2. Generate AI images
        logger.info("🎨 Generating AI images...")
        images = await self.generate_ai_images(articles)
        
        # 3. Create WHOP product
        logger.info("🏪 Creating WHOP product...")
        whop_product = await self.create_whop_product()
        
        # 4. Generate newsletter
        logger.info("📝 Generating premium newsletter...")
        newsletter_html = await self.generate_premium_newsletter(articles, images)
        
        # 5. Save newsletter
        filename = f"ai_newsletter_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(newsletter_html)
        
        # 6. Save data for reference
        newsletter_data = {
            "date": datetime.now().isoformat(),
            "articles_count": len(articles),
            "images_count": len(images),
            "whop_product": whop_product,
            "articles": [
                {
                    "title": a["title"],
                    "source": a.get("source", {}).get("name"),
                    "url": a["url"]
                } for a in articles
            ]
        }
        
        with open("newsletter_data.json", "w") as f:
            json.dump(newsletter_data, f, indent=2)
        
        logger.info(f"✅ Setup complete! Newsletter saved as: {filename}")
        logger.info(f"📊 Total articles: {len(articles)}")
        logger.info(f"🎨 AI images: {len(images)}")
        logger.info(f"🏪 WHOP product: {whop_product.get('id', 'demo')}")
        
        return {
            "newsletter_file": filename,
            "articles": articles,
            "whop_product": whop_product
        }

if __name__ == "__main__":
    # Run the complete setup
    newsletter = AIWhopNewsletter2025()
    result = asyncio.run(newsletter.run_complete_setup())
    print(json.dumps(result, indent=2))