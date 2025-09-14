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
from final_headline_analyzer import FinalHeadlineAnalyzer  # Final precise analysis - ZERO off-topic terms
# NOUVELLES AMÉLIORATIONS ADAPTATIVES - 100% GRATUIT
from adaptive_keyword_context import AdaptiveKeywordContextAnalyzer  # Analyse contextuelle adaptative
from advanced_keyword_tools import AdvancedKeywordResearchTool  # Outils avancés de recherche de mots-clés
from economic_data_validator import EconomicDataValidator  # Système de validation des données économiques

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
    model="deepseek/deepseek-chat",  # Correct LiteLLM format with provider
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL,
    temperature=0.7,  # Balanced for creative yet factual output
    max_tokens=8000,  # Increased for longer, more detailed responses to support 1000-1500 word articles
)

# Setup free search tools (NO API REQUIRED!)
print("🚀 INITIALIZING ADAPTIVE KEYWORD RESEARCH SYSTEM...")
print("=" * 60)

print("🔍 Initializing free search tools...")
free_search_tool = FreeSearchCrewAITool()

print("📅 Initializing data freshness validator...")
freshness_validator = DataFreshnessValidator()

print("🎯 Initializing adaptive headline analyzer...")
headline_analyzer = FinalHeadlineAnalyzer()

print("🚀 Initializing advanced keyword research tools...")
advanced_keyword_tool = AdvancedKeywordResearchTool()

print("🧠 Initializing adaptive context analyzer...")
adaptive_context_analyzer = AdaptiveKeywordContextAnalyzer()

print("🔍 Initializing advanced economic data validator...")
economic_validator = EconomicDataValidator()

# Combine all tools for agents
tools = [free_search_tool, advanced_keyword_tool]

print("✅ Free search tool ready (RSS + DuckDuckGo + Public sources)")
print("✅ Data freshness validator ready")
print("✅ Adaptive headline analyzer ready")
print("✅ Advanced keyword research tools ready (Google Trends + Autocomplete)")
print("✅ Adaptive context analyzer ready")
print("✅ Advanced economic data validator ready (Forex + Inflation + Rates + DXY + Central Banks)")
print("🎯 SYSTEM READY FOR ADAPTIVE KEYWORD RESEARCH!")
print("=" * 60)

# Define the Original Prompt/Headline
HEADLINE = "What's up next week? Central Bank decisions highlighted by the FOMC rate decision - Forex TRADING IMPLICATIONS"

# ADAPTIVE ANALYSIS SYSTEM (NO MORE HARDCODING!)
print("\n🧠 ADAPTIVE HEADLINE ANALYSIS...")
print("=" * 50)

# Analyze headline context adaptively
print(f"📋 Analyzing headline: '{HEADLINE[:50]}...'")
headline_context = adaptive_context_analyzer.detect_headline_domain(HEADLINE)
print(f"✅ Detected domain: {headline_context['primary_domain']}")
print(f"📊 Headline type: {headline_context['headline_type']}")
print(f"🎯 Confidence: {headline_context['domain_confidence']:.2f}")

# Generate adaptive search terms
print("\n🎯 Generating adaptive search terms...")
search_terms = headline_analyzer.generate_automatic_search_terms(HEADLINE)
search_terms_str = "', '".join(search_terms)

print(f"✅ Generated {len(search_terms)} adaptive search terms:")
for i, term in enumerate(search_terms[:8], 1):  # Show first 8
    print(f"   {i}. \"{term}\"")

if len(search_terms) > 8:
    print(f"   ... and {len(search_terms) - 8} more terms")

