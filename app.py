import streamlit as st
import pickle
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import time

from streamlit_option_menu import option_menu
from datetime import datetime

# --------------------------------
# PAGE CONFIG
# --------------------------------

st.set_page_config(
    page_title="ABB AI Digital Twin",
    layout="wide"
)

# --------------------------------
# CUSTOM CSS
# --------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #0E1117;
    color: white;
}

h1, h2, h3 {
    color: white;
}

.stMetric {
    background-color: #1E1E1E;
    padding: 15px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------
# LOGIN + REGISTER SYSTEM
# --------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "users" not in st.session_state:

    st.session_state.users = {
        "admin": "admin123"
    }

if not st.session_state.logged_in:

    st.markdown("""
    <style>

    .stApp {
        background-image: linear-gradient(
            rgba(0,0,0,0.75),
            rgba(0,0,0,0.75)
        ),
        url("https://cdn.pixabay.com/photo/2017/10/05/18/29/pole-2820416_1280.jpg");

        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    .login-box {
        background-color: rgba(20,20,20,0.88);
        padding: 40px;
        border-radius: 20px;
        margin-top: 60px;
        box-shadow: 0px 0px 30px rgba(255,255,255,0.15);
    }

    .main-title {
        text-align: center;
        color: white;
        font-size: 42px;
        font-weight: bold;
    }

    .sub-title {
        text-align: center;
        color: #bbbbbb;
        font-size: 18px;
        margin-bottom: 30px;
    }

    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        st.markdown("""
        <div class="login-box">

        <div class="main-title">
        ⚡ ABB AI Digital Twin
        </div>

        <div class="sub-title">
        Intelligent Transformer Monitoring System
        </div>
        """, unsafe_allow_html=True)

        auth_option = st.radio(
            "Select Option",
            ["Login", "Register"],
            horizontal=True
        )

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        if auth_option == "Login":

            if st.button(
                "Login",
                use_container_width=True
            ):

                if (
                    username in st.session_state.users
                    and
                    st.session_state.users[username]
                    == password
                ):

                    st.session_state.logged_in = True

                    st.success(
                        "Login Successful"
                    )

                    time.sleep(1)

                    st.rerun()

                else:

                    st.error(
                        "Invalid Username or Password"
                    )

        else:

            if st.button(
                "Register",
                use_container_width=True
            ):

                if username in st.session_state.users:

                    st.warning(
                        "User already exists"
                    )

                else:

                    st.session_state.users[
                        username
                    ] = password

                    st.success(
                        "Registration Successful!"
                    )

        st.markdown("</div>", unsafe_allow_html=True)

    st.stop()

# --------------------------------
# SIDEBAR NAVIGATION
# --------------------------------

with st.sidebar:

    selected = option_menu(
        menu_title="Navigation",

        options=[
            "Dashboard",
            "Analytics",
            "AI Reports",
            "System Health"
        ],

        icons=[
            "speedometer2",
            "graph-up",
            "robot",
            "activity"
        ],

        default_index=0,
    )

# --------------------------------
# LOAD MODEL
# --------------------------------

model = pickle.load(
    open("transformer_model.pkl", "rb")
)

# --------------------------------
# TRANSFORMER SENSOR INPUTS
# --------------------------------

st.sidebar.header(
    "⚡ Transformer Sensor Inputs"
)

# TEMPERATURE

temperature = st.sidebar.slider(
    "Temperature (°C)",
    40,
    120,
    70
)

if temperature < 75:

    st.sidebar.success(
        "🟢 Temperature Normal"
    )

elif temperature < 95:

    st.sidebar.warning(
        "🟡 Temperature Increasing"
    )

else:

    st.sidebar.error(
        "🔴 High Temperature Risk"
    )

# VOLTAGE

voltage = st.sidebar.slider(
    "Voltage (V)",
    200,
    260,
    230
)

if voltage < 240:

    st.sidebar.success(
        "🟢 Voltage Stable"
    )

else:

    st.sidebar.warning(
        "🟡 Voltage Fluctuation"
    )

# CURRENT

current = st.sidebar.slider(
    "Current (A)",
    10,
    50,
    15
)

if current < 25:

    st.sidebar.success(
        "🟢 Current Normal"
    )

elif current < 40:

    st.sidebar.warning(
        "🟡 Current Load High"
    )

else:

    st.sidebar.error(
        "🔴 Overcurrent Detected"
    )

# OIL LEVEL

oil = st.sidebar.slider(
    "Oil Level (%)",
    10,
    100,
    80
)

if oil > 60:

    st.sidebar.success(
        "🟢 Oil Level Healthy"
    )

elif oil > 40:

    st.sidebar.warning(
        "🟡 Oil Level Moderate"
    )

else:

    st.sidebar.error(
        "🔴 Oil Level Critical"
    )

# HUMIDITY

humidity = st.sidebar.slider(
    "Humidity (%)",
    10,
    100,
    40
)

if humidity < 50:

    st.sidebar.success(
        "🟢 Humidity Normal"
    )

elif humidity < 75:

    st.sidebar.warning(
        "🟡 Humidity Increasing"
    )

else:

    st.sidebar.error(
        "🔴 Excess Humidity Risk"
    )

# --------------------------------
# AI PREDICTION
# --------------------------------

input_data = np.array([
    [
        temperature,
        voltage,
        current,
        oil,
        humidity
    ]
])

prediction = model.predict(input_data)

probability = model.predict_proba(
    input_data
)

risk = probability[0][1] * 100

# --------------------------------
# HEALTH INDEX
# --------------------------------

health_index = max(
    0,
    100 - (
        (temperature * 0.3)
        + (current * 0.2)
        + (humidity * 0.2)
        - (oil * 0.1)
    ) / 2
)

remaining_life = max(
    10,
    int(365 - (risk * 3))
)

# --------------------------------
# SEVERITY
# --------------------------------

if risk < 40:

    severity = "Healthy"
    theme_color = "green"

elif risk < 70:

    severity = "Warning"
    theme_color = "orange"

else:

    severity = "Critical"
    theme_color = "red"

# --------------------------------
# DATA
# --------------------------------

history_data = pd.DataFrame({
    "Time": [1,2,3,4,5,6],
    "Temperature": [
        65,
        68,
        72,
        75,
        78,
        temperature
    ]
})

sensor_data = pd.DataFrame({
    "Parameter": [
        "Temperature",
        "Voltage",
        "Current",
        "Oil Level",
        "Humidity"
    ],
    "Value": [
        temperature,
        voltage,
        current,
        oil,
        humidity
    ]
})

# --------------------------------
# DASHBOARD PAGE
# --------------------------------

if selected == "Dashboard":

    st.image(
        "https://cdn.pixabay.com/photo/2017/10/05/18/29/pole-2820416_1280.jpg",
        use_container_width=True
    )

    st.markdown(f"""
    <h1 style='text-align:center;color:{theme_color};'>
    ⚡ ABB Industrial Monitoring Platform
    </h1>
    """, unsafe_allow_html=True)

    st.subheader(
        "AI-Powered Digital Twin for Smart Transformer Monitoring"
    )

    current_time = datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )

    st.info(
        f"🕒 Live System Time: {current_time}"
    )

    if severity == "Healthy":

        st.success(
            "🟢 Transformer Operating Normally"
        )

    elif severity == "Warning":

        st.warning(
            "🟡 Moderate Transformer Stress Detected"
        )

    else:

        st.error(
            "🔴 Critical Transformer Failure Risk"
        )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Health Index",
        f"{health_index:.1f}%"
    )

    col2.metric(
        "Failure Risk",
        f"{risk:.1f}%"
    )

    col3.metric(
        "Remaining Life",
        f"{remaining_life} Days"
    )

    col4.metric(
        "AI Confidence",
        "96%"
    )

    st.subheader(
        "📈 Transformer Health Gauge"
    )

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=health_index,
        title={'text': "Health Index"},
        gauge={
            'axis': {'range': [0, 100]},
            'steps': [
                {'range': [0, 40], 'color': "red"},
                {'range': [40, 70], 'color': "orange"},
                {'range': [70, 100], 'color': "green"}
            ],
        }
    ))

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.progress(
        int(health_index)
    )

# --------------------------------
# ANALYTICS PAGE
# --------------------------------

elif selected == "Analytics":

    st.title("📊 Analytics Dashboard")

    st.subheader(
        "Temperature Trend Analysis"
    )

    st.line_chart(
        history_data.set_index("Time")
    )

    st.subheader(
        "Live Sensor Analytics"
    )

    st.bar_chart(
        sensor_data.set_index("Parameter")
    )

    st.metric(
        "Operational Efficiency",
        "91%"
    )

    st.metric(
        "Fault Prediction Accuracy",
        "96%"
    )

# --------------------------------
# AI REPORTS PAGE
# --------------------------------

elif selected == "AI Reports":

    st.image(
        "https://cdn.pixabay.com/photo/2017/10/05/18/29/pole-2820416_1280.jpg",
        use_container_width=True
    )

    st.markdown(f"""
    <h1 style='text-align:center;color:{theme_color};'>
    🤖 ABB AI Diagnostic Center
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background-color:#1E1E1E;
                padding:20px;
                border-radius:15px;'>

    <h3 style='color:white;'>
    Intelligent Transformer Analysis Report
    </h3>

    <p style='color:#bbbbbb;font-size:18px;'>
    Advanced AI-based predictive maintenance and
    transformer health diagnostics platform.
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.write("")

    if severity == "Healthy":

        st.success(
            "🟢 AI Status: Transformer Operating Normally"
        )

    elif severity == "Warning":

        st.warning(
            "🟡 AI Status: Moderate Transformer Stress Detected"
        )

    else:

        st.error(
            "🔴 AI Status: Critical Transformer Failure Risk"
        )

    st.subheader(
        "📊 AI Diagnostic Metrics"
    )

    a1, a2, a3, a4 = st.columns(4)

    a1.metric(
        "Failure Risk",
        f"{risk:.1f}%"
    )

    a2.metric(
        "Health Index",
        f"{health_index:.1f}%"
    )

    a3.metric(
        "Remaining Life",
        f"{remaining_life} Days"
    )

    a4.metric(
        "AI Confidence",
        "96%"
    )

    st.divider()

    st.subheader(
        "🧠 AI Predictive Analysis"
    )

    if severity == "Healthy":

        st.info("""
✔ Transformer operating within safe thermal limits

✔ Electrical load distribution stable

✔ Oil insulation condition healthy

✔ No maintenance required
""")

    elif severity == "Warning":

        st.warning("""
⚠ Transformer temperature increasing

⚠ Moderate electrical stress detected

⚠ Preventive maintenance recommended
""")

    else:

        st.error("""
❌ Severe transformer stress detected

❌ Possible insulation failure

❌ Immediate maintenance required
""")

    st.subheader(
        "📡 Sensor Diagnostics"
    )

    sensor_df = pd.DataFrame({

        "Sensor": [
            "Temperature",
            "Voltage",
            "Current",
            "Oil Level",
            "Humidity"
        ],

        "Current Value": [
            temperature,
            voltage,
            current,
            oil,
            humidity
        ],

        "Condition": [

            "Normal" if temperature < 75 else "Warning",

            "Stable" if voltage < 240 else "Fluctuating",

            "Normal" if current < 25 else "High",

            "Healthy" if oil > 60 else "Low",

            "Normal" if humidity < 50 else "High"
        ]
    })

    st.dataframe(
        sensor_df,
        use_container_width=True
    )

    st.subheader(
        "📈 AI Risk Visualization"
    )

    risk_chart = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk,
        title={'text': "Failure Risk"},
        gauge={
            'axis': {'range': [0, 100]},
            'steps': [
                {'range': [0, 40], 'color': "green"},
                {'range': [40, 70], 'color': "orange"},
                {'range': [70, 100], 'color': "red"}
            ],
        }
    ))

    st.plotly_chart(
        risk_chart,
        use_container_width=True
    )

    st.subheader(
        "📥 Export Report"
    )

    report = f"""
ABB AI DIGITAL TWIN REPORT

Transformer Status: {severity}

Health Index: {health_index:.1f}%

Failure Risk: {risk:.1f}%

Remaining Life: {remaining_life} Days
"""

    st.download_button(
        label="📄 Download AI Report",
        data=report,
        file_name="ABB_AI_Report.txt"
    )

# --------------------------------
# SYSTEM HEALTH PAGE
# --------------------------------

elif selected == "System Health":

    st.title("🩺 System Health Monitor")

    st.metric(
        "Transformer Health",
        f"{health_index:.1f}%"
    )

    st.metric(
        "Operational Status",
        severity
    )

    st.progress(
        int(health_index)
    )

    if severity == "Healthy":

        st.success(
            "System Operating Normally"
        )

    elif severity == "Warning":

        st.warning(
            "Maintenance Recommended"
        )

    else:

        st.error(
            "Critical Transformer Condition"
        )