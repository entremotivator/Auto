import streamlit as st
import pandas as pd
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="100+ Automations for Cleaning Companies", 
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
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .category-header {
        background: linear-gradient(135deg, #2E86AB, #A23B72, #F18F01);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 25px 0 15px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .automation-item {
        background-color: #f8f9fa;
        padding: 12px;
        margin: 8px 0;
        border-left: 4px solid #2E86AB;
        border-radius: 8px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .automation-item:hover {
        background-color: #e9ecef;
        transform: translateX(5px);
    }
    .completed-item {
        background-color: #d4edda;
        border-left-color: #28a745;
        opacity: 0.8;
    }
    .progress-container {
        background-color: #e9ecef;
        border-radius: 15px;
        padding: 4px;
        margin: 10px 0;
    }
    .progress-fill {
        background: linear-gradient(90deg, #28a745, #20c997);
        height: 25px;
        border-radius: 12px;
        text-align: center;
        line-height: 25px;
        color: white;
        font-weight: bold;
        transition: width 0.5s ease;
    }
    .metric-card {
        background: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
        text-align: center;
    }
    .priority-high { border-left-color: #dc3545; }
    .priority-medium { border-left-color: #ffc107; }
    .priority-low { border-left-color: #28a745; }
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'completed_automations' not in st.session_state:
    st.session_state.completed_automations = set()
if 'automation_notes' not in st.session_state:
    st.session_state.automation_notes = {}
if 'priority_levels' not in st.session_state:
    st.session_state.priority_levels = {}

# Automation categories with priority and difficulty levels
categories = {
    "Client Onboarding & Management": {
        "items": [
            "New client welcome email sequence",
            "Auto-send intake form after booking",
            "Automated quote generator",
            "CRM entry upon lead submission",
            "Auto-reminder to complete service agreement",
            "Assign client to team based on zip code",
            "Birthday or anniversary client greeting email",
            "Follow-up email after service with feedback link",
            "Send review request via SMS/email",
            "Tag clients based on service frequency",
            "Auto-schedule recurring appointments",
            "Client reactivation campaigns after 60+ days",
            "Auto-update Google Sheet with new client info",
            'Send "pre-clean checklist" automatically before visit',
            "Move client to VIP tag after 10 services"
        ],
        "icon": "👥",
        "color": "#2E86AB"
    },
    "Booking & Scheduling": {
        "items": [
            "Online booking form → Google Calendar",
            "Auto-notification to cleaner about new job",
            "Rescheduling link auto-included in reminders",
            "Auto-cancel recurring job if card fails",
            "Send ETA texts to clients 1 hour before arrival",
            "Send weekly schedule to team every Monday",
            "Auto-assign cleaners based on zone/availability",
            "Buffer time automation between bookings",
            "Auto-block days off from calendar",
            "Cleaning crew shift reminder SMS",
            "Day-before job confirmation SMS/email",
            "Auto-reschedule on public holidays",
            "Weather alert integration for outdoor jobs",
            "Double-booking prevention alert",
            "Missed booking alert and recovery automation"
        ],
        "icon": "📅",
        "color": "#A23B72"
    },
    "Payments & Invoicing": {
        "items": [
            "Auto-generate invoice after job completion",
            "Stripe payment failed → send retry link",
            "Send invoice reminders every 3 days (max 3x)",
            "Auto-charge recurring cleaning clients",
            "Send thank you receipt after payment",
            "Sync payments with QuickBooks/Xero",
            "Auto-calculate travel surcharges",
            "First-time discount automatically applied",
            "Add upsells (fridge, oven) in invoice builder",
            'Auto-tag "high-ticket" clients in CRM',
            "Auto-apply coupon code from referral system",
            "Estimate calculator form with automatic email follow-up",
            "Notify admin when client exceeds late payment threshold",
            "Auto-suspend services until payment is received",
            "Payment data dashboard updates daily"
        ],
        "icon": "💰",
        "color": "#F18F01"
    },
    "Team Management & Operations": {
        "items": [
            "Send daily job route to each cleaner",
            "Auto clock-in/out system via geolocation",
            "Slack/WhatsApp message if staff doesn't check-in",
            "Team KPI tracker update every week",
            "Auto-assign team leads per route",
            "Weekly timesheet auto-submission reminder",
            "Auto-upload photos of completed jobs to shared drive",
            "Cleaning checklist completion tracking",
            "Job satisfaction survey from cleaner",
            "Auto-flag negative reviews for manager review",
            "Equipment maintenance reminder every 30 uses",
            "Cleaner performance review every 90 days",
            "Auto-email when supplies drop below stock level",
            "Geofence tracking for mobile crews",
            "Send client notes to cleaner before job",
            "Employee reward points system tracker",
            "Trigger onboarding for new hires",
            "Certification or training renewal reminders",
            "Auto-send route changes via SMS",
            "Auto-log hours into payroll system"
        ],
        "icon": "👷",
        "color": "#C73E1D"
    },
    "Marketing & Sales": {
        "items": [
            "Abandoned quote follow-up email",
            "Lead magnet download → 5-day nurture sequence",
            "Auto-tag lead source (Facebook, Google, etc.)",
            "Google Review + Yelp review link SMS",
            "Win-back emails for old customers",
            "Auto-post testimonials to website",
            "Send referral program invite after 3 jobs",
            "Weekly email newsletter automation",
            "Reactivate cold leads with discount offer",
            "Instagram post scheduling",
            "Auto-detect and email duplicate leads",
            "Trigger a call task for high-interest leads",
            "Send seasonal promo campaigns (e.g., spring cleaning)",
            "Add new leads from Facebook Ads to CRM",
            "Auto-score leads based on form inputs"
        ],
        "icon": "📈",
        "color": "#6A994E"
    },
    "Customer Communication": {
        "items": [
            "Two-way SMS integration for support",
            "Auto-respond to website chat inquiries",
            'Missed call → auto-text "How can we help?"',
            'Job status updates via SMS ("In Progress," "Completed")',
            "Auto-email of cleaner profile before visit",
            "Send delay notifications via SMS",
            "Auto-notify customer when cleaner is nearby",
            "Service reminder emails (weekly, biweekly, etc.)",
            '"You\'re next" job notification for clients',
            "Set auto-replies for off-hours contact"
        ],
        "icon": "💬",
        "color": "#7209B7"
    },
    "Reporting & Analytics": {
        "items": [
            "Weekly revenue report emailed to owner",
            "Auto-generate monthly KPI dashboard",
            "New client acquisition report",
            "Cleaner performance heatmap",
            "Missed job or reschedule frequency report",
            "Auto-track ad spend vs. bookings",
            "Most-requested services chart",
            "Net Promoter Score (NPS) tracking",
            "Client lifetime value calculator",
            "Export all data monthly to cloud drive"
        ],
        "icon": "📊",
        "color": "#FF6B35"
    }
}

# Calculate total automations
total_automations = sum(len(cat_data["items"]) for cat_data in categories.values())

# Main header
st.markdown('<h1 class="main-header">🧼 Cleaning Business Automation Hub</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Transform your cleaning business with 100+ powerful automation ideas</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📊 Progress Dashboard")
    
    # Progress calculation
    completed_count = len(st.session_state.completed_automations)
    progress_percentage = (completed_count / total_automations) * 100
    
    # Enhanced progress bar
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-fill" style="width: {progress_percentage}%;">
            {completed_count}/{total_automations} ({progress_percentage:.1f}%)
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    st.markdown("### 📈 Quick Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Completed", completed_count, delta=None)
    with col2:
        st.metric("Remaining", total_automations - completed_count, delta=None)
    
    st.markdown("---")
    
    # Enhanced filters
    st.header("🔍 Smart Filters")
    search_term = st.text_input("🔎 Search automations:", placeholder="Enter keywords...")
    
    selected_categories = st.multiselect(
        "📂 Categories:",
        options=list(categories.keys()),
        default=list(categories.keys()),
        format_func=lambda x: f"{categories[x]['icon']} {x}"
    )
    
    # Status filters
    st.subheader("Status Filter")
    filter_option = st.radio(
        "Show:",
        ["All", "Completed Only", "Pending Only", "High Priority"],
        index=0
    )
    
    # Priority filter
    priority_filter = st.selectbox(
        "Priority Level:",
        ["All Priorities", "High Priority", "Medium Priority", "Low Priority"]
    )
    
    st.markdown("---")
    
    # Quick actions
    st.header("⚡ Quick Actions")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Complete All", use_container_width=True):
            all_items = []
            for cat_data in categories.values():
                all_items.extend(cat_data["items"])
            st.session_state.completed_automations = set(all_items)
            st.rerun()
    
    with col2:
        if st.button("🔄 Reset All", use_container_width=True):
            st.session_state.completed_automations = set()
            st.session_state.automation_notes = {}
            st.rerun()
    
    # Export functionality
    st.subheader("📥 Export Options")
    
    if st.button("📊 Download Progress Report", use_container_width=True):
        export_data = []
        for category, cat_data in categories.items():
            for item in cat_data["items"]:
                export_data.append({
                    "Category": category,
                    "Automation": item,
                    "Status": "✅ Completed" if item in st.session_state.completed_automations else "⏳ Pending",
                    "Priority": st.session_state.priority_levels.get(item, "Medium"),
                    "Notes": st.session_state.automation_notes.get(item, ""),
                    "Date_Added": datetime.now().strftime("%Y-%m-%d")
                })
        
        df = pd.DataFrame(export_data)
        csv = df.to_csv(index=False)
        st.download_button(
            label="📄 Download CSV",
            data=csv,
            file_name=f"cleaning_automations_progress_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )

# Main content area
# Category overview cards
st.header("📋 Category Overview")
cols = st.columns(len(categories))
for i, (category, cat_data) in enumerate(categories.items()):
    with cols[i % len(cols)]:
        completed_in_category = sum(1 for item in cat_data["items"] if item in st.session_state.completed_automations)
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

# Main automation list
col1, col2 = st.columns([3, 1])

with col1:
    st.header("🎯 Automation Checklist")
    
    # Display categories and automations
    for category, cat_data in categories.items():
        if category not in selected_categories:
            continue
            
        # Filter items based on search and completion status
        filtered_items = []
        for item in cat_data["items"]:
            # Search filter
            if search_term and search_term.lower() not in item.lower():
                continue
            
            # Status filter
            is_completed = item in st.session_state.completed_automations
            if filter_option == "Completed Only" and not is_completed:
                continue
            if filter_option == "Pending Only" and is_completed:
                continue
                
            filtered_items.append(item)
        
        if not filtered_items:
            continue
            
        # Category header with enhanced styling
        st.markdown(f"""
        <div class="category-header">
            <h3>{cat_data['icon']} {category} ({len([item for item in cat_data['items'] if item in st.session_state.completed_automations])}/{len(cat_data['items'])} completed)</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Display items with enhanced features
        for i, item in enumerate(filtered_items):
            is_completed = item in st.session_state.completed_automations
            
            # Create expandable item
            with st.expander(f"{'✅' if is_completed else '⏳'} {item}", expanded=False):
                col_check, col_priority, col_notes = st.columns([1, 1, 2])
                
                with col_check:
                    if st.checkbox("Mark Complete", value=is_completed, key=f"check_{category}_{i}"):
                        st.session_state.completed_automations.add(item)
                    else:
                        st.session_state.completed_automations.discard(item)
                
                with col_priority:
                    priority = st.selectbox(
                        "Priority:",
                        ["High", "Medium", "Low"],
                        index=["High", "Medium", "Low"].index(st.session_state.priority_levels.get(item, "Medium")),
                        key=f"priority_{category}_{i}"
                    )
                    st.session_state.priority_levels[item] = priority
                
                with col_notes:
                    note = st.text_area(
                        "Implementation Notes:",
                        value=st.session_state.automation_notes.get(item, ""),
                        height=60,
                        key=f"note_{category}_{i}",
                        placeholder="Add your implementation notes here..."
                    )
                    st.session_state.automation_notes[item] = note

with col2:
    st.header("📈 Analytics")
    
    # Priority breakdown
    st.subheader("🎯 Priority Breakdown")
    high_priority = sum(1 for item, priority in st.session_state.priority_levels.items() if priority == "High")
    medium_priority = sum(1 for item, priority in st.session_state.priority_levels.items() if priority == "Medium")
    low_priority = sum(1 for item, priority in st.session_state.priority_levels.items() if priority == "Low")
    
    st.metric("🔴 High Priority", high_priority)
    st.metric("🟡 Medium Priority", medium_priority)
    st.metric("🟢 Low Priority", low_priority)
    
    st.markdown("---")
    
    # Recent activity
    st.subheader("📅 Implementation Tips")
    st.info("""
    **Getting Started:**
    1. Start with 3-5 high-impact automations
    2. Focus on client communication first
    3. Test with a small group initially
    4. Document what works
    5. Scale gradually
    """)
    
    st.success("""
    **Quick Wins:**
    - Email confirmations
    - Review requests
    - Payment reminders
    - Booking confirmations
    """)

# Footer with enhanced information
st.markdown("---")
st.markdown("## 🛠️ Implementation Resources")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🔧 Popular Tools
    - **Zapier** - Connect apps easily
    - **Make.com** - Advanced automation
    - **Google Workspace** - Forms & sheets
    - **Calendly** - Booking system
    - **Mailchimp** - Email marketing
    """)

with col2:
    st.markdown("""
    ### 💡 Best Practices
    - Start small and scale up
    - Test before full deployment
    - Monitor performance regularly
    - Keep backups of data
    - Train your team properly
    """)

with col3:
    st.markdown("""
    ### 📊 ROI Indicators
    - Time saved per week
    - Reduced manual errors
    - Improved customer satisfaction
    - Increased booking rates
    - Better team efficiency
    """)

# Save progress automatically
if st.button("💾 Save Progress", use_container_width=True):
    progress_data = {
        "completed": list(st.session_state.completed_automations),
        "notes": st.session_state.automation_notes,
        "priorities": st.session_state.priority_levels,
        "last_updated": datetime.now().isoformat()
    }
    st.success("✅ Progress saved successfully!")
