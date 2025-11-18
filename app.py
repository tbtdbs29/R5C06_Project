import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(
    page_title="Analyse des Sports en France",
    page_icon="📈",
    layout="wide"
)

# --- FONCTIONS DE CHARGEMENT ET DE TRAITEMENT ---
@st.cache_data
def load_data(filepath):
    """
    Charge le fichier CSV et effectue un pré-traitement léger si nécessaire.
    """
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        st.error(f"Le fichier '{filepath}' est introuvable. Assurez-vous qu'il est dans le même dossier.")
        return pd.DataFrame()


def get_age_columns(df):
    """Identifie les colonnes d'âge pour hommes et femmes."""
    # On cherche les colonnes qui contiennent 'ans' et qui commencent par F ou H
    cols = [c for c in df.columns if 'ans' in c and ('F -' in c or 'H -' in c)]
    return cols

def prepare_demographics_data(df_filtered):
    """
    Agrège les données par âge et genre pour le dataframe filtré (ex: un sport spécifique).
    Optimisé pour ne pas 'melt' tout le dataset énorme.
    """
    age_cols = get_age_columns(df_filtered)
    
    # Faire la somme sur les colonnes d'âge
    sums = df_filtered[age_cols].sum().reset_index()
    sums.columns = ['column_name', 'count']
    
    # Extraire Genre et Tranche d'âge
    # Format attendu: "F - 1 à 4 ans"
    sums['Genre'] = sums['column_name'].apply(lambda x: 'Femme' if x.startswith('F') else 'Homme')
    sums['Age'] = sums['column_name'].apply(lambda x: x.split(' - ')[1])
    
    return sums

# --- Streamlit interface ---

def main():
    st.title("Dashboard Interactif des Sports")
    st.markdown("""
    Cette application permet d'analyser la répartition des licences sportives en France
    selon les régions, les sports et la démographie (âge/genre).
    """)

    # Chargement des données
    FILE_PATH = 'project/src/clean/out/clean_sports.csv' # data/lite_clean.csv
    df = load_data(FILE_PATH)

    if df.empty:
        return

    # --- SIDEBAR (Filtres Globaux) ---
    st.sidebar.header("Filtres Globaux")
    
    # Choix de la colonne de nom de sport 
    use_standard_names = st.sidebar.checkbox("Utiliser noms standardisés", value=True)
    sport_col = 'sport' if use_standard_names and 'sport' in df.columns else 'federation'

    # Filtre Régions 
    all_regions = sorted(df['region'].unique())
    selected_regions = st.sidebar.multiselect(
        "Filtrer par Région(s)",
        all_regions,
        default=all_regions
    )
    
    # Appliquer le filtre de région au dataframe global
    df_filtered = df[df['region'].isin(selected_regions)]
    
    st.sidebar.markdown("---")
    st.sidebar.info(f"Données chargées : {len(df)} communes / clubs")

    # --- ONGLETS (TABS) ---
    tab1, tab2, tab3 = st.tabs(["Top Sports (National)", "Analyse Régionale", "Âge & Genre"])

    # === TAB 1: TOP SPORTS ===
    with tab1:
        st.header("Sports les plus pratiqués en France")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            nb_top = st.slider("Nombre de sports à afficher", min_value=5, max_value=50, value=10)
            show_metric = st.radio("Métrique", ["Total Licenciés", "Hommes", "Femmes"])
            
            metric_col = 'total'
            if show_metric == "Hommes": metric_col = 'h_count'
            if show_metric == "Femmes": metric_col = 'f_count'

        with col2:
            # Agrégation
            top_sports = df_filtered.groupby(sport_col)[metric_col].sum().sort_values(ascending=False).head(nb_top).reset_index()
            
            fig_top = px.bar(
                top_sports, 
                x=metric_col, 
                y=sport_col, 
                orientation='h',
                title=f"Top {nb_top} Sports ({show_metric})",
                text_auto=True,
                color=metric_col,
                color_continuous_scale='Viridis'
            )
            fig_top.update_layout(yaxis={'categoryorder':'total ascending'}) # Trie du plus grand au plus petit
            st.plotly_chart(fig_top, use_container_width=True)

    # === TAB 2: ANALYSE RÉGIONALE ===
    with tab2:
        st.header("Focus par Région")
        
        # Input spécifique à ce graph
        region_choice = st.selectbox("Choisir une région à analyser", all_regions)
        
        # Filtrer sur la région choisie
        df_region = df[df['region'] == region_choice]
        
        col_r1, col_r2 = st.columns(2)
        
        with col_r1:
            st.subheader(f"Top 10 Sports en {region_choice}")
            top_sports_region = df_region.groupby(sport_col)['total'].sum().sort_values(ascending=False).head(10).reset_index()
            
            fig_region_bar = px.bar(
                top_sports_region,
                x=sport_col,
                y='total',
                color='total',
                title=f"Licenciés par sport ({region_choice})"
            )
            st.plotly_chart(fig_region_bar, use_container_width=True)
            
        with col_r2:
            st.subheader("Répartition Hommes / Femmes (Global Région)")
            total_h = df_region['h_count'].sum()
            total_f = df_region['f_count'].sum()
            
            fig_pie = px.pie(
                names=['Hommes', 'Femmes'],
                values=[total_h, total_f],
                title=f"Parité en {region_choice}",
                color_discrete_sequence=px.colors.qualitative.Set1
            )
            st.plotly_chart(fig_pie, use_container_width=True)

    # === TAB 3: DÉMOGRAPHIE (ÂGE ET GENRE) ===
    with tab3:
        st.header("Pyramide des âges par Sport")
        
        # Input : Choix du sport
        # On prend la liste des sports disponibles
        available_sports = sorted(df_filtered[sport_col].unique())
        selected_sport = st.selectbox("Sélectionnez un sport pour voir la démographie", available_sports, index=0)
        
        # Filtrer les données pour ce sport
        df_sport_demo = df_filtered[df_filtered[sport_col] == selected_sport]
        
        if not df_sport_demo.empty:
            # Préparer les données (Melt intelligent)
            data_demo = prepare_demographics_data(df_sport_demo)
            
            # Ordre des âges (Important pour que le graph soit dans le bon ordre)
            # On définit l'ordre manuellement pour éviter le tri alphabétique (10 avant 5)
            age_order = [
                '1 à 4 ans', '5 à 9 ans', '10 à 14 ans', '15 à 19 ans', '20 à 24 ans', 
                '25 à 29 ans', '30 à 34 ans', '35 à 39 ans', '40 à 44 ans', '45 à 49 ans', 
                '50 à 54 ans', '55 à 59 ans', '60 à 64 ans', '65 à 69 ans', '70 à 74 ans', 
                '75 à 79 ans', '80 à 99 ans'
            ]
            
            # Graphique
            fig_demo = px.bar(
                data_demo,
                x='Age',
                y='count',
                color='Genre',
                barmode='group', # 'group' pour côte à côte, 'relative' pour empilé
                title=f"Répartition par Âge et Genre : {selected_sport}",
                category_orders={"Age": age_order}, # Force l'ordre des âges
                color_discrete_map={"Homme": "blue", "Femme": "pink"}
            )
            st.plotly_chart(fig_demo, use_container_width=True)
        else:
            st.warning("Pas de données disponibles pour ce sport.")

if __name__ == "__main__":
    main()