"""
Olympic Performance Trends & Biometric Analytics Dashboard
===========================================================
A comprehensive, production-grade Streamlit application designed 
to ingest historical Olympic athlete data, parse complex trends, 
and visualize performance distributions across eras, teams, and disciplines.

Author: AI Analytics Engine
File: app.py
Required Libraries: streamlit, pandas, numpy, plotly
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. PAGE INITIALIZATION & CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Global Olympic Analytics Engine",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom injection of CSS to refine layout presentation and cards
st.markdown("""
    <style>
    .reportview-container .main .block-container{ padding-top: 1rem; }
    .metric-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 5px solid #1f77b4;
        margin-bottom: 15px;
    }
    .metric-val { font-size: 28px; font-weight: bold; color: #111; }
    .metric-lbl { font-size: 14px; color: #666; text-transform: uppercase; }
    </style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 2. OPTIMIZED DATA INGESTION & PIPELINE ARCHITECTURE
# -----------------------------------------------------------------------------
@st.cache_data(show_spinner="Optimizing dataset structures and caching matrices...")
def ingest_and_prepare_data():
    """
    Loads raw CSV data, resolves data types, generates advanced 
    calculated fields like BMI, and categories timelines into historical eras.
    """
    df = pd.read_csv("athlete_events.csv")
    
    # Generate Advanced Biometric Index: Body Mass Index (BMI)
    # Formula: Weight (kg) / [Height (m)]^2
    df['BMI'] = df['Weight'] / ((df['Height'] / 100) ** 2)
    
    # Feature Engineering: Geopolitical Era Segments
    def segment_era(year):
        if year < 1914:
            return "Early Modern Era (1896-1912)"
        elif year <= 1948:
            return "World Wars Transition (1920-1948)"
        elif year <= 1992:
            return "Cold War & Global Expansion (1952-1992)"
        else:
            return "Contemporary Professional Era (1994-Present)"
            
    df['Historical_Era'] = df['Year'].apply(segment_era)
    
    # Standardize medal mappings for explicit prioritization ordering
    df['Medal_Weight'] = df['Medal'].map({'Gold': 3, 'Silver': 2, 'Bronze': 1}).fillna(0)
    
    return df

try:
    raw_df = ingest_and_prepare_data()
except FileNotFoundError:
    st.error("### 🚨 Crucial Data Asset Missing")
    st.info("Please ensure the source file `athlete_events.csv` resides within the execution root directory.")
    st.stop()


# -----------------------------------------------------------------------------
# 3. SIDEBAR NAVIGATION & FILTER CONTROL CONTROLLERS
# -----------------------------------------------------------------------------
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/5/5c/Olympic_rings_without_rims.svg", width=160)
st.sidebar.title("Navigation & Control")

# Primary Module Routing
app_mode = st.sidebar.selectbox(
    "Choose Analytic Module",
    [
        "📊 Executive Summary Hub",
        "🏆 Medal Laboratory & Dominance",
        "🧬 Biometric & Demographic Shifts",
        "🎯 Discipline Archetypes Tracker",
        "🔍 Granular Data Miner"
    ]
)

st.sidebar.markdown("---")
st.sidebar.subheader("Global Data Sub-Setting")

# Season Segmenting
seasons = raw_df['Season'].dropna().unique().tolist()
selected_seasons = st.sidebar.multiselect("Filter by Season", seasons, default=seasons)

# Year Coordinate Range Slider
min_y, max_y = int(raw_df['Year'].min()), int(raw_df['Year'].max())
year_range = st.sidebar.slider("Select Timeline Bounds", min_y, max_y, (min_y, max_y))

# Cohort Gender Categorization
genders = {'Male Only': ['M'], 'Female Only': ['F'], 'All Athletes': ['M', 'F']}
gender_choice = st.sidebar.radio("Cohort Demographics", list(genders.keys()), index=2)

# Execution of Global Masking Array
filtered_df = raw_df[
    (raw_df['Season'].isin(selected_seasons)) &
    (raw_df['Year'] >= year_range[0]) &
    (raw_df['Year'] <= year_range[1]) &
    (raw_df['Sex'].isin(genders[gender_choice]))
]


# -----------------------------------------------------------------------------
# 4. MODULE 1: EXECUTIVE SUMMARY HUB
# -----------------------------------------------------------------------------
if app_mode == "📊 Executive Summary Hub":
    st.markdown("# 📊 Executive Summary Hub")
    st.markdown("Macro-level historical KPI assessment and multi-decade dynamic metrics.")
    st.write("---")
    
    # Pre-calculate strings to bypass layout spacing issues within HTML tags
    tot_entries = f"{filtered_df['ID'].nunique():,}"
    uniq_comps = f"{filtered_df['Event'].nunique():,}"
    part_nocs = f"{filtered_df['NOC'].nunique():,}"
    tot_medals = f"{filtered_df['Medal'].notna().sum():,}"

    # Structural Implementation of Performance KPI Matrix Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-lbl'>Total Athlete Entries</div>
            <div class='metric-val'>{tot_entries}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-lbl'>Unique Competitions</div>
            <div class='metric-val'>{uniq_comps}</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-lbl'>Participating NOCs</div>
            <div class='metric-val'>{part_nocs}</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-lbl'>Total Medals Awarded</div>
            <div class='metric-val'>{tot_medals}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("### 📈 Chronological Footprint & Structural Progression")
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("Expansion Profile of Unique Disciplines")
        growth_df = filtered_df.groupby('Year').agg({
            'Sport': 'nunique',
            'Event': 'nunique',
            'NOC': 'nunique'
        }).reset_index()
        
        fig_growth = go.Figure()
        fig_growth.add_trace(go.Scatter(x=growth_df['Year'], y=growth_df['Sport'], name='Sports Count', line=dict(color='#1f77b4', width=3)))
        fig_growth.add_trace(go.Scatter(x=growth_df['Year'], y=growth_df['Event'], name='Specific Events', line=dict(color='#ff7f0e', width=2, dash='dash')))
        fig_growth.update_layout(title="Volume of Sports & Events Over Time", template="plotly_white", xaxis_title="Year", yaxis_title="Count")
        st.plotly_chart(fig_growth, use_container_width=True)

    with col_b:
        st.subheader("Proportional Footprint of Gender Diversity")
        gender_timeline = filtered_df.groupby(['Year', 'Sex'])['ID'].nunique().unstack().fillna(0).reset_index()
        if 'F' not in gender_timeline.columns: gender_timeline['F'] = 0
        if 'M' not in gender_timeline.columns: gender_timeline['M'] = 0
        
        fig_gen = go.Figure()
        fig_gen.add_trace(go.Bar(x=gender_timeline['Year'], y=gender_timeline['M'], name='Male Competitors', marker_color='#2ca02c'))
        fig_gen.add_trace(go.Bar(x=gender_timeline['Year'], y=gender_timeline['F'], name='Female Competitors', marker_color='#e377c2'))
        fig_gen.update_layout(barmode='stack', title="Athlete Volume Distributed Chronologically", template="plotly_white", xaxis_title="Year", yaxis_title="Roster Sizes")
        st.plotly_chart(fig_gen, use_container_width=True)

    st.markdown("### 🌍 Topography of Host Geographies")
    city_map = filtered_df.groupby(['City', 'Season']).agg({'Year': 'nunique', 'Sport': 'count'}).reset_index()
    city_map.columns = ['Host City', 'Season', 'Occurrences Hosted', 'Total Athlete Interactions']
    st.dataframe(city_map.sort_values(by='Occurrences Hosted', ascending=False).reset_index(drop=True), use_container_width=True)


# -----------------------------------------------------------------------------
# 5. MODULE 2: MEDAL LABORATORY & DOMINANCE
# -----------------------------------------------------------------------------
elif app_mode == "🏆 Medal Laboratory & Dominance":
    st.markdown("# 🏆 Medal Laboratory & Dominance Models")
    st.markdown("Evaluating podium efficiencies, team concentration profiles, and historical tallies.")
    st.write("---")
    
    medals_only_df = filtered_df.dropna(subset=['Medal'])
    
    if medals_only_df.empty:
        st.warning("The active filters yielded no medal events. Adjust the year or season parameters in the sidebar.")
    else:
        tab_tallies, tab_efficiency, tab_legends = st.tabs(["Leaderboards", "NOC Efficiency", "Elite Competitors"])
        
        with tab_tallies:
            st.subheader("Absolute Regional Podium Dominance Matrix")
            noc_pivot = medals_only_df.groupby(['Team', 'Medal']).size().unstack(fill_value=0)
            available_medals = [m for m in ['Gold', 'Silver', 'Bronze'] if m in noc_pivot.columns]
            noc_pivot = noc_pivot[available_medals]
            noc_pivot['Total_Medals'] = noc_pivot.sum(axis=1)
            noc_pivot = noc_pivot.sort_values(by='Total_Medals', ascending=False).head(15).reset_index()
            
            fig_bar_tallies = px.bar(
                noc_pivot, x='Team', y=available_medals,
                title="Top 15 Teams Ranked by Composite Medals Count",
                color_discrete_map={'Gold': '#FFD700', 'Silver': '#C0C0C0', 'Bronze': '#CD7F32'},
                barmode='stack', template='plotly_white'
            )
            st.plotly_chart(fig_bar_tallies, use_container_width=True)
            
        with tab_efficiency:
            st.subheader("Efficiency Index: Medals Won vs Total Athletes Dispatched")
            st.write("Measures how effectively a nation secures podium placements relative to their delegation size.")
            
            delegation_size = filtered_df.groupby('Team')['ID'].count().reset_index(name='Roster_Size')
            medal_size = medals_only_df.groupby('Team')['Medal'].count().reset_index(name='Medal_Count')
            
            efficiency_merge = pd.merge(delegation_size, medal_size, on='Team')
            efficiency_merge = efficiency_merge[efficiency_merge['Roster_Size'] > 100]
            efficiency_merge['Conversion_Rate'] = (efficiency_merge['Medal_Count'] / efficiency_merge['Roster_Size']) * 100
            efficiency_merge = efficiency_merge.sort_values(by='Conversion_Rate', ascending=False).head(20)
            
            fig_eff = px.scatter(
                efficiency_merge, x='Roster_Size', y='Medal_Count', size='Conversion_Rate',
                hover_name='Team', text='Team', color='Conversion_Rate', color_continuous_scale='Plasma',
                title='Top 20 Nations Podiums Yield Ratio (Min 100 Athlete Outings)',
                labels={'Roster_Size': 'Total Campaign Roster Size', 'Medal_Count': 'Podiums Claimed'},
                template='plotly_white'
            )
            fig_eff.update_traces(textposition='top center')
            st.plotly_chart(fig_eff, use_container_width=True)
            
        with tab_legends:
            st.subheader("Elite Olympian Hall of Fame")
            athlete_medals = medals_only_df.groupby(['Name', 'Team', 'Sport']).agg(
                Gold_Count=('Medal', lambda x: (x == 'Gold').sum()),
                Silver_Count=('Medal', lambda x: (x == 'Silver').sum()),
                Bronze_Count=('Medal', lambda x: (x == 'Bronze').sum()),
                Total_Podiums=('Medal', 'count')
            ).reset_index()
            
            top_legends = athlete_medals.sort_values(by=['Gold_Count', 'Total_Podiums'], ascending=False).head(20).reset_index(drop=True)
            st.table(top_legends)


# -----------------------------------------------------------------------------
# 6. MODULE 3: BIOMETRIC & DEMOGRAPHIC SHIFTS
# -----------------------------------------------------------------------------
elif app_mode == "🧬 Biometric & Demographic Shifts":
    st.markdown("# 🧬 Biometric & Demographic Shift Regressions")
    st.markdown("Plotting long-term adaptations in age distributions, height arrays, weight constraints, and BMI.")
    st.write("---")
    
    st.subheader("Decade-by-Decade Demographic Evolutions")
    bio_metric_option = st.selectbox("Select Target Biometric Variable", ["Age", "Height", "Weight", "BMI"])
    
    clean_bio = filtered_df.dropna(subset=[bio_metric_option])
    
    if clean_bio.empty:
        st.error("No valid entries containing that selection metric are available.")
    else:
        fig_violin = px.violin(
            clean_bio, x="Historical_Era", y=bio_metric_option, color="Sex",
            box=True, points="outliers",
            title=f"Evolutionary Distribution of {bio_metric_option} Across Geopolitical Eras",
            color_discrete_map={'M': '#4682B4', 'F': '#FF69B4'},
            template='plotly_white', category_orders={"Historical_Era": [
                "Early Modern Era (1896-1912)",
                "World Wars Transition (1920-1948)",
                "Cold War & Global Expansion (1952-1992)",
                "Contemporary Professional Era (1994-Present)"
            ]}
        )
        st.plotly_chart(fig_violin, use_container_width=True)
        
    st.markdown("### 📉 Longitudinal Trajectory Analysis")
    col_left_bio, col_right_bio = st.columns(2)
    
    with col_left_bio:
        st.subheader("Mean Age Shifts Across Centuries")
        age_trend = clean_bio.groupby(['Year', 'Sex'])['Age'].mean().reset_index()
        fig_age_line = px.line(age_trend, x='Year', y='Age', color='Sex', markers=True,
                               title='Average Age Changes Over Time',
                               color_discrete_map={'M': '#4682B4', 'F': '#FF69B4'}, template='plotly_white')
        st.plotly_chart(fig_age_line, use_container_width=True)
        
    with col_right_bio:
        st.subheader("Physical Build Scatter Index: Height vs. Weight Correlations")
        scatter_sample = filtered_df.dropna(subset=['Height', 'Weight'])
        if len(scatter_sample) > 8000:
            scatter_sample = scatter_sample.sample(8000, random_state=42)
            st.caption("⚠️ Displaying a balanced sample dataset of 8,000 records for optimal cross-filtering rendering speed.")
            
        fig_bi_scatter = px.scatter(
            scatter_sample, x="Height", y="Weight", color="Sex", opacity=0.4,
            hover_data=['Sport', 'Year', 'Name'],
            title="Height-Weight Cross Interaction Mapping",
            labels={'Height': 'Height (Centimeters)', 'Weight': 'Weight (Kilograms)'},
            color_discrete_map={'M': '#4682B4', 'F': '#FF69B4'}, template='plotly_white'
        )
        st.plotly_chart(fig_bi_scatter, use_container_width=True)


# -----------------------------------------------------------------------------
# 7. MODULE 4: DISCIPLINE ARCHETYPES TRACKER
# -----------------------------------------------------------------------------
elif app_mode == "🎯 Discipline Archetypes Tracker":
    st.markdown("# 🎯 Discipline Archetypes Tracker")
    st.markdown("Isolating sports-specific physical benchmarks and regional core competencies.")
    st.write("---")
    
    available_sports = sorted(filtered_df['Sport'].dropna().unique())
    
    if not available_sports:
        st.warning("No sports data found matching the selected global sidebar limits.")
    else:
        col_ctrl1, col_ctrl2 = st.columns(2)
        with col_ctrl1:
            target_sport = st.selectbox("Select Target Sport Category", available_sports, index=0)
        with col_ctrl2:
            comp_metric = st.selectbox("Physical Benchmark Profiler", ["Height", "Weight", "Age", "BMI"])
            
        sport_subset = filtered_df[filtered_df['Sport'] == target_sport]
        
        st.markdown(f"### 📊 Physical Phenotype Analysis for Olympic {target_sport}")
        
        col_sp1, col_sp2 = st.columns([3, 2])
        
        with col_sp1:
            fig_sport_hist = px.histogram(
                sport_subset.dropna(subset=[comp_metric]), x=comp_metric, color="Sex",
                marginal="box", barmode="overlay", nbins=30,
                title=f"Density Index for {comp_metric} in {target_sport}",
                color_discrete_map={'M': '#008080', 'F': '#FF7F50'}, template='plotly_white'
            )
            st.plotly_chart(fig_sport_hist, use_container_width=True)
            
        with col_sp2:
            st.markdown(f"**Descriptive Statistics Summary ({target_sport})**")
            stats_summary = sport_subset.groupby('Sex')[comp_metric].agg(['count', 'mean', 'std', 'min', 'max']).rename(
                columns={'count': 'Rosters Checked', 'mean': 'Mean Value', 'std': 'Std Dev', 'min': 'Minimum', 'max': 'Maximum'}
            ).T
            st.dataframe(stats_summary, use_container_width=True)
            
        st.write("---")
        st.markdown(f"### 🗺️ Geopolitical Dominance Concentration in {target_sport}")
        
        sport_medals = sport_subset.dropna(subset=['Medal'])
        if sport_medals.empty:
            st.info(f"No podium placements have records logged for {target_sport} with your active filters.")
        else:
            col_sd1, col_sd2 = st.columns(2)
            
            with col_sd1:
                dom_df = sport_medals['Team'].value_counts().head(10).reset_index()
                dom_df.columns = ['Country/Team', 'Podiums Claimed']
                fig_dom_bar = px.bar(
                    dom_df, x='Podiums Claimed', y='Country/Team', orientation='h',
                    title=f"Top 10 Global Leaders: {target_sport}",
                    color='Podiums Claimed', color_continuous_scale='Viridis', template='plotly_white'
                )
                fig_dom_bar.update_layout(yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig_dom_bar, use_container_width=True)
                
            with col_sd2:
                top_country_name = dom_df.iloc[0]['Country/Team']
                top_country_medals = sport_medals[sport_medals['Team'] == top_country_name]
                
                fig_pie_shares = px.pie(
                    top_country_medals, names='Medal',
                    title=f"Medal Split Configuration for {top_country_name} ({target_sport})",
                    color='Medal', color_discrete_map={'Gold': '#FFD700', 'Silver': '#C0C0C0', 'Bronze': '#CD7F32'},
                    hole=0.4, template='plotly_white'
                )
                st.plotly_chart(fig_pie_shares, use_container_width=True)


# -----------------------------------------------------------------------------
# 8. MODULE 5: GRANULAR DATA MINER
# -----------------------------------------------------------------------------
elif app_mode == "🔍 Granular Data Miner":
    st.markdown("# 🔍 Granular Data Miner & Matrix Engine")
    st.markdown("Query, isolate, slicing multi-parameter constraints, and export target CSV structures.")
    st.write("---")
    
    st.subheader("Multi-Parameter Query Matrix Block")
    
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        search_noc = st.multiselect("Isolate Specific NOC Region Codes", sorted(filtered_df['NOC'].dropna().unique().tolist()))
    with col_m2:
        search_sport = st.multiselect("Isolate Target Sports Framework", sorted(filtered_df['Sport'].dropna().unique().tolist()))
    with col_m3:
        search_medal = st.multiselect("Podium Target Layering", ['Gold', 'Silver', 'Bronze'])
        
    mined_df = filtered_df.copy()
    if search_noc:
        mined_df = mined_df[mined_df['NOC'].isin(search_noc)]
    if search_sport:
        mined_df = mined_df[mined_df['Sport'].isin(search_sport)]
    if search_medal:
        mined_df = mined_df[mined_df['Medal'].isin(search_medal)]
        
    text_search = st.text_input("Regex/Keyword Search Athlete Names or Specific Team Strings:", "")
    if text_search:
        mined_df = mined_df[
            mined_df['Name'].str.contains(text_search, case=False, na=False) |
            mined_df['Team'].str.contains(text_search, case=False, na=False)
        ]
        
    st.markdown(f"#### Data Output Stream Result Matrix: **{len(mined_df):,} matching rows found**")
    st.dataframe(mined_df.head(500), use_container_width=True)
    
    st.markdown("### 📥 Compile Package and Download Deployment Extract")
    st.write("Extract the slice rendered below down into external analysis engines like R, Excel, or local files.")
    
    csv_payload = mined_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⚡ Export Current Filtered Slices via CSV",
        data=csv_payload,
        file_name="mined_olympic_performance_extract.csv",
        mime="text/csv"
    )

# -----------------------------------------------------------------------------
# 9. PERSISTENT UTILITY SYSTEM SIGNALS
# -----------------------------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.caption("⚙️ Framework Version Architecture Engine v4.2.0")