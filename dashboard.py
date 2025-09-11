# Tableau de bord complet du système de génération d'articles SEO
# Affiche l'état de tous les composants et les performances

import os
import json
from datetime import datetime

def check_files_status():
    """Vérifier l'état de tous les fichiers du système"""
    
    files_to_check = {
        # Scripts principaux
        'main.py': 'Script principal génération article',
        'html_generator.py': 'Générateur HTML SEO',
        'seo_score_analyzer.py': 'Analyseur score SEO',
        'seo_optimizer.py': 'Optimiseur automatique',
        
        # Scripts de workflow
        'complete_workflow.py': 'Workflow complet automatisé',
        'change_topic.py': 'Changement sujet rapide',
        
        # Scripts de recherche
        'free_search_tools.py': 'Recherche web gratuite',
        'freshness_validator.py': 'Validation fraîcheur',
        
        # Scripts de test
        'test_free_search.py': 'Test recherche gratuite',
        'test_freshness_integration.py': 'Test intégration fraîcheur',
        
        # Fichiers de configuration
        'requirements.txt': 'Dépendances Python',
        'README_workflow.md': 'Documentation complète',
        
        # Fichiers générés (optionnels)
        'seo_article_output.json': 'Article JSON généré',
        'seo_optimized_article.html': 'Page HTML générée',
        'seo_optimized_article_v2.html': 'Page HTML optimisée',
        'seo_analysis_report.txt': 'Rapport analyse SEO'
    }
    
    file_status = {}
    for filename, description in files_to_check.items():
        exists = os.path.exists(filename)
        size = os.path.getsize(filename) if exists else 0
        file_status[filename] = {
            'exists': exists,
            'size': size,
            'description': description,
            'status': '✅' if exists else ('⚠️' if 'generated' in description.lower() else '❌')
        }
    
    return file_status

