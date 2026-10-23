
import io
import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

# =========================================================
# THEME COLOURS (replaces Streamlit's default red/orange)
# =========================================================
try:
    st._config.set_option("theme.base", "dark")
    st._config.set_option("theme.primaryColor", "#f438d0")
    st._config.set_option("theme.backgroundColor", "#170b29")
    st._config.set_option("theme.secondaryBackgroundColor", "#211035")
    st._config.set_option("theme.textColor", "#f4e9ff")
except Exception:
    pass

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Diabetes Health Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# DARK PURPLE + MAGENTA + VIOLET THEME
# =========================================================
st.markdown("""
<style>
/* ==========================================
   BASE
   ========================================== */
.stApp {
    background: linear-gradient(135deg, #170b29, #24103c 65%, #1a0c30);
    color: #f4e9ff;
    font-family: "Inter", "Segoe UI", sans-serif;
}

[data-testid="stHeader"] { background: #170b29; }
[data-testid="stAppViewContainer"] { background: transparent; }

h1, h2, h3, h4 {
    color: #fff3ff !important;
    font-weight: 700 !important;
    letter-spacing: -0.3px;
}

p, li, label { color: #ddcdee; }

[data-testid="stCaptionContainer"] p { color: #c0acd8 !important; }

hr { border-color: #442653 !important; }

::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: #10091c; }
::-webkit-scrollbar-thumb {
    background: #442653;
    border-radius: 8px;
}
::-webkit-scrollbar-thumb:hover { background: #ff58d7; }

/* ==========================================
   SIDEBAR
   ========================================== */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div:first-child {
    background: #10091c !important;
}

[data-testid="stSidebar"] { border-right: 1px solid #38204a; }

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p { color: #f0e2ff !important; }

[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #ff8ce8 !important; }

[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    color: #decaf0 !important;
    font-weight: 600 !important;
}

[data-testid="stSidebar"] .stButton button,
[data-testid="stSidebar"] .stDownloadButton button {
    background: linear-gradient(100deg, #7125b7, #a626c9) !important;
    color: #ffffff !important;
    border: 1px solid #ff58d7 !important;
    border-radius: 10px !important;
}

[data-testid="stSidebar"] .stButton button:hover,
[data-testid="stSidebar"] .stDownloadButton button:hover {
    background: linear-gradient(100deg, #d831d1, #ff51d6) !important;
    border-color: #ff8ce8 !important;
}

/* ==========================================
   TABS
   ========================================== */
.stTabs [data-baseweb="tab-list"] {
    display: flex;
    gap: 8px !important;
    background: #211035 !important;
    border: 1px solid #442653 !important;
    border-radius: 14px !important;
    padding: 7px !important;
    margin-top: 14px;
    margin-bottom: 24px;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #d9bfef !important;
    border-radius: 10px !important;
    border: 1px solid transparent !important;
    padding: 12px 18px;
    font-size: 0.94rem;
    font-weight: 600;
    transition: all 0.2s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    background: #342047 !important;
    color: #ff8ce8 !important;
    border-color: #ff58d7 !important;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(100deg, #e02dc9, #7b35e8) !important;
    color: #ffffff !important;
    border: 1px solid #ff61d5 !important;
    box-shadow: 0 3px 12px rgba(224, 45, 201, 0.25);
}

.stTabs [data-baseweb="tab-highlight"] {
    background-color: #f438d0 !important;
}

.stTabs [data-baseweb="tab-border"] {
    background-color: #442653 !important;
}

/* ==========================================
   SELECT BOXES (ALL DROPDOWNS)
   ========================================== */
.stApp div[data-baseweb="select"] > div {
    background-color: #211034 !important;
    border: 1px solid #442653 !important;
    border-radius: 10px !important;
    color: #fff4ff !important;
    transition: all 0.2s ease;
}

.stApp div[data-baseweb="select"] > div:hover,
.stApp div[data-baseweb="select"] > div:focus-within {
    border-color: #f438d0 !important;
    box-shadow: 0 0 0 1px #f438d0 !important;
}

.stApp div[data-baseweb="select"] span,
.stApp div[data-baseweb="select"] div {
    color: #fff4ff !important;
}

.stApp div[data-baseweb="select"] svg {
    fill: #ff8ce8 !important;
    color: #ff8ce8 !important;
}

[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background-color: #27103a !important;
    border: 1px solid #ff58d7 !important;
}

/* ==========================================
   DROPDOWN LIST (OPEN MENU) — PURPLE HOVER
   ========================================== */
div[data-baseweb="popover"],
div[data-baseweb="popover"] > div {
    background-color: #1b0c2c !important;
    border-radius: 10px !important;
}

div[data-baseweb="popover"] ul,
ul[role="listbox"],
div[data-baseweb="menu"] {
    background-color: #1b0c2c !important;
    border: 1px solid #4a265f !important;
    border-radius: 10px !important;
    padding: 4px !important;
}

/* normal option */
div[data-baseweb="popover"] li,
ul[role="listbox"] li,
li[role="option"] {
    background-color: transparent !important;
    color: #f4e7ff !important;
    border-radius: 8px !important;
    margin: 2px 0 !important;
    transition: all 0.15s ease;
}

/* currently selected option */
div[data-baseweb="popover"] li[aria-selected="true"],
ul[role="listbox"] li[aria-selected="true"],
li[role="option"][aria-selected="true"] {
    background-color: #3b1955 !important;
    color: #ff8ce8 !important;
    box-shadow: inset 3px 0 0 #f438d0;
}

/* hovered / keyboard-focused option */
div[data-baseweb="popover"] li:hover,
div[data-baseweb="popover"] li:focus,
ul[role="listbox"] li:hover,
ul[role="listbox"] li:focus,
li[role="option"]:hover,
li[role="option"]:focus {
    background: linear-gradient(100deg, #e02dc9, #7b35e8) !important;
    color: #ffffff !important;
}

div[data-baseweb="popover"] li:hover *,
ul[role="listbox"] li:hover *,
li[role="option"]:hover * {
    color: #ffffff !important;
}

/* ==========================================
   TEXT / NUMBER INPUTS
   ========================================== */
.stApp div[data-baseweb="input"],
.stApp div[data-baseweb="base-input"] {
    background-color: #211034 !important;
    border-radius: 9px !important;
}

.stApp div[data-baseweb="input"] {
    border: 1px solid #442653 !important;
}

.stApp div[data-baseweb="input"]:hover,
.stApp div[data-baseweb="input"]:focus-within {
    border-color: #f438d0 !important;
    box-shadow: 0 0 0 1px #f438d0 !important;
}

.stApp input {
    color: #fff4ff !important;
    background-color: transparent !important;
}

.stApp button[kind="stepper"],
[data-testid="stNumberInput"] button {
    background-color: #211034 !important;
    color: #ff8ce8 !important;
}

.stApp button[kind="stepper"]:hover,
[data-testid="stNumberInput"] button:hover {
    background-color: #4a1c55 !important;
    color: #ffffff !important;
}

/* ==========================================
   MULTISELECT TAGS
   ========================================== */
[data-baseweb="tag"],
span[data-baseweb="tag"] {
    background: linear-gradient(100deg, #e02dc9, #7b35e8) !important;
    background-color: #c635e3 !important;
    color: #ffffff !important;
    border: 1px solid #ff61d5 !important;
    border-radius: 8px !important;
}

[data-baseweb="tag"] span,
[data-baseweb="tag"] div {
    color: #ffffff !important;
}

[data-baseweb="tag"] svg {
    fill: #ff8ce8 !important;
    color: #ff8ce8 !important;
}

[data-baseweb="tag"]:hover {
    background: linear-gradient(100deg, #f72fd1, #b83eff) !important;
    border-color: #ff8ce8 !important;
}

/* ==========================================
   SLIDERS
   ========================================== */
[data-testid="stSlider"] [role="slider"] {
    background-color: #f438d0 !important;
    border: 2px solid #fff0ff !important;
    box-shadow: 0 0 8px rgba(244, 56, 208, 0.35) !important;
}

[data-testid="stSlider"] [role="slider"]:hover,
[data-testid="stSlider"] [role="slider"]:focus {
    background-color: #ff8ce8 !important;
    border-color: #ffffff !important;
    box-shadow: 0 0 10px rgba(244, 56, 208, 0.55) !important;
}

[data-testid="stSliderThumbValue"],
[data-testid="stSliderThumbValue"] p,
[data-testid="stSlider"] [data-testid="stThumbValue"] {
    color: #ff8ce8 !important;
}

[data-testid="stSliderTickBarMin"],
[data-testid="stSliderTickBarMax"],
[data-testid="stSlider"] [data-testid="stTickBar"] {
    color: #d9bfef !important;
}

/* ==========================================
   CHECKBOX / RADIO / TOGGLE
   ========================================== */
input[type="checkbox"],
input[type="radio"] { accent-color: #f438d0 !important; }

/* ==========================================
   METRIC CARDS
   ========================================== */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #c332d5 0%, #8b35e8 100%);
    border: 1px solid #e34acf;
    border-radius: 16px;
    padding: 20px 18px;
    box-shadow: 0 6px 20px rgba(139, 53, 232, 0.18);
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p {
    color: #ffe9fa !important;
    font-weight: 600 !important;
}

[data-testid="stMetricValue"],
[data-testid="stMetricValue"] div {
    color: #ffffff !important;
    font-weight: 800 !important;
}

[data-testid="stMetricDelta"] { color: #ffd7f7 !important; }

[data-testid="stHorizontalBlock"] [data-testid="stColumn"]:nth-child(even)
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #ed39ce 0%, #8a43ff 100%);
    border-color: #ff72df;
}

/* ==========================================
   BUTTONS
   ========================================== */
.stButton button,
.stDownloadButton button,
.stFormSubmitButton button,
button[kind="primary"],
button[kind="secondaryFormSubmit"] {
    background: linear-gradient(100deg, #d932ca, #8537f2) !important;
    color: #ffffff !important;
    border: 1px solid #de35d4 !important;
    border-radius: 10px !important;
    font-weight: 650 !important;
}

.stButton button:hover,
.stDownloadButton button:hover,
.stFormSubmitButton button:hover {
    background: linear-gradient(100deg, #fb4ad6, #b33cff) !important;
    border-color: #f438d0 !important;
    color: #ffffff !important;
}

.stButton button:focus,
.stDownloadButton button:focus,
.stFormSubmitButton button:focus {
    outline: 2px solid #f438d0 !important;
    outline-offset: 2px !important;
    box-shadow: none !important;
}

/* ==========================================
   TABLES, EXPANDERS, FORMS, UPLOADER, ALERTS
   ========================================== */
[data-testid="stDataFrame"] {
    border: 1px solid #442653;
    border-radius: 12px;
    overflow: hidden;
}

[data-testid="stExpander"] {
    background: #211035;
    border: 1px solid #442653;
    border-radius: 12px;
}

[data-testid="stForm"] {
    background: rgba(33, 16, 53, 0.55);
    border: 1px solid #442653;
    border-radius: 14px;
}

[data-testid="stFileUploader"] {
    background: #211035;
    border: 1px dashed #654276;
    border-radius: 12px;
    padding: 12px;
}

[data-testid="stFileUploader"] button {
    background: linear-gradient(100deg, #7125b7, #a626c9) !important;
    color: #ffffff !important;
    border: 1px solid #ff58d7 !important;
}

/* alerts: dark cards with a theme-coloured left accent (no orange/yellow) */
[data-testid="stAlert"],
[data-testid="stAlert"] > div {
    background: #211034 !important;
    border: 1px solid #54305d !important;
    border-left: 4px solid #ff61d5 !important;
    border-radius: 12px !important;
    color: #f4e9ff !important;
}

[data-testid="stAlert"] p,
[data-testid="stAlert"] div { color: #f4e9ff !important; }

[data-testid="stAlert"] svg {
    fill: #ff8ce8 !important;
    color: #ff8ce8 !important;
}

a { color: #ff8ce8 !important; }

[data-testid="stProgress"] > div > div > div > div {
    background-color: #f438d0 !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# FILES AND CONSTANTS
# =========================================================
DATA_FILE = "diabetes_binary_health_indicators_BRFSS2015.csv"
COMPARISON_FILE = "diabetes_model_comparison.csv"

LOGISTIC_FILE = "logistic_regression_model.pkl"
FOREST_FILE = "random_forest_model.pkl"
SCALER_FILE = "diabetes_feature_scaler.pkl"

# Folder where app.py lives (works no matter where Streamlit is launched from)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SEARCH_FOLDERS = [
    BASE_DIR,
    os.path.join(BASE_DIR, "data"),
    os.path.join(BASE_DIR, "models"),
    os.getcwd()
]

FEATURES = [
    "HighBP", "HighChol", "CholCheck", "BMI", "Smoker",
    "Stroke", "HeartDiseaseorAttack", "PhysActivity", "Fruits",
    "Veggies", "HvyAlcoholConsump", "AnyHealthcare",
    "NoDocbcCost", "GenHlth", "MentHlth", "PhysHlth",
    "DiffWalk", "Sex", "Age", "Education", "Income"
]

BINARY_FEATURES = [
    "HighBP", "HighChol", "CholCheck", "Smoker", "Stroke",
    "HeartDiseaseorAttack", "PhysActivity", "Fruits", "Veggies",
    "HvyAlcoholConsump", "AnyHealthcare", "NoDocbcCost",
    "DiffWalk", "Sex"
]

LABELS = {
    "HighBP": "High Blood Pressure",
    "HighChol": "High Cholesterol",
    "CholCheck": "Cholesterol Check",
    "BMI": "Body Mass Index",
    "Smoker": "Smoker",
    "Stroke": "History of Stroke",
    "HeartDiseaseorAttack": "Heart Disease / Attack",
    "PhysActivity": "Physical Activity",
    "Fruits": "Fruit Consumption",
    "Veggies": "Vegetable Consumption",
    "HvyAlcoholConsump": "Heavy Alcohol Consumption",
    "AnyHealthcare": "Healthcare Coverage",
    "NoDocbcCost": "Could Not Visit Doctor Due to Cost",
    "GenHlth": "General Health",
    "MentHlth": "Mental Health Days",
    "PhysHlth": "Physical Health Days",
    "DiffWalk": "Difficulty Walking",
    "Sex": "Sex",
    "Age": "Age Category",
    "Education": "Education",
    "Income": "Income"
}

AGE_LABELS = {
    1: "18–24", 2: "25–29", 3: "30–34",
    4: "35–39", 5: "40–44", 6: "45–49",
    7: "50–54", 8: "55–59", 9: "60–64",
    10: "65–69", 11: "70–74", 12: "75–79", 13: "80+"
}

HEALTH_LABELS = {
    1: "Excellent",
    2: "Very Good",
    3: "Good",
    4: "Fair",
    5: "Poor"
}

EDUCATION_LABELS = {
    1: "Never attended / Kindergarten",
    2: "Grades 1–8",
    3: "Grades 9–11",
    4: "Grade 12 / GED",
    5: "College 1–3 years",
    6: "College 4+ years"
}

INCOME_LABELS = {
    1: "Below $10,000",
    2: "$10,000–$14,999",
    3: "$15,000–$19,999",
    4: "$20,000–$24,999",
    5: "$25,000–$34,999",
    6: "$35,000–$49,999",
    7: "$50,000–$74,999",
    8: "$75,000 or more"
}

COLORS = ["#c23bff", "#f438d0", "#8a43ff", "#853eff", "#b57bff"]

# =========================================================
# HELPER FUNCTIONS
# =========================================================
def find_file(filename):
    """Look for a file next to app.py (or in data/ or models/ folders)."""
    for folder in SEARCH_FOLDERS:
        path = os.path.join(folder, filename)
        if os.path.exists(path):
            return path
    return None


def style_chart(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="#f0e5ff",
            family="Inter, Segoe UI, sans-serif"
        ),
        title_font=dict(color="#fff3ff", size=18),
        margin=dict(l=20, r=20, t=60, b=35),
        xaxis=dict(
            gridcolor="#39224d",
            zerolinecolor="#39224d",
            tickfont=dict(color="#f0e5ff"),
            title_font=dict(color="#dfc5f1")
        ),
        yaxis=dict(
            gridcolor="#39224d",
            zerolinecolor="#39224d",
            tickfont=dict(color="#f0e5ff"),
            title_font=dict(color="#dfc5f1")
        ),
        legend=dict(font=dict(color="#f0e5ff")),
        legend_title_font=dict(color="#dfc5f1"),
        hoverlabel=dict(
            bgcolor="#211034",
            bordercolor="#f438d0",
            font=dict(color="#ffffff")
        )
    )
    return fig


def vertical_box_plot(data, title, y_label, color, fill):
    fig = px.box(
        y=data,
        points="outliers",
        title=title,
        labels={"y": y_label}
    )

    fig.update_traces(
        marker=dict(color=color, size=6),
        line=dict(color=color, width=2),
        fillcolor=fill,
        width=0.4
    )

    fig = style_chart(fig)

    fig.update_layout(
        height=520,
        xaxis=dict(showticklabels=False, showgrid=False),
        yaxis=dict(title=y_label, range=[-1, 31])
    )

    return fig


def get_target(data):
    for col in [
        "Diabetes_binary", "diabetes_binary",
        "Diabetes_012", "diabetes_012"
    ]:
        if col in data.columns:
            return col
    return None


def clean_dataset(data):
    data.columns = data.columns.astype(str).str.strip()

    for col in data.columns:
        try:
            data[col] = pd.to_numeric(data[col])
        except (ValueError, TypeError):
            pass

    return data


@st.cache_data(show_spinner="Loading dataset...")
def load_csv_from_path(path):
    return clean_dataset(pd.read_csv(path))


@st.cache_data(show_spinner="Reading uploaded file...")
def load_csv_from_bytes(content):
    return clean_dataset(pd.read_csv(io.BytesIO(content)))


@st.cache_resource(show_spinner=False)
def _load_model_cached(path):
    return joblib.load(path)


def load_model(filename):
    path = find_file(filename)

    if path is None:
        return None

    try:
        return _load_model_cached(path)
    except Exception as error:
        st.error(f"Could not load {filename}: {error}")
        return None


def diabetes_positive(series, target_name):
    if target_name.lower() == "diabetes_012":
        return series.isin([1, 2])
    return series.eq(1)


# =========================================================
# HEADER
# =========================================================
st.title("Diabetes Health Indicators")
st.caption(
    "Interactive analytics  •  Risk factors  •  "
    "Model performance  •  Prediction"
)

# =========================================================
# SIDEBAR HEADER + RESET
# =========================================================
st.sidebar.markdown("""
<div style="padding:8px 0 16px;border-bottom:1px solid #442653;margin-bottom:18px">
    <div style="font-size:21px;font-weight:750;color:#fff3ff">
        ◈ Health Analytics
    </div>
    <div style="font-size:12px;color:#b89ac8;margin-top:5px">
        DASHBOARD FILTERS
    </div>
</div>
""", unsafe_allow_html=True)

if "reset_count" not in st.session_state:
    st.session_state.reset_count = 0

if st.sidebar.button("↻ Reset All Filters", use_container_width=True):
    st.session_state.reset_count += 1
    st.rerun()

reset = st.session_state.reset_count

# =========================================================
# DATA LOADING — BUNDLED DATASET LOADS AUTOMATICALLY
# =========================================================
with st.sidebar.expander("Use your own dataset (optional)", expanded=False):
    custom_upload = st.file_uploader(
        "Upload CSV", type=["csv"], key="custom_upload"
    )

DATA_PATH = find_file(DATA_FILE)
COMPARISON_PATH = find_file(COMPARISON_FILE)

try:
    if custom_upload is not None:
        df = load_csv_from_bytes(custom_upload.getvalue())
    elif DATA_PATH is not None:
        df = load_csv_from_path(DATA_PATH)
    else:
        st.error(
            f"Dataset file not found: {DATA_FILE}\n\n"
            "Place this file in the same folder as app.py and "
            "restart the app."
        )
        st.caption(f"Folder searched: {BASE_DIR}")

        try:
            st.caption(
                "Files found there: " +
                ", ".join(sorted(os.listdir(BASE_DIR)))
            )
        except Exception:
            pass

        st.stop()
except Exception as error:
    st.error(f"Unable to load dataset: {error}")
    st.stop()

TARGET = get_target(df)

if TARGET:
    df[TARGET] = pd.to_numeric(df[TARGET], errors="coerce")

    if TARGET.lower() == "diabetes_012":
        status_labels = {
            0: "No Diabetes",
            1: "Prediabetes",
            2: "Diabetes"
        }
    else:
        status_labels = {
            0: "No Diabetes",
            1: "Diabetes"
        }

    df["Diabetes Status"] = (
        df[TARGET].map(status_labels).fillna("Unknown")
    )

view = df.copy()

# =========================================================
# SIDEBAR FILTERS
# =========================================================
st.sidebar.divider()
st.sidebar.subheader("Age & BMI")

if "Age" in view:
    age_values = pd.to_numeric(
        view["Age"], errors="coerce"
    ).dropna()

    if not age_values.empty:
        age_range = st.sidebar.slider(
            "Age Category",
            int(age_values.min()),
            int(age_values.max()),
            (int(age_values.min()), int(age_values.max())),
            key=f"age_{reset}"
        )

        view = view[
            pd.to_numeric(view["Age"], errors="coerce").between(*age_range)
        ]

if "BMI" in view:
    bmi_values = pd.to_numeric(
        view["BMI"], errors="coerce"
    ).dropna()

    if not bmi_values.empty and bmi_values.min() < bmi_values.max():
        bmi_range = st.sidebar.slider(
            "BMI Range",
            float(bmi_values.min()),
            float(bmi_values.max()),
            (float(bmi_values.min()), float(bmi_values.max())),
            key=f"bmi_{reset}"
        )

        view = view[
            pd.to_numeric(view["BMI"], errors="coerce").between(*bmi_range)
        ]

with st.sidebar.expander(
    "Blood Pressure, Cholesterol & Lifestyle",
    expanded=True
):
    for col in BINARY_FEATURES:
        if col in view:
            choice = st.selectbox(
                LABELS.get(col, col),
                ["All", "Yes", "No"],
                key=f"{col}_{reset}"
            )

            if choice != "All":
                expected = 1 if choice == "Yes" else 0
                view = view[
                    pd.to_numeric(view[col], errors="coerce") == expected
                ]

for col, mapping, heading in [
    ("GenHlth", HEALTH_LABELS, "General Health"),
    ("Education", EDUCATION_LABELS, "Education Level"),
    ("Income", INCOME_LABELS, "Income Level")
]:
    if col in view:
        codes = sorted(
            pd.to_numeric(view[col], errors="coerce")
            .dropna().astype(int).unique()
        )

        if codes:
            options = {
                mapping.get(int(value), str(value)): int(value)
                for value in codes
            }

            selected = st.sidebar.multiselect(
                heading,
                list(options.keys()),
                default=list(options.keys()),
                key=f"{col}_{reset}"
            )

            view = view[
                view[col].isin([options[item] for item in selected])
            ]

# Download filtered data
st.sidebar.divider()
st.sidebar.subheader("Export Data")

st.sidebar.download_button(
    "⬇ Download Filtered CSV",
    data=view.to_csv(index=False).encode("utf-8"),
    file_name="filtered_diabetes_health_data.csv",
    mime="text/csv",
    use_container_width=True
)

# =========================================================
# TOP NAVIGATION
# =========================================================
overview_tab, risk_tab, model_tab, prediction_tab = st.tabs([
    "◈ Overview",
    "✦ Risk Factor Analysis",
    "▥ Model Performance",
    "◎ Diabetes Prediction"
])

# =========================================================
# TAB 1: OVERVIEW
# =========================================================
with overview_tab:
    st.subheader("Dashboard Overview")

    if view.empty:
        st.warning(
            "No records match these filters. Reset filters and try again."
        )

    else:
        total_records = len(view)

        avg_bmi = (
            pd.to_numeric(view["BMI"], errors="coerce").mean()
            if "BMI" in view else np.nan
        )

        diabetes_rate = np.nan

        if TARGET:
            diabetes_rate = (
                diabetes_positive(view[TARGET], TARGET).mean() * 100
            )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Filtered Records", f"{total_records:,}")

        col2.metric(
            "Diabetes Rate",
            f"{diabetes_rate:.1f}%"
            if pd.notna(diabetes_rate) else "N/A"
        )

        col3.metric(
            "Average BMI",
            f"{avg_bmi:.1f}" if pd.notna(avg_bmi) else "N/A"
        )

        col4.metric(
            "Available Indicators",
            len([feature for feature in FEATURES if feature in view])
        )

        st.divider()
        st.subheader("Automatic Insights")

        if pd.notna(diabetes_rate):
            st.write(
                f"• Diabetes-positive rate in the selected records: "
                f"**{diabetes_rate:.1f}%**."
            )

        if pd.notna(avg_bmi):
            st.write(
                f"• Average BMI in the selected records: **{avg_bmi:.1f}**."
            )

        if "GenHlth" in view:
            average_health = pd.to_numeric(
                view["GenHlth"], errors="coerce"
            ).mean()

            if pd.notna(average_health):
                st.write(
                    f"• Average general-health code: "
                    f"**{average_health:.2f}** "
                    "(1 = Excellent, 5 = Poor)."
                )

        st.divider()

        left, right = st.columns(2)

        with left:
            if "Diabetes Status" in view:
                counts = (
                    view["Diabetes Status"]
                    .value_counts()
                    .rename_axis("Status")
                    .reset_index(name="Records")
                )

                fig = px.pie(
                    counts,
                    names="Status",
                    values="Records",
                    hole=0.55,
                    title="Diabetes Status Distribution",
                    color_discrete_sequence=COLORS
                )

                st.plotly_chart(
                    style_chart(fig), use_container_width=True
                )

            elif "BMI" in view:
                fig = px.histogram(
                    view,
                    x="BMI",
                    title="BMI Distribution",
                    color_discrete_sequence=["#f438d0"]
                )

                st.plotly_chart(
                    style_chart(fig), use_container_width=True
                )

        with right:
            if TARGET and "Age" in view:
                temp = view.dropna(subset=["Age", TARGET]).copy()

                if not temp.empty:
                    temp["_positive"] = diabetes_positive(
                        temp[TARGET], TARGET
                    ).astype(int)

                    rates = (
                        temp.groupby("Age", as_index=False)["_positive"]
                        .mean()
                    )

                    rates["Rate (%)"] = rates["_positive"] * 100

                    rates["Age Group"] = (
                        rates["Age"].map(AGE_LABELS)
                        .fillna(rates["Age"].astype(str))
                    )

                    fig = px.bar(
                        rates,
                        x="Age Group",
                        y="Rate (%)",
                        title="Diabetes Rate by Age",
                        color_discrete_sequence=["#c23bff"]
                    )

                    st.plotly_chart(
                        style_chart(fig), use_container_width=True
                    )

        if "GenHlth" in view:
            temp = view.copy()
            temp["Health Description"] = temp["GenHlth"].map(HEALTH_LABELS)

            counts = (
                temp["Health Description"]
                .value_counts()
                .rename_axis("General Health")
                .reset_index(name="Records")
            )

            fig = px.bar(
                counts,
                x="General Health",
                y="Records",
                title="General Health Distribution",
                color_discrete_sequence=["#8a43ff"]
            )

            st.plotly_chart(
                style_chart(fig), use_container_width=True
            )


# =========================================================
# TAB 2: RISK FACTOR ANALYSIS
# =========================================================
with risk_tab:
    st.subheader("Risk Factor Analysis")

    if view.empty:
        st.warning("No records match the selected filters.")

    elif not TARGET:
        st.info("A diabetes target column is required for this analysis.")

    else:
        available_factors = [
            col for col in BINARY_FEATURES if col in view
        ]

        selected_factors = st.multiselect(
            "Choose risk factors to compare",
            available_factors,
            default=available_factors[:5],
            format_func=lambda value: LABELS.get(value, value)
        )

        metric = st.selectbox(
            "Choose comparison metric",
            ["Diabetes Rate (%)", "Number of Records"]
        )

        # Map the dropdown choice to the real column name in the table
        metric_column = {
            "Diabetes Rate (%)": "Diabetes Rate (%)",
            "Number of Records": "Records"
        }[metric]

        results = []

        for factor in selected_factors:
            temp = view[[factor, TARGET]].copy()

            temp[factor] = pd.to_numeric(
                temp[factor], errors="coerce"
            )

            temp[TARGET] = pd.to_numeric(
                temp[TARGET], errors="coerce"
            )

            temp = temp.dropna()

            for value in sorted(temp[factor].unique()):
                group = temp[temp[factor] == value]

                positive = diabetes_positive(group[TARGET], TARGET)

                results.append({
                    "Risk Factor": LABELS.get(factor, factor),
                    "Response": (
                        "Yes" if value == 1
                        else "No" if value == 0
                        else str(value)
                    ),
                    "Records": len(group),
                    "Diabetes Rate (%)": positive.mean() * 100
                })

        if results:
            results_df = pd.DataFrame(results)

            fig = px.bar(
                results_df,
                x="Risk Factor",
                y=metric_column,
                color="Response",
                barmode="group",
                title=f"{metric} by Risk Factor",
                labels={metric_column: metric},
                color_discrete_sequence=["#f438d0", "#c23bff"]
            )

            fig.update_layout(xaxis_tickangle=-25)

            st.plotly_chart(
                style_chart(fig), use_container_width=True
            )

        elif not selected_factors:
            st.info("Select at least one risk factor to display the chart.")

    # Physical & Mental health box plots (vertical, side by side)
    st.divider()

    phys_col, ment_col = st.columns(2)

    with phys_col:
        st.subheader("Physical Health Days — Outlier Analysis")

        if "PhysHlth" in view:
            physical_data = pd.to_numeric(
                view["PhysHlth"], errors="coerce"
            ).dropna()

            if not physical_data.empty:
                fig = vertical_box_plot(
                    physical_data,
                    "Physical Health Days Not Good",
                    "Physical Health Days (0–30)",
                    "#f438d0",
                    "rgba(244,56,208,0.22)"
                )

                st.plotly_chart(fig, use_container_width=True)

                st.caption(
                    "The box represents the middle 50% of values. "
                    "Points beyond the whiskers are potential outliers."
                )
            else:
                st.info("No valid physical health data is available.")
        else:
            st.info("Physical health data is unavailable.")

    with ment_col:
        st.subheader("Mental Health Days — Outlier Analysis")

        if "MentHlth" in view:
            mental_data = pd.to_numeric(
                view["MentHlth"], errors="coerce"
            ).dropna()

            if not mental_data.empty:
                fig = vertical_box_plot(
                    mental_data,
                    "Mental Health Days Not Good",
                    "Mental Health Days (0–30)",
                    "#c23bff",
                    "rgba(194,59,255,0.22)"
                )

                st.plotly_chart(fig, use_container_width=True)

                st.caption(
                    "The box represents the middle 50% of values. "
                    "Points beyond the whiskers are potential outliers."
                )
            else:
                st.info("No valid mental health data is available.")
        else:
            st.info("Mental health data is unavailable.")

    # Correlation heatmap
    numeric_data = view.select_dtypes(include=np.number)

    if len(numeric_data.columns) >= 2:
        st.divider()
        st.subheader("Indicator Correlations")

        correlation_options = [
            col for col in numeric_data.columns if col != TARGET
        ]

        selected_columns = st.multiselect(
            "Choose indicators for correlation chart",
            correlation_options,
            default=correlation_options[:10],
            key="correlation_columns"
        )

        if len(selected_columns) >= 2:
            corr_matrix = view[selected_columns].corr(numeric_only=True)

            fig = px.imshow(
                corr_matrix,
                text_auto=".2f",
                aspect="auto",
                title="Correlation Heatmap",
                color_continuous_scale=[
                    [0.0, "#7b35e8"],   # strong negative: violet
                    [0.5, "#24113d"],   # near zero: dark purple
                    [1.0, "#f438d0"]    # strong positive: magenta
                ],
                zmin=-1,
                zmax=1
            )

            fig = style_chart(fig)

            fig.update_traces(
                textfont=dict(color="#ffffff", size=13),
                xgap=3,
                ygap=3
            )

            fig.update_layout(
                height=max(480, 48 * len(selected_columns) + 160),
                margin=dict(l=20, r=20, t=60, b=90),
                xaxis=dict(
                    tickangle=-35,
                    showgrid=False,
                    tickfont=dict(color="#edddff", size=12)
                ),
                yaxis=dict(
                    showgrid=False,
                    tickfont=dict(color="#edddff", size=12)
                ),
                coloraxis_colorbar=dict(
                    tickfont=dict(color="#f0e5ff"),
                    outlinewidth=0,
                    thickness=14
                )
            )

            st.plotly_chart(fig, use_container_width=True)


# =========================================================
# TAB 3: MODEL PERFORMANCE
# =========================================================
with model_tab:
    st.subheader("Model Performance Comparison")

    if COMPARISON_PATH is not None:
        try:
            comp = pd.read_csv(COMPARISON_PATH)
            comp.columns = comp.columns.astype(str).str.strip()

            st.dataframe(
                comp,
                use_container_width=True,
                hide_index=True
            )

            normalized = {
                str(col).lower().replace("_", "").replace("-", "").replace(" ", ""): col
                for col in comp.columns
            }

            model_col = next(
                (
                    normalized[key]
                    for key in [
                        "model", "modelname", "classifier", "algorithm"
                    ]
                    if key in normalized
                ),
                None
            )

            aliases = {
                "Accuracy": ["accuracy"],
                "Precision": ["precision"],
                "Recall": ["recall"],
                "F1-Score": ["f1score", "f1"],
                "AUC": ["auc", "rocauc", "rocaucscore"]
            }

            metric_cols = {}

            for display_name, keys in aliases.items():
                for key in keys:
                    if key in normalized:
                        column = normalized[key]

                        if pd.api.types.is_numeric_dtype(comp[column]):
                            metric_cols[display_name] = column
                            break

            if model_col and metric_cols:
                selected_metrics = st.multiselect(
                    "Choose metrics to compare",
                    list(metric_cols.keys()),
                    default=[
                        metric_name for metric_name in [
                            "Accuracy", "Precision", "Recall", "F1-Score"
                        ] if metric_name in metric_cols
                    ]
                )

                if selected_metrics:
                    chart_data = comp[
                        [model_col] +
                        [metric_cols[m] for m in selected_metrics]
                    ].copy()

                    rename_columns = {
                        metric_cols[m]: m for m in selected_metrics
                    }

                    chart_data = chart_data.rename(
                        columns=rename_columns
                    )

                    long_data = chart_data.melt(
                        id_vars=[model_col],
                        var_name="Metric",
                        value_name="Score"
                    )

                    long_data["Score"] = pd.to_numeric(
                        long_data["Score"], errors="coerce"
                    )

                    long_data = long_data.dropna(subset=["Score"])

                    fig = px.bar(
                        long_data,
                        x=model_col,
                        y="Score",
                        color="Metric",
                        barmode="group",
                        title="Grouped Model Performance",
                        color_discrete_sequence=COLORS
                    )

                    if (
                        not long_data.empty
                        and long_data["Score"].min() >= 0
                        and long_data["Score"].max() <= 1
                    ):
                        fig.update_yaxes(range=[0, 1])

                    st.plotly_chart(
                        style_chart(fig), use_container_width=True
                    )

            else:
                st.info(
                    "The comparison CSV needs a model-name column and "
                    "numeric performance columns such as Accuracy, "
                    "Precision, Recall, F1-Score or AUC."
                )

        except Exception as error:
            st.error(f"Could not read model comparison: {error}")

    else:
        st.warning(
            f"{COMPARISON_FILE} was not found. "
            "Place it in the same folder as app.py to show the results."
        )


# =========================================================
# TAB 4: DIABETES PREDICTION
# =========================================================
with prediction_tab:
    st.subheader("Try a Diabetes Prediction")
    st.caption(
        "Enter health-indicator values and compare your saved models."
    )

    logistic_model = load_model(LOGISTIC_FILE)
    forest_model = load_model(FOREST_FILE)
    scaler = load_model(SCALER_FILE)

    available_models = {}

    if logistic_model is not None:
        available_models["Logistic Regression"] = logistic_model

    if forest_model is not None:
        available_models["Random Forest"] = forest_model

    if not available_models:
        st.warning(
            "Saved prediction models were not found. "
            "Place the model PKL files in the same folder as app.py."
        )

    else:
        with st.form("prediction_form"):
            st.markdown("#### Personal & Health Indicators")

            col1, col2, col3 = st.columns(3)

            with col1:
                highbp = st.selectbox(
                    "High Blood Pressure", [0, 1],
                    format_func=lambda x: "Yes" if x else "No"
                )

                highchol = st.selectbox(
                    "High Cholesterol", [0, 1],
                    format_func=lambda x: "Yes" if x else "No"
                )

                cholcheck = st.selectbox(
                    "Cholesterol Check", [0, 1],
                    format_func=lambda x: "Yes" if x else "No"
                )

                bmi = st.number_input(
                    "BMI", min_value=10.0, max_value=100.0,
                    value=27.0, step=0.5
                )

                smoker = st.selectbox(
                    "Smoker", [0, 1],
                    format_func=lambda x: "Yes" if x else "No"
                )

                stroke = st.selectbox(
                    "History of Stroke", [0, 1],
                    format_func=lambda x: "Yes" if x else "No"
                )

                heart = st.selectbox(
                    "Heart Disease / Attack", [0, 1],
                    format_func=lambda x: "Yes" if x else "No"
                )

            with col2:
                activity = st.selectbox(
                    "Physical Activity", [0, 1],
                    format_func=lambda x: "Yes" if x else "No"
                )

                fruits = st.selectbox(
                    "Fruit Consumption", [0, 1],
                    format_func=lambda x: "Yes" if x else "No"
                )

                veggies = st.selectbox(
                    "Vegetable Consumption", [0, 1],
                    format_func=lambda x: "Yes" if x else "No"
                )

                alcohol = st.selectbox(
                    "Heavy Alcohol Consumption", [0, 1],
                    format_func=lambda x: "Yes" if x else "No"
                )

                healthcare = st.selectbox(
                    "Healthcare Coverage", [0, 1],
                    format_func=lambda x: "Yes" if x else "No"
                )

                no_doctor = st.selectbox(
                    "Could Not Visit Doctor Due to Cost", [0, 1],
                    format_func=lambda x: "Yes" if x else "No"
                )

                genhlth = st.selectbox(
                    "General Health",
                    list(HEALTH_LABELS),
                    format_func=lambda x: f"{x} - {HEALTH_LABELS[x]}"
                )

            with col3:
                menthlth = st.number_input(
                    "Mental Health Days", 0, 30, 0
                )

                physhlth = st.number_input(
                    "Physical Health Days", 0, 30, 0
                )

                diffwalk = st.selectbox(
                    "Difficulty Walking", [0, 1],
                    format_func=lambda x: "Yes" if x else "No"
                )

                sex = st.selectbox(
                    "Sex Code", [0, 1],
                    format_func=lambda x:
                    "Female (0)" if x == 0 else "Male (1)"
                )

                age = st.selectbox(
                    "Age Category",
                    list(AGE_LABELS),
                    index=8,
                    format_func=lambda x: f"{x} - {AGE_LABELS[x]}"
                )

                education = st.selectbox(
                    "Education",
                    list(EDUCATION_LABELS),
                    index=5,
                    format_func=lambda x:
                    f"{x} - {EDUCATION_LABELS[x]}"
                )

                income = st.selectbox(
                    "Income",
                    list(INCOME_LABELS),
                    index=4,
                    format_func=lambda x:
                    f"{x} - {INCOME_LABELS[x]}"
                )

            selected_model_name = st.selectbox(
                "Prediction Model",
                list(available_models.keys())
            )

            submitted = st.form_submit_button(
                "Predict", use_container_width=True
            )

        if submitted:
            input_values = {
                "HighBP": highbp,
                "HighChol": highchol,
                "CholCheck": cholcheck,
                "BMI": bmi,
                "Smoker": smoker,
                "Stroke": stroke,
                "HeartDiseaseorAttack": heart,
                "PhysActivity": activity,
                "Fruits": fruits,
                "Veggies": veggies,
                "HvyAlcoholConsump": alcohol,
                "AnyHealthcare": healthcare,
                "NoDocbcCost": no_doctor,
                "GenHlth": genhlth,
                "MentHlth": menthlth,
                "PhysHlth": physhlth,
                "DiffWalk": diffwalk,
                "Sex": sex,
                "Age": age,
                "Education": education,
                "Income": income
            }

            input_df = pd.DataFrame(
                [[input_values[feature] for feature in FEATURES]],
                columns=FEATURES
            )

            model = available_models[selected_model_name]

            try:
                prepared_data = input_df

                if (
                    selected_model_name == "Logistic Regression"
                    and scaler is not None
                    and not hasattr(model, "named_steps")
                ):
                    prepared_data = scaler.transform(input_df)

                prediction = model.predict(prepared_data)[0]

                probabilities = (
                    model.predict_proba(prepared_data)[0]
                    if hasattr(model, "predict_proba")
                    else None
                )

                model_classes = (
                    model.classes_.tolist()
                    if hasattr(model, "classes_")
                    else None
                )

                st.divider()
                st.subheader("Prediction Result")

                if int(prediction) == 0:
                    st.success("Model Output: No Diabetes")
                elif int(prediction) == 1:
                    st.warning("Model Output: Diabetes")
                else:
                    st.warning(f"Model Output Class: {prediction}")

                st.write(
                    f"Selected model: **{selected_model_name}**"
                )

                if probabilities is not None:
                    if model_classes is None:
                        model_classes = list(range(len(probabilities)))

                    probability_values = {
                        int(cls): float(prob) * 100
                        for cls, prob in zip(
                            model_classes, probabilities
                        )
                    }

                    st.subheader("Prediction Probability")

                    col1, col2 = st.columns(2)

                    with col1:
                        if 0 in probability_values:
                            st.metric(
                                "No Diabetes",
                                f"{probability_values[0]:.2f}%"
                            )

                    with col2:
                        if 1 in probability_values:
                            st.metric(
                                "Diabetes",
                                f"{probability_values[1]:.2f}%"
                            )

                else:
                    st.info(
                        "This saved model does not provide class "
                        "probabilities, so a percentage cannot be shown."
                    )

            except Exception as error:
                st.error(
                    "Prediction failed. Check that your model and scaler "
                    "were trained with the same 21 features in the same "
                    f"order. Details: {error}"
                )


# =========================================================
# FOOTER
# =========================================================
st.divider()
st.caption("Diabetes Health Indicators Analysis and Prediction")
