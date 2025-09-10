# Comprehensive CrewAI Code Example: Generating SEO-Optimized Business News Article using DeepSeek API
# This script uses CrewAI to orchestrate multiple agents for deep research, keyword analysis, article generation,
# and SEO auditing based on the given headline. It outputs a structured JSON as specified in the original prompt.
# Improvements for longer article:
# - Increased max_tokens to 8000 for deeper, more expansive generations.
# - Enhanced agent goals and task descriptions to emphasize detailed, comprehensive content (target 1000-1500 words for robustness).
# - Added instructions in prompts to expand sections with more analysis, examples, data points, and sub-sections for length and depth.
# - Fact researcher now instructed to provide extended reports with multiple angles, historical context, and future projections.
# - Article writer prompted to create expansive body with 8-12 sections/paragraphs, including detailed breakdowns, quotes, and impacts.
# - Maintained initial sequential logic: keyword -> facts -> write -> audit.
# - Still no search tools (crewai-tools limitation); relies on LLM knowledge. For production, integrate custom search via LiteLLM or update tools.
# Requirements:
# - pip install crewai crewai-tools langchain-openai litellm pydantic python-dotenv
# - Set environment variables:
#   export DEEPSEEK_API_KEY="your_deepseek_api_key_here"
#   export SERPER_API_KEY="your_serper_dev_api_key_here"  # For future web search tool
# - DeepSeek API: https://platform.deepseek.com/api_keys (free tier available)
# - Serper API: https://serper.dev/ (for Google-like search, if tools enabled)
# - Run this script: python this_script.py
# - Date context: Assumes current date is September 10, 2025, for timeliness.

import os
import json
from typing import Dict, Any
from crewai import Agent, Task, Crew, Process
# from crewai_tools import SerperDevTool  # For web search - enable when available
from langchain_openai import ChatOpenAI  # Compatible with DeepSeek via custom config
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Configure DeepSeek API as LLM (OpenAI-compatible)
# Base URL and model for DeepSeek
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    raise ValueError("Please set DEEPSEEK_API_KEY environment variable.")

# Custom LLM setup for DeepSeek using ChatOpenAI (via LiteLLM compatibility)
llm = ChatOpenAI(
    model="deepseek/deepseek-chat",  # Correct format for LiteLLM
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL,
    temperature=0.7,  # Balanced for creative yet factual output
    max_tokens=8000,  # Increased for longer, more detailed responses to support 1000-1500 word articles
)

# Search Tool Setup - Placeholder for future integration
# serper_tool = SerperDevTool()  # Uncomment and add to agents when crewai-tools supports it
# tools = [serper_tool]

# Define the Original Prompt/Headline
HEADLINE = "Trump reportedly asks EU to levy 100% tariffs on India and China; Ozempic maker Novo to cut 9,000 jobs – business live."
PROMPT_INSTRUCTIONS = f"""
Generate a comprehensive, SEO-optimized business news article in English based on the headline: '{HEADLINE}'.
Use available knowledge or search tools to gather recent, reliable sources for facts, context, expert analysis, and global impacts on trade, pharmaceuticals, and economies.
Ensure the article is original, fact-checked, 1000-1500 words (expanded for depth), engaging, and professional for a business audience. Expand sections with detailed analysis, historical context, multiple stakeholder perspectives, data visualizations ideas, and forward-looking scenarios.

Before writing, conduct keyword research: Identify 5-10 primary keywords, 10-15 long-tail phrases, and related LSI terms. List them with estimated search volumes, competition levels, and natural incorporation suggestions.

Structure per SEO best practices and E-E-A-T:
- Title (H1): Compelling, keyword-rich (include 1-2 primaries).
- Meta Description: 150-160 characters, including primaries and CTA (suggest at end).
- Headings: Use H2/H3/H4 for readability and depth (aim for 8-12 sub-sections).
- Introduction: Hook with key facts and broader implications, include 2-3 primaries, outline article (200-300 words).
- Body: Short paragraphs (3-5 sentences), active voice, bullets/lists/tables for impacts/quotes/data/comparisons; interweave secondary keywords/long-tails, inline citations, expert quotes, data (e.g., trade stats, market forecasts). Expand with historical parallels, stakeholder reactions, economic modeling, and interconnections between tariffs and pharma (e.g., supply chain effects). Target Flesch score 60+, mobile-friendly. Aim for 700-1000 words here.
- Conclusion: Summarize implications, forward-looking analysis (e.g., 2026 projections), include CTA (300+ words for closure).

Additional SEO: Suggest 3-5 internal links, 2-3 external links to sources, 3-5 image ideas with alt text (include charts/graphs). Maintain keyword density: 1-2% for primaries, use synonyms/variations/LSI naturally.

Ensure high-quality, unique content; paraphrase all sources and add original insights.

After the article, provide an SEO audit: Analyze keyword placement/density, readability score, mobile optimization suggestions, and backlink opportunities. Expand audit with detailed metrics and improvement plans.

Output the entire response as a structured JSON object with the following keys:
- "keyword_research": An object containing arrays for "primary_keywords", "long_tail_phrases", and "lsi_terms". Each item in the arrays should include details like estimated search volume, competition level, and incorporation suggestions.
- "article": An object with keys for "title", "meta_description", "introduction" (string, 200-300 words), "body" (array of 10+ strings for sections/paragraphs, including headings as H2/H3/H4 marked strings), and "conclusion" (string, 200-300 words).
- "seo_suggestions": An object with keys for "internal_links" (array of 3-5 suggestions), "external_links" (array of 2-3 source URLs), and "image_ideas" (array of 3-5 objects each with "description" and "alt_text").
- "seo_audit": An object with keys for "keyword_analysis" (detailed string summary of placement/density), "readability_score" (number or string, e.g., '62'), "mobile_optimization" (array of 4+ suggestions), and "backlink_opportunities" (array of 3+ ideas).

Ensure the JSON is valid, clean, and comprehensive. Current date: September 10, 2025.
"""