print("🚀 ADAPTIVE ANALYSIS COMPLETE - All terms generated from headline context!")
PROMPT_INSTRUCTIONS = f"""
Generate a comprehensive, SEO-optimized FOREX TRADING article in English based on the headline: '{HEADLINE}'.
Use available knowledge or search tools to gather recent, reliable sources for facts, context, expert analysis, and FOREX TRADING IMPLICATIONS related to the headline topic. The article MUST include specific trading insights, market analysis, and actionable trading strategies to drive traffic to our forex trading signals platform.

CRITICAL - ECONOMIC DATA ACCURACY REQUIREMENTS:
- Use ONLY the most recent economic data available as of September 2025
- For forex rates, use CURRENT values: EUR/USD ~1.1715, GBP/USD ~1.353, USD/JPY ~147.45
- For inflation data, use LATEST figures: CPI Headline 2.9%, CPI Core 3.1% (August 2025)
- For unemployment data, use CURRENT statistics: Unemployment Rate 4.3%, Initial Claims 240,500 (September 2025)
- For treasury yields, use LATEST values: 10Y Treasury ~4.08%, 2Y Treasury ~3.85% (September 2025)
- For Fed rates, use CURRENT range: 4.25-4.50% (effective rate: 4.33%)
- For rate probabilities, use LATEST market pricing: Fed hold ~15%, Fed cut 25bp ~80%, Fed cut 50bp ~5%
- For DXY index, use CURRENT value: ~97.61 (as of September 12, 2025)
- For central bank meetings, use CORRECT dates: FOMC September 16-17, BoC September 17
- For expert citations, ONLY quote recognized analysts from reputable organizations
- Double-check ALL economic figures before including them in the article
- Avoid using outdated or incorrect economic data that could mislead traders

Ensure the article is original, fact-checked, 1000-1500 words (expanded for depth), PROFESSIONAL in tone, and targeted for a sophisticated FOREX TRADER audience. Expand sections with detailed technical analysis, chart patterns, support/resistance levels, and specific currency pair implications (EUR/USD, GBP/USD, USD/JPY).

Before writing, conduct keyword research: Identify 5-10 primary keywords (MUST include forex trading terms), 10-15 long-tail phrases, and related LSI terms. List them with estimated search volumes, competition levels, and natural incorporation suggestions.

Structure per SEO best practices and E-E-A-T:
- Title (H1): CREATE A NEW SEO-optimized title (50-60 characters) using keyword research data. DO NOT use the original headline. Make it compelling, keyword-rich (include 1-2 primary keywords), and optimized for search engines. MUST include trading/forex relevance.
- Meta Description: 150-160 characters, including primaries and CTA directing to our forex trading signals platform.
- Headings: Use H2/H3/H4 for readability and depth (aim for 8-12 sub-sections). Include specific trading-focused headings.
- Introduction: Hook with key facts and TRADING IMPLICATIONS, include 2-3 primaries, outline article (200-300 words). Establish professional authority immediately.
- Body: Write in PROFESSIONAL, AUTHORITATIVE style with precise technical language appropriate for traders. Include specific trading strategies, technical analysis, and market projections. Maintain professional tone while being engaging. Include data-driven insights, chart pattern analysis, and specific currency pair impacts. Target sophisticated traders who understand market mechanics. Aim for 700-1000 words of high-value trading content.
- Conclusion: Summarize trading implications, forward-looking analysis (e.g., 2026 projections), include CTA directing to our forex signals platform (300+ words for closure).

Additional SEO: Suggest 3-5 internal links to trading resources, 2-3 external links to authoritative financial sources, 3-5 image ideas with alt text (MUST include forex charts/technical analysis visuals). Maintain keyword density: 1-2% for primaries, use trading terminology naturally.

Ensure high-quality, unique content; paraphrase all sources and add original expert trading insights.

After the article, provide an SEO audit: Analyze keyword placement/density, readability score, mobile optimization suggestions, and backlink opportunities. Expand audit with detailed metrics and improvement plans.

Output the entire response as a structured JSON object with the following keys:
- "keyword_research": An object containing arrays for "primary_keywords", "long_tail_phrases", and "lsi_terms". Each item in the arrays should include details like estimated search volume, competition level, and incorporation suggestions. MUST include forex/trading specific keywords.
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
    image_generation_prompt: str = Field(..., description="Detailed prompt for AI image generation based on article content")

# ===================================================================
# ADAPTIVE AGENT CREATION FUNCTIONS (NO MORE HARDCODING!)
# ===================================================================

def create_adaptive_keyword_researcher(headline: str, context: Dict[str, Any]) -> Agent:
    """Crée un agent de recherche de mots-clés adapté au headline et contexte spécifiques"""
    
    # Adapter le goal selon le contexte détecté
    domain = context.get('primary_domain', 'general_business')
    headline_type = context.get('headline_type', 'general_business_news')
    
    adaptive_goal = f"""
    🎯 ADAPTIVE KEYWORD RESEARCH for: '{headline}'
    
    DETECTED CONTEXT:
    - Domain: {domain}
    - Type: {headline_type} 
    - Confidence: {context.get('domain_confidence', 0):.2f}
    
    ADAPTIVE STRATEGY - Conduct comprehensive keyword research tailored to this specific context:
    
    1. 📊 PRIMARY KEYWORDS (15-25): Use BOTH search tools to discover trending terms
       • Free web search tool: Get current news and discussions
       • Advanced keyword tool: Get Google Trends data and autocomplete suggestions
    
    2. 🎯 LONG-TAIL EXPANSION (30-50): Generate based on discovered patterns
       • Question-based keywords adapted to headline type
       • Contextual modifiers based on detected domain
       • Trending combinations from real search data
    
    3. 📈 VOLUME & COMPETITION ANALYSIS: 
       • Use advanced tool for Google Trends analysis
       • Estimate search volumes via multiple signals
       • Analyze competition levels from SERP data
    
    4. 🚀 ADAPTIVE RECOMMENDATIONS:
       • Prioritize keywords by business impact and ranking opportunity
       • Provide implementation strategy adapted to content type
       • Include seasonal trends and search patterns
    
    CRITICAL: Everything must adapt to the headline content. NO generic patterns!
    """
    
    adaptive_backstory = f"""
    You are an advanced SEO strategist with adaptive intelligence, analyzing: '{headline[:50]}...'
    
    Your expertise automatically adjusts to content context:
    • For {domain} domain → You focus on relevant industry terminology and audience
    • For {headline_type} type → You adapt keyword strategy to content format
    
    TOOLS AT YOUR DISPOSAL:
    1. Free Web Search Tool → Real-time news, trends, current discussions
    2. Advanced Keyword Tool → Google Trends, autocomplete, volume estimation
    
    METHOD:
    - Discover what people are ACTUALLY searching for related to this headline
    - Use real data to validate keyword opportunities
    - Combine multiple signals for accurate volume estimation
    - Adapt strategy based on discovered patterns, not predetermined lists
    
    You excel at finding the perfect balance between search volume and ranking opportunity.
    """
    
    return Agent(
        role=f"Adaptive SEO Keyword Researcher ({domain.replace('_', ' ').title()})",
        goal=adaptive_goal,
        backstory=adaptive_backstory,
        tools=tools,  # Utilise les nouveaux outils adaptatifs
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

def create_adaptive_keyword_task(headline: str, context: Dict[str, Any], agent: Agent) -> Task:
    """Crée une tâche de recherche adaptée au headline et contexte"""
    
    domain = context.get('primary_domain', 'general_business')
    extracted_patterns = context.get('extracted_patterns', {})
    
    # Extraire les entités clés pour la tâche
    key_entities = extracted_patterns.get('organizations', [])[:3]
    key_data = extracted_patterns.get('measurements', [])[:2]
    key_time = extracted_patterns.get('time_indicators', [])[:2]
    
    adaptive_description = f"""
    🚀 COMPREHENSIVE ADAPTIVE KEYWORD RESEARCH 
    
    TARGET HEADLINE: '{headline}'
    DETECTED CONTEXT: {domain} | {context.get('headline_type', 'general')}
    KEY ENTITIES: {', '.join(key_entities) if key_entities else 'Auto-detected from headline'}
    DATA POINTS: {', '.join(key_data) if key_data else 'None'}
    TIME CONTEXT: {', '.join(key_time) if key_time else 'Current'}
    
    📋 RESEARCH PHASES:
    
    PHASE 1 - CONTEXTUAL DISCOVERY:
    • Use FREE WEB SEARCH TOOL to find current discussions about: {', '.join(key_entities[:3]) if key_entities else 'headline topics'}
    • Analyze how people currently discuss this topic
    • Extract vocabulary from real search results and news sources
    
    PHASE 2 - ADVANCED KEYWORD MINING:
    • Use ADVANCED KEYWORD RESEARCH TOOL for:
      - Google Trends data analysis
      - Autocomplete suggestions (Google/Bing)
      - Question-based keyword generation
      - Competition difficulty analysis
    
    PHASE 3 - ADAPTIVE EXPANSION:
    • Generate keyword variations based on discovered patterns
    • Create long-tail phrases using real terminology found in research
    • Build semantic keyword clusters around main concepts
    • Include seasonal and trending modifiers
    
    PHASE 4 - STRATEGIC ANALYSIS:
    • Estimate search volumes using multiple signals
    • Analyze keyword difficulty and competition
    • Prioritize by ranking opportunity vs business value
    • Provide integration suggestions for natural content placement
    
    📊 DELIVERABLE REQUIREMENTS:
    - 50+ keywords with volume estimates and difficulty scores
    - Clear categorization by search intent and business value
    - Implementation roadmap with priority recommendations
    - Trend analysis and seasonal considerations
    
    CRITICAL SUCCESS FACTORS:
    ✅ All keywords must be relevant to the headline topic
    ✅ Use BOTH search tools for comprehensive coverage
    ✅ Base everything on real search data, not assumptions
    ✅ Adapt terminology to discovered audience language
    ✅ Provide actionable implementation guidance
    """
    
    return Task(
        description=adaptive_description,
        agent=agent,
        expected_output=f"Comprehensive adaptive keyword strategy for '{headline}' with 50+ researched keywords, volume estimates, competition analysis, and strategic implementation recommendations based on {domain} domain context."
    )

# ===================================================================
# CREATE ADAPTIVE KEYWORD RESEARCH SYSTEM
# ===================================================================

print("\n🎯 CREATING ADAPTIVE KEYWORD RESEARCH SYSTEM...")
keyword_researcher = create_adaptive_keyword_researcher(HEADLINE, headline_context)
print("✅ Adaptive keyword researcher created and configured")

# Create Adaptive Keyword Task
print("🎯 Creating adaptive keyword research task...")
keyword_task = create_adaptive_keyword_task(HEADLINE, headline_context, keyword_researcher)
print("✅ Adaptive keyword task created and configured")

# Agent 2: Fact and Deep Researcher with Forex Trading Focus
# Role: Gather facts, sources, expert analysis via deep web search with forex trading implications.
fact_researcher = Agent(
    role="Forex Trading Market Analyst",
    goal="Perform in-depth research on the headline topic using the FREE search tool to get real-time data WITH SPECIFIC FOREX TRADING IMPLICATIONS! Collect extensive facts on economic events, central bank decisions, and geopolitical developments. CRITICAL: For each fact, analyze specific impacts on major currency pairs (EUR/USD, GBP/USD, USD/JPY), identify key support/resistance levels, and note relevant technical indicators. Search for recent news, expert trading analysis, market data, and potential trading opportunities. Get current information from forex-specific sources, trading platforms, and financial news.",
    backstory="You are a professional forex market analyst with deep expertise in fundamental and technical analysis. You understand how macroeconomic news impacts currency markets and can identify specific trading opportunities from headline events. You actively use search functionality to gather the most current information from trading sources, financial news, and market data to provide actionable insights for forex traders.",
    tools=tools,  # Utilise l'outil de recherche gratuit
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

# AUTOMATIC FACTS TASK GENERATION (No more hardcoding!)
fact_task_description = headline_analyzer.generate_automatic_task_description(HEADLINE, "facts")

fact_task = Task(
    description=f"{fact_task_description}\n\nCRITICAL FOREX TRADING REQUIREMENTS:\n- For EACH fact or news item, analyze specific impacts on major currency pairs (EUR/USD, GBP/USD, USD/JPY)\n- Identify key support/resistance levels relevant to the headline topic\n- Note technical indicators (RSI, MACD, Moving Averages) that traders should monitor\n- Analyze potential trading scenarios based on the news (bullish/bearish outlook)\n- Include expert opinions from forex analysts and trading strategists\n- Research historical market reactions to similar events for trading context\n- Identify specific entry/exit points and risk management considerations\n\nECONOMIC DATA ACCURACY REQUIREMENTS:\n- VERIFY all economic data with the most recent sources available\n- Use ONLY the following CURRENT economic data (September 2025):\n  * Forex Rates: EUR/USD ~1.1715, GBP/USD ~1.353, USD/JPY ~147.45\n  * Inflation: CPI Headline 2.9%, CPI Core 3.1% (August 2025)\n  * Unemployment: Rate 4.3%, Initial Claims 240,500 (September 2025)\n  * Treasury Yields: 10Y ~4.08%, 2Y ~3.85% (September 2025)\n- Cross-check all data points with multiple sources before including them\n- For any data not listed above, ensure it's from the most recent publications (September 2025)\n- Clearly indicate the date/source of ALL economic data mentioned in your analysis\n- NEVER use outdated economic figures that could lead to incorrect trading decisions",
    agent=fact_researcher,
    expected_output="A professional forex market analysis report based on current web search results, including: 1) Comprehensive facts about the headline topic using VERIFIED current economic data, 2) Specific impacts on major currency pairs with accurate rates, 3) Key technical levels and indicators, 4) Trading scenarios with entry/exit points, 5) Expert analyst opinions, and 6) Historical market context - all with proper source citations and date verification.",
)

# Agent 3: Data Freshness Validator
# Role: Valider la fraîcheur des données et recommander des améliorations
freshness_agent = Agent(
    role="Data Freshness Validator",
    goal="Analyze the freshness of collected data and ensure the article uses only recent and relevant information. Identify outdated sources and recommend additional research if necessary. Calculate freshness metrics for the final SEO audit.",
    backstory="You are a data validation expert with particular expertise in content freshness for SEO. You know that Google favors recent and up-to-date content. You analyze publication dates, assess temporal relevance of information, and filter out outdated data.",
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

freshness_task = Task(
    description="ANALYZE the freshness of all data collected by the research agent. Identify sources older than 30 days for news content, 90 days for business analysis. Calculate a global freshness score. Recommend additional research if too many sources are outdated. Prepare a freshness report with metrics for the final SEO audit (average source age, percentage of recent sources, global freshness score).",
    agent=freshness_agent,
    expected_output="A freshness validation report with global score, age distribution of sources, improvement recommendations, and detailed metrics for the final SEO audit.",
)

# Agent 4: Article Writer
# Role: Generate the full article using research. Enhanced for professional forex trading content.
article_writer = Agent(
    role="Professional Forex Trading Content Specialist",
    goal="Write a professional, authoritative 1200-1800 word forex trading article that demonstrates expert market analysis while maintaining reader engagement. CRITICAL: Create an SEO-optimized title (50-60 characters) using keyword research data, NOT the original headline. Write with precision, data-driven insights, and technical analysis that establishes credibility with sophisticated traders. Every paragraph must deliver valuable trading insights while driving traffic to our forex signals platform.",
    backstory="You are a seasoned forex market analyst and trading expert with years of experience in financial markets. You understand both technical and fundamental analysis, and can translate complex market movements into actionable trading strategies. You write with authority and precision while keeping content accessible to traders of all levels. Your articles combine professional market analysis with clear explanations that help traders make informed decisions. You excel at connecting macroeconomic news to specific forex pair movements and trading opportunities.",
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

write_task = Task(
    description=f"""Write a professional, authoritative forex trading article about '{HEADLINE}' that delivers expert market analysis while maintaining reader engagement. 

