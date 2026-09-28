import os
import json
from datetime import datetime, timedelta, timezone

from tavily import TavilyClient
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# Clients
# -----------------------------

tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

groq = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


MODEL = "openai/gpt-oss-120b"


# -----------------------------
# Search AI news
# -----------------------------

def search_ai_updates():

    queries = [
        "latest AI model releases",
        "latest AI company announcements",
        "latest AI tools and products",
        "latest AI research breakthroughs",
        "latest AI agent developments",
        "latest generative AI news"
    ]

    all_results = []

    for query in queries:

        response = tavily.search(
            query=query,
            topic="news",
            search_depth="advanced",
            time_range="day",
            max_results=3
        )

        all_results.extend(response.get("results", []))

    # Remove duplicate URLs
    unique_results = {}

    for result in all_results:

        url = result.get("url")

        if url:
            unique_results[url] = {
                "title": result.get("title", ""),
                "url": url,
                "content": result.get("content", ""),
                "published_date": result.get("published_date", "")
            }

    return list(unique_results.values())


# -----------------------------
# AI processing
# -----------------------------

def generate_ai_updates(results):

    # Keep only the best 12 search results
    results = results[:12]

    news_text = ""

    for i, item in enumerate(results, 1):

        content = item.get("content", "")

        # IMPORTANT: don't send the entire article
        content = content[:500]

        news_text += f"""
NEWS {i}
Title: {item.get('title', '')}
URL: {item.get('url', '')}
Content: {content}
---
"""

    prompt = f"""
You are an AI news research agent.

From the following news collected from the last 24 hours,
select the 5-8 most important AI updates.

Focus only on:
- New AI models
- AI product launches
- AI company announcements
- AI tools
- AI agents
- Important AI research
- Major open-source AI releases

Ignore:
- Duplicate news
- Old news
- Clickbait
- Generic AI articles

For every selected update provide:

title
company
category
summary
why_it_matters
source_url

IMPORTANT:
- Use ONLY the information provided.
- Never invent facts.
- Keep each summary under 50 words.
- Keep why_it_matters under 30 words.
- Preserve the original URL.

Return ONLY JSON in this format:

{{
    "updates": [
        {{
            "title": "...",
            "company": "...",
            "category": "...",
            "summary": "...",
            "why_it_matters": "...",
            "source_url": "..."
        }}
    ]
}}

NEWS:

{news_text}
"""

    response = groq.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a precise AI news researcher."},
        {"role": "user", "content": prompt},
    ],
    temperature=0.5,
    max_completion_tokens=8000,   # was 2000
    reasoning_effort="medium",       # less reasoning, more room for the JSON
    response_format={"type": "json_object"},
)

    content = response.choices[0].message.content

    data = json.loads(content)

    return data.get("updates", [])

# -----------------------------
# Main Agent
# -----------------------------

def get_ai_updates():

    results = search_ai_updates()

    if not results:
        return []

    updates = generate_ai_updates(results)

    return updates