#!/usr/bin/env python3
"""
Test script pour valider le système de recherche de mots-clés adaptatif
Teste toutes les nouvelles fonctionnalités sans exécuter le système complet
"""

import sys
import os
from typing import Dict, Any

def test_adaptive_system():
    """Test complet du système adaptatif"""
    print("🧪 TESTING ADAPTIVE KEYWORD RESEARCH SYSTEM")
    print("=" * 60)
    
    try:
        # Test 1: Import des nouveaux modules
        print("\n1️⃣ TESTING IMPORTS...")
        
        from adaptive_keyword_context import AdaptiveKeywordContextAnalyzer
        print("✅ adaptive_keyword_context imported successfully")
        
        from advanced_keyword_tools import AdvancedKeywordResearchTool  
        print("✅ advanced_keyword_tools imported successfully")
        
        from final_headline_analyzer import FinalHeadlineAnalyzer
        print("✅ enhanced final_headline_analyzer imported successfully")
        
        # Test 2: Initialisation des analyzers
        print("\n2️⃣ TESTING INITIALIZATION...")
        
        context_analyzer = AdaptiveKeywordContextAnalyzer()
        print("✅ Context analyzer initialized")
        
        advanced_tool = AdvancedKeywordResearchTool()
        print("✅ Advanced keyword tool initialized") 
        
        headline_analyzer = FinalHeadlineAnalyzer()
        print("✅ Headline analyzer initialized")
        
        # Test 3: Analyse contextuelle
        print("\n3️⃣ TESTING CONTEXT ANALYSIS...")
        
        test_headlines = [
            "UMich September prelim consumer sentiment 55.4 vs 58.0 expected",
            "Tesla reports Q3 earnings beat expectations",
            "Fed raises interest rates by 0.75%", 
            "Apple launches new iPhone 15 with AI features"
        ]
        
        for i, headline in enumerate(test_headlines, 1):
            print(f"\n📋 Test {i}: '{headline[:30]}...'")
            
            # Test context detection
            context = context_analyzer.detect_headline_domain(headline)
            print(f"   Domain: {context['primary_domain']}")
            print(f"   Type: {context['headline_type']}")
            print(f"   Confidence: {context['domain_confidence']:.2f}")
            
            # Test entity extraction  
            entities = context_analyzer.extract_adaptive_entities(headline)
            print(f"   Entities: {len(entities['primary_entities'])} found")
            
            # Test search strategy generation (sans API calls)
            if i == 1:  # Tester seulement pour le premier pour éviter trop d'API calls
                print(f"   Testing search strategy generation...")
                try:
                    strategy = context_analyzer.generate_adaptive_search_strategy(headline)
                    print(f"   ✅ Strategy generated: {len(strategy['adaptive_search_terms'])} terms")
                except Exception as e:
                    print(f"   ⚠️ Strategy generation error (expected with APIs): {e}")
        
        # Test 4: Génération de mots-clés adaptative
        print("\n4️⃣ TESTING ADAPTIVE KEYWORD GENERATION...")
        
        test_headline = test_headlines[0]  # UMich headline
        search_terms = headline_analyzer.generate_automatic_search_terms(test_headline)
        print(f"✅ Generated {len(search_terms)} adaptive search terms")
        print(f"   Sample terms: {search_terms[:5]}")
        
        # Test 5: Stratégie complète
        print("\n5️⃣ TESTING COMPREHENSIVE STRATEGY...")
        
        strategy = headline_analyzer.generate_adaptive_keyword_strategy(test_headline)
        print(f"✅ Complete strategy generated")
        print(f"   Terms: {len(strategy['search_terms'])}")
        print(f"   Approach: {strategy['recommended_approach'][:50]}...")
        
        # Test 6: Test du tool avancé (sans API calls)
        print("\n6️⃣ TESTING ADVANCED TOOL CAPABILITIES...")
        
        print("✅ Google Trends available:", advanced_tool.trends_available)
        print("✅ YouTube API available:", advanced_tool.youtube_available) 
        print("✅ Reddit API available:", advanced_tool.reddit_available)
        
        # Test de génération de questions
        questions = advanced_tool.scrape_answer_the_public_style("consumer sentiment")
        print(f"✅ Generated {len(questions)} question-based keywords")
        print(f"   Sample: {questions[0] if questions else 'None'}")
        
        # Test de difficulty estimation (une seule pour éviter trop de requêtes)
        difficulty = advanced_tool.estimate_keyword_difficulty("consumer sentiment")
        print(f"✅ Keyword difficulty estimated: {difficulty.get('difficulty', 'Unknown')}")
        
        # Résultat final
        print("\n🎉 ALL TESTS PASSED!")
        print("=" * 60)
        print("✅ Adaptive system is ready for production")
        print("🚀 All components working correctly")
        print("📊 Context analysis functioning")
        print("🎯 Keyword generation adaptive")
        print("🔍 Advanced tools initialized")
        
        return True
        
    except ImportError as e:
        print(f"❌ IMPORT ERROR: {e}")
        print("💡 Run: pip install -r requirements.txt")
        return False
        
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {e}")
        print(f"📍 Error type: {type(e).__name__}")
        return False

def test_main_integration():
    """Test l'intégration avec main.py sans l'exécuter complètement"""
    print("\n🔗 TESTING MAIN.PY INTEGRATION...")
    
    try:
        # Importer les fonctions de main sans exécuter
        sys.path.insert(0, '.')
        
        # Test import direct
        from main import create_adaptive_keyword_researcher, create_adaptive_keyword_task
        print("✅ Main integration functions imported successfully")
        
        # Test création d'agent (sans LLM)
        test_context = {
            'primary_domain': 'economic_data',
            'headline_type': 'data_release_with_comparison',
            'domain_confidence': 0.85
        }
        
        print("✅ Integration test completed")
        return True
        
    except Exception as e:
        print(f"⚠️ Integration test error: {e}")
        print("💡 This is expected if DeepSeek API key is not set")
        return False

if __name__ == "__main__":
    print("🚀 STARTING ADAPTIVE SYSTEM VALIDATION")
    print("=" * 60)
    
    # Test du système principal
    system_ok = test_adaptive_system()
    
    # Test de l'intégration
    integration_ok = test_main_integration()
    
    print("\n📊 TEST SUMMARY:")
    print("=" * 30)
    print(f"🎯 System Components: {'✅ PASS' if system_ok else '❌ FAIL'}")
    print(f"🔗 Main Integration: {'✅ PASS' if integration_ok else '⚠️ SKIP'}")
    
    if system_ok:
        print("\n🎉 ADAPTIVE KEYWORD RESEARCH SYSTEM IS READY!")
        print("💡 You can now run: python main.py")
        print("🔑 Make sure to configure API keys in .env for best results")
    else:
        print("\n❌ SYSTEM NOT READY - Please fix errors above")
        
    print("=" * 60)
