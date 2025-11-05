import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import hashlib

# Page configuration
st.set_page_config(
    page_title="MediSmart AI - Healthcare Analytics",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with enhanced styling for login and lock page
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #e3f2fd 0%, #bbdefb 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        font-weight: 600;
    }
    /* Login page styling */
    .login-container {
        max-width: 500px;
        margin: 5rem auto;
        padding: 3rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    .login-title {
        color: white;
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .login-subtitle {
        color: #e0e0e0;
        text-align: center;
        margin-bottom: 2rem;
    }
    /* Lock page styling */
    .lock-container {
        text-align: center;
        padding: 3rem;
        margin: 2rem auto;
        max-width: 800px;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    .lock-icon {
        font-size: 5rem;
        color: #ff6b6b;
        margin-bottom: 1rem;
        animation: pulse 2s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    .lock-title {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .lock-subtitle {
        font-size: 1.3rem;
        color: #555;
        margin-bottom: 2rem;
    }
    .premium-feature {
        display: inline-block;
        margin: 0.5rem;
        padding: 0.8rem 1.5rem;
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        font-weight: 600;
        color: #667eea;
    }
    .upgrade-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 3rem;
        border-radius: 50px;
        font-size: 1.2rem;
        font-weight: bold;
        border: none;
        cursor: pointer;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        transition: all 0.3s;
    }
    .upgrade-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.6);
    }
    /* Premium preview styling */
    .premium-preview-container {
        position: relative;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
        border: 3px solid #667eea;
        animation: glow 2s ease-in-out infinite;
    }
    @keyframes glow {
        0%, 100% { box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3); }
        50% { box-shadow: 0 20px 80px rgba(102, 126, 234, 0.6); }
    }
    </style>
""", unsafe_allow_html=True)

# Authentication system
USERS = {
    "sherlock": {
        "password": "elementary",
        "role": "admin",
        "name": "Sherlock Holmes"
    },
    "drwatson": {
        "password": "moriarty",
        "role": "viewer",
        "name": "Dr. Watson"
    }
}


def check_password(username, password):
    """Validate username and password"""
    if username in USERS:
        if USERS[username]["password"] == password:
            return True, USERS[username]["role"], USERS[username]["name"]
    return False, None, None


def show_login_page():
    """Display beautiful login page"""

    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("""
            <div class="login-container">
                <div class="login-title">🤖 MediSmart AI</div>
                <div class="login-subtitle">Healthcare Analytics Platform</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🔐 Secure Login")

        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit = st.form_submit_button("🚀 Login", use_container_width=True)

            if submit:
                if username and password:
                    valid, role, name = check_password(username, password)
                    if valid:
                        st.session_state['logged_in'] = True
                        st.session_state['username'] = username
                        st.session_state['role'] = role
                        st.session_state['name'] = name
                        st.success(f"✅ Welcome, {name}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")
                else:
                    st.warning("⚠️ Please enter both username and password")


def show_premium_locked():
    """Display beautiful locked premium page"""

    st.markdown("""
        <div class="lock-container">
            <div class="lock-icon">🔒</div>
            <div class="lock-title">Unlock the Potential of AI over Data</div>
            <div class="lock-subtitle">Premium AI-Powered Analytics Awaits</div>
        </div>
    """, unsafe_allow_html=True)

    # Try to display the image if it exists
    image_path = "medi_ai.jpg"
    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True)
    else:
        # Create a beautiful placeholder with gradient
        st.markdown("""
            <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        border-radius: 20px; margin: 2rem 0;">
                <div style="font-size: 8rem; margin-bottom: 1rem;">🤖</div>
                <h2 style="color: white; margin-bottom: 1rem;">AI-Powered Intelligence</h2>
                <p style="color: #e0e0e0; font-size: 1.2rem;">Transform Healthcare Data into Actionable Insights</p>
            </div>
        """, unsafe_allow_html=True)

    # Premium features showcase
    st.markdown("### 🌟 Premium Features Include:")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="premium-feature">🔮 Natural Language Queries</div>
        <div class="premium-feature">📊 Advanced Analytics</div>
        <div class="premium-feature">🎯 Predictive Insights</div>
        <div class="premium-feature">💡 Smart Recommendations</div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="premium-feature">🤖 GPT-Powered Analysis</div>
        <div class="premium-feature">📈 Revenue Optimization</div>
        <div class="premium-feature">🎨 Custom Reports</div>
        <div class="premium-feature">⚡ Real-time Insights</div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Upgrade call-to-action with preview
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style="text-align: center; padding: 2rem; background: white; border-radius: 15px; 
                        box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
                <h3 style="color: #667eea; margin-bottom: 1rem;">🎁 Upgrade to Premium</h3>
                <p style="color: #666; margin-bottom: 1.5rem;">
                    Get access to AI-powered analytics and transform your healthcare data into strategic insights
                </p>
            </div>
        """, unsafe_allow_html=True)

        # Show the actual premium interface as a teaser
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
            <div style="text-align: center; margin: 1rem 0;">
                <h4 style="color: #667eea;">👀 Sneak Peek: AI-Powered Analytics in Action</h4>
                <p style="color: #888; font-size: 0.9rem;">See what you're missing...</p>
            </div>
        """, unsafe_allow_html=True)

        # Display the premium preview screenshot
        preview_path = "premium_preview.png"
        if os.path.exists(preview_path):
            st.markdown('<div class="premium-preview-container">', unsafe_allow_html=True)
            st.image(preview_path, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("""
                <div style="text-align: center; margin-top: 1.5rem;">
                    <p style="color: #667eea; font-size: 0.95rem; font-weight: 600; margin-bottom: 0.5rem;">
                        ✨ Natural Language Queries with Actionable AI Insights
                    </p>
                    <p style="color: #888; font-size: 0.85rem;">
                        Ask: <em>"Show me medicines which needs immediate attention"</em><br>
                        Get: <strong>Instant analysis</strong> + <strong>Specific actions</strong> + <strong>Business recommendations</strong>
                    </p>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Upgrade button
        st.markdown("""
            <div style="text-align: center;">
                <button class="upgrade-button">✨ Upgrade Now</button>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Benefits section
    st.markdown("### 💎 What You'll Get:")

    benefits = [
        {"icon": "🚀", "title": "Ask Anything", "desc": "Query your data in plain English - no SQL needed"},
        {"icon": "🎯", "title": "Actionable Insights", "desc": "Get specific recommendations, not just data dumps"},
        {"icon": "💰", "title": "Revenue Growth", "desc": "Identify lost opportunities and optimize earnings"},
        {"icon": "🔍", "title": "Deep Analytics", "desc": "Uncover patterns invisible to traditional analysis"},
        {"icon": "⚡", "title": "Instant Answers", "desc": "Get results in seconds, not hours"},
        {"icon": "📱", "title": "Export & Share", "desc": "Download insights as CSV for presentations"}
    ]

    cols = st.columns(3)
    for idx, benefit in enumerate(benefits):
        with cols[idx % 3]:
            st.markdown(f"""
                <div style="padding: 1.5rem; background: white; border-radius: 15px; 
                            box-shadow: 0 5px 15px rgba(0,0,0,0.1); margin-bottom: 1rem; 
                            border-left: 4px solid #667eea;">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{benefit['icon']}</div>
                    <h4 style="color: #667eea; margin-bottom: 0.5rem;">{benefit['title']}</h4>
                    <p style="color: #666; font-size: 0.9rem; margin: 0;">{benefit['desc']}</p>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Contact/Support section
    st.info("💬 **Want to learn more?** Contact your administrator to upgrade your account to Premium access.")


# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False


@st.cache_resource
def get_db_connection():
    """Create and return database connection"""
    if not os.path.exists('medical_pharmacy.db'):
        st.error("Database not found! Please run data_generator.py first.")
        st.stop()
    return sqlite3.connect('medical_pharmacy.db', check_same_thread=False)


def load_data(query):
    """Load data from database"""
    conn = get_db_connection()
    df = pd.read_sql_query(query, conn)
    return df


def overview_tab():
    """Display overview metrics"""
    st.markdown("### 📊 Business Overview")

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_patients = load_data("SELECT COUNT(*) as count FROM patients")['count'][0]
        st.metric("Total Patients", f"{total_patients:,}")

    with col2:
        total_consultations = load_data("SELECT COUNT(*) as count FROM consultations")['count'][0]
        st.metric("Total Consultations", f"{total_consultations:,}")

    with col3:
        total_transactions = load_data("SELECT COUNT(*) as count FROM transactions")['count'][0]
        st.metric("Total Transactions", f"{total_transactions:,}")

    with col4:
        total_revenue = load_data("SELECT SUM(total_amount) as revenue FROM transactions")['revenue'][0]
        st.metric("Total Revenue", f"₹{total_revenue:,.2f}")

    st.markdown("---")

    # Time-based analysis
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📅 Monthly Consultation Trends")
        monthly_consults = load_data("""
            SELECT 
                strftime('%Y-%m', consultation_date) as month,
                COUNT(*) as consultations
            FROM consultations
            GROUP BY month
            ORDER BY month
        """)

        fig = px.line(monthly_consults, x='month', y='consultations',
                      title='Consultations Over Time',
                      labels={'month': 'Month', 'consultations': 'Number of Consultations'})
        fig.update_traces(line_color='#1f77b4', line_width=3)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 💰 Monthly Revenue Trends")
        monthly_revenue = load_data("""
            SELECT 
                strftime('%Y-%m', transaction_date) as month,
                SUM(total_amount) as revenue
            FROM transactions
            GROUP BY month
            ORDER BY month
        """)

        fig = px.bar(monthly_revenue, x='month', y='revenue',
                     title='Revenue Over Time',
                     labels={'month': 'Month', 'revenue': 'Revenue (₹)'})
        fig.update_traces(marker_color='#2ca02c')
        st.plotly_chart(fig, use_container_width=True)

    # Top ailments and medicines
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🏥 Top 10 Ailments")
        top_ailments = load_data("""
            SELECT ailment, COUNT(*) as count
            FROM consultations
            GROUP BY ailment
            ORDER BY count DESC
            LIMIT 10
        """)

        fig = px.bar(top_ailments, x='count', y='ailment', orientation='h',
                     title='Most Common Ailments',
                     labels={'count': 'Number of Cases', 'ailment': 'Ailment'})
        fig.update_traces(marker_color='#ff7f0e')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 💊 Top 10 Selling Medicines")
        top_medicines = load_data("""
            SELECT 
                m.name,
                SUM(ti.quantity) as total_quantity,
                SUM(ti.total_price) as total_sales
            FROM transaction_items ti
            JOIN medicines m ON ti.medicine_id = m.medicine_id
            GROUP BY m.name
            ORDER BY total_quantity DESC
            LIMIT 10
        """)

        fig = px.bar(top_medicines, x='total_quantity', y='name', orientation='h',
                     title='Best Selling Medicines',
                     labels={'total_quantity': 'Units Sold', 'name': 'Medicine'})
        fig.update_traces(marker_color='#d62728')
        st.plotly_chart(fig, use_container_width=True)


def pharmacy_analytics_tab():
    """Display pharmacy-specific analytics"""
    st.markdown("### 💊 Pharmacy Analytics")

    # Inventory status
    col1, col2, col3 = st.columns(3)

    with col1:
        total_medicines = load_data("SELECT COUNT(*) as count FROM medicines")['count'][0]
        st.metric("Total Medicines", f"{total_medicines:,}")

    with col2:
        low_stock = load_data("""
            SELECT COUNT(*) as count FROM medicines 
            WHERE stock_quantity < reorder_level
        """)['count'][0]
        st.metric("Low Stock Items", f"{low_stock:,}", delta="-Alert" if low_stock > 0 else "OK")

    with col3:
        total_stock_value = load_data("""
            SELECT SUM(stock_quantity * price) as value FROM medicines
        """)['value'][0]
        st.metric("Total Stock Value", f"₹{total_stock_value:,.2f}")

    st.markdown("---")

    # Stock analysis
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📦 Stock Status by Category")
        category_stock = load_data("""
            SELECT 
                category,
                COUNT(*) as medicine_count,
                SUM(stock_quantity) as total_stock
            FROM medicines
            GROUP BY category
            ORDER BY total_stock DESC
        """)

        fig = px.bar(category_stock, x='category', y='total_stock',
                     title='Stock Quantity by Category',
                     labels={'category': 'Category', 'total_stock': 'Total Stock'},
                     color='medicine_count')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### ⚠️ Low Stock Alerts")
        low_stock_items = load_data("""
            SELECT 
                name,
                category,
                stock_quantity,
                reorder_level,
                (reorder_level - stock_quantity) as shortage
            FROM medicines
            WHERE stock_quantity < reorder_level
            ORDER BY shortage DESC
        """)

        if len(low_stock_items) > 0:
            st.dataframe(low_stock_items, use_container_width=True, hide_index=True)
        else:
            st.success("✅ All medicines are adequately stocked!")

    # Payment modes and revenue
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 💳 Revenue by Payment Mode")
        payment_revenue = load_data("""
            SELECT 
                payment_mode,
                COUNT(*) as transactions,
                SUM(total_amount) as revenue
            FROM transactions
            GROUP BY payment_mode
            ORDER BY revenue DESC
        """)

        fig = px.pie(payment_revenue, values='revenue', names='payment_mode',
                     title='Revenue Distribution by Payment Mode',
                     hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 📊 Transaction Statistics")
        st.dataframe(payment_revenue, use_container_width=True, hide_index=True)

        avg_transaction = load_data("""
            SELECT AVG(total_amount) as avg_amount FROM transactions
        """)['avg_amount'][0]
        st.info(f"**Average Transaction Value:** ₹{avg_transaction:.2f}")

    # Medicine performance
    st.markdown("#### 🏆 Top Performing Medicines (Revenue)")
    top_revenue_meds = load_data("""
        SELECT 
            m.name,
            m.category,
            m.manufacturer,
            SUM(ti.quantity) as units_sold,
            SUM(ti.total_price) as revenue,
            m.price as unit_price
        FROM transaction_items ti
        JOIN medicines m ON ti.medicine_id = m.medicine_id
        GROUP BY m.medicine_id
        ORDER BY revenue DESC
        LIMIT 15
    """)

    st.dataframe(top_revenue_meds, use_container_width=True, hide_index=True)


def patient_analytics_tab():
    """Display patient-specific analytics"""
    st.markdown("### 👥 Patient Analytics")

    # Patient demographics
    col1, col2, col3 = st.columns(3)

    with col1:
        gender_dist = load_data("""
            SELECT gender, COUNT(*) as count
            FROM patients
            GROUP BY gender
        """)

        fig = px.pie(gender_dist, values='count', names='gender',
                     title='Patient Gender Distribution',
                     color_discrete_map={'Male': '#1f77b4', 'Female': '#ff7f0e'})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        age_dist = load_data("""
            SELECT 
                CASE 
                    WHEN age < 18 THEN 'Child (<18)'
                    WHEN age BETWEEN 18 AND 35 THEN 'Young Adult (18-35)'
                    WHEN age BETWEEN 36 AND 50 THEN 'Adult (36-50)'
                    WHEN age BETWEEN 51 AND 65 THEN 'Senior (51-65)'
                    ELSE 'Elderly (65+)'
                END as age_group,
                COUNT(*) as count
            FROM patients
            GROUP BY age_group
        """)

        fig = px.bar(age_dist, x='age_group', y='count',
                     title='Patient Age Distribution',
                     labels={'age_group': 'Age Group', 'count': 'Number of Patients'})
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        city_dist = load_data("""
            SELECT city, COUNT(*) as count
            FROM patients
            GROUP BY city
            ORDER BY count DESC
            LIMIT 10
        """)

        fig = px.bar(city_dist, x='city', y='count',
                     title='Patients by City (Top 10)',
                     labels={'city': 'City', 'count': 'Number of Patients'})
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Consultation patterns
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📅 Patient Visit Frequency")
        visit_freq = load_data("""
            SELECT 
                CASE 
                    WHEN visit_count = 1 THEN '1 visit'
                    WHEN visit_count = 2 THEN '2 visits'
                    WHEN visit_count = 3 THEN '3 visits'
                    WHEN visit_count >= 4 THEN '4+ visits'
                END as frequency,
                COUNT(*) as patient_count
            FROM (
                SELECT patient_id, COUNT(*) as visit_count
                FROM consultations
                GROUP BY patient_id
            )
            GROUP BY frequency
        """)

        fig = px.bar(visit_freq, x='frequency', y='patient_count',
                     title='Patient Visit Frequency',
                     labels={'frequency': 'Number of Visits', 'patient_count': 'Number of Patients'})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 💰 Consultation Fee Revenue")
        fee_revenue = load_data("""
            SELECT 
                strftime('%Y-%m', consultation_date) as month,
                SUM(consultation_fee) as revenue
            FROM consultations
            GROUP BY month
            ORDER BY month
        """)

        fig = px.area(fee_revenue, x='month', y='revenue',
                      title='Consultation Fee Revenue Over Time',
                      labels={'month': 'Month', 'revenue': 'Revenue (₹)'})
        fig.update_traces(fillcolor='rgba(31, 119, 180, 0.3)', line_color='#1f77b4')
        st.plotly_chart(fig, use_container_width=True)

    # Top patients
    st.markdown("#### 🌟 Top Patients by Spending")
    top_patients = load_data("""
        SELECT 
            p.patient_id,
            p.first_name || ' ' || p.last_name as patient_name,
            p.age,
            p.gender,
            p.city,
            COUNT(DISTINCT c.consultation_id) as consultations,
            SUM(c.consultation_fee) as consultation_fees,
            COALESCE(SUM(t.total_amount), 0) as medicine_purchases,
            (SUM(c.consultation_fee) + COALESCE(SUM(t.total_amount), 0)) as total_spent
        FROM patients p
        LEFT JOIN consultations c ON p.patient_id = c.patient_id
        LEFT JOIN transactions t ON c.consultation_id = t.consultation_id
        GROUP BY p.patient_id
        ORDER BY total_spent DESC
        LIMIT 20
    """)

    st.dataframe(top_patients, use_container_width=True, hide_index=True)


def correlation_analysis_tab():
    """Analyze correlation between consultations and pharmacy purchases"""
    st.markdown("### 🔗 Consultation-Purchase Correlation Analysis")

    # Key metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        total_consults = load_data("SELECT COUNT(*) as count FROM consultations")['count'][0]
        st.metric("Total Consultations", f"{total_consults:,}")

    with col2:
        linked_purchases = load_data("""
            SELECT COUNT(*) as count FROM transactions 
            WHERE prescription_linked = 1
        """)['count'][0]
        conversion_rate = (linked_purchases / total_consults * 100) if total_consults > 0 else 0
        st.metric("Linked Purchases", f"{linked_purchases:,}",
                  delta=f"{conversion_rate:.1f}% conversion")

    with col3:
        unlinked = total_consults - linked_purchases
        st.metric("Lost Opportunities", f"{unlinked:,}",
                  delta=f"-{(unlinked / total_consults * 100):.1f}%", delta_color="inverse")

    st.markdown("---")

    # Conversion funnel
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📊 Purchase Conversion Funnel")

        funnel_data = pd.DataFrame({
            'Stage': ['Consultations', 'Purchased Medicines', 'Walk-in Only'],
            'Count': [
                total_consults,
                linked_purchases,
                load_data("SELECT COUNT(*) as count FROM transactions WHERE prescription_linked = 0")['count'][0]
            ]
        })

        fig = go.Figure(go.Funnel(
            y=funnel_data['Stage'],
            x=funnel_data['Count'],
            textinfo="value+percent previous"
        ))
        fig.update_layout(title='Consultation to Purchase Funnel')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 🎯 Conversion Rate by Ailment")
        conversion_by_ailment = load_data("""
            SELECT 
                c.ailment,
                COUNT(DISTINCT c.consultation_id) as consultations,
                COUNT(DISTINCT t.transaction_id) as purchases,
                ROUND(CAST(COUNT(DISTINCT t.transaction_id) AS FLOAT) / 
                      COUNT(DISTINCT c.consultation_id) * 100, 2) as conversion_rate
            FROM consultations c
            LEFT JOIN transactions t ON c.consultation_id = t.consultation_id 
                                     AND t.prescription_linked = 1
            GROUP BY c.ailment
            HAVING consultations >= 5
            ORDER BY conversion_rate DESC
            LIMIT 10
        """)

        fig = px.bar(conversion_by_ailment, x='conversion_rate', y='ailment',
                     orientation='h',
                     title='Top 10 Ailments by Conversion Rate',
                     labels={'conversion_rate': 'Conversion Rate (%)', 'ailment': 'Ailment'},
                     color='conversion_rate',
                     color_continuous_scale='RdYlGn')
        st.plotly_chart(fig, use_container_width=True)

    # Time-based correlation
    st.markdown("#### ⏱️ Time Gap Between Consultation and Purchase")

    time_gap_data = load_data("""
        SELECT 
            julianday(t.transaction_date) - julianday(c.consultation_date) as days_gap,
            COUNT(*) as count
        FROM transactions t
        JOIN consultations c ON t.consultation_id = c.consultation_id
        WHERE t.prescription_linked = 1
        GROUP BY CAST(days_gap AS INTEGER)
        HAVING CAST(days_gap AS INTEGER) >= 0 AND CAST(days_gap AS INTEGER) <= 7
        ORDER BY days_gap
    """)

    if len(time_gap_data) > 0:
        fig = px.bar(time_gap_data, x='days_gap', y='count',
                     title='Distribution of Time Gap (Days)',
                     labels={'days_gap': 'Days After Consultation', 'count': 'Number of Purchases'})
        st.plotly_chart(fig, use_container_width=True)

    # Detailed discrepancy analysis
    st.markdown("#### 🔍 Consultations Without Purchases (Lost Opportunities)")

    lost_opportunities = load_data("""
        SELECT 
            c.consultation_id,
            p.first_name || ' ' || p.last_name as patient_name,
            c.consultation_date,
            c.ailment,
            c.consultation_fee,
            GROUP_CONCAT(m.name, ', ') as prescribed_medicines,
            CASE 
                WHEN t.transaction_id IS NULL THEN 'No Purchase'
                ELSE 'Purchased'
            END as status
        FROM consultations c
        JOIN patients p ON c.patient_id = p.patient_id
        LEFT JOIN prescriptions pr ON c.consultation_id = pr.consultation_id
        LEFT JOIN medicines m ON pr.medicine_id = m.medicine_id
        LEFT JOIN transactions t ON c.consultation_id = t.consultation_id
        WHERE t.transaction_id IS NULL
        GROUP BY c.consultation_id
        ORDER BY c.consultation_date DESC
        LIMIT 50
    """)

    st.dataframe(lost_opportunities, use_container_width=True, hide_index=True)

    # Revenue impact
    col1, col2 = st.columns(2)

    with col1:
        actual_revenue = load_data("""
            SELECT SUM(total_amount) as revenue 
            FROM transactions 
            WHERE prescription_linked = 1
        """)['revenue'][0] or 0

        st.metric("Actual Medicine Revenue (Linked)", f"₹{actual_revenue:,.2f}")

    with col2:
        potential_revenue = load_data("""
            SELECT SUM(m.price * pr.quantity) as potential
            FROM prescriptions pr
            JOIN medicines m ON pr.medicine_id = m.medicine_id
            JOIN consultations c ON pr.consultation_id = c.consultation_id
            LEFT JOIN transactions t ON c.consultation_id = t.consultation_id
            WHERE t.transaction_id IS NULL
        """)['potential'][0] or 0

        st.metric("Potential Lost Revenue", f"₹{potential_revenue:,.2f}",
                  delta=f"-{(potential_revenue / (actual_revenue + potential_revenue) * 100):.1f}% opportunity",
                  delta_color="inverse")


def ai_query_tab():
    """AI-powered natural language query interface"""
    st.markdown("### 🤖 AI-Powered Analytics (Premium)")

    st.info("""
    **Welcome to AI-Powered Analytics!**

    Ask questions in plain English and get actionable business insights from your data.

    **Example questions for actionable insights:**
    - "Which patients haven't visited in the last 3 months?"
    - "What medicines are running low on stock?"
    - "Show me consultations that didn't result in purchases"
    - "Which chronic patients have high spending potential?"
    - "What are the top revenue-generating medicines this month?"
    - "Which cities have the most patients but lowest revenue?"
    """)

    # API Key input
    api_key = st.text_input("Enter OpenAI API Key:", type="password",
                            help="Your API key is not stored and only used for this session")

    if not api_key:
        st.warning("⚠️ Please enter your OpenAI API key to use AI features")
        return

    # Query input
    user_query = st.text_area("Enter your question in natural language:",
                              height=100,
                              placeholder="E.g., Show me all patients from Mumbai who visited more than 3 times")

    col1, col2 = st.columns([1, 5])
    with col1:
        execute_button = st.button("🚀 Execute Query", type="primary")
    with col2:
        show_sql = st.checkbox("Show underlying SQL query", value=True)

    if execute_button and user_query:
        with st.spinner("🤖 AI is analyzing your question..."):
            try:
                # Import OpenAI (supports both old and new versions)
                try:
                    from openai import OpenAI
                    client = OpenAI(api_key=api_key)
                    use_new_api = True
                except ImportError:
                    import openai
                    openai.api_key = api_key
                    use_new_api = False

                # Get database schema
                schema = load_data("""
                    SELECT sql FROM sqlite_master WHERE type='table'
                """)

                schema_text = "\n".join(schema['sql'].tolist())

                # Create prompt for GPT
                prompt = f"""You are a SQL expert. Given the following SQLite database schema and a user question,
generate a valid SQLite query to answer the question.

Database Schema:
{schema_text}

Important notes:
- Use proper SQLite syntax
- Return ONLY the SQL query, no explanations
- Use JOINs appropriately
- Format dates using strftime when needed
- Use || for string concatenation

User Question: {user_query}

SQL Query:"""

                # Call OpenAI API (compatible with both versions)
                if use_new_api:
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a SQL expert that generates SQLite queries."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0,
                        max_tokens=500
                    )
                    sql_query = response.choices[0].message.content.strip()
                else:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a SQL expert that generates SQLite queries."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0,
                        max_tokens=500
                    )
                    sql_query = response.choices[0].message.content.strip()

                # Clean up the query
                sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

                if show_sql:
                    st.markdown("#### 📝 Generated SQL Query:")
                    st.code(sql_query, language="sql")

                # Execute the query
                try:
                    result_df = load_data(sql_query)

                    st.markdown("#### 📊 Query Results:")
                    st.dataframe(result_df, use_container_width=True, hide_index=True)

                    # Generate actionable business insights
                    # Get top 3 rows as sample for context
                    sample_data = result_df.head(3).to_string(index=False) if len(result_df) > 0 else "No data"

                    explain_prompt = f"""You are a healthcare business analyst providing actionable insights to a doctor/admin.

Based on this query result, provide specific, actionable recommendations and key findings.

Question asked: {user_query}
Number of results: {len(result_df)}
Sample data:
{sample_data}

Provide 2-3 actionable insights focusing on:
- What actions should be taken
- What opportunities exist
- What problems need attention
- Specific numbers/metrics that matter

Be direct and actionable. Avoid describing the query itself. Think like a business consultant."""

                    if use_new_api:
                        explanation = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content": "You are a data analyst providing insights."},
                                {"role": "user", "content": explain_prompt}
                            ],
                            temperature=0.7,
                            max_tokens=200
                        )
                        insight_text = explanation.choices[0].message.content.strip()
                    else:
                        explanation = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content": "You are a data analyst providing insights."},
                                {"role": "user", "content": explain_prompt}
                            ],
                            temperature=0.7,
                            max_tokens=200
                        )
                        insight_text = explanation.choices[0].message.content.strip()

                    st.markdown("#### 💡 AI Insights:")
                    st.success(insight_text)

                    # Download option
                    csv = result_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Results as CSV",
                        data=csv,
                        file_name=f"query_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )

                except Exception as e:
                    st.error(f"❌ Error executing query: {str(e)}")
                    st.info("The AI-generated query might have syntax issues. Try rephrasing your question.")

            except Exception as e:
                st.error(f"❌ Error with AI service: {str(e)}")
                st.info("Please check your API key and try again.")


def main():
    """Main application"""

    # Check if user is logged in
    if not st.session_state.get('logged_in', False):
        show_login_page()
        return

    # Header with logout button
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown('<div class="main-header">🤖 MediSmart AI - Healthcare Analytics Platform</div>',
                    unsafe_allow_html=True)
    with col2:
        st.write("")  # Spacing
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state['logged_in'] = False
            st.session_state.clear()
            st.rerun()

    # Sidebar with user info
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2913/2913133.png", width=100)
        st.markdown("### 🤖 MediSmart AI")
        st.markdown("*Intelligent Healthcare Analytics*")
        st.markdown("---")

        # User info
        st.markdown(f"**👤 User:** {st.session_state.get('name', 'User')}")
        role = st.session_state.get('role', 'viewer')
        role_display = "🔑 Admin (Full Access)" if role == "admin" else "👁️ Viewer (Limited)"
        st.markdown(f"**🎭 Role:** {role_display}")

        st.markdown("---")
        st.markdown("**🎯 Platform:** AI-Powered Insights")
        st.markdown("**📊 Analytics:** Real-time")
        st.markdown("**🔒 Data:** Synthetic Demo")

        st.markdown("---")
        st.markdown("### 📊 Quick Stats")

        try:
            total_patients = load_data("SELECT COUNT(*) as count FROM patients")['count'][0]
            today_consultations = load_data("""
                SELECT COUNT(*) as count FROM consultations 
                WHERE DATE(consultation_date) = DATE('now')
            """)['count'][0]

            st.metric("Total Patients", total_patients)
            st.metric("Today's Consultations", today_consultations)

        except Exception as e:
            st.warning("Database connection issue")

        st.markdown("---")
        st.markdown("**Version:** 2.1")
        st.markdown(f"**Status:** 🟢 Online")

    # Main tabs - check role for Premium tab
    user_role = st.session_state.get('role', 'viewer')

    if user_role == "admin":
        # Full access for admin
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Overview",
            "💊 Pharmacy Analytics",
            "👥 Patient Analytics",
            "🔗 Correlation Analysis",
            "🤖 AI Query (Premium)"
        ])
    else:
        # Limited access for viewer - no AI Query tab shown initially
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Overview",
            "💊 Pharmacy Analytics",
            "👥 Patient Analytics",
            "🔗 Correlation Analysis",
            "🔒 Premium (Locked)"
        ])

    with tab1:
        overview_tab()

    with tab2:
        pharmacy_analytics_tab()

    with tab3:
        patient_analytics_tab()

    with tab4:
        correlation_analysis_tab()

    with tab5:
        if user_role == "admin":
            ai_query_tab()
        else:
            # Show locked premium page for non-admin users
            show_premium_locked()

    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666; padding: 1rem;'>
            <p>Built with ❤️ using Streamlit | © 2024 MediSmart AI | 
            Logged in as: <strong>{}</strong></p>
        </div>
    """.format(st.session_state.get('name', 'User')), unsafe_allow_html=True)


if __name__ == "__main__":
    main()