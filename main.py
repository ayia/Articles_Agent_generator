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

# Combine all tools for agents
tools = [free_search_tool, advanced_keyword_tool]

print("✅ Free search tool ready (RSS + DuckDuckGo + Public sources)")
print("✅ Data freshness validator ready")
print("✅ Adaptive headline analyzer ready")
print("✅ Advanced keyword research tools ready (Google Trends + Autocomplete)")
print("✅ Adaptive context analyzer ready")
print("🎯 SYSTEM READY FOR ADAPTIVE KEYWORD RESEARCH!")
print("=" * 60)

# Define the Original Prompt/Headline
HEADLINE = "Gold is testing the top of the daily range. It's up $15 to $3649 today and perked up following the softer UMich consumer sentiment data.The precious metal is consolidating now after reaching $3675 on Tuesday in a spike higher. It's likely to continue sideways until Wednesday's FOMC decision. A dovish bent from the Fed chair would be a green light for the gold bulls to take it another leg higher. I don't think we'd need to see a surprise 50 bps cut but if Powell validates employment concerns and downplays inflation then it could continue the surge.Techncially, Tuesday's high and overbought conditions are the only thing standing in the way of further gains and beyond that it will be big round figures like $3750 and $4000 offering up resistance.On the geopolitical side, the US appears to be trying to ramp up pressure on Russia to enter talks on Ukraine peace. That presents two-sided risks as harsher Russian sanctions or reserve confiscation could strengthen the case for gold, while a peace deal would weaken it. My sense is that Trump has played his best cards in terms of diplomacy but Russia isn't interested and feels it has the upper hand in the war."

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
Generate a comprehensive, SEO-optimized business news article in English based on the headline: '{HEADLINE}'.
Use available knowledge or search tools to gather recent, reliable sources for facts, context, expert analysis, and relevant economic impacts related to the headline topic.
Ensure the article is original, fact-checked, 1000-1500 words (expanded for depth), engaging, and professional for a business audience. Expand sections with detailed analysis, historical context, multiple stakeholder perspectives, data visualizations ideas, and forward-looking scenarios.

Before writing, conduct keyword research: Identify 5-10 primary keywords, 10-15 long-tail phrases, and related LSI terms. List them with estimated search volumes, competition levels, and natural incorporation suggestions.

Structure per SEO best practices and E-E-A-T:
- Title (H1): CREATE A NEW SEO-optimized title (50-60 characters) using keyword research data. DO NOT use the original headline. Make it compelling, keyword-rich (include 1-2 primary keywords), and optimized for search engines.
- Meta Description: 150-160 characters, including primaries and CTA (suggest at end).
- Headings: Use H2/H3/H4 for readability and depth (aim for 8-12 sub-sections).
- Introduction: Hook with key facts and broader implications, include 2-3 primaries, outline article (200-300 words).
- Body: Write in natural, conversational style with varied sentence structures. Mix short punchy sentences with longer explanatory ones. Use natural transitions like "Here's what this means...", "But wait, there's more...", "Here's the thing...". Include analogies and real-world examples. Avoid robotic corporate language. Interweave keywords naturally (not forced). Add personal insights and human perspective. Target Flesch score 60+ but prioritize natural flow. Aim for 700-1000 engaging words.
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

# AUTOMATIC FACTS TASK GENERATION (No more hardcoding!)
fact_task_description = headline_analyzer.generate_automatic_task_description(HEADLINE, "facts")

