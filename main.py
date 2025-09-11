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
from typing import Dict, Any, List
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI  # Compatible with DeepSeek via custom config
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from free_search_tools import FreeSearchCrewAITool  # Recherche web gratuite sans API
from freshness_validator import DataFreshnessValidator  # Validation fraîcheur données

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

# Configuration de l'outil de recherche gratuit (AUCUNE API REQUISE!)
print("🔧 Initialisation de l'outil de recherche gratuit...")
free_search_tool = FreeSearchCrewAITool()
print("📅 Initialisation du validateur de fraîcheur...")
freshness_validator = DataFreshnessValidator()
tools = [free_search_tool]
print("✅ Outil de recherche gratuit prêt (RSS + DuckDuckGo + Sources publiques)")
print("✅ Validateur de fraîcheur des données prêt")

# Define the Original Prompt/Headline
HEADLINE = "Trump’s pressure on Europe to slap 100% tariffs on India and China raises eyebrows"
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
- "article": An object with keys for "title", "meta_description", "introduction" (string, 200-300 words), "body" (array of 10+ strings for sections/paragraphs, including headings as H2/H3/H4 marked strings), and "conclusion" (string, 200-300 words). CRITICAL: Include the full article text content, not just metadata.
- "seo_suggestions": An object with keys for "internal_links" (array of 3-5 suggestions), "external_links" (array of 2-3 source URLs), and "image_ideas" (array of 3-5 objects each with "description" and "alt_text").
- "seo_audit": An object with keys for "keyword_analysis" (detailed string summary of placement/density), "readability_score" (number or string, e.g., '62'), "mobile_optimization" (array of 4+ suggestions), and "backlink_opportunities" (array of 3+ ideas).

