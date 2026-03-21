import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import json
import time
from datetime import datetime

st.set_page_config(page_title="Halal Quant", page_icon="☪️", layout="wide", initial_sidebar_state="collapsed")

# ══════════════════════════════════════════════════════
# BILINGUAL SYSTEM
# ══════════════════════════════════════════════════════

if "lang" not in st.session_state:
    st.session_state.lang = "fr"

LANG = {
    "fr": {
        # Brand
        "brand_actions": "{n} actions Euronext",
        "brand_norm": "Norme AAOIFI",
        "brand_by": "Par Mbilah Gossene",
        # Tabs
        "tab_screener": "📊  Screener",
        "tab_search": "🔍  Recherche",
        "tab_portfolio": "💼  Portefeuille",
        "tab_benchmark": "⚡  Benchmark",
        "tab_alerts": "🔔  Alertes",
        "tab_etf": "📈  ETF Islamiques",
        "tab_method": "📖  Méthodologie",
        # Statuses
        "status_conforme": "Conforme",
        "status_non_conforme": "Non conforme",
        "status_haram": "Haram",
        "status_nodata": "Données insuff.",
        # Verdict labels
        "verdict_halal": "CONFORME SHARIA",
        "verdict_halal_sub": "Tous les critères AAOIFI sont respectés",
        "verdict_nc": "NON CONFORME",
        "verdict_nc_sub": "Un ou plusieurs ratios financiers dépassent les seuils",
        "verdict_haram": "HARAM",
        "verdict_haram_sub": "Activité principale incompatible avec la Sharia",
        "verdict_nodata": "DONNÉES INSUFFISANTES",
        "verdict_nodata_sub": "Pas assez de données financières pour une analyse fiable",
        # Search page
        "search_desc": "Analysez n'importe quelle action dans le monde selon les normes AAOIFI.",
        "search_placeholder": "Entrez un ticker — ex: AAPL, MSFT, TTE.PA, AIR.PA...",
        "search_analyzing": "Analyse de {tc}...",
        "search_nodata": "Aucune donnée trouvée pour {tc}.",
        "search_error": "Erreur lors de l'analyse : {e}",
        # Sections
        "sec_business": "Business Activity Screening",
        "sec_financial": "Financial Screening — Ratios AAOIFI",
        "sec_score": "Score Sharia",
        "sec_valuation": "Valorisation",
        "sec_profitability": "Profitabilité & Croissance",
        "sec_risk": "Risque & Endettement",
        "sec_company": "À propos de l'entreprise",
        "sec_purification": "Purification",
        "sec_alternatives": "Alternatives conformes",
        # Business screening
        "biz_pass": "L'activité principale de l'entreprise est conforme aux principes de la Sharia. Aucune activité interdite détectée.",
        "biz_fail_sector": "Secteur interdit : {reason}",
        "biz_fail_industry": "Industrie interdite : {reason}",
        "biz_fail_blacklist": "Entreprise exclue : {reason}",
        "biz_fail_keywords": "Mots-clés haram détectés : {reason}",
        "biz_fail_revenue": "Revenus haram : {reason}",
        "biz_grayzone": "Zone grise — Cette industrie ({ind}) nécessite une vigilance accrue. Un malus de 10 points est appliqué au score.",
        # Financial screening
        "fin_debt": "Dette / Capitalisation",
        "fin_cash": "Cash + Invest. / Capitalisation",
        "fin_receivables": "Créances / Capitalisation",
        "fin_haram_rev": "Revenus haram / CA",
        "fin_interest": "Charges d'intérêts / CA",
        "fin_threshold": "seuil {s}%",
        "pass": "PASS",
        "fail": "FAIL",
        "na": "N/A",
        # Company info
        "employees": "Employés",
        "website": "Site web",
        "country": "Pays",
        "sector": "Secteur",
        "industry": "Industrie",
        "cap_type": "Cap. boursière",
        "week52": "52 semaines",
        "avg_volume": "Volume moyen",
        "description": "Description",
        "no_desc": "Aucune description disponible.",
        # Purification
        "purif_text": "{pct}% de vos dividendes sont à reverser en sadaqa (charité) pour purifier votre investissement. Sur un investissement de 10 000€ avec un rendement de {div}%, cela représente environ {amount}€ par an.",
        "purif_none": "Aucune purification nécessaire — les revenus haram sont à 0%.",
        # Alternatives
        "alt_text": "Voici des actions conformes Sharia dans le même secteur ({sec}) que vous pouvez envisager :",
        "alt_none": "Lancez le screener complet pour découvrir des alternatives conformes dans ce secteur.",
        "alt_run_screener": "Lancez d'abord le Screener pour obtenir des alternatives personnalisées.",
        # Screener
        "screener_launch": "Lancer l'analyse complète",
        "screener_desc": "Analysez {n} actions selon 10 niveaux de filtrage AAOIFI.",
        "screener_sub": "Capitalisation moyenne 12 mois · Vérification trimestrielle · 25+ métriques.",
        "analyzed": "Analysées",
        "conformes": "Conformes",
        "non_conformes": "Non conformes",
        "haram": "Haram",
        "data_insuff": "Data insuff.",
        "gray_zones": "Zones grises",
        "compliant_stocks": "Actions conformes Sharia",
        "download_csv": "📥  CSV complet",
        "download_conformes": "📥  Conformes seuls",
        "download_json": "📥  Rapport JSON",
        # Portfolio
        "ptf_desc": "Construisez un portefeuille d'actions conformes Sharia, diversifié par secteur et optimisé selon votre profil de risque.",
        "ptf_amount": "Montant à investir (€)",
        "ptf_profile": "Profil de risque",
        "ptf_strategy": "Stratégie d'allocation",
        "ptf_build": "Construire le portefeuille",
        "ptf_prudent": "Prudent",
        "ptf_balanced": "Équilibré",
        "ptf_dynamic": "Dynamique",
        "ptf_score": "Score Sharia",
        "ptf_equal": "Équipondération",
        "ptf_cap": "Capitalisation",
        "ptf_advanced": "Paramètres avancés",
        "ptf_max_stocks": "Nombre max d'actions",
        "ptf_max_sector": "Max par secteur (%)",
        "ptf_min_score": "Score Sharia minimum",
        # Quarterly
        "quarterly_yes": "✓ Données trimestrielles disponibles — cross-check effectué.",
        "div_suspect": "Dividende suspect (>15%) — donnée probablement erronée, à vérifier.",
        # Data quality
        "data_quality": "Qualité des données",
        # Metrics
        "price": "Prix",
        "per": "PER",
        "per_fwd": "PER Forward",
        "cap": "Cap. (M€)",
        "dividend": "Dividende",
        "roe": "ROE",
        "op_margin": "Marge op.",
        "net_margin": "Marge nette",
        "rev_growth": "Croiss. CA",
        "fcf": "FCF (M€)",
        "beta": "Bêta",
        "de_ratio": "D/E Ratio",
        "current_ratio": "Current Ratio",
        "ocf": "OCF (M€)",
        "pb_ratio": "Price/Book",
        "gross_margin": "Marge brute",
        "earnings_growth": "Croiss. BN",
    },
    "en": {
        "brand_actions": "{n} Euronext stocks",
        "brand_norm": "AAOIFI Standard",
        "brand_by": "By Mbilah Gossene",
        "tab_screener": "📊  Screener",
        "tab_search": "🔍  Search",
        "tab_portfolio": "💼  Portfolio",
        "tab_benchmark": "⚡  Benchmark",
        "tab_alerts": "🔔  Alerts",
        "tab_etf": "📈  Islamic ETFs",
        "tab_method": "📖  Methodology",
        "status_conforme": "Compliant",
        "status_non_conforme": "Non-compliant",
        "status_haram": "Haram",
        "status_nodata": "Insufficient data",
        "verdict_halal": "SHARIAH COMPLIANT",
        "verdict_halal_sub": "All AAOIFI criteria are met",
        "verdict_nc": "NON-COMPLIANT",
        "verdict_nc_sub": "One or more financial ratios exceed the thresholds",
        "verdict_haram": "HARAM",
        "verdict_haram_sub": "Core business activity is incompatible with Shariah",
        "verdict_nodata": "INSUFFICIENT DATA",
        "verdict_nodata_sub": "Not enough financial data for a reliable analysis",
        "search_desc": "Analyze any stock worldwide against AAOIFI standards.",
        "search_placeholder": "Enter a ticker — e.g. AAPL, MSFT, TTE.PA, AIR.PA...",
        "search_analyzing": "Analyzing {tc}...",
        "search_nodata": "No data found for {tc}.",
        "search_error": "Error during analysis: {e}",
        "sec_business": "Business Activity Screening",
        "sec_financial": "Financial Screening — AAOIFI Ratios",
        "sec_score": "Shariah Score",
        "sec_valuation": "Valuation",
        "sec_profitability": "Profitability & Growth",
        "sec_risk": "Risk & Leverage",
        "sec_company": "About the Company",
        "sec_purification": "Purification",
        "sec_alternatives": "Compliant Alternatives",
        "biz_pass": "The company's core business activity is compliant with Shariah principles. No prohibited activities detected.",
        "biz_fail_sector": "Prohibited sector: {reason}",
        "biz_fail_industry": "Prohibited industry: {reason}",
        "biz_fail_blacklist": "Blacklisted company: {reason}",
        "biz_fail_keywords": "Haram keywords detected: {reason}",
        "biz_fail_revenue": "Haram revenue: {reason}",
        "biz_grayzone": "Gray zone — This industry ({ind}) requires extra vigilance. A 10-point penalty is applied to the score.",
        "fin_debt": "Debt / Market Cap",
        "fin_cash": "Cash + Invest. / Market Cap",
        "fin_receivables": "Receivables / Market Cap",
        "fin_haram_rev": "Haram Revenue / Revenue",
        "fin_interest": "Interest Expense / Revenue",
        "fin_threshold": "threshold {s}%",
        "pass": "PASS",
        "fail": "FAIL",
        "na": "N/A",
        "employees": "Employees",
        "website": "Website",
        "country": "Country",
        "sector": "Sector",
        "industry": "Industry",
        "cap_type": "Market Cap",
        "week52": "52-Week Range",
        "avg_volume": "Avg Volume",
        "description": "Description",
        "no_desc": "No description available.",
        "purif_text": "{pct}% of your dividends should be given as sadaqah (charity) to purify your investment. On a €10,000 investment with a {div}% yield, that's roughly €{amount} per year.",
        "purif_none": "No purification needed — haram revenue is at 0%.",
        "alt_text": "Here are Shariah-compliant stocks in the same sector ({sec}) you may consider:",
        "alt_none": "Run the full screener to discover compliant alternatives in this sector.",
        "alt_run_screener": "Run the Screener first to get personalized alternatives.",
        "screener_launch": "Run Full Analysis",
        "screener_desc": "Analyze {n} stocks through 10 levels of AAOIFI screening.",
        "screener_sub": "12-month average market cap · Quarterly verification · 25+ metrics.",
        "analyzed": "Analyzed",
        "conformes": "Compliant",
        "non_conformes": "Non-compliant",
        "haram": "Haram",
        "data_insuff": "Insuff. data",
        "gray_zones": "Gray zones",
        "compliant_stocks": "Shariah-compliant stocks",
        "download_csv": "📥  Full CSV",
        "download_conformes": "📥  Compliant only",
        "download_json": "📥  JSON Report",
        "ptf_desc": "Build a diversified Shariah-compliant stock portfolio optimized for your risk profile.",
        "ptf_amount": "Investment amount (€)",
        "ptf_profile": "Risk profile",
        "ptf_strategy": "Allocation strategy",
        "ptf_build": "Build Portfolio",
        "ptf_prudent": "Conservative",
        "ptf_balanced": "Balanced",
        "ptf_dynamic": "Aggressive",
        "ptf_score": "Shariah Score",
        "ptf_equal": "Equal Weight",
        "ptf_cap": "Market Cap",
        "ptf_advanced": "Advanced Settings",
        "ptf_max_stocks": "Max stocks",
        "ptf_max_sector": "Max per sector (%)",
        "ptf_min_score": "Min Shariah Score",
        "quarterly_yes": "✓ Quarterly data available — cross-check performed.",
        "div_suspect": "Suspicious dividend (>15%) — data likely incorrect, please verify.",
        "data_quality": "Data Quality",
        "price": "Price",
        "per": "P/E",
        "per_fwd": "Forward P/E",
        "cap": "Cap. (M€)",
        "dividend": "Dividend",
        "roe": "ROE",
        "op_margin": "Op. Margin",
        "net_margin": "Net Margin",
        "rev_growth": "Rev. Growth",
        "fcf": "FCF (M€)",
        "beta": "Beta",
        "de_ratio": "D/E Ratio",
        "current_ratio": "Current Ratio",
        "ocf": "OCF (M€)",
        "pb_ratio": "Price/Book",
        "gross_margin": "Gross Margin",
        "earnings_growth": "Earn. Growth",
    }
}

def T(key, **kwargs):
    text = LANG[st.session_state.lang].get(key, key)
    if kwargs:
        try: text = text.format(**kwargs)
        except: pass
    return text

