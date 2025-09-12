# 🔑 Configuration des API Keys - 100% GRATUITES

## ⚡ ÉTAPES D'INSTALLATION

### 1. Créer le fichier .env
Créez un fichier `.env` dans le répertoire racine du projet avec le contenu suivant :

```bash
# DeepSeek API (OBLIGATOIRE)
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# YouTube API (OPTIONNEL - améliore les résultats)
YOUTUBE_API_KEY=your_youtube_api_key_here

# Reddit API (OPTIONNEL - améliore les résultats)
REDDIT_CLIENT_ID=your_reddit_client_id_here
REDDIT_CLIENT_SECRET=your_reddit_client_secret_here
```

### 2. Obtenir les clés API GRATUITES

## 🚀 **DeepSeek API (OBLIGATOIRE)**
- **Coût** : Gratuit avec crédits offerts
- **Limite** : Aucune limite de temps
- **Comment obtenir** :
  1. Aller sur https://platform.deepseek.com/api_keys
  2. Créer un compte gratuit
  3. Copier la clé API
  4. Remplacer `your_deepseek_api_key_here` dans .env

## 🎥 **YouTube Data API v3 (OPTIONNEL)**
- **Coût** : 100% Gratuit
- **Limite** : 10,000 unités/jour (très élevé)
- **Comment obtenir** :
  1. Aller sur https://console.developers.google.com/
  2. Créer un nouveau projet Google Cloud
  3. Activer "YouTube Data API v3"
  4. Créer des identifiants > Clé API
  5. Copier la clé et remplacer dans .env

## 🔍 **Reddit API (OPTIONNEL)**  
- **Coût** : 100% Gratuit
- **Limite** : 1000 requêtes/minute
- **Comment obtenir** :
  1. Aller sur https://www.reddit.com/prefs/apps
  2. Cliquer "Create App" ou "Create Another App"
  3. Type : "script"
  4. Nom : "KeywordResearch" 
  5. Description : "Keyword research tool"
  6. Copier Client ID et Client Secret

## ✅ **APIs Automatiques (SANS CLÉ)**

Ces services fonctionnent automatiquement sans configuration :

- **Google Trends** (via pytrends) - 100% gratuit
- **Google/Bing Autocomplete** - APIs publiques
- **DuckDuckGo Search** - gratuit et sans limite  
- **RSS Feeds** - sources publiques
- **Scraping éthique** - gratuit

## 🚫 **Services PAYANTS NON Utilisés**

Ce projet n'utilise AUCUN service payant :
- ❌ Google Search Console API
- ❌ SEMrush API  
- ❌ Ahrefs API
- ❌ Moz API
- ❌ Serper API (remplacé par DuckDuckGo)

## 🛡️ **Sécurité**

1. **Ne jamais** commit le fichier `.env` dans git
2. Ajouter `.env` dans `.gitignore`
3. Les clés API sont personnelles et sensibles

## ⚠️ **Note Importante**

- **DEEPSEEK_API_KEY** est OBLIGATOIRE pour faire fonctionner le système
- Les autres clés sont OPTIONNELLES mais améliorent significativement les résultats
- Sans les clés optionnelles, le système fonctionne avec les sources gratuites uniquement