Ensure the JSON is valid, clean, and comprehensive. Current date: September 10, 2025.
"""

# Pydantic model for structured JSON output to ensure validity
class ArticleContent(BaseModel):
    title: str = Field(..., description="Article title")
    meta_description: str = Field(..., description="SEO meta description")
    introduction: str = Field(..., description="Article introduction text (200-300 words)")
    body: List[str] = Field(..., description="Array of article body sections including H2/H3/H4 headings")
    conclusion: str = Field(..., description="Article conclusion text (200-300 words)")

class SEOArticleOutput(BaseModel):
    keyword_research: Dict[str, Any] = Field(..., description="Keyword research section")
    article: ArticleContent = Field(..., description="Complete article structure with full content")
    seo_suggestions: Dict[str, Any] = Field(..., description="SEO suggestions")
    seo_audit: Dict[str, Any] = Field(..., description="SEO audit with freshness metrics")

# Agent 1: Keyword Researcher
# Role: Perform keyword research using web search for volumes, competition, etc.
keyword_researcher = Agent(
    role="SEO Keyword Researcher",
    goal="Conduct thorough keyword research for the given headline, identifying 5-10 primary keywords, 10-15 long-tail phrases, and LSI terms with estimated search volumes, competition levels (low/medium/high), and natural incorporation suggestions. Focus on business, trade, pharma topics. Expand with related sub-topics for broader coverage. USE the search tool to get real-time trend data!",
    backstory="You are an expert SEO analyst specializing in business news keywords. You have access to real-time web search tools to validate keyword trends and competition. Use the free search tool to check current news and trends around the topic.",
    tools=tools,  # Utilise l'outil de recherche gratuit
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

# Task for Keyword Research
keyword_task = Task(
    description=f"FIRST: Use the search tool to find current trending topics related to: '{HEADLINE}'. Search for terms like 'Trump tariffs', 'EU China trade', 'Novo Nordisk layoffs', 'Ozempic market'. Then analyze the search results to identify 5-10 primary keywords, 10-15 long-tail phrases, and LSI terms based on what's currently trending in news. Include estimated search volumes, competition levels, and natural incorporation suggestions.",
    agent=keyword_researcher,
    expected_output="A comprehensive keyword analysis based on real search data, including trending terms found in current news sources.",
)

# Agent 2: Fact and Deep Researcher
# Role: Gather facts, sources, expert analysis via deep web search. Enhanced for more depth.
fact_researcher = Agent(
    role="Business News Fact Researcher",
    goal="Perform in-depth research on the headline topic using the FREE search tool to get real-time data! Collect extensive facts on Trump tariffs (EU 100% on China/India, Russian oil context, negotiation history), Novo Nordisk layoffs (9,000 jobs, Ozempic production, competition with Eli Lilly, supply chain details). Search for recent news, expert analysis, trade statistics, market data, and economic impacts. Get current information from RSS feeds and news sources.",
    backstory="You are a seasoned business journalist with access to real-time web search tools. You actively use the search functionality to gather the most current information from news sources, RSS feeds, and public data before writing your analysis.",
    tools=tools,  # Utilise l'outil de recherche gratuit
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

fact_task = Task(
    description=f"MANDATORY: Use the search tool extensively! Search for: 'Trump tariffs EU China India 2025', 'Novo Nordisk layoffs 9000 jobs', 'Ozempic competition Eli Lilly', 'pharmaceutical market trends 2025'. Gather real-time information from news sources, RSS feeds, and recent publications. Extract facts, expert quotes, market data, trade statistics, and economic impacts. Cross-reference multiple sources and include recent developments, stakeholder reactions, and market analysis. Build a comprehensive fact base with current citations.",
    agent=fact_researcher,
    expected_output="A fact-rich report based on current web search results, including recent news articles, market data, expert opinions, and up-to-date statistics with proper source citations.",
)

# Agent 3: Data Freshness Validator
# Role: Valider la fraîcheur des données et recommander des améliorations
freshness_agent = Agent(
    role="Data Freshness Validator",
    goal="Analyser la fraîcheur des données collectées et s'assurer que l'article utilisera uniquement des informations récentes et pertinentes. Identifier les sources obsolètes et recommander des recherches complémentaires si nécessaire. Calculer des métriques de fraîcheur pour l'audit SEO final.",
    backstory="Vous êtes un expert en validation de données avec une expertise particulière dans la fraîcheur du contenu pour le SEO. Vous savez que Google privilégie le contenu récent et à jour. Vous analysez les dates de publication, évaluez la pertinence temporelle des informations et filtrez les données obsolètes.",
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

freshness_task = Task(
    description="ANALYSER la fraîcheur de toutes les données collectées par l'agent de recherche. Identifier les sources datées de plus de 30 jours pour les actualités, 90 jours pour les analyses business. Calculer un score de fraîcheur global. Recommander des recherches supplémentaires si trop de sources sont obsolètes. Préparer un rapport de fraîcheur avec métriques pour l'audit SEO (âge moyen des sources, pourcentage de sources récentes, score de fraîcheur global).",
    agent=freshness_agent,
    expected_output="Un rapport de validation de fraîcheur avec score global, distribution par âge des sources, recommandations d'amélioration, et métriques détaillées pour l'audit SEO final.",
)

# Agent 4: Article Writer
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

# Agent 5: SEO Auditor and JSON Formatter
# Role: Audit SEO, ensure structure, output valid JSON. Enhanced for detailed audit with freshness metrics.
seo_auditor = Agent(
    role="SEO Auditor and JSON Structurer",
    goal="Analyze the generated content in depth: Calculate keyword density/placement (1-2%, with breakdowns), estimate Flesch score (target 60+, with factors), suggest mobile opts/backlinks with rationale. INTEGRATE freshness validation results into the SEO audit - include data freshness scores, source age distribution, and freshness impact on SEO performance. Format everything into valid JSON per schema: keyword_research, article, seo_suggestions, seo_audit (with freshness metrics).",
    backstory="You are an SEO specialist and data validator with expertise in content freshness validation. You understand that Google rewards fresh, up-to-date content and you incorporate data age and freshness metrics into comprehensive SEO audits.",
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

audit_task = Task(
    description="Take inputs from ALL previous tasks including freshness validation. CRITICAL: Include the COMPLETE ARTICLE TEXT (introduction, body paragraphs, conclusion) in the article section, not just metadata. Audit in detail: keyword_analysis (summary with metrics), readability_score (e.g., '65', with explanation), mobile_optimization (array of 4+ suggestions with benefits), backlink_opportunities (array of 3+ ideas with targets). CRITICAL: Include comprehensive freshness metrics in seo_audit: data_freshness_score, source_age_distribution, freshness_impact_on_seo, recommendations_for_freshness. Compile full JSON with COMPLETE article content: Integrate all sections including freshness validation results and the full article text. Ensure no errors, validate schema compliance.",
    agent=seo_auditor,
    expected_output="A single, valid JSON string matching the exact schema with COMPLETE article content (title, meta_description, introduction, body array, conclusion) and ENHANCED seo_audit section including detailed freshness metrics.",
    output_pydantic=SEOArticleOutput,  # Enforce structured output
)

# Create the Crew: Hierarchical process for sequential execution with freshness validation
crew = Crew(
    agents=[keyword_researcher, fact_researcher, freshness_agent, article_writer, seo_auditor],
    tasks=[keyword_task, fact_task, freshness_task, write_task, audit_task],
    process=Process.sequential,  # Run tasks in order: keywords → facts → freshness validation → writing → audit
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