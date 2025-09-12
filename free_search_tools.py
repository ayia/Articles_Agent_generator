# Outils de recherche web gratuits - AUCUNE API REQUISE
# Ce module utilise uniquement des sources publiques et gratuites
# - Pas d'inscription nécessaire
# - Pas de clés API 
# - Pas de limites de requêtes
# - Données en temps réel

import requests
from bs4 import BeautifulSoup
import feedparser
import json
import time
import random
from typing import List, Dict, Any, Optional
from urllib.parse import quote_plus
import re
from datetime import datetime, timedelta
from freshness_validator import DataFreshnessValidator

# Imports CrewAI pour l'héritage BaseTool
try:
    from crewai_tools import BaseTool
except ImportError:
    # Fallback si crewai_tools n'a pas BaseTool
    from crewai.tools.base_tool import BaseTool

class FreeWebSearchTool:
    """Outil de recherche web gratuit utilisant plusieurs sources publiques"""
    
    def __init__(self):
        # Initialiser le validateur de fraîcheur
        self.freshness_validator = DataFreshnessValidator()
        print("✅ Validateur de fraîcheur des données activé")
        
        # User agents pour éviter les blocages
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
        ]
        
        # Sources d'actualités gratuites avec RSS
        self.news_sources = {
          'forexlive': 'https://www.forexlive.com/feed/',
            'actionforex': 'https://www.actionforex.com/feed/',
            'leaprate': 'https://www.leaprate.com/feed/',
            'fxnewsgroup': 'https://fxnewsgroup.com/feed/',
            'finance_magnates': 'https://www.financemagnates.com/feed/',
            'forexcrunch': 'https://www.forexcrunch.com/feed/',
        }
        
        # Sites de recherche publics (pas Google, mais alternatives gratuites)
        self.search_engines = [
            'https://duckduckgo.com/html/?q=',
            'https://search.brave.com/search?q=',
        ]
    
    def get_headers(self):
        """Génère des headers aléatoires pour éviter la détection"""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def search_rss_feeds(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Recherche dans les flux RSS gratuits"""
        results = []
        query_lower = query.lower()
        
        print(f"🔍 Recherche RSS pour: {query}")
        
        for source_name, rss_url in self.news_sources.items():
            try:
                # Ajouter un délai aléatoire pour éviter les blocages
                time.sleep(random.uniform(0.5, 1.5))
                
                print(f"  📡 Scan de {source_name}...")
                feed = feedparser.parse(rss_url)
                
                for entry in feed.entries[:20]:  # Limiter à 20 par source
                    title = entry.get('title', '')
                    summary = entry.get('summary', '')
                    link = entry.get('link', '')
                    published = entry.get('published', '')
                    
                    # Recherche de mots-clés dans le titre et résumé
                    text_to_search = f"{title} {summary}".lower()
                    query_words = query_lower.split()
                    
                    # Si au moins un mot-clé est trouvé
                    if any(word in text_to_search for word in query_words):
                        results.append({
                            'title': title,
                            'summary': summary,
                            'url': link,
                            'published': published,
                            'source': source_name,
                            'relevance_score': sum(1 for word in query_words if word in text_to_search)
                        })
                        
                        if len(results) >= limit:
                            break
                            
            except Exception as e:
                print(f"  ⚠️ Erreur avec {source_name}: {str(e)}")
                continue
        
        # Trier par pertinence
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        return results[:limit]
    
    def search_duckduckgo(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Recherche sur DuckDuckGo (gratuit, pas de tracking)"""
        try:
            search_url = f"https://duckduckgo.com/html/?q={quote_plus(query)}"
            
            response = requests.get(search_url, headers=self.get_headers(), timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            results = []
            
            # Recherche des résultats DuckDuckGo
            for result in soup.find_all('div', class_='result')[:limit]:
                try:
                    title_elem = result.find('a', class_='result__a')
                    snippet_elem = result.find('div', class_='result__snippet')
                    
                    if title_elem and snippet_elem:
                        title = title_elem.get_text().strip()
                        url = title_elem.get('href', '')
                        snippet = snippet_elem.get_text().strip()
                        
                        results.append({
                            'title': title,
                            'url': url,
                            'snippet': snippet,
                            'source': 'duckduckgo'
                        })
                except:
                    continue
            
            return results
        except Exception as e:
            print(f"Erreur DuckDuckGo: {e}")
            return []
    
    def get_free_business_data(self, query: str) -> Dict[str, Any]:
        """Récupère des données business gratuites de sources publiques"""
        business_data = {
            'market_data': self.get_free_market_data(),
            'economic_indicators': self.get_free_economic_data(),
            'news_analysis': self.search_rss_feeds(query, limit=15)
        }
        return business_data
    
    def get_free_market_data(self) -> Dict[str, Any]:
        """Données de marché gratuites (sans API)"""
        try:
            # Yahoo Finance RSS (gratuit)
            market_rss = 'https://feeds.finance.yahoo.com/rss/2.0/headline'
            feed = feedparser.parse(market_rss)
            
            market_news = []
            for entry in feed.entries[:5]:
                market_news.append({
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'published': entry.get('published', '')
                })
            
            return {
                'source': 'Yahoo Finance RSS',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'market_headlines': market_news
            }
        except:
            return {'error': 'Données de marché temporairement indisponibles'}
    
    def get_free_economic_data(self) -> Dict[str, Any]:
        """Indicateurs économiques gratuits"""
        try:
            # Sources gouvernementales gratuites
            economic_sources = [
                'https://www.ecb.europa.eu/rss/press.html',  # BCE
                'https://www.federalreserve.gov/feeds/press_all.xml',  # Fed US
            ]
            
            economic_news = []
            for source_url in economic_sources:
                try:
                    feed = feedparser.parse(source_url)
                    for entry in feed.entries[:3]:
                        economic_news.append({
                            'title': entry.get('title', ''),
                            'summary': entry.get('summary', ''),
                            'published': entry.get('published', '')
                        })
                except:
                    continue
            
            return {
                'economic_updates': economic_news,
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except:
            return {'error': 'Données économiques temporairement indisponibles'}
    
    def comprehensive_search(self, query: str, max_results: int = 20, min_freshness_score: float = 0.3) -> Dict[str, Any]:
        """Recherche complète utilisant toutes les sources gratuites avec validation de fraîcheur"""
        print(f"\n🔍 RECHERCHE GRATUITE COMPLÈTE pour: '{query}'")
        print("=" * 60)
        print(f"📅 Validation de fraîcheur activée (score min: {min_freshness_score})")
        
        results = {
            'query': query,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'sources_used': [],
            'rss_results': [],
            'search_results': [],
            'business_data': {},
            'freshness_validation': {},
            'total_results': 0,
            'fresh_results': 0,
            'filtered_results': 0
        }
        
        try:
            # 1. Recherche RSS
            print("📡 Recherche dans les flux RSS...")
            rss_results = self.search_rss_feeds(query, limit=max_results//2)
            results['rss_results'] = rss_results
            results['sources_used'].append('RSS Feeds')
            print(f"  ✅ Trouvé {len(rss_results)} résultats RSS")
            
            # Délai pour éviter les blocages
            time.sleep(2)
            
            # 2. Recherche DuckDuckGo
            print("🦆 Recherche DuckDuckGo...")
            search_results = self.search_duckduckgo(query, limit=max_results//2)
            results['search_results'] = search_results
            results['sources_used'].append('DuckDuckGo')
            print(f"  ✅ Trouvé {len(search_results)} résultats DuckDuckGo")
            
            # 3. Données business gratuites
            print("💼 Récupération des données business...")
            business_data = self.get_free_business_data(query)
            results['business_data'] = business_data
            results['sources_used'].append('Business Data')
            
            # 4. VALIDATION DE FRAÎCHEUR - ÉTAPE CRITIQUE
            print("\n📅 VALIDATION DE FRAÎCHEUR...")
            all_articles = rss_results + search_results
            
            if all_articles:
                # Valider la fraîcheur de tous les articles
                freshness_report = self.freshness_validator.validate_dataset_freshness(all_articles)
                results['freshness_validation'] = freshness_report
                
                print(f"  📊 Score de fraîcheur global: {freshness_report['overall_freshness_score']:.2f}")
                print(f"  ✅ Articles acceptables: {freshness_report['freshness_summary']['acceptable_percentage']:.1f}%")
                
                # Filtrer par fraîcheur
                fresh_rss = self.freshness_validator.filter_by_freshness(rss_results, min_freshness_score)
                fresh_search = self.freshness_validator.filter_by_freshness(search_results, min_freshness_score)
                
                # Mettre à jour les résultats avec les articles filtrés
                results['rss_results'] = fresh_rss
                results['search_results'] = fresh_search
                results['fresh_results'] = len(fresh_rss) + len(fresh_search)
                results['filtered_results'] = len(all_articles) - results['fresh_results']
                
                print(f"  🔥 Articles frais conservés: {results['fresh_results']}")
                print(f"  🗑️ Articles obsolètes filtrés: {results['filtered_results']}")
                
                # Afficher les avertissements
                if freshness_report['recommendations']:
                    print(f"  ⚠️ Recommandations fraîcheur:")
                    for rec in freshness_report['recommendations'][:3]:
                        print(f"    {rec}")
            
            results['total_results'] = results['fresh_results']
            
            print(f"\n✅ RECHERCHE TERMINÉE: {results['total_results']} résultats FRAIS trouvés")
            print(f"📊 Sources utilisées: {', '.join(results['sources_used'])}")
            print(f"📅 Validation de fraîcheur: ACTIVÉE")
            
        except Exception as e:
            print(f"❌ Erreur dans la recherche: {e}")
            results['error'] = str(e)
        
        return results


class FreeSearchCrewAITool(BaseTool):
    """Intégration avec CrewAI - Outil de recherche gratuit compatible BaseTool"""
    
    name: str = "free_web_search"
    description: str = "Recherche web gratuite utilisant RSS feeds et sources publiques. Utilise des flux RSS de Reuters, BBC, Bloomberg, CNBC et autres sources d'actualités pour obtenir des informations récentes. Inclut la validation de fraîcheur des données pour s'assurer que seules les sources récentes sont utilisées."
    
    def __init__(self):
        super().__init__()
    
    def _run(self, query: str) -> str:
        """Interface pour CrewAI avec validation de fraîcheur intégrée"""
        try:
            # Instancier l'outil de recherche directement dans la méthode
            search_engine = FreeWebSearchTool()
            results = search_engine.comprehensive_search(query, max_results=15, min_freshness_score=0.3)
            
            # Formatter les résultats pour CrewAI avec métriques de fraîcheur
            formatted_output = f"🔍 RÉSULTATS DE RECHERCHE POUR: {query}\n"
            formatted_output += f"⏰ Recherche effectuée le: {results['timestamp']}\n"
            
            # Ajouter les métriques de fraîcheur
            if 'freshness_validation' in results and results['freshness_validation']:
                fv = results['freshness_validation']['freshness_summary']
                formatted_output += f"📅 VALIDATION FRAÎCHEUR: Score {fv['overall_freshness_score']:.2f} | "
                formatted_output += f"{fv['acceptable_percentage']:.0f}% acceptable | "
                formatted_output += f"Âge moyen: {fv['average_age_days']:.1f} jours\n"
                formatted_output += f"🔥 {results['fresh_results']} articles frais | "
                formatted_output += f"🗑️ {results['filtered_results']} filtrés\n\n"
            else:
                formatted_output += "\n"
            
            # Résultats RSS avec métriques de fraîcheur
            if results['rss_results']:
                formatted_output += "📡 ACTUALITÉS RSS (VALIDÉES FRAÎCHEUR):\n"
                for i, item in enumerate(results['rss_results'][:10], 1):
                    formatted_output += f"{i}. {item['title']}\n"
                    formatted_output += f"   Source: {item['source']} | {item.get('published', 'N/A')}\n"
                    
                    # Ajouter les infos de fraîcheur si disponibles
                    if 'freshness_validation' in item:
                        fv = item['freshness_validation']
                        freshness_emoji = {'excellent': '🔥', 'very_good': '✅', 'good': '👍', 'acceptable': '⚠️', 'poor': '❌', 'outdated': '🚫'}.get(fv['freshness_level'], '❓')
                        formatted_output += f"   {freshness_emoji} Fraîcheur: {fv['freshness_level']} (score: {fv['freshness_score']:.2f})"
                        if fv['age_days'] is not None:
                            formatted_output += f" | Âge: {fv['age_days']} jours"
                        formatted_output += "\n"
                    
                    formatted_output += f"   Résumé: {item['summary'][:200]}...\n"
                    formatted_output += f"   Lien: {item['url']}\n\n"
            
            # Résultats de recherche
            if results['search_results']:
                formatted_output += "🔍 RÉSULTATS DE RECHERCHE:\n"
                for i, item in enumerate(results['search_results'][:5], 1):
                    formatted_output += f"{i}. {item['title']}\n"
                    formatted_output += f"   {item['snippet'][:200]}...\n"
                    formatted_output += f"   Lien: {item['url']}\n\n"
            
            # Données business
            if results['business_data'].get('news_analysis'):
                formatted_output += "💼 ANALYSE BUSINESS:\n"
                for item in results['business_data']['news_analysis'][:5]:
                    formatted_output += f"• {item['title']}\n"
            
            return formatted_output
            
        except Exception as e:
            return f"❌ Erreur de recherche: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Version asynchrone - utilise la version synchrone"""
        return self._run(query)


# Test rapide
if __name__ == "__main__":
    print("🧪 TEST DE L'OUTIL DE RECHERCHE GRATUIT")
    print("=" * 50)
    
    # Créer l'instance
    search_tool = FreeWebSearchTool()
    
    # Test avec une requête
    test_query = "Trump tariffs China EU business news"
    results = search_tool.comprehensive_search(test_query, max_results=10)
    
    print(f"\n📊 RÉSULTATS DU TEST:")
    print(f"Total des résultats: {results['total_results']}")
    print(f"Sources utilisées: {results['sources_used']}")
    
    if results['rss_results']:
        print(f"\nPremier résultat RSS: {results['rss_results'][0]['title']}")