# Pydantic model for structured JSON output to ensure validity
class SEOArticleOutput(BaseModel):
    keyword_research: Dict[str, Any] = Field(..., description="Keyword research section")
    article: Dict[str, Any] = Field(..., description="Article structure")
    seo_suggestions: Dict[str, Any] = Field(..., description="SEO suggestions")
    seo_audit: Dict[str, Any] = Field(..., description="SEO audit")

# Agent 1: Keyword Researcher
# Role: Perform keyword research using web search for volumes, competition, etc.
keyword_researcher = Agent(
    role="SEO Keyword Researcher",
    goal="Conduct thorough keyword research for the given headline, identifying 5-10 primary keywords, 10-15 long-tail phrases, and LSI terms with estimated search volumes, competition levels (low/medium/high), and natural incorporation suggestions. Focus on business, trade, pharma topics. Expand with related sub-topics for broader coverage.",
    backstory="You are an expert SEO analyst specializing in business news keywords. You estimate volumes based on your knowledge and experience (e.g., 50k for high-volume terms like 'tariffs on China'). Provide detailed suggestions for integration across article sections.",
    tools=[],  # Placeholder for tools=[serper_tool]
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

# Task for Keyword Research
keyword_task = Task(
    description=f"Research keywords for headline: '{HEADLINE}'. Based on your knowledge, identify 5-10 primary keywords, 10-15 long-tail phrases, and LSI terms with estimated search volumes, competition levels (low/medium/high), and natural incorporation suggestions. Focus on business, trade, pharma topics. Expand list with variations for comprehensive SEO.",
    agent=keyword_researcher,
    expected_output="A dictionary-like structure with keyword_research key containing arrays of objects with keyword, volume, competition, suggestions. Aim for detailed, expansive entries.",
)

# Agent 2: Fact and Deep Researcher
# Role: Gather facts, sources, expert analysis via deep web search. Enhanced for more depth.
fact_researcher = Agent(
    role="Business News Fact Researcher",
    goal="Perform in-depth research on the headline topic. Collect extensive facts on Trump tariffs (EU 100% on China/India, Russian oil context, negotiation history), Novo Nordisk layoffs (9,000 jobs, Ozempic production, competition with Eli Lilly, supply chain details). Include expert analysis from economists/pharma analysts, trade stats (e.g., GDP impacts, bilateral volumes €500B+), pharma market data ($100B+ by 2030), historical parallels (e.g., 2018 tariffs), and global ripple effects. Provide multiple angles: US-EU relations, Asian economies, investor reactions. Date: Sept 10, 2025. Structure for expansive article use.",
    backstory="You are a seasoned business journalist with extensive knowledge of global trade, pharmaceuticals, and economic impacts. You provide well-informed, detailed analysis based on your expertise, including projections and interconnections.",
    tools=[],  # Placeholder for tools=[serper_tool]
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

fact_task = Task(
    description=f"Research the headline topic: 'Trump EU tariffs China India September 2025' and 'Novo Nordisk 9000 job cuts Ozempic 2025 reasons impacts'. Based on your knowledge, gather extensive facts, analysis, and data (e.g., trade volumes €500B, market $100B by 2030, job cut rationales like cost pressures). Include historical context, expert quotes, stakeholder views, and future scenarios. Structure for article: hooks, detailed body data (with sub-sections), citations, and interconnections (e.g., tariff effects on pharma imports). Aim for a comprehensive report to support 1000+ word article.",
    agent=fact_researcher,
    expected_output="An expansive report with sections: Trade Facts (detailed), Pharma Facts (detailed), Expert Analysis (multi-perspective), Global Impacts (bullets/lists/tables with data points), Historical Context, Future Projections.",
)

# Agent 3: Article Writer
# Role: Generate the full article using research. Enhanced for length and structure.
article_writer = Agent(
    role="Professional Business Article Writer",
    goal="Write a well-structured, logical 1000-1500 word article based on research. Create a clear narrative flow: Introduction (hook + context), Body with logical progression (Background → Current Events → Analysis → Implications), Conclusion (summary + outlook). Use proper paragraph structure, clear transitions, and coherent arguments. Avoid repetitive content and ensure each section builds on the previous one.",
    backstory="You are an experienced business journalist who writes clear, logical articles for major publications. You excel at creating coherent narratives that flow naturally from one point to the next.",
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

write_task = Task(
    description=f"Using keyword and fact research, generate a well-structured, logical article on '{HEADLINE}'. Create a clear narrative flow: 1) Introduction with hook and context, 2) Background on Trump's tariff strategy, 3) Current events and developments, 4) Analysis of economic impacts, 5) Novo Nordisk layoffs context, 6) Interconnections between events, 7) Expert perspectives, 8) Future implications, 9) Conclusion with outlook. Ensure each paragraph flows logically to the next. Avoid repetition and maintain coherence throughout.",
    agent=article_writer,
    expected_output="A well-structured article with clear narrative flow: title, meta_description, introduction (engaging hook + context), body (logical progression of 6-8 coherent sections), conclusion (summary + outlook). Each section should build naturally on the previous one.",
)

# Agent 4: SEO Auditor and JSON Formatter
# Role: Audit SEO, ensure structure, output valid JSON. Enhanced for detailed audit.
seo_auditor = Agent(
    role="SEO Auditor and JSON Structurer",
    goal="Analyze the generated content in depth: Calculate keyword density/placement (1-2%, with breakdowns), estimate Flesch score (target 60+, with factors), suggest mobile opts/backlinks with rationale. Format everything into valid JSON per schema: keyword_research, article, seo_suggestions, seo_audit. Validate cleanliness/comprehensiveness, ensure length targets met.",
    backstory="You are an SEO specialist and data validator, ensuring outputs meet best practices, JSON schema, and expanded content requirements.",
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

audit_task = Task(
    description="Take inputs from previous tasks. Audit in detail: keyword_analysis (summary with metrics), readability_score (e.g., '65', with explanation), mobile_optimization (array of 4+ suggestions with benefits), backlink_opportunities (array of 3+ ideas with targets). Compile full JSON: Integrate all sections expansively. Ensure no errors, paraphrase/expand if needed for coherence and length.",
    agent=seo_auditor,
    expected_output="A single, valid JSON string matching the exact schema in instructions. Use Pydantic if possible for validation.",
    output_pydantic=SEOArticleOutput,  # Enforce structured output
)

# Create the Crew: Hierarchical process for sequential execution
crew = Crew(
    agents=[keyword_researcher, fact_researcher, article_writer, seo_auditor],
    tasks=[keyword_task, fact_task, write_task, audit_task],
    process=Process.sequential,  # Run tasks in order, passing context (maintains initial logic)
    verbose=True,  # Detailed logging
    memory=False,  # Disabled to avoid ChromaDB issues
    share_crew=False,  # Independent agents
    manager_llm=llm,  # For any delegation (though set to False)
)

# Execute the Crew
if __name__ == "__main__":
    print("Starting CrewAI execution with DeepSeek API...")
    result = crew.kickoff(inputs={"headline": HEADLINE, "instructions": PROMPT_INSTRUCTIONS})
    
    # Parse and print the JSON output
    print("\nGenerated JSON Output:")
    
    # Extract the JSON content from the CrewOutput result
    if hasattr(result, 'raw'):
        json_content = result.raw
    else:
        json_content = result
    
    # If the content is a JSON string, parse it to Python object
    if isinstance(json_content, str):
        try:
            json_content = json.loads(json_content)
        except json.JSONDecodeError:
            print("Error: Unable to parse JSON")
            exit(1)
    
    print(json.dumps(json_content, indent=2, ensure_ascii=False))
    
    # Save to file
    with open("seo_article_output.json", "w", encoding="utf-8") as f:
        json.dump(json_content, f, indent=2, ensure_ascii=False)
    print("\nOutput saved to 'seo_article_output.json'")
    
    # Optional: Estimate word count for verification
    if 'article' in json_content:
        body_text = json_content['article'].get('introduction', '') + ' '.join(json_content['article'].get('body', [])) + json_content['article'].get('conclusion', '')
        word_count = len(body_text.split())
        print(f"\nEstimated article word count: {word_count} (target: 1000-1500)")
    
    print("\nExecution complete. Check logs for deep search details.")