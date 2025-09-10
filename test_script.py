# Script de test pour vérifier que CrewAI fonctionne correctement
# Ce script ne nécessite pas de clés API

import os
import json
from typing import Dict, Any
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# Configuration pour un test simple sans clés API
print("=== Test de CrewAI sans clés API ===")

# Créer un LLM factice pour le test
class MockLLM:
    def __init__(self):
        self.model_name = "mock-model"
    
    def invoke(self, messages, **kwargs):
        # Simulation d'une réponse
        return type('Response', (), {
            'content': 'Ceci est une réponse simulée pour tester CrewAI. Le système fonctionne correctement !'
        })()

# Utiliser le LLM factice
llm = MockLLM()

# Outil de recherche simple
class SimpleSearchTool:
    def __init__(self):
        self.name = "simple_search"
    
    def run(self, query: str) -> str:
        return f"Résultats de recherche simulés pour: {query}"

search_tool = SimpleSearchTool()

# Créer un agent simple
test_agent = Agent(
    role="Test Agent",
    goal="Tester que CrewAI fonctionne correctement",
    backstory="Agent de test pour vérifier l'installation",
    tools=[],  # Pas d'outils pour le test
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

# Créer une tâche simple
test_task = Task(
    description="Générer un message de test simple",
    agent=test_agent,
    expected_output="Un message confirmant que CrewAI fonctionne",
)

# Créer le crew
crew = Crew(
    agents=[test_agent],
    tasks=[test_task],
    process=Process.sequential,
    verbose=True,
)

print("✅ Tous les imports fonctionnent correctement")
print("✅ Les agents et tâches sont créés avec succès")
print("✅ Le crew est configuré correctement")
print("\n🎉 CrewAI est correctement installé et configuré !")
print("\nPour utiliser le script principal (main.py), vous devez :")
print("1. Obtenir une clé API DeepSeek sur https://platform.deepseek.com/api_keys")
print("2. Obtenir une clé API Serper sur https://serper.dev/")
print("3. Définir les variables d'environnement DEEPSEEK_API_KEY et SERPER_API_KEY")
print("4. Ou modifier le script pour utiliser d'autres APIs de recherche")
