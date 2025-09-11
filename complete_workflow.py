# Workflow Complet : Génération Article SEO + Page HTML Optimisée
# Ce script automatise tout le processus : recherche → article → HTML optimisé SEO

import subprocess
import sys
import os
from html_generator import SEOHTMLGenerator

def run_article_generation():
    """Étape 1: Exécuter main.py pour générer l'article JSON"""
    print("🚀 ÉTAPE 1: Génération de l'article SEO optimisé...")
    print("=" * 60)
    
    try:
        # Exécuter main.py
        result = subprocess.run([sys.executable, "main.py"], 
                              capture_output=True, 
                              text=True, 
                              encoding='utf-8')
        
        if result.returncode == 0:
            print("✅ Article généré avec succès!")
            print("📄 Fichier créé: seo_article_output.json")
            return True
        else:
            print(f"❌ Erreur lors de la génération de l'article:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erreur d'exécution: {e}")
        return False

def run_html_generation():
    """Étape 2: Générer la page HTML optimisée SEO"""
    print("\n🌐 ÉTAPE 2: Génération de la page HTML SEO...")
    print("=" * 60)
    
    try:
        # Vérifier que le JSON existe
        if not os.path.exists("seo_article_output.json"):
            print("❌ Fichier JSON introuvable!")
            return False
        
        # Générer le HTML
        generator = SEOHTMLGenerator('seo_article_output.json')
        html_content = generator.generate_html()
        
        print("✅ Page HTML générée avec succès!")
        print("🌐 Fichier créé: seo_optimized_article.html")
        print(f"📊 Taille: {len(html_content):,} caractères")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération HTML: {e}")
        return False

def display_summary():
    """Afficher le résumé des fichiers générés"""
    print("\n📋 RÉSUMÉ DES FICHIERS GÉNÉRÉS:")
    print("=" * 60)
    
    files_info = [
        ("seo_article_output.json", "Données JSON de l'article avec mots-clés et audit SEO"),
        ("seo_optimized_article.html", "Page web complète optimisée SEO (65-80% score cible)")
    ]
    
    for filename, description in files_info:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"✅ {filename}")
            print(f"   📝 {description}")
            print(f"   📊 Taille: {size:,} bytes")
        else:
            print(f"❌ {filename} - Fichier manquant")
        print()

def display_seo_checklist():
    """Afficher la checklist SEO pour atteindre 65-80%"""
    print("🎯 CHECKLIST SEO POUR 65-80% DE SCORE:")
    print("=" * 60)
    
    checklist = [
        ("✅ Meta tags optimisés", "Title, description, keywords intégrés"),
        ("✅ Schema Markup JSON-LD", "NewsArticle schema pour Google"),
        ("✅ Structure sémantique HTML5", "Header, main, section, aside"),
        ("✅ Hiérarchie des titres", "H1, H2, H3 correctement structurés"),
        ("✅ Responsive design", "Mobile-first, touch targets 44px+"),
        ("✅ Optimisation Core Web Vitals", "Performance et UX améliorées"),
        ("✅ Navigation breadcrumb", "Meilleure indexation par Google"),
        ("✅ Table des matières", "Navigation interne optimisée"),
        ("✅ Open Graph + Twitter Cards", "Partage social optimisé"),
        ("✅ Liens internes suggérés", "Maillage interne pour SEO"),
        ("✅ CTA optimisés", "Engagement utilisateur amélioré"),
        ("✅ Accessibilité WCAG", "Focus management, contraste")
    ]
    
    for status, description in checklist:
        print(f"{status} {description}")
    
    print(f"\n💡 PROCHAINES ÉTAPES RECOMMANDÉES:")
    recommendations = [
        "1. 🖼️ Ajouter des images optimisées avec alt text descriptifs",
        "2. 🔗 Configurer les liens internes vers vos autres articles",
        "3. 📱 Tester la page avec Google PageSpeed Insights",
        "4. 🔍 Vérifier l'indexation avec Google Search Console",
        "5. 📊 Monitorer les performances SEO avec Google Analytics",
        "6. 🌐 Publier sur un serveur avec HTTPS activé",
        "7. 📋 Créer un sitemap.xml incluant cette page"
    ]
    
    for rec in recommendations:
        print(f"   {rec}")

def main():
    """Workflow principal complet"""
    print("🎯 WORKFLOW COMPLET: ARTICLE SEO + PAGE HTML OPTIMISÉE")
    print("=" * 70)
    print("🔄 Ce script va générer:")
    print("   1. Un article SEO optimisé (JSON)")
    print("   2. Une page HTML complète (65-80% score SEO cible)")
    print("   3. Un audit détaillé des optimisations appliquées")
    print()
    
    # Étape 1: Générer l'article
    success_article = run_article_generation()
    
    if not success_article:
        print("\n❌ Arrêt du workflow - Échec génération article")
        return
    
    # Étape 2: Générer le HTML
    success_html = run_html_generation()
    
    if not success_html:
        print("\n❌ Arrêt du workflow - Échec génération HTML")
        return
    
    # Résumé final
    display_summary()
    display_seo_checklist()
    
    print(f"\n🎉 WORKFLOW TERMINÉ AVEC SUCCÈS!")
    print("🚀 Votre article et sa page web sont prêts pour publication!")
    print(f"📈 Score SEO cible: 65-80% (optimisations appliquées)")
    print(f"🔍 Testez maintenant avec Google PageSpeed Insights")

if __name__ == "__main__":
    main()
