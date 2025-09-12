"""
Advanced Keyword Research Tools - 100% FREE APIs
Utilise uniquement des services gratuits et sans limite pour la recherche de mots-clés avancée
"""

import requests
import time
import random
from typing import List, Dict, Any, Optional
from urllib.parse import quote_plus, urlencode
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

try:
    from crewai_tools import BaseTool
except ImportError:
    from crewai.tools.base_tool import BaseTool

class AdvancedKeywordResearchTool(BaseTool):
    """
    Outil avancé de recherche de mots-clés utilisant UNIQUEMENT des APIs gratuites
    """
    
    name: str = "advanced_keyword_research"
    description: str = "Recherche avancée de mots-clés avec estimation de volumes via sources gratuites multiples (Google Trends, suggestions, Reddit, etc.)"
    
    def __init__(self):
        super().__init__()
        print("✅ Advanced Keyword Research Tool initialized (100% FREE)")
        
        # Initialiser les propriétés d'instance (pas comme fields Pydantic)
        self._user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]
        
        # Initialiser pytrends (Google Trends - 100% GRATUIT)
        self._trends_available = False
        try:
            from pytrends.request import TrendReq
            self._pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 25), retries=2, backoff_factor=0.1)
            self._trends_available = True
            print("✅ Google Trends (pytrends) available")
        except ImportError:
            print("⚠️ pytrends not available - run: pip install pytrends")
        
        # APIs gratuites (optionnelles avec clés)
        self._reddit_available = bool(os.getenv("REDDIT_CLIENT_ID"))
        self._youtube_available = bool(os.getenv("YOUTUBE_API_KEY"))
        
        if self._reddit_available:
            print("✅ Reddit API available")
        if self._youtube_available:
            print("✅ YouTube API available")
    
    # Properties for backward compatibility
    @property
    def trends_available(self):
        return self._trends_available
    
    @property
    def youtube_available(self):
        return self._youtube_available
    
    @property
    def reddit_available(self):
        return self._reddit_available
    
    def get_headers(self):
        """Headers aléatoires pour éviter la détection"""
        return {
            'User-Agent': random.choice(self._user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
    
    def get_google_trends_data(self, keywords: List[str]) -> Dict[str, Any]:
        """Récupère les données Google Trends (100% GRATUIT - pas d'API key)"""
        if not self._trends_available:
            return {"error": "pytrends not available"}
        
        try:
            print(f"📈 Getting Google Trends data for: {keywords[:5]}")
            
            # Limiter à 5 keywords max pour éviter les erreurs
            search_terms = keywords[:5]
            
            # Construire les requêtes pour pytrends
            self._pytrends.build_payload(search_terms, cat=0, timeframe='today 12-m', geo='', gprop='')
            
            # Récupérer l'intérêt au fil du temps
            interest_over_time = self._pytrends.interest_over_time()
            
            # Récupérer les suggestions de requêtes associées
            related_queries = self._pytrends.related_queries()
            
            trends_data = {
                'search_terms': search_terms,
                'interest_data': interest_over_time.to_dict() if not interest_over_time.empty else {},
                'related_queries': related_queries,
                'timestamp': datetime.now().isoformat()
            }
            
            print(f"✅ Google Trends data collected for {len(search_terms)} terms")
            return trends_data
            
        except Exception as e:
            print(f"⚠️ Google Trends error: {e}")
            return {"error": str(e)}
    
    def get_youtube_suggestions(self, keyword: str) -> List[str]:
        """Récupère les suggestions YouTube (API gratuite avec quota élevé)"""
        if not self._youtube_available:
            return []
        
        try:
            print(f"🎥 Getting YouTube suggestions for: {keyword}")
            
            api_key = os.getenv("YOUTUBE_API_KEY")
            url = "https://www.googleapis.com/youtube/v3/search"
            
            params = {
                'part': 'snippet',
                'q': keyword,
                'type': 'video',
                'order': 'relevance',
                'maxResults': 20,
                'key': api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                suggestions = []
                
                for item in data.get('items', []):
                    title = item.get('snippet', {}).get('title', '')
                    # Extraire des mots-clés du titre
                    title_words = re.findall(r'\b[a-zA-Z]{3,}\b', title.lower())
                    suggestions.extend(title_words)
                
                # Retourner les termes uniques les plus fréquents
                unique_suggestions = list(set(suggestions))[:15]
                print(f"✅ Found {len(unique_suggestions)} YouTube suggestions")
                return unique_suggestions
            
        except Exception as e:
            print(f"⚠️ YouTube API error: {e}")
        
        return []
    
    def get_reddit_keywords(self, keyword: str) -> List[str]:
        """Récupère les mots-clés populaires depuis Reddit (API gratuite)"""
        if not self._reddit_available:
            return []
        
        try:
            print(f"🔍 Searching Reddit for: {keyword}")
            
            client_id = os.getenv("REDDIT_CLIENT_ID")
            client_secret = os.getenv("REDDIT_CLIENT_SECRET")
            user_agent = "KeywordResearch/1.0"
            
            # Authentification Reddit
            auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
            data = {
                'grant_type': 'client_credentials'
            }
            headers = {'User-Agent': user_agent}
            
            # Obtenir le token d'accès
            auth_response = requests.post('https://www.reddit.com/api/v1/access_token',
                                        auth=auth, data=data, headers=headers, timeout=10)
            
            if auth_response.status_code == 200:
                token = auth_response.json()['access_token']
                headers['Authorization'] = f'bearer {token}'
                
                # Rechercher des posts liés au keyword
                search_url = f"https://oauth.reddit.com/search"
                params = {
                    'q': keyword,
                    'type': 'link',
                    'sort': 'hot',
                    'limit': 20
                }
                
                search_response = requests.get(search_url, headers=headers, params=params, timeout=10)
                
                if search_response.status_code == 200:
                    data = search_response.json()
                    reddit_keywords = []
                    
                    for post in data.get('data', {}).get('children', []):
                        title = post.get('data', {}).get('title', '')
                        # Extraire mots-clés du titre
                        title_words = re.findall(r'\b[a-zA-Z]{3,}\b', title.lower())
                        reddit_keywords.extend(title_words)
                    
                    # Retourner les termes uniques
                    unique_keywords = list(set(reddit_keywords))[:15]
                    print(f"✅ Found {len(unique_keywords)} Reddit keywords")
                    return unique_keywords
            
        except Exception as e:
            print(f"⚠️ Reddit API error: {e}")
        
        return []
    
    def scrape_answer_the_public_style(self, keyword: str) -> List[str]:
        """Génère des questions style 'AnswerThePublic' (100% gratuit, pas d'API)"""
        try:
            print(f"❓ Generating question patterns for: {keyword}")
            
            question_patterns = [
                f"how to {keyword}",
                f"what is {keyword}",
                f"why {keyword}",
                f"when {keyword}",
                f"where {keyword}",
                f"who {keyword}",
                f"how does {keyword}",
                f"what does {keyword}",
                f"how much {keyword}",
                f"how many {keyword}",
                f"best {keyword}",
                f"top {keyword}",
                f"{keyword} guide",
                f"{keyword} tips",
                f"{keyword} examples",
                f"{keyword} benefits",
                f"{keyword} problems",
                f"{keyword} solutions",
                f"{keyword} 2024",
                f"{keyword} trends"
            ]
            
            print(f"✅ Generated {len(question_patterns)} question-based keywords")
            return question_patterns
            
        except Exception as e:
            print(f"⚠️ Question generation error: {e}")
            return []
    
    def estimate_keyword_difficulty(self, keyword: str) -> Dict[str, Any]:
        """Estime la difficulté d'un mot-clé via analyse SERP (gratuit)"""
        try:
            print(f"⚖️ Estimating difficulty for: {keyword}")
            
            # Recherche DuckDuckGo pour analyser la concurrence
            search_url = f"https://duckduckgo.com/html/?q={quote_plus(keyword)}"
            response = requests.get(search_url, headers=self.get_headers(), timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                results = soup.find_all('div', class_='result')
                
                # Analyser les types de sites dans les résultats
                authority_sites = 0
                total_results = len(results)
                
                authority_domains = ['wikipedia.org', 'forbes.com', 'reuters.com', 'bloomberg.com', 
                                   'investopedia.com', 'marketwatch.com', 'cnbc.com', 'wsj.com']
                
                for result in results:
                    link_elem = result.find('a', class_='result__a')
                    if link_elem:
                        href = link_elem.get('href', '')
                        if any(domain in href for domain in authority_domains):
                            authority_sites += 1
                
                # Calculer le score de difficulté
                authority_ratio = authority_sites / max(total_results, 1)
                
                if authority_ratio > 0.7:
                    difficulty = "Very High"
                    score = 90
                elif authority_ratio > 0.5:
                    difficulty = "High"  
                    score = 70
                elif authority_ratio > 0.3:
                    difficulty = "Medium"
                    score = 50
                else:
                    difficulty = "Low"
                    score = 30
                
                return {
                    'keyword': keyword,
                    'difficulty': difficulty,
                    'difficulty_score': score,
                    'authority_sites_ratio': authority_ratio,
                    'total_serp_results': total_results
                }
        
        except Exception as e:
            print(f"⚠️ Difficulty estimation error: {e}")
        
        return {'keyword': keyword, 'difficulty': 'Unknown', 'difficulty_score': 50}
    
    def _run(self, query: str) -> str:
        """Interface principale pour CrewAI"""
        try:
            print(f"\n🚀 ADVANCED KEYWORD RESEARCH for: '{query}'")
            print("=" * 60)
            
            # 1. Extraire les mots-clés de base de la query
            base_keywords = re.findall(r'\b[a-zA-Z]{3,}\b', query.lower())
            unique_keywords = list(set(base_keywords))[:5]  # Limiter pour éviter les quotas
            
            results = {
                'query': query,
                'timestamp': datetime.now().isoformat(),
                'base_keywords': unique_keywords,
                'trends_data': {},
                'youtube_suggestions': [],
                'reddit_keywords': [],
                'question_patterns': [],
                'difficulty_analysis': [],
                'total_keywords_found': 0
            }
            
            # 2. Google Trends data
            if self._trends_available and unique_keywords:
                print("\n📈 PHASE 1: Google Trends Analysis")
                results['trends_data'] = self.get_google_trends_data(unique_keywords)
                time.sleep(1)  # Respecter les limites
            
            # 3. YouTube suggestions (si API disponible)
            if self._youtube_available and unique_keywords:
                print("\n🎥 PHASE 2: YouTube Keyword Mining")
                for keyword in unique_keywords[:2]:  # Limiter pour éviter quota
                    youtube_suggestions = self.get_youtube_suggestions(keyword)
                    results['youtube_suggestions'].extend(youtube_suggestions)
                    time.sleep(1)
            
            # 4. Reddit keywords (si API disponible)
            if self._reddit_available and unique_keywords:
                print("\n🔍 PHASE 3: Reddit Trend Analysis")
                for keyword in unique_keywords[:2]:
                    reddit_keywords = self.get_reddit_keywords(keyword)
                    results['reddit_keywords'].extend(reddit_keywords)
                    time.sleep(2)  # Reddit a des limites plus strictes
            
            # 5. Question patterns (toujours disponible)
            print("\n❓ PHASE 4: Question-Based Keywords")
            for keyword in unique_keywords[:3]:
                question_keywords = self.scrape_answer_the_public_style(keyword)
                results['question_patterns'].extend(question_keywords)
            
            # 6. Difficulty analysis pour les mots-clés principaux
            print("\n⚖️ PHASE 5: Competition Analysis")
            for keyword in unique_keywords[:3]:
                difficulty = self.estimate_keyword_difficulty(keyword)
                results['difficulty_analysis'].append(difficulty)
                time.sleep(2)  # Éviter d'être bloqué
            
            # Calculer le total
            all_keywords = (results['youtube_suggestions'] + 
                          results['reddit_keywords'] + 
                          results['question_patterns'])
            results['total_keywords_found'] = len(set(all_keywords))
            
            # Formater la sortie pour CrewAI
            formatted_output = self._format_results_for_crewai(results)
            
            print(f"\n✅ ADVANCED KEYWORD RESEARCH COMPLETE!")
            print(f"📊 Total unique keywords found: {results['total_keywords_found']}")
            
            return formatted_output
            
        except Exception as e:
            return f"❌ Advanced keyword research error: {str(e)}"
    
    def _format_results_for_crewai(self, results: Dict) -> str:
        """Formate les résultats pour une sortie claire dans CrewAI"""
        output = f"🚀 ADVANCED KEYWORD RESEARCH RESULTS for: '{results['query']}'\n"
        output += f"⏰ Analysis completed: {results['timestamp']}\n"
        output += f"📊 Total unique keywords discovered: {results['total_keywords_found']}\n\n"
        
        # Base keywords
        if results['base_keywords']:
            output += "🎯 BASE KEYWORDS ANALYZED:\n"
            for i, keyword in enumerate(results['base_keywords'], 1):
                output += f"{i}. {keyword}\n"
            output += "\n"
        
        # Google Trends data
        if results['trends_data'].get('related_queries'):
            output += "📈 GOOGLE TRENDS INSIGHTS:\n"
            for term, queries in results['trends_data']['related_queries'].items():
                if queries and queries.get('top'):
                    top_queries = queries['top']
                    if hasattr(top_queries, 'head'):
                        top_list = top_queries.head(5).index.tolist()
                        for query in top_list:
                            output += f"• {query}\n"
            output += "\n"
        
        # YouTube suggestions
        if results['youtube_suggestions']:
            output += "🎥 YOUTUBE-DERIVED KEYWORDS (Top 10):\n"
            unique_youtube = list(set(results['youtube_suggestions']))[:10]
            for i, keyword in enumerate(unique_youtube, 1):
                output += f"{i}. {keyword}\n"
            output += "\n"
        
        # Reddit keywords  
        if results['reddit_keywords']:
            output += "🔍 REDDIT TRENDING KEYWORDS (Top 10):\n"
            unique_reddit = list(set(results['reddit_keywords']))[:10]
            for i, keyword in enumerate(unique_reddit, 1):
                output += f"{i}. {keyword}\n"
            output += "\n"
        
        # Question patterns
        if results['question_patterns']:
            output += "❓ QUESTION-BASED LONG-TAIL KEYWORDS (Top 15):\n"
            for i, question in enumerate(results['question_patterns'][:15], 1):
                output += f"{i}. {question}\n"
            output += "\n"
        
        # Competition analysis
        if results['difficulty_analysis']:
            output += "⚖️ KEYWORD DIFFICULTY ANALYSIS:\n"
            for analysis in results['difficulty_analysis']:
                output += f"• '{analysis['keyword']}': {analysis['difficulty']} "
                output += f"(Score: {analysis['difficulty_score']}/100)\n"
            output += "\n"
        
        output += "💡 RECOMMENDATION: Use a mix of low-difficulty keywords for quick wins "
        output += "and medium-difficulty keywords for long-term growth.\n"
        
        return output
    
    async def _arun(self, query: str) -> str:
        """Version asynchrone"""
        return self._run(query)

# Test unitaire
if __name__ == "__main__":
    print("🧪 TESTING ADVANCED KEYWORD RESEARCH TOOL")
    print("=" * 60)
    
    tool = AdvancedKeywordResearchTool()
    
    # Test avec une requête d'exemple
    test_query = "UMich consumer sentiment September preliminary"
    result = tool._run(test_query)
    
    print("\n📋 TEST RESULTS:")
    print(result[:500] + "..." if len(result) > 500 else result)
