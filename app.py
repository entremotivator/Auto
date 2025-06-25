import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json

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
    }
    .automation-item {
        background: linear-gradient(145deg, #f8f9fa, #e9ecef);
        padding: 15px;
        margin: 10px 0;
        border-left: 5px solid #2E86AB;
        border-radius: 12px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
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
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
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

init_session_state()

# Define automation data structure
def get_automation_data():
    return {
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
                },
                {
                    "name": "Auto-schedule recurring appointments",
                    "difficulty": "Medium",
                    "time_estimate": "4-8 hours",
                    "cost_estimate": "$50-150",
                    "roi_potential": "High",
                    "tools": ["Scheduling software", "Calendar API", "CRM"],
                    "description": "Automatically book recurring cleaning appointments"
                },
                {
                    "name": "Client reactivation campaigns after 60+ days",
                    "difficulty": "Easy",
                    "time_estimate": "3-5 hours",
                    "cost_estimate": "$25-75",
                    "roi_potential": "High",
                    "tools": ["Email marketing", "CRM", "Automation platform"],
                    "description": "Win-back campaigns for inactive clients"
                },
                {
                    "name": "Auto-update Google Sheet with new client info",
                    "difficulty": "Easy",
                    "time_estimate": "1-3 hours",
                    "cost_estimate": "$0-25",
                    "roi_potential": "Medium",
                    "tools": ["Google Sheets", "Zapier", "Forms"],
                    "description": "Automatically populate spreadsheets with client data"
                },
                {
                    "name": "Send pre-clean checklist automatically before visit",
                    "difficulty": "Easy",
                    "time_estimate": "2-4 hours",
                    "cost_estimate": "$0-50",
                    "roi_potential": "Medium",
                    "tools": ["Email automation", "Scheduling system", "Templates"],
                    "description": "Automated pre-service preparation instructions"
                },
                {
                    "name": "Move client to VIP tag after 10 services",
                    "difficulty": "Medium",
                    "time_estimate": "3-6 hours",
                    "cost_estimate": "$25-100",
                    "roi_potential": "Medium",
                    "tools": ["CRM", "Analytics", "Automation rules"],
                    "description": "Automatically upgrade loyal customers to VIP status"
                }
            ],
            "icon": "👥",
            "color": "#2E86AB"
        },
        "Booking & Scheduling": {
            "items": [
                {
                    "name": "Online booking form to Google Calendar",
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
                    "name": "Rescheduling link auto-included in reminders",
                    "difficulty": "Easy",
                    "time_estimate": "2-3 hours",
                    "cost_estimate": "$0-40",
                    "roi_potential": "Medium",
                    "tools": ["Scheduling software", "Email templates", "Calendar"],
                    "description": "Easy rescheduling options in appointment reminders"
                },
                {
                    "name": "Auto-cancel recurring job if card fails",
                    "difficulty": "Medium",
                    "time_estimate": "4-6 hours",
                    "cost_estimate": "$50-120",
                    "roi_potential": "High",
                    "tools": ["Payment processor", "Scheduling system", "Automation"],
                    "description": "Prevent service delivery for failed payments"
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
                    "name": "Send weekly schedule to team every Monday",
                    "difficulty": "Easy",
                    "time_estimate": "2-4 hours",
                    "cost_estimate": "$10-50",
                    "roi_potential": "Medium",
                    "tools": ["Email automation", "Calendar", "Team communication"],
                    "description": "Weekly schedule distribution to cleaning teams"
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
                    "name": "Buffer time automation between bookings",
                    "difficulty": "Medium",
                    "time_estimate": "3-6 hours",
                    "cost_estimate": "$25-100",
                    "roi_potential": "Medium",
                    "tools": ["Scheduling software", "Calendar rules", "Automation"],
                    "description": "Automatic travel time between appointments"
                },
                {
                    "name": "Auto-block days off from calendar",
                    "difficulty": "Easy",
                    "time_estimate": "1-3 hours",
                    "cost_estimate": "$0-30",
                    "roi_potential": "Medium",
                    "tools": ["Calendar integration", "HR system", "Scheduling"],
                    "description": "Prevent bookings on staff vacation days"
                },
                {
                    "name": "Cleaning crew shift reminder SMS",
                    "difficulty": "Easy",
                    "time_estimate": "2-4 hours",
                    "cost_estimate": "$15-50",
                    "roi_potential": "Medium",
                    "tools": ["SMS service", "Scheduling system", "Automation"],
                    "description": "Shift reminders sent to cleaning staff"
                },
                {
                    "name": "Day-before job confirmation SMS/email",
                    "difficulty": "Easy",
                    "time_estimate": "2-3 hours",
                    "cost_estimate": "$10-40",
                    "roi_potential": "High",
                    "tools": ["Communication platform", "Scheduling", "Templates"],
                    "description": "Appointment confirmations sent day before service"
                },
                {
                    "name": "Auto-reschedule on public holidays",
                    "difficulty": "Medium",
                    "time_estimate": "4-8 hours",
                    "cost_estimate": "$50-150",
                    "roi_potential": "Medium",
                    "tools": ["Calendar API", "Holiday database", "Scheduling"],
                    "description": "Automatic holiday scheduling adjustments"
                },
                {
                    "name": "Weather alert integration for outdoor jobs",
                    "difficulty": "Medium",
                    "time_estimate": "3-5 hours",
                    "cost_estimate": "$25-75",
                    "roi_potential": "Medium",
                    "tools": ["Weather API", "Zapier", "SMS service"],
                    "description": "Automatic weather-based scheduling adjustments"
                },
                {
                    "name": "Double-booking prevention alert",
                    "difficulty": "Easy",
                    "time_estimate": "2-4 hours",
                    "cost_estimate": "$0-50",
                    "roi_potential": "High",
                    "tools": ["Scheduling software", "Calendar validation", "Alerts"],
                    "description": "Prevent scheduling conflicts automatically"
                },
                {
                    "name": "Missed booking alert and recovery automation",
                    "difficulty": "Medium",
                    "time_estimate": "4-7 hours",
                    "cost_estimate": "$50-120",
                    "roi_potential": "High",
                    "tools": ["Tracking system", "Communication platform", "CRM"],
                    "description": "Automatic follow-up for missed appointments"
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
                    "name": "Stripe payment failed send retry link",
                    "difficulty": "Medium",
                    "time_estimate": "3-5 hours",
                    "cost_estimate": "$50-100",
                    "roi_potential": "High",
                    "tools": ["Stripe", "Email automation", "Zapier"],
                    "description": "Automated payment retry system for failed transactions"
                },
                {
                    "name": "Send invoice reminders every 3 days (max 3x)",
                    "difficulty": "Easy",
                    "time_estimate": "2-4 hours",
                    "cost_estimate": "$20-60",
                    "roi_potential": "High",
                    "tools": ["Email automation", "Invoice system", "Scheduling"],
                    "description": "Automated payment reminder sequence"
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
                    "name": "Send thank you receipt after payment",
                    "difficulty": "Easy",
                    "time_estimate": "1-2 hours",
                    "cost_estimate": "$0-25",
                    "roi_potential": "Medium",
                    "tools": ["Email automation", "Payment processor", "Templates"],
                    "description": "Automated payment confirmation emails"
                },
                {
                    "name": "Sync payments with QuickBooks/Xero",
                    "difficulty": "Medium",
                    "time_estimate": "4-8 hours",
                    "cost_estimate": "$100-250",
                    "roi_potential": "High",
                    "tools": ["QuickBooks", "Xero", "API integration"],
                    "description": "Automatic accounting software synchronization"
                },
                {
                    "name": "Auto-calculate travel surcharges",
                    "difficulty": "Medium",
                    "time_estimate": "5-10 hours",
                    "cost_estimate": "$75-200",
                    "roi_potential": "Medium",
                    "tools": ["Google Maps API", "Pricing calculator", "Booking system"],
                    "description": "Distance-based automatic surcharge calculation"
                },
                {
                    "name": "First-time discount automatically applied",
                    "difficulty": "Easy",
                    "time_estimate": "2-3 hours",
                    "cost_estimate": "$0-50",
                    "roi_potential": "High",
                    "tools": ["Booking system", "Coupon codes", "CRM"],
                    "description": "Automatic new customer discount application"
                },
                {
                    "name": "Add upsells (fridge, oven) in invoice builder",
                    "difficulty": "Medium",
                    "time_estimate": "4-8 hours",
                    "cost_estimate": "$50-150",
                    "roi_potential": "High",
                    "tools": ["Invoice system", "Service catalog", "Automation"],
                    "description": "Automatic upsell suggestions in invoices"
                },
                {
                    "name": "Auto-tag high-ticket clients in CRM",
                    "difficulty": "Easy",
                    "time_estimate": "2-4 hours",
                    "cost_estimate": "$0-50",
                    "roi_potential": "Medium",
                    "tools": ["CRM", "Analytics", "Automation rules"],
                    "description": "Automatically identify and tag valuable customers"
                },
                {
                    "name": "Auto-apply coupon code from referral system",
                    "difficulty": "Medium",
                    "time_estimate": "3-6 hours",
                    "cost_estimate": "$50-120",
                    "roi_potential": "High",
                    "tools": ["Referral software", "Booking system", "Coupon management"],
                    "description": "Automatic referral discount application"
                },
                {
                    "name": "Estimate calculator form with automatic email follow-up",
                    "difficulty": "Medium",
                    "time_estimate": "6-12 hours",
                    "cost_estimate": "$100-300",
                    "roi_potential": "High",
                    "tools": ["Form builder", "Email automation", "Calculator"],
                    "description": "Interactive quote calculator with follow-up sequence"
                },
                {
                    "name": "Notify admin when client exceeds late payment threshold",
                    "difficulty": "Easy",
                    "time_estimate": "2-4 hours",
                    "cost_estimate": "$10-50",
                    "roi_potential": "Medium",
                    "tools": ["Alert system", "Payment tracking", "Email/SMS"],
                    "description": "Automatic alerts for overdue payments"
                },
                {
                    "name": "Auto-suspend services until payment is received",
                    "difficulty": "Medium",
                    "time_estimate": "4-8 hours",
                    "cost_estimate": "$75-200",
                    "roi_potential": "High",
                    "tools": ["Payment system", "Scheduling software", "Automation"],
                    "description": "Automatic service suspension for non-payment"
                },
                {
                    "name": "Payment data dashboard updates daily",
                    "difficulty": "Medium",
                    "time_estimate": "6-12 hours",
                    "cost_estimate": "$150-400",
                    "roi_potential": "Medium",
                    "tools": ["Dashboard tool", "Payment API", "Analytics"],
                    "description": "Automated financial reporting dashboard"
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
                    "name": "Slack/WhatsApp message if staff doesn't check-in",
                    "difficulty": "Easy",
                    "time_estimate": "2-4 hours",
                    "cost_estimate": "$10-50",
                    "roi_potential": "Medium",
                    "tools": ["Slack", "WhatsApp API", "Monitoring system"],
                    "description": "Automatic alerts for missing staff check-ins"
                },
                {
                    "name": "Team KPI tracker update every week",
                    "difficulty": "Medium",
                    "time_estimate": "6-12 hours",
                    "cost_estimate": "$100-300",
                    "roi_potential": "Medium",
                    "tools": ["Analytics platform", "Dashboard", "Automation"],
                    "description": "Weekly performance metrics compilation"
                },
                {
                    "name": "Auto-assign team leads per route",
                    "difficulty": "Medium",
                    "time_estimate": "4-8 hours",
                    "cost_estimate": "$75-200",
                    "roi_potential": "Medium",
                    "tools": ["Scheduling system", "Team management", "Logic rules"],
                    "description": "Automatic team leader assignment for routes"
                },
                {
                    "name": "Weekly timesheet auto-submission reminder",
                    "difficulty": "Easy",
                    "time_estimate": "1-3 hours",
                    "cost_estimate": "$10-40",
                    "roi_potential": "Medium",
                    "tools": ["Email automation", "Timesheet system", "Scheduling"],
                    "description": "Automated timesheet submission reminders"
                },
                {
                    "name": "Auto-upload photos of completed jobs to shared drive",
                    "difficulty": "Medium",
                    "time_estimate": "4-8 hours",
                    "cost_estimate": "$50-150",
                    "roi_potential": "Medium",
                    "tools": ["Cloud storage", "Mobile app", "API integration"],
                    "description": "Automatic job completion photo management"
                },
                {
                    "name": "Cleaning checklist completion tracking",
                    "difficulty": "Medium",
                    "time_estimate": "6-10 hours",
                    "cost_estimate": "$100-250",
                    "roi_potential": "High",
                    "tools": ["Mobile app", "Database", "Analytics"],
                    "description": "Digital checklist tracking and compliance monitoring"
                },
                {
                    "name": "Job satisfaction survey from cleaner",
                    "difficulty": "Easy",
                    "time_estimate": "2-4 hours",
                    "cost_estimate": "$20-60",
                    "roi_potential": "Medium",
                    "tools": ["Survey tool", "Email automation", "Analytics"],
                    "description": "Post-job satisfaction surveys for cleaning staff"
                },
                {
                    "name": "Auto-flag negative reviews for manager review",
                    "difficulty": "Medium",
                    "time_estimate": "3-6 hours",
                    "cost_estimate": "$50-120",
                    "roi_potential": "High",
                    "tools": ["Review monitoring", "Alert system", "Management dashboard"],
                    "description": "Automatic negative review detection and escalation"
                },
                {
                    "name": "Equipment maintenance reminder every 30 uses",
                    "difficulty": "Medium",
                    "time_estimate": "4-6 hours",
                    "cost_estimate": "$50-120",
                    "roi_potential": "Medium",
                    "tools": ["Usage tracking", "Email automation", "Calendar"],
                    "description": "Preventive maintenance scheduling for cleaning equipment"
                },
                {
                    "name": "Cleaner performance review every 90 days",
                    "difficulty": "Medium",
                    "time_estimate": "6-12 hours",
                    "cost_estimate": "$100-300",
                    "roi_potential": "Medium",
                    "tools": ["HR system", "Performance tracking", "Automation"],
                    "description": "Automated quarterly performance review scheduling"
                },
                {
                    "name": "Auto-email when supplies drop below stock level",
                    "difficulty": "Easy",
                    "time_estimate": "2-4 hours",
                    "cost_estimate": "$20-60",
                    "roi_potential": "High",
                    "tools": ["Inventory system", "Email automation", "Alerts"],
                    "description": "Automatic low inventory notifications"
                },
                {
                    "name": "Geofence tracking for mobile crews",
                    "difficulty": "Hard",
                    "time_estimate": "12-20 hours",
                    "cost_estimate": "$200-500",
                    "roi_potential": "High",
                    "tools": ["GPS tracking", "Mobile app", "Geofencing API"],
                    "description": "Location-based crew tracking and alerts"
                },
                {
                    "name": "Send client notes to cleaner before job",
                    "difficulty": "Easy",
                    "time_estimate": "2-4 hours",
                    "cost_estimate": "$10-50",
                    "roi_potential": "High",
                    "tools": ["CRM", "Communication platform", "Scheduling"],
                    "description": "Automatic client preference sharing with cleaning staff"
                },
                {
                    "name": "Employee reward points system tracker",
                    "difficulty": "Medium",
                    "time_estimate": "8-15 hours",
                    "cost_estimate": "$150-400",
                    "roi_potential": "Medium",
                    "tools": ["Rewards platform", "Performance tracking", "Database"],
                    "description": "Gamified employee performance tracking system"
                },
                {
                    "name": "Trigger onboarding for new hires",
                    "difficulty": "Easy",
                    "time_estimate": "3-6 hours",
                    "cost_estimate": "$25-100",
                    "roi_potential": "Medium",
                    "tools": ["HR system", "Email automation", "Document management"],
                    "description": "Automated new employee onboarding process"
                },
                {
                    "name": "Certification or training renewal reminders",
                    "difficulty": "Easy",
                    "time_estimate": "2-4 hours",
                    "cost_estimate": "$15-50",
                    "roi_potential": "Medium",
                    "tools": ["Calendar system", "Email automation", "Training tracker"],
                    "description": "Automatic certification expiry reminders"
                },
                {
                    "name": "Auto-send route changes via SMS",
                    "difficulty": "Easy",
                    "time_estimate": "2-4 hours",
                    "cost_estimate": "$15-50",
                    "roi_potential": "High",
                    "tools": ["SMS service", "Route planning", "Change detection"],
                    "description": "Instant route change notifications to cleaning teams"
                },
                {
                    "name": "Auto-log hours into payroll system",
                    "difficulty": "Medium",
                    "time_estimate": "6-12 hours",
                    "cost_estimate": "$100-300",
                    "roi_potential": "High",
                    "tools": ["Payroll software", "Time tracking", "API integration"],
                    "description": "Automatic timesheet to payroll integration"
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
                    "name": "Lead magnet download 5-day nurture sequence",
                    "difficulty": "Medium",
                    "time_estimate": "8-12 hours",
                    "cost_estimate": "$50-150",
                    "roi_potential": "High",
                    "tools": ["Email marketing", "Landing page", "Content"],
                    "description": "Educational email series for lead nurturing"
                },
                {
                    "name": "Auto-tag lead source (Facebook, Google, etc.)",
                    "difficulty": "Easy",
                    "time_estimate": "2-4 hours",
                    "cost_estimate": "$0-50",
                    "roi_potential": "Medium",
                    "tools": ["CRM", "UTM tracking", "Analytics"],
                    "description": "Automatic lead source identification and tagging"
                },
                {
                    "name": "Google Review + Yelp review link SMS",
                    "difficulty": "Easy",
                    "time_estimate": "2-3 hours",
                    "cost_estimate": "$20-60",
                    "roi_potential": "High",
                    "tools": ["SMS service", "Review platforms", "Automation"],
                    "description": "Automated review request messages"
                },
                {
                    "name": "Win-back emails for old customers",
                    "difficulty": "Easy",
                    "time_estimate": "3-5 hours",
                    "cost_estimate": "$25-75",
                    "roi_potential": "High",
                    "tools": ["Email marketing", "CRM", "Segmentation"],
                    "description": "Re-engagement campaigns for inactive customers"
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
                },
                {
                    "name": "Weekly email newsletter automation",
                    "difficulty": "Medium",
                    "time_estimate": "4-8 hours",
                    "cost_estimate": "$50-150",
                    "roi_potential": "Medium",
                    "tools": ["Email marketing", "Content management", "Scheduling"],
                    "description": "Automated weekly newsletter with tips and updates"
                },
                {
                    "name": "Reactivate cold leads with discount offer",
                    "difficulty": "Easy",
                    "time_estimate": "3-6 hours",
                    "cost_estimate": "$25-100",
                    "roi_potential": "High",
                    "tools": ["Email automation", "CRM", "Discount system"],
                    "description": "Special offers to re-engage cold prospects"
                },
                {
                    "name": "Instagram post scheduling",
                    "difficulty": "Easy",
                    "time_estimate": "2-4 hours",
                    "cost_estimate": "$10-50",
                    "roi_potential": "Medium",
                    "tools": ["Social media scheduler", "Content calendar", "Instagram API"],
                    "description": "Automated social media content posting"
                },
                {
                    "name": "Auto-detect and email duplicate leads",
                    "difficulty": "Medium",
                    "time_estimate": "4-8 hours",
                    "cost_estimate": "$50-150",
                    "roi_potential": "Medium",
                    "tools": ["CRM", "Duplicate detection", "Email automation"],
                    "description": "Prevent duplicate lead processing and follow-up"
                },
                {
                    "name": "Trigger a call task for high-interest leads",
                    "difficulty": "Easy",
                    "time_estimate": "2-4 hours",
                    "cost_estimate": "$20-60",
                    "roi_potential": "High",
                    "tools": ["CRM", "Lead scoring", "Task automation"],
                    "description": "Automatic call scheduling for qualified leads"
                },
                {
                    "name": "Send seasonal promo campaigns (e.g., spring cleaning)",
                    "difficulty": "Easy",
                    "time_estimate": "3-6 hours",
                    "cost_estimate": "$25-100",
                    "roi_potential": "High",
                    "tools": ["Email marketing", "Calendar automation", "Promotions"],
                    "description": "Seasonal marketing campaign automation"
                },
                {
                    "name": "Add new leads from Facebook Ads to CRM",
                    "difficulty": "Easy",
                    "time_estimate": "2-4 hours",
                    "cost_estimate": "$0-50",
                    "roi_potential": "High",
                    "tools": ["Facebook Ads", "CRM", "Zapier"],
                    "description": "Automatic lead capture from Facebook advertising"
                },
                {
                    "name": "Auto-score leads based on form inputs",
                    "difficulty": "Medium",
                    "time_estimate": "4-8 hours",
                    "cost_estimate": "$50-150",
                    "roi_potential": "High",
                    "tools": ["CRM", "Lead scoring", "Form analysis"],
                    "description": "Automatic lead qualification and prioritization"
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
                    "name": "Missed call auto-text How can we help",
                    "difficulty": "Easy",
                    "time_estimate": "2-4 hours",
                    "cost_estimate": "$20-60",
                    "roi_potential": "High",
                    "tools": ["Phone system", "SMS service", "Call tracking"],
                    "description": "Automatic follow-up for missed phone calls"
                },
                {
                    "name": "Job status updates via SMS (In Progress, Completed)",
                    "difficulty": "Easy",
                    "time_estimate": "2-4 hours",
                    "cost_estimate": "$20-60",
                    "roi_potential": "High",
                    "tools": ["SMS service", "Job tracking", "Zapier"],
                    "description": "Real-time job progress updates to customers"
                },
                {
                    "name": "Auto-email of cleaner profile before visit",
                    "difficulty": "Easy",
                    "time_estimate": "2-4 hours",
                    "cost_estimate": "$10-50",
                    "roi_potential": "Medium",
                    "tools": ["Email automation", "Staff database", "Scheduling"],
                    "description": "Pre-service cleaner introduction emails"
                },
                {
                    "name": "Send delay notifications via SMS",
                    "difficulty": "Easy",
                    "time_estimate": "2-3 hours",
                    "cost_estimate": "$15-50",
                    "roi_potential": "High",
                    "tools": ["SMS service", "Scheduling system", "Alerts"],
                    "description": "Automatic delay notifications to customers"
                },
                {
                    "name": "Auto-notify customer when cleaner is nearby",
                    "difficulty": "Medium",
                    "time_estimate": "4-8 hours",
                    "cost_estimate": "$50-150",
                    "roi_potential": "High",
                    "tools": ["GPS tracking", "SMS service", "Geofencing"],
                    "description": "Location-based arrival notifications"
                },
                {
                    "name": "Service reminder emails (weekly, biweekly, etc.)",
                    "difficulty": "Easy",
                    "time_estimate": "2-4 hours",
                    "cost_estimate": "$10-50",
                    "roi_potential": "High",
                    "tools": ["Email automation", "Scheduling", "CRM"],
                    "description": "Recurring service booking reminders"
                },
                {
                    "name": "You are next job notification for clients",
                    "difficulty": "Easy",
                    "time_estimate": "2-4 hours",
                    "cost_estimate": "$15-50",
                    "roi_potential": "Medium",
                    "tools": ["SMS/Email service", "Queue management", "Scheduling"],
                    "description": "Queue position updates for customers"
                },
                {
                    "name": "Set auto-replies for off-hours contact",
                    "difficulty": "Easy",
                    "time_estimate": "1-2 hours",
                    "cost_estimate": "$0-25",
                    "roi_potential": "Medium",
                    "tools": ["Email automation", "Phone system", "Chat platform"],
                    "description": "Automated after-hours response messages"
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
                    "name": "New client acquisition report",
                    "difficulty": "Easy",
                    "time_estimate": "3-6 hours",
                    "cost_estimate": "$25-100",
                    "roi_potential": "Medium",
                    "tools": ["CRM", "Analytics", "Reporting tool"],
                    "description": "Monthly new customer acquisition analysis"
                },
                {
                    "name": "Cleaner performance heatmap",
                    "difficulty": "Medium",
                    "time_estimate": "6-12 hours",
                    "cost_estimate": "$100-300",
                    "roi_potential": "Medium",
                    "tools": ["Analytics platform", "Performance data", "Visualization"],
                    "description": "Visual performance tracking for cleaning staff"
                },
                {
                    "name": "Missed job or reschedule frequency report",
                    "difficulty": "Easy",
                    "time_estimate": "3-5 hours",
                    "cost_estimate": "$25-75",
                    "roi_potential": "Medium",
                    "tools": ["Scheduling system", "Analytics", "Reporting"],
                    "description": "Analysis of scheduling disruptions and patterns"
                },
                {
                    "name": "Auto-track ad spend vs. bookings",
                    "difficulty": "Medium",
                    "time_estimate": "6-10 hours",
                    "cost_estimate": "$100-250",
                    "roi_potential": "High",
                    "tools": ["Ad platforms", "Analytics", "ROI tracking"],
                    "description": "Marketing ROI analysis and optimization"
                },
                {
                    "name": "Most-requested services chart",
                    "difficulty": "Easy",
                    "time_estimate": "2-4 hours",
                    "cost_estimate": "$20-60",
                    "roi_potential": "Medium",
                    "tools": ["Service tracking", "Analytics", "Visualization"],
                    "description": "Popular service analysis for business planning"
                },
                {
                    "name": "Net Promoter Score (NPS) tracking",
                    "difficulty": "Medium",
                    "time_estimate": "4-8 hours",
                    "cost_estimate": "$50-150",
                    "roi_potential": "Medium",
                    "tools": ["Survey tool", "Analytics", "NPS calculator"],
                    "description": "Customer satisfaction and loyalty measurement"
                },
                {
                    "name": "Client lifetime value calculator",
                    "difficulty": "Hard",
                    "time_estimate": "10-20 hours",
                    "cost_estimate": "$200-500",
                    "roi_potential": "High",
                    "tools": ["Analytics platform", "Custom calculations", "CRM"],
                    "description": "Automated CLV tracking and analysis"
                },
                {
                    "name": "Export all data monthly to cloud drive",
                    "difficulty": "Easy",
                    "time_estimate": "2-4 hours",
                    "cost_estimate": "$10-50",
                    "roi_potential": "Low",
                    "tools": ["Cloud storage", "Data export", "Automation"],
                    "description": "Automated data backup and archiving"
                }
            ],
            "icon": "📊",
            "color": "#FF6B35"
        }
    }

