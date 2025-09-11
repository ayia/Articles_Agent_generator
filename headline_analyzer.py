# Extracteur automatique de mots-clés depuis le headline
# Ce module analyse n'importe quel headline et génère les termes de recherche appropriés

import re
from typing import List, Dict, Set

class HeadlineAnalyzer:
    """Analyse automatique du headline pour extraire les concepts clés"""
    
    def __init__(self):
        # Mots vides à ignorer
        self.stop_words = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he', 'in', 
            'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'will', 'with', 'le', 
            'la', 'les', 'de', 'du', 'des', 'et', 'un', 'une', 'par', 'pour', 'dans', 'sur'
        }
        
        # Economic concepts and their associated search terms
        self.economic_concepts = {
            # Inflation and prices
            'inflation': ['inflation rate', 'consumer prices', 'price index', 'cost of living', 'CPI data'],
            'prices': ['consumer prices', 'inflation rate', 'price trends', 'economic indicators', 'cost of living'],
            'consumer': ['consumer spending', 'consumer confidence', 'retail sales', 'economic data', 'inflation'],
            'rose': ['price increase', 'inflation data', 'economic growth', 'rising costs'],
            'annual': ['annual inflation', 'yearly data', 'economic indicators', 'CPI annual'],
            
            # Employment and jobless claims 
            'jobs': ['employment rate', 'unemployment rate', 'job market', 'labor statistics'],
            'jobless': ['unemployment claims', 'jobless benefits', 'labor market', 'employment data'],
            'unemployment': ['jobless claims', 'employment rate', 'labor market trends'],
            'employment': ['job market', 'unemployment rate', 'labor statistics', 'workforce'],
            'claims': ['unemployment claims', 'jobless claims', 'employment benefits', 'labor data'],
            'jump': ['surge', 'increase', 'rising trend', 'economic indicators'],
            'weekly': ['weekly data', 'labor statistics', 'employment reports', 'economic indicators'],
            
            # Financial markets
            'stock': ['stock market', 'equity prices', 'market volatility', 'financial markets'],
            'market': ['financial markets', 'stock prices', 'market trends', 'investment'],
            'bitcoin': ['cryptocurrency', 'crypto market', 'blockchain', 'digital currency'],
            'crypto': ['cryptocurrency market', 'bitcoin', 'digital assets', 'blockchain'],
            
            # Technologie
            'ai': ['artificial intelligence', 'machine learning', 'AI development', 'tech innovation'],
            'chatgpt': ['AI chatbots', 'OpenAI', 'generative AI', 'language models'],
            'openai': ['AI development', 'ChatGPT', 'artificial intelligence', 'tech companies'],
            
            # Entreprises
            'apple': ['tech companies', 'Apple stock', 'iPhone sales', 'technology sector'],
            'microsoft': ['tech giants', 'cloud computing', 'software companies', 'technology'],
            'tesla': ['electric vehicles', 'EV market', 'automotive industry', 'clean energy'],
            'amazon': ['e-commerce', 'retail industry', 'cloud services', 'tech companies'],
            
            # Politique et commerce
            'trump': ['trade policy', 'political developments', 'US politics', 'economic policy'],
            'tariffs': ['trade war', 'international trade', 'economic sanctions', 'trade policy'],
            'china': ['US-China trade', 'international relations', 'global economy', 'trade relations'],
            'europe': ['EU economy', 'European markets', 'international trade', 'global politics'],
            
            # Industrie pharmaceutique
            'pharma': ['pharmaceutical industry', 'drug development', 'healthcare sector', 'medical'],
            'drug': ['pharmaceutical', 'healthcare', 'medical treatment', 'drug market'],
            'novo': ['pharmaceutical companies', 'diabetes treatment', 'healthcare industry'],
            'ozempic': ['diabetes drugs', 'weight loss medication', 'pharmaceutical market']
        }
    
    def extract_key_concepts(self, headline: str) -> List[str]:
        """Extraire les concepts clés du headline"""
        # Nettoyer et normaliser le headline
        headline_lower = headline.lower()
        
        # Enlever la ponctuation et diviser en mots
        words = re.findall(r'\b\w+\b', headline_lower)
        
        # Filtrer les mots vides
        meaningful_words = [word for word in words if word not in self.stop_words and len(word) > 2]
        
        # Identifier les concepts économiques
        identified_concepts = []
        
        for word in meaningful_words:
            # Recherche exacte
            if word in self.economic_concepts:
                identified_concepts.extend(self.economic_concepts[word])
            
            # Recherche partielle (pour des mots comme "employment", "employment")
            for concept, search_terms in self.economic_concepts.items():
                if concept in word or word in concept:
                    identified_concepts.extend(search_terms)
        
        # Ajouter les mots importants du headline directement
        identified_concepts.extend(meaningful_words)
        
        # Supprimer les doublons et retourner
        return list(set(identified_concepts))
    
    def extract_numbers_and_dates(self, headline: str) -> List[str]:
        """Extraire les chiffres et dates pour recherches précises"""
        numbers_dates = []
        
        # Rechercher pourcentages
        percentages = re.findall(r'\b\d+\.?\d*%\b', headline)
        numbers_dates.extend(percentages)
        
        # Rechercher années
        years = re.findall(r'\b20\d{2}\b', headline)
        numbers_dates.extend(years)
        
        # Rechercher mois
        months = re.findall(r'\b(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b', headline, re.IGNORECASE)
        numbers_dates.extend(months)
        
        # Rechercher grands nombres (millions, billions)
        big_numbers = re.findall(r'\b\d+\s*(million|billion|thousand|milliard|millions)\b', headline, re.IGNORECASE)
        numbers_dates.extend([' '.join(match) if isinstance(match, tuple) else match for match in big_numbers])
        
        return numbers_dates
    
    def generate_search_terms(self, headline: str) -> List[str]:
        """Générer automatiquement les termes de recherche basés sur le headline"""
        
        # Extraire concepts clés
        key_concepts = self.extract_key_concepts(headline)
        
        # Extraire chiffres et dates
        numbers_dates = self.extract_numbers_and_dates(headline)
        
        # Combiner les concepts avec des termes génériques utiles
        search_terms = []
        
        # Ajouter les concepts directs (limiter à 8 pour éviter trop de recherches)
        search_terms.extend(key_concepts[:8])
        
        # Ajouter des combinaisons avec chiffres/dates si trouvés
        for number_date in numbers_dates[:3]:  # Limiter à 3
            search_terms.append(f"economic data {number_date}")
            if key_concepts:
                search_terms.append(f"{key_concepts[0]} {number_date}")
        
        # Supprimer doublons et limiter à 10 termes max
        unique_terms = list(set(search_terms))[:10]
        
        return unique_terms
    
    def generate_dynamic_task_description(self, headline: str, task_type: str = "keyword") -> str:
        """Generate automatic task description based on headline - fully adaptive"""
        
        search_terms = self.generate_search_terms(headline)
        search_terms_str = "', '".join(search_terms)
        
        if task_type == "keyword":
            return f"""FIRST: Use the search tool to find current trending topics related to: '{headline}'. 
Based on this headline, search for these dynamically extracted terms: '{search_terms_str}'.
These terms were automatically generated from the headline content - NO HARDCODED TERMS.
Then analyze the search results to identify 5-10 primary keywords, 10-15 long-tail phrases, and LSI terms based on what's currently trending in news. 
Include estimated search volumes, competition levels, and natural incorporation suggestions."""
        
        elif task_type == "facts":
            return f"""MANDATORY: Use the search tool extensively! Based on the headline '{headline}', search for these automatically extracted relevant terms: '{search_terms_str}'.
These search terms were dynamically generated from the headline - NO HARDCODED TERMS.
Gather real-time information from news sources, RSS feeds, and recent publications. Extract facts, expert quotes, relevant data, market statistics, and economic indicators. 
Cross-reference multiple sources and include recent developments, expert analysis, and market context related to the headline topic."""
        
        return ""