CRITICAL: CREATE A NEW SEO-OPTIMIZED TITLE (50-60 characters) using keyword research data - DO NOT copy the original headline. MUST include forex/trading relevance.

PROFESSIONAL FOREX CONTENT REQUIREMENTS:
- START with authoritative market context and clear trading implications that establish expertise
- Include specific technical analysis: support/resistance levels, chart patterns, key indicators (RSI, MACD, etc.)
- Analyze impact on major currency pairs: EUR/USD, GBP/USD, USD/JPY, etc.
- Provide data-driven insights with precise figures, percentages, and market movements
- Include expert quotes or consensus views from reputable market analysts
- Connect macroeconomic news to specific forex trading opportunities
- End with 2-3 ACTIONABLE trading strategies readers can implement, with specific entry/exit points

PROFESSIONAL WRITING STYLE:
- Write with authority and precision that demonstrates market expertise
- Use professional trading terminology correctly and appropriately
- Balance technical analysis with clear explanations for traders of all levels
- Maintain professional tone while being engaging and accessible
- Include evidence-based statements with proper market reasoning
- Use "traders should consider" instead of "you should" for professional distance
- Reference historical market patterns and precedents when relevant

STRUCTURED CONTENT:
- Professional introduction establishing market context and trading relevance (2-3 paragraphs)
- 6-8 body sections with informative H2 headings focused on analysis and strategy
- Within each section: H3 subheadings, bullet points for key trading insights, important data in bold
- Comprehensive conclusion with specific trading outlook and strategies
- Include a final CTA directing to our forex signals platform

