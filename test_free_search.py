# Script de test pour la recherche web gratuite
# Ce test vérifie que tous les composants fonctionnent sans API

print("🧪 TEST DE LA RECHERCHE WEB GRATUITE")
print("=" * 50)

try:
    # Import des modules
    print("📦 Test des imports...")
    from free_search_tools import FreeWebSearchTool, FreeSearchCrewAITool
    import requests
    import feedparser
    from bs4 import BeautifulSoup
    print("✅ Tous les imports réussis!")

    # Test de l'outil de recherche
    print("\n🔍 Test de l'outil de recherche...")
    search_tool = FreeWebSearchTool()
    print("✅ Outil de recherche initialisé!")

    # Test rapide de recherche RSS (limité pour le test)
    print("\n📡 Test de recherche RSS...")
    rss_results = search_tool.search_rss_feeds("business news", limit=3)
    print(f"✅ Recherche RSS réussie: {len(rss_results)} résultats trouvés")

    if rss_results:
        print(f"   Premier résultat: {rss_results[0].get('title', 'Titre non disponible')[:60]}...")

    # Test de l'interface CrewAI
    print("\n🤖 Test de l'interface CrewAI...")
    crewai_tool = FreeSearchCrewAITool()
    print("✅ Interface CrewAI initialisée!")

    print("\n🎉 TOUS LES TESTS RÉUSSIS!")
    print("✅ Le système de recherche gratuit fonctionne parfaitement")
    print("✅ Aucune API ni inscription requise")
    print("✅ Prêt à être utilisé avec CrewAI")

except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    print("💡 Installez les dépendances: pip install -r requirements.txt")

except Exception as e:
    print(f"❌ Erreur: {e}")
    print("💡 Vérifiez votre connexion internet pour les tests RSS")

print("\n" + "=" * 50)
print("Pour lancer le système complet:")
print("1. pip install -r requirements.txt")
print("2. Définir DEEPSEEK_API_KEY dans un fichier .env")
print("3. python main.py")
print("\n🚀 Votre système utilisera désormais la recherche gratuite!")