# ══════════════════════════════════════════════════════
# CSS — Premium Warm Fintech + Phase 1 Components
# ══════════════════════════════════════════════════════

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Source+Code+Pro:wght@400;500;600;700&display=swap');

    :root {
        --cream: #FDFCFA; --white: #FFFFFF; --warm-50: #FAF8F5; --warm-100: #F3F0EB;
        --warm-200: #E8E4DD; --warm-300: #D4CFC6; --warm-400: #B0AAA0;
        --ink: #1B1B18; --ink-2: #4A4A45; --ink-3: #7C7C75; --ink-4: #A8A8A2;
        --sage: #2D7A5F; --sage-light: #E6F3ED; --sage-bg: #F2FAF6; --sage-dark: #1F5C46;
        --coral: #C2442D; --coral-light: #FCEEED; --coral-bg: #FFF5F4;
        --honey: #B8860B; --honey-light: #FFF8E7; --honey-bg: #FFFDF5;
        --sky: #3576C2; --sky-light: #EBF3FC;
        --stone: #6B6B65; --stone-light: #F5F5F3;
        --r: 14px; --r-sm: 10px; --r-xs: 6px; --r-full: 50px;
        --shadow-sm: 0 1px 2px rgba(27,27,24,0.04);
        --shadow: 0 2px 8px rgba(27,27,24,0.06), 0 1px 2px rgba(27,27,24,0.04);
        --shadow-lg: 0 8px 24px rgba(27,27,24,0.08), 0 2px 6px rgba(27,27,24,0.04);
        --shadow-glow-sage: 0 4px 16px rgba(45,122,95,0.12);
    }

    /* ── Global ── */
    .stApp { font-family: 'Inter', -apple-system, sans-serif; background: var(--cream); color: var(--ink); }
    [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
    #MainMenu, footer, header { visibility: hidden; }

    /* ── Brand Bar ── */
    .brand {
        display: flex; align-items: center; justify-content: space-between;
        padding: 14px 0; margin-bottom: 4px;
    }
    .brand-left { display: flex; align-items: center; gap: 10px; }
    .brand-mark {
        width: 38px; height: 38px; border-radius: 10px;
        background: linear-gradient(135deg, var(--sage) 0%, var(--sage-dark) 100%);
        display: flex; align-items: center; justify-content: center;
        font-size: 1.1rem; color: white; box-shadow: var(--shadow-glow-sage);
    }
    .brand-text { font-size: 1.15rem; font-weight: 800; color: var(--ink); letter-spacing: -0.5px; }
    .brand-text em { font-style: normal; color: var(--sage); }
    .brand-right { display: flex; gap: 6px; flex-wrap: wrap; align-items: center; }
    .brand-pill {
        font-size: 0.6rem; font-weight: 700; padding: 3px 10px; border-radius: var(--r-full);
        background: var(--warm-50); border: 1px solid var(--warm-200); color: var(--ink-3);
        letter-spacing: 0.2px;
    }

    /* ── Hero ── */
    .hero-empty {
        text-align: center; padding: 3.5rem 1.5rem;
        background: linear-gradient(160deg, var(--sage-bg) 0%, var(--cream) 50%, var(--honey-bg) 100%);
        border: 1px solid var(--warm-200); border-radius: 20px;
        position: relative; overflow: hidden;
    }
    .hero-empty::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
        background: repeating-conic-gradient(var(--warm-100) 0% 25%, transparent 0% 50%) 50% / 60px 60px;
        opacity: 0.3;
    }
    .hero-empty * { position: relative; }
    .hero-icon { font-size: 3rem; margin-bottom: 8px; filter: drop-shadow(0 2px 8px rgba(45,122,95,0.15)); }
    .hero-title { font-size: 1.2rem; font-weight: 700; color: var(--ink); margin: 0 0 6px; }
    .hero-sub { font-size: 0.8rem; color: var(--ink-3); margin: 0; line-height: 1.5; }
    .hero-chips { display: flex; gap: 6px; justify-content: center; margin-top: 14px; flex-wrap: wrap; }
    .hero-chip {
        font-size: 0.62rem; font-weight: 600; padding: 4px 10px; border-radius: var(--r-full);
        background: white; border: 1px solid var(--warm-200); color: var(--ink-2);
        box-shadow: var(--shadow-sm);
    }

    /* ── Stats Row ── */
    .kpis { display: grid; grid-template-columns: repeat(auto-fit, minmax(110px, 1fr)); gap: 8px; margin: 14px 0; }
    .kpi {
        background: var(--white); border: 1px solid var(--warm-200); border-radius: var(--r);
        padding: 14px 10px 12px; text-align: center; position: relative; overflow: hidden;
        box-shadow: var(--shadow-sm); transition: box-shadow 0.2s, transform 0.2s;
    }
    .kpi:hover { box-shadow: var(--shadow); transform: translateY(-1px); }
    .kpi::after {
        content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
        border-radius: var(--r) var(--r) 0 0;
    }
    .kpi .kv {
        font-family: 'Source Code Pro', monospace; font-size: 1.7rem; font-weight: 700;
        line-height: 1; letter-spacing: -1px;
    }
    .kpi .kl {
        font-size: 0.55rem; color: var(--ink-4); text-transform: uppercase;
        letter-spacing: 0.8px; margin-top: 4px; font-weight: 700;
    }
    .kpi.k-sage .kv{color:var(--sage);} .kpi.k-sage::after{background:var(--sage);}
    .kpi.k-coral .kv{color:var(--coral);} .kpi.k-coral::after{background:var(--coral);}
    .kpi.k-honey .kv{color:var(--honey);} .kpi.k-honey::after{background:var(--honey);}
    .kpi.k-sky .kv{color:var(--sky);} .kpi.k-sky::after{background:var(--sky);}
    .kpi.k-stone .kv{color:var(--stone);} .kpi.k-stone::after{background:var(--stone);}

    /* ── Section Divider ── */
    .sdiv {
        display: flex; align-items: center; gap: 10px;
        margin: 1.8rem 0 0.6rem; padding-bottom: 8px;
    }
    .sdiv-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
    .sdiv-dot.d-sage{background:var(--sage);} .sdiv-dot.d-coral{background:var(--coral);}
    .sdiv-dot.d-honey{background:var(--honey);} .sdiv-dot.d-stone{background:var(--stone);}
    .sdiv-dot.d-sky{background:var(--sky);}
    .sdiv h3 { font-size: 0.92rem; font-weight: 700; color: var(--ink); margin: 0; letter-spacing: -0.2px; }
    .sdiv .sdiv-cnt {
        font-family: 'Source Code Pro', monospace; font-size: 0.62rem; font-weight: 600;
        color: var(--ink-3); background: var(--warm-100); padding: 2px 8px; border-radius: var(--r-full);
    }

    /* ══════════════════════════════════════════════
       PHASE 1 — ZOYA-STYLE STOCK DETAIL
       ══════════════════════════════════════════════ */

    /* ── Stock Header ── */
    .stock-header {
        background: var(--white); border: 1px solid var(--warm-200); border-radius: 20px;
        padding: 28px 28px 24px; margin: 14px 0; box-shadow: var(--shadow);
        position: relative; overflow: hidden;
    }
    .stock-header::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px;
    }
    .stock-header.sh-ok::before { background: linear-gradient(90deg, var(--sage) 0%, #4CAF50 100%); }
    .stock-header.sh-nc::before { background: linear-gradient(90deg, var(--honey) 0%, #F5A623 100%); }
    .stock-header.sh-h::before  { background: linear-gradient(90deg, var(--coral) 0%, #E74C3C 100%); }
    .stock-header.sh-nd::before { background: linear-gradient(90deg, var(--stone) 0%, #999 100%); }

    .sh-top { display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 16px; }
    .sh-info { flex: 1; min-width: 200px; }
    .sh-name { font-size: 1.5rem; font-weight: 800; color: var(--ink); margin: 0; letter-spacing: -0.5px; line-height: 1.2; }
    .sh-meta { font-size: 0.75rem; color: var(--ink-3); margin: 5px 0 0; display: flex; gap: 6px; flex-wrap: wrap; align-items: center; }
    .sh-meta-pill {
        font-size: 0.62rem; font-weight: 600; padding: 2px 8px; border-radius: var(--r-full);
        background: var(--warm-100); color: var(--ink-3);
    }
    .sh-price-row { display: flex; align-items: baseline; gap: 8px; margin-top: 10px; }
    .sh-price { font-family: 'Source Code Pro', monospace; font-size: 1.8rem; font-weight: 700; color: var(--ink); }
    .sh-currency { font-size: 0.85rem; color: var(--ink-3); font-weight: 600; }

    /* ── Giant Verdict Badge (Zoya-style) ── */
    .verdict-hero {
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        padding: 16px 24px; border-radius: 16px; min-width: 180px; text-align: center;
    }
    .verdict-hero-ok { background: var(--sage-bg); border: 2px solid rgba(45,122,95,0.2); }
    .verdict-hero-nc { background: var(--honey-bg); border: 2px solid rgba(184,134,11,0.2); }
    .verdict-hero-h  { background: var(--coral-bg); border: 2px solid rgba(194,68,29,0.2); }
    .verdict-hero-nd { background: var(--stone-light); border: 2px solid rgba(107,107,101,0.2); }

    .vh-icon { font-size: 2rem; margin-bottom: 4px; }
    .vh-label { font-size: 0.85rem; font-weight: 800; letter-spacing: 0.5px; }
    .verdict-hero-ok .vh-label { color: var(--sage); }
    .verdict-hero-nc .vh-label { color: var(--honey); }
    .verdict-hero-h .vh-label  { color: var(--coral); }
    .verdict-hero-nd .vh-label { color: var(--stone); }
    .vh-sub { font-size: 0.62rem; color: var(--ink-3); margin-top: 2px; max-width: 180px; line-height: 1.4; }

    /* ── Screening Section Cards ── */
    .screen-card {
        background: var(--white); border: 1px solid var(--warm-200); border-radius: 16px;
        padding: 22px 24px; margin: 10px 0; box-shadow: var(--shadow-sm);
    }
    .sc-header {
        display: flex; align-items: center; justify-content: space-between; gap: 12px;
        margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid var(--warm-100);
    }
    .sc-title {
        font-size: 0.85rem; font-weight: 700; color: var(--ink); display: flex; align-items: center; gap: 8px;
    }
    .sc-title-icon {
        width: 28px; height: 28px; border-radius: 8px; display: inline-flex;
        align-items: center; justify-content: center; font-size: 0.85rem; flex-shrink: 0;
    }
    .sc-title-icon.sci-biz { background: var(--sky-light); }
    .sc-title-icon.sci-fin { background: var(--sage-light); }

    .sc-badge {
        font-size: 0.62rem; font-weight: 800; padding: 4px 12px; border-radius: var(--r-full);
        letter-spacing: 0.5px;
    }
    .sc-badge-pass { background: var(--sage-light); color: var(--sage); }
    .sc-badge-fail { background: var(--coral-light); color: var(--coral); }
    .sc-badge-warn { background: var(--honey-light); color: var(--honey); }
    .sc-badge-na   { background: var(--stone-light); color: var(--stone); }

    .sc-body { font-size: 0.78rem; color: var(--ink-2); line-height: 1.6; }
    .sc-body strong { color: var(--ink); }

    /* ── Financial Ratio Rows (Zoya-style) ── */
    .ratio-row {
        display: flex; align-items: center; gap: 14px; padding: 14px 0;
        border-bottom: 1px solid var(--warm-100);
    }
    .ratio-row:last-child { border-bottom: none; }

    .rr-info { flex: 1; min-width: 120px; }
    .rr-name { font-size: 0.78rem; font-weight: 600; color: var(--ink); }
    .rr-threshold { font-size: 0.6rem; color: var(--ink-4); margin-top: 1px; }

    .rr-bar-wrap { flex: 2; min-width: 100px; }
    .rr-bar { height: 8px; background: var(--warm-200); border-radius: 4px; overflow: hidden; position: relative; }
    .rr-fill { height: 100%; border-radius: 4px; transition: width 0.6s ease; }

    .rr-value {
        font-family: 'Source Code Pro', monospace; font-size: 0.88rem; font-weight: 700;
        min-width: 55px; text-align: right;
    }
    .rr-badge {
        font-size: 0.55rem; font-weight: 800; padding: 3px 8px; border-radius: var(--r-xs);
        letter-spacing: 0.3px; min-width: 36px; text-align: center;
    }
    .rr-badge-pass { background: var(--sage-light); color: var(--sage); }
    .rr-badge-fail { background: var(--coral-light); color: var(--coral); }
    .rr-badge-na   { background: var(--stone-light); color: var(--stone); }

    /* ── Score Circle (CSS conic-gradient) ── */
    .score-ring-wrap {
        display: flex; align-items: center; gap: 24px; padding: 20px 24px;
        background: var(--white); border: 1px solid var(--warm-200); border-radius: 16px;
        box-shadow: var(--shadow-sm); margin: 10px 0;
    }
    .score-ring {
        width: 110px; height: 110px; border-radius: 50%; display: flex;
        align-items: center; justify-content: center; flex-shrink: 0;
    }
    .score-ring-inner {
        width: 82px; height: 82px; border-radius: 50%; background: var(--white);
        display: flex; flex-direction: column; align-items: center; justify-content: center;
    }
    .score-ring-val {
        font-family: 'Source Code Pro', monospace; font-size: 1.8rem; font-weight: 800; line-height: 1;
    }
    .score-ring-label { font-size: 0.55rem; color: var(--ink-4); font-weight: 600; }
    .score-details { flex: 1; }
    .score-details p { margin: 0 0 4px; font-size: 0.78rem; color: var(--ink-2); line-height: 1.5; }
    .score-details strong { color: var(--ink); }
    .score-breakdown {
        display: flex; gap: 6px; flex-wrap: wrap; margin-top: 8px;
    }
    .sb-chip {
        font-size: 0.58rem; font-weight: 600; padding: 3px 8px; border-radius: var(--r-xs);
        background: var(--warm-100); color: var(--ink-3);
    }
    .sb-chip.sb-bonus { background: var(--sage-light); color: var(--sage); }
    .sb-chip.sb-malus { background: var(--coral-light); color: var(--coral); }

    /* ── Company Info Grid ── */
    .company-grid {
        display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1px;
        background: var(--warm-200); border-radius: 12px; overflow: hidden; margin: 10px 0;
        border: 1px solid var(--warm-200);
    }
    .cg-item { background: var(--white); padding: 14px 16px; }
    .cg-label { font-size: 0.58rem; color: var(--ink-4); text-transform: uppercase; letter-spacing: 0.5px; font-weight: 700; margin: 0; }
    .cg-value { font-size: 0.82rem; font-weight: 600; color: var(--ink); margin: 3px 0 0; word-break: break-word; }
    .cg-value a { color: var(--sage); text-decoration: none; }

    .company-desc {
        background: var(--white); border: 1px solid var(--warm-200); border-radius: 12px;
        padding: 18px 20px; margin: 10px 0; font-size: 0.78rem; color: var(--ink-2);
        line-height: 1.7; max-height: 200px; overflow-y: auto;
    }

    /* ── Metric Cards (financial data) ── */
    .metric-grid {
        display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 8px; margin: 10px 0;
    }
    .m-card {
        background: var(--white); border: 1px solid var(--warm-200); border-radius: var(--r);
        padding: 14px 12px; text-align: center; box-shadow: var(--shadow-sm);
        transition: box-shadow 0.2s, transform 0.2s;
    }
    .m-card:hover { box-shadow: var(--shadow); transform: translateY(-1px); }
    .m-label { font-size: 0.55rem; color: var(--ink-4); text-transform: uppercase; letter-spacing: 0.5px; font-weight: 700; margin: 0; }
    .m-val { font-family: 'Source Code Pro', monospace; font-size: 1.15rem; font-weight: 700; color: var(--ink); margin: 4px 0 0; }

    /* ── Purification Card ── */
    .purif-card {
        background: linear-gradient(135deg, var(--sage-bg) 0%, var(--white) 100%);
        border: 1px solid rgba(45,122,95,0.15); border-radius: 16px;
        padding: 20px 24px; margin: 10px 0; display: flex; gap: 16px; align-items: flex-start;
    }
    .purif-icon { font-size: 1.5rem; flex-shrink: 0; }
    .purif-body { flex: 1; }
    .purif-title { font-size: 0.85rem; font-weight: 700; color: var(--sage-dark); margin: 0 0 6px; }
    .purif-text { font-size: 0.78rem; color: var(--ink-2); line-height: 1.6; margin: 0; }
    .purif-pct {
        font-family: 'Source Code Pro', monospace; font-size: 1.8rem; font-weight: 800;
        color: var(--sage); margin: 0; text-align: center; min-width: 80px;
    }
    .purif-pct-label { font-size: 0.55rem; color: var(--ink-4); text-align: center; }

    /* ── Alternatives Grid ── */
    .alt-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 8px; margin: 10px 0; }
    .alt-card {
        background: var(--white); border: 1px solid var(--warm-200); border-radius: var(--r);
        padding: 14px; box-shadow: var(--shadow-sm); transition: box-shadow 0.2s;
    }
    .alt-card:hover { box-shadow: var(--shadow); }
    .alt-name { font-size: 0.82rem; font-weight: 700; color: var(--ink); margin: 0; }
    .alt-ticker { font-size: 0.65rem; color: var(--ink-3); margin: 2px 0 0; font-family: 'Source Code Pro', monospace; }
    .alt-badge {
        display: inline-block; font-size: 0.55rem; font-weight: 700; padding: 2px 6px;
        border-radius: var(--r-xs); background: var(--sage-light); color: var(--sage); margin-top: 6px;
    }

    /* ── Info Callout ── */
    .callout {
        display: flex; gap: 12px; padding: 14px 16px;
        background: var(--sage-bg); border: 1px solid rgba(45,122,95,0.12); border-radius: var(--r);
        margin: 10px 0; align-items: flex-start;
    }
    .callout-icon { font-size: 1rem; flex-shrink: 0; margin-top: 1px; }
    .callout p { margin: 0; font-size: 0.8rem; color: var(--sage-dark); line-height: 1.5; }
    .callout strong { color: var(--ink); }

    /* ── DQ pill ── */
    .dq-pill {
        font-family: 'Source Code Pro', monospace; font-size: 0.58rem; font-weight: 600;
        padding: 2px 8px; border-radius: var(--r-xs); display: inline-block;
    }
    .dq-h { background: var(--sage-light); color: var(--sage); }
    .dq-m { background: var(--honey-light); color: var(--honey); }
    .dq-l { background: var(--coral-light); color: var(--coral); }

    /* ── Pipeline (methodology) ── */
    .pipeline { margin: 1.5rem 0; }
    .pipe-step {
        display: flex; align-items: flex-start; gap: 14px; padding: 12px 0;
        position: relative;
    }
    .pipe-step:not(:last-child)::after {
        content: ''; position: absolute; left: 15px; top: 36px; bottom: 0;
        width: 2px; background: var(--warm-200);
    }
    .pipe-num {
        width: 32px; height: 32px; border-radius: 50%; flex-shrink: 0;
        display: flex; align-items: center; justify-content: center;
        font-family: 'Source Code Pro', monospace; font-size: 0.65rem; font-weight: 700;
        background: var(--sage-light); color: var(--sage); border: 2px solid var(--sage);
        position: relative; z-index: 1;
    }
    .pipe-step.pipe-new .pipe-num { background: var(--honey-light); color: var(--honey); border-color: var(--honey); }
    .pipe-body { flex: 1; }
    .pipe-title { font-size: 0.82rem; font-weight: 700; color: var(--ink); margin: 0 0 2px; }
    .pipe-title .pipe-new-tag {
        font-size: 0.5rem; font-weight: 800; color: var(--honey); background: var(--honey-light);
        padding: 1px 5px; border-radius: 3px; margin-left: 6px; letter-spacing: 0.5px; vertical-align: middle;
    }
    .pipe-desc { font-size: 0.72rem; color: var(--ink-3); margin: 0; }

    /* ── Footer ── */
    .foot {
        text-align: center; padding: 2.5rem 0 1rem; color: var(--ink-4);
        font-size: 0.68rem; border-top: 1px solid var(--warm-200); margin-top: 3rem;
    }
    .foot a { color: var(--sage); text-decoration: none; font-weight: 600; }

    /* ── Streamlit Overrides ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px; background: var(--warm-100); border-radius: var(--r); padding: 3px;
        border: 1px solid var(--warm-200);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: var(--r-sm); font-family: 'Inter', sans-serif;
        font-weight: 700; font-size: 0.75rem; color: var(--ink-3);
    }
    .stTabs [aria-selected="true"] {
        background: var(--white) !important; color: var(--ink) !important;
        box-shadow: var(--shadow-sm);
    }
    div[data-testid="stMetric"] {
        background: var(--white); border: 1px solid var(--warm-200);
        border-radius: var(--r-sm); padding: 12px 14px; box-shadow: var(--shadow-sm);
    }
    div[data-testid="stMetric"] label { font-size: 0.65rem !important; color: var(--ink-4) !important; font-weight: 700 !important; text-transform: uppercase; letter-spacing: 0.5px; }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] { font-family: 'Source Code Pro', monospace !important; font-size: 1.1rem !important; }
    .stDownloadButton button {
        border-radius: var(--r-sm) !important; font-weight: 700 !important;
        font-size: 0.75rem !important; font-family: 'Inter', sans-serif !important;
    }
    button[data-testid="stBaseButton-primary"] {
        background: linear-gradient(135deg, var(--sage) 0%, var(--sage-dark) 100%) !important;
        border: none !important; border-radius: var(--r) !important;
        font-family: 'Inter', sans-serif !important; font-weight: 700 !important;
        font-size: 0.85rem !important; padding: 12px 24px !important;
        box-shadow: var(--shadow-glow-sage) !important;
        transition: all 0.2s !important;
    }
    button[data-testid="stBaseButton-primary"]:hover {
        transform: translateY(-1px) !important; box-shadow: var(--shadow-lg) !important;
    }
    .stTextInput input {
        border-radius: var(--r) !important; border: 1.5px solid var(--warm-200) !important;
        font-family: 'Inter', sans-serif !important; padding: 12px 16px !important;
        font-size: 0.88rem !important; background: var(--white) !important;
    }
    .stTextInput input:focus { border-color: var(--sage) !important; box-shadow: 0 0 0 3px rgba(45,122,95,0.1) !important; }
    [data-testid="stExpander"] { border: 1px solid var(--warm-200) !important; border-radius: var(--r) !important; }
    .stDataFrame { border-radius: var(--r) !important; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# CONFIG AAOIFI V11 — ALL FILTERS (UNCHANGED)
# ══════════════════════════════════════════════════════

SECTEURS_HARAM = ["Financial Services"]
INDUSTRIES_HARAM = [
    "Banks - Regional","Banks - Diversified","Banks - Global","Credit Services","Mortgage Finance",
    "Financial Data & Stock Exchanges","Capital Markets","Asset Management","Financial Conglomerates",
    "Insurance - Diversified","Insurance - Life","Insurance - Property & Casualty",
    "Insurance - Reinsurance","Insurance - Specialty","Insurance Brokers",
    "Alcoholic Beverages","Breweries","Wineries & Distilleries","Distillers & Vintners",
    "Beverages - Wineries & Distilleries","Beverages - Brewers",
    "Tobacco","Gambling","Casinos & Gaming","Resorts & Casinos","Adult Entertainment",
    "Aerospace & Defense","Weapons & Ammunition","Meat Products",
]
LISTE_NOIRE = {
    "MC.PA":"LVMH — alcool > 5% du CA","RI.PA":"Pernod Ricard — alcool 100%",
    "KER.PA":"Kering — Chateau Latour","RCO.PA":"Remy Cointreau — alcool 100%",
    "SW.PA":"Sodexo — alcool en restauration","FDJ.PA":"FDJ — jeux de hasard 100%",
    "CNP.PA":"CNP Assurances","SCR.PA":"SCOR — reassurance",
    "COFA.PA":"Coface — assurance credit","AMUN.PA":"Amundi — gestion actifs/taux",
    "TKO.PA":"Tikehau Capital","RF.PA":"Eurazeo — investissement",
    "UG.PA":"Peugeot Invest","MF.PA":"Wendel — investissement",
}
REVENUE_HARAM_MANUAL = {
    "VIV.PA": ("Vivendi","Canal+ — contenus pour adultes",8),
    "BOL.PA": ("Bollore","Participations medias mixtes",6),
    "ELIOR.PA": ("Elior","Restauration — alcool significatif",7),
}
INDUSTRIES_ATTENTION = [
    "Entertainment","Restaurants","Hotels & Motels","Resorts & Casinos","Packaged Foods",
    "Food Distribution","Drug Manufacturers - General","Drug Manufacturers - Specialty & Generic",
    "Biotechnology","Leisure","Media - Diversified","Advertising Agencies","Broadcasting",
    "Electronic Gaming & Multimedia","Travel Services","Lodging","Luxury Goods",
]
KEYWORDS_HARAM = [
    "alcohol","beer","wine","spirits","brewing","distill","casino","gambling","betting",
    "wagering","tobacco","cigarette","smoking","pork","swine","pig","adult entertainment",
    "pornograph","cannabis","marijuana","interest income","lending","mortgage",
    "weapons","ammunition","military","lottery","slot machine",
]
SEUIL_DETTE=33;SEUIL_CASH=33;SEUIL_CREANCES=49;SEUIL_REV_HARAM=5
SEUIL_REV_ATTENTION=3;SEUIL_INT_EXP=5;SEUIL_DE=150;DQ_MIN=40;DIV_MAX=15

TICKERS = {
    "AI.PA":"Air Liquide","AIR.PA":"Airbus","ALO.PA":"Alstom","MT.AS":"ArcelorMittal",
    "CS.PA":"AXA","BNP.PA":"BNP Paribas","EN.PA":"Bouygues","CAP.PA":"Capgemini",
    "CA.PA":"Carrefour","ACA.PA":"Credit Agricole","BN.PA":"Danone","DSY.PA":"Dassault Systemes",
    "ENGI.PA":"Engie","EL.PA":"EssilorLuxottica","ERF.PA":"Eurofins","RMS.PA":"Hermes",
    "KER.PA":"Kering","LR.PA":"Legrand","OR.PA":"L'Oreal","MC.PA":"LVMH","ML.PA":"Michelin",
    "ORA.PA":"Orange","RI.PA":"Pernod Ricard","PUB.PA":"Publicis","RNO.PA":"Renault",
    "SAF.PA":"Safran","SGO.PA":"Saint-Gobain","SAN.PA":"Sanofi","SU.PA":"Schneider Electric",
    "GLE.PA":"Societe Generale","STLAP.PA":"Stellantis","STMPA.PA":"STMicroelectronics",
    "TEP.PA":"Teleperformance","HO.PA":"Thales","TTE.PA":"TotalEnergies",
    "URW.AS":"Unibail-Rodamco","DG.PA":"Vinci","VIE.PA":"Veolia","VIV.PA":"Vivendi","WLN.PA":"Worldline",
    "AF.PA":"Air France-KLM","AKE.PA":"Arkema","BIM.PA":"bioMerieux","BOL.PA":"Bollore",
    "AM.PA":"Dassault Aviation","FGR.PA":"Eiffage","FDJ.PA":"FDJ","GET.PA":"Getlink",
    "GFC.PA":"Gecina","GTT.PA":"GTT","ILD.PA":"Iliad","IPH.PA":"Ipsen","IPS.PA":"Ipsos",
    "LI.PA":"Klepierre","MMB.PA":"Lagardere","MF.PA":"Wendel","NK.PA":"Imerys",
    "POM.PA":"Plastic Omnium","RXL.PA":"Rexel","RIN.PA":"Rubis","SCR.PA":"SCOR",
    "SK.PA":"SEB","SOI.PA":"Soitec","SOP.PA":"Sopra Steria","SW.PA":"Sodexo",
    "TFI.PA":"TF1","UBI.PA":"Ubisoft","DIM.PA":"Sartorius Stedim",
    "ABIO.PA":"Alten","ALTO.PA":"Altarea","AMUN.PA":"Amundi","APAM.PA":"Aperam",
    "ATO.PA":"Atos","BB.PA":"BIC","BLC.PA":"Boiron","BVI.PA":"Bureau Veritas",
    "CNP.PA":"CNP Assurances","COFA.PA":"Coface","CRI.PA":"Chargeurs","DBV.PA":"DBV Technologies",
    "DEC.PA":"JCDecaux","ELIS.PA":"Elis","FNAC.PA":"Fnac Darty","GBT.PA":"Guerbet",
    "ICAD.PA":"Icade","JXR.PA":"Jacquet Metals","LNA.PA":"LNA Sante",
    "MERY.PA":"Maisons du Monde","MRN.PA":"Mersen","NANO.PA":"Nanobiotix","NEX.PA":"Nexans",
    "OVH.PA":"OVHcloud","PERR.PA":"Gerard Perrier","PSAT.PA":"Pharmagest",
    "RCO.PA":"Remy Cointreau","SAVE.PA":"Savencia","SMCP.PA":"SMCP","SPIE.PA":"SPIE",
    "UG.PA":"Peugeot Invest","VAC.PA":"Vallourec","VRLA.PA":"Verallia",
    "RF.PA":"Eurazeo","ERA.PA":"Eramet","ELIOR.PA":"Elior","NRG.PA":"Neoen",
    "SESG.PA":"SES-imagotag","TKO.PA":"Tikehau Capital","ARGAN.PA":"Argan",
    "MAU.PA":"Maurel et Prom","VCT.PA":"Vicat","VIRP.PA":"Virbac","RBT.PA":"Robertet",
    "QUA.PA":"Quadient","NXI.PA":"Nexity","COV.PA":"Covivio","CGG.PA":"CGG",
}
ETF_ISL = {
    "ISWD.L":{"n":"iShares MSCI World Islamic","e":"BlackRock","z":"Monde","f":0.30,"d":"Irlande","no":"MSCI","ds":"ETF mondial MSCI World Islamic."},
    "ISDE.L":{"n":"iShares MSCI EM Islamic","e":"BlackRock","z":"Emergents","f":0.35,"d":"Irlande","no":"MSCI","ds":"ETF emergents Sharia."},
    "ISUS.L":{"n":"iShares MSCI USA Islamic","e":"BlackRock","z":"USA","f":0.30,"d":"Irlande","no":"MSCI","ds":"ETF actions US Sharia."},
    "SPUS":{"n":"SP Funds S&P 500 Sharia","e":"SP Funds","z":"USA","f":0.49,"d":"USA","no":"AAOIFI","ds":"S&P 500 norme AAOIFI."},
    "HLAL":{"n":"Wahed FTSE USA Shariah","e":"Wahed Invest","z":"USA","f":0.50,"d":"USA","no":"AAOIFI","ds":"ETF Wahed fintech islamique."},
    "UMMA":{"n":"Wahed DJ Islamic World","e":"Wahed Invest","z":"Monde (hors USA)","f":0.65,"d":"USA","no":"DJIMI","ds":"ETF mondial hors USA."},
    "SPRE":{"n":"SP Funds Global REIT Sharia","e":"SP Funds","z":"Immobilier","f":0.59,"d":"USA","no":"AAOIFI","ds":"ETF immobilier Sharia."},
    "APTS":{"n":"Apartment Shariah ETF","e":"SP Funds","z":"USA (Immobilier)","f":0.49,"d":"USA","no":"AAOIFI","ds":"ETF immobilier residentiel US."},
}

# ══════════════════════════════════════════════════════
# ENGINE (UNCHANGED)
# ══════════════════════════════════════════════════════

def avg_mcap(to):
    try:
        h=to.history(period="1y")
        if len(h)<20: return None
        s=to.info.get("sharesOutstanding",0) or 0
        return h["Close"].mean()*s if s else None
    except: return None

def q_check(to):
    try:
        q=to.quarterly_balance_sheet
        if q is None or q.empty: return None
        l=q.iloc[:,0]
        return {"d":l.get("Total Debt",l.get("Long Term Debt",0)) or 0,
                "c":l.get("Cash And Cash Equivalents",0) or 0,
                "r":l.get("Net Receivable",l.get("Receivables",0)) or 0}
    except: return None

def dq(info,ha,hq):
    s=0
    for f in ["marketCap","totalDebt","totalCash","totalRevenue"]:
        if info.get(f) and info[f]!=0: s+=12
    for f in ["currentPrice","sector","industry","netReceivables"]:
        v=info.get(f)
        if v and v!=0 and v!="Inconnu": s+=5
    for f in ["trailingPE","returnOnEquity","profitMargins","beta","dividendYield",
              "interestExpense","shortTermInvestments","longTermInvestments",
              "operatingCashflow","freeCashflow","debtToEquity","currentRatio"]:
        if info.get(f) and info[f]!=0: s+=1.2
    if ha: s+=4
    if hq: s+=3
    return min(100,round(s))

def ckw(info):
    d=(info.get("longBusinessSummary","") or "").lower()
    n=(info.get("shortName","") or "").lower()
    return [k for k in KEYWORDS_HARAM if k in d or k in n]

def sd(a,b): return a/b if b and b!=0 else 0

def analyze(tk,info,to=None):
    sec=info.get("sector","Inconnu") or "Inconnu"
    ind=info.get("industry","Inconnu") or "Inconnu"
    mc_s=info.get("marketCap",0) or 0
    td=info.get("totalDebt",0) or 0; tc=info.get("totalCash",0) or 0
    si=info.get("shortTermInvestments",0) or 0; li=info.get("longTermInvestments",0) or 0
    rec=info.get("netReceivables",0) or 0
    ii=info.get("interestIncome",0) or 0; ie=info.get("interestExpense",0) or 0
    tr=info.get("totalRevenue",0) or 0; oi=info.get("otherIncome",0) or 0
    px=info.get("currentPrice",0) or info.get("regularMarketPrice",0) or info.get("previousClose",0) or 0
    pe=info.get("trailingPE") or info.get("forwardPE"); fpe=info.get("forwardPE")
    dy=info.get("dividendYield",0) or 0
    roe=info.get("returnOnEquity"); pm=info.get("profitMargins"); om=info.get("operatingMargins")
    gm=info.get("grossMargins"); rg=info.get("revenueGrowth"); eg=info.get("earningsGrowth")
    bt=info.get("beta"); der=info.get("debtToEquity"); cr=info.get("currentRatio")
    fcf=info.get("freeCashflow",0) or 0; ocf=info.get("operatingCashflow",0) or 0
    nm=info.get("shortName") or info.get("longName") or TICKERS.get(tk,tk)
    pb=info.get("priceToBook")

    am=avg_mcap(to) if to else None; qd=q_check(to) if to else None
    mc=am if am and am>0 else mc_s; mt="Moy.12m" if (am and am>0) else "Spot"
    dqs=dq(info,am is not None,qd is not None); kw=ckw(info)

    dd=0;ds=False
    if dy and 0<dy<1: dd=round(dy*100,2)
    if dd>DIV_MAX: ds=True
    if dy and dy>=1: ds=True;dd=0

    def rv(v,m=1): return round(v*m,1) if isinstance(v,(int,float)) and v else "—"

    b={"Ticker":tk,"Nom":nm,"Secteur":sec,"Industrie":ind,"Prix":round(px,2) if px else 0,
        "Cap.(M€)":round(mc/1e6,0) if mc else 0,"Cap.type":mt,
        "PER":rv(pe),"PER Fwd":rv(fpe),"P/B":rv(pb),"Div.(%)":dd,"Div.suspect":ds,
        "ROE(%)":rv(roe,100),"Marge op.(%)":rv(om,100),"Marge nette(%)":rv(pm,100),
        "Marge brute(%)":rv(gm,100),"Croiss.CA(%)":rv(rg,100),"Croiss.BN(%)":rv(eg,100),
        "Beta":rv(bt),"D/E":rv(der),"Current Ratio":round(cr,2) if isinstance(cr,(int,float)) and cr else "—",
        "FCF(M€)":round(fcf/1e6,0) if fcf else "—","OCF(M€)":round(ocf/1e6,0) if ocf else "—",
        "Data":dqs,"Trim.":"Oui" if qd else "Non",
        # New Phase 1 fields
        "Description":info.get("longBusinessSummary","") or "",
        "Employes":info.get("fullTimeEmployees") or "—",
        "Site":info.get("website","") or "",
        "Pays":info.get("country","") or "—",
        "Ville":info.get("city","") or "",
        "52wHigh":round(info.get("fiftyTwoWeekHigh",0) or 0,2),
        "52wLow":round(info.get("fiftyTwoWeekLow",0) or 0,2),
        "AvgVolume":info.get("averageVolume",0) or 0,
        "Keywords":kw,
    }

    def mk(st_,sc,ra,nv,fail_level=""):
        b.update({"Statut":st_,"Score":sc,"Raison":ra,"Dette/Cap(%)":"—","Cash+Inv/Cap(%)":"—",
            "Creances/Cap(%)":"—","Rev.haram(%)":"—","Charges int.(%)":"—","Purif.(%)":"—",
            "Attention":"","Niveaux":nv,"FailLevel":fail_level})
        return b

    if dqs<DQ_MIN: return mk("Donnees insuff.",0,f"Donnees insuffisantes ({dqs}%)","N0","N0")
    if sec in SECTEURS_HARAM: return mk("Haram",0,f"Secteur interdit : {sec}","N1","N1")
    if ind in INDUSTRIES_HARAM: return mk("Haram",0,f"Industrie interdite : {ind}","N2","N2")
    if tk in LISTE_NOIRE: return mk("Haram",0,LISTE_NOIRE[tk],"N3","N3")
    if kw: return mk("Haram",0,f"Activite haram : {', '.join(kw[:4])}","N4","N4")
    if tk in REVENUE_HARAM_MANUAL:
        _,rs,pc=REVENUE_HARAM_MANUAL[tk]
        if pc>SEUIL_REV_HARAM: return mk("Haram",0,f"{rs} (~{pc}% CA)","N4b","N4b")

    rd=round(sd(td,mc)*100,1) if mc>0 else 0
    ct=tc+si+li; rc_=round(sd(ct,mc)*100,1) if mc>0 else 0
    rr=round(sd(rec,mc)*100,1) if mc>0 else 0
    rh=round(sd(abs(ii)+max(0,oi),abs(tr))*100,2) if tr else 0
    ci=round(sd(abs(ie),abs(tr))*100,2) if tr else 0
    pu=round(rh,2) if rh>0 else 0
    att=f"Zone grise : {ind}" if ind in INDUSTRIES_ATTENTION else ""

    fl=[];nv=[]
    if rh>SEUIL_REV_HARAM: fl.append(f"Rev.haram {rh}%>{SEUIL_REV_HARAM}%");nv.append("N5")
    if ci>SEUIL_INT_EXP: fl.append(f"Charges int. {ci}%>{SEUIL_INT_EXP}%");nv.append("N5b")
    if rd>SEUIL_DETTE: fl.append(f"Dette {rd}%>{SEUIL_DETTE}%");nv.append("N6")
    if rc_>SEUIL_CASH: fl.append(f"Cash+Inv {rc_}%>{SEUIL_CASH}%");nv.append("N6")
    if rr>SEUIL_CREANCES: fl.append(f"Creances {rr}%>{SEUIL_CREANCES}%");nv.append("N6")
    if isinstance(der,(int,float)) and der>SEUIL_DE: fl.append(f"D/E {der}>{SEUIL_DE}");nv.append("N6b")
    qw=""
    if qd and mc>0:
        qdr=round(sd(qd["d"],mc)*100,1)
        if qdr>SEUIL_DETTE and rd<=SEUIL_DETTE:
            qw=f"Trim.: dette {qdr}%>seuil"
            att=(att+" | "+qw) if att else qw

    s1=max(0,100-sd(rd,SEUIL_DETTE)*100);s2=max(0,100-sd(rc_,SEUIL_CASH)*100)
    s3=max(0,100-sd(rr,SEUIL_CREANCES)*100)
    s4=max(0,100-sd(rh,SEUIL_REV_HARAM)*100) if SEUIL_REV_HARAM else 100
    s5=max(0,100-sd(ci,SEUIL_INT_EXP)*100) if SEUIL_INT_EXP else 100
    sc=round((s1+s2+s3+s4+s5)/5,0)
    if att: sc=max(0,sc-10)
    if rh>SEUIL_REV_ATTENTION: sc=max(0,sc-5)
    if dqs>=80: sc=min(100,sc+2)
    if am and am>0: sc=min(100,sc+1)
    if qd: sc=min(100,sc+1)

    st_="Non conforme" if fl else "Conforme"
    ra=" | ".join(fl) if fl else ("Tous criteres AAOIFI respectes"+(f" — {att}" if att else ""))
    b.update({"Statut":st_,"Score":sc,"Raison":ra,"Dette/Cap(%)":rd,"Cash+Inv/Cap(%)":rc_,
        "Creances/Cap(%)":rr,"Rev.haram(%)":rh,"Charges int.(%)":ci,"Purif.(%)":pu,
        "Attention":att,"Niveaux":", ".join(set(nv)) if nv else "OK","FailLevel":""})
    return b


# ══════════════════════════════════════════════════════
# UI HELPER — Zoya-style Stock Detail Page
# ══════════════════════════════════════════════════════

def render_stock_detail(r, tc, inf):
    """Render a full Zoya-style compliance report for a single stock."""

    statut = r["Statut"]
    # Determine verdict styling
    if statut == "Conforme":
        sh_cls, vh_cls, vh_icon, vh_label, vh_sub = "sh-ok", "verdict-hero-ok", "✅", T("verdict_halal"), T("verdict_halal_sub")
    elif statut == "Non conforme":
        sh_cls, vh_cls, vh_icon, vh_label, vh_sub = "sh-nc", "verdict-hero-nc", "⚠️", T("verdict_nc"), T("verdict_nc_sub")
    elif statut == "Haram":
        sh_cls, vh_cls, vh_icon, vh_label, vh_sub = "sh-h", "verdict-hero-h", "🚫", T("verdict_haram"), T("verdict_haram_sub")
    else:
        sh_cls, vh_cls, vh_icon, vh_label, vh_sub = "sh-nd", "verdict-hero-nd", "❓", T("verdict_nodata"), T("verdict_nodata_sub")

    # Data quality pill
    dqc = "dq-h" if r["Data"]>=70 else ("dq-m" if r["Data"]>=40 else "dq-l")

    # ── HEADER ──
    price_str = f"{r['Prix']} €" if r['Prix'] else "—"
    st.markdown(f"""
    <div class="stock-header {sh_cls}">
        <div class="sh-top">
            <div class="sh-info">
                <p class="sh-name">{r['Nom']}</p>
                <div class="sh-meta">
                    <span class="sh-meta-pill">{tc}</span>
                    <span class="sh-meta-pill">{r['Secteur']}</span>
                    <span class="sh-meta-pill">{r['Industrie']}</span>
                    <span class="dq-pill {dqc}">{T('data_quality')} {r['Data']}%</span>
                </div>
                <div class="sh-price-row">
                    <span class="sh-price">{price_str}</span>
                    <span class="sh-currency">{r.get('Cap.type','')}</span>
                </div>
            </div>
            <div class="verdict-hero {vh_cls}">
                <div class="vh-icon">{vh_icon}</div>
                <div class="vh-label">{vh_label}</div>
                <div class="vh-sub">{vh_sub}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── BUSINESS ACTIVITY SCREENING ──
    fail_level = r.get("FailLevel", "")
    is_biz_fail = fail_level in ["N1","N2","N3","N4","N4b"]
    biz_badge_cls = "sc-badge-fail" if is_biz_fail else "sc-badge-pass"
    biz_badge_text = T("fail") if is_biz_fail else T("pass")

    if is_biz_fail:
        biz_body = f"<strong>{r['Raison']}</strong>"
    elif statut == "Donnees insuff.":
        biz_badge_cls = "sc-badge-na"
        biz_badge_text = T("na")
        biz_body = r['Raison']
    else:
        biz_body = T("biz_pass")

    # Gray zone warning
    grayzone_html = ""
    if r.get("Attention") and "Zone grise" in r.get("Attention",""):
        ind = r.get("Industrie","")
        grayzone_html = f"""<div style="margin-top:10px;padding:10px 14px;background:var(--honey-bg);border:1px solid rgba(184,134,11,0.15);border-radius:var(--r-sm);">
            <p style="margin:0;font-size:0.75rem;color:var(--honey);">⚠️ {T('biz_grayzone', ind=ind)}</p>
        </div>"""

    st.markdown(f"""
    <div class="screen-card">
        <div class="sc-header">
            <div class="sc-title">
                <span class="sc-title-icon sci-biz">🏢</span>
                {T('sec_business')}
            </div>
            <span class="sc-badge {biz_badge_cls}">{biz_badge_text}</span>
        </div>
        <div class="sc-body">{biz_body}</div>
        {grayzone_html}
    </div>
    """, unsafe_allow_html=True)

    # ── FINANCIAL SCREENING ──
    if statut not in ["Haram", "Donnees insuff."] or (statut == "Non conforme"):
        has_ratios = isinstance(r.get("Dette/Cap(%)"), (int, float))

        if has_ratios:
            # Determine overall financial screening result
            fin_fails = []
            ratios_data = [
                ("Dette/Cap(%)", SEUIL_DETTE, T("fin_debt")),
                ("Cash+Inv/Cap(%)", SEUIL_CASH, T("fin_cash")),
                ("Creances/Cap(%)", SEUIL_CREANCES, T("fin_receivables")),
                ("Rev.haram(%)", SEUIL_REV_HARAM, T("fin_haram_rev")),
                ("Charges int.(%)", SEUIL_INT_EXP, T("fin_interest")),
            ]

            for key, seuil, label in ratios_data:
                v = r.get(key)
                if isinstance(v, (int, float)) and v > seuil:
                    fin_fails.append(label)

            fin_pass = len(fin_fails) == 0
            fin_badge_cls = "sc-badge-pass" if fin_pass else "sc-badge-fail"
            fin_badge_text = T("pass") if fin_pass else T("fail")

            # Build ratio rows
            ratio_rows = ""
            for key, seuil, label in ratios_data:
                v = r.get(key)
                if isinstance(v, (int, float)):
                    pct = min(100, v / seuil * 100)
                    is_ok = v <= seuil
                    fill_color = "var(--sage)" if v <= seuil * 0.6 else ("var(--honey)" if v <= seuil else "var(--coral)")
                    val_color = fill_color
                    badge_cls = "rr-badge-pass" if is_ok else "rr-badge-fail"
                    badge_text = T("pass") if is_ok else T("fail")
                    val_str = f"{v}%"
                else:
                    pct = 0
                    fill_color = "var(--stone)"
                    val_color = "var(--ink-4)"
                    badge_cls = "rr-badge-na"
                    badge_text = T("na")
                    val_str = "—"

                ratio_rows += f"""
                <div class="ratio-row">
                    <div class="rr-info">
                        <div class="rr-name">{label}</div>
                        <div class="rr-threshold">{T('fin_threshold', s=seuil)}</div>
                    </div>
                    <div class="rr-bar-wrap">
                        <div class="rr-bar"><div class="rr-fill" style="width:{pct}%;background:{fill_color};"></div></div>
                    </div>
                    <div class="rr-value" style="color:{val_color};">{val_str}</div>
                    <span class="rr-badge {badge_cls}">{badge_text}</span>
                </div>"""

            # D/E ratio extra
            der_v = r.get("D/E")
            if isinstance(der_v, (int, float)):
                der_pct = min(100, der_v / SEUIL_DE * 100)
                der_ok = der_v <= SEUIL_DE
                der_fill = "var(--sage)" if der_v <= SEUIL_DE * 0.6 else ("var(--honey)" if der_v <= SEUIL_DE else "var(--coral)")
                der_badge_cls = "rr-badge-pass" if der_ok else "rr-badge-fail"
                der_badge_text = T("pass") if der_ok else T("fail")
                ratio_rows += f"""
                <div class="ratio-row">
                    <div class="rr-info">
                        <div class="rr-name">D/E Ratio</div>
                        <div class="rr-threshold">{T('fin_threshold', s=SEUIL_DE)}</div>
                    </div>
                    <div class="rr-bar-wrap">
                        <div class="rr-bar"><div class="rr-fill" style="width:{der_pct}%;background:{der_fill};"></div></div>
                    </div>
                    <div class="rr-value" style="color:{der_fill};">{der_v}</div>
                    <span class="rr-badge {der_badge_cls}">{der_badge_text}</span>
                </div>"""

            st.markdown(f"""
            <div class="screen-card">
                <div class="sc-header">
                    <div class="sc-title">
                        <span class="sc-title-icon sci-fin">📊</span>
                        {T('sec_financial')}
                    </div>
                    <span class="sc-badge {fin_badge_cls}">{fin_badge_text}</span>
                </div>
                {ratio_rows}
            </div>
            """, unsafe_allow_html=True)

    # ── SCORE SHARIA (Circular Gauge) ──
    if r["Score"] > 0:
        sc_val = int(r["Score"])
        deg = round(sc_val / 100 * 360)
        sc_color = "var(--sage)" if sc_val >= 70 else ("var(--honey)" if sc_val >= 40 else "var(--coral)")

        # Breakdown chips
        chips = ""
        if r["Data"] >= 80:
            chips += '<span class="sb-chip sb-bonus">Data ≥80% → +2</span>'
        if r.get("Cap.type") == "Moy.12m":
            chips += '<span class="sb-chip sb-bonus">Cap. moy. 12m → +1</span>'
        if r.get("Trim.") == "Oui":
            chips += '<span class="sb-chip sb-bonus">Trim. dispo → +1</span>'
        if r.get("Attention") and "Zone grise" in r.get("Attention",""):
            chips += '<span class="sb-chip sb-malus">Zone grise → -10</span>'
        rh_val = r.get("Rev.haram(%)")
        if isinstance(rh_val, (int, float)) and rh_val > SEUIL_REV_ATTENTION:
            chips += f'<span class="sb-chip sb-malus">Rev. haram >{SEUIL_REV_ATTENTION}% → -5</span>'

        score_desc_fr = "Moyenne inversée des 5 ratios financiers, avec bonus et malus."
        score_desc_en = "Inverse average of 5 financial ratios, with bonuses and penalties."
        score_desc = score_desc_fr if st.session_state.lang == "fr" else score_desc_en

        st.markdown(f"""
        <div class="score-ring-wrap">
            <div class="score-ring" style="background:conic-gradient({sc_color} 0deg {deg}deg, var(--warm-200) {deg}deg 360deg);">
                <div class="score-ring-inner">
                    <span class="score-ring-val" style="color:{sc_color};">{sc_val}</span>
                    <span class="score-ring-label">/ 100</span>
                </div>
            </div>
            <div class="score-details">
                <p><strong>{T('sec_score')}</strong></p>
                <p>{score_desc}</p>
                <div class="score-breakdown">{chips}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── PURIFICATION ──
    purif = r.get("Purif.(%)")
    if isinstance(purif, (int, float)):
        st.markdown(f'<div class="sdiv"><div class="sdiv-dot d-sage"></div><h3>{T("sec_purification")}</h3></div>', unsafe_allow_html=True)
        div_pct = r.get("Div.(%)", 0)
        est_amount = round(10000 * (div_pct / 100) * (purif / 100), 2) if div_pct and purif else 0

        if purif > 0:
            st.markdown(f"""
            <div class="purif-card">
                <div class="purif-icon">🕌</div>
                <div class="purif-body">
                    <p class="purif-title">{T('sec_purification')}</p>
                    <p class="purif-text">{T('purif_text', pct=purif, div=div_pct, amount=est_amount)}</p>
                </div>
                <div>
                    <p class="purif-pct">{purif}%</p>
                    <p class="purif-pct-label">à purifier</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="callout"><span class="callout-icon">✅</span><p>{T('purif_none')}</p></div>""", unsafe_allow_html=True)

    # ── FINANCIAL METRICS ──
    def fmt_metric(v, suffix=""):
        if v == "—" or v is None:
            return "—"
        return f"{v}{suffix}"

    # Valuation
    st.markdown(f'<div class="sdiv"><div class="sdiv-dot d-sage"></div><h3>{T("sec_valuation")}</h3></div>', unsafe_allow_html=True)
    metrics_val = [
        (T("price"), f"{r['Prix']} €" if r['Prix'] else "—"),
        (T("per"), fmt_metric(r['PER'])),
        (T("per_fwd"), fmt_metric(r['PER Fwd'])),
        (T("pb_ratio"), fmt_metric(r.get('P/B'))),
        (T("cap"), fmt_metric(r.get('Cap.(M€)'))),
        (T("dividend"), fmt_metric(r['Div.(%)'], '%')),
    ]
    mg = '<div class="metric-grid">'
    for label, val in metrics_val:
        mg += f'<div class="m-card"><p class="m-label">{label}</p><p class="m-val">{val}</p></div>'
    mg += '</div>'
    st.markdown(mg, unsafe_allow_html=True)

    # Profitability
    st.markdown(f'<div class="sdiv"><div class="sdiv-dot d-sky"></div><h3>{T("sec_profitability")}</h3></div>', unsafe_allow_html=True)
    metrics_prof = [
        (T("roe"), fmt_metric(r['ROE(%)'], '%')),
        (T("op_margin"), fmt_metric(r['Marge op.(%)'], '%')),
        (T("net_margin"), fmt_metric(r['Marge nette(%)'], '%')),
        (T("gross_margin"), fmt_metric(r['Marge brute(%)'], '%')),
        (T("rev_growth"), fmt_metric(r['Croiss.CA(%)'], '%')),
        (T("earnings_growth"), fmt_metric(r['Croiss.BN(%)'], '%')),
        (T("fcf"), fmt_metric(r.get('FCF(M€)'))),
    ]
    mg = '<div class="metric-grid">'
    for label, val in metrics_prof:
        mg += f'<div class="m-card"><p class="m-label">{label}</p><p class="m-val">{val}</p></div>'
    mg += '</div>'
    st.markdown(mg, unsafe_allow_html=True)

    # Risk
    st.markdown(f'<div class="sdiv"><div class="sdiv-dot d-honey"></div><h3>{T("sec_risk")}</h3></div>', unsafe_allow_html=True)
    w52 = f"{r.get('52wLow',0)} — {r.get('52wHigh',0)}" if r.get('52wLow') and r.get('52wHigh') else "—"
    avg_vol = f"{r.get('AvgVolume',0):,.0f}" if r.get('AvgVolume') else "—"
    metrics_risk = [
        (T("beta"), fmt_metric(r['Beta'])),
        (T("de_ratio"), fmt_metric(r['D/E'])),
        (T("current_ratio"), fmt_metric(r['Current Ratio'])),
        (T("ocf"), fmt_metric(r.get('OCF(M€)'))),
        (T("week52"), w52),
        (T("avg_volume"), avg_vol),
    ]
    mg = '<div class="metric-grid">'
    for label, val in metrics_risk:
        mg += f'<div class="m-card"><p class="m-label">{label}</p><p class="m-val">{val}</p></div>'
    mg += '</div>'
    st.markdown(mg, unsafe_allow_html=True)

    # ── COMPANY INFO ──
    desc = r.get("Description", "")
    if desc or r.get("Employes") != "—" or r.get("Site"):
        st.markdown(f'<div class="sdiv"><div class="sdiv-dot d-stone"></div><h3>{T("sec_company")}</h3></div>', unsafe_allow_html=True)

        site_html = f'<a href="{r["Site"]}" target="_blank">{r["Site"][:40]}...</a>' if r.get("Site") and len(r["Site"]) > 40 else (f'<a href="{r["Site"]}" target="_blank">{r["Site"]}</a>' if r.get("Site") else "—")
        emp_str = f"{r['Employes']:,}" if isinstance(r.get('Employes'), int) else str(r.get('Employes', '—'))
        ville_pays = f"{r.get('Ville', '')}, {r.get('Pays', '')}" if r.get('Ville') else r.get('Pays', '—')

        st.markdown(f"""
        <div class="company-grid">
            <div class="cg-item"><p class="cg-label">{T('sector')}</p><p class="cg-value">{r['Secteur']}</p></div>
            <div class="cg-item"><p class="cg-label">{T('industry')}</p><p class="cg-value">{r['Industrie']}</p></div>
            <div class="cg-item"><p class="cg-label">{T('country')}</p><p class="cg-value">{ville_pays}</p></div>
            <div class="cg-item"><p class="cg-label">{T('employees')}</p><p class="cg-value">{emp_str}</p></div>
            <div class="cg-item"><p class="cg-label">{T('website')}</p><p class="cg-value">{site_html}</p></div>
            <div class="cg-item"><p class="cg-label">{T('cap_type')}</p><p class="cg-value">{r.get('Cap.(M€)',0)} M€ ({r.get('Cap.type','—')})</p></div>
        </div>
        """, unsafe_allow_html=True)

        if desc:
            st.markdown(f'<div class="company-desc">{desc[:1500]}{"..." if len(desc)>1500 else ""}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="company-desc" style="color:var(--ink-4);font-style:italic;">{T("no_desc")}</div>', unsafe_allow_html=True)

    # ── ALERTS ──
    if r.get("Div.suspect"):
        st.warning(T("div_suspect"))
    if r.get("Trim.") == "Oui":
        st.success(T("quarterly_yes"))

    # ── HALAL ALTERNATIVES ──
    if statut in ["Non conforme", "Haram"]:
        st.markdown(f'<div class="sdiv"><div class="sdiv-dot d-sage"></div><h3>{T("sec_alternatives")}</h3></div>', unsafe_allow_html=True)

        # Check if screener results exist in session
        if "screener_results" in st.session_state and st.session_state.screener_results is not None:
            df_cache = st.session_state.screener_results
            same_sector = df_cache[(df_cache["Statut"] == "Conforme") & (df_cache["Secteur"] == r["Secteur"])].head(6)
            if len(same_sector) > 0:
                st.markdown(f'<p style="font-size:0.78rem;color:var(--ink-2);margin:0 0 8px;">{T("alt_text", sec=r["Secteur"])}</p>', unsafe_allow_html=True)
                alt_html = '<div class="alt-grid">'
                for _, alt in same_sector.iterrows():
                    alt_html += f"""<div class="alt-card">
                        <p class="alt-name">{alt['Nom']}</p>
                        <p class="alt-ticker">{alt['Ticker']}</p>
                        <span class="alt-badge">Score {int(alt['Score'])}</span>
                    </div>"""
                alt_html += '</div>'
                st.markdown(alt_html, unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="callout"><span class="callout-icon">💡</span><p>{T("alt_none")}</p></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="callout"><span class="callout-icon">💡</span><p>{T("alt_run_screener")}</p></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# BRAND BAR
# ══════════════════════════════════════════════════════

bc1, bc2 = st.columns([9, 1])
with bc1:
    st.markdown(f"""
    <div class="brand">
        <div class="brand-left">
            <div class="brand-mark">☪️</div>
            <span class="brand-text">Halal <em>Quant</em></span>
        </div>
        <div class="brand-right">
            <span class="brand-pill">{T('brand_actions', n=len(TICKERS))}</span>
            <span class="brand-pill">{T('brand_norm')}</span>
            <span class="brand-pill">{T('brand_by')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
with bc2:
    lang_label = "🇬🇧 EN" if st.session_state.lang == "fr" else "🇫🇷 FR"
    if st.button(lang_label, key="lang_toggle"):
        st.session_state.lang = "en" if st.session_state.lang == "fr" else "fr"
        st.rerun()

# ══════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════

t1,t2,t3,t4,t5,t6,t7 = st.tabs([
    T("tab_screener"), T("tab_search"), T("tab_portfolio"),
    T("tab_benchmark"), T("tab_alerts"), T("tab_etf"), T("tab_method")
])

# ══════════════════════════════════════════════════════
# TAB 1 — SCREENER
# ══════════════════════════════════════════════════════

with t1:
    if st.button(T("screener_launch"), type="primary", use_container_width=True):
        pg=st.progress(0); sx=st.empty(); res=[]; err=0
        for i,(tk,nm) in enumerate(TICKERS.items()):
            pg.progress((i+1)/len(TICKERS))
            sx.text(f"{'Analyse de' if st.session_state.lang=='fr' else 'Analyzing'} {nm} ({tk}) — {i+1}/{len(TICKERS)}")
            try:
                to=yf.Ticker(tk); inf=to.info
                if not inf or inf.get("quoteType")=="NONE": raise ValueError("No data")
                res.append(analyze(tk,inf,to))
            except Exception as e:
                err+=1
                eb={k:"—" for k in ["PER","PER Fwd","P/B","ROE(%)","Marge op.(%)","Marge nette(%)","Marge brute(%)",
                    "Croiss.CA(%)","Croiss.BN(%)","Beta","D/E","Current Ratio","FCF(M€)","OCF(M€)",
                    "Dette/Cap(%)","Cash+Inv/Cap(%)","Creances/Cap(%)","Rev.haram(%)","Charges int.(%)","Purif.(%)"]}
                eb.update({"Ticker":tk,"Nom":nm,"Statut":"Donnees insuff.","Score":0,
                    "Raison":f"Erreur: {str(e)[:40]}","Prix":0,"Div.(%)":0,"Div.suspect":False,
                    "Cap.(M€)":0,"Cap.type":"—","Secteur":"Inconnu","Industrie":"Inconnu",
                    "Attention":"","Data":0,"Niveaux":"Erreur","Trim.":"Non","FailLevel":"",
                    "Description":"","Employes":"—","Site":"","Pays":"—","Ville":"",
                    "52wHigh":0,"52wLow":0,"AvgVolume":0,"Keywords":[]})
                res.append(eb)
            if (i+1)%12==0: time.sleep(1.5)
        pg.empty(); sx.empty()

        df=pd.DataFrame(res)
        # Cache results for alternatives feature
        st.session_state.screener_results = df

        co=df[df["Statut"]=="Conforme"]; nc=df[df["Statut"]=="Non conforme"]
        ha=df[df["Statut"]=="Haram"]; nd=df[df["Statut"]=="Donnees insuff."]
        gr=co[co["Attention"]!=""]

        # KPIs
        st.markdown(f"""<div class="kpis">
            <div class="kpi k-sky"><div class="kv">{len(df)}</div><div class="kl">{T('analyzed')}</div></div>
            <div class="kpi k-sage"><div class="kv">{len(co)}</div><div class="kl">{T('conformes')}</div></div>
            <div class="kpi k-honey"><div class="kv">{len(nc)}</div><div class="kl">{T('non_conformes')}</div></div>
            <div class="kpi k-coral"><div class="kv">{len(ha)}</div><div class="kl">{T('haram')}</div></div>
            <div class="kpi k-stone"><div class="kv">{len(nd)}</div><div class="kl">{T('data_insuff')}</div></div>
            <div class="kpi"><div class="kv" style="color:var(--honey);">{len(gr)}</div><div class="kl">{T('gray_zones')}</div></div>
        </div>""", unsafe_allow_html=True)

        # Conformes
        st.markdown(f'<div class="sdiv"><div class="sdiv-dot d-sage"></div><h3>{T("compliant_stocks")}</h3><span class="sdiv-cnt">{len(co)}</span></div>', unsafe_allow_html=True)
        if len(co)>0:
            st.dataframe(co.sort_values("Score",ascending=False)[["Nom","Score","Data","Trim.","Prix","Cap.(M€)","Cap.type",
                "PER","Div.(%)","ROE(%)","Marge op.(%)","Marge nette(%)","Beta","D/E","Current Ratio","FCF(M€)",
                "Dette/Cap(%)","Cash+Inv/Cap(%)","Creances/Cap(%)","Charges int.(%)","Purif.(%)","Secteur","Attention"]],
                use_container_width=True, hide_index=True, height=min(600,50+len(co)*35))
        else:
            st.info("Aucune action conforme trouvee." if st.session_state.lang=="fr" else "No compliant stocks found.")

        # Non conformes
        st.markdown(f'<div class="sdiv"><div class="sdiv-dot d-honey"></div><h3>{T("non_conformes")}</h3><span class="sdiv-cnt">{len(nc)}</span></div>', unsafe_allow_html=True)
        if len(nc)>0:
            st.dataframe(nc[["Nom","Raison","Prix","Cap.(M€)","Dette/Cap(%)","Cash+Inv/Cap(%)","Creances/Cap(%)","Rev.haram(%)","Charges int.(%)","D/E","Secteur","Niveaux"]],
                use_container_width=True, hide_index=True)

        # Haram
        st.markdown(f'<div class="sdiv"><div class="sdiv-dot d-coral"></div><h3>{T("haram")}</h3><span class="sdiv-cnt">{len(ha)}</span></div>', unsafe_allow_html=True)
        if len(ha)>0:
            st.dataframe(ha[["Nom","Raison","Secteur","Industrie","Niveaux"]], use_container_width=True, hide_index=True)

        # Data insuff.
        if len(nd)>0:
            st.markdown(f'<div class="sdiv"><div class="sdiv-dot d-stone"></div><h3>{T("data_insuff")}</h3><span class="sdiv-cnt">{len(nd)}</span></div>', unsafe_allow_html=True)
            st.dataframe(nd[["Nom","Ticker","Raison","Data"]], use_container_width=True, hide_index=True)

        # Downloads
        st.markdown("---")
        c1,c2,c3 = st.columns(3)
        with c1: st.download_button(T("download_csv"), df.to_csv(index=False).encode("utf-8"), f"halal_quant_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv", use_container_width=True)
        with c2: st.download_button(T("download_conformes"), co.to_csv(index=False).encode("utf-8"), f"hq_conformes_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv", use_container_width=True)
        with c3: st.download_button(T("download_json"), df.to_json(orient="records",indent=2).encode("utf-8"), f"hq_rapport_{datetime.now().strftime('%Y%m%d')}.json", "application/json", use_container_width=True)

    else:
        st.markdown(f"""
        <div class="hero-empty">
            <div class="hero-icon">☪️</div>
            <p class="hero-title">Screener Sharia — Euronext Paris</p>
            <p class="hero-sub">{T('screener_desc', n=len(TICKERS))}<br>{T('screener_sub')}</p>
            <div class="hero-chips">
                <span class="hero-chip">10 {'niveaux' if st.session_state.lang=='fr' else 'levels'} AAOIFI</span>
                <span class="hero-chip">Cap. {'moy.' if st.session_state.lang=='fr' else 'avg.'} 12 {'mois' if st.session_state.lang=='fr' else 'mo'}</span>
                <span class="hero-chip">{'Vérif. trimestrielle' if st.session_state.lang=='fr' else 'Quarterly check'}</span>
                <span class="hero-chip">Export CSV / JSON</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# TAB 2 — RECHERCHE (PHASE 1 — ZOYA-STYLE REDESIGN)
# ══════════════════════════════════════════════════════

with t2:
    st.markdown(f'<p style="font-size:0.82rem;color:var(--ink-3);margin:0 0 8px;">{T("search_desc")}</p>', unsafe_allow_html=True)
    ti = st.text_input("Ticker", placeholder=T("search_placeholder"), label_visibility="collapsed")

    if ti:
        tc = ti.strip().upper()
        with st.spinner(T("search_analyzing", tc=tc)):
            try:
                to = yf.Ticker(tc); inf = to.info
                if not inf or inf.get("quoteType") == "NONE":
                    st.error(T("search_nodata", tc=tc))
                else:
                    r = analyze(tc, inf, to)
                    render_stock_detail(r, tc, inf)
            except Exception as e:
                st.error(T("search_error", e=str(e)))


# ══════════════════════════════════════════════════════
# TAB 3 — PORTEFEUILLE HALAL
# ══════════════════════════════════════════════════════

with t3:
    st.markdown(f'<p style="font-size:0.85rem;color:var(--ink-2);line-height:1.6;margin:0 0 14px;">{T("ptf_desc")}</p>', unsafe_allow_html=True)

    pc1, pc2, pc3 = st.columns(3)
    with pc1:
        montant = st.number_input(T("ptf_amount"), min_value=500, max_value=1000000, value=10000, step=500)
    with pc2:
        profil_options = [T("ptf_prudent"), T("ptf_balanced"), T("ptf_dynamic")]
        profil = st.selectbox(T("ptf_profile"), profil_options)
    with pc3:
        strat_options = [T("ptf_score"), T("ptf_equal"), T("ptf_cap")]
        strategie = st.selectbox(T("ptf_strategy"), strat_options)

    with st.expander(T("ptf_advanced")):
        ac1, ac2, ac3 = st.columns(3)
        with ac1: max_actions = st.slider(T("ptf_max_stocks"), 5, 30, 15)
        with ac2: max_secteur = st.slider(T("ptf_max_sector"), 10, 50, 30)
        with ac3: score_min = st.slider(T("ptf_min_score"), 50, 95, 70)

    if st.button(T("ptf_build"), type="primary", use_container_width=True):
        pg = st.progress(0); sx = st.empty(); res = []
        for i, (tk, nm) in enumerate(TICKERS.items()):
            pg.progress((i + 1) / len(TICKERS))
            sx.text(f"{'Analyse de' if st.session_state.lang=='fr' else 'Analyzing'} {nm} ({tk}) — {i+1}/{len(TICKERS)}")
            try:
                to = yf.Ticker(tk); inf = to.info
                if not inf or inf.get("quoteType") == "NONE": raise ValueError("No data")
                res.append(analyze(tk, inf, to))
            except: pass
            if (i + 1) % 12 == 0: time.sleep(1.5)
        pg.empty(); sx.empty()

        df_all = pd.DataFrame(res)
        if "Statut" in df_all.columns and len(df_all) > 0:
            conformes = df_all[(df_all["Statut"] == "Conforme") & (df_all["Score"] >= score_min)].copy()
        else:
            conformes = pd.DataFrame()

        if len(conformes) == 0:
            st.warning(f"{'Aucune action conforme avec un score >=' if st.session_state.lang=='fr' else 'No compliant stock with score >='} {score_min}.")
        else:
            # Profile filter
            profil_key = profil_options.index(profil)
            if profil_key == 0:  # Prudent
                conformes = conformes[conformes["Beta"].apply(lambda x: isinstance(x, (int, float)) and x <= 1.0 or not isinstance(x, (int, float)))]
                profil_desc = "Faible volatilite, entreprises stables" if st.session_state.lang=="fr" else "Low volatility, stable companies"
                profil_emoji = "🛡️"
            elif profil_key == 2:  # Dynamic
                profil_desc = "Forte croissance, volatilite acceptee" if st.session_state.lang=="fr" else "High growth, higher volatility accepted"
                profil_emoji = "🚀"
            else:
                profil_desc = "Equilibre stabilite/croissance" if st.session_state.lang=="fr" else "Balance of stability and growth"
                profil_emoji = "⚖️"

            # Sort
            strat_key = strat_options.index(strategie)
            if strat_key == 0:
                conformes = conformes.sort_values("Score", ascending=False)
            elif strat_key == 2:
                conformes = conformes.sort_values("Cap.(M€)", ascending=False)
            else:
                conformes = conformes.sample(frac=1, random_state=42)

            # Select with sector diversification
            max_per_sector = max(1, int(max_actions * max_secteur / 100))
            selected = []; sector_count = {}
            for _, row in conformes.iterrows():
                if len(selected) >= max_actions: break
                sec = row["Secteur"]
                if sector_count.get(sec, 0) < max_per_sector:
                    selected.append(row)
                    sector_count[sec] = sector_count.get(sec, 0) + 1

            if len(selected) == 0:
                st.warning("Impossible de construire un portefeuille." if st.session_state.lang=="fr" else "Cannot build portfolio with these constraints.")
            else:
                ptf = pd.DataFrame(selected)
                if strat_key == 0:
                    total_score = ptf["Score"].sum()
                    ptf["Poids (%)"] = (ptf["Score"] / total_score * 100).round(1)
                elif strat_key == 2:
                    caps = ptf["Cap.(M€)"].apply(lambda x: x if isinstance(x, (int, float)) and x > 0 else 1)
                    ptf["Poids (%)"] = (caps / caps.sum() * 100).round(1)
                else:
                    ptf["Poids (%)"] = round(100 / len(ptf), 1)

                ptf["Montant (€)"] = (ptf["Poids (%)"] / 100 * montant).round(0).astype(int)
                purif_vals = ptf["Purif.(%)"].apply(lambda x: x if isinstance(x, (int, float)) else 0)
                purif_moy = round(purif_vals.mean(), 2)
                score_moy = round(ptf["Score"].mean(), 0)
                nb_secteurs = ptf["Secteur"].nunique()
                betas = ptf["Beta"].apply(lambda x: x if isinstance(x, (int, float)) else None).dropna()
                beta_moy = round(betas.mean(), 2) if len(betas) > 0 else "—"

                st.markdown(f"""<div class="kpis">
                    <div class="kpi k-sage"><div class="kv">{len(ptf)}</div><div class="kl">Actions</div></div>
                    <div class="kpi k-sage"><div class="kv">{int(score_moy)}</div><div class="kl">Score {'moyen' if st.session_state.lang=='fr' else 'avg'}</div></div>
                    <div class="kpi k-sky"><div class="kv">{nb_secteurs}</div><div class="kl">{'Secteurs' if st.session_state.lang=='fr' else 'Sectors'}</div></div>
                    <div class="kpi"><div class="kv" style="color:var(--ink);">{beta_moy}</div><div class="kl">{'Bêta moyen' if st.session_state.lang=='fr' else 'Avg Beta'}</div></div>
                    <div class="kpi"><div class="kv" style="color:var(--ink);">{montant:,}€</div><div class="kl">{'Investissement' if st.session_state.lang=='fr' else 'Investment'}</div></div>
                    <div class="kpi k-honey"><div class="kv">{purif_moy}%</div><div class="kl">Purif. {'moy.' if st.session_state.lang=='fr' else 'avg.'}</div></div>
                </div>""", unsafe_allow_html=True)

                st.markdown(f"""<div class="callout"><span class="callout-icon">{profil_emoji}</span>
                    <p><strong>{'Profil' if st.session_state.lang=='fr' else 'Profile'} {profil}</strong> — {profil_desc}.</p>
                </div>""", unsafe_allow_html=True)

                display_ptf = ptf[["Nom","Ticker","Score","Poids (%)","Montant (€)","Prix",
                    "Cap.(M€)","PER","ROE(%)","Beta","Div.(%)","Purif.(%)","Dette/Cap(%)","Secteur"]].copy()
                display_ptf = display_ptf.sort_values("Poids (%)", ascending=False)
                st.dataframe(display_ptf, use_container_width=True, hide_index=True, height=min(600, 50 + len(ptf) * 35))

                # Sector breakdown
                sector_alloc = ptf.groupby("Secteur").agg(
                    Actions=("Nom", "count"), Poids_total=("Poids (%)", "sum"),
                    Montant_total=("Montant (€)", "sum"), Score_moy=("Score", "mean")
                ).round(1).sort_values("Poids_total", ascending=False)
                sector_alloc.columns = ["Nb actions", "Poids total (%)", "Montant (€)", "Score moyen"]
                st.dataframe(sector_alloc, use_container_width=True)

                if purif_moy > 0:
                    div_total = ptf.apply(lambda r: r["Montant (€)"] * r["Div.(%)"] / 100 if isinstance(r["Div.(%)"], (int, float)) and r["Div.(%)"] > 0 else 0, axis=1).sum()
                    purif_amount = round(div_total * purif_moy / 100, 2)
                    st.markdown(f"""<div class="callout"><span class="callout-icon">🕌</span>
                        <p><strong>{'Purification estimée :' if st.session_state.lang=='fr' else 'Estimated purification:'}</strong> ~{purif_amount}€ ({purif_moy}%)</p>
                    </div>""", unsafe_allow_html=True)

                st.markdown(f"""<div class="callout"><span class="callout-icon">💡</span>
                    <p><strong>{'Optimisation fiscale :' if st.session_state.lang=='fr' else 'Tax optimization:'}</strong> {'Toutes ces actions sont éligibles PEA. Après 5 ans, vos plus-values sont exonérées d\'impôt sur le revenu.' if st.session_state.lang=='fr' else 'All these stocks are PEA-eligible. After 5 years, capital gains are income-tax-free.'}</p>
                </div>""", unsafe_allow_html=True)

                st.markdown("---")
                dc1, dc2 = st.columns(2)
                with dc1:
                    st.download_button("📥  CSV", display_ptf.to_csv(index=False).encode("utf-8"),
                        f"portefeuille_halal_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv", use_container_width=True)
                with dc2:
                    st.download_button("📥  JSON", display_ptf.to_json(orient="records", indent=2).encode("utf-8"),
                        f"portefeuille_halal_{datetime.now().strftime('%Y%m%d')}.json", "application/json", use_container_width=True)

    else:
        st.markdown(f"""<div class="hero-empty" style="padding:2.5rem;">
            <div class="hero-icon">💼</div>
            <p class="hero-title">{'Constructeur de portefeuille halal' if st.session_state.lang=='fr' else 'Halal Portfolio Builder'}</p>
            <p class="hero-sub">{'Sélectionnez votre profil de risque et laissez l\'algorithme construire un portefeuille diversifié.' if st.session_state.lang=='fr' else 'Select your risk profile and let the algorithm build a diversified portfolio.'}</p>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# TAB 4 — BENCHMARK
# ══════════════════════════════════════════════════════

with t4:
    st.markdown(f"""<p style="font-size:0.85rem;color:var(--ink-2);line-height:1.6;margin:0 0 14px;">
        {'Comparez la performance d\'un portefeuille halal Euronext face à l\'ETF <strong>iShares MSCI World Islamic</strong> (ISWD.L).' if st.session_state.lang=='fr' else 'Compare the performance of a halal Euronext portfolio against the <strong>iShares MSCI World Islamic</strong> ETF (ISWD.L).'}
    </p>""", unsafe_allow_html=True)

    bc1, bc2, bc3 = st.columns(3)
    with bc1:
        bench_period = st.selectbox("Periode" if st.session_state.lang=="fr" else "Period", ["6mo","1y","2y"], index=1,
            format_func=lambda x: {"6mo":"6 mois" if st.session_state.lang=="fr" else "6 months","1y":"1 an" if st.session_state.lang=="fr" else "1 year","2y":"2 ans" if st.session_state.lang=="fr" else "2 years"}[x])
    with bc2:
        bench_top = st.slider("Top N" + (" actions conformes" if st.session_state.lang=="fr" else " compliant stocks"), 5, 25, 10)
    with bc3:
        bench_weight = st.selectbox("Ponderation" if st.session_state.lang=="fr" else "Weighting",
            ["Equiponderation" if st.session_state.lang=="fr" else "Equal Weight", "Score Sharia"])

    if st.button("Lancer le benchmark" if st.session_state.lang=="fr" else "Run Benchmark", type="primary", use_container_width=True):
        pg = st.progress(0); sx = st.empty()
        sx.text("Etape 1/3 — Analyse..." if st.session_state.lang=="fr" else "Step 1/3 — Analyzing...")
        res = []
        for i, (tk, nm) in enumerate(TICKERS.items()):
            pg.progress((i + 1) / len(TICKERS) * 0.5)
            try:
                to = yf.Ticker(tk); inf = to.info
                if not inf or inf.get("quoteType") == "NONE": raise ValueError("No data")
                res.append(analyze(tk, inf, to))
            except: pass
            if (i + 1) % 12 == 0: time.sleep(1.5)

        df_all = pd.DataFrame(res)
        if "Statut" in df_all.columns and len(df_all) > 0:
            conformes = df_all[df_all["Statut"] == "Conforme"].sort_values("Score", ascending=False).head(bench_top)
        else:
            conformes = pd.DataFrame()

        if len(conformes) < 3:
            pg.empty(); sx.empty()
            st.warning("Pas assez d'actions conformes." if st.session_state.lang=="fr" else "Not enough compliant stocks.")
        else:
            sx.text("Etape 2/3 — Historiques..." if st.session_state.lang=="fr" else "Step 2/3 — Historical data...")
            pg.progress(0.55)
            try:
                etf_hist = yf.Ticker("ISWD.L").history(period=bench_period)
                if len(etf_hist) < 10: raise ValueError("Not enough ETF data")
                etf_returns = etf_hist["Close"].pct_change().dropna()
                etf_cumul = (1 + etf_returns).cumprod(); etf_ok = True
            except: etf_ok = False

            sx.text("Etape 3/3 — Calcul..." if st.session_state.lang=="fr" else "Step 3/3 — Computing...")
            pg.progress(0.7)
            tickers_conf = conformes["Ticker"].tolist()
            scores_conf = conformes.set_index("Ticker")["Score"].to_dict()
            stock_returns = {}
            for j, tk in enumerate(tickers_conf):
                pg.progress(0.7 + 0.3 * (j + 1) / len(tickers_conf))
                try:
                    h = yf.Ticker(tk).history(period=bench_period)
                    if len(h) > 10: stock_returns[tk] = h["Close"].pct_change().dropna()
                except: pass
                if (j + 1) % 5 == 0: time.sleep(1)
            pg.empty(); sx.empty()

            if len(stock_returns) < 3:
                st.warning("Pas assez de données historiques." if st.session_state.lang=="fr" else "Not enough historical data.")
            else:
                returns_df = pd.DataFrame(stock_returns).dropna(how="all")
                if "Score" in bench_weight:
                    total_s = sum(scores_conf.get(tk, 50) for tk in returns_df.columns)
                    weights = {tk: scores_conf.get(tk, 50) / total_s for tk in returns_df.columns}
                else:
                    n = len(returns_df.columns)
                    weights = {tk: 1/n for tk in returns_df.columns}

                ptf_daily = sum(returns_df[tk].fillna(0) * weights[tk] for tk in returns_df.columns)
                ptf_cumul = (1 + ptf_daily).cumprod()

                if etf_ok:
                    common_dates = ptf_cumul.index.intersection(etf_cumul.index)
                    if len(common_dates) > 10:
                        ptf_aligned = ptf_cumul.loc[common_dates]
                        etf_aligned = etf_cumul.loc[common_dates]
                    else: etf_ok = False

                ann_factor = 252
                ptf_total_return = round((ptf_cumul.iloc[-1] - 1) * 100, 2)
                ptf_vol = round(ptf_daily.std() * np.sqrt(ann_factor) * 100, 2)
                ptf_sharpe = round((ptf_daily.mean() / ptf_daily.std()) * np.sqrt(ann_factor), 2) if ptf_daily.std() > 0 else 0
                ptf_max_dd = round((ptf_cumul / ptf_cumul.cummax() - 1).min() * 100, 2)

                if etf_ok:
                    etf_total_return = round((etf_cumul.iloc[-1] - 1) * 100, 2)
                    etf_vol = round(etf_returns.std() * np.sqrt(ann_factor) * 100, 2)
                    etf_sharpe = round((etf_returns.mean() / etf_returns.std()) * np.sqrt(ann_factor), 2) if etf_returns.std() > 0 else 0
                    etf_max_dd = round((etf_cumul / etf_cumul.cummax() - 1).min() * 100, 2)
                else:
                    etf_total_return="—";etf_vol="—";etf_sharpe="—";etf_max_dd="—"

                ptf_color = "var(--sage)" if ptf_total_return > 0 else "var(--coral)"
                etf_color = "var(--sage)" if etf_ok and etf_total_return > 0 else "var(--coral)" if etf_ok else "var(--stone)"

                st.markdown(f"""<div class="kpis">
                    <div class="kpi k-sage"><div class="kv">{len(stock_returns)}</div><div class="kl">Actions</div></div>
                    <div class="kpi"><div class="kv" style="color:{ptf_color};">{ptf_total_return:+}%</div><div class="kl">Halal Quant</div></div>
                    <div class="kpi"><div class="kv" style="color:{etf_color};">{f"{etf_total_return:+}%" if etf_ok else "—"}</div><div class="kl">MSCI Islamic</div></div>
                    <div class="kpi"><div class="kv" style="color:var(--ink);">{ptf_vol}%</div><div class="kl">{'Vol.' if st.session_state.lang=='fr' else 'Vol.'}</div></div>
                    <div class="kpi"><div class="kv" style="color:var(--ink);">{ptf_sharpe}</div><div class="kl">Sharpe</div></div>
                    <div class="kpi k-coral"><div class="kv">{ptf_max_dd}%</div><div class="kl">Max DD</div></div>
                </div>""", unsafe_allow_html=True)

                chart_data = pd.DataFrame({"Halal Quant": ptf_cumul})
                if etf_ok: chart_data["MSCI World Islamic"] = etf_aligned
                chart_data = chart_data.dropna()
                for col in chart_data.columns:
                    chart_data[col] = chart_data[col] / chart_data[col].iloc[0] * 100
                st.line_chart(chart_data, use_container_width=True, height=400)

                st.download_button("📥  CSV", pd.DataFrame([{"Metric":k,"Value":v} for k,v in {
                    "Perf Halal Quant":f"{ptf_total_return}%","Vol":f"{ptf_vol}%","Sharpe":ptf_sharpe,"Max DD":f"{ptf_max_dd}%"
                }.items()]).to_csv(index=False).encode("utf-8"), f"benchmark_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")

    else:
        st.markdown(f"""<div class="hero-empty" style="padding:2.5rem;">
            <div class="hero-icon">⚡</div>
            <p class="hero-title">Benchmark vs MSCI World Islamic</p>
            <p class="hero-sub">{'Comparez la performance historique d\'un portefeuille halal Euronext face au MSCI World Islamic.' if st.session_state.lang=='fr' else 'Compare historical performance of a halal Euronext portfolio vs MSCI World Islamic.'}</p>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# TAB 5 — ALERTES DE CONFORMITE
# ══════════════════════════════════════════════════════

with t5:
    st.markdown(f"""<p style="font-size:0.85rem;color:var(--ink-2);line-height:1.6;margin:0 0 14px;">
        {'Détectez les changements de conformité Sharia entre deux analyses.' if st.session_state.lang=='fr' else 'Detect Shariah compliance status changes between two analyses.'}
    </p>""", unsafe_allow_html=True)

    st.markdown(f'<div class="sdiv"><div class="sdiv-dot d-sage"></div><h3>{"Étape 1 — Importer les résultats précédents" if st.session_state.lang=="fr" else "Step 1 — Import previous results"}</h3></div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Import CSV/JSON", type=["csv", "json"], label_visibility="collapsed")

    prev_df = None
    if uploaded:
        try:
            if uploaded.name.endswith(".csv"): prev_df = pd.read_csv(uploaded)
            else: prev_df = pd.DataFrame(json.loads(uploaded.read().decode("utf-8")))
            if "Statut" in prev_df.columns and "Nom" in prev_df.columns:
                st.success(f"{'Fichier chargé :' if st.session_state.lang=='fr' else 'File loaded:'} {len(prev_df)} actions — {uploaded.name}")
            else:
                st.error("Fichier invalide." if st.session_state.lang=="fr" else "Invalid file.")
                prev_df = None
        except Exception as e:
            st.error(f"Erreur : {e}"); prev_df = None

    st.markdown(f'<div class="sdiv"><div class="sdiv-dot d-honey"></div><h3>{"Étape 2 — Nouvelle analyse" if st.session_state.lang=="fr" else "Step 2 — New analysis"}</h3></div>', unsafe_allow_html=True)

    if st.button("Analyser et comparer" if st.session_state.lang=="fr" else "Analyze & Compare", type="primary", use_container_width=True):
        pg = st.progress(0); sx = st.empty(); res = []
        for i, (tk, nm) in enumerate(TICKERS.items()):
            pg.progress((i + 1) / len(TICKERS))
            sx.text(f"{'Analyse de' if st.session_state.lang=='fr' else 'Analyzing'} {nm} ({tk}) — {i+1}/{len(TICKERS)}")
            try:
                to = yf.Ticker(tk); inf = to.info
                if not inf or inf.get("quoteType") == "NONE": raise ValueError("No data")
                res.append(analyze(tk, inf, to))
            except: pass
            if (i + 1) % 12 == 0: time.sleep(1.5)
        pg.empty(); sx.empty()

        new_df = pd.DataFrame(res)
        if "Statut" not in new_df.columns or len(new_df) == 0:
            st.error("Impossible de récupérer les données." if st.session_state.lang=="fr" else "Could not retrieve data.")
        else:
            n_conf = len(new_df[new_df["Statut"]=="Conforme"])
            n_nc = len(new_df[new_df["Statut"]=="Non conforme"])
            n_h = len(new_df[new_df["Statut"]=="Haram"])
            n_nd = len(new_df[new_df["Statut"]=="Donnees insuff."])

            st.markdown(f"""<div class="kpis">
                <div class="kpi k-sage"><div class="kv">{n_conf}</div><div class="kl">{T('conformes')}</div></div>
                <div class="kpi k-honey"><div class="kv">{n_nc}</div><div class="kl">{T('non_conformes')}</div></div>
                <div class="kpi k-coral"><div class="kv">{n_h}</div><div class="kl">{T('haram')}</div></div>
                <div class="kpi k-stone"><div class="kv">{n_nd}</div><div class="kl">{T('data_insuff')}</div></div>
            </div>""", unsafe_allow_html=True)

            if prev_df is not None:
                key_col = "Ticker" if "Ticker" in prev_df.columns and "Ticker" in new_df.columns else "Nom"
                prev_map = dict(zip(prev_df[key_col], prev_df["Statut"]))
                new_map = dict(zip(new_df[key_col], new_df["Statut"]))
                changes = []
                for key in set(prev_map.keys()) & set(new_map.keys()):
                    old_s = prev_map[key]; new_s = new_map[key]
                    if old_s != new_s:
                        nom = new_df[new_df[key_col]==key]["Nom"].values[0] if "Nom" in new_df.columns else key
                        changes.append({"Action":nom,"Ticker":key if key_col=="Ticker" else "—",
                            "Ancien":old_s,"Nouveau":new_s,
                            "Alerte":"⬆️" if new_s=="Conforme" else ("⬇️" if old_s=="Conforme" else "🔄")})
                if changes:
                    st.dataframe(pd.DataFrame(changes), use_container_width=True, hide_index=True)
                else:
                    st.markdown(f"""<div class="callout"><span class="callout-icon">✅</span><p><strong>{'Aucun changement détecté.' if st.session_state.lang=='fr' else 'No changes detected.'}</strong></p></div>""", unsafe_allow_html=True)

            st.markdown("---")
            st.download_button("📥  CSV", new_df.to_csv(index=False).encode("utf-8"),
                f"snapshot_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv", use_container_width=True)
    else:
        st.markdown(f"""<div class="hero-empty" style="padding:2.5rem;">
            <div class="hero-icon">🔔</div>
            <p class="hero-title">{'Alertes de conformité' if st.session_state.lang=='fr' else 'Compliance Alerts'}</p>
            <p class="hero-sub">{'Importez vos résultats précédents et détectez les changements de statut.' if st.session_state.lang=='fr' else 'Import previous results and detect status changes.'}</p>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# TAB 6 — ETF ISLAMIQUES
# ══════════════════════════════════════════════════════

with t6:
    st.markdown(f'<p style="font-size:0.82rem;color:var(--ink-3);margin:0 0 10px;">{"Comparez les principaux ETF conformes Sharia." if st.session_state.lang=="fr" else "Compare the main Shariah-compliant ETFs."}</p>', unsafe_allow_html=True)
    cf1,cf2,cf3 = st.columns(3)
    with cf1: zf=st.multiselect("Zone" if st.session_state.lang=="en" else "Zone géographique", sorted(set(e["z"] for e in ETF_ISL.values())), default=sorted(set(e["z"] for e in ETF_ISL.values())))
    with cf2: nf=st.multiselect("Norme Sharia" if st.session_state.lang=="fr" else "Shariah Standard", sorted(set(e["no"] for e in ETF_ISL.values())), default=sorted(set(e["no"] for e in ETF_ISL.values())))
    with cf3: fm=st.slider("Frais max (%)" if st.session_state.lang=="fr" else "Max fee (%)", 0.0, 1.0, 0.70, 0.05)

    if st.button("Analyser les ETF" if st.session_state.lang=="fr" else "Analyze ETFs", type="primary", use_container_width=True):
        pg=st.progress(0); sx=st.empty(); rs=[]
        ef={k:v for k,v in ETF_ISL.items() if v["z"] in zf and v["no"] in nf and v["f"]<=fm}
        for i,(t_,m) in enumerate(ef.items()):
            pg.progress((i+1)/max(1,len(ef))); sx.text(f"{'Analyse de' if st.session_state.lang=='fr' else 'Analyzing'} {m['n']}...")
            try:
                et=yf.Ticker(t_); inf=et.info; h=et.history(period="1y")
                px=inf.get("regularMarketPrice") or inf.get("previousClose") or 0
                au=inf.get("totalAssets",0) or 0; dy_=inf.get("yield",0) or 0
                p1=round((h["Close"].iloc[-1]-h["Close"].iloc[0])/h["Close"].iloc[0]*100,2) if len(h)>1 and h["Close"].iloc[0]>0 else 0
                vo=round(h["Close"].pct_change().dropna().std()*(252**0.5)*100,2) if len(h)>20 else 0
                rs.append({"Nom":m["n"],"Ticker":t_,"Emetteur":m["e"],"Zone":m["z"],"Norme":m["no"],
                    "Frais(%)":m["f"],"Prix":round(px,2) if px else "—","AUM(M$)":round(au/1e6,0) if au else "—",
                    "Perf.1an(%)":p1,"Vol.(%)":vo,"Div.(%)":round(dy_*100,2) if dy_ and dy_<1 else 0,"Domicile":m["d"],"Desc":m["ds"]})
            except:
                rs.append({"Nom":m["n"],"Ticker":t_,"Emetteur":m["e"],"Zone":m["z"],"Norme":m["no"],
                    "Frais(%)":m["f"],"Prix":"—","AUM(M$)":"—","Perf.1an(%)":"—","Vol.(%)":"—","Div.(%)":"—","Domicile":m["d"],"Desc":m["ds"]})
        pg.empty(); sx.empty()
        de=pd.DataFrame(rs)

        st.markdown(f"""<div class="kpis">
            <div class="kpi k-sky"><div class="kv">{len(de)}</div><div class="kl">ETF</div></div>
            <div class="kpi k-sage"><div class="kv">{len(de[de["Norme"]=="AAOIFI"])}</div><div class="kl">AAOIFI</div></div>
            <div class="kpi"><div class="kv" style="color:var(--honey);">{len(de[de["Norme"]=="MSCI"])}</div><div class="kl">MSCI</div></div>
            <div class="kpi k-coral"><div class="kv">0</div><div class="kl">{'Éligible PEA' if st.session_state.lang=='fr' else 'PEA Eligible'}</div></div>
        </div>""", unsafe_allow_html=True)

        st.dataframe(de[["Nom","Ticker","Emetteur","Zone","Norme","Frais(%)","Prix","AUM(M$)","Perf.1an(%)","Vol.(%)","Div.(%)"]],
            use_container_width=True, hide_index=True)

        st.markdown(f"""<div class="callout"><span class="callout-icon">💡</span><p><strong>{'Aucun ETF islamique n\'est éligible PEA en France.' if st.session_state.lang=='fr' else 'No Islamic ETF is PEA-eligible in France.'}</strong></p></div>""", unsafe_allow_html=True)
        st.download_button("📥  CSV", de.to_csv(index=False).encode("utf-8"), f"hq_etf_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
    else:
        st.markdown(f"""<div class="hero-empty" style="padding:2.5rem;">
            <div class="hero-icon">📈</div>
            <p class="hero-title">ETF {'Islamiques' if st.session_state.lang=='fr' else 'Islamic'}</p>
            <p class="hero-sub">{'Comparez' if st.session_state.lang=='fr' else 'Compare'} {len(ETF_ISL)} ETF {'conformes Sharia.' if st.session_state.lang=='fr' else 'Shariah-compliant ETFs.'}</p>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# TAB 7 — METHODOLOGIE
# ══════════════════════════════════════════════════════

with t7:
    st.markdown(f"### {'Comment fonctionne Halal Quant ?' if st.session_state.lang=='fr' else 'How does Halal Quant work?'}")
    st.markdown(f"""<p style="font-size:0.85rem;color:var(--ink-2);line-height:1.7;margin-bottom:1.5rem;">
        {'Halal Quant applique un pipeline séquentiel de <strong>10 niveaux de filtrage</strong> basé sur les normes <strong>AAOIFI</strong>.' if st.session_state.lang=='fr'
        else 'Halal Quant applies a sequential pipeline of <strong>10 filtering levels</strong> based on <strong>AAOIFI</strong> standards.'}
    </p>""", unsafe_allow_html=True)

    pipeline_steps = [
        ("N0","Qualite des donnees" if st.session_state.lang=="fr" else "Data Quality",f"Score minimum de {DQ_MIN}%." if st.session_state.lang=="fr" else f"Minimum score of {DQ_MIN}%.",False),
        ("N1","Exclusion par secteur" if st.session_state.lang=="fr" else "Sector Exclusion",f"{'Secteurs interdits :' if st.session_state.lang=='fr' else 'Prohibited sectors:'} {', '.join(SECTEURS_HARAM)}.",False),
        ("N2","Exclusion par industrie" if st.session_state.lang=="fr" else "Industry Exclusion",f"{len(INDUSTRIES_HARAM)} {'sous-industries exclues.' if st.session_state.lang=='fr' else 'sub-industries excluded.'}",False),
        ("N3","Liste noire" if st.session_state.lang=="fr" else "Blacklist",f"{len(LISTE_NOIRE)} {'entreprises exclues.' if st.session_state.lang=='fr' else 'companies excluded.'}",False),
        ("N4","Mots-cles haram" if st.session_state.lang=="fr" else "Haram Keywords",f"{len(KEYWORDS_HARAM)} {'termes scannes.' if st.session_state.lang=='fr' else 'terms scanned.'}",False),
        ("N4b","Segments revenus" if st.session_state.lang=="fr" else "Revenue Segments",f"{len(REVENUE_HARAM_MANUAL)} {'entreprises verifiees.' if st.session_state.lang=='fr' else 'companies verified.'}",True),
        ("N5","Revenus haram" if st.session_state.lang=="fr" else "Haram Revenue",f"< {SEUIL_REV_HARAM}%",False),
        ("N5b","Charges d'interets" if st.session_state.lang=="fr" else "Interest Expense",f"< {SEUIL_INT_EXP}%",False),
        ("N6","Ratios AAOIFI",f"{'Dette' if st.session_state.lang=='fr' else 'Debt'} < {SEUIL_DETTE}% · Cash < {SEUIL_CASH}% · {'Créances' if st.session_state.lang=='fr' else 'Receivables'} < {SEUIL_CREANCES}%",False),
        ("N6b","D/E Ratio",f"< {SEUIL_DE}",True),
        ("N7","Vérif. trimestrielle" if st.session_state.lang=="fr" else "Quarterly Check","Cross-check",True),
        ("N8","Zones grises" if st.session_state.lang=="fr" else "Gray Zones",f"{len(INDUSTRIES_ATTENTION)} {'industries surveillées. -10 pts.' if st.session_state.lang=='fr' else 'monitored industries. -10 pts.'}",False),
    ]

    ph = '<div class="pipeline">'
    for code,title,desc,is_new in pipeline_steps:
        new_cls = " pipe-new" if is_new else ""
        new_tag = '<span class="pipe-new-tag">NEW</span>' if is_new else ""
        ph += f"""<div class="pipe-step{new_cls}">
            <div class="pipe-num">{code}</div>
            <div class="pipe-body">
                <p class="pipe-title">{title}{new_tag}</p>
                <p class="pipe-desc">{desc}</p>
            </div>
        </div>"""
    ph += '</div>'
    st.markdown(ph, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"### {'Comparaison des normes' if st.session_state.lang=='fr' else 'Standards Comparison'}")
    st.dataframe(pd.DataFrame({
        "Critere" if st.session_state.lang=="fr" else "Criteria":["Dette/cap","Cash/cap","Creances/cap","Rev.haram","Charges int.","D/E ratio","Verif. trim." if st.session_state.lang=="fr" else "Quarterly","Purification"],
        "Halal Quant":[f"< {SEUIL_DETTE}%",f"< {SEUIL_CASH}%",f"< {SEUIL_CREANCES}%",f"< {SEUIL_REV_HARAM}%",f"< {SEUIL_INT_EXP}%",f"< {SEUIL_DE}","Oui" if st.session_state.lang=="fr" else "Yes","Oui" if st.session_state.lang=="fr" else "Yes"],
        "AAOIFI":["< 33%","< 33%","< 49%","< 5%","—","—","Recommande" if st.session_state.lang=="fr" else "Recommended","Oui" if st.session_state.lang=="fr" else "Yes"],
        "MSCI":["< 33.33%","< 33.33%","< 33.33%","< 5%","—","—","Non" if st.session_state.lang=="fr" else "No","Non specifie" if st.session_state.lang=="fr" else "Not specified"],
    }), use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════

st.markdown(f"""<div class="foot">
    <p><strong>Halal Quant</strong> · 10 {'niveaux' if st.session_state.lang=='fr' else 'levels'} AAOIFI · 25+ {'métriques' if st.session_state.lang=='fr' else 'metrics'} · {len(TICKERS)} actions Euronext Paris</p>
    <p>{'Créé par' if st.session_state.lang=='fr' else 'Created by'} <strong>Mbilah Gossene</strong> · <a href="https://github.com/mbilah-gossene/halal-quant-screener">GitHub</a></p>
    <p>{'Données Yahoo Finance · Outil d\'aide à la décision, pas de conseil en investissement' if st.session_state.lang=='fr' else 'Yahoo Finance data · Decision support tool, not investment advice'}</p>
</div>""", unsafe_allow_html=True)
