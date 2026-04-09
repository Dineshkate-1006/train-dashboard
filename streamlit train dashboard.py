!pip install streamlit pandas
import streamlit as st
import pandas as pd

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Rajdhani Express · Route Dashboard",
    page_icon="🚄",
    layout="wide",
)

# ── Data ─────────────────────────────────────────────────────────────────────
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

# ── Derived helpers ───────────────────────────────────────────────────────────
def to_minutes(t: str) -> int | None:
    """Convert 'HH:MM' to total minutes from midnight. Returns None for non-time strings."""
    try:
        h, m = map(int, t.split(":"))
        return h * 60 + m
    except Exception:
        return None

route = api_response["route"]
n_stops = len(route)

# Build enriched rows
rows = []
for i, stop in enumerate(route):
    arr_min = to_minutes(stop["arrival"])
    dep_min = to_minutes(stop["departure"])

    # Halt duration
    if arr_min is not None and dep_min is not None:
        halt = dep_min - arr_min
        halt_str = f"{halt} min"
    else:
        halt_str = "—"

    # Travel time from previous station
    if i == 0:
        travel_str = "—"
    else:
        prev_dep_min = to_minutes(route[i - 1]["departure"])
        if prev_dep_min is not None and arr_min is not None:
            travel = arr_min - prev_dep_min
            h, m = divmod(travel, 60)
            travel_str = f"{h}h {m}m" if h else f"{m}m"
        else:
            travel_str = "—"

    rows.append(
        {
            "Stop": i + 1,
            "Station": stop["station"],
            "Arrival": stop["arrival"],
            "Departure": stop["departure"],
            "Halt": halt_str,
            "Travel from Prev": travel_str,
        }
    )