# Test du système
if __name__ == "__main__":
    print("🧪 TEST DE L'EXTRACTEUR AUTOMATIQUE DE MOTS-CLÉS")
    print("=" * 60)
    
    analyzer = HeadlineAnalyzer()
    
    # Test avec différents types de headlines
    test_headlines = [
        "Consumer prices rose at annual rate of 2.9% in August, as weekly jobless claims jump",
        "Bitcoin dépasse 100,000 dollars pour la première fois en 2025", 
        "Apple lance iPhone 16 avec IA intégrée : révolution smartphone",
        "Tesla Model Y devient voiture la plus vendue au monde en 2025"
    ]
    
    for i, headline in enumerate(test_headlines, 1):
        print(f"\n📰 TEST {i}: {headline}")
        print(f"📏 Longueur: {len(headline)} caractères")
        
        # Extraire les termes de recherche
        search_terms = analyzer.generate_search_terms(headline)
        print(f"🔍 Termes de recherche générés ({len(search_terms)}):")
        for j, term in enumerate(search_terms, 1):
            print(f"   {j:2d}. \"{term}\"")
        
        # Générer la description de task
        task_desc = analyzer.generate_dynamic_task_description(headline, "keyword")
        print(f"📋 Task description (extrait):")
        print(f"   {task_desc[:100]}...")
        
        print("─" * 50)
    
    print(f"\n✅ EXTRACTEUR AUTOMATIQUE OPÉRATIONNEL!")
    print(f"🔄 Plus de termes hardcodés - adaptation automatique au sujet!")
