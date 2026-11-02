import streamlit as st
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from leetcode_fetcher import fetch_leetcode_profile
from agent_tools import ask_performance_agent

st.set_page_config(page_title="Student LeetCode Monitor", layout="wide")
st.title("🎓 Multi-Class LeetCode Performance & AI Monitor")

# Sidebar for Class File Upload
st.sidebar.header("📁 Class Data Source")
uploaded_file = st.sidebar.file_uploader("Upload Class CSV (Name, Roll, Username)", type=["csv"])

# Function to fetch single student row safely
def get_student_row(row):
    username = str(row.get("leetcode_username", "")).strip()
    stats = fetch_leetcode_profile(username)
    if stats:
        return {
            "Name": row.get("name", "Unknown"),
            "Roll No": row.get("roll_no", "N/A"),
            "Username": username,
            "Total Solved": stats["all"],
            "Easy": stats["easy"],
            "Medium": stats["medium"],
            "Hard": stats["hard"],
            "Ranking": stats["ranking"]
        }
    return {
        "Name": row.get("name", "Unknown"),
        "Roll No": row.get("roll_no", "N/A"),
        "Username": username,
        "Total Solved": 0, "Easy": 0, "Medium": 0, "Hard": 0, "Ranking": "Not Found"
    }

# Parallel Data Fetcher for 200+ students
@st.cache_data(ttl=1800)
def load_bulk_data(csv_data):
    students_df = pd.read_csv(csv_data)
    
    # 10 parallel threads to make it super fast
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(get_student_row, [row for _, row in students_df.iterrows()]))
    
    return pd.DataFrame(results)

# Determine data source
target_file = uploaded_file if uploaded_file is not None else "students.csv"

with st.spinner("Fetching data from LeetCode..."):
    df = load_bulk_data(target_file)

# Overview KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Students", len(df))
col2.metric("Class Average Solved", f"{df['Total Solved'].mean():.1f}")
col3.metric("Top Solver Score", df['Total Solved'].max())
inactive_count = len(df[df['Total Solved'] == 0])
col4.metric("Inactive / Not Found", inactive_count)

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Class Leaderboard", "🤖 AI Performance Agent", "📥 Download Report"])

with tab1:
    st.subheader("Real-Time Ranking Table")
    # Filters
    search_name = st.text_input("🔍 Search Student by Name or Roll No:")
    filtered_df = df.copy()
    if search_name:
        filtered_df = filtered_df[
            filtered_df["Name"].str.contains(search_name, case=False, na=False) |
            filtered_df["Roll No"].astype(str).str.contains(search_name, case=False, na=False)
        ]
    sorted_df = filtered_df.sort_values(by="Total Solved", ascending=False).reset_index(drop=True)
    st.dataframe(sorted_df, use_container_width=True)

with tab2:
    st.subheader("Class Insights AI Agent")
    st.markdown("Mam can ask questions directly about the class:")
    user_query = st.text_input("Example: 'Un baccho ke roll number batao jinhone 10 se kam questions kiye hain'")
    
    if st.button("Ask Agent") and user_query:
        with st.spinner("Agent analyzing class data..."):
            ans = ask_performance_agent(user_query, df)
            st.markdown(ans)

with tab3:
    st.subheader("Export Semester Progress")
    csv_download = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Full Batch Excel/CSV Report",
        data=csv_download,
        file_name='class_performance_report.csv',
        mime='text/csv'
    )
    