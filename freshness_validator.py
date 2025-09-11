# Système de Vérification de Fraîcheur des Données
# Module pour s'assurer que les articles SEO utilisent des informations récentes et pertinentes
# CRITIQUE pour le SEO car Google privilégie le contenu frais

import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple, Optional
import dateutil.parser
from dateutil.relativedelta import relativedelta

class DataFreshnessValidator:
    """Validateur de fraîcheur des données pour articles SEO"""
    
    def __init__(self):
        # Seuils de fraîcheur (en jours)
        self.freshness_thresholds = {
            'excellent': 1,      # Articles d'aujourd'hui ou d'hier
            'very_good': 7,      # Articles de la semaine
            'good': 30,          # Articles du mois
            'acceptable': 90,    # Articles du trimestre
            'poor': 365,         # Articles de l'année
            'outdated': float('inf')  # Plus ancien qu'un an
        }
        
        # Pondération par type de contenu
        self.content_type_weights = {
            'breaking_news': 0.5,    # Actualités : fraîcheur critique
            'market_data': 1,        # Données de marché : très important
            'business_analysis': 7,   # Analyses : acceptables sur une semaine
            'industry_report': 30,    # Rapports : OK sur un mois
            'background_info': 90     # Info contextuelle : OK sur un trimestre
        }
        
        # Expressions régulières pour détecter les dates dans le texte
        self.date_patterns = [
            r'\b(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})\b',  # DD/MM/YYYY ou MM/DD/YYYY
            r'\b(\d{4})[\/\-](\d{1,2})[\/\-](\d{1,2})\b',  # YYYY/MM/DD
            r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),?\s+(\d{4})\b',
            r'\b(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})\b',
            r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.?\s+(\d{1,2}),?\s+(\d{4})\b'
        ]
        
        # Mots-clés indiquant la fraîcheur
        self.freshness_indicators = {
            'breaking': 1.0,
            'latest': 0.9,
            'today': 1.0,
            'yesterday': 0.9,
            'this week': 0.8,
            'recent': 0.7,
            'current': 0.8,
            'new': 0.7,
            'updated': 0.8,
            'just in': 1.0,
            'developing': 0.9
        }
    
    def parse_date(self, date_string: str) -> Optional[datetime]:
        """Parse différents formats de date"""
        if not date_string:
            return None
            
        try:
            # Essayer dateutil.parser d'abord (très flexible)
            return dateutil.parser.parse(date_string)
        except:
            pass
            
        # Essayer nos patterns réguliers
        for pattern in self.date_patterns:
            match = re.search(pattern, date_string, re.IGNORECASE)
            if match:
                try:
                    groups = match.groups()
                    if len(groups) == 3:
                        # Détecter le format et parser
                        if groups[0].isdigit() and len(groups[0]) == 4:  # YYYY first
                            return datetime(int(groups[0]), int(groups[1]), int(groups[2]))
                        else:
                            # Assumer DD/MM/YYYY ou MM/DD/YYYY
                            return datetime(int(groups[2]), int(groups[1]), int(groups[0]))
                except:
                    continue
                    
        return None
    
    def calculate_age_in_days(self, article_date: datetime) -> int:
        """Calcule l'âge d'un article en jours"""
        now = datetime.now()
        if article_date.tzinfo is not None:
            # Si l'article a un timezone, on l'utilise
            from datetime import timezone
            now = datetime.now(timezone.utc)
            if article_date.tzinfo != timezone.utc:
                article_date = article_date.astimezone(timezone.utc)
        else:
            # Assurer qu'on compare des datetime naifs
            now = now.replace(tzinfo=None)
            article_date = article_date.replace(tzinfo=None)
            
        delta = now - article_date
        return delta.days
    
    def get_freshness_score(self, age_days: int, content_type: str = 'business_analysis') -> Tuple[str, float]:
        """Calcule le score de fraîcheur (niveau + score numérique)"""
        # Ajuster l'âge selon le type de contenu
        weight = self.content_type_weights.get(content_type, 7)
        adjusted_age = age_days / max(1, weight / 7)  # Normaliser par rapport à business_analysis
        
        # Déterminer le niveau de fraîcheur
        if adjusted_age <= self.freshness_thresholds['excellent']:
            return 'excellent', 1.0
        elif adjusted_age <= self.freshness_thresholds['very_good']:
            return 'very_good', 0.9
        elif adjusted_age <= self.freshness_thresholds['good']:
            return 'good', 0.7
        elif adjusted_age <= self.freshness_thresholds['acceptable']:
            return 'acceptable', 0.5
        elif adjusted_age <= self.freshness_thresholds['poor']:
            return 'poor', 0.3
        else:
            return 'outdated', 0.1
    
    def detect_freshness_indicators(self, text: str) -> float:
        """Détecte les indicateurs de fraîcheur dans le texte"""
        text_lower = text.lower()
        max_indicator_score = 0.0
        
        for indicator, score in self.freshness_indicators.items():
            if indicator in text_lower:
                max_indicator_score = max(max_indicator_score, score)
                
        return max_indicator_score
    
    def validate_article_freshness(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """Valide la fraîcheur d'un article et retourne des métriques détaillées"""
        validation_result = {
            'article_title': article.get('title', 'Unknown'),
            'source': article.get('source', 'Unknown'),
            'original_date': article.get('published', ''),
            'parsed_date': None,
            'age_days': None,
            'freshness_level': 'unknown',
            'freshness_score': 0.0,
            'content_type': 'business_analysis',  # Par défaut
            'freshness_indicators': [],
            'is_acceptable': False,
            'warnings': []
        }
        
        try:
            # 1. Parser la date
            date_str = article.get('published', '') or article.get('date', '')
            if date_str:
                parsed_date = self.parse_date(date_str)
                if parsed_date:
                    validation_result['parsed_date'] = parsed_date
                    validation_result['age_days'] = self.calculate_age_in_days(parsed_date)
                    
                    # 2. Déterminer le type de contenu
                    content_type = self.classify_content_type(article)
                    validation_result['content_type'] = content_type
                    
                    # 3. Calculer le score de fraîcheur
                    freshness_level, freshness_score = self.get_freshness_score(
                        validation_result['age_days'], content_type
                    )
                    validation_result['freshness_level'] = freshness_level
                    validation_result['freshness_score'] = freshness_score
                    
                    # 4. Détecter les indicateurs de fraîcheur
                    text_content = f"{article.get('title', '')} {article.get('summary', '')} {article.get('snippet', '')}"
                    indicator_boost = self.detect_freshness_indicators(text_content)
                    validation_result['freshness_indicators'] = [k for k, v in self.freshness_indicators.items() if k in text_content.lower()]
                    
                    # Bonus pour les indicateurs
                    validation_result['freshness_score'] = min(1.0, freshness_score + (indicator_boost * 0.1))
                    
                    # 5. Déterminer si acceptable
                    validation_result['is_acceptable'] = freshness_score >= 0.5  # Seuil configurable
                    
                    # 6. Générer les avertissements
                    if validation_result['age_days'] > 90:
                        validation_result['warnings'].append(f"Article ancien ({validation_result['age_days']} jours)")
                    if freshness_level == 'outdated':
                        validation_result['warnings'].append("Contenu obsolète - impact SEO négatif possible")
                        
                else:
                    validation_result['warnings'].append("Impossible de parser la date")
            else:
                validation_result['warnings'].append("Aucune date trouvée")
                
        except Exception as e:
            validation_result['warnings'].append(f"Erreur de validation: {str(e)}")
        
        return validation_result
    
    def classify_content_type(self, article: Dict[str, Any]) -> str:
        """Classifie le type de contenu pour ajuster les seuils de fraîcheur"""
        text_content = f"{article.get('title', '')} {article.get('summary', '')} {article.get('snippet', '')}".lower()
        
        # Mots-clés pour identifier le type
        type_keywords = {
            'breaking_news': ['breaking', 'urgent', 'alert', 'just in', 'developing'],
            'market_data': ['stock', 'market', 'trading', 'price', 'shares', 'earnings'],
            'business_analysis': ['analysis', 'report', 'study', 'research', 'outlook'],
            'industry_report': ['industry', 'sector', 'quarterly', 'annual', 'forecast'],
            'background_info': ['background', 'history', 'context', 'overview']
        }
        
        # Score chaque type
        type_scores = {}
        for content_type, keywords in type_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_content)
            if score > 0:
                type_scores[content_type] = score
        
        # Retourner le type avec le meilleur score, ou 'business_analysis' par défaut
        if type_scores:
            return max(type_scores, key=type_scores.get)
        else:
            return 'business_analysis'
    
    def validate_dataset_freshness(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Valide la fraîcheur d'un ensemble d'articles"""
        if not articles:
            return {
                'total_articles': 0,
                'validation_results': [],
                'freshness_summary': {},
                'recommendations': [],
                'overall_freshness_score': 0.0
            }
        
        validation_results = []
        freshness_levels = {'excellent': 0, 'very_good': 0, 'good': 0, 'acceptable': 0, 'poor': 0, 'outdated': 0, 'unknown': 0}
        total_score = 0.0
        acceptable_count = 0
        
        # Valider chaque article
        for article in articles:
            result = self.validate_article_freshness(article)
            validation_results.append(result)
            
            freshness_levels[result['freshness_level']] += 1
            total_score += result['freshness_score']
            if result['is_acceptable']:
                acceptable_count += 1
        
        # Calculer les métriques globales
        overall_score = total_score / len(articles) if articles else 0.0
        acceptable_percentage = (acceptable_count / len(articles)) * 100 if articles else 0.0
        
        # Générer des recommandations
        recommendations = []
        if acceptable_percentage < 70:
            recommendations.append("⚠️ Moins de 70% des sources sont suffisamment fraîches")
        if freshness_levels['outdated'] > 0:
            recommendations.append(f"❌ {freshness_levels['outdated']} source(s) obsolète(s) détectée(s)")
        if overall_score < 0.6:
            recommendations.append("📈 Score de fraîcheur global faible - chercher des sources plus récentes")
        if freshness_levels['excellent'] == 0:
            recommendations.append("🔥 Aucune source très récente - ajouter des breaking news si possible")
        
        return {
            'total_articles': len(articles),
            'validation_results': validation_results,
            'freshness_summary': {
                'levels_distribution': freshness_levels,
                'acceptable_percentage': acceptable_percentage,
                'overall_freshness_score': overall_score,
                'average_age_days': sum(r['age_days'] for r in validation_results if r['age_days'] is not None) / max(1, len([r for r in validation_results if r['age_days'] is not None]))
            },
            'recommendations': recommendations,
            'overall_freshness_score': overall_score
        }
    
    def filter_by_freshness(self, articles: List[Dict[str, Any]], min_score: float = 0.5) -> List[Dict[str, Any]]:
        """Filtre les articles selon leur fraîcheur"""
        filtered_articles = []
        
        for article in articles:
            validation = self.validate_article_freshness(article)
            if validation['freshness_score'] >= min_score:
                # Ajouter les métriques de fraîcheur à l'article
                article['freshness_validation'] = validation
                filtered_articles.append(article)
        
        return filtered_articles


# Test rapide du validateur
if __name__ == "__main__":
    print("🧪 TEST DU VALIDATEUR DE FRAÎCHEUR")
    print("=" * 50)
    
    validator = DataFreshnessValidator()
    
    # Données de test
    test_articles = [
        {
            'title': 'Breaking: Trump announces new tariffs',
            'published': '2025-09-11T08:00:00Z',
            'summary': 'Latest breaking news about trade policy',
            'source': 'Reuters'
        },
        {
            'title': 'Old market analysis from 2023',
            'published': '2023-01-15T10:00:00Z',
            'summary': 'Historical market data and trends',
            'source': 'Bloomberg'
        }
    ]
    
    # Test de validation
    dataset_result = validator.validate_dataset_freshness(test_articles)
    
    print(f"✅ Articles testés: {dataset_result['total_articles']}")
    print(f"📊 Score global de fraîcheur: {dataset_result['overall_freshness_score']:.2f}")
    print(f"📈 Pourcentage acceptable: {dataset_result['freshness_summary']['acceptable_percentage']:.1f}%")
    
    if dataset_result['recommendations']:
        print("\n💡 Recommandations:")
        for rec in dataset_result['recommendations']:
            print(f"  {rec}")
    
    print("\n🎯 Validateur de fraîcheur fonctionnel !")