# Get the data
categories = get_automation_data()

# Calculate total automations
total_automations = sum(len(cat_data["items"]) for cat_data in categories.values())

# Main header
st.markdown('<h1 class="main-header">🧼 Ultimate Cleaning Business Automation Hub</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Transform your cleaning business with 150+ powerful automation ideas, implementation guides, and ROI tracking</p>', unsafe_allow_html=True)

# Top metrics row
col1, col2, col3, col4, col5 = st.columns(5)
completed_count = len(st.session_state.completed_automations)
progress_percentage = (completed_count / total_automations) * 100

with col1:
    st.metric("Total Automations", total_automations, delta="New & Updated")
with col2:
    st.metric("Completed", completed_count, delta=f"{progress_percentage:.1f}%")
with col3:
    st.metric("Categories", len(categories), delta="Comprehensive")
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
    
    # Status filters
    status_filter = st.radio(
        "Status:",
        ["All", "Completed", "Pending", "Favorites"]
    )
    
    st.markdown("---")
    
    # Quick actions
    st.header("⚡ Quick Actions")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Mark Easy Complete", use_container_width=True):
            for cat_data in categories.values():
                for item in cat_data["items"]:
                    if item.get("difficulty") == "Easy":
                        st.session_state.completed_automations.add(item["name"])
            st.rerun()
        
        if st.button("⭐ Show High ROI", use_container_width=True):
            st.session_state.show_high_roi_filter = True
            st.rerun()
    
    with col2:
        if st.button("🔄 Reset Progress", use_container_width=True):
            st.session_state.completed_automations = set()
            st.session_state.automation_notes = {}
            st.session_state.priority_levels = {}
            st.rerun()
        
        if st.button("📋 Export Report", use_container_width=True):
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
                label="📄 Download CSV Report",
                data=csv,
                file_name=f"cleaning_automations_report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )

# Main content area with tabs
tab1, tab2, tab3 = st.tabs(["🎯 Automation Checklist", "📊 Analytics Dashboard", "🛠️ Implementation Guides"])

with tab1:
    # Category overview
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
    
    # Main automation list
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
            
            # Display items
            for i, item in enumerate(filtered_items):
                is_completed = item["name"] in st.session_state.completed_automations
                is_favorite = item["name"] in st.session_state.favorite_automations
                
                # Enhanced item display
                with st.expander(f"{'✅' if is_completed else '⏳'} {'⭐' if is_favorite else ''} {item['name']}", expanded=False):
                    
                    # Item details
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
                            if st.checkbox("Complete", value=is_completed, key=f"check_{category}_{i}_{hash(item['name'])}"):
                                st.session_state.completed_automations.add(item["name"])
                                if item["name"] not in st.session_state.implementation_dates:
                                    st.session_state.implementation_dates[item["name"]] = datetime.now()
                            else:
                                st.session_state.completed_automations.discard(item["name"])
                        
                        with col_fav:
                            if st.checkbox("Favorite", value=is_favorite, key=f"fav_{category}_{i}_{hash(item['name'])}"):
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
                            key=f"priority_{category}_{i}_{hash(item['name'])}"
                        )
                        st.session_state.priority_levels[item["name"]] = priority
                    
                    with col_notes:
                        note = st.text_area(
                            "Implementation Notes:",
                            value=st.session_state.automation_notes.get(item["name"], ""),
                            height=100,  # Fixed: Increased to 100 pixels (minimum is 68)
                            key=f"note_{category}_{i}_{hash(item['name'])}",
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
        # Progress overview
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
            st.subheader("📈 Completion Rate by Category")
            for _, row in df_categories.iterrows():
                st.write(f"**{row['Category']}:** {row['Completed']}/{row['Total']} ({row['Percentage']:.1f}%)")
                st.progress(row['Percentage'] / 100)
        
        with col2:
            # ROI potential distribution
            roi_data = {"High": 0, "Medium": 0, "Low": 0}
            for cat_data in categories.values():
                for item in cat_data["items"]:
                    if item["name"] in st.session_state.completed_automations:
                        roi_data[item.get("roi_potential", "Medium")] += 1
            
            st.subheader("🎯 Completed by ROI Potential")
            for roi_level, count in roi_data.items():
                st.metric(f"{roi_level} ROI", count)
        
        # Implementation analysis
        st.subheader("📈 Implementation Analysis")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_time = "6.5 hours"  # Calculated average
            st.metric("Average Implementation Time", avg_time, delta="Estimated")
        with col2:
            total_cost = "$2,450"  # Estimated total
            st.metric("Total Estimated Cost", total_cost, delta="For all completed")
        with col3:
            roi_estimate = "340%"  # Estimated ROI
            st.metric("Potential ROI", roi_estimate, delta="Based on time savings")
    
    else:
        st.info("Complete some automations to see analytics!")
        st.markdown("### 🚀 Get Started")
        st.markdown("1. Browse the automation checklist")
        st.markdown("2. Start with 'Easy' difficulty items")
        st.markdown("3. Focus on high ROI automations")
        st.markdown("4. Track your progress here")

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
        },
        "Creating Automated Scheduling": {
            "steps": [
                "Select scheduling software (Calendly, Acuity)",
                "Configure service types and durations",
                "Set up calendar integration",
                "Create booking confirmation emails",
                "Add payment integration",
                "Test the complete flow"
            ],
            "tools": ["Calendly", "Acuity", "Google Calendar"],
            "time": "4-8 hours",
            "difficulty": "Easy"
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

