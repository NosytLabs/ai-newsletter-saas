# AI Newsletter SaaS - API Documentation

## Overview

This document describes the API endpoints and integrations for the AI Newsletter SaaS system.

## Whop Integration

### Subscription Webhooks

The system handles Whop subscription webhooks at:

```
POST /whop/webhook
```

#### Webhook Events

**New Subscription (`membership.created`)**
```json
{
  "type": "membership.created",
  "data": {
    "id": "mem_123",
    "status": "active",
    "user": {
      "email": "user@example.com",
      "username": "johndoe"
    },
    "created_at": "2024-01-01T08:00:00Z"
  }
}
```

**Cancelled Subscription (`membership.cancelled`)**
```json
{
  "type": "membership.cancelled",
  "data": {
    "id": "mem_123",
    "status": "cancelled",
    "user": {
      "email": "user@example.com",
      "username": "johndoe"
    },
    "cancelled_at": "2024-01-15T10:30:00Z"
  }
}
```

### Product Creation

Create a new AI Newsletter product on Whop:

```python
from src.whop_integration import WhopIntegration

whop = WhopIntegration()
result = whop.create_ai_newsletter_product()
```

#### Product Configuration

- **Name**: "Nosyt Labs Daily AI Intelligence"
- **Price**: $19.99/month
- **Category**: Newsletter
- **Features**: Daily AI news, expert analysis, mobile-friendly

## Kit (ConvertKit) Integration

### Email Management

**Add Subscriber**
```python
from src.email_sender import EmailSender

email_sender = EmailSender()
success = email_sender.add_subscriber("user@example.com", "John")
```

**Remove Subscriber**
```python
success = email_sender.remove_subscriber("user@example.com")
```

**Send Newsletter**
```python
newsletter = {
    'subject': 'Daily AI Intelligence',
    'html': '<html>...</html>',
    'text': 'Plain text version'
}

subscribers = [{'email': 'user@example.com'}]
result = email_sender.send_newsletter(newsletter, subscribers)
```

## News Collection

### RSS Sources

The system collects news from 20+ RSS sources:

- VentureBeat AI
- TechCrunch
- Wired
- The Verge
- Ars Technica
- OpenAI Blog
- Google AI Blog
- Microsoft AI Blog
- And more...

### NewsAPI Integration

If `NEWSAPI_KEY` is configured, the system also pulls from NewsAPI:

```python
from src.news_collector import NewsCollector

collector = NewsCollector()
articles = collector.collect_daily_news()
```

## AI Content Generation

### Summarization

Using Hugging Face transformers for article summarization:

```python
from src.newsletter_generator import NewsletterGenerator

generator = NewsletterGenerator()
newsletter = generator.generate_newsletter(articles)
```

#### Models Used

- **Summarization**: `facebook/bart-large-cnn`
- **Categorization**: Keyword-based filtering

## Environment Variables

Required environment variables:

```bash
# NewsAPI (free tier: 1,000 requests/day)
NEWSAPI_KEY=your_newsapi_key_here

# Hugging Face (free tier: unlimited inference)
HF_TOKEN=your_huggingface_token_here

# Kit/ConvertKit (free tier: 1,000 subscribers)
KIT_API_KEY=your_kit_api_key_here

# Whop (for subscription management)
WHOP_API_KEY=your_whop_api_key_here
WHOP_WEBHOOK_SECRET=your_webhook_secret_here
```

## GitHub Actions

### Daily Newsletter Workflow

Automated daily newsletter generation:

```yaml
name: Daily AI Newsletter
on:
  schedule:
    - cron: '0 13 * * 1-5'  # 8 AM EST, weekdays
  workflow_dispatch: # Manual trigger
```

### Required Secrets

Set these in GitHub repository secrets:

- `NEWSAPI_KEY`
- `HF_TOKEN`
- `KIT_API_KEY`
- `WHOP_API_KEY`
- `WHOP_WEBHOOK_SECRET`

## Error Handling

The system includes comprehensive error handling:

- **News Collection**: Continues with available sources if some fail
- **AI Processing**: Falls back to simple summaries if AI fails
- **Email Sending**: Logs errors and continues with remaining subscribers
- **Webhook Processing**: Returns appropriate HTTP status codes

## Logging

All operations are logged with timestamps and severity levels:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

Logs are saved to `newsletter.log` and uploaded as GitHub Actions artifacts.

## Rate Limits

- **NewsAPI**: 1,000 requests/day (free tier)
- **Hugging Face**: Unlimited inference (free tier)
- **Kit**: 1,000 subscribers (free tier)
- **Whop**: No specific limits mentioned

## Testing

Run the test suite:

```bash
python test_system.py          # Full system test
python scripts/test_newsletter.py  # Newsletter generation only
```

## Deployment

### Webhook Server

Deploy webhook server for Whop integration:

```bash
python webhook_server.py
```

Exposes endpoints:
- `GET /health` - Health check
- `POST /whop/webhook` - Subscription webhooks

### Production Deployment

For production, use a process manager like PM2 or deploy to platforms like:

- Railway
- Render
- Heroku
- Digital Ocean App Platform

## Support

For questions or issues:

1. Check the logs for error details
2. Verify all environment variables are set
3. Test individual components using the test scripts
4. Review the GitHub Actions workflow logs

---

**Built by Nosyt Labs** - Start earning $19.99/month recurring revenue today!