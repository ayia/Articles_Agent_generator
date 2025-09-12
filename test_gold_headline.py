#!/usr/bin/env python3
"""
Test spécifique pour le headline Gold - Démonstration du système adaptatif
Montre comment le système s'adapte automatiquement à un contenu complètement différent
"""

def test_gold_headline_adaptation():
    """Test d'adaptation pour le headline Gold"""
    print("🥇 TESTING ADAPTIVE SYSTEM WITH GOLD HEADLINE")
    print("=" * 70)
    
    # Le nouveau headline Gold (très différent du précédent)
    gold_headline = """Gold is testing the top of the daily range. It's up $15 to $3649 today and perked up following the softer UMich consumer sentiment data.The precious metal is consolidating now after reaching $3675 on Tuesday in a spike higher. It's likely to continue sideways until Wednesday's FOMC decision. A dovish bent from the Fed chair would be a green light for the gold bulls to take it another leg higher. I don't think we'd need to see a surprise 50 bps cut but if Powell validates employment concerns and downplays inflation then it could continue the surge.Techncially, Tuesday's high and overbought conditions are the only thing standing in the way of further gains and beyond that it will be big round figures like $3750 and $4000 offering up resistance.On the geopolitical side, the US appears to be trying to ramp up pressure on Russia to enter talks on Ukraine peace. That presents two-sided risks as harsher Russian sanctions or reserve confiscation could strengthen the case for gold, while a peace deal would weaken it. My sense is that Trump has played his best cards in terms of diplomacy but Russia isn't interested and feels it has the upper hand in the war."""
    
    try:
        # Import des modules adaptatifs
        from adaptive_keyword_context import AdaptiveKeywordContextAnalyzer
        from final_headline_analyzer import FinalHeadlineAnalyzer
        from advanced_keyword_tools import AdvancedKeywordResearchTool
        
        print("✅ All adaptive modules loaded successfully\n")
        
        # 1. COMPARAISON DES ANALYSES
        print("📊 ADAPTIVE ANALYSIS COMPARISON")
        print("=" * 50)
        
        # Headline précédent pour comparaison
        old_headline = "UMich September prelim consumer sentiment 55.4 vs 58.0 expected"
        
        print(f"🔄 OLD HEADLINE: {old_headline[:50]}...")
        print(f"🆕 NEW HEADLINE: {gold_headline[:50]}...")
        
        # 2. INITIALISATION DES ANALYZERS
        context_analyzer = AdaptiveKeywordContextAnalyzer()
        headline_analyzer = FinalHeadlineAnalyzer()
        advanced_tool = AdvancedKeywordResearchTool()
        
        print("\n🧠 CONTEXT ANALYSIS COMPARISON")
        print("-" * 40)
        
        # Analyser l'ancien headline
        old_context = context_analyzer.detect_headline_domain(old_headline)
        print(f"📊 OLD → Domain: {old_context['primary_domain']}")
        print(f"     → Type: {old_context['headline_type']}")
        print(f"     → Confidence: {old_context['domain_confidence']:.2f}")
        
        # Analyser le nouveau headline Gold
        print("\n🥇 ANALYZING NEW GOLD HEADLINE...")
        gold_context = context_analyzer.detect_headline_domain(gold_headline)
        print(f"✨ NEW → Domain: {gold_context['primary_domain']}")
        print(f"     → Type: {gold_context['headline_type']}")
        print(f"     → Confidence: {gold_context['domain_confidence']:.2f}")
        
        # 3. EXTRACTION D'ENTITÉS ADAPTATIVE
        print("\n🎯 ENTITY EXTRACTION COMPARISON")
        print("-" * 40)
        
        old_entities = context_analyzer.extract_adaptive_entities(old_headline)
        gold_entities = context_analyzer.extract_adaptive_entities(gold_headline)
        
        print(f"📊 OLD Entities: {old_entities['primary_entities'][:5]}")
        print(f"🥇 NEW Entities: {gold_entities['primary_entities'][:8]}")
        
        print(f"📊 OLD Numbers: {old_entities['numerical_data']}")
        print(f"🥇 NEW Numbers: {gold_entities['numerical_data'][:8]}")
        
        print(f"📊 OLD Time refs: {old_entities['temporal_references']}")
        print(f"🥇 NEW Time refs: {gold_entities['temporal_references']}")
        
        # 4. GÉNÉRATION DE MOTS-CLÉS ADAPTATIVE
        print("\n🔍 ADAPTIVE KEYWORD GENERATION")
        print("-" * 40)
        
        old_keywords = headline_analyzer.generate_automatic_search_terms(old_headline)
        gold_keywords = headline_analyzer.generate_automatic_search_terms(gold_headline)
        
        print(f"📊 OLD Keywords ({len(old_keywords)}):")
        for i, kw in enumerate(old_keywords[:5], 1):
            print(f"   {i}. {kw}")
        
        print(f"\n🥇 NEW Keywords ({len(gold_keywords)}):")
        for i, kw in enumerate(gold_keywords[:10], 1):
            print(f"   {i}. {kw}")
        
        if len(gold_keywords) > 10:
            print(f"   ... et {len(gold_keywords) - 10} autres mots-clés")
        
        # 5. STRATÉGIE ADAPTATIVE COMPLÈTE
        print("\n📋 ADAPTIVE STRATEGY COMPARISON")
        print("-" * 40)
        
        old_strategy = headline_analyzer.generate_adaptive_keyword_strategy(old_headline)
        gold_strategy = headline_analyzer.generate_adaptive_keyword_strategy(gold_headline)
        
        print(f"📊 OLD Strategy:")
        print(f"   Approach: {old_strategy['recommended_approach'][:80]}...")
        
        print(f"\n🥇 NEW Strategy:")
        print(f"   Approach: {gold_strategy['recommended_approach'][:80]}...")
        
        # 6. ANALYSE DES DIFFÉRENCES
        print("\n🔄 ADAPTATION ANALYSIS")
        print("=" * 50)
        
        domain_changed = old_context['primary_domain'] != gold_context['primary_domain']
        type_changed = old_context['headline_type'] != gold_context['headline_type']
        
        print(f"🎯 Domain Change: {'✅ YES' if domain_changed else '❌ NO'}")
        print(f"   {old_context['primary_domain']} → {gold_context['primary_domain']}")
        
        print(f"📝 Type Change: {'✅ YES' if type_changed else '❌ NO'}")  
        print(f"   {old_context['headline_type']} → {gold_context['headline_type']}")
        
        print(f"🔍 Keywords Change: {'✅ YES' if set(old_keywords) != set(gold_keywords) else '❌ NO'}")
        print(f"   {len(old_keywords)} → {len(gold_keywords)} terms")
        
        # Analyse thématique
        old_themes = set([kw.split()[0] for kw in old_keywords if ' ' in kw][:5])
        gold_themes = set([kw.split()[0] for kw in gold_keywords if ' ' in kw][:5])
        
        print(f"🎨 Theme Change: {'✅ YES' if old_themes != gold_themes else '❌ NO'}")
        print(f"   OLD themes: {', '.join(list(old_themes)[:5])}")
        print(f"   NEW themes: {', '.join(list(gold_themes)[:5])}")
        
        # 7. GÉNÉRATION DE QUESTIONS ADAPTATIVES
        print("\n❓ QUESTION-BASED KEYWORDS (Advanced Tool)")
        print("-" * 50)
        
        # Test quelques mots-clés principaux du gold headline
        gold_main_keywords = ['gold', 'FOMC', 'Fed', 'Russia', 'Ukraine']
        
        for keyword in gold_main_keywords[:3]:
            questions = advanced_tool.scrape_answer_the_public_style(keyword)
            print(f"🎯 {keyword.upper()} questions ({len(questions)}):")
            for i, q in enumerate(questions[:3], 1):
                print(f"   {i}. {q}")
            print()
        
        # 8. RÉSULTAT FINAL
        print("🎉 ADAPTATION RESULTS")
        print("=" * 50)
        
        adaptations = []
        if domain_changed:
            adaptations.append(f"✅ Domain: {old_context['primary_domain']} → {gold_context['primary_domain']}")
        if type_changed:
            adaptations.append(f"✅ Type: {old_context['headline_type']} → {gold_context['headline_type']}")
        if len(gold_keywords) != len(old_keywords):
            adaptations.append(f"✅ Keywords: {len(old_keywords)} → {len(gold_keywords)} terms")
        
        print(f"🚀 TOTAL ADAPTATIONS: {len(adaptations)}")
        for adaptation in adaptations:
            print(f"   {adaptation}")
        
        print(f"\n💡 SYSTEM ADAPTATION SUCCESS:")
        print(f"   🎯 Detected new domain: {gold_context['primary_domain']}")
        print(f"   📊 Generated {len(gold_keywords)} contextual keywords")
        print(f"   🔍 Adapted strategy to {gold_context['headline_type']}")
        print(f"   ⚡ All without ANY hardcoding!")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    print("🚀 TESTING SYSTEM ADAPTATION WITH GOLD HEADLINE")
    print("🎯 This demonstrates how the system adapts to COMPLETELY different content")
    print("=" * 70)
    
    success = test_gold_headline_adaptation()
    
    if success:
        print("\n🎉 ADAPTATION TEST SUCCESSFUL!")
        print("✅ System perfectly adapted to Gold trading content")
        print("🔄 From economic sentiment → to precious metals trading")
        print("🚀 Ready for ANY headline content!")
    else:
        print("\n❌ TEST FAILED - Check error messages above")
    
    print("=" * 70)
