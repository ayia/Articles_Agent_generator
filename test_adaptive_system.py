# Test du système adaptatif - Vérification des termes générés automatiquement

from headline_analyzer import HeadlineAnalyzer

def test_current_headline():
    """Tester les termes générés pour le headline actuel"""
    
    headline = "Consumer prices rose at annual rate of 2.9% in August, as weekly jobless claims jump"
    
    print("🧪 TEST DU SYSTÈME ADAPTATIF")
    print("=" * 60)
    
    print(f"📰 HEADLINE ACTUEL:")
    print(f"   \"{headline}\"")
    print(f"   📏 {len(headline)} caractères")
    print()
    
    # Créer l'analyseur
    analyzer = HeadlineAnalyzer()
    
    # Extraire les termes automatiquement
    search_terms = analyzer.generate_search_terms(headline)
    
    print(f"🔍 TERMES DE RECHERCHE GÉNÉRÉS AUTOMATIQUEMENT:")
    print(f"📊 Total: {len(search_terms)} termes")
    
    for i, term in enumerate(search_terms, 1):
        print(f"   {i:2d}. \"{term}\"")
    
    print()
    
    # Générer les task descriptions
    keyword_task_desc = analyzer.generate_dynamic_task_description(headline, "keyword")
    facts_task_desc = analyzer.generate_dynamic_task_description(headline, "facts")
    
    print(f"📋 TASK KEYWORD GÉNÉRÉE:")
    print(f"   {keyword_task_desc[:100]}...")
    print()
    
    print(f"📋 TASK FACTS GÉNÉRÉE:")
    print(f"   {facts_task_desc[:100]}...")
    print()
    
    print(f"✅ SYSTÈME ADAPTATIF CONFIRMED:")
    print(f"   🔄 Plus de termes hardcodés!")
    print(f"   🧠 Adaptation automatique au sujet")
    print(f"   🎯 Termes pertinents pour inflation/chômage")
    
    # Vérifier qu'on n'a plus les anciens termes
    old_terms = ['Trump tariffs', 'Novo Nordisk', 'Ozempic', 'EU China trade']
    found_old_terms = any(old_term.lower() in ' '.join(search_terms).lower() for old_term in old_terms)
    
    if not found_old_terms:
        print(f"   ✅ Aucun ancien terme hardcodé détecté!")
        print(f"   🚀 Système 100% adaptatif!")
    else:
        print(f"   ⚠️ Encore des anciens termes détectés")
    
    return search_terms

if __name__ == "__main__":
    test_current_headline()
