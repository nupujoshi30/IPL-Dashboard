import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the Streamlit page configuration
st.set_page_config(page_title="IPL Dashboard", layout="wide")

# Page title
st.title("🏏 IPL Dashboard")
st.markdown("Explore IPL insights with interactive visuals.")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("C:\\Users\\Dell\\Downloads\\LINKEDLN\\IPL Analysis\\ipl dataset.csv")  # Make sure this path is correct relative to your app.py
    return df

df = load_data()

# Show raw data on checkbox
if st.checkbox("Show Raw Data"):
    st.dataframe(df.head(10))

# Sidebar filters
st.sidebar.header("Filter")
selected_team = st.sidebar.selectbox("Choose Team", sorted(df['team1'].dropna().unique()))
selected_season = st.sidebar.slider("Select Season", int(df['season'].min()), int(df['season'].max()), step=1)

# Filtered data
filtered_df = df[(df['team1'] == selected_team) & (df['season'] == selected_season)]

# Key Stats
st.subheader(f"Overview for {selected_team} in {selected_season}")
st.metric("Matches Played", len(filtered_df))
st.metric("Wins", len(filtered_df[filtered_df['winner'] == selected_team]))

# Plotting: Match Result Count
st.subheader("Match Result Breakdown")
fig, ax = plt.subplots()
sns.countplot(data=filtered_df, x='result', palette='Set2', ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# Add Toss vs Match Win (optional)
st.subheader("Toss vs Match Win Correlation (Overall)")
fig2, ax2 = plt.subplots()
toss_match_win = (df['toss_winner'] == df['winner']).value_counts()
toss_match_win.plot(kind='pie', labels=['Won Both Toss & Match', 'Did Not Win Both'],
                    autopct='%1.1f%%', startangle=90, colors=['#66c2a5', '#fc8d62'], ax=ax2)
ax2.set_ylabel("")
st.pyplot(fig2)

# ----------------------------------------
# TEAM COMPARISON SECTION
# ----------------------------------------

st.header("📊 Team vs Team Comparison")

teams = sorted(df['team1'].dropna().unique())
col1, col2 = st.columns(2)
team_a = col1.selectbox("Select Team A", teams, index=0, key="team_a")
team_b = col2.selectbox("Select Team B", teams, index=1, key="team_b")

if team_a == team_b:
    st.warning("Please select two different teams for comparison.")
else:
    col1, col2 = st.columns(2)

    # Filter data
    team_a_df = df[(df['team1'] == team_a) | (df['team2'] == team_a)]
    team_b_df = df[(df['team1'] == team_b) | (df['team2'] == team_b)]

    def compute_stats(team_df, team_name):
        played = len(team_df)
        won = team_df[team_df['winner'] == team_name].shape[0]
        toss_won = team_df[team_df['toss_winner'] == team_name].shape[0]
        toss_and_match_won = team_df[(team_df['toss_winner'] == team_name) & (team_df['winner'] == team_name)].shape[0]
        win_pct = round((won / played) * 100, 2) if played else 0
        toss_conversion = round((toss_and_match_won / toss_won) * 100, 2) if toss_won else 0
        return played, won, win_pct, toss_won, toss_conversion

    # Compute stats
    stats_a = compute_stats(team_a_df, team_a)
    stats_b = compute_stats(team_b_df, team_b)

    # Show stats
    with col1:
        st.subheader(team_a)
        st.metric("Matches Played", stats_a[0])
        st.metric("Matches Won", stats_a[1])
        st.metric("Win %", stats_a[2])
        st.metric("Toss Won", stats_a[3])
        st.metric("Toss-Win Conversion %", stats_a[4])

    with col2:
        st.subheader(team_b)
        st.metric("Matches Played", stats_b[0])
        st.metric("Matches Won", stats_b[1])
        st.metric("Win %", stats_b[2])
        st.metric("Toss Won", stats_b[3])
        st.metric("Toss-Win Conversion %", stats_b[4])

    # --------------------------
    # Head-to-Head Chart
    # --------------------------
    st.subheader(f"⚔️ Head-to-Head: {team_a} vs {team_b}")
    h2h_df = df[((df['team1'] == team_a) & (df['team2'] == team_b)) | ((df['team1'] == team_b) & (df['team2'] == team_a))]
    h2h_counts = h2h_df['winner'].value_counts()[[team_a, team_b]].fillna(0)

    fig, ax = plt.subplots()
    sns.barplot(x=h2h_counts.index, y=h2h_counts.values, palette='Set1')
    plt.title(f"Matches Won Between {team_a} and {team_b}")
    plt.xlabel("Team")
    plt.ylabel("Wins")
    st.pyplot(fig)
