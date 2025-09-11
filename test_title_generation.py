# Test de génération de titre SEO optimisé
# Ce script démontre la différence entre le headline original et le titre généré

import json
import os
from datetime import datetime

def analyze_title_optimization():
    """Analyser l'optimisation du titre généré vs headline original"""
    
    # Récupérer le headline original du script
    headline_original = "Trump reportedly asks EU to levy 100% tariffs on India and China; Ozempic maker Novo to cut 9,000 jobs – business live."
    
    print("🎯 ANALYSE : TITRE GÉNÉRÉ VS HEADLINE ORIGINAL")
    print("=" * 60)
    
    print(f"📰 HEADLINE ORIGINAL (Votre input):")
    print(f"   \"{headline_original}\"")
    print(f"   📏 Longueur: {len(headline_original)} caractères")
    print(f"   ❌ Problème: Trop long pour SEO (>60 caractères)")
    print(f"   ❌ Problème: Format journalistique, pas web/SEO")
    print()
    
    # Vérifier si un article a été généré
    if os.path.exists('seo_article_output.json'):
        try:
            with open('seo_article_output.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            article = data.get('article', {})
            titre_genere = article.get('title', '')
            
            print(f"🎯 TITRE GÉNÉRÉ (Par l'IA SEO):")
            print(f"   \"{titre_genere}\"")
            print(f"   📏 Longueur: {len(titre_genere)} caractères")
            
            # Analyser l'optimisation
            if len(titre_genere) <= 60:
                print(f"   ✅ Longueur optimale pour SEO (<60 caractères)")
            else:
                print(f"   ⚠️ Encore trop long - Besoin d'optimisation")
            
            # Vérifier les mots-clés
            keywords = data.get('keyword_research', {}).get('primary_keywords', [])
            if keywords:
                print(f"\n🔍 ANALYSE MOTS-CLÉS DANS LE TITRE:")
                for i, kw_data in enumerate(keywords[:5], 1):
                    keyword = kw_data.get('keyword', '')
                    if keyword.lower() in titre_genere.lower():
                        print(f"   ✅ {i}. \"{keyword}\" → Présent dans le titre")
                    else:
                        print(f"   ❌ {i}. \"{keyword}\" → Absent du titre")
            
            print(f"\n📊 COMPARAISON:")
            print(f"   Original: {len(headline_original)} chars (❌ trop long)")
            print(f"   Généré:   {len(titre_genere)} chars ({'✅ optimal' if len(titre_genere) <= 60 else '⚠️ à optimiser'})")
            
            # Recommandations
            print(f"\n💡 RECOMMANDATIONS:")
            if len(titre_genere) > 60:
                print(f"   🔧 Raccourcir le titre généré à 50-60 caractères")
                
                # Proposer une version optimisée
                mots_cles_principaux = [kw.get('keyword', '') for kw in keywords[:2]]
                if mots_cles_principaux:
                    titre_optimise = f"{mots_cles_principaux[0]}: UE Face aux Tarifs 100% Chine-Inde"
                    print(f"   💡 Suggestion: \"{titre_optimise}\" ({len(titre_optimise)} chars)")
            else:
                print(f"   ✅ Titre déjà optimisé pour le SEO")
                
        except Exception as e:
            print(f"❌ Erreur lecture JSON: {e}")
    else:
        print(f"⚠️ Aucun article généré trouvé")
        print(f"💡 Génération d'exemples de titres optimisés basés sur le headline:")
        
        # Générer des exemples de titres optimisés
        exemples_titres = [
            "Tarifs UE 100%: Trump Presse l'Europe vs Chine-Inde",
            "Trump Pousse UE: Tarifs 100% Chine Inde + Novo Layoffs",
            "UE Tarifs 100%: Pression Trump + Novo Nordisk 9000 Jobs", 
            "Trump Tarifs: Europe vs Chine-Inde + Ozempic Crisis",
            "Tarifs 100% UE-Chine: Trump Strategy + Pharma Layoffs"
        ]
        
        print(f"\n🎯 EXEMPLES DE TITRES SEO OPTIMISÉS:")
        for i, titre in enumerate(exemples_titres, 1):
            print(f"   {i}. \"{titre}\" ({len(titre)} chars)")
        
        print(f"\n✅ Ces titres sont:")
        print(f"   • Courts (50-60 caractères)")
        print(f"   • Riches en mots-clés")  
        print(f"   • Accorcheurs pour le web")
        print(f"   • Optimisés pour le SEO")

def show_seo_title_best_practices():
    """Afficher les bonnes pratiques pour les titres SEO"""
    
    print(f"\n📚 BONNES PRATIQUES TITRES SEO:")
    print("=" * 40)
    
    practices = [
        ("📏 Longueur", "50-60 caractères (max 65)", "Pour affichage complet Google"),
        ("🎯 Mots-clés", "1-2 mots-clés primaires", "Inclure au début si possible"),
        ("🔥 Accroche", "Émotions + urgence", "Améliorer CTR (taux de clic)"),
        ("🌐 Format", "Web-friendly", "Éviter format journalistique"),
        ("💡 Clarté", "Comprendre en 2 secondes", "Utilisateur doit saisir le sujet"),
        ("📊 Données", "Chiffres si pertinents", "\"9000 jobs\", \"100%\", dates"),
        ("🎨 Ponctuation", "Utilisez \":\" et \"|\"", "Séparer concepts clairement")
    ]
    
    for category, rule, explanation in practices:
        print(f"{category} {rule:<25} - {explanation}")
    
    print(f"\n❌ ERREURS À ÉVITER:")
    errors = [
        "• Titres trop longs (>65 caractères)",
        "• Répétition exacte du headline",
        "• Pas de mots-clés dans le titre",
        "• Format trop journalistique",
        "• Manque d'émotion/accroche",
        "• Titre pas clair ou confus"
    ]
    
    for error in errors:
        print(f"  {error}")

def main():
    """Tester la génération de titre optimisé"""
    
    # Analyser le titre actuel
    analyze_title_optimization()
    
    # Montrer les bonnes pratiques
    show_seo_title_best_practices()
    
    print(f"\n🚀 PROCHAINES ÉTAPES:")
    print(f"1. 🔄 Régénérer un article avec: python main.py")
    print(f"2. 🔍 Vérifier que le nouveau titre est différent du headline")
    print(f"3. 📊 Analyser avec: python seo_score_analyzer.py")
    print(f"4. 🎯 Le titre doit être 50-60 caractères + mots-clés")
    
    print(f"\n💡 MODIFICATION APPLIQUÉE:")
    print(f"✅ L'agent rédacteur va maintenant CRÉER un titre SEO")
    print(f"✅ Plus de copie du headline original")
    print(f"✅ Utilisation des mots-clés trouvés par recherche")
    print(f"✅ Respect des bonnes pratiques SEO (50-60 chars)")

if __name__ == "__main__":
    main()
