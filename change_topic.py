# Script pour changer rapidement le sujet d'article et régénérer automatiquement
# Usage: python change_topic.py "Votre nouveau sujet d'article"

import sys
import subprocess
import re

def change_headline_in_main(new_headline):
    """Changer le HEADLINE dans main.py automatiquement"""
    
    try:
        # Lire le fichier main.py
        with open('main.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Trouver et remplacer la ligne HEADLINE
        pattern = r'HEADLINE = ".*?"'
        replacement = f'HEADLINE = "{new_headline}"'
        
        new_content = re.sub(pattern, replacement, content)
        
        # Sauvegarder le fichier modifié
        with open('main.py', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Sujet mis à jour dans main.py:")
        print(f"📰 Nouveau sujet: {new_headline}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la modification: {e}")
        return False

def run_complete_workflow():
    """Exécuter le workflow complet après changement de sujet"""
    try:
        print("\n🚀 Lancement du workflow complet...")
        result = subprocess.run([sys.executable, "complete_workflow.py"], 
                              capture_output=True, 
                              text=True, 
                              encoding='utf-8')
        
        # Afficher la sortie
        if result.stdout:
            print(result.stdout)
        
        if result.returncode == 0:
            print("🎉 Workflow terminé avec succès!")
            return True
        else:
            print("❌ Erreur dans le workflow:")
            if result.stderr:
                print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erreur d'exécution: {e}")
        return False

def show_usage():
    """Afficher les instructions d'utilisation"""
    print("📋 UTILISATION:")
    print("=" * 50)
    print("python change_topic.py \"Votre sujet d'article\"")
    print()
    print("📝 EXEMPLES:")
    print("python change_topic.py \"IA et emplois : impact sur le marché français en 2025\"")
    print("python change_topic.py \"Bitcoin dépasse 100,000$ : analyse des conséquences économiques\"")
    print("python change_topic.py \"Microsoft acquiert OpenAI pour 50 milliards de dollars\"")
    print()
    print("🎯 Le script va automatiquement:")
    print("✅ 1. Modifier le sujet dans main.py")
    print("✅ 2. Générer un nouvel article SEO optimisé")
    print("✅ 3. Créer la page HTML correspondante")
    print("✅ 4. Fournir un audit SEO complet")

def main():
    print("🔄 CHANGEMENT DE SUJET D'ARTICLE")
    print("=" * 50)
    
    # Vérifier les arguments
    if len(sys.argv) != 2:
        print("❌ Argument manquant!")
        show_usage()
        return
    
    new_headline = sys.argv[1].strip()
    
    if not new_headline:
        print("❌ Sujet vide!")
        show_usage()
        return
    
    print(f"📰 Nouveau sujet: {new_headline}")
    print(f"📏 Longueur: {len(new_headline)} caractères")
    
    # Validation du sujet
    if len(new_headline) < 10:
        print("⚠️ Attention: Sujet très court (moins de 10 caractères)")
    elif len(new_headline) > 200:
        print("⚠️ Attention: Sujet très long (plus de 200 caractères)")
    
    print()
    
    # Étape 1: Changer le sujet
    if not change_headline_in_main(new_headline):
        print("❌ Échec du changement de sujet")
        return
    
    # Étape 2: Lancer le workflow complet
    success = run_complete_workflow()
    
    if success:
        print(f"\n🎊 SUCCÈS TOTAL!")
        print(f"📄 Article généré: seo_article_output.json")
        print(f"🌐 Page web créée: seo_optimized_article.html")
        print(f"🎯 Score SEO cible: 65-80%")
        print(f"\n💡 Votre nouvel article est prêt à être publié!")
    else:
        print(f"\n❌ Échec du workflow complet")

if __name__ == "__main__":
    main()
