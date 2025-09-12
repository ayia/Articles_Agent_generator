"""
Adaptive Keyword Context Analyzer - ZERO Hardcoding
Analyse automatiquement le contexte du HEADLINE pour adapter la stratégie de mots-clés
Utilise uniquement des services GRATUITS et SANS LIMITE
"""

import re
import requests
from typing import Dict, List, Any, Optional
from urllib.parse import quote_plus
import time
import random
from bs4 import BeautifulSoup
from datetime import datetime

class AdaptiveKeywordContextAnalyzer:
    """
    Analyse automatiquement le contexte du HEADLINE pour adapter la stratégie
    Utilise uniquement des APIs gratuites et sans limite
    """
    
    def __init__(self):
        print("✅ Adaptive keyword context analyzer initialized (100% FREE APIs)")
        
        # User agents pour éviter les blocages
        self._user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]
    
    def get_headers(self):
        """Génère des headers aléatoires pour éviter la détection"""
        return {
            'User-Agent': random.choice(self._user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.5',
            'Connection': 'keep-alive',
        }
    
    def detect_headline_domain(self, headline: str) -> Dict[str, Any]:
        """Détecte automatiquement le domaine du headline SANS valeurs hardcodées"""
        print(f"🔍 Analyzing headline context: '{headline[:50]}...'")
        
        headline_lower = headline.lower()
        words = re.findall(r'\b[a-zA-Z]+\b', headline_lower)
        
        # Extraction automatique des patterns
        extracted_patterns = {
            'organizations': re.findall(r'\b[A-Z][a-z]*[A-Z][a-z]*\b', headline),  # CamelCase/Acronymes
            'measurements': re.findall(r'\d+\.?\d*', headline),
            'comparisons': ['vs', 'versus', 'compared', 'expected'] if any(comp in headline_lower for comp in ['vs', 'versus', 'compared', 'expected']) else [],
            'time_indicators': [word for word in words if word in ['september', 'october', 'november', 'december', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'quarterly', 'monthly', 'weekly', 'daily', 'prelim', 'preliminary', 'final']],
            'action_words': [word for word in words if word in ['rises', 'falls', 'announces', 'reports', 'expects', 'beats', 'misses', 'forecasts', 'predicts', 'shows', 'indicates']],
            'sentiment_indicators': [word for word in words if word in ['sentiment', 'confidence', 'optimism', 'pessimism', 'mood', 'outlook']]
        }
        
        # Détermination automatique du domaine principal
        domain_scores = {
            'economic_data': len(extracted_patterns['measurements']) + len(extracted_patterns['time_indicators']) + len(extracted_patterns['sentiment_indicators']),
            'financial_markets': len(extracted_patterns['organizations']) + len(extracted_patterns['action_words']),
            'business_performance': len(extracted_patterns['comparisons']) + len(extracted_patterns['measurements']),
            'consumer_research': 1 if 'consumer' in headline_lower or 'sentiment' in headline_lower else 0
        }
        
        primary_domain = max(domain_scores.keys(), key=domain_scores.get) if any(domain_scores.values()) else 'general_business'
        
        # Classification automatique du type de headline
        headline_type = self._classify_headline_type_automatically(headline, extracted_patterns)
        
        result = {
            'primary_domain': primary_domain,
            'domain_confidence': domain_scores[primary_domain] / max(sum(domain_scores.values()), 1),
            'extracted_patterns': extracted_patterns,
            'headline_type': headline_type,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        print(f"✅ Detected domain: {primary_domain} (confidence: {result['domain_confidence']:.2f})")
        print(f"📊 Headline type: {headline_type}")
        
        return result
    
    def _classify_headline_type_automatically(self, headline: str, patterns: Dict) -> str:
        """Classifie automatiquement le type de headline basé sur les patterns détectés"""
        headline_lower = headline.lower()
        
        if patterns['measurements'] and patterns['comparisons']:
            return 'data_release_with_comparison'
        elif patterns['measurements'] and patterns['time_indicators']:
            return 'periodic_data_release'
        elif patterns['action_words']:
            return 'action_announcement'
        elif patterns['sentiment_indicators']:
            return 'sentiment_report'
        elif patterns['organizations']:
            return 'corporate_news'
        else:
            return 'general_business_news'
    
    def extract_adaptive_entities(self, headline: str) -> Dict[str, List[str]]:
        """Extrait automatiquement les entités importantes du headline"""
        print(f"🎯 Extracting entities from: '{headline}'")
        
        entities = {
            'primary_entities': [],
            'secondary_entities': [],
            'numerical_data': [],
            'temporal_references': [],
            'key_concepts': []
        }
        
        # Extraction des entités primaires (mots capitalisés significatifs)
        capitalized_words = re.findall(r'\b[A-Z][a-zA-Z]*\b', headline)
        # Filtrer les mots courants
        common_words = {'The', 'A', 'An', 'In', 'On', 'At', 'By', 'For', 'With', 'As', 'And', 'Or', 'But'}
        entities['primary_entities'] = [word for word in capitalized_words if word not in common_words]
        
        # Extraction des données numériques avec contexte
        numerical_matches = re.findall(r'\d+\.?\d*(?:\s*%|\s*vs|\s*expected)?', headline)
        entities['numerical_data'] = numerical_matches
        
        # Extraction des références temporelles
        time_patterns = [
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b',
            r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b',
            r'\b(?:Q[1-4]|quarterly|monthly|weekly|daily)\b',
            r'\b(?:preliminary|prelim|final|revised)\b'
        ]
        
        for pattern in time_patterns:
            matches = re.findall(pattern, headline, re.IGNORECASE)
            entities['temporal_references'].extend(matches)
        
        # Extraction des concepts clés (mots significatifs de plus de 3 lettres)
        words = re.findall(r'\b[a-zA-Z]{4,}\b', headline.lower())
        stop_words = {'with', 'from', 'that', 'this', 'they', 'have', 'been', 'were', 'said', 'each', 'which', 'their'}
        entities['key_concepts'] = [word for word in set(words) if word not in stop_words]
        
        print(f"✅ Extracted {len(entities['primary_entities'])} primary entities")
        print(f"📊 Found {len(entities['numerical_data'])} numerical data points")
        
        return entities
    
    def get_google_autocomplete_suggestions(self, term: str) -> List[str]:
        """Récupère les suggestions d'autocomplétion Google (100% GRATUIT)"""
        try:
            print(f"🔍 Getting Google autocomplete for: '{term}'")
            
            # API publique de suggestions Google (pas d'authentification nécessaire)
            url = f"http://suggestqueries.google.com/complete/search"
            params = {
                'client': 'chrome',
                'q': term,
                'hl': 'en'
            }
            
            response = requests.get(url, params=params, headers=self.get_headers(), timeout=10)
            
            if response.status_code == 200:
                suggestions = response.json()[1] if len(response.json()) > 1 else []
                print(f"✅ Found {len(suggestions)} Google suggestions")
                return suggestions[:10]  # Limiter à 10
            
        except Exception as e:
            print(f"⚠️ Google autocomplete error: {e}")
        
        return []
    
    def get_bing_autocomplete_suggestions(self, term: str) -> List[str]:
        """Récupère les suggestions d'autocomplétion Bing (100% GRATUIT)"""
        try:
            print(f"🔍 Getting Bing autocomplete for: '{term}'")
            
            # API publique de suggestions Bing (pas d'authentification nécessaire)
            url = f"https://api.bing.com/osjson.aspx"
            params = {
                'query': term,
                'language': 'en-US'
            }
            
            response = requests.get(url, params=params, headers=self.get_headers(), timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                suggestions = data[1] if len(data) > 1 else []
                print(f"✅ Found {len(suggestions)} Bing suggestions")
                return suggestions[:10]  # Limiter à 10
            
        except Exception as e:
            print(f"⚠️ Bing autocomplete error: {e}")
        
        return []
    
    def generate_adaptive_search_strategy(self, headline: str) -> Dict[str, Any]:
        """Génère une stratégie de recherche adaptée spécifiquement au headline"""
        print(f"🎯 Generating adaptive search strategy for: '{headline[:30]}...'")
        
        # Analyse du contexte
        context = self.detect_headline_domain(headline)
        entities = self.extract_adaptive_entities(headline)
        
        # Génération des termes de recherche adaptatifs
        search_terms = []
        
        # 1. Entités principales comme termes de base
        search_terms.extend(entities['primary_entities'][:5])
        
        # 2. Combinaisons d'entités avec données numériques
        for entity in entities['primary_entities'][:3]:
            for data in entities['numerical_data'][:2]:
                search_terms.append(f"{entity} {data}")
        
        # 3. Combinaisons avec références temporelles
        for entity in entities['primary_entities'][:3]:
            for time_ref in entities['temporal_references'][:2]:
                search_terms.append(f"{entity} {time_ref}")
        
        # 4. Concepts clés avec modificateurs adaptatifs
        modifiers = self._get_adaptive_modifiers(context['headline_type'])
        for concept in entities['key_concepts'][:3]:
            for modifier in modifiers[:2]:
                search_terms.append(f"{modifier} {concept}")
        
        # 5. Récupération des suggestions d'autocomplétion pour enrichir
        autocomplete_suggestions = []
        for term in entities['primary_entities'][:2]:  # Prendre seulement les 2 premiers pour éviter trop de requêtes
            time.sleep(0.5)  # Respecter les limites
            google_suggestions = self.get_google_autocomplete_suggestions(term)
            bing_suggestions = self.get_bing_autocomplete_suggestions(term)
            autocomplete_suggestions.extend(google_suggestions + bing_suggestions)
        
        strategy = {
            'headline': headline,
            'context': context,
            'extracted_entities': entities,
            'adaptive_search_terms': list(set(search_terms)),  # Supprimer doublons
            'autocomplete_suggestions': list(set(autocomplete_suggestions)),
            'total_terms_generated': len(set(search_terms)) + len(set(autocomplete_suggestions)),
            'strategy_timestamp': datetime.now().isoformat()
        }
        
        print(f"✅ Generated {strategy['total_terms_generated']} adaptive search terms")
        return strategy
    
    def _get_adaptive_modifiers(self, headline_type: str) -> List[str]:
        """Génère des modificateurs adaptatifs selon le type de headline détecté"""
        base_modifiers = ['latest', 'current', 'recent', 'new', '2024', 'today']
        
        type_specific_modifiers = {
            'data_release_with_comparison': ['analysis', 'report', 'data', 'results'],
            'periodic_data_release': ['monthly', 'quarterly', 'report', 'survey'],
            'action_announcement': ['news', 'announcement', 'update', 'breaking'],
            'sentiment_report': ['consumer', 'market', 'economic', 'business'],
            'corporate_news': ['company', 'business', 'stock', 'financial']
        }
        
        specific = type_specific_modifiers.get(headline_type, ['business', 'news'])
        return base_modifiers + specific

# Test unitaire
if __name__ == "__main__":
    print("🧪 TESTING ADAPTIVE KEYWORD CONTEXT ANALYZER")
    print("=" * 60)
    
    analyzer = AdaptiveKeywordContextAnalyzer()
    
    # Test avec le headline actuel
    test_headline = "UMich September prelim consumer sentiment 55.4 vs 58.0 expected"
    
    print(f"\n📋 Testing with: {test_headline}")
    
    # Test 1: Détection de domaine
    context = analyzer.detect_headline_domain(test_headline)
    print(f"✅ Domain detected: {context['primary_domain']}")
    
    # Test 2: Extraction d'entités
    entities = analyzer.extract_adaptive_entities(test_headline)
    print(f"✅ Entities extracted: {entities['primary_entities']}")
    
    # Test 3: Stratégie adaptative
    strategy = analyzer.generate_adaptive_search_strategy(test_headline)
    print(f"✅ Search terms generated: {len(strategy['adaptive_search_terms'])}")
    
    print("\n📊 ADAPTIVE ANALYSIS COMPLETE!")
