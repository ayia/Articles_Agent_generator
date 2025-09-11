# Générateur HTML SEO automatique basé sur seo_article_output.json
# Ce script transforme le JSON en page HTML optimisée pour atteindre 65-80% de score SEO

import json
import re
from datetime import datetime
from typing import Dict, Any, List

class SEOHTMLGenerator:
    """Générateur HTML optimisé SEO à partir du JSON CrewAI"""
    
    def __init__(self, json_file_path: str):
        """Charger le fichier JSON généré par CrewAI"""
        with open(json_file_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        # Extraire les données clés
        self.article = self.data.get('article', {})
        self.keywords = self.data.get('keyword_research', {})
        self.seo_suggestions = self.data.get('seo_suggestions', {})
        self.seo_audit = self.data.get('seo_audit', {})
    
    def generate_meta_tags(self) -> str:
        """Générer les meta tags optimisés SEO"""
        primary_keywords = [kw['keyword'] for kw in self.keywords.get('primary_keywords', [])[:3]]
        keywords_string = ', '.join(primary_keywords)
        
        meta_tags = f'''    <!-- Meta Tags SEO Essentiels -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.article.get('title', 'Article')}</title>
    <meta name="description" content="{self.article.get('meta_description', '')}">
    <meta name="keywords" content="{keywords_string}">
    
    <!-- Meta Tags Open Graph (Social Media) -->
    <meta property="og:title" content="{self.article.get('title', '')}">
    <meta property="og:description" content="{self.article.get('meta_description', '')}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://votre-site.com/articles/current-article">
    <meta property="og:image" content="https://votre-site.com/images/article-cover.jpg">
    
    <!-- Meta Tags Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{self.article.get('title', '')}">
    <meta name="twitter:description" content="{self.article.get('meta_description', '')}">
    <meta name="twitter:image" content="https://votre-site.com/images/article-cover.jpg">
    
    <!-- Meta Tags pour SEO -->
    <meta name="author" content="Votre Site">
    <meta name="robots" content="index, follow">
    <meta name="googlebot" content="index, follow">
    <link rel="canonical" href="https://votre-site.com/articles/current-article">'''
        
        return meta_tags
    
    def generate_schema_markup(self) -> str:
        """Générer le Schema Markup JSON-LD pour améliorer le SEO"""
        # Calculer le temps de lecture estimé
        word_count = len(self.article.get('introduction', '').split()) + \
                    sum(len(section.split()) for section in self.article.get('body', [])) + \
                    len(self.article.get('conclusion', '').split())
        reading_time = max(1, round(word_count / 200))  # 200 mots par minute
        
        schema = {
            "@context": "https://schema.org",
            "@type": "NewsArticle",
            "headline": self.article.get('title', ''),
            "description": self.article.get('meta_description', ''),
            "articleBody": self.get_full_article_text(),
            "datePublished": datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00'),
            "dateModified": datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00'),
            "author": {
                "@type": "Person",
                "name": "Expert Business Analyst"
            },
            "publisher": {
                "@type": "Organization",
                "name": "Votre Site Business",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://votre-site.com/logo.png"
                }
            },
            "wordCount": word_count,
            "timeRequired": f"PT{reading_time}M",
            "keywords": [kw['keyword'] for kw in self.keywords.get('primary_keywords', [])[:5]]
        }
        
        return f'''    <script type="application/ld+json">
{json.dumps(schema, indent=8, ensure_ascii=False)}
    </script>'''
    
    def get_full_article_text(self) -> str:
        """Récupérer le texte complet de l'article"""
        intro = self.article.get('introduction', '')
        body_sections = self.article.get('body', [])
        conclusion = self.article.get('conclusion', '')
        
        full_text = intro + ' ' + ' '.join(body_sections) + ' ' + conclusion
        return full_text.strip()
    
    def generate_css(self) -> str:
        """Générer le CSS responsive optimisé pour mobile et SEO"""
        return '''    <style>
        /* CSS Optimisé SEO et Mobile-First */
        :root {
            --primary-color: #2c3e50;
            --secondary-color: #3498db;
            --text-color: #333;
            --bg-color: #ffffff;
            --light-gray: #f8f9fa;
            --border-color: #e9ecef;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background-color: var(--bg-color);
            font-size: 16px; /* Minimum recommandé pour mobile */
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        
        /* Headers optimisés SEO */
        h1 {
            font-size: 2rem;
            font-weight: 700;
            color: var(--primary-color);
            margin-bottom: 1rem;
            line-height: 1.2;
        }
        
        h2 {
            font-size: 1.5rem;
            color: var(--primary-color);
            margin: 2rem 0 1rem 0;
            border-left: 4px solid var(--secondary-color);
            padding-left: 1rem;
        }
        
        h3 {
            font-size: 1.25rem;
            color: var(--primary-color);
            margin: 1.5rem 0 0.75rem 0;
        }
        
        /* Paragraphes optimisés lisibilité */
        p {
            margin-bottom: 1.25rem;
            text-align: justify;
        }
        
        /* Meta description visuelle */
        .article-meta {
            background-color: var(--light-gray);
            padding: 1rem;
            border-radius: 8px;
            margin: 1.5rem 0;
            font-style: italic;
            border-left: 4px solid var(--secondary-color);
        }
        
        /* Navigation breadcrumb pour SEO */
        .breadcrumb {
            margin-bottom: 1.5rem;
            font-size: 0.9rem;
            color: #666;
        }
        
        .breadcrumb a {
            color: var(--secondary-color);
            text-decoration: none;
        }
        
        .breadcrumb a:hover {
            text-decoration: underline;
        }
        
        /* Stats de l'article */
        .article-stats {
            display: flex;
            justify-content: space-between;
            background-color: var(--light-gray);
            padding: 1rem;
            border-radius: 8px;
            margin: 1.5rem 0;
            font-size: 0.9rem;
            color: #666;
        }
        
        /* Boutons CTA optimisés touch */
        .cta-button {
            background-color: var(--secondary-color);
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            cursor: pointer;
            margin: 1rem 0;
            min-height: 44px; /* Minimum touch target */
            display: inline-block;
            text-decoration: none;
            text-align: center;
        }
        
        .cta-button:hover {
            background-color: #2980b9;
        }
        
        /* SEO-friendly links */
        a {
            color: var(--secondary-color);
            text-decoration: none;
        }
        
        a:hover {
            text-decoration: underline;
        }
        
        /* Table of Contents pour longues articles */
        .table-of-contents {
            background-color: var(--light-gray);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1.5rem;
            margin: 2rem 0;
        }
        
        .table-of-contents h3 {
            margin-top: 0;
            color: var(--primary-color);
        }
        
        .table-of-contents ul {
            list-style: none;
            padding-left: 0;
        }
        
        .table-of-contents li {
            margin: 0.5rem 0;
            padding-left: 1rem;
        }
        
        .table-of-contents a {
            color: var(--text-color);
        }
        
        /* Mobile Responsive */
        @media (max-width: 768px) {
            .container {
                padding: 15px;
            }
            
            h1 {
                font-size: 1.75rem;
            }
            
            h2 {
                font-size: 1.35rem;
            }
            
            .article-stats {
                flex-direction: column;
                gap: 0.5rem;
            }
        }
        
        /* Optimisations performance */
        img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
        }
        
        /* Focus pour accessibilité */
        *:focus {
            outline: 2px solid var(--secondary-color);
            outline-offset: 2px;
        }
    </style>'''
    
    def generate_table_of_contents(self) -> str:
        """Générer une table des matières pour améliorer l'UX et SEO"""
        body_sections = self.article.get('body', [])
        toc_items = []
        
        for i, section in enumerate(body_sections):
            # Extraire les titres H2/H3 du contenu
            if section.strip().startswith('H2:') or section.strip().startswith('H3:'):
                # Nettoyer le titre
                title = re.sub(r'^H[23]:\s*', '', section.strip())
                anchor = f"section-{i+1}"
                toc_items.append(f'<li><a href="#{anchor}">{title}</a></li>')
        
        if not toc_items:
            return ""
        
        return f'''        <nav class="table-of-contents">
            <h3>📋 Sommaire de l'Article</h3>
            <ul>
                {''.join(toc_items)}
            </ul>
        </nav>'''
    
    def format_body_sections(self) -> str:
        """Formater les sections du corps avec les bonnes balises HTML"""
        body_sections = self.article.get('body', [])
        formatted_sections = []
        
        for i, section in enumerate(body_sections):
            section = section.strip()
            anchor = f"section-{i+1}"
            
            if section.startswith('H2:'):
                # Titre H2
                title = re.sub(r'^H2:\s*', '', section)
                formatted_sections.append(f'        <h2 id="{anchor}">{title}</h2>')
            elif section.startswith('H3:'):
                # Titre H3
                title = re.sub(r'^H3:\s*', '', section)
                formatted_sections.append(f'        <h3 id="{anchor}">{title}</h3>')
            else:
                # Contenu paragraphe
                formatted_sections.append(f'        <p>{section}</p>')
        
        return '\n'.join(formatted_sections)
    
    def generate_article_stats(self) -> str:
        """Générer les statistiques de l'article pour l'engagement"""
        # Calculer les stats depuis le JSON
        word_count = len(self.get_full_article_text().split())
        reading_time = max(1, round(word_count / 200))
        
        freshness_score = self.seo_audit.get('freshness_metrics', {}).get('data_freshness_score', 'N/A')
        seo_score = self.seo_audit.get('overall_seo_score', 'N/A')
        
        return f'''        <div class="article-stats">
            <span>📖 {word_count} mots</span>
            <span>⏱️ {reading_time} min de lecture</span>
            <span>🔥 Fraîcheur: {freshness_score}/100</span>
            <span>🎯 Score SEO: {seo_score}/100</span>
        </div>'''
    
    def generate_html(self, output_file: str = "seo_optimized_article.html") -> str:
        """Générer le HTML complet optimisé SEO"""
        
        html_template = f'''<!DOCTYPE html>
<html lang="fr">
<head>
{self.generate_meta_tags()}
    
{self.generate_schema_markup()}
    
{self.generate_css()}
</head>
<body>
    <div class="container">
        <!-- Breadcrumb Navigation -->
        <nav class="breadcrumb">
            <a href="/">Accueil</a> &gt; 
            <a href="/actualites">Actualités Business</a> &gt; 
            <span>Article Actuel</span>
        </nav>
        
        <!-- Article Header -->
        <header>
            <h1>{self.article.get('title', '')}</h1>
            <div class="article-meta">
                {self.article.get('meta_description', '')}
            </div>
{self.generate_article_stats()}
        </header>
        
        <!-- Table of Contents -->
{self.generate_table_of_contents()}
        
        <!-- Article Content -->
        <main>
            <!-- Introduction -->
            <section class="introduction">
                <p><strong>{self.article.get('introduction', '')}</strong></p>
            </section>
            
            <!-- Article Body -->
            <section class="article-body">
{self.format_body_sections()}
            </section>
            
            <!-- Conclusion -->
            <section class="conclusion">
                <h2>Conclusion</h2>
                <p>{self.article.get('conclusion', '')}</p>
            </section>
        </main>
        
        <!-- Call to Action -->
        <section class="cta-section">
            <h3>📬 Restez Informé des Dernières Actualités Business</h3>
            <p>Recevez nos analyses exclusives directement dans votre boîte mail.</p>
            <a href="/newsletter" class="cta-button">S'abonner à la Newsletter</a>
        </section>
        
        <!-- Related Articles Section -->
        <aside class="related-articles">
            <h3>📰 Articles Connexes</h3>
            <ul>
                <li><a href="/articles/trade-wars-impact">Impact des Guerres Commerciales sur l'Économie</a></li>
                <li><a href="/articles/pharmaceutical-trends">Tendances du Secteur Pharmaceutique 2025</a></li>
                <li><a href="/articles/eu-trade-policy">Politique Commerciale de l'UE : Enjeux et Perspectives</a></li>
            </ul>
        </aside>
    </div>
    
    <!-- JavaScript pour améliorer l'UX (optionnel) -->
    <script>
        // Smooth scrolling pour les liens d'ancrage
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{
                        behavior: 'smooth',
                        block: 'start'
                    }});
                }}
            }});
        }});
        
        // Améliorer les métriques Core Web Vitals
        if ('loading' in HTMLImageElement.prototype) {{
            const images = document.querySelectorAll('img[loading="lazy"]');
            images.forEach(img => {{
                img.src = img.dataset.src;
            }});
        }}
    </script>
</body>
</html>'''
        
        # Sauvegarder le fichier HTML
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_template)
        
        return html_template

