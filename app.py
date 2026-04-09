!pip install streamlit pandas
import streamlit as st
import pandas as pd

# --- Data ---
api_response = {
    "train_name": "Rajdhani Express",
    "train_number": "12301",
    "route": [
        {"station": "New Delhi",      "arrival": "Source",      "departure": "07:05"},
        {"station": "Kanpur Central", "arrival": "10:10",       "departure": "10:15"},
        {"station": "Allahabad Jn",   "arrival": "12:00",       "departure": "12:10"},
        {"station": "Patna Jn",       "arrival": "16:30",       "departure": "16:40"},
        {"station": "Howrah Jn",      "arrival": "21:30",       "departure": "Destination"},
    ],
}

# --- 1. Train Name & Number ---
st.markdown(f"# 🚆 {api_response['train_name']}")
st.markdown(f"**Train Number:** `{api_response['train_number']}`")

st.divider()

# --- 2. Full Route Table ---
st.markdown("### 📍 Full Route")

df = pd.DataFrame(api_response["route"])
df.index = df.index + 1          # start index from 1
df.columns = ["Station", "Arrival", "Departure"]

st.dataframe(
    df,
    use_container_width=True,
    hide_index=False,
)

st.divider()

# --- 3. Station Selector ---
st.markdown("### 🔍 Check Station Timings")

station_names = [stop["station"] for stop in api_response["route"]]

selected_station = st.selectbox("Select a station:", station_names)

# Look up the selected station's timings
selected_info = next(
    stop for stop in api_response["route"] if stop["station"] == selected_station
)

col1, col2 = st.columns(2)
with col1:
    st.text(f"🟢 Arrival :  {selected_info['arrival']}")
with col2:
    st.text(f"🔴 Departure: {selected_info['departure']}")