def analyze_json_data():
    """Analyser les données de l'article JSON si disponible"""
    
    if not os.path.exists('seo_article_output.json'):
        return None
    
    try:
        with open('seo_article_output.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extraire les métriques clés
        article = data.get('article', {})
        seo_audit = data.get('seo_audit', {})
        keyword_research = data.get('keyword_research', {})
        
        return {
            'title': article.get('title', 'N/A'),
            'word_count': len(article.get('introduction', '').split()) + 
                         sum(len(section.split()) for section in article.get('body', [])) +
                         len(article.get('conclusion', '').split()),
            'primary_keywords': len(keyword_research.get('primary_keywords', [])),
            'long_tail_keywords': len(keyword_research.get('long_tail_phrases', [])),
            'freshness_score': seo_audit.get('freshness_metrics', {}).get('data_freshness_score', 'N/A'),
            'overall_seo_score': seo_audit.get('overall_seo_score', 'N/A'),
            'readability_score': seo_audit.get('readability_score', 'N/A')
        }
        
    except Exception as e:
        return {'error': str(e)}

def check_system_health():
    """Vérifier la santé générale du système"""
    
    health_checks = []
    
    # Vérifier les scripts essentiels
    essential_files = ['main.py', 'free_search_tools.py', 'freshness_validator.py', 'html_generator.py']
    all_essential_present = all(os.path.exists(f) for f in essential_files)
    
    health_checks.append({
        'check': 'Scripts essentiels',
        'status': '✅ OK' if all_essential_present else '❌ MANQUANT',
        'details': f"{sum(1 for f in essential_files if os.path.exists(f))}/{len(essential_files)} présents"
    })
    
    # Vérifier les dépendances
    deps_exist = os.path.exists('requirements.txt')
    health_checks.append({
        'check': 'Fichier dépendances',
        'status': '✅ OK' if deps_exist else '❌ MANQUANT', 
        'details': 'requirements.txt présent' if deps_exist else 'requirements.txt manquant'
    })
    
    # Vérifier la génération récente
    json_exists = os.path.exists('seo_article_output.json')
    html_exists = os.path.exists('seo_optimized_article.html')
    
    if json_exists and html_exists:
        generation_status = '✅ COMPLET'
        generation_details = 'Article JSON + Page HTML générés'
    elif json_exists:
        generation_status = '⚠️ PARTIEL'
        generation_details = 'Article JSON généré, HTML manquant'
    else:
        generation_status = '❌ AUCUN'
        generation_details = 'Aucun fichier généré'
    
    health_checks.append({
        'check': 'Génération récente',
        'status': generation_status,
        'details': generation_details
    })
    
    return health_checks

def display_dashboard():
    """Afficher le tableau de bord complet"""
    
    print("🎯 TABLEAU DE BORD - SYSTÈME GÉNÉRATION ARTICLES SEO")
    print("=" * 70)
    
    # Date et heure
    print(f"📅 Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    # 1. Santé du système
    print("🔧 SANTÉ DU SYSTÈME")
    print("-" * 30)
    
    health_checks = check_system_health()
    for check in health_checks:
        print(f"{check['status']} {check['check']}: {check['details']}")
    print()
    
    # 2. État des fichiers
    print("📁 ÉTAT DES FICHIERS")
    print("-" * 30)
    
    file_status = check_files_status()
    
    # Scripts principaux
    print("🔥 Scripts Principaux:")
    main_scripts = ['main.py', 'html_generator.py', 'seo_score_analyzer.py', 'seo_optimizer.py']
    for script in main_scripts:
        if script in file_status:
            status = file_status[script]
            size_kb = status['size'] / 1024 if status['size'] > 0 else 0
            print(f"  {status['status']} {script:<25} ({size_kb:.1f} KB)")
    
    print()
    
    # Scripts de workflow
    print("🔄 Scripts Workflow:")
    workflow_scripts = ['complete_workflow.py', 'change_topic.py']
    for script in workflow_scripts:
        if script in file_status:
            status = file_status[script]
            size_kb = status['size'] / 1024 if status['size'] > 0 else 0
            print(f"  {status['status']} {script:<25} ({size_kb:.1f} KB)")
    
    print()
    
    # Fichiers générés
    print("📄 Fichiers Générés:")
    generated_files = ['seo_article_output.json', 'seo_optimized_article.html', 'seo_optimized_article_v2.html']
    for file in generated_files:
        if file in file_status:
            status = file_status[file]
            size_kb = status['size'] / 1024 if status['size'] > 0 else 0
            age = ""
            if status['exists']:
                mod_time = os.path.getmtime(file)
                age = f" - {datetime.fromtimestamp(mod_time).strftime('%H:%M:%S')}"
            print(f"  {status['status']} {file:<30} ({size_kb:.1f} KB{age})")
    
    print()
    
    # 3. Métriques de performance
    print("📊 MÉTRIQUES DE PERFORMANCE")
    print("-" * 40)
    
    json_data = analyze_json_data()
    if json_data and 'error' not in json_data:
        print(f"📰 Titre: {json_data['title'][:50]}{'...' if len(json_data['title']) > 50 else ''}")
        print(f"📝 Nombre de mots: {json_data['word_count']}")
        print(f"🎯 Mots-clés primaires: {json_data['primary_keywords']}")
        print(f"🔍 Long-tail phrases: {json_data['long_tail_keywords']}")
        print(f"🔥 Score fraîcheur: {json_data['freshness_score']}/100")
        print(f"🏆 Score SEO global: {json_data['overall_seo_score']}/100")
        print(f"📖 Score lisibilité: {json_data['readability_score']}")
        
        # Évaluation du score
        seo_score = json_data.get('overall_seo_score', 0)
        if isinstance(seo_score, (int, float)):
            if seo_score >= 80:
                seo_status = "🏆 EXCELLENT"
            elif seo_score >= 65:
                seo_status = "✅ OBJECTIF ATTEINT"
            elif seo_score >= 50:
                seo_status = "⚠️ AMÉLIORATIONS REQUISES"
            else:
                seo_status = "❌ OPTIMISATION NÉCESSAIRE"
            
            print(f"🎯 Statut SEO: {seo_status} ({seo_score}%)")
        
    elif json_data and 'error' in json_data:
        print(f"❌ Erreur lecture JSON: {json_data['error']}")
    else:
        print("⚠️ Aucun article généré récemment")
        print("💡 Utilisez: python main.py pour générer un article")
    
    print()
    
    # 4. Commandes disponibles
    print("🚀 COMMANDES DISPONIBLES")
    print("-" * 30)
    
    commands = [
        ("python main.py", "Générer un nouvel article"),
        ("python html_generator.py", "Créer page HTML SEO"),
        ("python seo_score_analyzer.py", "Analyser score SEO"),
        ("python complete_workflow.py", "Workflow complet"),
        ("python change_topic.py \"Sujet\"", "Changer sujet rapidement"),
        ("python seo_optimizer.py", "Optimiser pour 80%+")
    ]
    
    for cmd, desc in commands:
        print(f"  📌 {cmd:<35} - {desc}")
    
    print()
    
    # 5. Recommandations
    print("💡 RECOMMANDATIONS")
    print("-" * 25)
    
    recommendations = []
    
    if not os.path.exists('seo_article_output.json'):
        recommendations.append("🔧 Générer un premier article avec: python main.py")
    
    if os.path.exists('seo_article_output.json') and not os.path.exists('seo_optimized_article.html'):
        recommendations.append("🌐 Créer la page HTML avec: python html_generator.py")
    
    if os.path.exists('seo_optimized_article.html') and not os.path.exists('seo_analysis_report.txt'):
        recommendations.append("📊 Analyser le score SEO avec: python seo_score_analyzer.py")
    
    json_data = analyze_json_data()
    if json_data and isinstance(json_data.get('overall_seo_score'), (int, float)) and json_data.get('overall_seo_score') < 80:
        recommendations.append("⚡ Optimiser pour 80%+ avec: python seo_optimizer.py")
    
    if not recommendations:
        recommendations.append("🎉 Système optimal ! Prêt pour publication")
    
    for rec in recommendations:
        print(f"  {rec}")
    
    print()
    print("🎊 SYSTÈME OPÉRATIONNEL - Score SEO cible 65-80% atteignable")
    print("=" * 70)

if __name__ == "__main__":
    display_dashboard()
