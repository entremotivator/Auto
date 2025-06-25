import streamlit as st
import pandas as pd
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="100 Automations for Cleaning Companies", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        margin-bottom: 2rem;
    }
    .category-header {
        background: linear-gradient(90deg, #2E86AB, #A23B72);
        color: white;
        padding: 10px;
        border-radius: 5px;
        margin: 20px 0 10px 0;
    }
    .automation-item {
        background-color: #f8f9fa;
        padding: 10px;
        margin: 5px 0;
        border-left: 4px solid #2E86AB;
        border-radius: 3px;
    }
    .progress-bar {
        background-color: #e9ecef;
        border-radius: 10px;
        padding: 3px;
    }
    .progress-fill {
        background: linear-gradient(90deg, #28a745, #20c997);
        height: 20px;
        border-radius: 7px;
        text-align: center;
        line-height: 20px;
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for tracking completed automations
if 'completed_automations' not in st.session_state:
    st.session_state.completed_automations = set()

# Automation categories and items
categories = {
    "Client Onboarding & Management": [
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
        "Send "pre-clean checklist" automatically before visit",
        "Move client to VIP tag after 10 services"
    ],
    "Booking & Scheduling": [
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
    "Payments & Invoicing": [
        "Auto-generate invoice after job completion",
        "Stripe payment failed → send retry link",
        "Send invoice reminders every 3 days (max 3x)",
        "Auto-charge recurring cleaning clients",
        "Send thank you receipt after payment",
        "Sync payments with QuickBooks/Xero",
        "Auto-calculate travel surcharges",
        "First-time discount automatically applied",
        "Add upsells (fridge, oven) in invoice builder",
        "Auto-tag "high-ticket" clients in CRM",
        "Auto-apply coupon code from referral system",
        "Estimate calculator form with automatic email follow-up",
        "Notify admin when client exceeds late payment threshold",
        "Auto-suspend services until payment is received",
        "Payment data dashboard updates daily"
    ],
    "Team Management & Operations": [
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
    "Marketing & Sales": [
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
    "Customer Communication": [
        "Two-way SMS integration for support",
        "Auto-respond to website chat inquiries",
        "Missed call → auto-text "How can we help?"",
        "Job status updates via SMS ("In Progress," "Completed")",
        "Auto-email of cleaner profile before visit",
        "Send delay notifications via SMS",
        "Auto-notify customer when cleaner is nearby",
        "Service reminder emails (weekly, biweekly, etc.)",
        ""You're next" job notification for clients",
        "Set auto-replies for off-hours contact"
    ],
    "Reporting & Analytics": [
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
    ]
}

# Calculate total automations
total_automations = sum(len(items) for items in categories.values())

# Main header
st.markdown('<h1 class="main-header">🧼 100 Automations for Cleaning Companies</h1>', unsafe_allow_html=True)
st.markdown("**Streamline operations, improve client experience, and scale your cleaning business with these automation ideas.**")

# Sidebar for filters and progress
with st.sidebar:
    st.header("📊 Progress Tracker")
    
    # Progress calculation
    completed_count = len(st.session_state.completed_automations)
    progress_percentage = (completed_count / total_automations) * 100
    
    # Progress bar
    st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress_percentage}%;">
            {completed_count}/{total_automations} ({progress_percentage:.1f}%)
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Filters
    st.header("🔍 Filters")
    search_term = st.text_input("Search automations:", placeholder="Enter keywords...")
    
    selected_categories = st.multiselect(
        "Filter by category:",
        options=list(categories.keys()),
        default=list(categories.keys())
    )
    
    show_completed = st.checkbox("Show completed only", value=False)
    show_pending = st.checkbox("Show pending only", value=False)
    
    st.markdown("---")
    
    # Quick actions
    st.header("⚡ Quick Actions")
    if st.button("Mark All as Complete"):
        all_items = []
        for cat_items in categories.values():
            all_items.extend(cat_items)
        st.session_state.completed_automations = set(all_items)
        st.rerun()
    
    if st.button("Reset All Progress"):
        st.session_state.completed_automations = set()
        st.rerun()
    
    # Export functionality
    if st.button("📥 Export Progress"):
        export_data = []
        for category, items in categories.items():
            for item in items:
                export_data.append({
                    "Category": category,
                    "Automation": item,
                    "Status": "Completed" if item in st.session_state.completed_automations else "Pending"
                })
        
        df = pd.DataFrame(export_data)
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="cleaning_automations_progress.csv",
            mime="text/csv"
        )

# Main content area
col1, col2 = st.columns([3, 1])

with col1:
    # Display categories and automations
    for category, items in categories.items():
        if category not in selected_categories:
            continue
            
        # Filter items based on search and completion status
        filtered_items = []
        for item in items:
            # Search filter
            if search_term and search_term.lower() not in item.lower():
                continue
            
            # Completion status filter
            is_completed = item in st.session_state.completed_automations
            if show_completed and not is_completed:
                continue
            if show_pending and is_completed:
                continue
                
            filtered_items.append(item)
        
        if not filtered_items:
            continue
            
        # Category header
        st.markdown(f'<div class="category-header"><h3>{category}</h3></div>', unsafe_allow_html=True)
        
        # Display items with checkboxes
        for i, item in enumerate(filtered_items):
            col_check, col_text = st.columns([0.1, 0.9])
            
            with col_check:
                is_completed = item in st.session_state.completed_automations
                if st.checkbox("", value=is_completed, key=f"{category}_{i}_{item[:20]}"):
                    st.session_state.completed_automations.add(item)
                else:
                    st.session_state.completed_automations.discard(item)
            
            with col_text:
                status_emoji = "✅" if item in st.session_state.completed_automations else "⏳"
                st.markdown(f"{status_emoji} {item}")

with col2:
    # Category progress breakdown
    st.header("📈 Category Progress")
    
    for category, items in categories.items():
        if category not in selected_categories:
            continue
            
        completed_in_category = sum(1 for item in items if item in st.session_state.completed_automations)
        total_in_category = len(items)
        category_percentage = (completed_in_category / total_in_category) * 100 if total_in_category > 0 else 0
        
        st.metric(
            label=category.replace(" & ", " &\n"),
            value=f"{completed_in_category}/{total_in_category}",
            delta=f"{category_percentage:.0f}%"
        )

# Footer
st.markdown("---")
st.markdown("""
### 💡 Implementation Tips:
- **Start Small**: Begin with 3-5 high-impact automations
- **Prioritize**: Focus on automations that save the most time or improve customer experience
- **Test First**: Always test automations with a small group before full deployment
- **Document**: Keep track of what works and what doesn't
- **Iterate**: Continuously improve and refine your automations

### 🛠️ Popular Tools for Implementation:
- **Zapier** or **Make.com** for connecting different apps
- **Google Workspace** for forms, sheets, and calendar integration
- **Stripe** or **Square** for payment automation
- **Mailchimp** or **ConvertKit** for email marketing
- **Calendly** or **Acuity** for booking systems
- **Slack** or **Microsoft Teams** for team communication
""")