# Script principal pour générer le HTML
def main():
    print("🚀 Génération HTML SEO Optimisée")
    print("=" * 50)
    
    try:
        # Créer le générateur
        generator = SEOHTMLGenerator('seo_article_output.json')
        
        # Générer le HTML
        html_content = generator.generate_html()
        
        print("✅ Fichier HTML généré: seo_optimized_article.html")
        print(f"📊 Longueur du contenu: {len(html_content)} caractères")
        
        # Afficher les optimisations SEO appliquées
        print("\n📈 OPTIMISATIONS SEO APPLIQUÉES:")
        print("✅ Meta tags complets (title, description, keywords)")
        print("✅ Schema Markup JSON-LD (NewsArticle)")
        print("✅ Structure sémantique HTML5 (header, main, section, aside)")
        print("✅ Headings hiérarchiques (H1, H2, H3)")
        print("✅ Responsive design mobile-first")
        print("✅ Optimisation Core Web Vitals")
        print("✅ Table des matières pour navigation")
        print("✅ Breadcrumb navigation")
        print("✅ Open Graph et Twitter Card")
        print("✅ Liens internes et CTA optimisés")
        print("✅ Accessibilité (focus, touch targets 44px+)")
        
        print(f"\n🎯 SCORE SEO CIBLE: 65-80%")
        print("💡 Prochaines étapes:")
        print("   1. Publier le fichier HTML sur votre serveur")
        print("   2. Ajouter des images optimisées avec alt text")
        print("   3. Configurer les liens internes vers d'autres articles")
        print("   4. Tester avec Google PageSpeed Insights")
        print("   5. Vérifier avec Google Search Console")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    main()