df = pd.DataFrame(rows)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] { font-family: 'Sora', sans-serif; }

    /* Header strip */
    .train-header {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        border-radius: 14px;
        padding: 28px 36px;
        margin-bottom: 28px;
        display: flex;
        align-items: center;
        gap: 24px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.35);
    }
    .train-header .icon { font-size: 3.2rem; line-height: 1; }
    .train-header h1 {
        margin: 0; font-size: 2rem; font-weight: 700;
        color: #ffffff; letter-spacing: -0.5px;
    }
    .train-header .badge {
        background: #f97316; color: #fff;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem; font-weight: 500;
        padding: 4px 12px; border-radius: 20px;
        margin-top: 6px; display: inline-block;
    }
    .train-header .subtitle { color: #94a3b8; font-size: 0.9rem; margin-top: 4px; }

    /* Metric cards */
    .metric-row { display: flex; gap: 16px; margin-bottom: 28px; flex-wrap: wrap; }
    .metric-card {
        flex: 1; min-width: 140px;
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px 24px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    }
    .metric-card .label { color: #64748b; font-size: 0.75rem; font-weight: 600;
                          text-transform: uppercase; letter-spacing: 1px; }
    .metric-card .value { color: #f1f5f9; font-size: 1.6rem; font-weight: 700;
                          margin-top: 6px; font-family: 'JetBrains Mono', monospace; }
    .metric-card .sub   { color: #94a3b8; font-size: 0.78rem; margin-top: 4px; }

    /* Timeline */
    .timeline-wrap { margin-bottom: 28px; }
    .tl-stop {
        display: flex; align-items: flex-start;
        gap: 0; margin-bottom: 0;
    }
    .tl-left {
        display: flex; flex-direction: column; align-items: center;
        min-width: 36px;
    }
    .tl-dot {
        width: 16px; height: 16px; border-radius: 50%;
        border: 3px solid #f97316; background: #0f172a;
        flex-shrink: 0; margin-top: 6px;
        box-shadow: 0 0 0 4px rgba(249,115,22,0.15);
    }
    .tl-dot.source  { background: #22c55e; border-color: #22c55e;
                      box-shadow: 0 0 0 4px rgba(34,197,94,0.15); }
    .tl-dot.dest    { background: #f97316; border-color: #f97316; }
    .tl-line {
        width: 3px; flex-grow: 1; min-height: 40px;
        background: linear-gradient(to bottom, #334155 0%, #334155 100%);
        margin: 0 auto;
    }
    .tl-content {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 14px 18px;
        margin: 0 0 12px 16px;
        flex: 1;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }
    .tl-content .stn-name { color: #f1f5f9; font-weight: 600; font-size: 1rem; }
    .tl-content .stn-times {
        color: #94a3b8; font-size: 0.8rem; margin-top: 5px;
        font-family: 'JetBrains Mono', monospace;
    }
    .tl-content .stn-times span { color: #38bdf8; font-weight: 500; }
    .tl-content .stn-halt { color: #64748b; font-size: 0.75rem; margin-top: 3px; }
    .stop-num {
        background: #334155; color: #94a3b8;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem; border-radius: 4px;
        padding: 2px 6px; margin-right: 8px;
        display: inline-block;
    }

    /* Table */
    .styled-table {
        width: 100%; border-collapse: collapse;
        font-size: 0.88rem;
    }
    .styled-table th {
        background: #1e293b; color: #94a3b8;
        text-transform: uppercase; letter-spacing: 0.8px;
        font-size: 0.72rem; padding: 12px 16px;
        border-bottom: 2px solid #334155; text-align: left;
    }
    .styled-table td {
        padding: 12px 16px; color: #cbd5e1;
        border-bottom: 1px solid #1e293b;
        font-family: 'JetBrains Mono', monospace; font-size: 0.84rem;
    }
    .styled-table tr:hover td { background: #1e293b; color: #f1f5f9; }
    .styled-table tr:last-child td { border-bottom: none; }
    .table-wrap {
        background: #0f172a; border: 1px solid #334155;
        border-radius: 12px; overflow: hidden;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    }

    /* Sections */
    .section-title {
        color: #64748b; font-size: 0.72rem; font-weight: 600;
        text-transform: uppercase; letter-spacing: 1.2px;
        margin-bottom: 14px; margin-top: 4px;
    }

    /* Hide Streamlit default elements */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 1.5rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <div class="train-header">
        <div class="icon">🚄</div>
        <div>
            <h1>{api_response['train_name']}</h1>
            <div class="badge">Train #{api_response['train_number']}</div>
            <div class="subtitle">
                {route[0]['station']} → {route[-1]['station']} &nbsp;·&nbsp;
                {route[0]['departure']} – {route[-1]['arrival']}
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Metric cards ──────────────────────────────────────────────────────────────
# Total journey time
dep_start = to_minutes(route[0]["departure"])
arr_end   = to_minutes(route[-1]["arrival"])
total_min = arr_end - dep_start
total_h, total_m = divmod(total_min, 60)
total_str = f"{total_h}h {total_m}m"

# Total halt time
halt_total = sum(
    (to_minutes(s["departure"]) - to_minutes(s["arrival"]))
    for s in route
    if to_minutes(s["arrival"]) is not None and to_minutes(s["departure"]) is not None
)
halt_h, halt_m = divmod(halt_total, 60)
halt_str_total = f"{halt_h}h {halt_m}m" if halt_h else f"{halt_m}m"

# Running time
running_min = total_min - halt_total
run_h, run_m = divmod(running_min, 60)
run_str = f"{run_h}h {run_m}m"

st.markdown(
    f"""
    <div class="metric-row">
        <div class="metric-card">
            <div class="label">Total Journey</div>
            <div class="value">{total_str}</div>
            <div class="sub">{route[0]['departure']} → {route[-1]['arrival']}</div>
        </div>
        <div class="metric-card">
            <div class="label">Total Stops</div>
            <div class="value">{n_stops}</div>
            <div class="sub">incl. source &amp; destination</div>
        </div>
        <div class="metric-card">
            <div class="label">Running Time</div>
            <div class="value">{run_str}</div>
            <div class="sub">excl. halts</div>
        </div>
        <div class="metric-card">
            <div class="label">Total Halt</div>
            <div class="value">{halt_str_total}</div>
            <div class="sub">across intermediate stops</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Two-column layout ─────────────────────────────────────────────────────────
col1, col2 = st.columns([1, 1.6], gap="large")

# ── Timeline ──────────────────────────────────────────────────────────────────
with col1:
    st.markdown('<div class="section-title">🗺️ Route Timeline</div>', unsafe_allow_html=True)
    timeline_html = '<div class="timeline-wrap">'

    for i, r in enumerate(rows):
        is_first = i == 0
        is_last  = i == n_stops - 1
        dot_cls  = "source" if is_first else ("dest" if is_last else "")
        show_line = not is_last

        arr_display = r["Arrival"]
        dep_display = r["Departure"]

        times_html = ""
        if is_first:
            times_html = f'<span>Dep:</span> {dep_display}'
        elif is_last:
            times_html = f'<span>Arr:</span> {arr_display}'
        else:
            times_html = f'<span>Arr:</span> {arr_display} &nbsp;|&nbsp; <span>Dep:</span> {dep_display}'

        halt_html = f'<div class="stn-halt">Halt: {r["Halt"]}</div>' if r["Halt"] != "—" else ""

        timeline_html += f"""
        <div class="tl-stop">
            <div class="tl-left">
                <div class="tl-dot {dot_cls}"></div>
                {"<div class='tl-line'></div>" if show_line else ""}
            </div>
            <div class="tl-content">
                <div class="stn-name">
                    <span class="stop-num">#{r['Stop']}</span>{r['Station']}
                </div>
                <div class="stn-times">{times_html}</div>
                {halt_html}
            </div>
        </div>
        """

    timeline_html += "</div>"
    st.markdown(timeline_html, unsafe_allow_html=True)

# ── Table + Progress bar ──────────────────────────────────────────────────────
with col2:
    st.markdown('<div class="section-title">📋 Detailed Schedule</div>', unsafe_allow_html=True)

    # Build HTML table
    table_html = """
    <div class="table-wrap">
    <table class="styled-table">
        <thead>
            <tr>
                <th>#</th>
                <th>Station</th>
                <th>Arrival</th>
                <th>Departure</th>
                <th>Halt</th>
                <th>Travel from Prev</th>
            </tr>
        </thead>
        <tbody>
    """
    for _, row in df.iterrows():
        table_html += f"""
        <tr>
            <td>{row['Stop']}</td>
            <td>{row['Station']}</td>
            <td>{row['Arrival']}</td>
            <td>{row['Departure']}</td>
            <td>{row['Halt']}</td>
            <td>{row['Travel from Prev']}</td>
        </tr>
        """
    table_html += "</tbody></table></div>"
    st.markdown(table_html, unsafe_allow_html=True)

    # ── Journey progress chart ────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">⏱️ Journey Progress (by time)</div>', unsafe_allow_html=True)

    chart_data = []
    for stop in route:
        t = to_minutes(stop["arrival"]) or to_minutes(stop["departure"])
        if t is not None:
            pct = round((t - dep_start) / total_min * 100, 1)
            chart_data.append({"Station": stop["station"], "Progress (%)": pct})

    chart_df = pd.DataFrame(chart_data).set_index("Station")
    st.bar_chart(chart_df, color="#f97316", height=220)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="text-align:center; color:#334155; font-size:0.75rem;
                margin-top:32px; padding-top:16px;
                border-top: 1px solid #1e293b;">
        Rajdhani Express 12301 · New Delhi → Howrah Jn · Data via API
    </div>
    """,
    unsafe_allow_html=True,
)