PROFESSIONAL ENGAGEMENT ELEMENTS:
- Start each section with a clear market insight or analytical point
- Include "Trading Implications:" subsections within major points
- Add timely relevance: "Current market conditions indicate..." "This week's trading outlook..."
- Professional stakes: "Traders positioned in EUR/USD should note..." "Risk management suggests..."

Focus on delivering professional forex trading analysis and actionable insights that establish expertise while driving traffic to our forex signals platform.""",
    agent=article_writer,
    expected_output="A professional, authoritative forex trading article with: 1) NEW SEO title (50-60 chars) with forex relevance, 2) compelling meta description with CTA to our platform, 3) expert introduction establishing market context, 4) detailed technical analysis with specific currency pair implications, 5) conclusion with actionable trading strategies and platform CTA. Content should demonstrate forex expertise while remaining engaging and accessible to traders.",
)

# Agent 5: AI Image Generation Prompt Creator
# Role: Create detailed prompts for AI image generation based on article content
image_prompt_creator = Agent(
    role="AI Image Generation Specialist",
    goal="Create a detailed, specific prompt for AI image generation tools (DALL-E, Midjourney, Stable Diffusion) based on the article content. The prompt should capture the key visual elements, mood, style, and context of the article to generate a compelling, relevant image that enhances the article's impact.",
    backstory="You are a visual storytelling expert who understands how to translate complex business and economic concepts into compelling visual prompts. You know how to create prompts that generate professional, engaging images that perfectly complement written content and enhance reader engagement.",
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

# Agent 6: SEO Auditor and JSON Formatter
# Role: Audit SEO, ensure structure, output valid JSON. Enhanced for detailed audit with freshness metrics.
seo_auditor = Agent(
    role="SEO Auditor and JSON Structurer",
    goal="Analyze the generated content in depth: Calculate keyword density/placement (1-2%, with breakdowns), estimate Flesch score (target 60+, with factors), suggest mobile opts/backlinks with rationale. INTEGRATE freshness validation results into the SEO audit - include data freshness scores, source age distribution, and freshness impact on SEO performance. Format everything into valid JSON per schema: keyword_research, article, seo_suggestions, seo_audit (with freshness metrics), image_generation_prompt.",
    backstory="You are an SEO specialist and data validator with expertise in content freshness validation. You understand that Google rewards fresh, up-to-date content and you incorporate data age and freshness metrics into comprehensive SEO audits.",
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

# Task for Image Generation Prompt
image_task = Task(
    description=f"""Create a detailed AI image generation prompt based on the article content about '{HEADLINE}'. 

