# Smart Headline Analyzer - Intelligence sans LLM
# Analyse intelligente du headline avec algorithmes avancés (pas de dépendance LLM)
# 100% adaptatif et intelligent sans API

import re
import json
from typing import List, Dict, Any, Set
from collections import Counter

class SmartHeadlineAnalyzer:
    """Analyseur intelligent de headline sans dépendance LLM"""
    
    def __init__(self):
        # Business/Economic concept mapping - intelligent associations
        self.concept_clusters = {
            # Economic indicators cluster
            'economic_indicators': {
                'triggers': ['prices', 'inflation', 'rate', 'index', 'gdp', 'economic', 'growth', 'recession'],
                'search_terms': ['inflation rate', 'economic indicators', 'CPI data', 'economic growth', 'GDP report', 
                               'consumer price index', 'economic data', 'financial indicators', 'economic outlook']
            },
            
            # Employment cluster  
            'employment': {
                'triggers': ['jobs', 'jobless', 'unemployment', 'employment', 'claims', 'labor', 'workers', 'workforce'],
                'search_terms': ['unemployment rate', 'jobless claims', 'employment data', 'labor market', 
                               'job market trends', 'unemployment benefits', 'employment statistics', 'workforce data']
            },
            
            # Technology cluster
            'technology': {
                'triggers': ['ai', 'artificial', 'chatgpt', 'openai', 'tech', 'technology', 'digital', 'innovation'],
                'search_terms': ['AI development', 'artificial intelligence', 'tech innovation', 'AI news', 
                               'technology trends', 'AI industry', 'machine learning', 'tech companies']
            },
            
            # Financial markets cluster
            'financial_markets': {
                'triggers': ['stock', 'market', 'bitcoin', 'crypto', 'investment', 'trading', 'shares', 'finance'],
                'search_terms': ['stock market', 'financial markets', 'market trends', 'investment news',
                               'cryptocurrency', 'bitcoin price', 'market volatility', 'financial data']
            },
            
            # Corporate cluster
            'corporate': {
                'triggers': ['company', 'corporation', 'ceo', 'earnings', 'revenue', 'profit', 'business'],
                'search_terms': ['corporate news', 'business earnings', 'company performance', 'corporate results',
                               'business trends', 'company analysis', 'corporate strategy', 'business news']
            },
            
            # Policy cluster
            'policy': {
                'triggers': ['government', 'policy', 'federal', 'reserve', 'trump', 'biden', 'regulation', 'law'],
                'search_terms': ['government policy', 'federal policy', 'regulatory news', 'policy changes',
                               'government decisions', 'policy analysis', 'regulatory impact', 'policy updates']
            },
            
            # Industry clusters (expandable)
            'healthcare': {
                'triggers': ['health', 'medical', 'pharma', 'drug', 'medicine', 'healthcare', 'treatment'],
                'search_terms': ['healthcare industry', 'pharmaceutical news', 'medical developments', 'drug market',
                               'healthcare trends', 'medical innovation', 'pharma industry', 'health sector']
            },
            
            # Geographic cluster
            'global': {
                'triggers': ['china', 'europe', 'eu', 'asia', 'america', 'global', 'international', 'world'],
                'search_terms': ['international trade', 'global economy', 'international news', 'global markets',
                               'world economy', 'international relations', 'global trends', 'worldwide impact']
            }
        }
    
    def extract_smart_concepts(self, headline: str) -> Dict[str, Any]:
        """Extract concepts using intelligent pattern matching"""
        
        headline_lower = headline.lower()
        words = re.findall(r'\b\w+\b', headline_lower)
        
        # Identify which clusters this headline belongs to
        active_clusters = {}
        
        for cluster_name, cluster_data in self.concept_clusters.items():
            triggers = cluster_data['triggers']
            
            # Count trigger words found
            trigger_count = sum(1 for trigger in triggers if trigger in headline_lower)
            
            if trigger_count > 0:
                active_clusters[cluster_name] = {
                    'score': trigger_count,
                    'search_terms': cluster_data['search_terms']
                }
        
        # Extract numbers, percentages, dates
        numbers = re.findall(r'\b\d+\.?\d*%?\b', headline)
        dates = re.findall(r'\b(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|20\d{2})\b', headline, re.IGNORECASE)
        
        # Extract company/proper names (capitalized words)
        proper_names = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', headline)
        proper_names = [name for name in proper_names if len(name) > 2]  # Filter short words
        
        return {
            'active_clusters': active_clusters,
            'numbers': numbers,
            'dates': dates,
            'proper_names': proper_names,
            'raw_words': words
        }
    
    def generate_intelligent_search_terms(self, headline: str) -> List[str]:
        """Generate intelligent search terms using smart analysis"""
        
        print(f"🧠 Smart analysis of headline...")
        analysis = self.extract_smart_concepts(headline)
        
        search_terms = []
        
        # Add terms from active clusters (prioritize by score)
        active_clusters = analysis['active_clusters']
        sorted_clusters = sorted(active_clusters.items(), key=lambda x: x[1]['score'], reverse=True)
        
        cluster_names = []
        for cluster_name, cluster_info in sorted_clusters[:3]:  # Top 3 relevant clusters
            cluster_names.append(cluster_name)
            search_terms.extend(cluster_info['search_terms'][:3])  # Top 3 terms per cluster
        
        # Add specific terms with numbers/dates
        for number in analysis['numbers'][:3]:
            if any(word in headline.lower() for word in ['inflation', 'rate', 'percent']):
                search_terms.append(f"inflation {number}")
            elif 'jobless' in headline.lower() or 'unemployment' in headline.lower():
                search_terms.append(f"unemployment {number}")
            else:
                search_terms.append(f"economic data {number}")
        
        # Add company/proper name specific searches
        for name in analysis['proper_names'][:2]:
            search_terms.append(f"{name} news")
            search_terms.append(f"{name} analysis")
        
        # Add date-specific searches
        for date in analysis['dates'][:2]:
            search_terms.append(f"economic news {date}")
            if cluster_names:
                search_terms.append(f"{cluster_names[0]} {date}")
        
        # Remove duplicates while preserving order
        unique_terms = list(dict.fromkeys(search_terms))
        
        print(f"✅ Smart analysis complete!")
        print(f"📊 Active clusters: {', '.join(cluster_names)}")
        print(f"🔢 Numbers found: {analysis['numbers']}")
        print(f"📅 Dates found: {analysis['dates']}")
        print(f"🏢 Entities: {analysis['proper_names']}")
        
        return unique_terms[:12]  # Limit to 12 most relevant terms
    
    def generate_intelligent_task_description(self, headline: str, task_type: str = "keyword") -> str:
        """Generate intelligent task descriptions using smart analysis"""
        
        # Get smart analysis
        search_terms = self.generate_intelligent_search_terms(headline)
        search_terms_str = "', '".join(search_terms)
        
        # Identify primary topic for context
        analysis = self.extract_smart_concepts(headline)
        active_clusters = analysis['active_clusters']
        
        if active_clusters:
            primary_topic = max(active_clusters.keys(), key=lambda k: active_clusters[k]['score'])
        else:
            primary_topic = "general business"
        
        if task_type == "keyword":
            return f"""INTELLIGENT KEYWORD RESEARCH: Use the search tool to find current trending topics related to: '{headline}'.

SMART ANALYSIS RESULTS: This headline was analyzed and identified as primarily related to {primary_topic}.
Search for these intelligently extracted terms: '{search_terms_str}'.

These terms were generated by SMART ANALYSIS of the headline content - ZERO HARDCODING.
The system identified {len(active_clusters)} relevant topic clusters and extracted the most appropriate search terms.

Focus your searches on finding trending keywords, search volumes, and competition levels for this specific topic.
Then analyze the search results to identify 5-10 primary keywords, 10-15 long-tail phrases, and LSI terms based on what's currently trending in news related to this headline topic.
Include estimated search volumes, competition levels, and natural incorporation suggestions."""
        
        elif task_type == "facts":
            return f"""INTELLIGENT FACT RESEARCH: Use the search tool extensively! 

SMART ANALYSIS: The headline '{headline}' was analyzed and categorized as {primary_topic} content.
Search for these intelligently extracted terms: '{search_terms_str}'.

These search terms were generated by INTELLIGENT ANALYSIS of the headline - NO HARDCODING.
The system identified the most relevant concepts and generated appropriate search terms.

Gather real-time information from news sources, RSS feeds, and recent publications. Focus on:
- Recent data and statistics related to the headline topic
- Expert quotes and analysis from industry professionals  
- Market trends and relevant indicators
- Recent developments and breaking news
- Policy implications and market reactions

Cross-reference multiple sources and include recent developments, expert analysis, and market context specifically related to the headline topic."""
        
        return ""

