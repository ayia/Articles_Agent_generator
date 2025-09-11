# Analyseur PRÉCIS avec DeepSeek - Extraction UNIQUEMENT des concepts du headline
# Pas d'ajout de termes hors sujet - Le headline détermine TOUT

import os
import json
import re
from typing import List, Dict
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

class PreciseHeadlineAnalyzer:
    """Analyseur précis utilisant DeepSeek UNIQUEMENT pour les concepts du headline"""
    
    def __init__(self):
        load_dotenv()
        
        DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
        if not DEEPSEEK_API_KEY:
            raise ValueError("DEEPSEEK_API_KEY required for precise analysis")
        
        # DeepSeek LLM pour analyse précise
        self.llm = ChatOpenAI(
            model="deepseek-chat",  # Format direct DeepSeek
            api_key=DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com",  # URL simplifiée
            temperature=0.1,  # Très bas pour précision maximale
            max_tokens=1000,
        )
        
        print("🎯 Precise DeepSeek headline analyzer initialized")
    
    def extract_precise_terms(self, headline: str) -> List[str]:
        """Utiliser DeepSeek pour extraire UNIQUEMENT les concepts précis du headline"""
        
        prompt = f"""You are a precise content analyst. Analyze this headline and extract ONLY the directly relevant search terms.

HEADLINE: "{headline}"

RULES:
1. Extract ONLY concepts that are DIRECTLY mentioned or implied in the headline
2. DO NOT add unrelated topics  
3. Focus on the MAIN SUBJECT MATTER of the headline
4. Generate 8-12 specific search terms that would help find news about THIS EXACT TOPIC
5. DO NOT add general terms that are not related to the headline content

Return ONLY a JSON list of search terms:
["term1", "term2", "term3", ...]

Example:
If headline is about "inflation and jobless claims", return terms about inflation and employment ONLY.
If headline is about "Apple iPhone", return terms about Apple and smartphones ONLY.
DO NOT mix topics.

Focus on being PRECISE and RELEVANT to the headline content."""
        
        try:
            response = self.llm.invoke(prompt)
            content = response.content.strip()
            
            # Extract JSON array from response
            json_match = re.search(r'\[(.*?)\]', content, re.DOTALL)
            if json_match:
                json_str = '[' + json_match.group(1) + ']'
                search_terms = json.loads(json_str)
                
                # Validate and clean terms
                cleaned_terms = []
                for term in search_terms:
                    if isinstance(term, str) and len(term.strip()) > 2:
                        cleaned_terms.append(term.strip())
                
                return cleaned_terms[:10]  # Limit to 10 most relevant
            
            else:
                # Fallback: manual extraction if JSON parsing fails
                return self._manual_extraction_fallback(headline)
                
        except Exception as e:
            print(f"⚠️ DeepSeek error: {e}")
            return self._manual_extraction_fallback(headline)
    
    def _manual_extraction_fallback(self, headline: str) -> List[str]:
        """Fallback précis si DeepSeek échoue"""
        
        headline_lower = headline.lower()
        
        # Extraction manuelle PRÉCISE basée sur les mots du headline
        terms = []
        
        # Si inflation/prices mentionnés
        if any(word in headline_lower for word in ['price', 'inflation', 'consumer']):
            terms.extend(['inflation rate', 'consumer prices', 'CPI data', 'price index'])
        
        # Si emploi/chômage mentionnés  
        if any(word in headline_lower for word in ['job', 'unemployment', 'claims', 'labor']):
            terms.extend(['unemployment rate', 'jobless claims', 'employment data', 'labor market'])
        
        # Extraire les chiffres précis
        numbers = re.findall(r'\b\d+\.?\d*%?\b', headline)
        for num in numbers[:2]:
            if 'inflation' in headline_lower or 'price' in headline_lower:
                terms.append(f"inflation {num}")
            if 'job' in headline_lower or 'unemployment' in headline_lower:
                terms.append(f"unemployment {num}")
        
        # Extraire les dates
        dates = re.findall(r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\b', headline, re.IGNORECASE)
        for date in dates[:1]:
            terms.append(f"economic data {date}")
        
        return list(set(terms))[:8]  # Remove duplicates, limit to 8
    
    def generate_precise_task_description(self, headline: str, task_type: str) -> str:
        """Générer des descriptions de task PRÉCISES basées sur le headline"""
        
        search_terms = self.extract_precise_terms(headline)
        search_terms_str = "', '".join(search_terms)
        
        if task_type == "keyword":
            return f"""PRECISE KEYWORD RESEARCH: Use the search tool to find current trending topics related to: '{headline}'.

FOCUS: This headline analysis extracted ONLY these directly relevant terms: '{search_terms_str}'.
These terms are STRICTLY related to the headline content - NO UNRELATED TOPICS ADDED.

Search for trending keywords, search volumes, and competition levels for this SPECIFIC headline topic.
Then analyze the search results to identify 5-10 primary keywords, 10-15 long-tail phrases, and LSI terms.
Stay focused on the headline subject matter. Include estimated search volumes, competition levels, and natural incorporation suggestions."""
        
        elif task_type == "facts":
            return f"""PRECISE FACT RESEARCH: Use the search tool extensively for the headline '{headline}'.

SEARCH FOCUS: Use these precisely extracted terms: '{search_terms_str}'.
These terms are DIRECTLY related to the headline - NO OFF-TOPIC SEARCHES.

Gather real-time information specifically about:
- Recent data related to the headline topic
- Expert analysis on the specific subject matter
- Current developments on the headline topic
- Market/economic impacts of the headline subject

Stay focused on the headline content. Cross-reference sources and provide recent, relevant information."""
        
        return ""

def test_precise_system():
    """Test du système précis"""
    
    print("🎯 TEST OF PRECISE DEEPSEEK HEADLINE ANALYZER")
    print("=" * 60)
    
    try:
        analyzer = PreciseHeadlineAnalyzer()
        
        headline = "Consumer prices rose at annual rate of 2.9% in August, as weekly jobless claims jump"
        
        print(f"📰 HEADLINE:")
        print(f"   \"{headline}\"")
        print()
        
        # Analyse précise
        search_terms = analyzer.extract_precise_terms(headline)
        
        print(f"🎯 PRECISE SEARCH TERMS EXTRACTED ({len(search_terms)}):")
        for i, term in enumerate(search_terms, 1):
            print(f"   {i:2d}. \"{term}\"")
        
        # Vérification de pertinence
        headline_words = set(re.findall(r'\b\w+\b', headline.lower()))
        relevant_terms = []
        
        for term in search_terms:
            term_words = set(re.findall(r'\b\w+\b', term.lower()))
            if term_words.intersection(headline_words) or any(word in headline.lower() for word in ['inflation', 'unemployment', 'economic'] if word in term.lower()):
                relevant_terms.append(term)
        
        relevance_score = len(relevant_terms) / len(search_terms) * 100 if search_terms else 0
        
        print(f"\n📊 RELEVANCE CHECK:")
        print(f"   🎯 Relevant terms: {len(relevant_terms)}/{len(search_terms)} ({relevance_score:.1f}%)")
        print(f"   ✅ Quality: {'EXCELLENT' if relevance_score >= 80 else 'GOOD' if relevance_score >= 60 else 'NEEDS IMPROVEMENT'}")
        
        # Vérifier qu'il n'y a pas de termes hors sujet
        off_topic_indicators = ['ai development', 'artificial intelligence', 'tech innovation', 'trump tariffs']
        off_topic_found = [term for term in search_terms if any(indicator in term.lower() for indicator in off_topic_indicators)]
        
        if not off_topic_found:
            print(f"   ✅ NO OFF-TOPIC TERMS - Perfect focus!")
        else:
            print(f"   ⚠️ Off-topic terms found: {off_topic_found}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_precise_system()
