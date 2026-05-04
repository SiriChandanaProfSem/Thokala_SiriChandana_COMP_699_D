import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import datetime
import hashlib
import json
import time
import random
from collections import defaultdict

st.set_page_config(
    page_title="DNaaS - Deadline Negotiation as a Service",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600;700;800&display=swap');

*, body, .stApp {
    font-family: 'Open Sans', sans-serif !important;
}

.stApp {
    background: #f5f5f5;
}

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

section[data-testid="stSidebar"] {
    display: none !important;
    width: 0 !important;
}

header[data-testid="stHeader"] {
    background: transparent;
    height: 0;
}

.main-topnav {
    background: #003366;
    padding: 0 48px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 60px;
    position: sticky;
    top: 0;
    z-index: 999;
    box-shadow: 0 2px 8px rgba(0,0,0,0.18);
}

.nav-brand {
    font-size: 22px;
    font-weight: 800;
    color: #fff;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.nav-brand span {
    color: #e8b931;
}

.nav-links {
    display: flex;
    gap: 36px;
    align-items: center;
}

.nav-link {
    color: #cce0ff;
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    cursor: pointer;
    padding: 6px 0;
    border-bottom: 2px solid transparent;
    transition: all 0.2s;
}

.nav-link:hover {
    color: #fff;
    border-bottom: 2px solid #e8b931;
}

.nav-user-pill {
    background: #e8b931;
    color: #003366;
    font-weight: 700;
    font-size: 12px;
    padding: 7px 18px;
    border-radius: 20px;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.hero-banner {
    background: linear-gradient(135deg, #003366 0%, #0055b3 60%, #0073e6 100%);
    padding: 56px 60px 44px 60px;
    position: relative;
    overflow: hidden;
}

.hero-banner::before {
    content: '';
    position: absolute;
    right: -60px;
    top: -60px;
    width: 420px;
    height: 420px;
    background: rgba(232,185,49,0.08);
    border-radius: 50%;
}

.hero-banner::after {
    content: '';
    position: absolute;
    right: 80px;
    bottom: -100px;
    width: 280px;
    height: 280px;
    background: rgba(255,255,255,0.05);
    border-radius: 50%;
}

.hero-title {
    font-size: 36px;
    font-weight: 800;
    color: #fff;
    margin: 0 0 10px 0;
    letter-spacing: 0.5px;
}

.hero-title span {
    color: #e8b931;
}

.hero-sub {
    font-size: 16px;
    color: #a8ccf0;
    font-weight: 400;
    margin: 0 0 28px 0;
}

.metric-strip {
    display: flex;
    gap: 28px;
    flex-wrap: wrap;
}

.metric-chip {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 10px;
    padding: 14px 24px;
    text-align: center;
    backdrop-filter: blur(6px);
    min-width: 130px;
}

.metric-chip .val {
    font-size: 28px;
    font-weight: 800;
    color: #e8b931;
    line-height: 1;
}

.metric-chip .lbl {
    font-size: 11px;
    color: #cce0ff;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 4px;
}

.tab-bar {
    background: #fff;
    border-bottom: 3px solid #003366;
    padding: 0 48px;
    display: flex;
    gap: 0;
    overflow-x: auto;
}

.tab-item {
    padding: 14px 28px;
    font-size: 13px;
    font-weight: 700;
    color: #555;
    text-transform: uppercase;
    letter-spacing: 1px;
    cursor: pointer;
    border-bottom: 3px solid transparent;
    margin-bottom: -3px;
    white-space: nowrap;
    transition: all 0.2s;
}

.tab-item.active {
    color: #003366;
    border-bottom: 3px solid #e8b931;
}

.tab-item:hover {
    color: #003366;
}

.page-body {
    padding: 36px 48px;
    background: #f5f5f5;
    min-height: 80vh;
}

.card {
    background: #fff;
    border-radius: 10px;
    padding: 28px 28px 24px 28px;
    margin-bottom: 24px;
    box-shadow: 0 2px 12px rgba(0,51,102,0.07);
    border: 1px solid #e8eef6;
}

.card-title {
    font-size: 16px;
    font-weight: 700;
    color: #003366;
    letter-spacing: 0.3px;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 10px;
    border-bottom: 2px solid #e8eef6;
    padding-bottom: 12px;
}

.card-title .accent-bar {
    width: 4px;
    height: 20px;
    background: #e8b931;
    border-radius: 2px;
    display: inline-block;
}

.stat-card {
    background: linear-gradient(135deg, #003366 0%, #0055b3 100%);
    color: #fff;
    border-radius: 10px;
    padding: 24px 22px;
    text-align: center;
    box-shadow: 0 4px 16px rgba(0,51,102,0.18);
}

.stat-card.gold {
    background: linear-gradient(135deg, #c9920a 0%, #e8b931 100%);
    color: #003366;
}

.stat-card.green {
    background: linear-gradient(135deg, #0d7230 0%, #28a745 100%);
}

.stat-card.red {
    background: linear-gradient(135deg, #9b1c1c 0%, #dc3545 100%);
}

.stat-card .s-val {
    font-size: 38px;
    font-weight: 800;
    line-height: 1;
}

.stat-card .s-lbl {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-top: 6px;
    opacity: 0.85;
}

.task-row {
    display: flex;
    align-items: center;
    padding: 13px 16px;
    border-radius: 8px;
    margin-bottom: 8px;
    background: #f8fafd;
    border-left: 4px solid #0055b3;
    transition: background 0.15s;
}

.task-row.conflict {
    border-left: 4px solid #dc3545;
    background: #fff5f5;
}

.task-row.approved {
    border-left: 4px solid #28a745;
    background: #f0fff4;
}

.task-row.pending {
    border-left: 4px solid #e8b931;
    background: #fffdf0;
}

.badge {
    display: inline-block;
    padding: 3px 11px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

.badge-blue { background: #e0ecff; color: #003366; }
.badge-red { background: #ffe0e0; color: #9b1c1c; }
.badge-green { background: #e0fff0; color: #0d7230; }
.badge-gold { background: #fff5d0; color: #7a5800; }
.badge-gray { background: #ececec; color: #555; }

.progress-bar-outer {
    background: #e0e8f0;
    border-radius: 6px;
    height: 10px;
    overflow: hidden;
    margin-top: 6px;
}

.progress-bar-inner {
    height: 10px;
    border-radius: 6px;
    background: linear-gradient(90deg, #003366, #0073e6);
    transition: width 0.5s;
}

.progress-bar-inner.warn {
    background: linear-gradient(90deg, #c9920a, #e8b931);
}

.progress-bar-inner.danger {
    background: linear-gradient(90deg, #9b1c1c, #dc3545);
}

.timeline-item {
    display: flex;
    gap: 16px;
    align-items: flex-start;
    padding: 12px 0;
    border-bottom: 1px solid #f0f0f0;
}

.timeline-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: #003366;
    margin-top: 4px;
    flex-shrink: 0;
    border: 2px solid #0055b3;
}

.timeline-dot.gold { background: #e8b931; border-color: #c9920a; }
.timeline-dot.green { background: #28a745; border-color: #0d7230; }
.timeline-dot.red { background: #dc3545; border-color: #9b1c1c; }

.auth-wrapper {
    min-height: 100vh;
    background: linear-gradient(135deg, #001f44 0%, #003366 50%, #004d99 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 40px 20px;
}

.auth-card {
    background: #fff;
    border-radius: 16px;
    padding: 48px 44px;
    width: 100%;
    max-width: 440px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.25);
}

.auth-logo {
    text-align: center;
    margin-bottom: 32px;
}

.auth-logo .brand {
    font-size: 32px;
    font-weight: 800;
    color: #003366;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.auth-logo .brand span {
    color: #e8b931;
}

.auth-logo .tagline {
    font-size: 12px;
    color: #888;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 4px;
}

.auth-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, #003366, transparent);
    margin: 20px 0;
    opacity: 0.15;
}

.stTextInput > div > div > input,
.stSelectbox > div > div > div,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input,
.stDateInput > div > div > input {
    border: 1.5px solid #d0d8e8 !important;
    border-radius: 7px !important;
    font-family: 'Open Sans', sans-serif !important;
    font-size: 14px !important;
    color: #222 !important;
    background: #f9fafc !important;
    transition: border 0.2s !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border: 1.5px solid #003366 !important;
    background: #fff !important;
    box-shadow: 0 0 0 3px rgba(0,51,102,0.08) !important;
}

.stButton > button {
    background: #003366 !important;
    color: #fff !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 7px !important;
    padding: 10px 28px !important;
    width: 100% !important;
    transition: all 0.2s !important;
    font-family: 'Open Sans', sans-serif !important;
    box-shadow: 0 4px 12px rgba(0,51,102,0.15) !important;
}

.stButton > button:hover {
    background: #0055b3 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 18px rgba(0,51,102,0.22) !important;
}

.stButton > button[kind="secondary"] {
    background: #e8b931 !important;
    color: #003366 !important;
}

.stSelectbox label, .stTextInput label, .stDateInput label,
.stNumberInput label, .stTextArea label, .stMultiSelect label {
    font-weight: 600 !important;
    font-size: 13px !important;
    color: #003366 !important;
    letter-spacing: 0.3px !important;
}

div[data-testid="metric-container"] {
    background: #fff;
    border: 1px solid #e0e8f6;
    border-radius: 10px;
    padding: 16px 18px !important;
    box-shadow: 0 2px 8px rgba(0,51,102,0.06);
}

div[data-testid="metric-container"] label {
    color: #555 !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    font-weight: 700 !important;
}

div[data-testid="metric-container"] div[data-testid="metric-value"] {
    color: #003366 !important;
    font-size: 28px !important;
    font-weight: 800 !important;
}

.stDataFrame {
    border-radius: 8px !important;
    overflow: hidden !important;
}

.stAlert {
    border-radius: 8px !important;
}

.risk-indicator {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
}

.risk-low { background: #e0fff0; color: #0d7230; }
.risk-medium { background: #fff5d0; color: #7a5800; }
.risk-high { background: #ffe0e0; color: #9b1c1c; }

.footer-bar {
    background: #001f44;
    color: #7a9abf;
    padding: 22px 48px;
    text-align: center;
    font-size: 12px;
    letter-spacing: 0.5px;
    margin-top: 48px;
}

.footer-bar strong {
    color: #e8b931;
}

.stTabs [data-baseweb="tab-list"] {
    background: #f0f4fa !important;
    border-radius: 10px 10px 0 0 !important;
    padding: 6px 6px 0 6px !important;
    gap: 4px !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 8px 8px 0 0 !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    color: #555 !important;
    letter-spacing: 0.5px !important;
    padding: 10px 20px !important;
    border: none !important;
}

.stTabs [aria-selected="true"] {
    background: #003366 !important;
    color: #fff !important;
}

.stTabs [data-baseweb="tab-panel"] {
    padding: 0 !important;
}

.notification-item {
    padding: 12px 16px;
    border-radius: 8px;
    margin-bottom: 8px;
    border-left: 4px solid #003366;
    background: #f0f5ff;
    font-size: 13px;
}

.notification-item.warning {
    border-left: 4px solid #e8b931;
    background: #fffbf0;
}

.notification-item.success {
    border-left: 4px solid #28a745;
    background: #f0fff8;
}

.notification-item.danger {
    border-left: 4px solid #dc3545;
    background: #fff5f5;
}

.gauge-container {
    text-align: center;
    padding: 10px;
}

h1, h2, h3, h4, h5 {
    font-family: 'Open Sans', sans-serif !important;
    color: #003366 !important;
}

.stExpander {
    border: 1px solid #e0e8f6 !important;
    border-radius: 8px !important;
}

.stExpander header {
    font-weight: 600 !important;
    color: #003366 !important;
    font-size: 14px !important;
}
</style>
""", unsafe_allow_html=True)

if "users_db" not in st.session_state:
    st.session_state.users_db = {
        "admin@dnaas.com": {
            "name": "System Administrator",
            "password": hashlib.sha256("Admin@2026".encode()).hexdigest(),
            "role": "Administrator",
            "weekly_hours": 40,
            "unavailable_dates": [],
            "max_workload": 40
        },
        "manager@dnaas.com": {
            "name": "Alex Morgan",
            "password": hashlib.sha256("Manager@2026".encode()).hexdigest(),
            "role": "Manager",
            "weekly_hours": 40,
            "unavailable_dates": [],
            "max_workload": 40
        },
        "contributor@dnaas.com": {
            "name": "Jordan Lee",
            "password": hashlib.sha256("Contrib@2026".encode()).hexdigest(),
            "role": "Contributor",
            "weekly_hours": 32,
            "unavailable_dates": [],
            "max_workload": 35
        },
        "client@dnaas.com": {
            "name": "Taylor Brooks",
            "password": hashlib.sha256("Client@2026".encode()).hexdigest(),
            "role": "Client",
            "weekly_hours": 40,
            "unavailable_dates": [],
            "max_workload": 40
        }
    }

if "projects_db" not in st.session_state:
    today = datetime.date.today()
    st.session_state.projects_db = {
        "PRJ-001": {
            "name": "Website Redesign Initiative",
            "description": "Complete overhaul of company digital presence with modern UX",
            "deadline": str(today + datetime.timedelta(days=45)),
            "priority": "High",
            "negotiable": True,
            "status": "Active",
            "created_by": "manager@dnaas.com",
            "contributors": ["contributor@dnaas.com"],
            "created_at": str(today - datetime.timedelta(days=10))
        },
        "PRJ-002": {
            "name": "Data Analytics Platform",
            "description": "Build real-time analytics dashboard for executive reporting",
            "deadline": str(today + datetime.timedelta(days=30)),
            "priority": "Critical",
            "negotiable": False,
            "status": "Active",
            "created_by": "manager@dnaas.com",
            "contributors": ["contributor@dnaas.com"],
            "created_at": str(today - datetime.timedelta(days=5))
        },
        "PRJ-003": {
            "name": "Mobile App Development",
            "description": "Cross-platform mobile application for customer engagement",
            "deadline": str(today + datetime.timedelta(days=60)),
            "priority": "Medium",
            "negotiable": True,
            "status": "Planning",
            "created_by": "manager@dnaas.com",
            "contributors": [],
            "created_at": str(today - datetime.timedelta(days=2))
        }
    }

if "tasks_db" not in st.session_state:
    today = datetime.date.today()
    st.session_state.tasks_db = {
        "TSK-001": {
            "name": "UI Wireframe Design",
            "project_id": "PRJ-001",
            "assigned_to": "contributor@dnaas.com",
            "effort_hours": 24,
            "deadline": str(today + datetime.timedelta(days=10)),
            "priority": "High",
            "status": "In Progress",
            "fixed_deadline": False,
            "created_by": "contributor@dnaas.com",
            "created_at": str(today - datetime.timedelta(days=8))
        },
        "TSK-002": {
            "name": "Backend API Development",
            "project_id": "PRJ-001",
            "assigned_to": "contributor@dnaas.com",
            "effort_hours": 40,
            "deadline": str(today + datetime.timedelta(days=20)),
            "priority": "Critical",
            "status": "Pending",
            "fixed_deadline": True,
            "created_by": "contributor@dnaas.com",
            "created_at": str(today - datetime.timedelta(days=7))
        },
        "TSK-003": {
            "name": "Database Schema Design",
            "project_id": "PRJ-002",
            "assigned_to": "contributor@dnaas.com",
            "effort_hours": 18,
            "deadline": str(today + datetime.timedelta(days=8)),
            "priority": "High",
            "status": "In Progress",
            "fixed_deadline": False,
            "created_by": "contributor@dnaas.com",
            "created_at": str(today - datetime.timedelta(days=4))
        },
        "TSK-004": {
            "name": "Dashboard Visualization Module",
            "project_id": "PRJ-002",
            "assigned_to": "contributor@dnaas.com",
            "effort_hours": 30,
            "deadline": str(today + datetime.timedelta(days=25)),
            "priority": "Medium",
            "status": "Pending",
            "fixed_deadline": False,
            "created_by": "contributor@dnaas.com",
            "created_at": str(today - datetime.timedelta(days=3))
        },
        "TSK-005": {
            "name": "User Authentication System",
            "project_id": "PRJ-001",
            "assigned_to": "contributor@dnaas.com",
            "effort_hours": 20,
            "deadline": str(today + datetime.timedelta(days=15)),
            "priority": "Critical",
            "status": "Pending",
            "fixed_deadline": True,
            "created_by": "manager@dnaas.com",
            "created_at": str(today - datetime.timedelta(days=6))
        }
    }

if "negotiations_db" not in st.session_state:
    today = datetime.date.today()
    st.session_state.negotiations_db = {
        "NEG-001": {
            "task_id": "TSK-001",
            "status": "Pending",
            "created_by": "manager@dnaas.com",
            "created_at": str(today - datetime.timedelta(days=2)),
            "proposals": [
                {
                    "proposed_deadline": str(today + datetime.timedelta(days=14)),
                    "justification": "Current deadline infeasible due to 24h effort in 10 days with 32h/week availability.",
                    "proposed_by": "manager@dnaas.com",
                    "status": "Pending",
                    "timestamp": str(today - datetime.timedelta(days=2))
                }
            ]
        },
        "NEG-002": {
            "task_id": "TSK-003",
            "status": "Approved",
            "created_by": "manager@dnaas.com",
            "created_at": str(today - datetime.timedelta(days=5)),
            "proposals": [
                {
                    "proposed_deadline": str(today + datetime.timedelta(days=12)),
                    "justification": "Conflict detected with TSK-001. Redistributed to allow parallel work.",
                    "proposed_by": "manager@dnaas.com",
                    "status": "Approved",
                    "timestamp": str(today - datetime.timedelta(days=4))
                }
            ]
        }
    }

if "audit_logs" not in st.session_state:
    today = datetime.date.today()
    st.session_state.audit_logs = [
        {"action": "Project PRJ-001 created", "user": "manager@dnaas.com", "timestamp": str(today - datetime.timedelta(days=10)), "category": "Project"},
        {"action": "Task TSK-001 assigned to contributor@dnaas.com", "user": "manager@dnaas.com", "timestamp": str(today - datetime.timedelta(days=8)), "category": "Task"},
        {"action": "Negotiation NEG-001 initiated for TSK-001", "user": "manager@dnaas.com", "timestamp": str(today - datetime.timedelta(days=2)), "category": "Negotiation"},
        {"action": "Proposal approved for NEG-002 (TSK-003)", "user": "manager@dnaas.com", "timestamp": str(today - datetime.timedelta(days=4)), "category": "Approval"},
        {"action": "Project PRJ-002 created", "user": "manager@dnaas.com", "timestamp": str(today - datetime.timedelta(days=5)), "category": "Project"},
        {"action": "Task TSK-003 created in PRJ-002", "user": "contributor@dnaas.com", "timestamp": str(today - datetime.timedelta(days=4)), "category": "Task"},
    ]

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"
if "notifications" not in st.session_state:
    st.session_state.notifications = []

def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

def add_audit(action, category="General"):
    st.session_state.audit_logs.append({
        "action": action,
        "user": st.session_state.current_user,
        "timestamp": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")),
        "category": category
    })

def get_user_tasks(email):
    return {k: v for k, v in st.session_state.tasks_db.items() if v["assigned_to"] == email}

def calculate_workload(email, days=30):
    tasks = get_user_tasks(email)
    total_effort = sum(t["effort_hours"] for t in tasks.values())
    user = st.session_state.users_db.get(email, {})
    available = user.get("weekly_hours", 40) * (days / 7)
    return total_effort, available, (total_effort / available * 100) if available > 0 else 0

def detect_conflicts(email):
    tasks = get_user_tasks(email)
    conflicts = []
    today = datetime.date.today()
    user = st.session_state.users_db.get(email, {})
    weekly = user.get("weekly_hours", 40)
    for tid, task in tasks.items():
        dl = datetime.date.fromisoformat(task["deadline"])
        days_left = max((dl - today).days, 1)
        weeks = days_left / 7
        hours_avail = weeks * weekly
        if task["effort_hours"] > hours_avail:
            overload = ((task["effort_hours"] - hours_avail) / hours_avail * 100) if hours_avail > 0 else 100
            conflicts.append({
                "task_id": tid,
                "task_name": task["name"],
                "effort": task["effort_hours"],
                "available": round(hours_avail, 1),
                "overload_pct": round(overload, 1),
                "deadline": task["deadline"],
                "priority": task["priority"]
            })
    return conflicts

def generate_proposal_deadline(task_id):
    task = st.session_state.tasks_db.get(task_id)
    if not task:
        return None
    today = datetime.date.today()
    email = task["assigned_to"]
    user = st.session_state.users_db.get(email, {})
    weekly = user.get("weekly_hours", 40)
    weeks_needed = task["effort_hours"] / weekly
    proposed = today + datetime.timedelta(days=int(weeks_needed * 7) + 5)
    return str(proposed)

def render_login():
    st.markdown('<div class="auth-wrapper">', unsafe_allow_html=True)
    col_center = st.columns([1, 1.2, 1])[1]
    with col_center:
        st.markdown("""
        <div class="auth-card">
            <div class="auth-logo">
                <div class="brand">DN<span>aaS</span></div>
                <div class="tagline">Deadline Negotiation as a Service</div>
            </div>
            <div class="auth-divider"></div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.auth_mode == "login":
            st.markdown("### Sign In to Your Account")
            with st.form("login_form", clear_on_submit=False):
                email = st.text_input("Email Address", placeholder="Enter your email")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                submitted = st.form_submit_button("Sign In")
                if submitted:
                    if email in st.session_state.users_db:
                        user = st.session_state.users_db[email]
                        if user["password"] == hash_password(password):
                            st.session_state.logged_in = True
                            st.session_state.current_user = email
                            st.session_state.current_page = "Dashboard"
                            add_audit("User signed in", "Auth")
                            st.rerun()
                        else:
                            st.error("Invalid credentials. Please check your password.")
                    else:
                        st.error("Account not found. Please register or check your email.")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Create New Account"):
                st.session_state.auth_mode = "register"
                st.rerun()

        else:
            st.markdown("### Create Your Account")
            with st.form("register_form", clear_on_submit=False):
                reg_name = st.text_input("Full Name", placeholder="Enter your full name")
                reg_email = st.text_input("Email Address", placeholder="Enter your email")
                reg_role = st.selectbox("Select Role", ["Contributor", "Manager", "Client"])
                reg_weekly = st.number_input("Weekly Available Hours", min_value=1, max_value=80, value=40)
                reg_password = st.text_input("Password", type="password", placeholder="Create a strong password")
                reg_confirm = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
                reg_submit = st.form_submit_button("Register Account")
                if reg_submit:
                    if not reg_name or not reg_email or not reg_password:
                        st.error("All fields are required.")
                    elif reg_password != reg_confirm:
                        st.error("Passwords do not match.")
                    elif reg_email in st.session_state.users_db:
                        st.error("Email already registered. Please sign in.")
                    elif len(reg_password) < 6:
                        st.error("Password must be at least 6 characters.")
                    else:
                        st.session_state.users_db[reg_email] = {
                            "name": reg_name,
                            "password": hash_password(reg_password),
                            "role": reg_role,
                            "weekly_hours": reg_weekly,
                            "unavailable_dates": [],
                            "max_workload": reg_weekly
                        }
                        st.success("Account created! Please sign in.")
                        st.session_state.auth_mode = "login"
                        time.sleep(1)
                        st.rerun()
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Back to Sign In"):
                st.session_state.auth_mode = "login"
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def render_topnav():
    user = st.session_state.users_db[st.session_state.current_user]
    role = user["role"]
    name = user["name"].split()[0]
    nav_pages = ["Dashboard", "Projects", "Tasks", "Workload Analysis", "Negotiations", "Reports", "Audit Logs"]
    if role == "Administrator":
        nav_pages.append("User Management")

    st.markdown(f"""
    <div class="main-topnav">
        <div class="nav-brand">DN<span>aaS</span></div>
        <div class="nav-links">
            {"".join(f'<div class="nav-link">{p}</div>' for p in nav_pages)}
        </div>
        <div class="nav-user-pill">{name} &bull; {role}</div>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(len(nav_pages) + 1)
    for i, pg in enumerate(nav_pages):
        with cols[i]:
            if st.button(pg, key=f"nav_{pg}", use_container_width=True):
                st.session_state.current_page = pg
                st.rerun()
    with cols[-1]:
        if st.button("Sign Out", key="signout_btn", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.current_page = "Dashboard"
            st.rerun()

def render_dashboard():
    user = st.session_state.users_db[st.session_state.current_user]
    role = user["role"]
    name = user["name"]
    today = datetime.date.today()

    total_projects = len(st.session_state.projects_db)
    total_tasks = len(st.session_state.tasks_db)
    active_negs = len([n for n in st.session_state.negotiations_db.values() if n["status"] == "Pending"])
    my_tasks = get_user_tasks(st.session_state.current_user)

    st.markdown(f"""
    <div class="hero-banner">
        <div class="hero-title">Welcome back, <span>{name.split()[0]}</span></div>
        <div class="hero-sub">Your project control center &mdash; {today.strftime("%A, %B %d, %Y")} &bull; {role}</div>
        <div class="metric-strip">
            <div class="metric-chip"><div class="val">{total_projects}</div><div class="lbl">Projects</div></div>
            <div class="metric-chip"><div class="val">{total_tasks}</div><div class="lbl">Total Tasks</div></div>
            <div class="metric-chip"><div class="val">{len(my_tasks)}</div><div class="lbl">My Tasks</div></div>
            <div class="metric-chip"><div class="val">{active_negs}</div><div class="lbl">Active Negotiations</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="page-body">', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        active_proj = len([p for p in st.session_state.projects_db.values() if p["status"] == "Active"])
        st.markdown(f'<div class="stat-card"><div class="s-val">{active_proj}</div><div class="s-lbl">Active Projects</div></div>', unsafe_allow_html=True)
    with c2:
        in_progress = len([t for t in st.session_state.tasks_db.values() if t["status"] == "In Progress"])
        st.markdown(f'<div class="stat-card gold"><div class="s-val">{in_progress}</div><div class="s-lbl">In Progress</div></div>', unsafe_allow_html=True)
    with c3:
        conflicts = detect_conflicts(st.session_state.current_user)
        st.markdown(f'<div class="stat-card red"><div class="s-val">{len(conflicts)}</div><div class="s-lbl">Conflicts Detected</div></div>', unsafe_allow_html=True)
    with c4:
        approved_negs = len([n for n in st.session_state.negotiations_db.values() if n["status"] == "Approved"])
        st.markdown(f'<div class="stat-card green"><div class="s-val">{approved_negs}</div><div class="s-lbl">Resolved</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><span class="accent-bar"></span>Project Timeline Overview</div>', unsafe_allow_html=True)
        proj_names = []
        starts = []
        ends = []
        colors = []
        color_map = {"Critical": "#dc3545", "High": "#e8b931", "Medium": "#0055b3", "Low": "#28a745"}
        for pid, proj in st.session_state.projects_db.items():
            proj_names.append(proj["name"][:30])
            created = datetime.date.fromisoformat(proj["created_at"])
            deadline = datetime.date.fromisoformat(proj["deadline"])
            starts.append(created)
            ends.append(deadline)
            colors.append(color_map.get(proj["priority"], "#0055b3"))

        fig = go.Figure()
        for i, (name_p, s, e, c) in enumerate(zip(proj_names, starts, ends, colors)):
            fig.add_trace(go.Bar(
                x=[(e - s).days],
                y=[name_p],
                base=[(s - datetime.date(2026, 1, 1)).days],
                orientation='h',
                marker_color=c,
                name=name_p,
                showlegend=False,
                hovertemplate=f"<b>{name_p}</b><br>Start: {s}<br>End: {e}<extra></extra>"
            ))
        fig.update_layout(
            height=220,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#e8eef6', title="Days from Jan 2026"),
            yaxis=dict(showgrid=False),
            font=dict(family="Open Sans", size=12, color="#003366"),
            barmode='overlay'
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><span class="accent-bar"></span>Workload Distribution by Priority</div>', unsafe_allow_html=True)
        priority_counts = defaultdict(int)
        priority_hours = defaultdict(int)
        for t in st.session_state.tasks_db.values():
            priority_counts[t["priority"]] += 1
            priority_hours[t["priority"]] += t["effort_hours"]

        fig2 = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "bar"}]])
        labels = list(priority_counts.keys())
        vals = list(priority_counts.values())
        pcolors = [color_map.get(l, "#888") for l in labels]
        fig2.add_trace(go.Pie(
            labels=labels, values=vals,
            marker=dict(colors=pcolors),
            hole=0.5,
            textinfo='label+percent',
            hovertemplate="<b>%{label}</b><br>Tasks: %{value}<extra></extra>"
        ), 1, 1)
        fig2.add_trace(go.Bar(
            x=list(priority_hours.keys()),
            y=list(priority_hours.values()),
            marker_color=pcolors,
            hovertemplate="<b>%{x}</b><br>Hours: %{y}<extra></extra>",
            name="Effort Hours"
        ), 1, 2)
        fig2.update_layout(
            height=240,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            font=dict(family="Open Sans", size=12, color="#003366")
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><span class="accent-bar"></span>My Workload Gauge</div>', unsafe_allow_html=True)
        total_effort, available, pct = calculate_workload(st.session_state.current_user)
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=round(pct, 1),
            title={'text': "Workload %", 'font': {'size': 14, 'color': '#003366'}},
            delta={'reference': 100, 'increasing': {'color': '#dc3545'}},
            gauge={
                'axis': {'range': [0, 150], 'tickwidth': 1, 'tickcolor': "#003366"},
                'bar': {'color': "#003366"},
                'steps': [
                    {'range': [0, 70], 'color': '#e0fff0'},
                    {'range': [70, 100], 'color': '#fff5d0'},
                    {'range': [100, 150], 'color': '#ffe0e0'}
                ],
                'threshold': {
                    'line': {'color': "#dc3545", 'width': 4},
                    'thickness': 0.75,
                    'value': 100
                }
            }
        ))
        fig_gauge.update_layout(
            height=220,
            margin=dict(l=20, r=20, t=30, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Open Sans")
        )
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.markdown(f"**Total Effort:** {total_effort}h &nbsp;|&nbsp; **Available:** {round(available, 1)}h", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><span class="accent-bar"></span>Recent Activity</div>', unsafe_allow_html=True)
        recent_logs = list(reversed(st.session_state.audit_logs))[:5]
        cat_colors = {"Project": "blue", "Task": "gold", "Negotiation": "red", "Approval": "green", "Auth": "gray"}
        for log in recent_logs:
            cat = log.get("category", "General")
            color = cat_colors.get(cat, "blue")
            st.markdown(f"""
            <div class="timeline-item">
                <div class="timeline-dot {'gold' if color=='gold' else 'green' if color=='green' else 'red' if color=='red' else ''}"></div>
                <div>
                    <div style="font-size:13px;color:#222;font-weight:500;">{log['action']}</div>
                    <div style="font-size:11px;color:#888;margin-top:2px;">{log['timestamp']} &bull; {log['user']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><span class="accent-bar"></span>Upcoming Deadlines</div>', unsafe_allow_html=True)
        today_d = datetime.date.today()
        upcoming = sorted(
            [(tid, t) for tid, t in st.session_state.tasks_db.items()
             if t.get("assigned_to") == st.session_state.current_user],
            key=lambda x: x[1]["deadline"]
        )[:4]
        for tid, task in upcoming:
            dl = datetime.date.fromisoformat(task["deadline"])
            days_left = (dl - today_d).days
            color = "red" if days_left < 7 else "gold" if days_left < 14 else "blue"
            badge_class = "badge-red" if color == "red" else "badge-gold" if color == "gold" else "badge-blue"
            st.markdown(f"""
            <div class="task-row {'conflict' if color=='red' else 'pending' if color=='gold' else ''}">
                <div style="flex:1">
                    <div style="font-size:13px;font-weight:600;color:#003366;">{task['name']}</div>
                    <div style="font-size:11px;color:#888;">{task['deadline']} &bull; {task['effort_hours']}h</div>
                </div>
                <span class="badge {badge_class}">{days_left}d left</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><span class="accent-bar"></span>Task Status Pipeline</div>', unsafe_allow_html=True)
    statuses = ["Pending", "In Progress", "Completed", "Blocked"]
    status_counts = defaultdict(int)
    for t in st.session_state.tasks_db.values():
        status_counts[t["status"]] += 1
    status_colors = {"Pending": "#e8b931", "In Progress": "#0055b3", "Completed": "#28a745", "Blocked": "#dc3545"}
    fig3 = go.Figure(go.Funnel(
        y=list(status_counts.keys()),
        x=list(status_counts.values()),
        textinfo="value+percent initial",
        marker=dict(color=[status_colors.get(s, "#888") for s in status_counts.keys()]),
        connector={"line": {"color": "#e0e8f6", "width": 2}}
    ))
    fig3.update_layout(
        height=200,
        margin=dict(l=20, r=20, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Open Sans", size=13, color="#003366")
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_projects():
    user = st.session_state.users_db[st.session_state.current_user]
    role = user["role"]
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">Project <span>Management</span></div>
        <div class="hero-sub">Create, manage, and monitor all projects in your portfolio</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="page-body">', unsafe_allow_html=True)

    if role in ["Manager", "Administrator"]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><span class="accent-bar"></span>Create New Project</div>', unsafe_allow_html=True)
        with st.form("create_project_form"):
            c1, c2 = st.columns(2)
            with c1:
                proj_name = st.text_input("Project Name*", placeholder="Enter project name")
                proj_priority = st.selectbox("Priority Level*", ["Low", "Medium", "High", "Critical"])
                proj_negotiable = st.selectbox("Deadline Negotiable?", ["Yes", "No"])
            with c2:
                proj_desc = st.text_area("Project Description*", placeholder="Describe the project objectives", height=100)
                proj_deadline = st.date_input("Project Deadline*", value=datetime.date.today() + datetime.timedelta(days=30))
                proj_status = st.selectbox("Initial Status", ["Planning", "Active"])
            submitted = st.form_submit_button("Create Project")
            if submitted:
                if not proj_name or not proj_desc:
                    st.error("Project name and description are required.")
                elif any(p["name"] == proj_name for p in st.session_state.projects_db.values()):
                    st.error("A project with this name already exists.")
                elif proj_deadline < datetime.date.today():
                    st.error("Deadline must be a future date.")
                else:
                    pid = f"PRJ-{str(len(st.session_state.projects_db)+1).zfill(3)}"
                    st.session_state.projects_db[pid] = {
                        "name": proj_name,
                        "description": proj_desc,
                        "deadline": str(proj_deadline),
                        "priority": proj_priority,
                        "negotiable": proj_negotiable == "Yes",
                        "status": proj_status,
                        "created_by": st.session_state.current_user,
                        "contributors": [],
                        "created_at": str(datetime.date.today())
                    }
                    add_audit(f"Project {pid} '{proj_name}' created", "Project")
                    st.success(f"Project {pid} created successfully.")
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><span class="accent-bar"></span>All Projects</div>', unsafe_allow_html=True)
    priority_colors = {"Critical": "badge-red", "High": "badge-gold", "Medium": "badge-blue", "Low": "badge-green"}
    status_colors_b = {"Active": "badge-green", "Planning": "badge-blue", "Completed": "badge-gray", "On Hold": "badge-gold"}
    for pid, proj in st.session_state.projects_db.items():
        today_d = datetime.date.today()
        dl = datetime.date.fromisoformat(proj["deadline"])
        days_left = (dl - today_d).days
        tasks_in_proj = [t for t in st.session_state.tasks_db.values() if t["project_id"] == pid]
        with st.expander(f"{pid} — {proj['name']} | {proj['status']} | Due: {proj['deadline']}", expanded=False):
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.markdown(f"**Description:** {proj['description']}")
                st.markdown(f"**Priority:** <span class='badge {priority_colors.get(proj['priority'], 'badge-blue')}'>{proj['priority']}</span>", unsafe_allow_html=True)
                st.markdown(f"**Status:** <span class='badge {status_colors_b.get(proj['status'], 'badge-blue')}'>{proj['status']}</span>", unsafe_allow_html=True)
                st.markdown(f"**Negotiable:** {'Yes' if proj['negotiable'] else 'No'}")
            with col2:
                st.markdown(f"**Deadline:** {proj['deadline']} ({days_left} days left)")
                st.markdown(f"**Created By:** {proj['created_by']}")
                st.markdown(f"**Tasks:** {len(tasks_in_proj)}")
                contrib_emails = proj.get("contributors", [])
                contrib_names = [st.session_state.users_db.get(e, {}).get("name", e) for e in contrib_emails]
                st.markdown(f"**Contributors:** {', '.join(contrib_names) if contrib_names else 'None assigned'}")
            with col3:
                if role in ["Manager", "Administrator"]:
                    with st.form(f"assign_contrib_{pid}"):
                        available_contribs = [e for e, u in st.session_state.users_db.items() if u["role"] == "Contributor"]
                        new_contrib = st.selectbox("Assign Contributor", available_contribs,
                                                   format_func=lambda e: st.session_state.users_db[e]["name"])
                        if st.form_submit_button("Assign"):
                            if new_contrib not in st.session_state.projects_db[pid]["contributors"]:
                                st.session_state.projects_db[pid]["contributors"].append(new_contrib)
                                add_audit(f"Contributor {new_contrib} assigned to {pid}", "Project")
                                st.success("Contributor assigned.")
                                st.rerun()
                    with st.form(f"update_proj_{pid}"):
                        new_status = st.selectbox("Update Status", ["Planning", "Active", "Completed", "On Hold"],
                                                  index=["Planning", "Active", "Completed", "On Hold"].index(proj["status"]) if proj["status"] in ["Planning", "Active", "Completed", "On Hold"] else 0)
                        if st.form_submit_button("Update Status"):
                            st.session_state.projects_db[pid]["status"] = new_status
                            add_audit(f"Project {pid} status updated to {new_status}", "Project")
                            st.success("Status updated.")
                            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><span class="accent-bar"></span>Project Health Overview</div>', unsafe_allow_html=True)
    proj_data = []
    for pid, proj in st.session_state.projects_db.items():
        tasks_in_proj = [t for t in st.session_state.tasks_db.values() if t["project_id"] == pid]
        total_hours = sum(t["effort_hours"] for t in tasks_in_proj)
        proj_data.append({"Project": proj["name"][:20], "Tasks": len(tasks_in_proj), "Total Hours": total_hours, "Priority": proj["priority"], "Status": proj["status"]})
    if proj_data:
        df_proj = pd.DataFrame(proj_data)
        fig_proj = px.scatter(df_proj, x="Tasks", y="Total Hours", color="Priority",
                              size="Total Hours", hover_name="Project",
                              color_discrete_map={"Critical": "#dc3545", "High": "#e8b931", "Medium": "#0055b3", "Low": "#28a745"},
                              title="Project Complexity vs Workload")
        fig_proj.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(248,250,253,1)',
                               font=dict(family="Open Sans", color="#003366"),
                               margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_proj, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_tasks():
    user = st.session_state.users_db[st.session_state.current_user]
    role = user["role"]
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">Task <span>Management</span></div>
        <div class="hero-sub">Track, create, and manage all tasks across your projects</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="page-body">', unsafe_allow_html=True)

    if role in ["Contributor", "Manager", "Administrator"]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><span class="accent-bar"></span>Create New Task</div>', unsafe_allow_html=True)
        with st.form("create_task_form"):
            c1, c2 = st.columns(2)
            with c1:
                task_name = st.text_input("Task Name*", placeholder="Enter task name")
                if role == "Contributor":
                    assigned_projects = {pid: proj["name"] for pid, proj in st.session_state.projects_db.items()
                                         if st.session_state.current_user in proj.get("contributors", [])}
                else:
                    assigned_projects = {pid: proj["name"] for pid, proj in st.session_state.projects_db.items()}
                proj_options = list(assigned_projects.keys())
                task_project = st.selectbox("Project*", proj_options, format_func=lambda x: assigned_projects.get(x, x)) if proj_options else st.selectbox("Project*", ["No projects available"])
                task_priority = st.selectbox("Priority*", ["Low", "Medium", "High", "Critical"])
            with c2:
                task_effort = st.number_input("Effort Hours*", min_value=1, max_value=500, value=8)
                task_deadline = st.date_input("Task Deadline*", value=datetime.date.today() + datetime.timedelta(days=14))
                if role in ["Manager", "Administrator"]:
                    available_contribs = {e: st.session_state.users_db[e]["name"] for e in st.session_state.users_db if st.session_state.users_db[e]["role"] == "Contributor"}
                    task_assignee = st.selectbox("Assign To*", list(available_contribs.keys()), format_func=lambda x: available_contribs.get(x, x)) if available_contribs else None
                    task_fixed = st.checkbox("Fixed (Non-Negotiable) Deadline")
                else:
                    task_assignee = st.session_state.current_user
                    task_fixed = False
            submitted = st.form_submit_button("Create Task")
            if submitted:
                if not task_name:
                    st.error("Task name is required.")
                elif not proj_options or task_project == "No projects available":
                    st.error("No assigned projects available. Please contact your manager.")
                elif task_deadline < datetime.date.today():
                    st.error("Deadline must be a future date.")
                else:
                    proj = st.session_state.projects_db.get(task_project, {})
                    proj_deadline_str = proj.get("deadline")
                    if proj_deadline_str and task_deadline > datetime.date.fromisoformat(proj_deadline_str):
                        st.warning(f"Task deadline exceeds project deadline ({proj_deadline_str}). Task created with warning.")
                    tid = f"TSK-{str(len(st.session_state.tasks_db)+1).zfill(3)}"
                    st.session_state.tasks_db[tid] = {
                        "name": task_name,
                        "project_id": task_project,
                        "assigned_to": task_assignee if task_assignee else st.session_state.current_user,
                        "effort_hours": task_effort,
                        "deadline": str(task_deadline),
                        "priority": task_priority,
                        "status": "Pending",
                        "fixed_deadline": task_fixed if role in ["Manager", "Administrator"] else False,
                        "created_by": st.session_state.current_user,
                        "created_at": str(datetime.date.today())
                    }
                    add_audit(f"Task {tid} '{task_name}' created in {task_project}", "Task")
                    st.success(f"Task {tid} created successfully.")
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><span class="accent-bar"></span>All Tasks</div>', unsafe_allow_html=True)
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    with filter_col1:
        filter_status = st.selectbox("Filter by Status", ["All", "Pending", "In Progress", "Completed", "Blocked"])
    with filter_col2:
        filter_priority = st.selectbox("Filter by Priority", ["All", "Low", "Medium", "High", "Critical"])
    with filter_col3:
        filter_project = st.selectbox("Filter by Project", ["All"] + [p["name"] for p in st.session_state.projects_db.values()])

    today_d = datetime.date.today()
    priority_badge = {"Critical": "badge-red", "High": "badge-gold", "Medium": "badge-blue", "Low": "badge-green"}
    status_badge = {"Pending": "badge-gold", "In Progress": "badge-blue", "Completed": "badge-green", "Blocked": "badge-red"}

    task_list = list(st.session_state.tasks_db.items())
    if role == "Contributor":
        task_list = [(tid, t) for tid, t in task_list if t["assigned_to"] == st.session_state.current_user]
    if filter_status != "All":
        task_list = [(tid, t) for tid, t in task_list if t["status"] == filter_status]
    if filter_priority != "All":
        task_list = [(tid, t) for tid, t in task_list if t["priority"] == filter_priority]
    if filter_project != "All":
        pid_match = [pid for pid, p in st.session_state.projects_db.items() if p["name"] == filter_project]
        task_list = [(tid, t) for tid, t in task_list if t["project_id"] in pid_match]

    for tid, task in task_list:
        dl = datetime.date.fromisoformat(task["deadline"])
        days_left = (dl - today_d).days
        proj_name = st.session_state.projects_db.get(task["project_id"], {}).get("name", task["project_id"])
        assignee_name = st.session_state.users_db.get(task["assigned_to"], {}).get("name", task["assigned_to"])
        row_class = "conflict" if days_left < 0 else "pending" if days_left < 7 else "approved" if task["status"] == "Completed" else ""
        st.markdown(f"""
        <div class="task-row {row_class}">
            <div style="flex:2">
                <div style="font-size:14px;font-weight:700;color:#003366;">{task['name']}</div>
                <div style="font-size:12px;color:#888;margin-top:2px;">{tid} &bull; {proj_name} &bull; Assigned: {assignee_name}</div>
            </div>
            <div style="flex:1;text-align:center;">
                <span class="badge {priority_badge.get(task['priority'], 'badge-blue')}">{task['priority']}</span>
            </div>
            <div style="flex:1;text-align:center;">
                <span class="badge {status_badge.get(task['status'], 'badge-gray')}">{task['status']}</span>
            </div>
            <div style="flex:1;text-align:right;font-size:12px;color:#555;">
                {task['effort_hours']}h &bull; Due {task['deadline']}<br>
                <span style="color:{'#dc3545' if days_left<0 else '#e8b931' if days_left<7 else '#28a745'};font-weight:700;">
                    {'OVERDUE' if days_left<0 else f'{days_left}d left'}
                </span>
                {'&nbsp;<span class="badge badge-red">FIXED</span>' if task.get('fixed_deadline') else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)
        if role in ["Manager", "Administrator"]:
            with st.expander(f"Edit {tid}"):
                with st.form(f"edit_task_{tid}"):
                    ec1, ec2 = st.columns(2)
                    with ec1:
                        new_effort = st.number_input("Effort Hours", value=task["effort_hours"], min_value=1, key=f"eff_{tid}")
                        new_priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"],
                                                    index=["Low", "Medium", "High", "Critical"].index(task["priority"]), key=f"pri_{tid}")
                    with ec2:
                        new_status = st.selectbox("Status", ["Pending", "In Progress", "Completed", "Blocked"],
                                                  index=["Pending", "In Progress", "Completed", "Blocked"].index(task["status"]) if task["status"] in ["Pending", "In Progress", "Completed", "Blocked"] else 0, key=f"sts_{tid}")
                        available_contribs = {e: st.session_state.users_db[e]["name"] for e in st.session_state.users_db if st.session_state.users_db[e]["role"] == "Contributor"}
                        current_idx = list(available_contribs.keys()).index(task["assigned_to"]) if task["assigned_to"] in available_contribs else 0
                        new_assignee = st.selectbox("Reassign To", list(available_contribs.keys()), index=current_idx, format_func=lambda x: available_contribs.get(x, x), key=f"asg_{tid}")
                    if st.form_submit_button("Save Changes"):
                        st.session_state.tasks_db[tid]["effort_hours"] = new_effort
                        st.session_state.tasks_db[tid]["priority"] = new_priority
                        st.session_state.tasks_db[tid]["status"] = new_status
                        st.session_state.tasks_db[tid]["assigned_to"] = new_assignee
                        add_audit(f"Task {tid} attributes updated", "Task")
                        st.success("Task updated successfully.")
                        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><span class="accent-bar"></span>Task Deadline Timeline</div>', unsafe_allow_html=True)
    task_timeline_data = []
    for tid, task in st.session_state.tasks_db.items():
        dl = datetime.date.fromisoformat(task["deadline"])
        days_left = (dl - today_d).days
        task_timeline_data.append({
            "Task": task["name"][:25],
            "Days Until Deadline": days_left,
            "Priority": task["priority"],
            "Effort (h)": task["effort_hours"]
        })
    if task_timeline_data:
        df_tl = pd.DataFrame(task_timeline_data)
        fig_tl = px.bar(df_tl, x="Days Until Deadline", y="Task", color="Priority",
                        orientation='h',
                        color_discrete_map={"Critical": "#dc3545", "High": "#e8b931", "Medium": "#0055b3", "Low": "#28a745"},
                        title="Days Until Task Deadline")
        fig_tl.update_layout(height=max(200, len(task_timeline_data)*35), paper_bgcolor='rgba(0,0,0,0)',
                              plot_bgcolor='rgba(248,250,253,1)', font=dict(family="Open Sans", color="#003366"),
                              margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_tl, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_workload():
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">Workload <span>Analysis</span></div>
        <div class="hero-sub">Analyze feasibility, detect conflicts, and understand capacity utilization</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="page-body">', unsafe_allow_html=True)
    user = st.session_state.users_db[st.session_state.current_user]
    role = user["role"]

    contributors = {e: u for e, u in st.session_state.users_db.items() if u["role"] == "Contributor"}
    if role == "Contributor":
        selected_email = st.session_state.current_user
        selected_name = user["name"]
    else:
        selected_email_key = st.selectbox("Select Contributor for Analysis",
                                           list(contributors.keys()),
                                           format_func=lambda e: contributors[e]["name"])
        selected_email = selected_email_key
        selected_name = contributors[selected_email]["name"]

    col1, col2, col3 = st.columns(3)
    total_effort, available, pct = calculate_workload(selected_email)
    with col1:
        st.metric("Total Effort Hours", f"{total_effort}h")
    with col2:
        st.metric("Available Hours (30d)", f"{round(available,1)}h")
    with col3:
        color = "normal" if pct <= 100 else "inverse"
        st.metric("Workload %", f"{round(pct,1)}%", delta=f"{round(pct-100,1)}% {'overloaded' if pct>100 else 'free'}", delta_color=color)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><span class="accent-bar"></span>Capacity vs Effort Analysis</div>', unsafe_allow_html=True)
    my_tasks = get_user_tasks(selected_email)
    today_d = datetime.date.today()
    user_info = st.session_state.users_db.get(selected_email, {})
    weekly = user_info.get("weekly_hours", 40)
    analysis_data = []
    for tid, task in my_tasks.items():
        dl = datetime.date.fromisoformat(task["deadline"])
        days_left = max((dl - today_d).days, 1)
        weeks = days_left / 7
        hours_avail = weeks * weekly
        status = "Feasible" if task["effort_hours"] <= hours_avail else "CONFLICT"
        overload = max(0, ((task["effort_hours"] - hours_avail) / hours_avail * 100)) if hours_avail > 0 else 100
        analysis_data.append({
            "Task": task["name"][:25],
            "Effort (h)": task["effort_hours"],
            "Available (h)": round(hours_avail, 1),
            "Overload %": round(overload, 1),
            "Status": status,
            "Priority": task["priority"]
        })
    if analysis_data:
        df_analysis = pd.DataFrame(analysis_data)
        fig_analysis = go.Figure()
        fig_analysis.add_trace(go.Bar(name="Effort Required", x=df_analysis["Task"], y=df_analysis["Effort (h)"],
                                      marker_color="#003366"))
        fig_analysis.add_trace(go.Bar(name="Hours Available", x=df_analysis["Task"], y=df_analysis["Available (h)"],
                                      marker_color="#28a745", opacity=0.7))
        fig_analysis.update_layout(barmode='group', height=300,
                                   paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(248,250,253,1)',
                                   font=dict(family="Open Sans", color="#003366"),
                                   legend=dict(orientation="h", y=1.1),
                                   margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_analysis, use_container_width=True)
        st.dataframe(df_analysis, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    conflicts = detect_conflicts(selected_email)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<div class="card-title"><span class="accent-bar"></span>Conflict Detection Results ({len(conflicts)} conflicts found)</div>', unsafe_allow_html=True)
    if conflicts:
        for conf in conflicts:
            st.markdown(f"""
            <div class="task-row conflict">
                <div style="flex:2">
                    <div style="font-size:14px;font-weight:700;color:#9b1c1c;">{conf['task_name']}</div>
                    <div style="font-size:12px;color:#888;">{conf['task_id']} &bull; Priority: {conf['priority']} &bull; Deadline: {conf['deadline']}</div>
                </div>
                <div style="flex:1;text-align:center;">
                    <div style="font-size:13px;color:#222;">Required: <strong>{conf['effort']}h</strong></div>
                    <div style="font-size:13px;color:#222;">Available: <strong>{conf['available']}h</strong></div>
                </div>
                <div style="flex:1;text-align:right;">
                    <span class="badge badge-red">{conf['overload_pct']}% overloaded</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        if conflicts:
            overload_vals = [c["overload_pct"] for c in conflicts]
            task_names = [c["task_name"][:20] for c in conflicts]
            fig_conf = go.Figure(go.Bar(
                x=task_names, y=overload_vals,
                marker=dict(color=overload_vals, colorscale=[[0, "#e8b931"], [0.5, "#ff8c00"], [1, "#dc3545"]]),
                text=[f"{v}%" for v in overload_vals],
                textposition="auto"
            ))
            fig_conf.update_layout(title="Overload Percentage by Task", height=250,
                                   paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(248,250,253,1)',
                                   font=dict(family="Open Sans", color="#003366"),
                                   margin=dict(l=10, r=10, t=40, b=10),
                                   yaxis_title="Overload %")
            st.plotly_chart(fig_conf, use_container_width=True)
    else:
        st.success("No scheduling conflicts detected for this contributor.")
    st.markdown('</div>', unsafe_allow_html=True)

    if role in ["Manager", "Administrator"]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><span class="accent-bar"></span>Team Workload Comparison</div>', unsafe_allow_html=True)
        team_data = []
        for email, u in contributors.items():
            te, av, pp = calculate_workload(email)
            conf_count = len(detect_conflicts(email))
            team_data.append({"Name": u["name"], "Total Effort (h)": te, "Available (h)": round(av, 1),
                               "Workload %": round(pp, 1), "Conflicts": conf_count})
        if team_data:
            df_team = pd.DataFrame(team_data)
            fig_team = px.bar(df_team, x="Name", y=["Total Effort (h)", "Available (h)"],
                              barmode="group",
                              color_discrete_map={"Total Effort (h)": "#003366", "Available (h)": "#28a745"},
                              title="Team Capacity vs Effort")
            fig_team.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(248,250,253,1)',
                                   font=dict(family="Open Sans", color="#003366"),
                                   legend=dict(orientation="h", y=1.1),
                                   margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig_team, use_container_width=True)
            st.dataframe(df_team, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><span class="accent-bar"></span>Feasibility Analysis Report</div>', unsafe_allow_html=True)
    if st.button("Run Full Feasibility Analysis"):
        with st.spinner("Running feasibility analysis..."):
            time.sleep(1)
        for pid, proj in st.session_state.projects_db.items():
            proj_tasks = {tid: t for tid, t in st.session_state.tasks_db.items() if t["project_id"] == pid}
            proj_total_effort = sum(t["effort_hours"] for t in proj_tasks.values())
            proj_dl = datetime.date.fromisoformat(proj["deadline"])
            days_to_proj = max((proj_dl - today_d).days, 1)
            risk = "Low" if proj_total_effort < days_to_proj * 4 else "High" if proj_total_effort > days_to_proj * 8 else "Medium"
            risk_class = f"risk-{'low' if risk=='Low' else 'high' if risk=='High' else 'medium'}"
            st.markdown(f"""
            <div style="padding:14px 16px;border-radius:8px;background:#f8fafd;border:1px solid #e0e8f6;margin-bottom:10px;">
                <div style="font-size:15px;font-weight:700;color:#003366;">{proj['name']}</div>
                <div style="font-size:13px;color:#555;margin-top:6px;">
                    Total Effort: <strong>{proj_total_effort}h</strong> &bull;
                    Tasks: <strong>{len(proj_tasks)}</strong> &bull;
                    Days Remaining: <strong>{days_to_proj}</strong> &bull;
                    Risk: <span class="risk-indicator {risk_class}">{risk}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        add_audit("Full feasibility analysis completed", "Analysis")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_negotiations():
    user = st.session_state.users_db[st.session_state.current_user]
    role = user["role"]
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">Deadline <span>Negotiations</span></div>
        <div class="hero-sub">Manage deadline proposals, counter-proposals, approvals, and escalations</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="page-body">', unsafe_allow_html=True)

    if role in ["Manager", "Administrator"]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><span class="accent-bar"></span>Initiate Negotiation Session</div>', unsafe_allow_html=True)
        with st.form("init_neg_form"):
            c1, c2 = st.columns(2)
            with c1:
                all_tasks = {tid: f"{t['name']} ({tid})" for tid, t in st.session_state.tasks_db.items()}
                sel_task = st.selectbox("Select Task*", list(all_tasks.keys()), format_func=lambda x: all_tasks[x])
            with c2:
                prop_deadline = st.date_input("Proposed Deadline*", value=datetime.date.today() + datetime.timedelta(days=21))
            justif = st.text_area("Justification / Reasoning*", placeholder="Explain why this new deadline is proposed...")
            if st.form_submit_button("Generate Proposal"):
                if not justif:
                    st.error("Justification is required.")
                elif prop_deadline < datetime.date.today():
                    st.error("Proposed deadline must be in the future.")
                else:
                    neg_id = f"NEG-{str(len(st.session_state.negotiations_db)+1).zfill(3)}"
                    st.session_state.negotiations_db[neg_id] = {
                        "task_id": sel_task,
                        "status": "Pending",
                        "created_by": st.session_state.current_user,
                        "created_at": str(datetime.date.today()),
                        "proposals": [{
                            "proposed_deadline": str(prop_deadline),
                            "justification": justif,
                            "proposed_by": st.session_state.current_user,
                            "status": "Pending",
                            "timestamp": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                        }]
                    }
                    add_audit(f"Negotiation {neg_id} initiated for {sel_task}", "Negotiation")
                    st.success(f"Negotiation {neg_id} created and proposal sent.")
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("Auto-Generate Proposals for All Conflicts"):
            contributors = {e: u for e, u in st.session_state.users_db.items() if u["role"] == "Contributor"}
            count = 0
            for email in contributors:
                conflicts = detect_conflicts(email)
                for conf in conflicts:
                    existing = [n for n in st.session_state.negotiations_db.values()
                                if n["task_id"] == conf["task_id"] and n["status"] == "Pending"]
                    if not existing:
                        proposed = generate_proposal_deadline(conf["task_id"])
                        neg_id = f"NEG-{str(len(st.session_state.negotiations_db)+1).zfill(3)}"
                        task = st.session_state.tasks_db[conf["task_id"]]
                        justif_auto = (f"Conflict: task requires {conf['effort']}h but only {conf['available']}h available "
                                       f"before original deadline. System suggests {proposed} based on current workload.")
                        st.session_state.negotiations_db[neg_id] = {
                            "task_id": conf["task_id"],
                            "status": "Pending",
                            "created_by": st.session_state.current_user,
                            "created_at": str(datetime.date.today()),
                            "proposals": [{
                                "proposed_deadline": proposed,
                                "justification": justif_auto,
                                "proposed_by": "System Auto-Generator",
                                "status": "Pending",
                                "timestamp": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                            }]
                        }
                        add_audit(f"Auto-proposal generated for {conf['task_id']}", "Negotiation")
                        count += 1
            if count:
                st.success(f"{count} auto-proposals generated for detected conflicts.")
                st.rerun()
            else:
                st.info("No new conflicts require proposals.")

    status_filter = st.selectbox("Filter Negotiations", ["All", "Pending", "Approved", "Rejected", "Escalated"])
    neg_list = [(nid, n) for nid, n in st.session_state.negotiations_db.items()]
    if status_filter != "All":
        neg_list = [(nid, n) for nid, n in neg_list if n["status"] == status_filter]

    for nid, neg in neg_list:
        task = st.session_state.tasks_db.get(neg["task_id"], {})
        task_name = task.get("name", neg["task_id"])
        assignee = task.get("assigned_to", "")
        is_my_task = assignee == st.session_state.current_user
        status_badge_map = {"Pending": "badge-gold", "Approved": "badge-green", "Rejected": "badge-red", "Escalated": "badge-gray"}
        badge_cls = status_badge_map.get(neg["status"], "badge-blue")

        st.markdown(f"""
        <div class="task-row {'pending' if neg['status']=='Pending' else 'approved' if neg['status']=='Approved' else 'conflict' if neg['status']=='Rejected' else ''}">
            <div style="flex:2">
                <div style="font-size:14px;font-weight:700;color:#003366;">{nid} &mdash; {task_name}</div>
                <div style="font-size:12px;color:#888;">Created: {neg['created_at']} &bull; By: {neg['created_by']}</div>
            </div>
            <div style="flex:1;text-align:center;"><span class="badge {badge_cls}">{neg['status']}</span></div>
            <div style="flex:1;text-align:right;font-size:12px;color:#555;">{len(neg['proposals'])} proposal(s)</div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander(f"View & Act on {nid}"):
            for i, prop in enumerate(neg["proposals"]):
                p_badge = status_badge_map.get(prop["status"], "badge-blue")
                st.markdown(f"""
                <div style="padding:14px;background:#f8fafd;border-radius:8px;border:1px solid #e0e8f6;margin-bottom:8px;">
                    <div style="font-size:13px;font-weight:700;color:#003366;">Proposal #{i+1} by {prop['proposed_by']}</div>
                    <div style="font-size:13px;margin-top:6px;"><strong>Proposed Deadline:</strong> {prop['proposed_deadline']}</div>
                    <div style="font-size:13px;margin-top:4px;"><strong>Justification:</strong> {prop['justification']}</div>
                    <div style="font-size:11px;color:#888;margin-top:6px;">{prop['timestamp']} &bull; <span class="badge {p_badge}">{prop['status']}</span></div>
                </div>
                """, unsafe_allow_html=True)

            if neg["status"] == "Pending":
                act_col1, act_col2, act_col3 = st.columns(3)
                if role in ["Manager", "Client", "Administrator"]:
                    with act_col1:
                        if st.button(f"Approve {nid}", key=f"approve_{nid}"):
                            st.session_state.negotiations_db[nid]["status"] = "Approved"
                            if neg["proposals"]:
                                last_prop = neg["proposals"][-1]
                                st.session_state.tasks_db[neg["task_id"]]["deadline"] = last_prop["proposed_deadline"]
                                st.session_state.negotiations_db[nid]["proposals"][-1]["status"] = "Approved"
                            add_audit(f"Negotiation {nid} approved by {st.session_state.current_user}", "Approval")
                            st.success("Deadline approved and task updated.")
                            st.rerun()
                    with act_col2:
                        if st.button(f"Reject {nid}", key=f"reject_{nid}"):
                            st.session_state.negotiations_db[nid]["status"] = "Rejected"
                            st.session_state.negotiations_db[nid]["proposals"][-1]["status"] = "Rejected"
                            add_audit(f"Negotiation {nid} rejected by {st.session_state.current_user}", "Negotiation")
                            st.warning("Proposal rejected.")
                            st.rerun()
                    with act_col3:
                        if role in ["Manager", "Administrator"]:
                            if st.button(f"Escalate {nid}", key=f"escalate_{nid}"):
                                st.session_state.negotiations_db[nid]["status"] = "Escalated"
                                add_audit(f"Negotiation {nid} escalated to administrator", "Escalation")
                                st.info("Conflict escalated to administrator.")
                                st.rerun()

                if is_my_task and role == "Contributor":
                    with st.form(f"counter_{nid}"):
                        counter_dl = st.date_input("Your Proposed Deadline", value=datetime.date.today() + datetime.timedelta(days=21), key=f"cdl_{nid}")
                        counter_just = st.text_area("Justification for Counter-Proposal", placeholder="Explain your reasoning...", key=f"cj_{nid}")
                        if st.form_submit_button("Submit Counter-Proposal"):
                            if not counter_just:
                                st.error("Justification is required.")
                            else:
                                st.session_state.negotiations_db[nid]["proposals"].append({
                                    "proposed_deadline": str(counter_dl),
                                    "justification": counter_just,
                                    "proposed_by": st.session_state.current_user,
                                    "status": "Pending",
                                    "timestamp": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                                })
                                add_audit(f"Counter-proposal submitted for {nid}", "Negotiation")
                                st.success("Counter-proposal submitted.")
                                st.rerun()

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><span class="accent-bar"></span>Negotiation Status Overview</div>', unsafe_allow_html=True)
    status_counts = defaultdict(int)
    for n in st.session_state.negotiations_db.values():
        status_counts[n["status"]] += 1
    if status_counts:
        fig_neg = go.Figure(go.Pie(
            labels=list(status_counts.keys()),
            values=list(status_counts.values()),
            hole=0.6,
            marker=dict(colors=["#e8b931", "#28a745", "#dc3545", "#888"]),
            textinfo='label+value'
        ))
        fig_neg.update_layout(height=280, paper_bgcolor='rgba(0,0,0,0)',
                               font=dict(family="Open Sans", color="#003366"),
                               margin=dict(l=10, r=10, t=10, b=10),
                               showlegend=True)
        st.plotly_chart(fig_neg, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_reports():
    user = st.session_state.users_db[st.session_state.current_user]
    role = user["role"]
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">Reports & <span>Analytics</span></div>
        <div class="hero-sub">Comprehensive project insights, risk analysis, and performance metrics</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="page-body">', unsafe_allow_html=True)
    today_d = datetime.date.today()
    tab1, tab2, tab3, tab4 = st.tabs(["Project Risk", "Workload Trends", "Negotiation Analytics", "Performance KPIs"])

    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><span class="accent-bar"></span>Project Risk Assessment</div>', unsafe_allow_html=True)
        risk_data = []
        for pid, proj in st.session_state.projects_db.items():
            proj_tasks = [t for t in st.session_state.tasks_db.values() if t["project_id"] == pid]
            total_effort = sum(t["effort_hours"] for t in proj_tasks)
            dl = datetime.date.fromisoformat(proj["deadline"])
            days_left = max((dl - today_d).days, 1)
            risk_score = min(100, (total_effort / (days_left * 0.5)) * 10)
            risk_label = "Low" if risk_score < 33 else "High" if risk_score > 66 else "Medium"
            neg_count = len([n for n in st.session_state.negotiations_db.values()
                             if any(t["project_id"] == pid for tid, t in st.session_state.tasks_db.items() if tid == n["task_id"])])
            risk_data.append({
                "Project": proj["name"][:25],
                "Risk Score": round(risk_score, 1),
                "Risk Level": risk_label,
                "Days Left": days_left,
                "Total Tasks": len(proj_tasks),
                "Total Effort (h)": total_effort,
                "Negotiations": neg_count
            })
        if risk_data:
            df_risk = pd.DataFrame(risk_data)
            fig_risk = px.bar(df_risk, x="Project", y="Risk Score", color="Risk Level",
                              color_discrete_map={"Low": "#28a745", "Medium": "#e8b931", "High": "#dc3545"},
                              title="Project Risk Scores", text="Risk Score")
            fig_risk.add_hline(y=33, line_dash="dash", line_color="#28a745", annotation_text="Low threshold")
            fig_risk.add_hline(y=66, line_dash="dash", line_color="#dc3545", annotation_text="High threshold")
            fig_risk.update_layout(height=320, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(248,250,253,1)',
                                   font=dict(family="Open Sans", color="#003366"),
                                   margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig_risk, use_container_width=True)
            st.dataframe(df_risk, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><span class="accent-bar"></span>Effort Distribution by Project</div>', unsafe_allow_html=True)
        effort_by_proj = defaultdict(int)
        for t in st.session_state.tasks_db.values():
            proj_name = st.session_state.projects_db.get(t["project_id"], {}).get("name", t["project_id"])
            effort_by_proj[proj_name[:20]] += t["effort_hours"]
        fig_effort = go.Figure(go.Treemap(
            labels=list(effort_by_proj.keys()),
            parents=[""] * len(effort_by_proj),
            values=list(effort_by_proj.values()),
            marker=dict(colorscale=[[0, "#cce0ff"], [0.5, "#003366"], [1, "#001f44"]]),
            texttemplate="<b>%{label}</b><br>%{value}h"
        ))
        fig_effort.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)',
                                 font=dict(family="Open Sans", color="#fff"),
                                 margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_effort, use_container_width=True)

        days_range = list(range(-14, 31))
        simulated_load = [max(0, 60 + 30 * np.sin(d * 0.3) + random.gauss(0, 8)) for d in days_range]
        dates_range = [today_d + datetime.timedelta(days=d) for d in days_range]
        fig_load = go.Figure()
        fig_load.add_trace(go.Scatter(
            x=dates_range, y=simulated_load,
            mode='lines+markers',
            line=dict(color="#003366", width=2.5),
            fill='tozeroy',
            fillcolor='rgba(0,51,102,0.08)',
            name="Daily Load"
        ))
        fig_load.add_hline(y=100, line_dash="dash", line_color="#dc3545", annotation_text="100% Capacity")
        fig_load.update_layout(title="Workload Trend (Past 2 Weeks + Next 30 Days)", height=280,
                               paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(248,250,253,1)',
                               font=dict(family="Open Sans", color="#003366"),
                               margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_load, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><span class="accent-bar"></span>Negotiation Outcomes Analysis</div>', unsafe_allow_html=True)
        outcomes = defaultdict(int)
        for n in st.session_state.negotiations_db.values():
            outcomes[n["status"]] += 1
        if outcomes:
            fig_out = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "bar"}]])
            colors_out = {"Pending": "#e8b931", "Approved": "#28a745", "Rejected": "#dc3545", "Escalated": "#888"}
            fig_out.add_trace(go.Pie(
                labels=list(outcomes.keys()), values=list(outcomes.values()),
                marker=dict(colors=[colors_out.get(k, "#aaa") for k in outcomes.keys()]),
                hole=0.5, textinfo='label+percent'
            ), 1, 1)
            fig_out.add_trace(go.Bar(
                x=list(outcomes.keys()), y=list(outcomes.values()),
                marker_color=[colors_out.get(k, "#aaa") for k in outcomes.keys()],
                name="Count"
            ), 1, 2)
            fig_out.update_layout(height=280, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(248,250,253,1)',
                                  font=dict(family="Open Sans", color="#003366"),
                                  showlegend=False, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig_out, use_container_width=True)
        neg_table = []
        for nid, neg in st.session_state.negotiations_db.items():
            task = st.session_state.tasks_db.get(neg["task_id"], {})
            neg_table.append({
                "ID": nid, "Task": task.get("name", neg["task_id"])[:25],
                "Status": neg["status"], "Proposals": len(neg["proposals"]),
                "Created": neg["created_at"]
            })
        st.dataframe(pd.DataFrame(neg_table), use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><span class="accent-bar"></span>System Performance KPIs</div>', unsafe_allow_html=True)
        k1, k2, k3, k4 = st.columns(4)
        total_t = len(st.session_state.tasks_db)
        completed = len([t for t in st.session_state.tasks_db.values() if t["status"] == "Completed"])
        completion_rate = round(completed / total_t * 100, 1) if total_t else 0
        total_n = len(st.session_state.negotiations_db)
        approved_n = len([n for n in st.session_state.negotiations_db.values() if n["status"] == "Approved"])
        resolution_rate = round(approved_n / total_n * 100, 1) if total_n else 0
        with k1:
            st.metric("Task Completion Rate", f"{completion_rate}%")
        with k2:
            st.metric("Conflict Resolution Rate", f"{resolution_rate}%")
        with k3:
            st.metric("Active Projects", len([p for p in st.session_state.projects_db.values() if p["status"] == "Active"]))
        with k4:
            total_hours = sum(t["effort_hours"] for t in st.session_state.tasks_db.values())
            st.metric("Total Effort Tracked", f"{total_hours}h")
        categories = ['Task Management', 'Conflict Detection', 'Workload Balance', 'Deadline Adherence', 'Negotiation Speed']
        scores = [completion_rate, min(100, resolution_rate * 1.2), 72, 65, 80]
        fig_radar = go.Figure(go.Scatterpolar(
            r=scores, theta=categories, fill='toself',
            fillcolor='rgba(0,51,102,0.15)',
            line=dict(color="#003366", width=2),
            name="System Performance"
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100],
                                       gridcolor='#e0e8f6', tickfont=dict(size=10))),
            height=320, paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Open Sans", color="#003366"),
            margin=dict(l=60, r=60, t=30, b=30),
            showlegend=False
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_audit_logs():
    user = st.session_state.users_db[st.session_state.current_user]
    role = user["role"]
    if role not in ["Manager", "Administrator"]:
        st.warning("Access restricted. You need Manager or Administrator role to view audit logs.")
        return
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">Audit <span>Logs</span></div>
        <div class="hero-sub">Complete immutable record of all system actions and decisions</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="page-body">', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><span class="accent-bar"></span>System Activity Log</div>', unsafe_allow_html=True)
    filter_cat = st.selectbox("Filter by Category", ["All", "Project", "Task", "Negotiation", "Approval", "Auth", "Analysis", "Escalation"])
    logs = list(reversed(st.session_state.audit_logs))
    if filter_cat != "All":
        logs = [l for l in logs if l.get("category") == filter_cat]

    cat_dot = {"Project": "blue", "Task": "gold", "Negotiation": "red", "Approval": "green", "Auth": "", "Analysis": "blue"}
    for log in logs:
        dot_cls = cat_dot.get(log.get("category", ""), "")
        cat = log.get("category", "General")
        cat_badge = {"Project": "badge-blue", "Task": "badge-gold", "Negotiation": "badge-red",
                     "Approval": "badge-green", "Auth": "badge-gray", "Analysis": "badge-blue",
                     "Escalation": "badge-red"}
        st.markdown(f"""
        <div class="timeline-item">
            <div class="timeline-dot {dot_cls}"></div>
            <div style="flex:1;">
                <div style="display:flex;align-items:center;gap:10px;">
                    <span style="font-size:13px;font-weight:600;color:#222;">{log['action']}</span>
                    <span class="badge {cat_badge.get(cat, 'badge-gray')}">{cat}</span>
                </div>
                <div style="font-size:11px;color:#888;margin-top:2px;">{log['timestamp']} &bull; {log['user']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><span class="accent-bar"></span>Activity Distribution</div>', unsafe_allow_html=True)
    all_logs = st.session_state.audit_logs
    cat_count = defaultdict(int)
    for l in all_logs:
        cat_count[l.get("category", "General")] += 1
    fig_cat = go.Figure(go.Bar(
        x=list(cat_count.keys()), y=list(cat_count.values()),
        marker_color="#003366",
        text=list(cat_count.values()), textposition="auto"
    ))
    fig_cat.update_layout(height=240, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(248,250,253,1)',
                          font=dict(family="Open Sans", color="#003366"),
                          margin=dict(l=10, r=10, t=10, b=10),
                          yaxis_title="Count")
    st.plotly_chart(fig_cat, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_user_management():
    user = st.session_state.users_db[st.session_state.current_user]
    role = user["role"]
    if role != "Administrator":
        st.warning("Access restricted. Administrator role required.")
        return
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">User <span>Management</span></div>
        <div class="hero-sub">Manage accounts, roles, availability, and system access</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="page-body">', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><span class="accent-bar"></span>All User Accounts</div>', unsafe_allow_html=True)
    role_badge = {"Administrator": "badge-red", "Manager": "badge-blue", "Contributor": "badge-green", "Client": "badge-gold"}
    for email, u in st.session_state.users_db.items():
        user_tasks = get_user_tasks(email)
        st.markdown(f"""
        <div class="task-row">
            <div style="flex:2">
                <div style="font-size:14px;font-weight:700;color:#003366;">{u['name']}</div>
                <div style="font-size:12px;color:#888;">{email} &bull; {u['weekly_hours']}h/week availability</div>
            </div>
            <div style="flex:1;text-align:center;"><span class="badge {role_badge.get(u['role'], 'badge-gray')}">{u['role']}</span></div>
            <div style="flex:1;text-align:right;font-size:12px;color:#555;">{len(user_tasks)} tasks assigned</div>
        </div>
        """, unsafe_allow_html=True)
        with st.expander(f"Edit Account: {u['name']}"):
            with st.form(f"edit_user_{email}"):
                eu1, eu2 = st.columns(2)
                with eu1:
                    new_name = st.text_input("Full Name", value=u["name"], key=f"un_{email}")
                    new_role = st.selectbox("Role", ["Administrator", "Manager", "Contributor", "Client"],
                                           index=["Administrator", "Manager", "Contributor", "Client"].index(u["role"]) if u["role"] in ["Administrator", "Manager", "Contributor", "Client"] else 2, key=f"ur_{email}")
                with eu2:
                    new_weekly = st.number_input("Weekly Hours", value=u["weekly_hours"], min_value=1, max_value=80, key=f"uw_{email}")
                    new_max = st.number_input("Max Workload Hours", value=u.get("max_workload", 40), min_value=1, max_value=80, key=f"um_{email}")
                if st.form_submit_button("Update Account"):
                    st.session_state.users_db[email]["name"] = new_name
                    st.session_state.users_db[email]["role"] = new_role
                    st.session_state.users_db[email]["weekly_hours"] = new_weekly
                    st.session_state.users_db[email]["max_workload"] = new_max
                    add_audit(f"User account {email} updated by administrator", "Admin")
                    st.success("Account updated.")
                    st.rerun()
            if email != st.session_state.current_user:
                if st.button(f"Deactivate {u['name']}", key=f"deact_{email}"):
                    active_tasks = [t for t in user_tasks.values() if t["status"] in ["Pending", "In Progress"]]
                    if active_tasks:
                        st.warning(f"Warning: {len(active_tasks)} active tasks. Deactivating anyway.")
                    del st.session_state.users_db[email]
                    add_audit(f"User account {email} deactivated by administrator", "Admin")
                    st.success("Account deactivated.")
                    st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><span class="accent-bar"></span>System Role Distribution</div>', unsafe_allow_html=True)
    role_dist = defaultdict(int)
    for u in st.session_state.users_db.values():
        role_dist[u["role"]] += 1
    fig_roles = go.Figure(go.Pie(
        labels=list(role_dist.keys()), values=list(role_dist.values()),
        hole=0.55,
        marker=dict(colors=["#dc3545", "#003366", "#28a745", "#e8b931"]),
        textinfo='label+value'
    ))
    fig_roles.update_layout(height=280, paper_bgcolor='rgba(0,0,0,0)',
                             font=dict(family="Open Sans", color="#003366"),
                             margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_roles, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_availability_settings():
    user = st.session_state.users_db[st.session_state.current_user]
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><span class="accent-bar"></span>My Availability Settings</div>', unsafe_allow_html=True)
    with st.form("availability_form"):
        new_weekly = st.number_input("Weekly Available Hours", value=user.get("weekly_hours", 40), min_value=1, max_value=80)
        new_max = st.number_input("Maximum Workload Threshold (h/week)", value=user.get("max_workload", 40), min_value=1, max_value=80)
        if st.form_submit_button("Update Availability"):
            st.session_state.users_db[st.session_state.current_user]["weekly_hours"] = new_weekly
            st.session_state.users_db[st.session_state.current_user]["max_workload"] = new_max
            add_audit("Availability settings updated", "Profile")
            st.success("Availability updated successfully.")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def render_footer():
    st.markdown("""
    <div class="footer-bar">
        <strong>DNaaS</strong> &mdash; Deadline Negotiation as a Service &bull;
        Deadline Solutions Group &bull; COMP-699 Professional Seminar &bull; Spring 2026
    </div>
    """, unsafe_allow_html=True)

def main():
    if not st.session_state.logged_in:
        render_login()
        return

    render_topnav()

    page = st.session_state.current_page
    if page == "Dashboard":
        render_dashboard()
    elif page == "Projects":
        render_projects()
    elif page == "Tasks":
        render_tasks()
    elif page == "Workload Analysis":
        render_workload()
    elif page == "Negotiations":
        render_negotiations()
    elif page == "Reports":
        render_reports()
    elif page == "Audit Logs":
        render_audit_logs()
    elif page == "User Management":
        render_user_management()

    render_footer()

if __name__ == "__main__":
    main()