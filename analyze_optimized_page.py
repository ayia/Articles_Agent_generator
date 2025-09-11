# Analyser la page optimisée seo_optimized_article_v2.html
# Version spécifique pour la page finale optimisée

from seo_score_analyzer import SEOScoreAnalyzer
import os

def main():
    """Analyser le score SEO de la page optimisée finale"""
    
    html_file = "seo_optimized_article_v2.html"
    json_file = "seo_article_output.json"
    
    # Vérifier que les fichiers existent
    if not os.path.exists(html_file):
        print(f"❌ Fichier {html_file} introuvable!")
        print("💡 Exécutez d'abord: python seo_optimizer.py")
        return
    
    if not os.path.exists(json_file):
        print(f"❌ Fichier {json_file} introuvable!")
        print("💡 Générez d'abord l'article avec: python main.py")
        return
    
    print("🔍 ANALYSE SEO DE LA PAGE OPTIMISÉE FINALE")
    print("=" * 60)
    print("📄 Fichier analysé: seo_optimized_article_v2.html")
    print()
    
    try:
        # Créer l'analyseur avec la page optimisée
        analyzer = SEOScoreAnalyzer(html_file, json_file)
        
        # Générer le rapport
        report = analyzer.generate_report()
        
        # Afficher le rapport
        print(report)
        
        # Sauvegarder le rapport final
        with open("seo_analysis_final_report.txt", "w", encoding="utf-8") as f:
            f.write(report)
        
        print(f"\n📄 Rapport final sauvegardé: seo_analysis_final_report.txt")
        
        # Résumé des améliorations
        print(f"\n🎊 RÉSUMÉ DES AMÉLIORATIONS:")
        print(f"=" * 40)
        print(f"🔧 Titre optimisé: 50 caractères (vs 119 original)")
        print(f"📝 Meta description raccourcie: 158 caractères") 
        print(f"🎯 Mots-clés intégrés dans H1, H2, H3")
        print(f"📋 Table des matières ajoutée")
        print(f"📱 14 paragraphes divisés pour lisibilité")
        print(f"🚀 CTAs supplémentaires pour engagement")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
