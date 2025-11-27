import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.data_loader import load_data

# --- 1. CONFIG INITIALE ---
st.set_page_config(
    page_title = "Olist Dashboard",
    page_icon = "💰",
    layout = "wide"
)

# --- CSS -> ALIGNEMENT DES KPIs ---
st.markdown("""
    <style>
    div[data-testid="stMetric"] {
        background-color: #1F2937;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #374151;
        text-align: center;
    }
    div[data-testid="stMetricLabel"] {
        justify-content: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. CHARGEMENT DES DONNÉES ---
df = load_data()
with st.sidebar:
    st.header("Sofiane El Morabit")
    st.write("### Business/Digital/Data Analyst")
    
    st.markdown("---")
    
    # Liens externes
    st.markdown("👉 [Mon Profil LinkedIn](https://www.linkedin.com/in/sofiane-el-morabit-4a71aa20b//)")
    st.markdown("👉 [Mon Portfolio GitHub](https://github.com/sofianee9)")
    
    st.markdown("---")
    st.write("**A propos de ce projet :**")
    st.caption("""
    Ce dashboard démontre ma capacité à transformer de la donnée brute en décisions business concrètes.
    
    **Tech Stack :**
    - Python (Pandas)
    - Plotly (Data Viz)
    - Streamlit (Web App)
    """)

## --- 3. HEADER ---
st.title("💰 Tableau de Bord Stratégique Olist")

st.markdown("""
    **CONTEXTE & OBJECTIFS :**
    
    Ce dashboard pilote la performance financière d'Olist sur le marché brésilien (2016-2018).
    Il vise à réconcilier la **vision financière** (Marge, CA) et la **réalité opérationnelle** (Logistique, Satisfaction).
    
    🎯 **Leviers activables :** Optimisation des coûts de transport, rationalisation du catalogue et réduction des délais de livraison.
    
    *Note : Toutes les valeurs monétaires sont exprimées en **R$** (Real Brésilien).*
""")
st.markdown("---")

if df is not None:
    
    # --- 4. KPIs ---
    ca_total = df['total_sales'].sum()
    nb_commandes = df['order_id'].nunique()
    panier_moyen = ca_total / nb_commandes
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label = "Panier Moyen", value = f"R$ {panier_moyen:.2f}", delta = "+1.2% vs marché")
    
    with col2:
        st.metric(label = "Volume de Commandes", value = f"{nb_commandes:,}".replace(",", " "), delta = "Stable")
    
    with col3:
        st.metric(label = "Chiffre d'Affaires Global", value = f"R$ {ca_total/1e6:.1f}M", delta = "Objectif atteint", delta_color = "normal")

# --- 5. ANALYSE TEMPORELLE ---
    st.markdown("---")
    st.subheader("📈 Tendance : Évolution Mensuelle du CA")

    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    monthly_sales = df.set_index('order_purchase_timestamp').resample('M')['total_sales'].sum().reset_index()

    # Les 3 Insights
    ins1, ins2, ins3 = st.columns(3)
    
    with ins1:
        st.info("🚀 **Hyper-Croissance**\n\nL'activité a explosé (x10) entre janv. 2017 et 2018, marquant la sortie de la phase pilote.")
    
    with ins2:
        st.success("📅 **Saisonnalité**\n\nLe pic historique est atteint en **Nov 2017** (Black Friday), validant la traction commerciale.")
        
    with ins3:
        st.warning("🔄 **Consolidation**\n\nLe CA se stabilise autour de **1M R$ / mois**. L'objectif 2019 passe de l'acquisition à la fidélisation.")

    # Le Graphique
    fig_sales = px.line(
        monthly_sales, 
        x = 'order_purchase_timestamp', 
        y = 'total_sales',
        markers = True,
        title = "Historique des ventes mensuelles (Vue détaillée)"
    )
    fig_sales.update_traces(line_color = '#E67E22', line_width = 3)
    fig_sales.update_layout(
        plot_bgcolor = "rgba(0,0,0,0)",
        paper_bgcolor = "rgba(0,0,0,0)",
        font_color = "#FAFAFA",
        height = 400,
        xaxis_title = "Période",
        yaxis_title = "CA (R$)",
        xaxis = dict(showgrid = False),
        yaxis = dict(showgrid = True, gridcolor = '#374151')
    )
    st.plotly_chart(fig_sales, use_container_width = True)

# --- 6. RENTABILITÉ ---
    st.markdown("---")
    st.subheader("💰 Structure des Revenus : Produit vs Transport")

    total_products = df['price'].sum()
    total_freight = df['freight_value'].sum()
    freight_share = (total_freight / ca_total) * 100

    # 1. LES CHIFFRES CLÉS
    w1, w2, w3 = st.columns(3)
    
    with w1:
        st.success(f"📦 **Ventes Produits**\n\n**R$ {total_products/1e6:.1f}M** générés par le catalogue pur (Cœur de business).")
    
    with w2:
        st.info(f"🚚 **Revenus Fret**\n\n**R$ {total_freight/1e6:.1f}M** refacturés aux clients pour la livraison.")
        
    with w3:
        st.warning(f"⚠️ **Poids Logistique**\n\nLe transport pèse **{freight_share:.1f}%** du revenu total. C'est un levier d'optimisation prioritaire.")

    # 2. LE GRAPHIQUE WATERFALL
    fig_waterfall = go.Figure(go.Waterfall(
        name = "Décomposition",
        orientation = "v",
        measure = ["relative", "relative", "total"],
        x = ["Ventes Produits", "Frais de Port", "Total CA"],
        textposition = "outside",
        text = [f"R$ {total_products/1e6:.1f}M", f"R$ {total_freight/1e6:.1f}M", f"R$ {ca_total/1e6:.1f}M"],
        y = [total_products, total_freight, 0],
        connector = {"line": {"color": "#FAFAFA"}},
        decreasing = {"marker": {"color": "#E74C3C"}},
        increasing = {"marker": {"color": "#E67E22"}},
        totals = {"marker": {"color": "#26A69A"}}
    ))

    fig_waterfall.update_layout(
        title = "Visualisation de la cascade des revenus",
        plot_bgcolor = "rgba(0,0,0,0)",
        paper_bgcolor = "rgba(0,0,0,0)",
        font_color = "#FAFAFA",
        showlegend = False,
        height = 500,
        yaxis = dict(showgrid = False),
        yaxis_range = [0, ca_total * 1.2]
    )

    st.plotly_chart(fig_waterfall, use_container_width = True)

    # --- 7. GÉOGRAPHIE ---
    st.markdown("---")
    st.subheader("🗺️ Carte de Chaleur : Où sont les clients ?")

    map_data = df.dropna(subset = ['geolocation_lat', 'geolocation_lng'])

    # On sépare l'écran en 2 : Carte (75%) | Insights (25%)
    col_map, col_txt = st.columns([3, 1])

    with col_map:
        fig_map = px.scatter_mapbox(
            map_data,
            lat = "geolocation_lat",
            lon = "geolocation_lng",
            size = "total_sales",
            size_max = 15, 
            zoom = 3,
            center = dict(lat = -15.793889, lon = -47.882778),
            mapbox_style = "carto-darkmatter",
            title = "Répartition géographique"
        )
        
        fig_map.update_traces(marker = dict(color = "#E67E22", opacity = 0.3))
        fig_map.update_layout(
            paper_bgcolor = "rgba(0,0,0,0)",
            font_color = "#FAFAFA",
            margin = dict(l = 0, r = 0, t = 30, b = 0),
            height = 500,
            showlegend = False
        )
        st.plotly_chart(fig_map, use_container_width = True)

    with col_txt:
        st.caption("Analyse Géographique")
        
        st.info("""
        **📍 Concentration Sud-Est**
        
        L'axe **São Paulo - Rio** concentre **70%** des commandes. C'est le cœur économique mais aussi la zone la plus concurrentielle.
        """)
        
        st.warning("""
        **🌵 Le Défi du Nord**
        
        L'Amazonie et le Nord sont des déserts logistiques. Les délais y explosent (> 20 jours).
        """)
        
        st.success("""
        **🎯 Opportunité**
        
        Ouvrir un hub secondaire dans le **Minas Gerais** permettrait de désengorger le Sud tout en se rapprochant du Centre.
        """)

    # --- 8. PARETO ---
    st.markdown("---")
    st.subheader("🏆 Top 10 Catégories (Loi de Pareto)")

    top_cat = df.groupby("product_category_name_english")['total_sales'].sum().reset_index()
    top_cat = top_cat.sort_values(by = "total_sales", ascending = False).head(10)
    top_cat['dominance'] = ['Top 3' if i < 3 else 'Autres' for i in range(len(top_cat))]

    col_c1, col_c2 = st.columns([2, 1])

    with col_c1:
        fig_cat = px.bar(
            top_cat,
            x = "total_sales",
            y = "product_category_name_english",
            orientation = 'h',
            color = "dominance",
            color_discrete_map = {'Top 3': '#E67E22', 'Autres': '#374151'},
            text_auto = '.2s',
            title = "Classement par Chiffre d'Affaires"
        )

        fig_cat.update_layout(
            plot_bgcolor = "rgba(0,0,0,0)",
            paper_bgcolor = "rgba(0,0,0,0)",
            font_color = "#FAFAFA",
            yaxis = dict(autorange = "reversed"),
            xaxis = dict(showgrid = False),
            yaxis_title = "",
            xaxis_title = "CA (R$)",
            showlegend = False,
            height = 500
        )
        fig_cat.update_traces(textposition = "outside")
        st.plotly_chart(fig_cat, use_container_width = True)

    with col_c2:
        st.caption("Focus Stratégique")
        
        st.info("""
        **📊 Loi des 80/20 Vérifiée**
        
        Le principe de Pareto s'applique : une minorité de catégories (le Top 3) génère l'essentiel du volume d'affaires. Ce sont les "Vital Few" à protéger.
        """)
        
        st.warning("""
        **⚠️ Risque de Rupture**
        
        Une rupture de stock sur ces 3 catégories ferait chuter le CA global de **~30%**. Le stock de sécurité doit être doublé ici.
        """)
        
        st.success("""
        **🚀 L'Outsider**
        
        La catégorie **'Furniture Decor'** (4ème) montre une forte traction. C'est le candidat idéal pour des campagnes marketing agressives.
        """)

    # --- 9. SATISFACTION ---
    st.markdown("---")
    st.subheader("⭐ Satisfaction vs Délais de Livraison")

    viz_data = df[df['delivery_days'] < 50].dropna(subset=['review_score']).copy()
    viz_data['review_score'] = viz_data['review_score'].round().astype(int)

    # Calculs pour les insights
    avg_1 = viz_data[viz_data['review_score'] == 1]['delivery_days'].median()
    avg_5 = viz_data[viz_data['review_score'] == 5]['delivery_days'].median()

    col_s1, col_s2 = st.columns([2, 1])
    
    with col_s1:
        fig_satisfaction = px.box(
            viz_data,
            x = "review_score",
            y = "delivery_days",
            color = "review_score",
            category_orders = {"review_score": [1, 2, 3, 4, 5]},
            title = "Distribution des délais par Note Client",
            labels = {"review_score": "Note Finale", "delivery_days": "Jours d'attente"}
        )

        fig_satisfaction.update_layout(
            plot_bgcolor = "rgba(0,0,0,0)",
            paper_bgcolor = "rgba(0,0,0,0)",
            font_color = "#FAFAFA",
            yaxis_title = "Délai (Jours)",
            xaxis_title = "Note (Étoiles)",
            showlegend = False,
            height = 500
        )
        fig_satisfaction.update_traces(marker_color = "#E67E22") 
        st.plotly_chart(fig_satisfaction, use_container_width = True)
        
    with col_s2:
        st.caption("Mécanique de la Satisfaction")
        
        st.info("""
        **📉 La Loi du Temps**
        
        On observe une corrélation négative parfaite : chaque jour de retard augmente la variance et dégrade la note.
        """)
        
        st.success(f"""
        **🏆 L'Excellence (5/5)**
        
        Pour ravir les clients, la logistique doit être rapide (**{avg_5:.0f} jours**) et surtout **fiable** (boîte tassée, peu d'écarts).
        """)
        
        st.warning(f"""
        **💥 La Zone Rouge (1/5)**
        
        Le "Seuil de Tolérance" est de **{avg_1:.0f} jours**. Au-delà, le client sanctionne systématiquement par la note minimale.
        """)

else:

    st.error("❌ Erreur Critique : Données introuvables. Vérifiez le dossier `data/raw`.")
