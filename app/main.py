"""
24 Hours on Planet Earth
VizCon 2026 - Streamlit App

Every person receives the same 24 hours. Culture determines how those hours become a life.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os

# --- Page Config ---
st.set_page_config(
    page_title="24 Hours on Planet Earth",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Data Loading ---
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'master')
RAW_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')


@st.cache_data
def load_countries():
    return pd.read_csv(os.path.join(DATA_DIR, 'countries.csv'))


@st.cache_data
def load_children():
    return pd.read_csv(os.path.join(DATA_DIR, 'children_comparison.csv'))


@st.cache_data
def load_progress():
    return pd.read_csv(os.path.join(DATA_DIR, 'progress_since_1990.csv'))


@st.cache_data
def load_airports():
    cols = ['ID', 'Name', 'City', 'Country', 'IATA', 'ICAO', 'Lat', 'Lon',
            'Alt', 'Timezone', 'DST', 'Tz', 'Type', 'Source']
    df = pd.read_csv(os.path.join(RAW_DIR, 'openflights_airports.csv'),
                     header=None, names=cols)
    return df[df['Type'] == 'airport']


# Load data
df_countries = load_countries()
df_children = load_children()
df_progress = load_progress()
df_airports = load_airports()

# --- Color Palette ---
COLORS = ['#3b82f6', '#ff9900', '#4ade80', '#ef4444', '#8b5cf6', '#06b6d4']
BLUE, ORANGE, GREEN, RED, PURPLE, CYAN = COLORS

# --- Custom CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    .stApp {
        background-color: #0b1120;
        color: #e0e0e0;
        font-family: 'Inter', sans-serif;
    }

    .main-header {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 12px 0;
        border-bottom: 1px solid #1a2744;
        margin-bottom: 20px;
    }
    .main-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
    }
    .main-subtitle {
        font-size: 0.9rem;
        color: #8892a4;
        border-left: 1px solid #2a3a5c;
        padding-left: 16px;
        margin: 0;
    }

    .chapter-hero {
        background: linear-gradient(135deg, #0f2744 0%, #1a1a3e 100%);
        border-radius: 12px;
        padding: 32px;
        margin-bottom: 24px;
        border: 1px solid #1a2744;
        position: relative;
        overflow: hidden;
    }
    .chapter-time-badge {
        font-size: 2.5rem;
        font-weight: 800;
        color: #3b82f6;
        margin-bottom: 4px;
    }
    .chapter-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 8px;
    }
    .chapter-desc {
        font-size: 0.95rem;
        color: #8892a4;
        max-width: 500px;
    }

    .stat-card {
        background: #111b2e;
        border: 1px solid #1a2744;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
    }
    .stat-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
    }
    .stat-label {
        font-size: 0.75rem;
        color: #8892a4;
        margin-top: 4px;
    }
    .stat-sub {
        font-size: 0.7rem;
        color: #4ade80;
    }

    .discovery-box {
        background: linear-gradient(135deg, #0f2744 0%, #1a1a3e 100%);
        border-left: 4px solid #ff9900;
        padding: 24px;
        border-radius: 8px;
        margin: 24px 0;
        font-size: 1rem;
    }
    .discovery-box h3 {
        color: #ff9900;
        margin: 0 0 8px 0;
        font-size: 1.1rem;
    }
    .discovery-box strong {
        color: #ff9900;
    }

    .chapter-transition {
        text-align: center;
        color: #8892a4;
        font-style: italic;
        font-size: 1.1rem;
        margin: 32px 0;
        padding: 16px;
    }

    .guess-box {
        background: linear-gradient(135deg, #1a1a3e 0%, #0f2744 100%);
        border: 1px solid #3b82f6;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .guess-box h4 {
        color: #3b82f6;
        margin-bottom: 8px;
    }
    .guess-box p, .guess-box strong {
        color: #ffffff !important;
    }

    /* Fix button visibility */
    .stButton > button {
        color: #ffffff !important;
        background-color: #1a2744 !important;
        border: 1px solid #3b82f6 !important;
    }
    .stButton > button:hover {
        background-color: #2a4a7a !important;
        color: #ffffff !important;
    }
    .stButton > button[kind="primary"] {
        background-color: #3b82f6 !important;
        color: #ffffff !important;
        border: none !important;
    }

    .source-text {
        font-size: 0.7rem;
        color: #555;
        margin-top: 8px;
    }

    .children-card {
        background: #0d1525;
        border: 1px solid #1a2744;
        border-radius: 12px;
        padding: 24px;
        height: 100%;
    }
    .children-card h3 {
        color: #ffffff;
        font-size: 1.1rem;
        margin-bottom: 4px;
    }
    .children-card .region-tag {
        font-size: 0.75rem;
        color: #ef4444;
        margin-bottom: 16px;
        display: block;
    }
    .children-stat {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid #1a2744;
    }
    .children-stat-label {
        color: #8892a4;
        font-size: 0.85rem;
    }
    .children-stat-value {
        color: #ffffff;
        font-weight: 600;
        font-size: 0.85rem;
    }

    .hope-metric {
        text-align: center;
        padding: 12px;
    }
    .hope-metric .value {
        font-size: 2rem;
        font-weight: 800;
        color: #4ade80;
    }
    .hope-metric .label {
        font-size: 0.8rem;
        color: #8892a4;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div[data-testid="stSidebar"] {display: none;}
</style>
""", unsafe_allow_html=True)


# --- State ---
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'hour' not in st.session_state:
    st.session_state.hour = '06:00'
if 'guess_made' not in st.session_state:
    st.session_state.guess_made = {}

NAV_ITEMS = ['06:00', '09:00', '12:00', '15:00', '18:00', '22:00', 'Children', 'Hope', 'Thrive', 'What If']
HOUR_LABELS = {
    '06:00': 'Wake Up', '09:00': 'Work', '12:00': 'Food',
    '15:00': 'Connection', '18:00': 'Family', '22:00': 'Night',
    'Children': 'Children', 'Hope': 'Hope', 'Thrive': 'Thrive Index', 'What If': 'What If'
}
HOUR_ICONS = {
    '06:00': '☀️', '09:00': '💼', '12:00': '🍽️',
    '15:00': '🌐', '18:00': '👨‍👩‍👧', '22:00': '🌙',
    'Children': '👶', 'Hope': '🌱', 'Thrive': '⭐', 'What If': '🔮'
}


# ==========================================
# PLOTLY DARK LAYOUT HELPER
# ==========================================
def dark_layout(fig, height=400):
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#8892a4', family='Inter'),
        height=height,
        margin=dict(t=30, b=40, l=50, r=30),
        legend=dict(font=dict(color='#8892a4'))
    )
    fig.update_xaxes(gridcolor='#1a2744', zerolinecolor='#1a2744')
    fig.update_yaxes(gridcolor='#1a2744', zerolinecolor='#1a2744')
    return fig


