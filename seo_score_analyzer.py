# Analyseur de Score SEO pour évaluer la page HTML générée
# Estime le score SEO et donne des recommandations pour atteindre 65-80%

import os
import re
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class SEOScoreAnalyzer:
    """Analyseur de score SEO pour pages HTML"""
    
    def __init__(self, html_file_path: str, json_file_path: str):
        self.html_file = html_file_path
        self.json_file = json_file_path
        
        # Charger les fichiers
        with open(html_file_path, 'r', encoding='utf-8') as f:
            self.html_content = f.read()
        
        with open(json_file_path, 'r', encoding='utf-8') as f:
            self.json_data = json.load(f)
        
        # Parser HTML
        self.soup = BeautifulSoup(self.html_content, 'html.parser')
        
        # Scores par catégorie
        self.scores = {}
        self.recommendations = []
    
    def analyze_meta_tags(self) -> int:
        """Analyser les meta tags (25 points max)"""
        score = 0
        
        # Title tag (5 points)
        title = self.soup.find('title')
        if title and title.text.strip():
            score += 5
            title_length = len(title.text)
            if 30 <= title_length <= 60:
                score += 2  # Bonus pour longueur optimale
            elif title_length > 60:
                self.recommendations.append("🔧 Titre trop long (>60 caractères) - Réduire à 50-60 caractères")
        else:
            self.recommendations.append("❌ Ajouter un titre (title tag)")
        
        # Meta description (5 points)
        meta_desc = self.soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            score += 5
            desc_length = len(meta_desc.get('content'))
            if 150 <= desc_length <= 160:
                score += 2  # Bonus pour longueur optimale
            elif desc_length > 160:
                self.recommendations.append("🔧 Meta description trop longue (>160 caractères)")
        else:
            self.recommendations.append("❌ Ajouter une meta description")
        
        # Meta keywords (2 points)
        meta_keywords = self.soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords and meta_keywords.get('content'):
            score += 2
        
        # Canonical link (3 points)
        canonical = self.soup.find('link', attrs={'rel': 'canonical'})
        if canonical:
            score += 3
        else:
            self.recommendations.append("🔧 Ajouter un lien canonical")
        
        # Open Graph tags (3 points)
        og_tags = self.soup.find_all('meta', attrs={'property': re.compile(r'^og:')})
        if len(og_tags) >= 3:
            score += 3
        elif len(og_tags) > 0:
            score += 1
            self.recommendations.append("🔧 Compléter les tags Open Graph (title, description, image, url)")
        
        # Viewport (3 points)
        viewport = self.soup.find('meta', attrs={'name': 'viewport'})
        if viewport:
            score += 3
        
        # Schema markup (2 points)
        schema_script = self.soup.find('script', attrs={'type': 'application/ld+json'})
        if schema_script:
            score += 2
        else:
            self.recommendations.append("🔧 Ajouter Schema Markup JSON-LD")
        
        return min(score, 25)
    
    def analyze_content_structure(self) -> int:
        """Analyser la structure du contenu (20 points max)"""
        score = 0
        
        # H1 tag (5 points)
        h1_tags = self.soup.find_all('h1')
        if len(h1_tags) == 1:
            score += 5
        elif len(h1_tags) > 1:
            score += 2
            self.recommendations.append("⚠️ Plusieurs H1 détectés - Utiliser un seul H1 par page")
        else:
            self.recommendations.append("❌ Ajouter un titre H1")
        
        # Structure des headings (5 points)
        h2_tags = self.soup.find_all('h2')
        h3_tags = self.soup.find_all('h3')
        
        if len(h2_tags) >= 3:
            score += 3
        elif len(h2_tags) >= 1:
            score += 1
        
        if len(h3_tags) >= 2:
            score += 2
        elif len(h3_tags) >= 1:
            score += 1
        
        if len(h2_tags) == 0:
            self.recommendations.append("🔧 Ajouter des titres H2 pour structurer le contenu")
        
        # Longueur du contenu (5 points)
        text_content = self.soup.get_text()
        word_count = len(text_content.split())
        
        if word_count >= 1000:
            score += 5
        elif word_count >= 500:
            score += 3
        elif word_count >= 300:
            score += 1
        else:
            self.recommendations.append(f"🔧 Contenu trop court ({word_count} mots) - Viser 1000+ mots")
        
        # Navigation/Table des matières (3 points)
        nav_elements = self.soup.find_all(['nav', 'div'], class_=re.compile(r'(nav|toc|table-of-contents)'))
        if nav_elements:
            score += 3
        else:
            self.recommendations.append("🔧 Ajouter une navigation ou table des matières")
        
        # Listes et structure (2 points)
        lists = self.soup.find_all(['ul', 'ol'])
        if len(lists) >= 2:
            score += 2
        elif len(lists) >= 1:
            score += 1
        
        return min(score, 20)
    
    def analyze_keyword_optimization(self) -> int:
        """Analyser l'optimisation des mots-clés (15 points max)"""
        score = 0
        
        try:
            primary_keywords = [kw.get('keyword', '') for kw in self.json_data.get('keyword_research', {}).get('primary_keywords', [])[:3]]
            
            if not primary_keywords:
                self.recommendations.append("❌ Aucun mot-clé primaire trouvé dans les données JSON")
                return 0
            
            text_content = self.soup.get_text().lower()
            title_text = (self.soup.find('title').text if self.soup.find('title') else '').lower()
            meta_desc = self.soup.find('meta', attrs={'name': 'description'})
            meta_desc_text = (meta_desc.get('content') if meta_desc else '').lower()
            
            # Mots-clés dans le titre (5 points)
            keywords_in_title = sum(1 for kw in primary_keywords if kw.lower() in title_text)
            if keywords_in_title >= 2:
                score += 5
            elif keywords_in_title >= 1:
                score += 3
            else:
                self.recommendations.append("🔧 Inclure des mots-clés primaires dans le titre")
            
            # Mots-clés dans meta description (3 points)
            keywords_in_meta = sum(1 for kw in primary_keywords if kw.lower() in meta_desc_text)
            if keywords_in_meta >= 2:
                score += 3
            elif keywords_in_meta >= 1:
                score += 2
            else:
                self.recommendations.append("🔧 Inclure des mots-clés dans la meta description")
            
            # Densité des mots-clés dans le contenu (4 points)
            total_words = len(text_content.split())
            if total_words > 0:
                keyword_density = sum(text_content.count(kw.lower()) for kw in primary_keywords) / total_words * 100
                
                if 1.0 <= keyword_density <= 3.0:
                    score += 4
                elif 0.5 <= keyword_density <= 4.0:
                    score += 2
                elif keyword_density > 0:
                    score += 1
                    if keyword_density > 4.0:
                        self.recommendations.append(f"⚠️ Densité de mots-clés trop élevée ({keyword_density:.1f}%) - Viser 1-3%")
                else:
                    self.recommendations.append("🔧 Intégrer plus naturellement les mots-clés dans le contenu")
            
            # Mots-clés dans les headings (3 points)
            all_headings = self.soup.find_all(['h1', 'h2', 'h3', 'h4'])
            headings_text = ' '.join([h.get_text().lower() for h in all_headings])
            keywords_in_headings = sum(1 for kw in primary_keywords if kw.lower() in headings_text)
            
            if keywords_in_headings >= 3:
                score += 3
            elif keywords_in_headings >= 1:
                score += 2
            else:
                self.recommendations.append("🔧 Inclure des mots-clés dans les titres (H1, H2, H3)")
                
        except Exception as e:
            self.recommendations.append(f"❌ Erreur analyse mots-clés: {e}")
        
        return min(score, 15)
    
    def analyze_technical_seo(self) -> int:
        """Analyser les aspects techniques SEO (20 points max)"""
        score = 0
        
        # HTML5 sémantique (5 points)
        semantic_tags = self.soup.find_all(['header', 'main', 'section', 'article', 'aside', 'footer', 'nav'])
        if len(semantic_tags) >= 4:
            score += 5
        elif len(semantic_tags) >= 2:
            score += 3
        elif len(semantic_tags) >= 1:
            score += 1
        else:
            self.recommendations.append("🔧 Utiliser plus de balises HTML5 sémantiques (header, main, section)")
        
        # Optimisation mobile (5 points)
        has_viewport = bool(self.soup.find('meta', attrs={'name': 'viewport'}))
        responsive_css = 'media' in self.html_content or '@media' in self.html_content
        
        if has_viewport and responsive_css:
            score += 5
        elif has_viewport or responsive_css:
            score += 3
        else:
            self.recommendations.append("🔧 Ajouter meta viewport et CSS responsive")
        
        # Optimisation images (3 points)
        images = self.soup.find_all('img')
        images_with_alt = [img for img in images if img.get('alt')]
        
        if len(images) == 0:
            score += 1  # Pas d'images à optimiser
        elif len(images_with_alt) == len(images):
            score += 3
        elif len(images_with_alt) > len(images) / 2:
            score += 2
        else:
            self.recommendations.append(f"🔧 Ajouter alt text à {len(images) - len(images_with_alt)}/{len(images)} images")
        
        # Liens internes (3 points)
        internal_links = self.soup.find_all('a', href=re.compile(r'^(/|#|\./)'))
        if len(internal_links) >= 5:
            score += 3
        elif len(internal_links) >= 3:
            score += 2
        elif len(internal_links) >= 1:
            score += 1
        else:
            self.recommendations.append("🔧 Ajouter des liens internes vers d'autres pages")
        
        # Performance (2 points)
        css_inline = '<style>' in self.html_content
        js_inline = '<script>' in self.html_content
        
        if css_inline:
            score += 1
        if js_inline:
            score += 1
        
        # Accessibilité (2 points)
        has_lang = bool(self.soup.find('html', attrs={'lang': True}))
        focus_styles = ':focus' in self.html_content
        
        if has_lang:
            score += 1
        if focus_styles:
            score += 1
        else:
            self.recommendations.append("🔧 Ajouter des styles :focus pour l'accessibilité")
        
        return min(score, 20)
    
    def analyze_user_experience(self) -> int:
        """Analyser l'expérience utilisateur (10 points max)"""
        score = 0
        
        # Temps de lecture estimé (2 points)
        text_content = self.soup.get_text()
        word_count = len(text_content.split())
        reading_time = max(1, round(word_count / 200))
        
        if 3 <= reading_time <= 10:
            score += 2
        elif reading_time <= 15:
            score += 1
        
        # CTA (Call to Action) (3 points)
        cta_elements = self.soup.find_all(['a', 'button'], class_=re.compile(r'(cta|button|btn)'))
        cta_elements += self.soup.find_all(['a', 'button'], string=re.compile(r'(s\'abonner|inscription|télécharger|contact)', re.I))
        
        if len(cta_elements) >= 2:
            score += 3
        elif len(cta_elements) >= 1:
            score += 2
        else:
            self.recommendations.append("🔧 Ajouter des Call-to-Action clairs")
        
        # Structure lisible (3 points)
        paragraphs = self.soup.find_all('p')
        avg_p_length = sum(len(p.get_text().split()) for p in paragraphs) / max(1, len(paragraphs))
        
        if 15 <= avg_p_length <= 30:
            score += 3
        elif 10 <= avg_p_length <= 50:
            score += 2
        elif avg_p_length <= 100:
            score += 1
        else:
            self.recommendations.append("🔧 Raccourcir les paragraphes (15-30 mots idéal)")
        
        # Breadcrumb navigation (2 points)
        breadcrumb = self.soup.find_all(['nav', 'div'], class_=re.compile(r'breadcrumb'))
        if breadcrumb:
            score += 2
        else:
            self.recommendations.append("🔧 Ajouter une navigation breadcrumb")
        
        return min(score, 10)
    
    def analyze_content_freshness(self) -> int:
        """Analyser la fraîcheur du contenu (10 points max)"""
        try:
            freshness_data = self.json_data.get('seo_audit', {}).get('freshness_metrics', {})
            freshness_score = freshness_data.get('data_freshness_score', 0)
            
            if freshness_score >= 95:
                return 10
            elif freshness_score >= 85:
                return 8
            elif freshness_score >= 70:
                return 6
            elif freshness_score >= 50:
                return 4
            elif freshness_score > 0:
                return 2
            else:
                self.recommendations.append("🔧 Utiliser des sources plus récentes")
                return 0
                
        except:
            self.recommendations.append("❌ Impossible d'analyser la fraîcheur des données")
            return 0
    
    def calculate_total_score(self) -> dict:
        """Calculer le score SEO total"""
        
        # Analyser chaque catégorie
        self.scores['meta_tags'] = self.analyze_meta_tags()
        self.scores['content_structure'] = self.analyze_content_structure()
        self.scores['keyword_optimization'] = self.analyze_keyword_optimization()
        self.scores['technical_seo'] = self.analyze_technical_seo()
        self.scores['user_experience'] = self.analyze_user_experience()
        self.scores['content_freshness'] = self.analyze_content_freshness()
        
        # Score total
        total_score = sum(self.scores.values())
        max_score = 100
        percentage = (total_score / max_score) * 100
        
        return {
            'total_score': total_score,
            'max_score': max_score,
            'percentage': percentage,
            'scores_breakdown': self.scores,
            'recommendations': self.recommendations
        }
    
    def get_grade(self, percentage: float) -> str:
        """Obtenir la note SEO"""
        if percentage >= 90:
            return "A+"
        elif percentage >= 80:
            return "A"
        elif percentage >= 70:
            return "B+"
        elif percentage >= 65:
            return "B"
        elif percentage >= 50:
            return "C"
        elif percentage >= 30:
            return "D"
        else:
            return "F"
    
    def generate_report(self) -> str:
        """Générer le rapport SEO complet"""
        results = self.calculate_total_score()
        
        report = f"""
🎯 RAPPORT D'ANALYSE SEO
{'=' * 60}

📊 SCORE GLOBAL: {results['percentage']:.1f}% ({results['total_score']}/{results['max_score']} points)
🏆 GRADE SEO: {self.get_grade(results['percentage'])}

📋 DÉTAIL PAR CATÉGORIE:
{'-' * 40}
🏷️  Meta Tags: {results['scores_breakdown']['meta_tags']}/25 points
📄 Structure Contenu: {results['scores_breakdown']['content_structure']}/20 points
🎯 Optimisation Mots-clés: {results['scores_breakdown']['keyword_optimization']}/15 points
⚙️  SEO Technique: {results['scores_breakdown']['technical_seo']}/20 points
👤 Expérience Utilisateur: {results['scores_breakdown']['user_experience']}/10 points
🔥 Fraîcheur Contenu: {results['scores_breakdown']['content_freshness']}/10 points

🎯 OBJECTIF: 65-80% pour un bon SEO
{'✅ OBJECTIF ATTEINT!' if results['percentage'] >= 65 else '⚠️ AMÉLIORATIONS NÉCESSAIRES'}

💡 RECOMMANDATIONS D'AMÉLIORATION:
{'-' * 40}"""
        
        if not results['recommendations']:
            report += "\n🎉 Aucune amélioration nécessaire - Excellente optimisation SEO!"
        else:
            for i, rec in enumerate(results['recommendations'], 1):
                report += f"\n{i:2d}. {rec}"
        
        # Conseils selon le score
        if results['percentage'] < 65:
            report += f"""

🔧 PLAN D'ACTION PRIORITAIRE:
{'-' * 30}
1. Corriger les recommandations marquées ❌ (critiques)
2. Appliquer les améliorations 🔧 (importantes)  
3. Optimiser les éléments ⚠️ (améliorations)
4. Retester pour vérifier l'amélioration du score"""
        
        elif 65 <= results['percentage'] < 80:
            report += f"""

🎯 VOUS ÊTES DANS LA CIBLE! (65-80%)
{'-' * 35}
✅ Votre page est bien optimisée pour le SEO
💡 Appliquez les recommandations pour atteindre 80%+
🚀 Votre contenu peut bien ranker sur Google"""
        
        else:
            report += f"""

🏆 EXCELLENT TRAVAIL! (80%+)
{'-' * 25}
🎉 Optimisation SEO exceptionnelle
🚀 Votre page a toutes les chances de bien ranker
💯 Continuez à monitorer et maintenir ce niveau"""
        
        return report

def main():
    """Analyser le score SEO de la page générée"""
    
    html_file = "seo_optimized_article.html"
    json_file = "seo_article_output.json"
    
    # Vérifier que les fichiers existent
    if not os.path.exists(html_file):
        print(f"❌ Fichier {html_file} introuvable!")
        print("💡 Générez d'abord la page HTML avec: python html_generator.py")
        return
    
    if not os.path.exists(json_file):
        print(f"❌ Fichier {json_file} introuvable!")
        print("💡 Générez d'abord l'article avec: python main.py")
        return
    
    print("🔍 ANALYSE SEO EN COURS...")
    print("=" * 50)
    
    try:
        # Créer l'analyseur
        analyzer = SEOScoreAnalyzer(html_file, json_file)
        
        # Générer le rapport
        report = analyzer.generate_report()
        
        # Afficher le rapport
        print(report)
        
        # Sauvegarder le rapport
        with open("seo_analysis_report.txt", "w", encoding="utf-8") as f:
            f.write(report)
        
        print(f"\n📄 Rapport sauvegardé: seo_analysis_report.txt")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
