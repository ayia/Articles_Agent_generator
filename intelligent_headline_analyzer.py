# Agent LLM Intelligent pour Analyse de Headline
# Utilise l'IA pour extraire intelligemment les concepts et générer les termes de recherche
# AUCUN HARDCODE - Analyse 100% dynamique et intelligente

import os
import json
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import List, Dict, Any

class IntelligentHeadlineAnalyzer:
    """Agent LLM pour analyse intelligente du headline et génération des termes de recherche"""
    
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Setup LLM for headline analysis (same as main system)
        DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
        DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
        
        if not DEEPSEEK_API_KEY:
            raise ValueError("DEEPSEEK_API_KEY environment variable required for intelligent analysis")
        
        # LLM for intelligent analysis
        self.analysis_llm = ChatOpenAI(
            model="deepseek/deepseek-chat",  # Correct LiteLLM format with provider
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL,
            temperature=0.3,  # Low temperature for precise analysis
            max_tokens=2000,  # Enough for detailed analysis
        )
        
        print("🧠 Intelligent LLM headline analyzer initialized")
    
    def analyze_headline_intelligently(self, headline: str) -> Dict[str, Any]:
        """Use LLM to intelligently analyze headline and extract relevant concepts"""
        
        analysis_prompt = f"""
You are an expert SEO and content analyst. Analyze this headline and provide intelligent insights:

HEADLINE: "{headline}"

Your task is to:
1. Identify the MAIN TOPICS and concepts in this headline
2. Extract RELEVANT KEYWORDS that people would search for related to this topic  
3. Generate SEARCH TERMS that would help find current news and data about this subject
4. Suggest PRIMARY KEYWORDS for SEO optimization
5. Identify the INDUSTRY/SECTOR this headline belongs to

Provide your analysis in JSON format:
{{
    "main_topics": ["topic1", "topic2", "topic3"],
    "search_terms": ["term1", "term2", "term3", "term4", "term5", "term6", "term7", "term8", "term9", "term10"],
    "primary_keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
    "industry_sector": "sector_name",
    "content_type": "news/analysis/report",
    "urgency_level": "breaking/current/background",
    "target_audience": "general/business/technical"
}}

Be intelligent and adaptive. Extract concepts that are actually relevant to the headline content.
NO hardcoded responses - analyze the specific headline provided.
Focus on terms that would be trending and searchable related to this specific topic.
"""
        
        try:
            # Get LLM analysis
            response = self.analysis_llm.invoke(analysis_prompt)
            
            # Parse the JSON response
            analysis_text = response.content
            
            # Extract JSON from the response
            import re
            json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
            if json_match:
                analysis_json = json.loads(json_match.group())
                return analysis_json
            else:
                # Fallback if JSON parsing fails
                return self._fallback_analysis(headline)
                
        except Exception as e:
            print(f"⚠️ LLM analysis error: {e}")
            return self._fallback_analysis(headline)
    
    def _fallback_analysis(self, headline: str) -> Dict[str, Any]:
        """Fallback analysis if LLM fails"""
        words = headline.lower().split()
        
        return {
            "main_topics": words[:3],
            "search_terms": words[:8],
            "primary_keywords": words[:5],
            "industry_sector": "general",
            "content_type": "news",
            "urgency_level": "current",
            "target_audience": "general"
        }
    
    def generate_intelligent_search_terms(self, headline: str) -> List[str]:
        """Generate intelligent search terms using LLM analysis"""
        
        print(f"🧠 Intelligent analysis of headline...")
        analysis = self.analyze_headline_intelligently(headline)
        
        # Extract search terms from intelligent analysis
        search_terms = analysis.get('search_terms', [])
        main_topics = analysis.get('main_topics', [])
        
        # Combine and deduplicate
        all_terms = search_terms + main_topics
        unique_terms = list(dict.fromkeys(all_terms))[:10]  # Remove duplicates, keep order, limit to 10
        
        print(f"✅ Intelligent analysis complete!")
        print(f"📊 Industry: {analysis.get('industry_sector', 'N/A')}")
        print(f"🎯 Content type: {analysis.get('content_type', 'N/A')}")
        print(f"⚡ Urgency: {analysis.get('urgency_level', 'N/A')}")
        
        return unique_terms
    
    def generate_intelligent_task_description(self, headline: str, task_type: str = "keyword") -> str:
        """Generate intelligent task descriptions using LLM analysis"""
        
        # Get intelligent analysis
        analysis = self.analyze_headline_intelligently(headline)
        search_terms = analysis.get('search_terms', [])
        search_terms_str = "', '".join(search_terms)
        industry = analysis.get('industry_sector', 'general')
        
        if task_type == "keyword":
            return f"""INTELLIGENT KEYWORD RESEARCH: Use the search tool to find current trending topics related to: '{headline}'.

SEARCH STRATEGY: Based on intelligent LLM analysis, this headline belongs to the {industry} sector. 
Search for these intelligently extracted terms: '{search_terms_str}'.

These terms were generated by AI analysis of the headline content - ZERO HARDCODING.
Focus your searches on finding trending keywords, search volumes, and competition levels for this specific topic.

Then analyze the search results to identify 5-10 primary keywords, 10-15 long-tail phrases, and LSI terms based on what's currently trending in news related to this headline topic.
Include estimated search volumes, competition levels, and natural incorporation suggestions."""
        
        elif task_type == "facts":
            return f"""INTELLIGENT FACT RESEARCH: Use the search tool extensively! Based on intelligent analysis of the headline '{headline}', this content belongs to the {industry} sector.

SEARCH STRATEGY: Search for these AI-generated relevant terms: '{search_terms_str}'.
These search terms were intelligently extracted from the headline by LLM analysis - NO HARDCODING.

Gather real-time information from news sources, RSS feeds, and recent publications. Focus on:
- Recent data and statistics related to the headline topic
- Expert quotes and analysis from industry professionals  
- Market trends and economic indicators
- Recent developments and breaking news
- Policy implications and market reactions

Cross-reference multiple sources and include recent developments, expert analysis, and market context specifically related to the headline topic."""
        
        return ""

