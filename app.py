import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Halal Quant", page_icon="🕌", layout="wide")
st.title("🕌 Halal Quant — Screener Sharia")
st.markdown("**Screening automatique des actions francaises selon les normes AAOIFI**")
st.markdown("---")

SECTEURS_HARAM = ["Financial Services"]
INDUSTRIES_HARAM = [
    "Banks - Regional", "Banks - Diversified", "Banks - Global",
    "Insurance - Diversified", "Insurance - Life",
    "Insurance - Property & Casualty", "Insurance - Reinsurance",
    "Insurance Brokers", "Credit Services", "Mortgage Finance",
    "Capital Markets", "Asset Management",
    "Alcoholic Beverages", "Breweries", "Wineries",
    "Distillers & Vintners", "Tobacco", "Gambling",
    "Casinos & Gaming", "Adult Entertainment", "Weapons & Ammunition"
]
LISTE_NOIRE = {
    "MC.PA": "LVMH alcool",
    "RI.PA": "Pernod Ricard alcool",
    "KER.PA": "Kering vignobles",
    "RCO.PA": "Remy Cointreau alcool"
}
TICKERS = {
    "AI.PA": "Air Liquide",
    "AIR.PA": "Airbus",
    "CAP.PA": "Capgemini",
    "DG.PA": "Vinci",
    "MC.PA": "LVMH",
    "OR.PA": "L Oreal",
    "SAN.PA": "Sanofi",
    "TTE.PA": "TotalEnergies",
    "BNP.PA": "BNP Paribas",
    "CS.PA": "AXA",
    "RI.PA": "Pernod Ricard",
    "SU.PA": "Schneider Electric",
    "EN.PA": "Bouygues",
    "DSY.PA": "Dassault Systemes",
    "HO.PA": "Thales",
    "RMS.PA": "Hermes",
    "SAF.PA": "Safran",
    "EL.PA": "EssilorLuxottica",
    "ML.PA": "Michelin",
    "BN.PA": "Danone",
    "ACA.PA": "Credit Agricole",
    "GLE.PA": "Societe Generale",
    "ENGI.PA": "Engie",
    "VIE.PA": "Veolia",
    "PUB.PA": "Publicis",
    "KER.PA": "Kering",
    "LR.PA": "Legrand",
    "MT.AS": "ArcelorMittal",
    "ORA.PA": "Orange",
    "RNO.PA": "Renault",
    "SGO.PA": "Saint-Gobain",
    "STLAP.PA": "Stellantis",
    "STMPA.PA": "STMicroelectronics",
    "TEP.PA": "Teleperformance",
    "URW.AS": "Unibail-Rodamco",
    "CA.PA": "Carrefour",
    "ERF.PA": "Eurofins Scientific",
    "VIV.PA": "Vivendi",
    "WLN.PA": "Worldline"
}

st.sidebar.header("Parametres AAOIFI")
st.sidebar.markdown("Seuil dette : < 33%")
st.sidebar.markdown("Seuil cash : < 33%")
st.sidebar.markdown("Seuil creances : < 49%")
st.sidebar.markdown("Revenus haram : < 5%")
st.sidebar.markdown("---")
st.sidebar.markdown("Cree par Mbilah Gossene")

if st.button("Lancer l analyse", type="primary"):
    progress = st.progress(0)
    status = st.empty()
    resultats = []

    for i, (ticker, nom) in enumerate(TICKERS.items()):
        progress.progress((i + 1) / len(TICKERS))
        status.text(f"Analyse de {nom}...")

        try:
            info = yf.Ticker(ticker).info
            sector = info.get("sector", "Inconnu")
            industry = info.get("industry", "Inconnu")
            market_cap = info.get("marketCap", 0)
            total_debt = info.get("totalDebt", 0)
            total_cash = info.get("totalCash", 0)
            receivables = info.get("netReceivables", 0)
            prix = info.get("currentPrice", 0)
            per = info.get("trailingPE", "N/A")
            dividend_yield = info.get("dividendYield", 0)
            interest_income = info.get("interestIncome", 0)
            total_revenue = info.get("totalRevenue", 1)

            if sector in SECTEURS_HARAM or industry in INDUSTRIES_HARAM:
                statut = "HARAM"
                score = 0
                r_dette = "N/A"
            elif ticker in LISTE_NOIRE:
                statut = "HARAM"
                score = 0
                r_dette = "N/A"
            else:
                r_dette = round(total_debt / market_cap * 100, 1) if market_cap > 0 else 0
                r_cash = round(total_cash / market_cap * 100, 1) if market_cap > 0 else 0
                r_creances = round(receivables / market_cap * 100, 1) if market_cap > 0 else 0
                rev_haram = 0
                if interest_income and total_revenue and total_revenue > 0:
                    rev_haram = round(abs(interest_income) / abs(total_revenue) * 100, 2)

                if rev_haram > 5:
                    statut = "NON CONFORME"
                elif r_dette > 33:
                    statut = "NON CONFORME"
                elif r_cash > 33:
                    statut = "NON CONFORME"
                elif r_creances > 49:
                    statut = "NON CONFORME"
                else:
                    statut = "CONFORME"

                s1 = max(0, 100 - (r_dette / 33 * 100))
                s2 = max(0, 100 - (r_cash / 33 * 100))
                s3 = max(0, 100 - (r_creances / 49 * 100))
                score = round((s1 + s2 + s3) / 3, 0)

            resultats.append({
                "Nom": nom,
                "Statut": statut,
                "Score": score,
                "Prix": round(prix, 2) if prix else 0,
                "PER": round(per, 1) if isinstance(per, (int, float)) else "N/A",
                "Dividende": round(dividend_yield * 100, 2) if dividend_yield else 0,
                "Dette": r_dette,
                "Secteur": sector
            })
        except Exception as e:
            pass

    status.text("Analyse terminee !")
    df = pd.DataFrame(resultats)

    conf = df[df["Statut"] == "CONFORME"]
    non_conf = df[df["Statut"] == "NON CONFORME"]
    haram = df[df["Statut"] == "HARAM"]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Analysees", len(df))
    col2.metric("Conformes", len(conf))
    col3.metric("Non conformes", len(non_conf))
    col4.metric("Haram", len(haram))

    st.markdown("---")

    st.subheader("Actions conformes")
    st.dataframe(
        conf.sort_values("Score", ascending=False)[["Nom", "Score", "Prix", "PER", "Dividende", "Dette", "Secteur"]],
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Actions non conformes")
    st.dataframe(
        non_conf[["Nom", "Prix", "Dette", "Secteur"]],
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Actions haram")
    st.dataframe(
        haram[["Nom", "Secteur"]],
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("Clique sur le bouton pour lancer l analyse")
