import streamlit as st
import pandas as pd
import yfinance as yf
import time
from datetime import datetime

st.set_page_config(page_title="Halal Quant", page_icon="☪️", layout="wide", initial_sidebar_state="collapsed")

# ══════════════════════════════════════════════════════
# REDESIGN CSS — Premium Warm Fintech
# ══════════════════════════════════════════════════════

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@300;400;500;600;700;800;900&family=Source+Code+Pro:wght@400;500;600;700&display=swap');

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
    .stApp { font-family: 'Nunito Sans', -apple-system, sans-serif; background: var(--cream); color: var(--ink); }
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
    .brand-pills { display: flex; gap: 6px; flex-wrap: wrap; }
    .brand-pill {
        font-size: 0.6rem; font-weight: 700; padding: 3px 10px; border-radius: var(--r-full);
        background: var(--warm-50); border: 1px solid var(--warm-200); color: var(--ink-3);
        letter-spacing: 0.2px;
    }

    /* ── Hero (screener landing) ── */
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
    .sdiv h3 { font-size: 0.92rem; font-weight: 700; color: var(--ink); margin: 0; letter-spacing: -0.2px; }
    .sdiv .sdiv-cnt {
        font-family: 'Source Code Pro', monospace; font-size: 0.62rem; font-weight: 600;
        color: var(--ink-3); background: var(--warm-100); padding: 2px 8px; border-radius: var(--r-full);
    }

    /* ── Stock Card (search) ── */
    .scard {
        background: var(--white); border: 1px solid var(--warm-200); border-radius: 18px;
        padding: 24px; margin: 14px 0; box-shadow: var(--shadow);
    }
    .scard.sc-ok { border-top: 4px solid var(--sage); }
    .scard.sc-no { border-top: 4px solid var(--honey); }
    .scard.sc-h  { border-top: 4px solid var(--coral); }
    .scard.sc-nd { border-top: 4px solid var(--stone); }

    .scard-top { display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px; margin-bottom: 16px; }
    .scard-name { font-size: 1.35rem; font-weight: 800; color: var(--ink); margin: 0; letter-spacing: -0.5px; }
    .scard-meta { font-size: 0.72rem; color: var(--ink-3); margin: 3px 0 0; }

    /* ── Verdict Badge (large, Zoya-style) ── */
    .verdict {
        display: inline-flex; align-items: center; gap: 6px;
        padding: 6px 16px; border-radius: var(--r-full);
        font-size: 0.72rem; font-weight: 700; letter-spacing: 0.3px;
    }
    .verdict-ok { background: var(--sage-light); color: var(--sage); }
    .verdict-no { background: var(--honey-light); color: var(--honey); }
    .verdict-h  { background: var(--coral-light); color: var(--coral); }
    .verdict-nd { background: var(--stone-light); color: var(--stone); }
    .dq-pill {
        font-family: 'Source Code Pro', monospace; font-size: 0.58rem; font-weight: 600;
        padding: 2px 8px; border-radius: var(--r-xs); margin-left: 6px;
    }
    .dq-h { background: var(--sage-light); color: var(--sage); }
    .dq-m { background: var(--honey-light); color: var(--honey); }
    .dq-l { background: var(--coral-light); color: var(--coral); }

    /* ── Ratio Gauges ── */
    .ratios { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 8px; margin: 14px 0; }
    .ratio {
        background: var(--warm-50); border: 1px solid var(--warm-200); border-radius: var(--r);
        padding: 14px 10px; text-align: center;
    }
    .ratio .rv {
        font-family: 'Source Code Pro', monospace; font-size: 1.3rem; font-weight: 700;
    }
    .ratio .rl { font-size: 0.58rem; color: var(--ink-4); text-transform: uppercase; letter-spacing: 0.4px; margin: 3px 0 8px; }
    .ratio .rb { height: 4px; background: var(--warm-200); border-radius: 2px; overflow: hidden; }
    .ratio .rf { height: 100%; border-radius: 2px; transition: width 0.5s ease; }
    .r-ok{color:var(--sage);} .r-warn{color:var(--honey);} .r-fail{color:var(--coral);} .r-na{color:var(--ink-4);}

    /* ── Score Bar ── */
    .score-box {
        display: flex; align-items: center; gap: 14px; padding: 12px 16px;
        background: var(--warm-50); border: 1px solid var(--warm-200); border-radius: var(--r); margin: 14px 0;
    }
    .score-label { font-size: 0.75rem; color: var(--ink-3); font-weight: 600; white-space: nowrap; }
    .score-track { flex: 1; height: 8px; background: var(--warm-200); border-radius: 4px; overflow: hidden; }
    .score-fill { height: 100%; border-radius: 4px; transition: width 0.5s ease; }
    .score-val {
        font-family: 'Source Code Pro', monospace; font-weight: 700; font-size: 1.2rem;
        min-width: 38px; text-align: right;
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

    /* ── Streamlit overrides ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px; background: var(--warm-100); border-radius: var(--r); padding: 3px;
        border: 1px solid var(--warm-200);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: var(--r-sm); font-family: 'Nunito Sans', sans-serif;
        font-weight: 700; font-size: 0.78rem; color: var(--ink-3);
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
        font-size: 0.75rem !important; font-family: 'Nunito Sans', sans-serif !important;
    }
    button[data-testid="stBaseButton-primary"] {
        background: linear-gradient(135deg, var(--sage) 0%, var(--sage-dark) 100%) !important;
        border: none !important; border-radius: var(--r) !important;
        font-family: 'Nunito Sans', sans-serif !important; font-weight: 700 !important;
        font-size: 0.85rem !important; padding: 12px 24px !important;
        box-shadow: var(--shadow-glow-sage) !important;
        transition: all 0.2s !important;
    }
    button[data-testid="stBaseButton-primary"]:hover {
        transform: translateY(-1px) !important; box-shadow: var(--shadow-lg) !important;
    }
    .stTextInput input {
        border-radius: var(--r) !important; border: 1.5px solid var(--warm-200) !important;
        font-family: 'Nunito Sans', sans-serif !important; padding: 12px 16px !important;
        font-size: 0.88rem !important; background: var(--white) !important;
    }
    .stTextInput input:focus { border-color: var(--sage) !important; box-shadow: 0 0 0 3px rgba(45,122,95,0.1) !important; }
    [data-testid="stExpander"] { border: 1px solid var(--warm-200) !important; border-radius: var(--r) !important; }
    .stDataFrame { border-radius: var(--r) !important; overflow: hidden; }
</style>
""", unsafe_allow_html=True)
# ══════════════════════════════════════════════════════
# CONFIG AAOIFI V11 — ALL FILTERS
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
# ENGINE
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
        "PER":rv(pe),"PER Fwd":rv(fpe),"Div.(%)":dd,"Div.suspect":ds,
        "ROE(%)":rv(roe,100),"Marge op.(%)":rv(om,100),"Marge nette(%)":rv(pm,100),
        "Marge brute(%)":rv(gm,100),"Croiss.CA(%)":rv(rg,100),"Croiss.BN(%)":rv(eg,100),
        "Beta":rv(bt),"D/E":rv(der),"Current Ratio":round(cr,2) if isinstance(cr,(int,float)) and cr else "—",
        "FCF(M€)":round(fcf/1e6,0) if fcf else "—","OCF(M€)":round(ocf/1e6,0) if ocf else "—",
        "Data":dqs,"Trim.":"Oui" if qd else "Non"}

    def mk(st,sc,ra,nv):
        b.update({"Statut":st,"Score":sc,"Raison":ra,"Dette/Cap(%)":"—","Cash+Inv/Cap(%)":"—",
            "Creances/Cap(%)":"—","Rev.haram(%)":"—","Charges int.(%)":"—","Purif.(%)":"—",
            "Attention":"","Niveaux":nv})
        return b

    if dqs<DQ_MIN: return mk("Donnees insuff.",0,f"Donnees insuffisantes ({dqs}%)","N0")
    if sec in SECTEURS_HARAM: return mk("Haram",0,f"Secteur interdit : {sec}","N1")
    if ind in INDUSTRIES_HARAM: return mk("Haram",0,f"Industrie interdite : {ind}","N2")
    if tk in LISTE_NOIRE: return mk("Haram",0,LISTE_NOIRE[tk],"N3")
    if kw: return mk("Haram",0,f"Activite haram : {', '.join(kw[:4])}","N4")
    if tk in REVENUE_HARAM_MANUAL:
        _,rs,pc=REVENUE_HARAM_MANUAL[tk]
        if pc>SEUIL_REV_HARAM: return mk("Haram",0,f"{rs} (~{pc}% CA)","N4b")

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
        "Attention":att,"Niveaux":", ".join(set(nv)) if nv else "OK"})
    return b

# ══════════════════════════════════════════════════════
# BRAND BAR
# ══════════════════════════════════════════════════════

st.markdown(f"""
<div class="brand">
    <div class="brand-left">
        <div class="brand-mark">☪️</div>
        <span class="brand-text">Halal <em>Quant</em></span>
    </div>
    <div class="brand-pills">
        <span class="brand-pill">{len(TICKERS)} actions Euronext</span>
        <span class="brand-pill">Norme AAOIFI</span>
        <span class="brand-pill">Par Mbilah Gossene</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════

t1,t2,t3,t4 = st.tabs(["📊  Screener","🔍  Recherche","📈  ETF Islamiques","📖  Methodologie"])

# ── SCREENER ──
with t1:
    if st.button("Lancer l'analyse complète",type="primary",use_container_width=True):
        pg=st.progress(0); sx=st.empty(); res=[]; err=0
        for i,(tk,nm) in enumerate(TICKERS.items()):
            pg.progress((i+1)/len(TICKERS))
            sx.text(f"Analyse de {nm} ({tk}) — {i+1}/{len(TICKERS)}")
            try:
                to=yf.Ticker(tk); inf=to.info
                if not inf or inf.get("quoteType")=="NONE": raise ValueError("No data")
                res.append(analyze(tk,inf,to))
            except Exception as e:
                err+=1
                eb={k:"—" for k in ["PER","PER Fwd","ROE(%)","Marge op.(%)","Marge nette(%)","Marge brute(%)",
                    "Croiss.CA(%)","Croiss.BN(%)","Beta","D/E","Current Ratio","FCF(M€)","OCF(M€)",
                    "Dette/Cap(%)","Cash+Inv/Cap(%)","Creances/Cap(%)","Rev.haram(%)","Charges int.(%)","Purif.(%)"]}
                eb.update({"Ticker":tk,"Nom":nm,"Statut":"Donnees insuff.","Score":0,
                    "Raison":f"Erreur: {str(e)[:40]}","Prix":0,"Div.(%)":0,"Div.suspect":False,
                    "Cap.(M€)":0,"Cap.type":"—","Secteur":"Inconnu","Industrie":"Inconnu",
                    "Attention":"","Data":0,"Niveaux":"Erreur","Trim.":"Non"})
                res.append(eb)
            if (i+1)%12==0: time.sleep(1.5)
        pg.empty(); sx.empty()

        df=pd.DataFrame(res)
        co=df[df["Statut"]=="Conforme"]; nc=df[df["Statut"]=="Non conforme"]
        ha=df[df["Statut"]=="Haram"]; nd=df[df["Statut"]=="Donnees insuff."]
        gr=co[co["Attention"]!=""]

        # KPIs
        st.markdown(f"""<div class="kpis">
            <div class="kpi k-sky"><div class="kv">{len(df)}</div><div class="kl">Analysees</div></div>
            <div class="kpi k-sage"><div class="kv">{len(co)}</div><div class="kl">Conformes</div></div>
            <div class="kpi k-honey"><div class="kv">{len(nc)}</div><div class="kl">Non conformes</div></div>
            <div class="kpi k-coral"><div class="kv">{len(ha)}</div><div class="kl">Haram</div></div>
            <div class="kpi k-stone"><div class="kv">{len(nd)}</div><div class="kl">Data insuff.</div></div>
            <div class="kpi"><div class="kv" style="color:var(--honey);">{len(gr)}</div><div class="kl">Zones grises</div></div>
        </div>""", unsafe_allow_html=True)

        # Conformes
        st.markdown(f'<div class="sdiv"><div class="sdiv-dot d-sage"></div><h3>Actions conformes Sharia</h3><span class="sdiv-cnt">{len(co)}</span></div>', unsafe_allow_html=True)
        if len(co)>0:
            st.dataframe(co.sort_values("Score",ascending=False)[["Nom","Score","Data","Trim.","Prix","Cap.(M€)","Cap.type",
                "PER","Div.(%)","ROE(%)","Marge op.(%)","Marge nette(%)","Beta","D/E","Current Ratio","FCF(M€)",
                "Dette/Cap(%)","Cash+Inv/Cap(%)","Creances/Cap(%)","Charges int.(%)","Purif.(%)","Secteur","Attention"]],
                use_container_width=True, hide_index=True, height=min(600,50+len(co)*35))
        else:
            st.info("Aucune action conforme trouvee.")

        # Non conformes
        st.markdown(f'<div class="sdiv"><div class="sdiv-dot d-honey"></div><h3>Non conformes</h3><span class="sdiv-cnt">{len(nc)}</span></div>', unsafe_allow_html=True)
        if len(nc)>0:
            st.dataframe(nc[["Nom","Raison","Prix","Cap.(M€)","Dette/Cap(%)","Cash+Inv/Cap(%)","Creances/Cap(%)","Rev.haram(%)","Charges int.(%)","D/E","Secteur","Niveaux"]],
                use_container_width=True, hide_index=True)

        # Haram
        st.markdown(f'<div class="sdiv"><div class="sdiv-dot d-coral"></div><h3>Haram</h3><span class="sdiv-cnt">{len(ha)}</span></div>', unsafe_allow_html=True)
        if len(ha)>0:
            st.dataframe(ha[["Nom","Raison","Secteur","Industrie","Niveaux"]], use_container_width=True, hide_index=True)

        # Data insuff.
        if len(nd)>0:
            st.markdown(f'<div class="sdiv"><div class="sdiv-dot d-stone"></div><h3>Donnees insuffisantes</h3><span class="sdiv-cnt">{len(nd)}</span></div>', unsafe_allow_html=True)
            st.dataframe(nd[["Nom","Ticker","Raison","Data"]], use_container_width=True, hide_index=True)

        # Downloads
        st.markdown("---")
        c1,c2,c3 = st.columns(3)
        with c1: st.download_button("📥  CSV complet", df.to_csv(index=False).encode("utf-8"), f"halal_quant_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv", use_container_width=True)
        with c2: st.download_button("📥  Conformes seuls", co.to_csv(index=False).encode("utf-8"), f"hq_conformes_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv", use_container_width=True)
        with c3: st.download_button("📥  Rapport JSON", df.to_json(orient="records",indent=2).encode("utf-8"), f"hq_rapport_{datetime.now().strftime('%Y%m%d')}.json", "application/json", use_container_width=True)

    else:
        st.markdown(f"""
        <div class="hero-empty">
            <div class="hero-icon">☪️</div>
            <p class="hero-title">Screener Sharia — Euronext Paris</p>
            <p class="hero-sub">Analysez {len(TICKERS)} actions selon 10 niveaux de filtrage AAOIFI.<br>Capitalisation moyenne 12 mois · Verification trimestrielle · 25+ metriques.</p>
            <div class="hero-chips">
                <span class="hero-chip">10 niveaux AAOIFI</span>
                <span class="hero-chip">Cap. moy. 12 mois</span>
                <span class="hero-chip">Verif. trimestrielle</span>
                <span class="hero-chip">Export CSV / JSON</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ── RECHERCHE ──
with t2:
    st.markdown(f"""<p style="font-size:0.82rem;color:var(--ink-3);margin:0 0 8px;">Analysez n'importe quelle action dans le monde selon les normes AAOIFI.</p>""", unsafe_allow_html=True)
    ti = st.text_input("Ticker", placeholder="Entrez un ticker — ex: AAPL, MSFT, TTE.PA, AIR.PA...", label_visibility="collapsed")

    if ti:
        tc = ti.strip().upper()
        with st.spinner(f"Analyse de {tc}..."):
            try:
                to=yf.Ticker(tc); inf=to.info
                if not inf or inf.get("quoteType")=="NONE":
                    st.error(f"Aucune donnee trouvee pour {tc}.")
                else:
                    r = analyze(tc, inf, to)
                    # Card class
                    cc = {"Conforme":"sc-ok","Non conforme":"sc-no","Haram":"sc-h"}.get(r["Statut"],"sc-nd")
                    vc = {"Conforme":"verdict-ok","Non conforme":"verdict-no","Haram":"verdict-h"}.get(r["Statut"],"verdict-nd")
                    dqc = "dq-h" if r["Data"]>=70 else ("dq-m" if r["Data"]>=40 else "dq-l")

                    st.markdown(f"""
                    <div class="scard {cc}">
                        <div class="scard-top">
                            <div>
                                <p class="scard-name">{r['Nom']}</p>
                                <p class="scard-meta">{tc} · {r['Secteur']} · {r['Industrie']} · Cap. {r.get('Cap.type','—')}</p>
                            </div>
                            <div>
                                <span class="verdict {vc}">{r['Statut']}</span>
                                <span class="dq-pill {dqc}">Data {r['Data']}%</span>
                            </div>
                        </div>
                        <p style="margin:14px 0 0;color:var(--ink-2);font-size:0.82rem;line-height:1.5;">
                            <strong style="color:var(--ink);">Verdict :</strong> {r['Raison']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                    # Ratio gauges (only if not Haram/NoData)
                    if r["Statut"] not in ["Haram","Donnees insuff."]:
                        def _gc(v,s):
                            if not isinstance(v,(int,float)): return "r-na"
                            return "r-ok" if v<=s*0.6 else ("r-warn" if v<=s else "r-fail")
                        def _gfc(v,s):
                            if not isinstance(v,(int,float)): return "var(--ink-4)"
                            return "var(--sage)" if v<=s*0.6 else ("var(--honey)" if v<=s else "var(--coral)")
                        def _gfw(v,s):
                            if not isinstance(v,(int,float)): return 0
                            return min(100,v/s*100)
                        def _fmt(v): return f"{v}%" if isinstance(v,(int,float)) else "—"

                        rh = '<div class="ratios">'
                        for key,seuil,label in [
                            ("Dette/Cap(%)",SEUIL_DETTE,"Dette / Cap."),
                            ("Cash+Inv/Cap(%)",SEUIL_CASH,"Cash+Inv / Cap."),
                            ("Creances/Cap(%)",SEUIL_CREANCES,"Creances / Cap."),
                            ("Rev.haram(%)",SEUIL_REV_HARAM,"Rev. haram / CA"),
                            ("Charges int.(%)",SEUIL_INT_EXP,"Charges int. / CA")]:
                            v = r.get(key)
                            rh += f"""<div class="ratio">
                                <div class="rv {_gc(v,seuil)}">{_fmt(v)}</div>
                                <div class="rl">{label} (seuil {seuil}%)</div>
                                <div class="rb"><div class="rf" style="width:{_gfw(v,seuil)}%;background:{_gfc(v,seuil)};"></div></div>
                            </div>"""
                        rh += '</div>'
                        st.markdown(rh, unsafe_allow_html=True)

                    # Financial metrics organized by category
                    st.markdown(f'<div class="sdiv"><div class="sdiv-dot d-sage"></div><h3>Valorisation</h3></div>', unsafe_allow_html=True)
                    c1,c2,c3,c4,c5 = st.columns(5)
                    c1.metric("Prix", f"{r['Prix']} €" if r['Prix'] else "—")
                    c2.metric("PER", r['PER'])
                    c3.metric("PER Forward", r['PER Fwd'])
                    c4.metric("Cap. (M€)", r.get('Cap.(M€)','—'))
                    c5.metric("Dividende", f"{r['Div.(%)']}%" if r['Div.(%)'] else "—")

                    st.markdown(f'<div class="sdiv"><div class="sdiv-dot d-sky"></div><h3>Profitabilite & Croissance</h3></div>', unsafe_allow_html=True)
                    c1,c2,c3,c4,c5 = st.columns(5)
                    c1.metric("ROE", f"{r['ROE(%)']}" if r['ROE(%)']!="—" else "—")
                    c2.metric("Marge op.", f"{r['Marge op.(%)']}" if r['Marge op.(%)']!="—" else "—")
                    c3.metric("Marge nette", f"{r['Marge nette(%)']}" if r['Marge nette(%)']!="—" else "—")
                    c4.metric("Croiss. CA", f"{r['Croiss.CA(%)']}" if r['Croiss.CA(%)']!="—" else "—")
                    c5.metric("FCF (M€)", r.get('FCF(M€)','—'))

                    st.markdown(f'<div class="sdiv"><div class="sdiv-dot d-honey"></div><h3>Risque & Endettement</h3></div>', unsafe_allow_html=True)
                    c1,c2,c3,c4 = st.columns(4)
                    c1.metric("Beta", r['Beta'])
                    c2.metric("D/E Ratio", r['D/E'])
                    c3.metric("Current Ratio", r['Current Ratio'])
                    c4.metric("OCF (M€)", r.get('OCF(M€)','—'))

                    # Alerts
                    if r.get("Div.suspect"):
                        st.warning("Dividende suspect (>15%) — donnee probablement erronee, a verifier.")
                    if r.get("Purif.(%)") and r["Purif.(%)"]!="—" and r["Purif.(%)"]>0:
                        st.markdown(f'<div class="callout"><span class="callout-icon">🕌</span><p><strong>Purification du dividende :</strong> {r["Purif.(%)"]}% de vos dividendes sont a reverser en sadaqa (charite) pour purifier votre investissement.</p></div>', unsafe_allow_html=True)
                    if r.get("Trim.")=="Oui":
                        st.success("✓ Donnees trimestrielles disponibles — cross-check effectue.")

                    # Score bar
                    if r["Score"]>0:
                        sc=r["Score"]
                        clr="var(--sage)" if sc>=70 else ("var(--honey)" if sc>=40 else "var(--coral)")
                        st.markdown(f"""<div class="score-box">
                            <span class="score-label">Score Sharia</span>
                            <div class="score-track"><div class="score-fill" style="width:{sc}%;background:{clr};"></div></div>
                            <span class="score-val" style="color:{clr};">{int(sc)}</span>
                        </div>""", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Erreur lors de l'analyse : {e}")


# ── ETF ISLAMIQUES ──
with t3:
    st.markdown('<p style="font-size:0.82rem;color:var(--ink-3);margin:0 0 10px;">Comparez les principaux ETF conformes Sharia disponibles sur le marche.</p>', unsafe_allow_html=True)
    cf1,cf2,cf3 = st.columns(3)
    with cf1: zf=st.multiselect("Zone geographique", sorted(set(e["z"] for e in ETF_ISL.values())), default=sorted(set(e["z"] for e in ETF_ISL.values())))
    with cf2: nf=st.multiselect("Norme Sharia", sorted(set(e["no"] for e in ETF_ISL.values())), default=sorted(set(e["no"] for e in ETF_ISL.values())))
    with cf3: fm=st.slider("Frais maximum (%)", 0.0, 1.0, 0.70, 0.05)

    if st.button("Analyser les ETF", type="primary", use_container_width=True):
        pg=st.progress(0); sx=st.empty(); rs=[]
        ef={k:v for k,v in ETF_ISL.items() if v["z"] in zf and v["no"] in nf and v["f"]<=fm}
        for i,(t,m) in enumerate(ef.items()):
            pg.progress((i+1)/max(1,len(ef))); sx.text(f"Analyse de {m['n']}...")
            try:
                et=yf.Ticker(t); inf=et.info; h=et.history(period="1y")
                px=inf.get("regularMarketPrice") or inf.get("previousClose") or 0
                au=inf.get("totalAssets",0) or 0; dy=inf.get("yield",0) or 0
                p1=round((h["Close"].iloc[-1]-h["Close"].iloc[0])/h["Close"].iloc[0]*100,2) if len(h)>1 and h["Close"].iloc[0]>0 else 0
                vo=round(h["Close"].pct_change().dropna().std()*(252**0.5)*100,2) if len(h)>20 else 0
                rs.append({"Nom":m["n"],"Ticker":t,"Emetteur":m["e"],"Zone":m["z"],"Norme":m["no"],
                    "Frais(%)":m["f"],"Prix":round(px,2) if px else "—","AUM(M$)":round(au/1e6,0) if au else "—",
                    "Perf.1an(%)":p1,"Vol.(%)":vo,"Div.(%)":round(dy*100,2) if dy and dy<1 else 0,"Domicile":m["d"],"Desc":m["ds"]})
            except:
                rs.append({"Nom":m["n"],"Ticker":t,"Emetteur":m["e"],"Zone":m["z"],"Norme":m["no"],
                    "Frais(%)":m["f"],"Prix":"—","AUM(M$)":"—","Perf.1an(%)":"—","Vol.(%)":"—","Div.(%)":"—","Domicile":m["d"],"Desc":m["ds"]})
        pg.empty(); sx.empty()
        de=pd.DataFrame(rs)

        st.markdown(f"""<div class="kpis">
            <div class="kpi k-sky"><div class="kv">{len(de)}</div><div class="kl">ETF analyses</div></div>
            <div class="kpi k-sage"><div class="kv">{len(de[de["Norme"]=="AAOIFI"])}</div><div class="kl">Norme AAOIFI</div></div>
            <div class="kpi"><div class="kv" style="color:var(--honey);">{len(de[de["Norme"]=="MSCI"])}</div><div class="kl">Norme MSCI</div></div>
            <div class="kpi k-coral"><div class="kv">0</div><div class="kl">Eligible PEA</div></div>
        </div>""", unsafe_allow_html=True)

        st.dataframe(de[["Nom","Ticker","Emetteur","Zone","Norme","Frais(%)","Prix","AUM(M$)","Perf.1an(%)","Vol.(%)","Div.(%)"]],
            use_container_width=True, hide_index=True)

        for _,rw in de.iterrows():
            with st.expander(f"{rw['Nom']} ({rw['Ticker']})"):
                c1,c2 = st.columns(2)
                c1.markdown(f"**Emetteur :** {rw['Emetteur']}\n\n**Zone :** {rw['Zone']}\n\n**Norme :** {rw['Norme']}")
                c2.markdown(f"**Prix :** {rw['Prix']}\n\n**Frais :** {rw['Frais(%)']}%\n\n**AUM :** {rw['AUM(M$)']}M$")
                st.caption(rw['Desc'])

        st.markdown("---")
        st.markdown(f"""<div class="callout"><span class="callout-icon">💡</span><p><strong>Aucun ETF islamique n'est eligible PEA en France.</strong> Strategie recommandee : ETF MSCI World Islamic en CTO + stock picking halal via ce screener en PEA pour l'optimisation fiscale.</p></div>""", unsafe_allow_html=True)
        st.download_button("📥  Telecharger CSV", de.to_csv(index=False).encode("utf-8"), f"hq_etf_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
    else:
        st.markdown(f"""<div class="hero-empty" style="padding:2.5rem;">
            <div class="hero-icon">📈</div>
            <p class="hero-title">ETF Islamiques</p>
            <p class="hero-sub">Comparez {len(ETF_ISL)} ETF conformes Sharia — performance, frais, volatilite.</p>
        </div>""", unsafe_allow_html=True)


# ── METHODOLOGIE ──
with t4:
    st.markdown("### Comment fonctionne Halal Quant ?")
    st.markdown(f"""<p style="font-size:0.85rem;color:var(--ink-2);line-height:1.7;margin-bottom:1.5rem;">
        Halal Quant applique un pipeline sequentiel de <strong>10 niveaux de filtrage</strong> base sur les normes
        <strong>AAOIFI</strong> — le standard de reference utilise par Zoya, Musaffa et les grandes institutions de finance islamique.
        Chaque action doit passer tous les niveaux pour etre classee <strong style="color:var(--sage);">Conforme</strong>.
    </p>""", unsafe_allow_html=True)

    # Visual Pipeline
    pipeline_steps = [
        ("N0","Qualite des donnees",f"Score minimum de {DQ_MIN}% sur 13+ champs financiers. Elimine les faux positifs.",False),
        ("N1","Exclusion par secteur",f"Secteurs 100% interdits : {', '.join(SECTEURS_HARAM)}.",False),
        ("N2","Exclusion par industrie",f"{len(INDUSTRIES_HARAM)} sous-industries exclues (banques, assurances, alcool, tabac, jeux, armes, porc).",False),
        ("N3","Liste noire manuelle",f"{len(LISTE_NOIRE)} entreprises verifiees et exclues manuellement.",False),
        ("N4","Detection par mots-cles",f"{len(KEYWORDS_HARAM)} termes scannes dans la description de l'entreprise.",False),
        ("N4b","Segments de revenus manuels",f"{len(REVENUE_HARAM_MANUAL)} entreprises avec segments haram connus (compense les limites de yfinance).",True),
        ("N5","Revenus haram",f"Revenus d'interets + autres revenus / CA < {SEUIL_REV_HARAM}%.",False),
        ("N5b","Charges d'interets",f"Charges d'interets / CA < {SEUIL_INT_EXP}%. Detecte l'endettement conventionnel.",False),
        ("N6","Ratios AAOIFI",f"Dette < {SEUIL_DETTE}% · Cash+Inv < {SEUIL_CASH}% · Creances < {SEUIL_CREANCES}% (sur cap. moy. 12 mois).",False),
        ("N6b","D/E Ratio complementaire",f"Debt-to-Equity < {SEUIL_DE}. Filtre de securite supplementaire.",True),
        ("N7","Verification trimestrielle","Cross-check des ratios sur les derniers etats trimestriels.",True),
        ("N8","Zones grises",f"{len(INDUSTRIES_ATTENTION)} industries a surveiller. Malus de -10 points sur le score.",False),
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

    st.markdown("### Score Sharia (0-100)")
    st.markdown("""
Moyenne de 5 ratios inverses (dette, cash+inv, creances, rev. haram, charges d'interets).
Penalites : zone grise (-10 pts), revenus haram > 3% (-5 pts).
Bonus : qualite data ≥ 80% (+2), cap. moyenne disponible (+1), donnees trimestrielles (+1).
    """)

    st.markdown("### Purification du dividende")
    st.markdown("Le pourcentage de revenus non conformes determine la part du dividende a reverser en sadaqa (charite) pour purifier l'investissement.")

    st.markdown("---")
    st.markdown("### Comparaison des normes Sharia")
    st.dataframe(pd.DataFrame({
        "Critere":["Dette/cap","Cash/cap","Creances/cap","Rev.haram","Charges int.","D/E ratio","Verif. trim.","Purification"],
        "Halal Quant":[f"< {SEUIL_DETTE}%",f"< {SEUIL_CASH}%",f"< {SEUIL_CREANCES}%",f"< {SEUIL_REV_HARAM}%",f"< {SEUIL_INT_EXP}%",f"< {SEUIL_DE}","Oui","Oui"],
        "AAOIFI":["< 33%","< 33%","< 49%","< 5%","—","—","Recommande","Oui"],
        "MSCI":["< 33.33%","< 33.33%","< 33.33%","< 5%","—","—","Non","Non specifie"],
    }), use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════

st.markdown(f"""<div class="foot">
    <p><strong>Halal Quant</strong> · 10 niveaux AAOIFI · 25+ metriques · {len(TICKERS)} actions Euronext Paris</p>
    <p>Cree par <strong>Mbilah Gossene</strong> · <a href="https://github.com/mbilah-gossene/halal-quant-screener">GitHub</a></p>
    <p>Donnees Yahoo Finance · Outil d'aide a la decision, pas de conseil en investissement</p>
</div>""", unsafe_allow_html=True)