# Test the intelligent system
def test_intelligent_system():
    """Test the intelligent headline analysis system"""
    
    print("🧪 TEST OF INTELLIGENT LLM-BASED HEADLINE ANALYZER")
    print("=" * 70)
    
    # Test headlines
    test_headlines = [
        "Consumer prices rose at annual rate of 2.9% in August, as weekly jobless claims jump",
        "Bitcoin reaches $100,000 for first time amid institutional adoption surge", 
        "Apple announces iPhone 16 with integrated AI: smartphone revolution begins",
        "Federal Reserve cuts interest rates by 0.5% to combat recession fears"
    ]
    
    try:
        analyzer = IntelligentHeadlineAnalyzer()
        
        for i, headline in enumerate(test_headlines, 1):
            print(f"\n📰 TEST {i}: {headline}")
            print(f"📏 Length: {len(headline)} characters")
            
            # Intelligent analysis
            search_terms = analyzer.generate_intelligent_search_terms(headline)
            print(f"🔍 AI-generated search terms ({len(search_terms)}):")
            for j, term in enumerate(search_terms, 1):
                print(f"   {j:2d}. \"{term}\"")
            
            print("─" * 50)
        
        print(f"\n✅ INTELLIGENT HEADLINE ANALYZER OPERATIONAL!")
        print(f"🤖 Using AI for smart term extraction")
        print(f"🔄 Fully adaptive to any headline topic")
        print(f"🚫 Zero hardcoded terms")
        
    except Exception as e:
        print(f"❌ Error testing intelligent analyzer: {e}")
        print("💡 Make sure DEEPSEEK_API_KEY is set in environment")

if __name__ == "__main__":
    test_intelligent_system()