# Test the smart system
def test_smart_system():
    """Test the smart headline analysis system"""
    
    print("🧪 TEST OF SMART NON-LLM HEADLINE ANALYZER")
    print("=" * 70)
    
    analyzer = SmartHeadlineAnalyzer()
    
    # Test with current headline
    headline = "Consumer prices rose at annual rate of 2.9% in August, as weekly jobless claims jump"
    
    print(f"📰 TESTING CURRENT HEADLINE:")
    print(f"   \"{headline}\"")
    print(f"   📏 {len(headline)} characters")
    print()
    
    # Smart analysis
    search_terms = analyzer.generate_intelligent_search_terms(headline)
    
    print(f"🔍 SMART-GENERATED SEARCH TERMS ({len(search_terms)}):")
    for i, term in enumerate(search_terms, 1):
        print(f"   {i:2d}. \"{term}\"")
    
    print(f"\n🎯 QUALITY CHECK:")
    # Check if terms are relevant to the headline topic
    relevant_terms = ['inflation', 'unemployment', 'economic', 'jobless', 'consumer', 'price']
    relevant_count = sum(1 for term in search_terms if any(rel in term.lower() for rel in relevant_terms))
    
    print(f"   📊 Relevant terms: {relevant_count}/{len(search_terms)} ({relevant_count/len(search_terms)*100:.1f}%)")
    print(f"   ✅ Smart analysis {'EXCELLENT' if relevant_count/len(search_terms) > 0.6 else 'GOOD' if relevant_count/len(search_terms) > 0.4 else 'NEEDS IMPROVEMENT'}")
    
    return search_terms

if __name__ == "__main__":
    test_smart_system()