REQUIREMENTS:
- Analyze the article's main themes, key concepts, and emotional tone
- Create a prompt that captures the economic/financial context (inflation, job market, consumer impact)
- Include specific visual elements: charts, graphs, people, urban settings, financial symbols
- Specify style: professional, modern, clean, business-focused
- Include mood: serious but accessible, concerned but not alarmist
- Add technical specifications: high resolution, professional photography style, good lighting
- Make it suitable for DALL-E, Midjourney, or Stable Diffusion

The prompt should be 2-3 sentences, detailed enough to generate a compelling image that would work as a hero image for this economic news article.""",
    agent=image_prompt_creator,
    expected_output="A detailed, specific prompt for AI image generation that captures the article's essence and would create a compelling visual representation of the economic concepts discussed.",
)

audit_task = Task(
    description="Take inputs from ALL previous tasks including freshness validation and image generation prompt. CRITICAL: Include the COMPLETE ARTICLE TEXT (introduction, body paragraphs, conclusion) in the article section, not just metadata. Audit in detail: keyword_analysis (summary with metrics), readability_score (e.g., '65', with explanation), mobile_optimization (array of 4+ suggestions with benefits), backlink_opportunities (array of 3+ ideas with targets). CRITICAL: Include comprehensive freshness metrics in seo_audit: data_freshness_score, source_age_distribution, freshness_impact_on_seo, recommendations_for_freshness. Include the image_generation_prompt from the image task. Compile full JSON with COMPLETE article content: Integrate all sections including freshness validation results, the full article text, and the image generation prompt. Ensure no errors, validate schema compliance.",
    agent=seo_auditor,
    expected_output="A single, valid JSON string matching the exact schema with COMPLETE article content (title, meta_description, introduction, body array, conclusion), ENHANCED seo_audit section including detailed freshness metrics, and image_generation_prompt for AI image creation.",
    output_pydantic=SEOArticleOutput,  # Enforce structured output
)

# Create the Crew: Hierarchical process for sequential execution with freshness validation and image generation
crew = Crew(
    agents=[keyword_researcher, fact_researcher, freshness_agent, article_writer, image_prompt_creator, seo_auditor],
    tasks=[keyword_task, fact_task, freshness_task, write_task, image_task, audit_task],
    process=Process.sequential,  # Run tasks in order: keywords → facts → freshness validation → writing → image prompt → audit
    verbose=True,  # Detailed logging
    memory=False,  # Disabled to avoid ChromaDB issues
    share_crew=False,  # Independent agents
    manager_llm=llm,  # For any delegation (though set to False)
)

# Execute the Crew
if __name__ == "__main__":
    print("Starting CrewAI execution with adaptive headline analysis...")
    print(f"Processing headline: {HEADLINE[:50]}...")
    print(f"Using {len(search_terms)} dynamically generated search terms")
    
    result = crew.kickoff(inputs={"headline": HEADLINE, "instructions": PROMPT_INSTRUCTIONS})
    
    # Parse and print the JSON output
    print("\nGenerated JSON Output:")
    
    # Extract the JSON content from the CrewOutput result
    if hasattr(result, 'raw'):
        json_content = result.raw
    else:
        json_content = result
    
    # Handle different result types
    if isinstance(json_content, str):
        try:
            json_content = json.loads(json_content)
        except json.JSONDecodeError:
            print("❌ Error: Unable to parse JSON")
            print(f"Raw content: {json_content[:500]}...")
            exit(1)
    elif hasattr(json_content, 'dict'):
        json_content = json_content.dict()
    elif not isinstance(json_content, dict):
        print("❌ Error: Unexpected result format")
        print(f"Result type: {type(json_content)}")
        print(f"Result content: {str(json_content)[:500]}...")
        exit(1)
    
    print(json.dumps(json_content, indent=2, ensure_ascii=False))
    
    # Valider les données économiques de l'article
    print("\n🔍 VALIDATION AVANCÉE DES DONNÉES ÉCONOMIQUES...")
    article_content = ""
    if 'article' in json_content:
        article_content = json_content['article'].get('introduction', '') + ' '.join(json_content['article'].get('body', [])) + json_content['article'].get('conclusion', '')
    
    validation_results = economic_validator.validate_article_data(article_content)
    
    # Ajouter les résultats de validation à la sortie JSON
    json_content['economic_data_validation'] = validation_results
    
    # Afficher un résumé des résultats de validation
    print(f"✅ Validation des données économiques terminée - Précision: {validation_results['overall_accuracy']}%")
    
    # Afficher les détails des données inexactes
    inaccurate_data = []
    categories = [
        "forex_rates", "inflation_data", "unemployment_data", "treasury_yields",
        "fed_meetings", "fed_rates", "rate_probabilities", "dxy_index",
        "other_central_banks", "expert_citations"
    ]
    
    for category in categories:
        if category in validation_results:
            for detail in validation_results[category]["details"]:
                if not detail.get("is_accurate", False):
                    if "pair" in detail:
                        inaccurate_data.append(f"{detail['pair']}: Article={detail['article_value']}, Actuel={detail['current_value']}")
                    elif "metric" in detail:
                        inaccurate_data.append(f"{detail['metric']}: Article={detail['article_value']}, Actuel={detail['current_value']}")
                    elif "tenor" in detail:
                        inaccurate_data.append(f"{detail['tenor']}: Article={detail['article_value']}%, Actuel={detail['current_value']}%")
                    elif "type" in detail:
                        type_name = detail['type']
                        if "fomc_meeting" in type_name:
                            inaccurate_data.append(f"FOMC Meeting: Article={detail['article_value']}, Actuel={detail['current_value']}")
                        elif "fed_rate" in type_name:
                            inaccurate_data.append(f"Fed Rate: Article={detail['article_value']}, Actuel={detail['current_value']}")
                        elif "prob" in type_name:
                            inaccurate_data.append(f"Rate Probability: Article={detail['article_value']}, Actuel={detail['current_value']}")
                        elif "dxy" in type_name:
                            inaccurate_data.append(f"DXY Index: Article={detail['article_value']}, Actuel={detail['current_value']}")
                        elif "boc" in type_name or "ecb" in type_name or "boe" in type_name:
                            inaccurate_data.append(f"Central Bank: Article={detail['article_value']}, Actuel={detail['current_value']}")
                        elif "expert" in type_name:
                            inaccurate_data.append(f"Expert Citation: {detail.get('expert', 'Unknown')}")
                        else:
                            inaccurate_data.append(f"{type_name}: Article={detail['article_value']}, Actuel={detail['current_value']}")
    
    if inaccurate_data:
        print("\n⚠️ DONNÉES ÉCONOMIQUES INEXACTES DÉTECTÉES:")
        for item in inaccurate_data:
            print(f"   - {item}")
    else:
        print("✅ Toutes les données économiques sont exactes et à jour!")
    
    # Save to file
    with open("seo_article_output.json", "w", encoding="utf-8") as f:
        json.dump(json_content, f, indent=2, ensure_ascii=False)
    print("\nOutput saved to 'seo_article_output.json'")
    
    # Verify title optimization
    if 'article' in json_content:
        generated_title = json_content['article'].get('title', '')
        title_length = len(generated_title)
        
        word_count = len(article_content.split())
        
        print(f"\nARTICLE METRICS:")
        print(f"   Generated title: \"{generated_title}\"")
        print(f"   Title length: {title_length} chars ({'Optimal' if title_length <= 60 else 'Too long'})")
        print(f"   Word count: {word_count} (target: 1000-1500)")
        print(f"   Economic data accuracy: {validation_results['overall_accuracy']}%")
        
        # Verify title is different from headline
        if generated_title.lower() != HEADLINE.lower():
            print(f"   Title successfully generated (different from headline)")
        else:
            print(f"   Title same as headline - optimization needed")
    
    print(f"\n✅ ADAPTIVE KEYWORD RESEARCH SYSTEM EXECUTION COMPLETE!")
    print("=" * 70)
    print(f"🎯 Headline analyzed: {HEADLINE[:50]}...")
    print(f"📊 Detected domain: {headline_context['primary_domain']}")
    print(f"📋 Headline type: {headline_context['headline_type']}")
    print(f"🔍 Search terms generated: {len(search_terms)} (adaptively from context)")
    print(f"🚀 Advanced tools used: Google Trends + Autocomplete + Competition Analysis")
    print("💡 All keywords adapted specifically to headline content - NO hardcoding!")
    print("=" * 70)