fact_task = Task(
    description=fact_task_description,
    agent=fact_researcher,
    expected_output="A fact-rich report based on current web search results about the headline topic, including recent data, expert analysis, and up-to-date statistics with proper source citations.",
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
# Role: Generate the full article using research. Enhanced for length and structure.
article_writer = Agent(
    role="Engaging Reader-First Content Creator",
    goal="Write a captivating 1200-1800 word article that hooks readers immediately and keeps them scrolling. CRITICAL: Create an SEO-optimized title (50-60 characters) using keyword research data, NOT the original headline. Write with urgency, emotion, and personal connection - like explaining crucial news to a friend who needs to understand it RIGHT NOW. Every paragraph must earn the reader's next scroll.",
    backstory="You are a master storyteller and engagement expert who understands modern web readers. You know people skim first, so you write scannable content with shocking hooks, short punchy paragraphs, and actionable insights. You never sound corporate or robotic - you write like that friend everyone goes to for advice because you explain complex things in simple, relatable ways. Your articles make people think 'I need to share this!' and 'I should bookmark this site.'",
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

write_task = Task(
    description=f"""Write a captivating, human-style article about '{HEADLINE}' that hooks readers and keeps them engaged. 

CRITICAL: CREATE A NEW SEO-OPTIMIZED TITLE (50-60 characters) using keyword research data - DO NOT copy the original headline.

READER ENGAGEMENT REQUIREMENTS:
- START with a shocking statistic, surprising fact, or bold statement that makes readers think "I MUST read this!"
- Write SHORT paragraphs (3-4 sentences maximum, 50-80 words each)
- Break up text with bullet points, numbered lists, and subheadings (H3) for easy scanning
- Use conversational questions directly to the reader: "Have you noticed...?" "What does this mean for you?"
- Include personal anecdotes: "I was talking to a friend..." "Last week, I saw..."
- Add analogies from daily life: "It's like when you're at the grocery store..."
- End with 2-3 CONCRETE actions readers can take RIGHT NOW

WRITING STYLE REQUIREMENTS:
- Write as if chatting with a close friend who needs to understand this topic
- Use emotional language: "shocking," "surprising," "crucial," "game-changing"
- Vary sentence lengths dramatically (mix 5-word punches with longer explanations)
- Include rhetorical questions that make readers pause and think
- Use "you" and "your" constantly to make it personal
- Avoid ALL corporate jargon - write like a real person talks

VISUAL STRUCTURE:
- Engaging introduction (2-3 SHORT paragraphs with hook)
- 6-8 body sections with conversational H2 headings
- Within each section: H3 subheadings, bullet points, key facts in bold
- Thoughtful conclusion with specific next steps for readers
- Make it scannable for mobile readers who skim first

ENGAGEMENT HOOKS:
- Start each section with a question or surprising statement
- Include "Here's what this means for you..." moments
- Add urgency: "Right now..." "This week..." "Before you..."
- Personal stakes: "If you're like most people..." "Your wallet will feel..."

Focus on the headline topics but write like you're urgently explaining something important to someone you care about.""",
    agent=article_writer,
    expected_output="A highly engaging, scannable article with: 1) NEW SEO title (50-60 chars), 2) compelling meta description, 3) hook-driven introduction with shocking opener, 4) short paragraphs with bullet points and H3 subheadings, 5) conclusion with 2-3 concrete action steps. Content should feel urgent, personal, and written by someone who genuinely cares about helping the reader understand.",
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
    
    # Save to file
    with open("seo_article_output.json", "w", encoding="utf-8") as f:
        json.dump(json_content, f, indent=2, ensure_ascii=False)
    print("\nOutput saved to 'seo_article_output.json'")
    
    # Verify title optimization
    if 'article' in json_content:
        generated_title = json_content['article'].get('title', '')
        title_length = len(generated_title)
        
        body_text = json_content['article'].get('introduction', '') + ' '.join(json_content['article'].get('body', [])) + json_content['article'].get('conclusion', '')
        word_count = len(body_text.split())
        
        print(f"\nARTICLE METRICS:")
        print(f"   Generated title: \"{generated_title}\"")
        print(f"   Title length: {title_length} chars ({'Optimal' if title_length <= 60 else 'Too long'})")
        print(f"   Word count: {word_count} (target: 1000-1500)")
        
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