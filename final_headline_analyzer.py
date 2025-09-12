"""
Final Headline Analyzer - Adaptive keyword extraction with context awareness
Automatically analyzes headlines to extract relevant search terms and adapt strategy
Intègre la logique d'analyse contextuelle pour une adaptation totale au HEADLINE
"""

import re
from typing import List, Dict, Any
from datetime import datetime

class FinalHeadlineAnalyzer:
    """Adaptive headline analyzer - extracts relevant terms and adapts strategy to headline content"""
    
    def __init__(self):
        print("✅ Adaptive Final Headline Analyzer initialized (ZERO hardcoding)")
        
        # Import des nouvelles capacités adaptatives
        try:
            from adaptive_keyword_context import AdaptiveKeywordContextAnalyzer
            self.context_analyzer = AdaptiveKeywordContextAnalyzer()
            self.context_analysis_available = True
            print("✅ Advanced context analysis available")
        except ImportError:
            self.context_analysis_available = False
            print("⚠️ Advanced context analysis not available")
        
        # Termes à éviter (détection automatique d'off-topic)
        self.off_topic_terms = [
            "crypto", "bitcoin", "blockchain", "nft", "cryptocurrency",
            "gaming", "video game", "streaming", "youtube", "twitch",
            "celebrity", "gossip", "entertainment", "movie", "music",
            "sports", "football", "basketball", "soccer", "tennis",
            "fashion", "beauty", "makeup", "clothing", "shopping"
        ]
    
    def extract_automatic_concepts(self, headline: str) -> Dict[str, List[str]]:
        """Automatically extract concepts from headline without predefined patterns"""
        
        headline_lower = headline.lower()
        extracted_concepts = {
            'key_terms': [],
            'entities': [],
            'numbers_data': [],
            'time_references': [],
            'action_verbs': [],
            'important_nouns': []
        }
        
        # 1. Extract important nouns (capitalized words, excluding common words)
        common_words = {'the', 'a', 'an', 'in', 'on', 'at', 'by', 'for', 'with', 'as', 'and', 'or', 'but', 'this', 'that', 'these', 'those', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must'}
        
        # Find all capitalized words
        capitalized_words = re.findall(r'\b[A-Z][a-z]+\b', headline)
        important_nouns = [word for word in capitalized_words if word.lower() not in common_words]
        extracted_concepts['important_nouns'] = important_nouns
        
        # 2. Extract entities (proper names, organizations, people)
        # Look for patterns like "Secretary X", "Company Y", "Dr. Z"
        entity_patterns = [
            r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b',  # Two capitalized words
            r'\b(?:Mr|Ms|Mrs|Dr|Prof|Secretary|President|CEO|CFO|Chairman)\s+[A-Z][a-z]+\b',  # Titles
            r'\b[A-Z][a-z]+\s+(?:Inc|Corp|LLC|Ltd|Co|Company|Department|Ministry|Bureau)\b',  # Organizations
        ]
        
        entities = []
        for pattern in entity_patterns:
            matches = re.findall(pattern, headline)
            entities.extend(matches)
        extracted_concepts['entities'] = list(set(entities))
        
        # 3. Extract numbers and percentages
        numbers = re.findall(r'\d+\.?\d*%?', headline)
        extracted_concepts['numbers_data'] = numbers
        
        # 4. Extract time references
        time_patterns = [
            r'\b(?:this|last|next)\s+(?:week|month|year|quarter|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b',
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b',
            r'\b(?:today|yesterday|tomorrow|now|recently|lately|soon|recent)\b',
            r'\b(?:20\d{2})\b'  # Years
        ]
        
        time_refs = []
        for pattern in time_patterns:
            matches = re.findall(pattern, headline, re.IGNORECASE)
            time_refs.extend(matches)
        extracted_concepts['time_references'] = time_refs
        
        # 5. Extract action verbs
        action_verbs = re.findall(r'\b(?:met|meeting|announced|declared|reported|said|told|confirmed|denied|agreed|disagreed|decided|voted|elected|appointed|hired|fired|resigned|retired|joined|left|started|ended|began|finished|launched|introduced|proposed|rejected|approved|passed|failed|increased|decreased|rose|fell|gained|lost|won|lost|beat|defeated|signed|signed|agreed|disagreed|negotiated|discussed|talked|spoke|addressed|focused|concentrated|emphasized|highlighted|stressed|mentioned|noted|observed|found|discovered|revealed|exposed|uncovered|investigated|studied|analyzed|examined|reviewed|evaluated|assessed|measured|calculated|estimated|predicted|forecast|projected|expected|anticipated|hoped|feared|worried|concerned|interested|excited|pleased|disappointed|satisfied|unsatisfied|happy|sad|angry|frustrated|confused|surprised|shocked|amazed|impressed|disappointed|pleased|satisfied|unsatisfied|happy|sad|angry|frustrated|confused|surprised|shocked|amazed|impressed)\b', headline, re.IGNORECASE)
        extracted_concepts['action_verbs'] = action_verbs
        
        # 6. Extract key terms (important words that aren't common)
        words = re.findall(r'\b[a-zA-Z]+\b', headline_lower)
        key_terms = [word for word in words if len(word) > 3 and word not in common_words and word not in self.off_topic_terms]
        extracted_concepts['key_terms'] = list(set(key_terms))
        
        return extracted_concepts
    
    def generate_automatic_search_terms(self, headline: str) -> List[str]:
        """Adaptively generate search terms based on headline context and content"""
        print(f"🎯 Generating adaptive search terms for: '{headline[:50]}...'")
        
        # 1. Use advanced context analysis if available
        if self.context_analysis_available:
            try:
                # Get comprehensive adaptive strategy
                strategy = self.context_analyzer.generate_adaptive_search_strategy(headline)
                
                # Combine all adaptive terms
                adaptive_terms = []
                adaptive_terms.extend(strategy['adaptive_search_terms'])
                adaptive_terms.extend(strategy['autocomplete_suggestions'])
                
                # Remove duplicates and filter
                unique_adaptive_terms = list(dict.fromkeys(adaptive_terms))
                filtered_adaptive_terms = [term for term in unique_adaptive_terms if len(term) > 2 and term not in self.off_topic_terms]
                
                print(f"✅ Generated {len(filtered_adaptive_terms)} adaptive search terms")
                return filtered_adaptive_terms[:20]  # Return top 20 adaptive terms
                
            except Exception as e:
                print(f"⚠️ Adaptive analysis error: {e}, falling back to basic extraction")
        
        # 2. Fallback to enhanced basic extraction
        concepts = self.extract_automatic_concepts(headline)
        search_terms = []
        
        # Enhanced extraction with better logic
        search_terms.extend(concepts['important_nouns'])
        search_terms.extend(concepts['entities'])
        
        # Create smarter combinations
        important_nouns = concepts['important_nouns']
        if len(important_nouns) >= 2:
            for i in range(len(important_nouns)):
                for j in range(i+1, min(len(important_nouns), i+3)):  # Limit combinations
                    search_terms.append(f"{important_nouns[i]} {important_nouns[j]}")
        
        # Add contextual terms
        search_terms.extend(concepts['key_terms'][:5])
        
        # Time and number combinations (more selective)
        for time_ref in concepts['time_references'][:2]:
            for noun in important_nouns[:2]:
                search_terms.append(f"{noun} {time_ref}")
        
        for number in concepts['numbers_data'][:2]:
            for noun in important_nouns[:2]:
                search_terms.append(f"{noun} {number}")
        
        # Action verb combinations
        for verb in concepts['action_verbs'][:2]:
            for noun in important_nouns[:2]:
                search_terms.append(f"{verb} {noun}")
        
        # Remove duplicates and filter
        unique_terms = list(dict.fromkeys(search_terms))
        filtered_terms = [term for term in unique_terms if len(term) > 2 and term not in self.off_topic_terms]
        
        print(f"✅ Generated {len(filtered_terms)} basic search terms (fallback mode)")
        return filtered_terms[:15]  # Return top 15 terms
    
    def generate_adaptive_keyword_strategy(self, headline: str) -> Dict[str, Any]:
        """Génère une stratégie complète de mots-clés adaptée au headline"""
        print(f"📋 Generating comprehensive keyword strategy for: '{headline[:30]}...'")
        
        strategy = {
            'headline': headline,
            'analysis_timestamp': datetime.now().isoformat(),
            'search_terms': [],
            'context_analysis': {},
            'keyword_categories': {},
            'recommended_approach': '',
            'estimated_difficulty': 'Unknown'
        }
        
        # Generate search terms
        strategy['search_terms'] = self.generate_automatic_search_terms(headline)
        
        # Add context analysis if available
        if self.context_analysis_available:
            try:
                context = self.context_analyzer.detect_headline_domain(headline)
                strategy['context_analysis'] = context
                
                # Adapt recommended approach based on context
                domain = context.get('primary_domain', 'general_business')
                headline_type = context.get('headline_type', 'general_business_news')
                
                strategy['recommended_approach'] = self._get_adaptive_approach(domain, headline_type)
                
                print(f"✅ Context-aware strategy generated for {domain} domain")
                
            except Exception as e:
                print(f"⚠️ Context analysis error: {e}")
        
        return strategy
    
    def _get_adaptive_approach(self, domain: str, headline_type: str) -> str:
        """Recommande une approche adaptée au contexte détecté"""
        
        approaches = {
            'economic_data': "Focus on analytical keywords, comparison terms, and data-driven long-tail phrases. Target users seeking economic analysis and forecasts.",
            'financial_markets': "Emphasize investment-related keywords, market sentiment terms, and financial performance phrases. Target investors and financial professionals.",
            'business_performance': "Prioritize business metrics keywords, competitive analysis terms, and performance comparison phrases. Target business decision-makers.",
            'consumer_research': "Focus on consumer behavior keywords, sentiment analysis terms, and market research phrases. Target marketers and business analysts."
        }
        
        type_modifiers = {
            'data_release_with_comparison': " Include comparison keywords and benchmark-related terms.",
            'periodic_data_release': " Emphasize time-based keywords and trend analysis terms.",
            'action_announcement': " Focus on news-related keywords and immediate impact terms.",
            'sentiment_report': " Prioritize sentiment analysis keywords and perception-related terms."
        }
        
        base_approach = approaches.get(domain, "Use a balanced mix of informational and commercial keywords targeting business professionals.")
        type_modifier = type_modifiers.get(headline_type, "")
        
        return base_approach + type_modifier
    
    def generate_automatic_task_description(self, headline: str, task_type: str) -> str:
        """Generate task descriptions with automatically extracted terms"""
        
        search_terms = self.generate_automatic_search_terms(headline)
        search_terms_str = "', '".join(search_terms)
        
        if task_type == "keyword":
            return f"""ULTRA-FOCUSED KEYWORD RESEARCH: Use the search tool to find current trending topics related to: '{headline}'.

AUTOMATIC ANALYSIS: This headline has been automatically analyzed and contains these key concepts: {', '.join(search_terms[:5])}.
Search ONLY for these automatically extracted terms: '{search_terms_str}'.
These terms are STRICTLY from the headline content - ZERO unrelated topics added.

Your goal: Find trending keywords, search volumes, and competition levels for THIS SPECIFIC headline topic ONLY.
Analyze search results to identify 5-10 primary keywords, 10-15 long-tail phrases, and LSI terms.
Stay laser-focused on the headline subject matter. Include estimated search volumes, competition levels, and natural incorporation suggestions.
DO NOT include keywords unrelated to the headline topic."""

        elif task_type == "facts":
            return f"""IN-DEPTH FACT RESEARCH: Use the search tool to gather comprehensive facts about: '{headline}'.

AUTOMATIC ANALYSIS: This headline has been automatically analyzed and contains these key concepts: {', '.join(search_terms[:5])}.
Search ONLY for these automatically extracted terms: '{search_terms_str}'.
These terms are STRICTLY from the headline content - ZERO unrelated topics added.

Your goal: Collect extensive, current facts about the headline topic using the search tool.
Gather recent news, expert analysis, statistics, market data, and economic impacts.
Focus on the most recent and relevant information available.
Provide detailed context, background information, and multiple perspectives.
Include proper source citations and publication dates.
DO NOT include information unrelated to the headline topic."""

        else:
            return f"""AUTOMATIC TASK: {task_type.upper()} for headline: '{headline}'

AUTOMATIC ANALYSIS: This headline has been automatically analyzed and contains these key concepts: {', '.join(search_terms[:5])}.
Search ONLY for these automatically extracted terms: '{search_terms_str}'.
These terms are STRICTLY from the headline content - ZERO unrelated topics added.

Focus on the headline topic and use the automatically extracted search terms for research."""

    def analyze_headline(self, headline: str) -> dict:
        """
        Analyze a headline for off-topic terms
        
        Args:
            headline (str): The headline to analyze
            
        Returns:
            dict: Analysis result
        """
        headline_lower = headline.lower()
        
        # Detect off-topic terms
        detected_terms = []
        for term in self.off_topic_terms:
            if term in headline_lower:
                detected_terms.append(term)
        
        # Calculate relevance score
        relevance_score = 100 - (len(detected_terms) * 20)
        relevance_score = max(0, relevance_score)
        
        return {
            "headline": headline,
            "relevance_score": relevance_score,
            "off_topic_terms": detected_terms,
            "is_relevant": len(detected_terms) == 0,
            "analysis": f"Relevance score: {relevance_score}%"
        }
    
    def is_headline_relevant(self, headline: str) -> bool:
        """
        Check if a headline is relevant (no off-topic terms)
        
        Args:
            headline (str): The headline to check
            
        Returns:
            bool: True if relevant, False otherwise
        """
        analysis = self.analyze_headline(headline)
        return analysis["is_relevant"]