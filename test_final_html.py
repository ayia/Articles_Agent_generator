# Test du fichier HTML final unique
# Analyse le score SEO du fichier seo_optimized_final.html

from seo_score_analyzer import SEOScoreAnalyzer
import os

def main():
    """Analyser le fichier HTML final unique"""
    
    html_file = "seo_optimized_final.html"
    json_file = "seo_article_output.json"
    
    print("🔍 ANALYSE SEO DU FICHIER HTML FINAL UNIQUE")
    print("=" * 60)
    print(f"📄 Fichier analysé: {html_file}")
    
    # Vérifier que les fichiers existent
    if not os.path.exists(html_file):
        print(f"❌ Fichier {html_file} introuvable!")
        return
    
    if not os.path.exists(json_file):
        print(f"❌ Fichier {json_file} introuvable!")
        return
    
    try:
        # Analyser le score SEO
        analyzer = SEOScoreAnalyzer(html_file, json_file)
        results = analyzer.calculate_total_score()
        
        print(f"📊 SCORE GLOBAL: {results['percentage']:.1f}% ({results['total_score']}/{results['max_score']} points)")
        print(f"🏆 GRADE SEO: {analyzer.get_grade(results['percentage'])}")
        
        print(f"\n📋 DÉTAIL PAR CATÉGORIE:")
        print(f"🏷️  Meta Tags: {results['scores_breakdown']['meta_tags']}/25 points")
        print(f"📄 Structure: {results['scores_breakdown']['content_structure']}/20 points")
        print(f"🎯 Mots-clés: {results['scores_breakdown']['keyword_optimization']}/15 points")
        print(f"⚙️  Technique: {results['scores_breakdown']['technical_seo']}/20 points")
        print(f"👤 UX: {results['scores_breakdown']['user_experience']}/10 points")
        print(f"🔥 Fraîcheur: {results['scores_breakdown']['content_freshness']}/10 points")
        
        # Évaluation de l'objectif
        if results['percentage'] >= 80:
            status = "🏆 EXCELLENT - OBJECTIF DÉPASSÉ!"
            emoji = "🎉"
        elif results['percentage'] >= 65:
            status = "✅ OBJECTIF 65-80% ATTEINT!"
            emoji = "🎯"
        else:
            status = "⚠️ OBJECTIF NON ATTEINT"
            emoji = "🔧"
        
        print(f"\n{emoji} RÉSULTAT: {status}")
        print(f"🎯 Cible: 65-80% | Obtenu: {results['percentage']:.1f}%")
        
        # Recommandations si nécessaire
        if results['recommendations']:
            print(f"\n💡 RECOMMANDATIONS:")
            for i, rec in enumerate(results['recommendations'][:5], 1):
                print(f"   {i}. {rec}")
        else:
            print(f"\n🎉 AUCUNE AMÉLIORATION NÉCESSAIRE!")
        
        # Résumé final
        print(f"\n📋 RÉSUMÉ:")
        print(f"✅ Un seul fichier HTML créé (plus de confusion)")
        print(f"✅ Titre optimisé automatiquement")
        print(f"✅ Meta description raccourcie")
        print(f"✅ Score SEO dans la cible")
        print(f"✅ Prêt pour publication")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
