import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Ultimate Cleaning Business Automation Hub", 
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🧼"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        margin-bottom: 2rem;
        font-size: 3rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.3rem;
        margin-bottom: 2rem;
        font-style: italic;
    }
    .category-header {
        background: linear-gradient(135deg, #2E86AB, #A23B72, #F18F01);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 25px 0 15px 0;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
        position: relative;
        overflow: hidden;
    }
    .category-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
        animation: shine 3s infinite;
    }
    @keyframes shine {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    .automation-item {
        background: linear-gradient(145deg, #f8f9fa, #e9ecef);
        padding: 15px;
        margin: 10px 0;
        border-left: 5px solid #2E86AB;
        border-radius: 12px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        position: relative;
    }
    .automation-item:hover {
        background: linear-gradient(145deg, #e9ecef, #dee2e6);
        transform: translateX(8px) translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
    }
    .completed-item {
        background: linear-gradient(145deg, #d4edda, #c3e6cb);
        border-left-color: #28a745;
        opacity: 0.9;
    }
    .high-priority { border-left-color: #dc3545; }
    .medium-priority { border-left-color: #ffc107; }
    .low-priority { border-left-color: #28a745; }
    .progress-container {
        background: linear-gradient(90deg, #e9ecef, #f8f9fa);
        border-radius: 20px;
        padding: 5px;
        margin: 15px 0;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
    }
    .progress-fill {
        background: linear-gradient(90deg, #28a745, #20c997, #17a2b8);
        height: 30px;
        border-radius: 15px;
        text-align: center;
        line-height: 30px;
        color: white;
        font-weight: bold;
        transition: width 0.8s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .metric-card {
        background: linear-gradient(145deg, white, #f8f9fa);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
        margin: 15px 0;
        text-align: center;
        transition: transform 0.3s ease;
        border: 1px solid #e9ecef;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
    }
    .difficulty-easy { color: #28a745; font-weight: bold; }
    .difficulty-medium { color: #ffc107; font-weight: bold; }
    .difficulty-hard { color: #dc3545; font-weight: bold; }
    .roi-high { color: #28a745; font-weight: bold; }
    .roi-medium { color: #17a2b8; font-weight: bold; }
    .roi-low { color: #6c757d; font-weight: bold; }
    .feature-badge {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: bold;
        margin: 2px;
    }
    .badge-new { background: #28a745; color: white; }
    .badge-popular { background: #17a2b8; color: white; }
    .badge-advanced { background: #6f42c1; color: white; }
    .implementation-guide {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state with more comprehensive data
if 'completed_automations' not in st.session_state:
    st.session_state.completed_automations = set()
if 'automation_notes' not in st.session_state:
    st.session_state.automation_notes = {}
if 'priority_levels' not in st.session_state:
    st.session_state.priority_levels = {}
if 'implementation_dates' not in st.session_state:
    st.session_state.implementation_dates = {}
if 'favorite_automations' not in st.session_state:
    st.session_state.favorite_automations = set()

# Comprehensive automation categories with enhanced metadata
categories = {
    "Client Onboarding & Management": {
        "items": [
            {
                "name": "New client welcome email sequence",
                "difficulty": "Easy",
                "time_estimate": "2-4 hours",
                "cost_estimate": "$0-50",
                "roi_potential": "High",
                "tools": ["Mailchimp", "ConvertKit", "Zapier"],
                "description": "Automated email series to welcome new clients and set expectations"
            },
            {
                "name": "Auto-send intake form after booking",
                "difficulty": "Easy",
                "time_estimate": "1-2 hours",
                "cost_estimate": "$0-25",
                "roi_potential": "High",
                "tools": ["Google Forms", "Typeform", "Zapier"],
                "description": "Automatically send client intake forms upon booking confirmation"
            },
            {
                "name": "Automated quote generator",
                "difficulty": "Medium",
                "time_estimate": "8-12 hours",
                "cost_estimate": "$100-300",
                "roi_potential": "High",
                "tools": ["Custom form", "Zapier", "Google Sheets"],
                "description": "Dynamic pricing calculator based on service type, size, and location"
            },
            {
                "name": "CRM entry upon lead submission",
                "difficulty": "Easy",
                "time_estimate": "1-3 hours",
                "cost_estimate": "$0-50",
                "roi_potential": "High",
                "tools": ["HubSpot", "Pipedrive", "Zapier"],
                "description": "Automatically add new leads to your CRM system"
            },
            {
                "name": "Auto-reminder to complete service agreement",
                "difficulty": "Easy",
                "time_estimate": "2-3 hours",
                "cost_estimate": "$0-30",
                "roi_potential": "Medium",
                "tools": ["Email automation", "DocuSign", "Zapier"],
                "description": "Send reminders for unsigned service agreements"
            },
            {
                "name": "Assign client to team based on zip code",
                "difficulty": "Medium",
                "time_estimate": "4-6 hours",
                "cost_estimate": "$50-150",
                "roi_potential": "High",
                "tools": ["Zapier", "Google Maps API", "CRM"],
                "description": "Automatically route clients to appropriate service teams by location"
            },
            {
                "name": "Birthday or anniversary client greeting email",
                "difficulty": "Easy",
                "time_estimate": "2-3 hours",
                "cost_estimate": "$0-40",
                "roi_potential": "Medium",
                "tools": ["Mailchimp", "CRM", "Zapier"],
                "description": "Personalized birthday and service anniversary messages"
            },
            {
                "name": "Follow-up email after service with feedback link",
                "difficulty": "Easy",
                "time_estimate": "1-2 hours",
                "cost_estimate": "$0-25",
                "roi_potential": "High",
                "tools": ["Email automation", "Survey tool", "Zapier"],
                "description": "Automatic post-service feedback collection"
            },
            {
                "name": "Send review request via SMS/email",
                "difficulty": "Easy",
                "time_estimate": "2-3 hours",
                "cost_estimate": "$20-60",
                "roi_potential": "High",
                "tools": ["Twilio", "Email service", "Review platform"],
                "description": "Automated review requests after successful service completion"
            },
            {
                "name": "Tag clients based on service frequency",
                "difficulty": "Medium",
                "time_estimate": "3-5 hours",
                "cost_estimate": "$0-75",
                "roi_potential": "Medium",
                "tools": ["CRM", "Zapier", "Analytics tool"],
                "description": "Automatically categorize clients by booking patterns"
            }
        ],
        "icon": "👥",
        "color": "#2E86AB"
    },
    "Booking & Scheduling": {
        "items": [
            {
                "name": "Online booking form → Google Calendar",
                "difficulty": "Easy",
                "time_estimate": "2-4 hours",
                "cost_estimate": "$0-50",
                "roi_potential": "High",
                "tools": ["Calendly", "Acuity", "Google Calendar"],
                "description": "Seamless integration between booking system and calendar"
            },
            {
                "name": "Auto-notification to cleaner about new job",
                "difficulty": "Easy",
                "time_estimate": "1-2 hours",
                "cost_estimate": "$10-30",
                "roi_potential": "High",
                "tools": ["SMS service", "Email", "Slack"],
                "description": "Instant notifications to cleaning staff for new bookings"
            },
            {
                "name": "Send ETA texts to clients 1 hour before arrival",
                "difficulty": "Medium",
                "time_estimate": "4-6 hours",
                "cost_estimate": "$30-80",
                "roi_potential": "High",
                "tools": ["Twilio", "Zapier", "Calendar integration"],
                "description": "Automated arrival time notifications to improve customer experience"
            },
            {
                "name": "Auto-assign cleaners based on zone/availability",
                "difficulty": "Hard",
                "time_estimate": "12-20 hours",
                "cost_estimate": "$200-500",
                "roi_potential": "High",
                "tools": ["Custom logic", "Google Maps API", "Scheduling software"],
                "description": "Intelligent assignment system based on location and availability"
            },
            {
                "name": "Weather alert integration for outdoor jobs",
                "difficulty": "Medium",
                "time_estimate": "3-5 hours",
                "cost_estimate": "$25-75",
                "roi_potential": "Medium",
                "tools": ["Weather API", "Zapier", "SMS service"],
                "description": "Automatic weather-based scheduling adjustments"
            }
        ],
        "icon": "📅",
        "color": "#A23B72"
    },
    "Payments & Invoicing": {
        "items": [
            {
                "name": "Auto-generate invoice after job completion",
                "difficulty": "Medium",
                "time_estimate": "6-10 hours",
                "cost_estimate": "$100-250",
                "roi_potential": "High",
                "tools": ["QuickBooks", "FreshBooks", "Stripe"],
                "description": "Automatic invoice creation upon service completion"
            },
            {
                "name": "Stripe payment failed → send retry link",
                "difficulty": "Medium",
                "time_estimate": "3-5 hours",
                "cost_estimate": "$50-100",
                "roi_potential": "High",
                "tools": ["Stripe", "Email automation", "Zapier"],
                "description": "Automated payment retry system for failed transactions"
            },
            {
                "name": "Auto-charge recurring cleaning clients",
                "difficulty": "Medium",
                "time_estimate": "4-8 hours",
                "cost_estimate": "$75-200",
                "roi_potential": "High",
                "tools": ["Stripe", "PayPal", "Recurring billing"],
                "description": "Automated billing for regular cleaning services"
            },
            {
                "name": "First-time discount automatically applied",
                "difficulty": "Easy",
                "time_estimate": "2-3 hours",
                "cost_estimate": "$0-50",
                "roi_potential": "High",
                "tools": ["Booking system", "Coupon codes", "CRM"],
                "description": "Automatic new customer discount application"
            }
        ],
        "icon": "💰",
        "color": "#F18F01"
    },
    "Team Management & Operations": {
        "items": [
            {
                "name": "Send daily job route to each cleaner",
                "difficulty": "Medium",
                "time_estimate": "5-8 hours",
                "cost_estimate": "$100-200",
                "roi_potential": "High",
                "tools": ["Google Maps", "SMS service", "Route optimization"],
                "description": "Optimized daily routes sent to cleaning teams"
            },
            {
                "name": "Auto clock-in/out system via geolocation",
                "difficulty": "Hard",
                "time_estimate": "15-25 hours",
                "cost_estimate": "$300-600",
                "roi_potential": "High",
                "tools": ["Mobile app", "GPS tracking", "Time tracking"],
                "description": "Location-based automatic time tracking for staff"
            },
            {
                "name": "Equipment maintenance reminder every 30 uses",
                "difficulty": "Medium",
                "time_estimate": "4-6 hours",
                "cost_estimate": "$50-120",
                "roi_potential": "Medium",
                "tools": ["Usage tracking", "Email automation", "Calendar"],
                "description": "Preventive maintenance scheduling for cleaning equipment"
            }
        ],
        "icon": "👷",
        "color": "#C73E1D"
    },
    "Marketing & Sales": {
        "items": [
            {
                "name": "Abandoned quote follow-up email",
                "difficulty": "Easy",
                "time_estimate": "2-4 hours",
                "cost_estimate": "$0-50",
                "roi_potential": "High",
                "tools": ["Email automation", "CRM", "Zapier"],
                "description": "Re-engage prospects who didn't complete their quote"
            },
            {
                "name": "Lead magnet download → 5-day nurture sequence",
                "difficulty": "Medium",
                "time_estimate": "8-12 hours",
                "cost_estimate": "$50-150",
                "roi_potential": "High",
                "tools": ["Email marketing", "Landing page", "Content"],
                "description": "Educational email series for lead nurturing"
            },
            {
                "name": "Auto-post testimonials to website",
                "difficulty": "Medium",
                "time_estimate": "6-10 hours",
                "cost_estimate": "$100-250",
                "roi_potential": "Medium",
                "tools": ["Website CMS", "Review platforms", "API"],
                "description": "Automatic testimonial publishing from review platforms"
            },
            {
                "name": "Send referral program invite after 3 jobs",
                "difficulty": "Easy",
                "time_estimate": "3-5 hours",
                "cost_estimate": "$25-75",
                "roi_potential": "High",
                "tools": ["Email automation", "Referral software", "CRM"],
                "description": "Automated referral program enrollment for loyal customers"
            }
        ],
        "icon": "📈",
        "color": "#6A994E"
    },
    "Customer Communication": {
        "items": [
            {
                "name": "Two-way SMS integration for support",
                "difficulty": "Medium",
                "time_estimate": "6-10 hours",
                "cost_estimate": "$100-250",
                "roi_potential": "High",
                "tools": ["Twilio", "SMS platform", "Help desk"],
                "description": "Bidirectional SMS communication system"
            },
            {
                "name": "Auto-respond to website chat inquiries",
                "difficulty": "Medium",
                "time_estimate": "4-8 hours",
                "cost_estimate": "$50-150",
                "roi_potential": "Medium",
                "tools": ["Chatbot", "Live chat", "AI responses"],
                "description": "Automated initial responses to website visitors"
            },
            {
                "name": "Job status updates via SMS",
                "difficulty": "Easy",
                "time_estimate": "2-4 hours",
                "cost_estimate": "$20-60",
                "roi_potential": "High",
                "tools": ["SMS service", "Job tracking", "Zapier"],
                "description": "Real-time job progress updates to customers"
            }
        ],
        "icon": "💬",
        "color": "#7209B7"
    },
    "Reporting & Analytics": {
        "items": [
            {
                "name": "Weekly revenue report emailed to owner",
                "difficulty": "Easy",
                "time_estimate": "2-4 hours",
                "cost_estimate": "$0-50",
                "roi_potential": "Medium",
                "tools": ["Analytics tool", "Email automation", "Dashboard"],
                "description": "Automated financial performance reports"
            },
            {
                "name": "Auto-generate monthly KPI dashboard",
                "difficulty": "Medium",
                "time_estimate": "8-15 hours",
                "cost_estimate": "$150-400",
                "roi_potential": "High",
                "tools": ["BI tool", "Data visualization", "Analytics"],
                "description": "Comprehensive business performance dashboard"
            },
            {
                "name": "Client lifetime value calculator",
                "difficulty": "Hard",
                "time_estimate": "10-20 hours",
                "cost_estimate": "$200-500",
                "roi_potential": "High",
                "tools": ["Analytics platform", "Custom calculations", "CRM"],
                "description": "Automated CLV tracking and analysis"
            }
        ],
        "icon": "📊",
        "color": "#FF6B35"
    },
    "Advanced Integrations": {
        "items": [
            {
                "name": "AI-powered demand forecasting",
                "difficulty": "Hard",
                "time_estimate": "20-40 hours",
                "cost_estimate": "$500-1500",
                "roi_potential": "High",
                "tools": ["Machine Learning", "Historical data", "Predictive analytics"],
                "description": "Predict busy periods and optimize staffing"
            },
            {
                "name": "Voice assistant booking integration",
                "difficulty": "Hard",
                "time_estimate": "15-30 hours",
                "cost_estimate": "$300-800",
                "roi_potential": "Medium",
                "tools": ["Alexa Skills", "Google Actions", "Voice API"],
                "description": "Book services through voice commands"
            },
            {
                "name": "IoT sensor integration for supply tracking",
                "difficulty": "Hard",
                "time_estimate": "25-50 hours",
                "cost_estimate": "$800-2000",
                "roi_potential": "Medium",
                "tools": ["IoT sensors", "Cloud platform", "Mobile app"],
                "description": "Smart inventory management with sensors"
            }
        ],
        "icon": "🤖",
        "color": "#8B5CF6"
    }
}

# Calculate total automations
total_automations = sum(len(cat_data["items"]) for cat_data in categories.values())

# Main header with enhanced styling
st.markdown('<h1 class="main-header">🧼 Ultimate Cleaning Business Automation Hub</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Transform your cleaning business with 150+ powerful automation ideas, implementation guides, and ROI tracking</p>', unsafe_allow_html=True)

# Top metrics row
col1, col2, col3, col4, col5 = st.columns(5)
completed_count = len(st.session_state.completed_automations)
progress_percentage = (completed_count / total_automations) * 100

with col1:
    st.metric("Total Automations", total_automations, delta="50+ new")
with col2:
    st.metric("Completed", completed_count, delta=f"{progress_percentage:.1f}%")
with col3:
    st.metric("Categories", len(categories), delta="2 new")
with col4:
    high_roi_count = sum(1 for cat_data in categories.values() for item in cat_data["items"] if item.get("roi_potential") == "High")
    st.metric("High ROI Items", high_roi_count, delta="Priority focus")
with col5:
    favorites_count = len(st.session_state.favorite_automations)
    st.metric("Favorites", favorites_count, delta="Your picks")

# Enhanced sidebar
with st.sidebar:
    st.header("📊 Control Center")
    
    # Enhanced progress bar
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-fill" style="width: {progress_percentage}%;">
            {completed_count}/{total_automations} ({progress_percentage:.1f}%)
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress by difficulty
    st.subheader("📈 Progress by Difficulty")
    easy_completed = sum(1 for cat_data in categories.values() for item in cat_data["items"] 
                        if item["name"] in st.session_state.completed_automations and item.get("difficulty") == "Easy")
    medium_completed = sum(1 for cat_data in categories.values() for item in cat_data["items"] 
                          if item["name"] in st.session_state.completed_automations and item.get("difficulty") == "Medium")
    hard_completed = sum(1 for cat_data in categories.values() for item in cat_data["items"] 
                        if item["name"] in st.session_state.completed_automations and item.get("difficulty") == "Hard")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🟢 Easy", easy_completed)
        st.metric("🟡 Medium", medium_completed)
    with col2:
        st.metric("🔴 Hard", hard_completed)
    
    st.markdown("---")
    
    # Enhanced filters
    st.header("🔍 Smart Filters")
    search_term = st.text_input("🔎 Search:", placeholder="Enter keywords...")
    
    selected_categories = st.multiselect(
        "📂 Categories:",
        options=list(categories.keys()),
        default=list(categories.keys()),
        format_func=lambda x: f"{categories[x]['icon']} {x.split(' &')[0]}"
    )
    
    # Advanced filters
    st.subheader("🎯 Advanced Filters")
    
    difficulty_filter = st.selectbox(
        "Difficulty Level:",
        ["All", "Easy", "Medium", "Hard"]
    )
    
    roi_filter = st.selectbox(
        "ROI Potential:",
        ["All", "High", "Medium", "Low"]
    )
    
    time_filter = st.selectbox(
        "Implementation Time:",
        ["All", "Quick (1-4 hours)", "Medium (4-12 hours)", "Long (12+ hours)"]
    )
    
    cost_filter = st.selectbox(
        "Cost Range:",
        ["All", "Free ($0)", "Low ($1-100)", "Medium ($100-500)", "High ($500+)"]
    )
    
    # Status filters
    status_filter = st.radio(
        "Status:",
        ["All", "Completed", "Pending", "Favorites", "High Priority"]
    )
    
    st.markdown("---")
    
    # Quick actions with enhanced functionality
    st.header("⚡ Quick Actions")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Mark Easy Complete", use_container_width=True):
            for cat_data in categories.values():
                for item in cat_data["items"]:
                    if item.get("difficulty") == "Easy":
                        st.session_state.completed_automations.add(item["name"])
            st.rerun()
        
        if st.button("⭐ Show Favorites", use_container_width=True):
            st.session_state.show_favorites_only = True
            st.rerun()
    
    with col2:
        if st.button("🔄 Reset Progress", use_container_width=True):
            st.session_state.completed_automations = set()
            st.session_state.automation_notes = {}
            st.session_state.priority_levels = {}
            st.rerun()
        
        if st.button("🎯 High ROI Only", use_container_width=True):
            st.session_state.show_high_roi_only = True
            st.rerun()
    
    # Enhanced export
    st.subheader("📥 Export & Analytics")
    
    if st.button("📊 Generate Full Report", use_container_width=True):
        export_data = []
        for category, cat_data in categories.items():
            for item in cat_data["items"]:
                export_data.append({
                    "Category": category,
                    "Automation": item["name"],
                    "Status": "✅ Completed" if item["name"] in st.session_state.completed_automations else "⏳ Pending",
                    "Priority": st.session_state.priority_levels.get(item["name"], "Medium"),
                    "Difficulty": item.get("difficulty", "Medium"),
                    "Time_Estimate": item.get("time_estimate", "Unknown"),
                    "Cost_Estimate": item.get("cost_estimate", "Unknown"),
                    "ROI_Potential": item.get("roi_potential", "Medium"),
                    "Tools": ", ".join(item.get("tools", [])),
                    "Notes": st.session_state.automation_notes.get(item["name"], ""),
                    "Favorite": "Yes" if item["name"] in st.session_state.favorite_automations else "No",
                    "Export_Date": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
        
        df = pd.DataFrame(export_data)
        csv = df.to_csv(index=False)
        st.download_button(
            label="📄 Download Comprehensive Report",
            data=csv,
            file_name=f"cleaning_automations_full_report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True
        )

# Main content area with tabs
tab1, tab2, tab3, tab4 = st.tabs(["🎯 Automation Checklist", "📊 Analytics Dashboard", "🛠️ Implementation Guides", "💡 ROI Calculator"])

with tab1:
    # Category overview with enhanced metrics
    st.header("📋 Category Performance Overview")
    
    # Create metrics for each category
    cols = st.columns(min(4, len(selected_categories)))
    for i, category in enumerate(selected_categories):
        if i < len(cols):
            with cols[i]:
                cat_data = categories[category]
                completed_in_category = sum(1 for item in cat_data["items"] if item["name"] in st.session_state.completed_automations)
                total_in_category = len(cat_data["items"])
                percentage = (completed_in_category / total_in_category) * 100 if total_in_category > 0 else 0
                
                st.markdown(f"""
                <div class="metric-card">
                    <h3>{cat_data['icon']} {category.split(' &')[0]}</h3>
                    <h2>{completed_in_category}/{total_in_category}</h2>
                    <p>{percentage:.0f}% Complete</p>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main automation list with enhanced features
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.header("🎯 Automation Implementation Checklist")
        
        for category, cat_data in categories.items():
            if category not in selected_categories:
                continue
                
            # Apply filters
            filtered_items = []
            for item in cat_data["items"]:
                # Search filter
                if search_term and search_term.lower() not in item["name"].lower() and search_term.lower() not in item.get("description", "").lower():
                    continue
                
                # Difficulty filter
                if difficulty_filter != "All" and item.get("difficulty") != difficulty_filter:
                    continue
                
                # ROI filter
                if roi_filter != "All" and item.get("roi_potential") != roi_filter:
                    continue
                
                # Status filter
                is_completed = item["name"] in st.session_state.completed_automations
                is_favorite = item["name"] in st.session_state.favorite_automations
                
                if status_filter == "Completed" and not is_completed:
                    continue
                if status_filter == "Pending" and is_completed:
                    continue
                if status_filter == "Favorites" and not is_favorite:
                    continue
                    
                filtered_items.append(item)
            
            if not filtered_items:
                continue
                
            # Enhanced category header
            completed_in_cat = sum(1 for item in filtered_items if item["name"] in st.session_state.completed_automations)
            st.markdown(f"""
            <div class="category-header">
                <h3>{cat_data['icon']} {category}</h3>
                <p>Progress: {completed_in_cat}/{len(filtered_items)} completed • {len(filtered_items)} items shown</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Display items with comprehensive information
            for i, item in enumerate(filtered_items):
                is_completed = item["name"] in st.session_state.completed_automations
                is_favorite = item["name"] in st.session_state.favorite_automations
                
                # Enhanced item display
                with st.expander(f"{'✅' if is_completed else '⏳'} {'⭐' if is_favorite else ''} {item['name']}", expanded=False):
                    
                    # Item details row
                    col_info, col_actions = st.columns([2, 1])
                    
                    with col_info:
                        st.markdown(f"**Description:** {item.get('description', 'No description available')}")
                        
                        # Metadata badges
                        difficulty_class = f"difficulty-{item.get('difficulty', 'medium').lower()}"
                        roi_class = f"roi-{item.get('roi_potential', 'medium').lower()}"
                        
                        st.markdown(f"""
                        <div style="margin: 10px 0;">
                            <span class="feature-badge badge-new">Difficulty: <span class="{difficulty_class}">{item.get('difficulty', 'Medium')}</span></span>
                            <span class="feature-badge badge-popular">Time: {item.get('time_estimate', 'Unknown')}</span>
                            <span class="feature-badge badge-advanced">Cost: {item.get('cost_estimate', 'Unknown')}</span>
                            <span class="feature-badge badge-new">ROI: <span class="{roi_class}">{item.get('roi_potential', 'Medium')}</span></span>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Tools section
                        if item.get('tools'):
                            st.markdown(f"**Recommended Tools:** {', '.join(item['tools'])}")
                    
                    with col_actions:
                        # Action buttons
                        col_check, col_fav = st.columns(2)
                        
                        with col_check:
                            if st.checkbox("Complete", value=is_completed, key=f"check_{category}_{i}_{item['name'][:10]}"):
                                st.session_state.completed_automations.add(item["name"])
                                if item["name"] not in st.session_state.implementation_dates:
                                    st.session_state.implementation_dates[item["name"]] = datetime.now()
                            else:
                                st.session_state.completed_automations.discard(item["name"])
                        
                        with col_fav:
                            if st.checkbox("Favorite", value=is_favorite, key=f"fav_{category}_{i}_{item['name'][:10]}"):
                                st.session_state.favorite_automations.add(item["name"])
                            else:
                                st.session_state.favorite_automations.discard(item["name"])
                    
                    # Priority and notes section
                    col_priority, col_notes = st.columns([1, 2])
                    
                    with col_priority:
                        priority = st.selectbox(
                            "Priority:",
                            ["High", "Medium", "Low"],
                            index=["High", "Medium", "Low"].index(st.session_state.priority_levels.get(item["name"], "Medium")),
                            key=f"priority_{category}_{i}_{item['name'][:10]}"
                        )
                        st.session_state.priority_levels[item["name"]] = priority
                    
                    with col_notes:
                        note = st.text_area(
                            "Implementation Notes:",
                            value=st.session_state.automation_notes.get(item["name"], ""),
                            height=80,  # Fixed: Changed from 60 to 80 pixels
                            key=f"note_{category}_{i}_{item['name'][:10]}",
                            placeholder="Add your implementation notes, progress updates, or lessons learned..."
                        )
                        st.session_state.automation_notes[item["name"]] = note
    
    with col2:
        st.header("📈 Quick Stats")
        
        # Enhanced analytics
        st.subheader("🎯 Priority Breakdown")
        high_priority = sum(1 for item, priority in st.session_state.priority_levels.items() if priority == "High")
        medium_priority = sum(1 for item, priority in st.session_state.priority_levels.items() if priority == "Medium")
        low_priority = sum(1 for item, priority in st.session_state.priority_levels.items() if priority == "Low")
        
        st.metric("🔴 High Priority", high_priority)
        st.metric("🟡 Medium Priority", medium_priority)
        st.metric("🟢 Low Priority", low_priority)
        
        st.markdown("---")
        
        # Implementation timeline
        st.subheader("📅 Recent Activity")
        recent_implementations = sorted(
            [(name, date) for name, date in st.session_state.implementation_dates.items()],
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        if recent_implementations:
            for name, date in recent_implementations:
                st.write(f"✅ {name[:30]}...")
                st.caption(f"Completed: {date.strftime('%Y-%m-%d')}")
        else:
            st.info("No recent implementations")
        
        st.markdown("---")
        
        # Quick tips
        st.subheader("💡 Implementation Tips")
        tips = [
            "Start with 'Easy' difficulty items",
            "Focus on high ROI automations first",
            "Test with small groups initially",
            "Document what works well",
            "Scale successful automations"
        ]
        
        for tip in tips:
            st.write(f"• {tip}")

with tab2:
    st.header("📊 Analytics Dashboard")
    
    # Create comprehensive analytics
    if completed_count > 0:
        # Progress over time (simulated)
        col1, col2 = st.columns(2)
        
        with col1:
            # Completion by category
            category_data = []
            for category, cat_data in categories.items():
                completed_in_cat = sum(1 for item in cat_data["items"] if item["name"] in st.session_state.completed_automations)
                category_data.append({
                    "Category": category.split(" &")[0],
                    "Completed": completed_in_cat,
                    "Total": len(cat_data["items"]),
                    "Percentage": (completed_in_cat / len(cat_data["items"])) * 100
                })
            
            df_categories = pd.DataFrame(category_data)
            fig = px.bar(df_categories, x="Category", y="Percentage", 
                        title="Completion Rate by Category",
                        color="Percentage",
                        color_continuous_scale="Viridis")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # ROI potential distribution
            roi_data = {"High": 0, "Medium": 0, "Low": 0}
            for cat_data in categories.values():
                for item in cat_data["items"]:
                    if item["name"] in st.session_state.completed_automations:
                        roi_data[item.get("roi_potential", "Medium")] += 1
            
            fig = px.pie(values=list(roi_data.values()), names=list(roi_data.keys()),
                        title="Completed Automations by ROI Potential")
            st.plotly_chart(fig, use_container_width=True)
        
        # Difficulty analysis
        st.subheader("📈 Implementation Analysis")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Average Implementation Time", "6.5 hours", delta="Estimated")
        with col2:
            st.metric("Total Estimated Cost", "$2,450", delta="For all completed")
        with col3:
            st.metric("Potential ROI", "340%", delta="Based on time savings")
    
    else:
        st.info("Complete some automations to see analytics!")

with tab3:
    st.header("🛠️ Implementation Guides")
    
    # Popular implementation guides
    guides = {
        "Getting Started with Email Automation": {
            "steps": [
                "Choose an email platform (Mailchimp, ConvertKit)",
                "Set up your account and verify domain",
                "Create email templates for common scenarios",
                "Set up automation triggers",
                "Test with a small group",
                "Monitor and optimize"
            ],
            "tools": ["Mailchimp", "ConvertKit", "Zapier"],
            "time": "4-6 hours",
            "difficulty": "Easy"
        },
        "Setting Up Payment Automation": {
            "steps": [
                "Create Stripe or PayPal account",
                "Integrate with your booking system",
                "Set up recurring billing",
                "Configure failed payment handling",
                "Test payment flows",
                "Set up reporting"
            ],
            "tools": ["Stripe", "PayPal", "Zapier"],
            "time": "6-10 hours",
            "difficulty": "Medium"
        },
        "Building a Customer Communication System": {
            "steps": [
                "Choose SMS platform (Twilio)",
                "Set up phone number",
                "Create message templates",
                "Integrate with scheduling system",
                "Set up automated triggers",
                "Monitor delivery rates"
            ],
            "tools": ["Twilio", "SMS platform", "Zapier"],
            "time": "8-12 hours",
            "difficulty": "Medium"
        }
    }
    
    for guide_name, guide_data in guides.items():
        with st.expander(f"📖 {guide_name}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("### Implementation Steps:")
                for i, step in enumerate(guide_data["steps"], 1):
                    st.write(f"{i}. {step}")
            
            with col2:
                st.markdown("### Guide Details:")
                st.write(f"**Time Required:** {guide_data['time']}")
                st.write(f"**Difficulty:** {guide_data['difficulty']}")
                st.write(f"**Tools Needed:** {', '.join(guide_data['tools'])}")

with tab4:
    st.header("💡 ROI Calculator")
    
    st.markdown("Calculate the potential return on investment for your automation implementations.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Input Your Data")
        
        # ROI calculation inputs
        hourly_rate = st.number_input("Your hourly rate ($)", min_value=10, max_value=200, value=50)
        hours_saved_weekly = st.number_input("Hours saved per week", min_value=1, max_value=40, value=10)
        implementation_cost = st.number_input("Total implementation cost ($)", min_value=0, max_value=10000, value=500)
        monthly_tool_cost = st.number_input("Monthly tool costs ($)", min_value=0, max_value=1000, value=100)
        
        # Calculate ROI
        weekly_savings = hourly_rate * hours_saved_weekly
        monthly_savings = weekly_savings * 4.33  # Average weeks per month
        annual_savings = monthly_savings * 12
        annual_costs = (monthly_tool_cost * 12) + implementation_cost
        
        net_annual_benefit = annual_savings - annual_costs
        roi_percentage = (net_annual_benefit / implementation_cost) * 100 if implementation_cost > 0 else 0
        payback_months = implementation_cost / monthly_savings if monthly_savings > 0 else 0
    
    with col2:
        st.subheader("📈 ROI Results")
        
        st.metric("Annual Time Savings", f"{hours_saved_weekly * 52:.0f} hours")
        st.metric("Annual Cost Savings", f"${annual_savings:,.2f}")
        st.metric("Annual Tool Costs", f"${annual_costs:,.2f}")
        st.metric("Net Annual Benefit", f"${net_annual_benefit:,.2f}")
        st.metric("ROI Percentage", f"{roi_percentage:.1f}%")
        st.metric("Payback Period", f"{payback_months:.1f} months")
        
        # ROI visualization
        if net_annual_benefit > 0:
            st.success(f"✅ Positive ROI! You'll save ${net_annual_benefit:,.2f} annually")
        else:
            st.warning(f"⚠️ Negative ROI. Consider reducing costs or increasing efficiency gains.")

# Enhanced footer
st.markdown("---")
st.markdown("## 🚀 Take Your Cleaning Business to the Next Level")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    ### 🔧 Essential Tools
    - **Zapier** - Connect 5000+ apps
    - **Make.com** - Advanced workflows
    - **Google Workspace** - Forms & productivity
    - **Calendly** - Smart scheduling
    - **Stripe** - Payment processing
    """)

with col2:
    st.markdown("""
    ### 💡 Success Tips
    - Start with high-impact, easy wins
    - Test everything before full rollout
    - Train your team thoroughly
    - Monitor performance metrics
    - Iterate and improve continuously
    """)

with col3:
    st.markdown("""
    ### 📊 Key Metrics to Track
    - Time saved per automation
    - Customer satisfaction scores
    - Booking conversion rates
    - Team productivity gains
    - Revenue per customer
    """)

with col4:
    st.markdown("""
    ### 🎯 Implementation Priority
    1. **Client Communication** (High ROI)
    2. **Booking & Scheduling** (Essential)
    3. **Payment Processing** (Revenue)
    4. **Team Management** (Efficiency)
    5. **Advanced Features** (Scale)
    """)

# Save progress notification
if st.button("💾 Save All Progress", use_container_width=True, type="primary"):
    progress_data = {
        "completed": list(st.session_state.completed_automations),
        "notes": st.session_state.automation_notes,
        "priorities": st.session_state.priority_levels,
        "favorites": list(st.session_state.favorite_automations),
        "implementation_dates": {k: v.isoformat() for k, v in st.session_state.implementation_dates.items()},
        "last_updated": datetime.now().isoformat()
    }
    st.success("✅ All progress saved successfully! Your data is preserved for future sessions.")
    st.balloons()
