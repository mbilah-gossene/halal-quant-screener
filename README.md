# ☪️ Halal Quant — Screener Sharia Euronext Paris

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-2D7A5F?style=flat)
![AAOIFI](https://img.shields.io/badge/Norme-AAOIFI-1a7a5c?style=flat)
![Actions](https://img.shields.io/badge/Actions-116+-blue?style=flat)
![Filtres](https://img.shields.io/badge/Filtres-10_niveaux-orange?style=flat)

**Screener d'actions conformes à la Sharia** pour les investisseurs musulmans. Analyse automatique de **116+ actions Euronext Paris** selon les normes **AAOIFI** avec 10 niveaux de filtrage, 25+ métriques financières, et un comparateur d'ETF islamiques.

> *"Investir en accord avec vos valeurs"*

---

## Fonctionnalités

### 📊 Screener Euronext Paris
- Analyse de **116+ actions** (CAC 40, SBF 120, Mid & Small Caps)
- **10 niveaux de filtrage AAOIFI** séquentiels
- Capitalisation boursière **moyenne sur 12 mois** (norme AAOIFI)
- Vérification croisée sur les **états trimestriels**
- Score Sharia (0-100) pour chaque action
- Export CSV et JSON

### 🔍 Recherche individuelle
- Analyse de **n'importe quelle action mondiale** (AAPL, MSFT, etc.)
- Fiche complète avec jauges visuelles des 5 ratios AAOIFI
- 25+ métriques organisées par catégorie (Valorisation, Profitabilité, Risque)
- Calcul du taux de purification du dividende

### 📈 Comparateur ETF Islamiques
- 8 ETF conformes Sharia (iShares, Wahed, SP Funds)
- Performance 1 an, volatilité, frais, AUM
- Comparaison des normes (AAOIFI, MSCI, DJIMI)
- Recommandation PEA vs CTO

### 📖 Méthodologie transparente
- Documentation complète du pipeline de filtrage
- Comparaison des normes Sharia internationales

---

## Pipeline de filtrage AAOIFI — 10 niveaux

```
Action Euronext
     │
     ▼
 [N0] Qualité des données ≥ 40% ──── NON ──→ ⬜ Données insuffisantes
     │ OUI
     ▼
 [N1] Secteur haram ? ──────────── OUI ──→ 🔴 Haram
     │ NON
     ▼
 [N2] Industrie haram ? (30+) ──── OUI ──→ 🔴 Haram
     │ NON
     ▼
 [N3] Liste noire ? (14) ──────── OUI ──→ 🔴 Haram
     │ NON
     ▼
 [N4] Mots-clés haram ? (28) ──── OUI ──→ 🔴 Haram
     │ NON
     ▼
[N4b] Segment haram manuel ? ──── OUI ──→ 🔴 Haram
     │ NON
     ▼
 [N5] Revenus haram > 5% CA ? ─── OUI ──→ 🟡 Non conforme
     │ NON
     ▼
[N5b] Charges int. > 5% CA ? ──── OUI ──→ 🟡 Non conforme
     │ NON
     ▼
 [N6] Ratios AAOIFI dépassés ? ─── OUI ──→ 🟡 Non conforme
     │  Dette/Cap > 33%
     │  Cash+Inv/Cap > 33%
     │  Créances/Cap > 49%
     │ NON
     ▼
[N6b] D/E Ratio > 150 ? ──────── OUI ──→ 🟡 Non conforme
     │ NON
     ▼
 [N7] Cross-check trimestriel ──── Warning si écart
     │
     ▼
 [N8] Zone grise ? ────────────── Malus -10 pts
     │
     ▼
 🟢 CONFORME SHARIA (Score 0-100)
```

### Ratios financiers AAOIFI

| Ratio | Formule | Seuil |
|-------|---------|-------|
| **Dette** | Dette totale / Cap. moyenne 12 mois | < 33% |
| **Liquidités** | (Cash + Placements CT + LT) / Cap. moyenne 12 mois | < 33% |
| **Créances** | Créances clients / Cap. moyenne 12 mois | < 49% |
| **Revenus haram** | (Intérêts + Autres revenus) / CA | < 5% |
| **Charges d'intérêts** | Charges d'intérêts / CA | < 5% |

---

## Installation

```bash
# Cloner le repo
git clone https://github.com/mbilah-gossene/halal-quant-screener.git
cd halal-quant-screener

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run app.py
```

### Prérequis

- Python 3.9+
- Connexion internet (pour Yahoo Finance)

### Dépendances

```
streamlit >= 1.30.0
pandas >= 2.0.0
yfinance >= 0.2.30
```

---

## Déploiement Streamlit Cloud

1. Fork ou push ce repo sur GitHub
2. Aller sur [share.streamlit.io](https://share.streamlit.io)
3. Connecter votre compte GitHub
4. Sélectionner ce repo, branche `main`, fichier `app.py`
5. Cliquer sur **Deploy**

L'app sera accessible via une URL publique.

---

## Structure du projet

```
halal-quant-screener/
├── app.py                  # Application principale Streamlit
├── requirements.txt        # Dépendances Python
├── .streamlit/
│   └── config.toml         # Configuration Streamlit (thème)
└── README.md               # Ce fichier
```

---

## Sources de données

- **Yahoo Finance** via la librairie `yfinance` — données financières, bilans, ratios
- **Données manuelles** — Liste noire, segments de revenus haram, industries à surveiller
- **Normes AAOIFI** — Seuils de conformité basés sur les standards de l'Accounting and Auditing Organization for Islamic Financial Institutions

### Limitations

- La ventilation du CA par segment n'est pas disponible via yfinance (compensé par le mapping manuel `REVENUE_HARAM_MANUAL`)
- Les participations croisées dans des sociétés haram ne sont pas détectables automatiquement
- La purification des plus-values (pas seulement des dividendes) nécessite un calcul manuel

---

## Comparaison avec les solutions existantes

| Fonctionnalité | Halal Quant | Zoya | Musaffa |
|---|---|---|---|
| Actions Euronext Paris | ✅ 116+ | ❌ | ❌ |
| Norme AAOIFI | ✅ | ✅ | ✅ |
| Cap. moyenne 12 mois | ✅ | ✅ | ✅ |
| Vérif. trimestrielle | ✅ | ✅ | ✅ |
| Charges d'intérêts | ✅ | ❌ | ❌ |
| D/E ratio complémentaire | ✅ | ❌ | ❌ |
| Open source | ✅ | ❌ | ❌ |
| Gratuit | ✅ | Freemium | Freemium |
| Focus France / PEA | ✅ | ❌ | ❌ |

---

## Auteur

**Mbilah Gossene** — M2 Finance, INSEEC Business School Bordeaux

- Alternance chez Floa (BNP Paribas)
- Fondateur de [Mirame Vidéo](https://miramevideo.com)
- Passionné de finance islamique et de data science

---

## Avertissement

Cet outil est un **aide à la décision** et ne constitue pas un conseil en investissement. Les données proviennent de Yahoo Finance et peuvent contenir des erreurs ou des retards. Consultez un conseiller financier qualifié et un scholar pour valider vos décisions d'investissement.

---

## Licence

MIT License — Libre d'utilisation, de modification et de distribution.

---

<p align="center">
  <strong>☪️ Halal Quant</strong> — Investir en accord avec vos valeurs
</p>