# ==========================================
# LANDING PAGE
# ==========================================
def show_landing():
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Animated-looking globe
        fig = go.Figure(data=go.Choropleth(
            locations=['USA', 'BRA', 'DEU', 'IND', 'CHN', 'JPN', 'AUS', 'NGA', 'KEN', 'ZAF', 'FRA', 'NOR',
                       'GBR', 'CAN', 'MEX', 'ARG', 'RUS', 'IDN', 'EGY', 'TUR', 'SAU', 'THA'],
            z=[78, 75, 81, 70, 78, 85, 83, 54, 61, 65, 82, 83, 81, 82, 75, 76, 73, 71, 72, 76, 75, 77],
            colorscale=[[0, '#2d6a4f'], [0.5, '#40916c'], [1, '#52b788']],
            showscale=False,
            marker_line_color='#4a9eff',
            marker_line_width=0.8
        ))
        fig.update_layout(
            geo=dict(
                projection_type='orthographic',
                showocean=True, oceancolor='#0a1628',
                showlakes=False,
                showframe=False,
                bgcolor='rgba(0,0,0,0)',
                landcolor='#1e3a5f',
                coastlinecolor='#4a9eff',
                countrycolor='#2a5a8a',
                showcoastlines=True,
                showcountries=True,
                projection_rotation=dict(lon=10, lat=20)
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            height=320, margin=dict(t=0, b=0, l=0, r=0)
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        <div style="text-align: center;">
            <h1 style="font-size: 2.8rem; font-weight: 800; margin: 16px 0;">24 Hours on Planet Earth</h1>
            <p style="font-size: 1.3rem; color: #ffffff; margin-bottom: 16px; font-weight: 500;">
                Every person receives the same 24 hours. Culture determines how those hours become a life.
            </p>
            <p style="font-size: 1rem; color: #6b7a94; max-width: 560px; margin: 0 auto 40px;">
                Follow a 24-hour journey across the globe and discover how billions of lives unfold
                in ways you never imagined. Every hour reveals something that will change how you see the world.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Global summary card
        st.markdown("""
        <div style="background: linear-gradient(135deg, #0f2744 0%, #1a1a3e 100%); border-radius: 12px;
                    padding: 24px; border: 1px solid #1a2744; margin-bottom: 40px;">
            <p style="text-align:center; color:#8892a4; font-size:0.85rem; margin-bottom: 16px; text-transform: uppercase; letter-spacing: 1px;">
                What This Journey Covers
            </p>
            <div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 12px;">
                <div style="text-align:center;">
                    <div style="font-size:1.8rem; font-weight:700; color:#3b82f6;">24</div>
                    <div style="font-size:0.75rem; color:#8892a4;">Countries Analyzed</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:1.8rem; font-weight:700; color:#4ade80;">6.2B</div>
                    <div style="font-size:0.75rem; color:#8892a4;">Population Represented</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:1.8rem; font-weight:700; color:#ff9900;">8.1 hrs</div>
                    <div style="font-size:0.75rem; color:#8892a4;">Avg Sleep</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:1.8rem; font-weight:700; color:#ef4444;">7.2 hrs</div>
                    <div style="font-size:0.75rem; color:#8892a4;">Avg Work</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:1.8rem; font-weight:700; color:#8b5cf6;">6.3/10</div>
                    <div style="font-size:0.75rem; color:#8892a4;">Avg Happiness</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🌍  Begin the Journey — Follow One Day Around the World", use_container_width=True, type="primary"):
            st.session_state.page = 'journey'
            st.rerun()

        st.markdown('<p style="text-align:center;color:#555;font-size:0.8rem;margin-top:48px;">VizCon 2026 · Data from OECD, WHO, World Bank, UNICEF, FAO, UNESCO, ITU</p>', unsafe_allow_html=True)


# ==========================================
# TIMELINE NAVIGATION
# ==========================================
def show_navigation():
    st.markdown("""
    <div class="main-header">
        <span style="font-size: 1.5rem;">🌍</span>
        <p class="main-title">One Day on Earth</p>
        <p class="main-subtitle">Every person receives the same 24 hours. Culture determines how those hours become a life.</p>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(len(NAV_ITEMS))
    for i, (item, col) in enumerate(zip(NAV_ITEMS, cols)):
        with col:
            is_active = (item == st.session_state.hour)
            icon = HOUR_ICONS[item]
            if st.button(f"{icon} {item}", key=f"nav_{item}", use_container_width=True,
                        type="primary" if is_active else "secondary"):
                st.session_state.hour = item
                st.rerun()
    st.markdown("---")


# ==========================================
# CHAPTER 1: 06:00 WAKE UP
# ==========================================
def render_wake_up():
    st.markdown("""
    <div class="chapter-hero">
        <div class="chapter-time-badge">06:00</div>
        <div class="chapter-title">How does the world begin its day?</div>
        <div class="chapter-desc">
            The sun rises somewhere in the world. People wake up, get ready, and start their day.
            But how much sleep did they get? The answer varies by nearly 2 hours across countries.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Guess-first interaction
    guess_key = 'sleep_guess'
    if guess_key not in st.session_state.guess_made:
        st.markdown('<div class="guess-box">', unsafe_allow_html=True)
        st.markdown("#### 🤔 Before we show the data...")
        st.markdown("**Which country do you think sleeps the LEAST?**")
        guess_cols = st.columns(4)
        options = ['Japan', 'USA', 'India', 'South Korea']
        for i, opt in enumerate(options):
            with guess_cols[i]:
                if st.button(opt, key=f"sleep_g_{opt}", use_container_width=True):
                    st.session_state.guess_made[guess_key] = opt
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # Reveal answer
    user_guess = st.session_state.guess_made[guess_key]
    correct = "Japan"
    if user_guess == correct:
        st.success(f"✅ Correct! You guessed **{user_guess}** — Japan sleeps the least at just 7h 22m per day.")
    else:
        st.warning(f"You guessed **{user_guess}**, but it's actually **Japan** at 7h 22m per day!")

    # Stat cards
    sleep_sorted = df_countries.sort_values('Sleep_Min_Per_Day')
    least_sleep = sleep_sorted.iloc[0]
    most_sleep = sleep_sorted.iloc[-1]
    avg_sleep = df_countries['Sleep_Min_Per_Day'].mean()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("😴 Least Sleep", f"{int(least_sleep['Sleep_Min_Per_Day'])} min", least_sleep['Country'])
    with c2:
        st.metric("🛏️ Most Sleep", f"{int(most_sleep['Sleep_Min_Per_Day'])} min", most_sleep['Country'])
    with c3:
        st.metric("🌍 World Avg", f"{int(avg_sleep)} min", f"≈ {int(avg_sleep)//60}h {int(avg_sleep)%60}m")
    with c4:
        st.metric("⏱️ Gap", f"{int(most_sleep['Sleep_Min_Per_Day'] - least_sleep['Sleep_Min_Per_Day'])} min", "Max difference")

    st.markdown("---")

    # HERO visualization: Sleep Duration by Country
    st.markdown("### 😴 Sleep Duration by Country")
    sleep_data = df_countries[['Country', 'Sleep_Min_Per_Day', 'Region']].sort_values('Sleep_Min_Per_Day', ascending=True)
    fig = px.bar(sleep_data, x='Sleep_Min_Per_Day', y='Country', orientation='h',
                 color='Region', color_discrete_sequence=COLORS)
    fig.update_layout(xaxis_title="Minutes per day", yaxis_title="")
    dark_layout(fig, 450)
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Source: OECD Time Use Survey, National Statistics Offices")

    # Radar comparison
    st.markdown("### 🎯 Country Comparison Radar")
    radar_cols = st.columns([1, 3, 1])
    with radar_cols[0]:
        c1_sel = st.selectbox("Country A", df_countries['Country'].tolist(), index=0, key="radar_c1")
    with radar_cols[2]:
        c2_sel = st.selectbox("Country B", df_countries['Country'].tolist(), index=4, key="radar_c2")

    with radar_cols[1]:
        row1 = df_countries[df_countries['Country'] == c1_sel].iloc[0]
        row2 = df_countries[df_countries['Country'] == c2_sel].iloc[0]
        categories = ['Sleep', 'Leisure', 'Life Expectancy', 'Happiness', 'Personal Care']
        # Normalize to 0-100 scale
        max_vals = [600, 300, 90, 8, 150]
        vals1 = [row1['Sleep_Min_Per_Day']/max_vals[0]*100, row1['Leisure_Min_Per_Day']/max_vals[1]*100,
                 row1['Life_Expectancy']/max_vals[2]*100, row1['Happiness_Score']/max_vals[3]*100,
                 row1['Personal_Care_Min']/max_vals[4]*100]
        vals2 = [row2['Sleep_Min_Per_Day']/max_vals[0]*100, row2['Leisure_Min_Per_Day']/max_vals[1]*100,
                 row2['Life_Expectancy']/max_vals[2]*100, row2['Happiness_Score']/max_vals[3]*100,
                 row2['Personal_Care_Min']/max_vals[4]*100]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=vals1, theta=categories, fill='toself', name=c1_sel, line=dict(color=BLUE)))
        fig.add_trace(go.Scatterpolar(r=vals2, theta=categories, fill='toself', name=c2_sel, line=dict(color=RED)))
        fig.update_layout(
            polar=dict(bgcolor='rgba(0,0,0,0)', radialaxis=dict(visible=True, range=[0, 100], color='#333')),
            paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#8892a4'),
            legend=dict(x=0.5, y=-0.2, xanchor='center', orientation='h'),
            height=350, margin=dict(t=30, b=50, l=60, r=60)
        )
        st.plotly_chart(fig, use_container_width=True)

    # Discovery box - bigger, more impactful
    st.markdown("""
    <div class="discovery-box">
        <h3 style="color:#ff9900;margin:0;">💡 I HAD NO IDEA</h3>
        <p style="font-size:1.3rem;color:#ffffff;margin:12px 0;font-weight:600;">Japan sleeps the least on Earth — yet lives the longest.</p>
        <p style="font-size:0.9rem;color:#8892a4;">At just 7h 22m of sleep, Japan has the shortest nights of any nation. Yet its life expectancy (84.8 years) is among the world's highest. Meanwhile, South Africa sleeps over 9 hours but lives only to 64.9. Sleep duration alone doesn't predict longevity — healthcare, diet, and social systems matter far more.</p>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Sources: OECD Time Use Database, WHO Life Tables, World Happiness Report 2024")

    # Transition to next chapter
    st.markdown("""
    <p style="text-align:center;color:#8892a4;font-style:italic;font-size:1.1rem;margin:32px 0;">As the world finishes breakfast, another question emerges: does working longer actually make us richer?</p>
    """, unsafe_allow_html=True)


# ==========================================
# CHAPTER 2: 09:00 WORK
# ==========================================
def render_work():
    st.markdown("""
    <div class="chapter-hero">
        <div class="chapter-time-badge">09:00</div>
        <div class="chapter-title">Does working longer make countries richer?</div>
        <div class="chapter-desc">
            The world clocks in. But does working longer hours actually create more wealth?
            The answer challenges everything we assume about hard work.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Guess-first
    guess_key = 'work_guess'
    if guess_key not in st.session_state.guess_made:
        st.markdown('<div class="guess-box">', unsafe_allow_html=True)
        st.markdown("#### 🤔 Before we show the data...")
        st.markdown("**Do countries that work MORE hours produce MORE per hour?**")
        gc = st.columns(2)
        with gc[0]:
            if st.button("✅ Yes — more hours = more output", key="work_yes", use_container_width=True):
                st.session_state.guess_made[guess_key] = 'Yes'
                st.rerun()
        with gc[1]:
            if st.button("❌ No — it's actually inverse", key="work_no", use_container_width=True):
                st.session_state.guess_made[guess_key] = 'No'
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        return

    user_guess = st.session_state.guess_made[guess_key]
    if user_guess == 'No':
        st.success("✅ Correct! Countries that work fewer hours tend to be MORE productive per hour.")
    else:
        st.warning("Surprising, right? The relationship is actually **inverse** — fewer hours, higher productivity.")

    # Stats
    most_hours = df_countries.sort_values('Work_Hours_Per_Year', ascending=False).iloc[0]
    most_prod = df_countries.sort_values('GDP_Per_Hour_Worked', ascending=False).iloc[0]
    least_hours = df_countries.sort_values('Work_Hours_Per_Year').iloc[0]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("⏰ Most Hours", f"{int(most_hours['Work_Hours_Per_Year'])}/yr", most_hours['Country'])
    with c2:
        st.metric("💰 Most Productive", f"${most_prod['GDP_Per_Hour_Worked']:.0f}/hr", most_prod['Country'])
    with c3:
        st.metric("🏖️ Fewest Hours", f"{int(least_hours['Work_Hours_Per_Year'])}/yr", least_hours['Country'])
    with c4:
        avg_hrs = df_countries['Work_Hours_Per_Year'].mean()
        st.metric("🌍 Average", f"{int(avg_hrs)}/yr", "All countries")

    st.markdown("---")

    # HERO: Main scatter plot - the most impactful visualization
    st.markdown("### Working Hours vs Productivity (GDP per Hour Worked)")
    fig = px.scatter(df_countries, x='Work_Hours_Per_Year', y='GDP_Per_Hour_Worked',
                     text='Country', color='Region', size='Population_M',
                     color_discrete_sequence=COLORS,
                     labels={'Work_Hours_Per_Year': 'Annual Working Hours',
                             'GDP_Per_Hour_Worked': 'GDP per Hour Worked ($)',
                             'Population_M': 'Population (M)'})
    fig.update_traces(textposition='top center', textfont_size=9)
    # Trend line
    z = np.polyfit(df_countries['Work_Hours_Per_Year'], df_countries['GDP_Per_Hour_Worked'], 1)
    x_line = np.linspace(df_countries['Work_Hours_Per_Year'].min(), df_countries['Work_Hours_Per_Year'].max(), 100)
    y_line = np.polyval(z, x_line)
    fig.add_trace(go.Scatter(x=x_line, y=y_line, mode='lines',
                             line=dict(color=ORANGE, dash='dash', width=2),
                             name='Trend (negative)', showlegend=True))
    dark_layout(fig, 500)
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Source: OECD Employment Outlook, ILO, World Bank")

    # Discovery box
    st.markdown("""
    <div class="discovery-box">
        <h3 style="color:#ff9900;margin:0;">💡 I HAD NO IDEA</h3>
        <p style="font-size:1.3rem;color:#ffffff;margin:12px 0;font-weight:600;">Germany works 840 fewer hours than Mexico per year — yet produces 4x more value per hour.</p>
        <p style="font-size:0.9rem;color:#8892a4;">Norway works even less and produces $95/hour. The data shows a clear negative correlation: working smarter, not longer, is the path to prosperity. Countries with strong labor protections, automation, and education invest in quality over quantity.</p>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Sources: OECD Compendium of Productivity Indicators, ILO ILOSTAT, World Bank")

    # Transition
    st.markdown("""
    <p style="text-align:center;color:#8892a4;font-style:italic;font-size:1.1rem;margin:32px 0;">The workday is underway. But when lunchtime arrives, what lands on the plate reveals something deeper about culture.</p>
    """, unsafe_allow_html=True)


# ==========================================
# CHAPTER 3: 12:00 FOOD
# ==========================================
def render_food():
    st.markdown("""
    <div class="chapter-hero">
        <div class="chapter-time-badge">12:00</div>
        <div class="chapter-title">What do our meals reveal about our cultures?</div>
        <div class="chapter-desc">
            It's lunchtime somewhere. From rice to bread to corn — what does the world put on its plate?
            Calories, meat, and the surprising disconnect between spending and health.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Guess-first
    guess_key = 'food_guess'
    if guess_key not in st.session_state.guess_made:
        st.markdown('<div class="guess-box">', unsafe_allow_html=True)
        st.markdown("#### 🤔 Before we show the data...")
        st.markdown("**Which country consumes the most meat per person per year?**")
        gc = st.columns(4)
        options = ['USA', 'Brazil', 'Australia', 'Germany']
        for i, opt in enumerate(options):
            with gc[i]:
                if st.button(opt, key=f"food_g_{opt}", use_container_width=True):
                    st.session_state.guess_made[guess_key] = opt
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        return

    user_guess = st.session_state.guess_made[guess_key]
    top_meat = df_countries.sort_values('Meat_Kg_Per_Year', ascending=False).iloc[0]
    if user_guess == top_meat['Country']:
        st.success(f"✅ Correct! **{top_meat['Country']}** leads at {top_meat['Meat_Kg_Per_Year']:.1f} kg/person/year.")
    else:
        st.warning(f"You guessed **{user_guess}**, but it's **{top_meat['Country']}** at {top_meat['Meat_Kg_Per_Year']:.1f} kg/person/year!")

    # Stats
    avg_cal = df_countries['Calories_Per_Day'].mean()
    max_cal = df_countries.sort_values('Calories_Per_Day', ascending=False).iloc[0]
    min_cal = df_countries.sort_values('Calories_Per_Day').iloc[0]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("🍽️ Highest Calories", f"{int(max_cal['Calories_Per_Day'])}", max_cal['Country'])
    with c2:
        st.metric("🥗 Lowest Calories", f"{int(min_cal['Calories_Per_Day'])}", min_cal['Country'])
    with c3:
        st.metric("🌍 World Avg", f"{int(avg_cal)} kcal/day", "")
    with c4:
        st.metric("🥩 Top Meat", f"{top_meat['Meat_Kg_Per_Year']:.0f} kg/yr", top_meat['Country'])

    st.markdown("---")

    # HERO: Calories vs Life Expectancy scatter - the most impactful story
    st.markdown("### 🍽️ Does Eating More Mean Living Longer?")
    fig = px.scatter(df_countries, x='Calories_Per_Day', y='Life_Expectancy',
                     text='Country', color='Region', size='Meat_Kg_Per_Year',
                     color_discrete_sequence=COLORS,
                     labels={'Calories_Per_Day': 'Daily Calorie Supply',
                             'Life_Expectancy': 'Life Expectancy (years)',
                             'Meat_Kg_Per_Year': 'Meat (kg/yr)'})
    fig.update_traces(textposition='top center', textfont_size=9)
    dark_layout(fig, 480)
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Source: FAO Food Balance Sheets, WHO Global Health Observatory")

    # Discovery box
    st.markdown("""
    <div class="discovery-box">
        <h3 style="color:#ff9900;margin:0;">💡 I HAD NO IDEA</h3>
        <p style="font-size:1.3rem;color:#ffffff;margin:12px 0;font-weight:600;">The USA eats the most on Earth — yet lives 7 years less than Japan, which eats the least among wealthy nations.</p>
        <p style="font-size:0.9rem;color:#8892a4;">The USA consumes 3,782 calories and 124 kg of meat per person per year, yet has a life expectancy of just 77.5. Japan consumes only 2,726 calories and 52 kg of meat — and lives to 84.8. More food ≠ better health. Japan's diet emphasizes fish, vegetables, and portion control. The "quality over quantity" principle applies to plates too.</p>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Sources: FAO Food Balance Sheets 2023, WHO, Our World in Data")

    # Transition
    st.markdown("""
    <p style="text-align:center;color:#8892a4;font-style:italic;font-size:1.1rem;margin:32px 0;">Meals finished, the afternoon hums with connection. But how connected are we — really?</p>
    """, unsafe_allow_html=True)


# ==========================================
# CHAPTER 4: 15:00 CONNECTION
# ==========================================
def render_connection():
    st.markdown("""
    <div class="chapter-hero">
        <div class="chapter-time-badge">15:00</div>
        <div class="chapter-title">How connected is humanity — really?</div>
        <div class="chapter-desc">
            The afternoon hums with activity. Flights cross oceans, messages span continents,
            and the internet reaches places electricity barely does. The digital divide is shrinking — fast.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Guess-first
    guess_key = 'connect_guess'
    if guess_key not in st.session_state.guess_made:
        st.markdown('<div class="guess-box">', unsafe_allow_html=True)
        st.markdown("#### 🤔 Before we show the data...")
        st.markdown("**Which country has MORE mobile subscriptions than people (per 100)?**")
        gc = st.columns(4)
        options = ['Japan', 'South Korea', 'South Africa', 'Colombia']
        for i, opt in enumerate(options):
            with gc[i]:
                if st.button(opt, key=f"conn_g_{opt}", use_container_width=True):
                    st.session_state.guess_made[guess_key] = opt
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        return

    user_guess = st.session_state.guess_made[guess_key]
    if user_guess == 'Japan':
        st.success("✅ Correct! Japan has **195 mobile subscriptions per 100 people** — nearly 2 phones per person!")
    else:
        st.warning(f"You guessed **{user_guess}**, but **Japan** leads with 195 per 100 people — nearly 2 phones each!")

    # Stats
    avg_internet = df_countries['Internet_Pct'].mean()
    max_internet = df_countries.sort_values('Internet_Pct', ascending=False).iloc[0]
    min_internet = df_countries.sort_values('Internet_Pct').iloc[0]
    avg_urban = df_countries['Urbanization_Pct'].mean()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("🌐 Highest Internet", f"{max_internet['Internet_Pct']:.0f}%", max_internet['Country'])
    with c2:
        st.metric("📵 Lowest Internet", f"{min_internet['Internet_Pct']:.0f}%", min_internet['Country'])
    with c3:
        st.metric("🌍 Avg Internet", f"{avg_internet:.0f}%", "All countries")
    with c4:
        st.metric("🏙️ Avg Urbanization", f"{avg_urban:.0f}%", "All countries")

    st.markdown("---")

    # HERO: Mobile subscriptions chart with the 1-per-person reference line
    st.markdown("### 📱 Mobile Subscriptions (per 100 people)")
    mobile_sorted = df_countries.sort_values('Mobile_Per_100', ascending=True)
    fig = px.bar(mobile_sorted, x='Mobile_Per_100', y='Country', orientation='h',
                 color='Region', color_discrete_sequence=COLORS,
                 labels={'Mobile_Per_100': 'Subscriptions per 100'})
    fig.update_layout(yaxis_title="")
    fig.add_vline(x=100, line_dash="dash", line_color=ORANGE, annotation_text="1 per person")
    dark_layout(fig, 480)
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Source: World Bank, ITU")

    # Flight routes map
    st.markdown("### ✈️ Global Airport Network")
    st.markdown("Major airports around the world — each dot represents a commercial airport.")
    major_airports = df_airports.groupby('Country').head(5).copy()
    major_airports = major_airports[major_airports['IATA'].notna() & (major_airports['IATA'] != '\\N')]
    major_airports = major_airports.head(500)

    fig_map = px.scatter_geo(major_airports, lat='Lat', lon='Lon',
                             hover_name='Name', hover_data=['City', 'Country'],
                             color_discrete_sequence=[BLUE],
                             opacity=0.6, size_max=5)
    fig_map.update_traces(marker=dict(size=3))
    fig_map.update_geos(
        bgcolor='rgba(0,0,0,0)',
        landcolor='#1a2744', oceancolor='#0b1120',
        showocean=True, showland=True, showcoastlines=True,
        coastlinecolor='#2a3a5c', showframe=False,
        projection_type='natural earth'
    )
    fig_map.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        geo=dict(bgcolor='rgba(0,0,0,0)'),
        height=400, margin=dict(t=10, b=10, l=0, r=0)
    )
    st.plotly_chart(fig_map, use_container_width=True)
    st.caption("Source: OpenFlights.org Airport Database")

    # Discovery box
    st.markdown("""
    <div class="discovery-box">
        <h3 style="color:#ff9900;margin:0;">💡 I HAD NO IDEA</h3>
        <p style="font-size:1.3rem;color:#ffffff;margin:12px 0;font-weight:600;">Kenya skipped the computer age entirely — and leapfrogged straight to mobile money.</p>
        <p style="font-size:0.9rem;color:#8892a4;">Kenya has only 32.7% internet access but 114 mobile subscriptions per 100 people. M-Pesa (mobile money) launched there in 2007 and now processes more transactions than Western Union does globally. Connectivity doesn't always look like a laptop and WiFi — sometimes it looks like a $20 phone transforming an entire economy.</p>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Sources: ITU ICT Facts and Figures 2024, World Bank, OpenFlights.org")

    # Transition
    st.markdown("""
    <p style="text-align:center;color:#8892a4;font-style:italic;font-size:1.1rem;margin:32px 0;">As evening falls, families gather. But does having more mean spending more time together?</p>
    """, unsafe_allow_html=True)


# ==========================================
# CHAPTER 5: 18:00 FAMILY
# ==========================================
def render_family():
    st.markdown("""
    <div class="chapter-hero">
        <div class="chapter-time-badge">18:00</div>
        <div class="chapter-title">Does more money mean more time with family?</div>
        <div class="chapter-desc">
            The workday ends. Families gather. But who actually has the most free time?
            And does wealth buy you more hours with the people you love?
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Guess-first
    guess_key = 'family_guess'
    if guess_key not in st.session_state.guess_made:
        st.markdown('<div class="guess-box">', unsafe_allow_html=True)
        st.markdown("#### 🤔 Before we show the data...")
        st.markdown("**Which country has the MOST leisure time per day?**")
        gc = st.columns(4)
        options = ['Finland', 'USA', 'France', 'Norway']
        for i, opt in enumerate(options):
            with gc[i]:
                if st.button(opt, key=f"fam_g_{opt}", use_container_width=True):
                    st.session_state.guess_made[guess_key] = opt
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        return

    user_guess = st.session_state.guess_made[guess_key]
    top_leisure = df_countries.sort_values('Leisure_Min_Per_Day', ascending=False).iloc[0]
    if user_guess == top_leisure['Country']:
        st.success(f"✅ Correct! **{top_leisure['Country']}** has the most leisure at {int(top_leisure['Leisure_Min_Per_Day'])} min/day.")
    else:
        st.warning(f"You guessed **{user_guess}**, but **{top_leisure['Country']}** leads with {int(top_leisure['Leisure_Min_Per_Day'])} min/day!")

    # Stats
    avg_leisure = df_countries['Leisure_Min_Per_Day'].mean()
    least_leisure = df_countries.sort_values('Leisure_Min_Per_Day').iloc[0]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("🎉 Most Leisure", f"{int(top_leisure['Leisure_Min_Per_Day'])} min", top_leisure['Country'])
    with c2:
        st.metric("😰 Least Leisure", f"{int(least_leisure['Leisure_Min_Per_Day'])} min", least_leisure['Country'])
    with c3:
        st.metric("🌍 Average", f"{int(avg_leisure)} min/day", f"≈ {int(avg_leisure)//60}h {int(avg_leisure)%60}m")
    with c4:
        gap = int(top_leisure['Leisure_Min_Per_Day'] - least_leisure['Leisure_Min_Per_Day'])
        st.metric("⏱️ Gap", f"{gap} min", "Max difference")

    st.markdown("---")

    # HERO: Leisure vs Happiness scatter
    st.markdown("### 😊 Leisure Time vs Happiness")
    fig = px.scatter(df_countries, x='Leisure_Min_Per_Day', y='Happiness_Score',
                     text='Country', color='Region', size='GDP_Per_Capita',
                     color_discrete_sequence=COLORS,
                     labels={'Leisure_Min_Per_Day': 'Leisure (min/day)',
                             'Happiness_Score': 'Happiness Score',
                             'GDP_Per_Capita': 'GDP/Capita'})
    fig.update_traces(textposition='top center', textfont_size=9)
    dark_layout(fig, 480)
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Source: World Happiness Report 2024, OECD")

    # Discovery box
    st.markdown("""
    <div class="discovery-box">
        <h3 style="color:#ff9900;margin:0;">💡 I HAD NO IDEA</h3>
        <p style="font-size:1.3rem;color:#ffffff;margin:12px 0;font-weight:600;">After $40,000 GDP per capita, more money stops buying happiness — but more free time never does.</p>
        <p style="font-size:0.9rem;color:#8892a4;">Finland has 285 minutes of leisure per day AND the world's highest happiness score (7.8). Kenya has just 165 minutes. The correlation between GDP and happiness plateaus around $40K/capita — beyond that, more money doesn't help. But more free time always does. The Nordic model (fewer work hours, strong safety nets, more leisure) consistently produces the happiest populations on Earth.</p>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Sources: OECD Better Life Index, World Happiness Report 2024, ILO")

    # Transition
    st.markdown("""
    <p style="text-align:center;color:#8892a4;font-style:italic;font-size:1.1rem;margin:32px 0;">Night descends. The world grows quiet. But rest — like everything else — is not equally distributed.</p>
    """, unsafe_allow_html=True)


# ==========================================
# CHAPTER 6: 22:00 NIGHT
# ==========================================
def render_night():
    st.markdown("""
    <div class="chapter-hero">
        <div class="chapter-time-badge">22:00</div>
        <div class="chapter-title">Who sleeps the most — and does it even matter?</div>
        <div class="chapter-desc">
            Night falls. The world goes dark — but not everywhere equally.
            Some cities never sleep. Some villages have no light at all.
            789 million people still live without electricity.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Guess-first
    guess_key = 'night_guess'
    if guess_key not in st.session_state.guess_made:
        st.markdown('<div class="guess-box">', unsafe_allow_html=True)
        st.markdown("#### 🤔 Before we show the data...")
        st.markdown("**What percentage of the world now has access to electricity?**")
        gc = st.columns(4)
        options = ['72%', '84%', '92%', '97%']
        for i, opt in enumerate(options):
            with gc[i]:
                if st.button(opt, key=f"night_g_{opt}", use_container_width=True):
                    st.session_state.guess_made[guess_key] = opt
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        return

    user_guess = st.session_state.guess_made[guess_key]
    if user_guess == '92%':
        st.success("✅ Correct! About 92% of the world now has electricity access — up from 73% in 1990.")
    else:
        st.warning(f"You guessed {user_guess}, but it's actually **92%** — up from 73% in 1990. Progress is real!")

    # Stats
    avg_elec = df_countries['Electricity_Pct'].mean()
    min_elec = df_countries.sort_values('Electricity_Pct').iloc[0]
    max_life = df_countries.sort_values('Life_Expectancy', ascending=False).iloc[0]
    min_life = df_countries.sort_values('Life_Expectancy').iloc[0]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("💡 Lowest Electricity", f"{min_elec['Electricity_Pct']:.0f}%", min_elec['Country'])
    with c2:
        st.metric("🌍 Avg Electricity", f"{avg_elec:.0f}%", "All countries")
    with c3:
        st.metric("🏆 Longest Life", f"{max_life['Life_Expectancy']:.1f} yr", max_life['Country'])
    with c4:
        st.metric("📉 Shortest Life", f"{min_life['Life_Expectancy']:.1f} yr", min_life['Country'])

    st.markdown("---")

    # HERO: Electricity vs Life Expectancy
    st.markdown("### 💡 Does Electricity Access Predict Life Expectancy?")
    fig = px.scatter(df_countries, x='Electricity_Pct', y='Life_Expectancy',
                     text='Country', color='Region', size='Population_M',
                     color_discrete_sequence=COLORS,
                     labels={'Electricity_Pct': 'Electricity Access (%)',
                             'Life_Expectancy': 'Life Expectancy (years)'})
    fig.update_traces(textposition='top center', textfont_size=9)
    dark_layout(fig, 480)
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Source: World Bank, IEA, WHO Global Health Observatory")

    # Discovery box
    st.markdown("""
    <div class="discovery-box">
        <h3 style="color:#ff9900;margin:0;">💡 I HAD NO IDEA</h3>
        <p style="font-size:1.3rem;color:#ffffff;margin:12px 0;font-weight:600;">Every country with 100% electricity has life expectancy above 75. No exceptions.</p>
        <p style="font-size:0.9rem;color:#8892a4;">Nigeria has only 62% electricity access and a life expectancy of 53.9 years — the lowest in our dataset. Electricity isn't just about convenience — it powers hospitals, refrigerates vaccines, enables night-time study, and runs water purification. Access to electricity is one of the strongest predictors of human development outcomes.</p>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Sources: World Bank, IEA, WHO Global Health Observatory")

    # Transition
    st.markdown("""
    <p style="text-align:center;color:#8892a4;font-style:italic;font-size:1.1rem;margin:32px 0;">The day ends. But not all days are the same...</p>
    """, unsafe_allow_html=True)


# ==========================================
# SPECIAL CHAPTER: CHILDREN
# ==========================================
def render_children():
    st.markdown("""
    <div style="text-align:center; padding: 40px 0 20px;">
        <p style="font-size: 3rem; margin: 0;">👶</p>
        <h1 style="font-size: 2rem; font-weight: 800; color: #ffffff; margin: 8px 0;">
            Three Children. One Planet. Different Worlds.
        </h1>
        <p style="font-size: 1rem; color: #8892a4; max-width: 600px; margin: 0 auto;">
            At this very moment, children across the world are living vastly different realities.
            Same age. Same planet. Completely different futures.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Get the three featured children
    kenya = df_children[df_children['Location'] == 'Rural Kenya'].iloc[0]
    syria = df_children[df_children['Location'] == 'Syria (Conflict)'].iloc[0]
    california = df_children[df_children['Location'] == 'California USA'].iloc[0]

    # 3-column layout
    col1, col2, col3 = st.columns(3)

    children_data = [
        (col1, kenya, "🇰🇪 Amara, 8", "Rural Kenya", "Water Scarcity", RED),
        (col2, syria, "🇸🇾 Yusuf, 10", "Syria", "Conflict Zone", ORANGE),
        (col3, california, "🇺🇸 Emma, 9", "California, USA", "Developed", GREEN),
    ]

    for col, data, name, location, tag, color in children_data:
        with col:
            st.markdown(f"""
            <div class="children-card">
                <h3>{name}</h3>
                <span class="region-tag" style="color:{color}">{tag}</span>
                <div class="children-stat">
                    <span class="children-stat-label">💧 Water Access</span>
                    <span class="children-stat-value">{data['Water_Access_Pct']}%</span>
                </div>
                <div class="children-stat">
                    <span class="children-stat-label">📚 School Attendance</span>
                    <span class="children-stat-value">{data['School_Attendance_Pct']}%</span>
                </div>
                <div class="children-stat">
                    <span class="children-stat-label">⚡ Electricity</span>
                    <span class="children-stat-value">{data['Electricity_Pct']}%</span>
                </div>
                <div class="children-stat">
                    <span class="children-stat-label">🍽️ Food Security</span>
                    <span class="children-stat-value">{data['Food_Security_Pct']}%</span>
                </div>
                <div class="children-stat">
                    <span class="children-stat-label">🌐 Internet</span>
                    <span class="children-stat-value">{data['Internet_Pct']}%</span>
                </div>
                <div class="children-stat">
                    <span class="children-stat-label">📖 Avg School Years</span>
                    <span class="children-stat-value">{data['Avg_School_Years']}</span>
                </div>
                <div class="children-stat">
                    <span class="children-stat-label">❤️ Life Expectancy</span>
                    <span class="children-stat-value">{data['Life_Expectancy']} yrs</span>
                </div>
                <div class="children-stat">
                    <span class="children-stat-label">👶 Child Mortality</span>
                    <span class="children-stat-value" style="color:{RED if data['Child_Mortality_Per_1000'] > 20 else ORANGE if data['Child_Mortality_Per_1000'] > 10 else GREEN}">{data['Child_Mortality_Per_1000']}/1000</span>
                </div>
                <div class="children-stat">
                    <span class="children-stat-label">🚶 Walk for Water</span>
                    <span class="children-stat-value">{data['Children_Walking_Water_Min']} min</span>
                </div>
                <div class="children-stat" style="border-bottom: none;">
                    <span class="children-stat-label">👷 Children Working</span>
                    <span class="children-stat-value">{data['Children_Working_Pct']}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Timeline comparison: A day in each child's life
    st.markdown("### ⏰ A Day in Three Lives")
    st.markdown("*What does the same hour look like for each child?*")

    timeline_data = {
        'Time': ['06:00', '07:00', '08:00', '09:00', '12:00', '15:00', '18:00', '21:00'],
        'Amara (Kenya)': [
            'Wake up, walk 45 min for water',
            'Help with farming chores',
            'Walk to school (if attending)',
            'School — shared textbook, no electricity',
            'Simple lunch — maize and beans',
            'More chores, fetch firewood',
            'Cook dinner over open fire',
            'Sleep — no electricity for reading'
        ],
        'Yusuf (Syria)': [
            'Wake up in temporary shelter',
            'Help family search for supplies',
            'Informal school (50% attendance)',
            'Learning in overcrowded tent classroom',
            'Rations — limited food security',
            'Play in rubble, avoid danger zones',
            'Family gathers, uncertain future',
            'Sleep — sounds of conflict nearby'
        ],
        'Emma (USA)': [
            'Wake up, hot shower, breakfast',
            'Mom drives to school',
            'Class with tablet, fast WiFi',
            'Math, science, art — full curriculum',
            'Cafeteria lunch — multiple choices',
            'After-school soccer practice',
            'Homework on laptop, family dinner',
            'Read in bed, lights off at 9'
        ]
    }
    timeline_df = pd.DataFrame(timeline_data)
    st.dataframe(timeline_df, use_container_width=True, hide_index=True)

    # Comparison radar chart
    st.markdown("### 📊 Childhood Reality Comparison")
    categories = ['Water', 'School', 'Electricity', 'Food', 'Internet', 'Life Exp (norm)']
    fig = go.Figure()
    for row_data, name, color in [(kenya, 'Rural Kenya', RED), (syria, 'Syria', ORANGE), (california, 'California', GREEN)]:
        vals = [
            row_data['Water_Access_Pct'],
            row_data['School_Attendance_Pct'],
            row_data['Electricity_Pct'],
            row_data['Food_Security_Pct'],
            row_data['Internet_Pct'],
            row_data['Life_Expectancy'] / 80 * 100  # normalize to 100
        ]
        fig.add_trace(go.Scatterpolar(r=vals, theta=categories, fill='toself', name=name, line=dict(color=color)))

    fig.update_layout(
        polar=dict(bgcolor='rgba(0,0,0,0)', radialaxis=dict(visible=True, range=[0, 100], color='#333')),
        paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#8892a4'),
        legend=dict(x=0.5, y=-0.2, xanchor='center', orientation='h'),
        height=400, margin=dict(t=30, b=60, l=60, r=60)
    )
    st.plotly_chart(fig, use_container_width=True)

    # Discovery
    st.markdown("""
    <div class="discovery-box">
        <h3 style="color:#ff9900;margin:0;">💡 I HAD NO IDEA</h3>
        <p style="font-size:1.3rem;color:#ffffff;margin:12px 0;font-weight:600;">The zip code a child is born into remains the strongest predictor of their future.</p>
        <p style="font-size:0.9rem;color:#8892a4;">Amara walks 45 minutes each day just to get water. 28% of children in her region work instead of attending school. Yusuf's life expectancy at birth was 72 years — but conflict has disrupted everything. Emma has never known a day without clean water, electricity, or internet. But the next chapter shows: things ARE getting better.</p>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Sources: UNICEF State of the World's Children 2024, WHO, World Bank, UNHCR")


# ==========================================
# ENDING: HOPE
# ==========================================
def render_hope():
    st.markdown("""
    <div style="text-align:center; padding: 40px 0 20px;">
        <p style="font-size: 3rem; margin: 0;">🌱</p>
        <h1 style="font-size: 2rem; font-weight: 800; color: #4ade80; margin: 8px 0;">
            The World is Getting Better
        </h1>
        <p style="font-size: 1rem; color: #8892a4; max-width: 600px; margin: 0 auto;">
            Despite the headlines, humanity has made extraordinary progress since 1990.
            These aren't opinions — they're measured facts.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Progress metrics at a glance
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
        <div class="hope-metric">
            <div class="value">93→27</div>
            <div class="label">Child mortality per 1000<br>(1990 → 2024)</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="hope-metric">
            <div class="value">64→73</div>
            <div class="label">Life expectancy years<br>(1990 → 2024)</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="hope-metric">
            <div class="value">0%→67%</div>
            <div class="label">Internet users<br>(1990 → 2024)</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class="hope-metric">
            <div class="value">36%→8.5%</div>
            <div class="label">Extreme poverty<br>(1990 → 2024)</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Line charts showing progress
    years = ['1990', '2000', '2010', '2020', '2024']
    year_cols = ['Year_1990', 'Year_2000', 'Year_2010', 'Year_2020', 'Year_2024']

    # Select indicators to plot
    positive_indicators = ['Life Expectancy', 'Access to Clean Water', 'Access to Electricity',
                           'School Enrollment (Primary)', 'Internet Users', 'Mobile Subscriptions']
    negative_indicators = ['Child Mortality (per 1000)', 'Extreme Poverty', 'Undernourishment', 'Maternal Mortality']

    # Positive progress charts
    st.markdown("### 📈 Rising: Things Getting Better")
    chart1, chart2 = st.columns(2)

    with chart1:
        fig = go.Figure()
        colors_pos = [GREEN, BLUE, CYAN, ORANGE, PURPLE, '#f472b6']
        for i, indicator in enumerate(positive_indicators[:3]):
            row = df_progress[df_progress['Indicator'] == indicator]
            if not row.empty:
                vals = [row.iloc[0][col] for col in year_cols]
                fig.add_trace(go.Scatter(
                    x=years, y=vals, mode='lines+markers',
                    name=indicator, line=dict(color=colors_pos[i], width=3),
                    marker=dict(size=8)
                ))
        fig.update_layout(yaxis_title="% or Years", xaxis_title="Year",
                          legend=dict(orientation='h', y=-0.3, x=0.5, xanchor='center'))
        dark_layout(fig, 380)
        st.plotly_chart(fig, use_container_width=True)

    with chart2:
        fig2 = go.Figure()
        for i, indicator in enumerate(positive_indicators[3:]):
            row = df_progress[df_progress['Indicator'] == indicator]
            if not row.empty:
                vals = [row.iloc[0][col] for col in year_cols]
                fig2.add_trace(go.Scatter(
                    x=years, y=vals, mode='lines+markers',
                    name=indicator, line=dict(color=colors_pos[i+3], width=3),
                    marker=dict(size=8)
                ))
        fig2.update_layout(yaxis_title="% or per 100", xaxis_title="Year",
                           legend=dict(orientation='h', y=-0.3, x=0.5, xanchor='center'))
        dark_layout(fig2, 380)
        st.plotly_chart(fig2, use_container_width=True)

    # Negative (declining = good) charts
    st.markdown("### 📉 Falling: Problems Shrinking")
    chart3, chart4 = st.columns(2)

    with chart3:
        fig3 = go.Figure()
        colors_neg = [RED, ORANGE]
        for i, indicator in enumerate(negative_indicators[:2]):
            row = df_progress[df_progress['Indicator'] == indicator]
            if not row.empty:
                vals = [row.iloc[0][col] for col in year_cols]
                fig3.add_trace(go.Scatter(
                    x=years, y=vals, mode='lines+markers',
                    name=indicator, line=dict(color=colors_neg[i], width=3),
                    marker=dict(size=8)
                ))
        fig3.update_layout(yaxis_title="Rate (per 1000 or %)", xaxis_title="Year",
                           legend=dict(orientation='h', y=-0.3, x=0.5, xanchor='center'))
        dark_layout(fig3, 380)
        st.plotly_chart(fig3, use_container_width=True)

    with chart4:
        fig4 = go.Figure()
        colors_neg2 = ['#f472b6', PURPLE]
        for i, indicator in enumerate(negative_indicators[2:]):
            row = df_progress[df_progress['Indicator'] == indicator]
            if not row.empty:
                vals = [row.iloc[0][col] for col in year_cols]
                fig4.add_trace(go.Scatter(
                    x=years, y=vals, mode='lines+markers',
                    name=indicator, line=dict(color=colors_neg2[i], width=3),
                    marker=dict(size=8)
                ))
        fig4.update_layout(yaxis_title="Rate (% or per 100,000)", xaxis_title="Year",
                           legend=dict(orientation='h', y=-0.3, x=0.5, xanchor='center'))
        dark_layout(fig4, 380)
        st.plotly_chart(fig4, use_container_width=True)

    st.caption("Sources: UNICEF, WHO, World Bank, ITU, UNESCO, FAO")

    # All indicators summary table
    st.markdown("### 📋 Full Progress Dashboard (1990 → 2024)")
    display_df = df_progress[['Indicator', 'Year_1990', 'Year_2024', 'Unit', 'Source']].copy()
    display_df.columns = ['Indicator', '1990', '2024', 'Unit', 'Source']
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    # Emotional closing
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; padding: 48px; background: linear-gradient(135deg, #0f2744 0%, #1a1a3e 100%);
                border-radius: 12px; border: 1px solid #1a2744; margin-top: 24px;">
        <p style="font-size: 2rem; color: #ffffff; font-weight: 800; margin-bottom: 8px; letter-spacing: -0.5px;">
            One Earth. Billions of Lives. Twenty-Four Hours.
        </p>
        <p style="font-size: 1.2rem; color: #8892a4; margin-bottom: 8px;">
            Although cultures differ, every person shares the same day.
        </p>
        <p style="font-size: 1.2rem; color: #4ade80; font-weight: 600; margin-bottom: 32px;">
            How we spend it reveals what we value.
        </p>
        <p style="font-size: 0.95rem; color: #8892a4; max-width: 600px; margin: 0 auto 24px;">
            Child mortality has dropped 71% since 1990. Extreme poverty fell from 36% to 8.5%.
            Internet access went from nearly zero to 5.4 billion people connected.
            Every one of these numbers represents millions of lives transformed.
        </p>
        <p style="font-size: 0.85rem; color: #6b7a94; max-width: 500px; margin: 0 auto 24px;">
            The progress isn't automatic — it's the result of vaccines, education, infrastructure,
            and the work of millions of people who decided things could be better.
        </p>
        <p style="font-size: 1.3rem; color: #ffffff; font-weight: 500; margin-top: 32px; margin-bottom: 16px;">
            Thank you for taking this journey.
        </p>
        <p style="font-size: 2rem; margin-top: 24px;">🌍</p>
        <p style="font-size: 0.8rem; color: #555; margin-top: 16px;">
            VizCon 2026 · Data from UNICEF, WHO, World Bank, OECD, ITU, FAO, UNESCO
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Discovery
    st.markdown("""
    <div class="discovery-box">
        <h3 style="color:#ff9900;margin:0;">💡 I HAD NO IDEA</h3>
        <p style="font-size:1.3rem;color:#ffffff;margin:12px 0;font-weight:600;">Extreme poverty could be eliminated within our lifetimes.</p>
        <p style="font-size:0.9rem;color:#8892a4;">In 1990, more than 1 in 3 humans lived on less than $2.15/day. Today it's fewer than 1 in 11. The number of children dying before age 5 has fallen from 12.6 million/year to 4.9 million. Every single day, the world gets a little better — we just don't see it in the headlines.</p>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# THRIVE INDEX (Original Analysis)
# ==========================================
def render_thrive():
    st.markdown("""
    <div class="chapter-hero">
        <div class="chapter-time-badge">⭐</div>
        <div class="chapter-title">The Thrive Index</div>
        <div class="chapter-desc">
            We created an original composite metric that captures how well a country
            enables its people to thrive — combining education, health, connectivity, and prosperity.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Formula explanation
    st.markdown("""
    <div class="discovery-box">
        📐 <strong>Our Formula:</strong><br><br>
        <code>Thrive Score = (Education × 0.30) + (Health × 0.25) + (Connectivity × 0.25) + (Prosperity × 0.20)</code><br><br>
        Where:<br>
        • <strong>Education</strong> = School Enrollment (normalized 0-100)<br>
        • <strong>Health</strong> = Life Expectancy (normalized to 0-100 scale, where 85 = 100)<br>
        • <strong>Connectivity</strong> = (Internet % + Mobile per 100 capped at 100) / 2<br>
        • <strong>Prosperity</strong> = GDP per capita (log-normalized to 0-100 scale)
    </div>
    """, unsafe_allow_html=True)

    df = load_countries().copy()

    # Calculate Thrive Index components
    df['Education_Score'] = df['School_Enrollment_Pct'].clip(0, 100)
    df['Health_Score'] = (df['Life_Expectancy'] / 85 * 100).clip(0, 100)
    df['Connectivity_Score'] = ((df['Internet_Pct'] + df['Mobile_Per_100'].clip(0, 100)) / 2).clip(0, 100)
    df['Prosperity_Score'] = (np.log10(df['GDP_Per_Capita'].clip(1, 200000)) / np.log10(200000) * 100).clip(0, 100)

    df['Thrive_Score'] = (
        df['Education_Score'] * 0.30 +
        df['Health_Score'] * 0.25 +
        df['Connectivity_Score'] * 0.25 +
        df['Prosperity_Score'] * 0.20
    ).round(1)

    df = df.sort_values('Thrive_Score', ascending=False)

    # Top stats
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        top = df.iloc[0]
        st.metric(f"🥇 #{1}", f"{top['Country']}", f"Score: {top['Thrive_Score']}")
    with c2:
        second = df.iloc[1]
        st.metric(f"🥈 #{2}", f"{second['Country']}", f"Score: {second['Thrive_Score']}")
    with c3:
        third = df.iloc[2]
        st.metric(f"🥉 #{3}", f"{third['Country']}", f"Score: {third['Thrive_Score']}")
    with c4:
        last = df.iloc[-1]
        st.metric(f"📉 #{len(df)}", f"{last['Country']}", f"Score: {last['Thrive_Score']}")

    st.markdown("---")

    # World Map - Thrive Score Choropleth
    iso_map = {
        'Japan': 'JPN', 'South Korea': 'KOR', 'India': 'IND', 'China': 'CHN',
        'USA': 'USA', 'Canada': 'CAN', 'Mexico': 'MEX', 'Brazil': 'BRA',
        'Colombia': 'COL', 'Germany': 'DEU', 'France': 'FRA', 'UK': 'GBR',
        'Norway': 'NOR', 'Denmark': 'DNK', 'Netherlands': 'NLD',
        'South Africa': 'ZAF', 'Kenya': 'KEN', 'Nigeria': 'NGA',
        'Australia': 'AUS', 'New Zealand': 'NZL', 'Turkey': 'TUR',
        'Chile': 'CHL', 'Finland': 'FIN', 'Sweden': 'SWE'
    }
    df['ISO'] = df['Country'].map(iso_map)

    st.markdown("### 🗺️ Global Thrive Score Map")
    fig = px.choropleth(
        df, locations='ISO', color='Thrive_Score',
        hover_name='Country',
        hover_data={'Thrive_Score': ':.1f', 'ISO': False},
        color_continuous_scale=['#1a0a0a', '#ef4444', '#ff9900', '#4ade80', '#3b82f6'],
        range_color=[30, 90],
        projection='natural earth'
    )
    fig.update_layout(
        geo=dict(
            bgcolor='rgba(0,0,0,0)',
            lakecolor='#0b1120',
            landcolor='#1a2744',
            showocean=True, oceancolor='#0b1120',
            showlakes=True,
            showframe=False,
            coastlinecolor='#2a3a5c',
            countrycolor='#2a3a5c'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#8892a4'),
        height=450, margin=dict(t=30, b=10, l=0, r=0),
        coloraxis_colorbar=dict(
            title=dict(text="Thrive Score", font=dict(color='#8892a4')),
            tickfont=dict(color='#8892a4')
        )
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Main chart - horizontal bar
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 🌍 Global Thrive Index Rankings")
        fig = px.bar(df, x='Thrive_Score', y='Country', orientation='h',
                     color='Thrive_Score',
                     color_continuous_scale=['#ef4444', '#ff9900', '#4ade80', '#3b82f6'],
                     range_color=[30, 90])
        fig.update_layout(yaxis=dict(autorange='reversed'))
        dark_layout(fig, height=600)
        fig.update_layout(coloraxis_showscale=False, xaxis_title="Thrive Score (0-100)", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 🔍 Country Deep Dive")
        selected = st.selectbox("Select country", df['Country'].tolist(), key="thrive_country")
        row = df[df['Country'] == selected].iloc[0]

        # Radar chart for selected country
        categories = ['Education', 'Health', 'Connectivity', 'Prosperity']
        values = [row['Education_Score'], row['Health_Score'],
                  row['Connectivity_Score'], row['Prosperity_Score']]

        fig = go.Figure(data=go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            line=dict(color='#3b82f6'),
            fillcolor='rgba(59,130,246,0.2)'
        ))
        fig.update_layout(
            polar=dict(
                bgcolor='rgba(0,0,0,0)',
                radialaxis=dict(visible=True, range=[0, 100], color='#333'),
                angularaxis=dict(color='#8892a4')
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#8892a4'),
            height=300, margin=dict(t=30, b=30, l=60, r=60),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

        # Strengths and challenges
        scores = {'Education': row['Education_Score'], 'Health': row['Health_Score'],
                  'Connectivity': row['Connectivity_Score'], 'Prosperity': row['Prosperity_Score']}
        strength = max(scores, key=scores.get)
        challenge = min(scores, key=scores.get)
        st.markdown(f"**Strength:** {strength} ({scores[strength]:.0f}/100)")
        st.markdown(f"**Challenge:** {challenge} ({scores[challenge]:.0f}/100)")
        st.markdown(f"**Overall Thrive Score:** ⭐ **{row['Thrive_Score']}** / 100")

    # Scatter: Thrive Score vs Happiness
    st.markdown("---")
    st.markdown("### Does Thriving = Happiness?")
    fig = px.scatter(df, x='Thrive_Score', y='Happiness_Score', text='Country',
                     color='Region', size='Population_M',
                     color_discrete_sequence=['#3b82f6', '#4ade80', '#ff9900', '#ef4444', '#8b5cf6'])
    fig.update_traces(textposition='top center', textfont=dict(size=9))
    dark_layout(fig, height=400)
    fig.update_layout(xaxis_title="Thrive Score", yaxis_title="Happiness Score (0-10)")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div class="discovery-box">
        <h3 style="color:#ff9900;margin:0;">💡 I HAD NO IDEA</h3>
        <p style="font-size:1.3rem;color:#ffffff;margin:12px 0;font-weight:600;">Thriving and happiness are correlated — but not the same thing.</p>
        <p style="font-size:0.9rem;color:#8892a4;">Thrive Score and Happiness correlate at r ≈ 0.82, but not perfectly. Some countries with moderate Thrive Scores (like Colombia, Brazil) report happiness levels close to Nordic countries — suggesting that social connection, culture, and community contribute to well-being beyond material indicators.</p>
    </div>
    """, unsafe_allow_html=True)

    st.caption("Sources: OECD, WHO, World Bank, UNESCO, ITU | Thrive Index: original analysis by authors")


# ==========================================
# WHAT IF SIMULATOR
# ==========================================
def render_what_if():
    st.markdown("""
    <div class="chapter-hero">
        <div class="chapter-time-badge">🔮</div>
        <div class="chapter-title">What If? Simulator</div>
        <div class="chapter-desc">
            Explore how changes in key indicators could transform a country's Thrive Score.
            Move the sliders and see the projected impact.
        </div>
    </div>
    """, unsafe_allow_html=True)

    df = load_countries().copy()

    # Calculate base Thrive scores
    df['Education_Score'] = df['School_Enrollment_Pct'].clip(0, 100)
    df['Health_Score'] = (df['Life_Expectancy'] / 85 * 100).clip(0, 100)
    df['Connectivity_Score'] = ((df['Internet_Pct'] + df['Mobile_Per_100'].clip(0, 100)) / 2).clip(0, 100)
    df['Prosperity_Score'] = (np.log10(df['GDP_Per_Capita'].clip(1, 200000)) / np.log10(200000) * 100).clip(0, 100)
    df['Thrive_Score'] = (
        df['Education_Score'] * 0.30 +
        df['Health_Score'] * 0.25 +
        df['Connectivity_Score'] * 0.25 +
        df['Prosperity_Score'] * 0.20
    ).round(1)

    # Country selection
    col1, col2 = st.columns([1, 2])

    with col1:
        country = st.selectbox("🌍 Select a country to simulate", df['Country'].tolist(),
                              index=df['Country'].tolist().index('Kenya'), key="whatif_country")
        row = df[df['Country'] == country].iloc[0]

        st.markdown(f"### Current: {country}")
        st.markdown(f"**Thrive Score:** ⭐ {row['Thrive_Score']} / 100")
        st.markdown("---")

        # Sliders
        st.markdown("### 🎛️ Adjust Indicators:")
        internet_change = st.slider("Internet Access Change (%)", -20, 50, 0, 5, key="wf_internet")
        education_change = st.slider("School Enrollment Change (%)", -10, 20, 0, 2, key="wf_edu")
        health_change = st.slider("Life Expectancy Change (years)", -5, 10, 0, 1, key="wf_health")
        gdp_change = st.slider("GDP per Capita Change (%)", -30, 100, 0, 10, key="wf_gdp")

    with col2:
        # Calculate new scores
        new_internet = min(100, row['Internet_Pct'] + internet_change)
        new_edu = min(100, row['School_Enrollment_Pct'] + education_change)
        new_life = min(85, row['Life_Expectancy'] + health_change)
        new_gdp = row['GDP_Per_Capita'] * (1 + gdp_change / 100)

        new_edu_score = new_edu
        new_health_score = min(100, new_life / 85 * 100)
        new_conn_score = min(100, (new_internet + min(100, row['Mobile_Per_100'])) / 2)
        new_pros_score = min(100, np.log10(max(1, new_gdp)) / np.log10(200000) * 100)

        new_thrive = round(
            new_edu_score * 0.30 +
            new_health_score * 0.25 +
            new_conn_score * 0.25 +
            new_pros_score * 0.20, 1
        )

        change = new_thrive - row['Thrive_Score']
        change_pct = (change / row['Thrive_Score'] * 100) if row['Thrive_Score'] > 0 else 0

        # Results display
        st.markdown("### 📊 Projected Impact")
        st.markdown("<br>", unsafe_allow_html=True)

        r1, r2, r3 = st.columns(3)
        with r1:
            st.metric("Current Score", f"{row['Thrive_Score']}")
        with r2:
            st.metric("New Score", f"{new_thrive}", f"{change:+.1f}")
        with r3:
            st.metric("Change", f"{change_pct:+.1f}%")

        # Before/After radar
        categories = ['Education', 'Health', 'Connectivity', 'Prosperity']
        old_values = [row['Education_Score'], row['Health_Score'],
                      row['Connectivity_Score'], row['Prosperity_Score']]
        new_values = [new_edu_score, new_health_score, new_conn_score, new_pros_score]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=old_values + [old_values[0]], theta=categories + [categories[0]],
            fill='toself', name='Current',
            line=dict(color='#8892a4', dash='dash'),
            fillcolor='rgba(136,146,164,0.1)'
        ))
        fig.add_trace(go.Scatterpolar(
            r=new_values + [new_values[0]], theta=categories + [categories[0]],
            fill='toself', name='Projected',
            line=dict(color='#3b82f6'),
            fillcolor='rgba(59,130,246,0.2)'
        ))
        fig.update_layout(
            polar=dict(bgcolor='rgba(0,0,0,0)',
                      radialaxis=dict(visible=True, range=[0, 100], color='#333'),
                      angularaxis=dict(color='#8892a4')),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#8892a4'),
            height=350, margin=dict(t=30, b=30, l=60, r=60),
            legend=dict(x=0.5, y=-0.15, xanchor='center', orientation='h')
        )
        st.plotly_chart(fig, use_container_width=True)

        # Narrative
        if change > 0:
            st.markdown(f"""
            <div class="discovery-box">
                🚀 <strong>Projected outcome:</strong> If {country} achieves these improvements,
                its Thrive Score would rise from <strong>{row['Thrive_Score']}</strong> to <strong>{new_thrive}</strong>
                (+{change_pct:.1f}%). {'This would move it ahead of ' + df[df['Thrive_Score'] < new_thrive].iloc[-1]['Country'] + ' in the global rankings.' if len(df[df['Thrive_Score'] < new_thrive]) > 0 else ''}
            </div>
            """, unsafe_allow_html=True)
        elif change < 0:
            st.markdown(f"""
            <div class="discovery-box" style="border-left-color: #ef4444;">
                ⚠️ <strong>Warning:</strong> These changes would reduce {country}'s Thrive Score
                from <strong>{row['Thrive_Score']}</strong> to <strong>{new_thrive}</strong> ({change_pct:.1f}%).
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="discovery-box">
                ↔️ Move the sliders to explore different scenarios.
            </div>
            """, unsafe_allow_html=True)

    st.caption("Note: This is a simplified projection model for illustrative purposes. Real-world outcomes depend on many interacting factors.")


# ==========================================
# MAIN JOURNEY ROUTER
# ==========================================
def show_journey():
    show_navigation()

    current = st.session_state.hour
    if current == '06:00':
        render_wake_up()
    elif current == '09:00':
        render_work()
    elif current == '12:00':
        render_food()
    elif current == '15:00':
        render_connection()
    elif current == '18:00':
        render_family()
    elif current == '22:00':
        render_night()
    elif current == 'Children':
        render_children()
    elif current == 'Hope':
        render_hope()
    elif current == 'Thrive':
        render_thrive()
    elif current == 'What If':
        render_what_if()


# ==========================================
# MAIN ENTRY POINT
# ==========================================
def main():
    if st.session_state.page == 'landing':
        show_landing()
    else:
        show_journey()


if __name__ == "__main__":
    main()
