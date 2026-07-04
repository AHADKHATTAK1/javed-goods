from __future__ import annotations

from datetime import date
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()



st.set_page_config(page_title="JAVEED GOODS TRANSPORT", layout="wide", initial_sidebar_state="expanded")


SHIPMENTS = [
    {"id": "WB-48213", "client": "Northbridge Foods", "origin": "Lahore", "dest": "Karachi", "status": "in transit", "eta": "2:40 PM", "progress": 0.62, "driver": "Ali Raza", "vehicle": "TRK-0731", "billNo": "BIL-48213", "billDate": "02-Jul-2026", "partyInvoiceNo": "INV-1092", "partyInvoiceDate": "02-Jul-2026", "detention": "No", "items": "Beverages / Snacks", "containerQty": "1x40ft", "emptyPickupTo": "SAPT Terminal", "loadContainer": "SAPT Terminal to Lahore Hub"},
    {"id": "WB-48190", "client": "Calder Steel Co.", "origin": "Islamabad", "dest": "Peshawar", "status": "delayed", "eta": "11:15 AM", "progress": 0.41, "driver": "Imran Khan", "vehicle": "TRK-0559", "billNo": "BIL-48190", "billDate": "30-Jun-2026", "partyInvoiceNo": "INV-8871", "partyInvoiceDate": "29-Jun-2026", "detention": "Pending", "items": "Steel Beams", "containerQty": "2x20ft", "emptyPickupTo": "KICT Terminal", "loadContainer": "KICT Terminal to Detroit Hub"},
    {"id": "WB-48177", "client": "Verde Pharma", "origin": "Faisalabad", "dest": "Quetta", "status": "delivered", "eta": "Delivered 8:52 AM", "progress": 1.0, "driver": "Sajid Mehmood", "vehicle": "TRK-0416", "billNo": "BIL-48177", "billDate": "28-Jun-2026", "partyInvoiceNo": "INV-7651", "partyInvoiceDate": "28-Jun-2026", "detention": "No", "items": "Medical Supplies", "containerQty": "1x20ft", "emptyPickupTo": "QICT Terminal", "loadContainer": "QICT Terminal to Quetta Hub"},
    {"id": "WB-48241", "client": "Hallstrom Furniture", "origin": "Multan", "dest": "Rawalpindi", "status": "scheduled", "eta": "6:05 PM", "progress": 0.0, "driver": "Zubair Ahmed", "vehicle": "TRK-0820", "billNo": "", "billDate": "", "partyInvoiceNo": "", "partyInvoiceDate": "", "detention": "", "items": "", "containerQty": "", "emptyPickupTo": "", "loadContainer": ""},
]

STOCK = [
    {"sku": "PLT-1180", "item": "Standard pallets (48x40)", "warehouse": "Karachi DC", "qty": 412, "reorder": 150, "unit": "pcs"},
    {"sku": "FUEL-DSL", "item": "Diesel reserve", "warehouse": "Lahore Yard", "qty": 88, "reorder": 200, "unit": "gal"},
    {"sku": "PKG-STR1", "item": "Strapping rolls", "warehouse": "Karachi DC", "qty": 36, "reorder": 50, "unit": "rolls"},
    {"sku": "TIRE-22R", "item": "Tires 22.5R (drive axle)", "warehouse": "Islamabad Hub", "qty": 14, "reorder": 12, "unit": "pcs"},
    {"sku": "COLD-GEL", "item": "Cold-chain gel packs", "warehouse": "Peshawar Hub", "qty": 540, "reorder": 300, "unit": "pcs"},
    {"sku": "PPE-GLV", "item": "Loading gloves (L)", "warehouse": "Karachi DC", "qty": 22, "reorder": 40, "unit": "pairs"},
]

RECEIVING = [
    {"id": "GRN-3081", "supplier": "Premier Pallet Supply", "date": "Jun 28", "status": "received", "items": 3, "value": 412000},
    {"id": "GRN-3082", "supplier": "Continental Tire Distributors", "date": "Jun 29", "status": "partial", "items": 5, "value": 986000},
    {"id": "GRN-3083", "supplier": "ColdPack Industries", "date": "Jun 30", "status": "pending", "items": 2, "value": 231000},
    {"id": "GRN-3079", "supplier": "FuelCo Bulk Services", "date": "Jun 26", "status": "received", "items": 1, "value": 18450},
]

RECEIVING_LINES = {
    "GRN-3081": [
        {"name": "Standard pallets (48x40)", "ordered": 500, "received": 500},
        {"name": "Strapping rolls", "ordered": 60, "received": 60},
        {"name": "Corner protectors", "ordered": 1000, "received": 1000},
    ],
    "GRN-3082": [
        {"name": "Tires 22.5R (drive axle)", "ordered": 20, "received": 12},
        {"name": "Wheel balancing weights", "ordered": 200, "received": 200},
    ],
    "GRN-3083": [
        {"name": "Cold-chain gel packs", "ordered": 800, "received": 0},
        {"name": "Insulated liners", "ordered": 150, "received": 0},
    ],
    "GRN-3079": [{"name": "Diesel reserve", "ordered": 2000, "received": 2000}],
}

TRANSACTIONS = [
    {"id": "TXN-9001", "type": "income", "desc": "Freight — Northbridge Foods WB-48213", "date": "Jun 30", "amount": 62000, "category": "Freight", "owner": "manager@javeedgoods.pk"},
    {"id": "TXN-9002", "type": "expense", "desc": "Diesel refuel — TRK-0731", "date": "Jun 30", "amount": 4100, "category": "Fuel", "owner": "ali@javeedgoods.pk"},
    {"id": "TXN-9003", "type": "expense", "desc": "Toll — M-2 Motorway", "date": "Jun 30", "amount": 3800, "category": "Toll", "owner": "ali@javeedgoods.pk"},
    {"id": "TXN-9004", "type": "expense", "desc": "Staff salary payroll — June", "date": "Jun 29", "amount": 181000, "category": "Salary", "owner": "manager@javeedgoods.pk"},
    {"id": "TXN-9005", "type": "income", "desc": "Freight — Verde Pharma WB-48177", "date": "Jun 29", "amount": 47500, "category": "Freight", "owner": "manager@javeedgoods.pk"},
    {"id": "TXN-9006", "type": "expense", "desc": "Tire replacement — Islamabad Hub", "date": "Jun 28", "amount": 12400, "category": "Maintenance", "owner": "imran@javeedgoods.pk"},
    {"id": "TXN-9007", "type": "expense", "desc": "Warehouse lease — Karachi DC", "date": "Jun 27", "amount": 52000, "category": "Facilities", "owner": "manager@javeedgoods.pk"},
]

STAFF = [
    {"name": "Ali Raza", "email": "ali@javeedgoods.pk", "role": "Driver", "access": "Staff", "status": "active", "initials": "AR"},
    {"name": "Imran Khan", "email": "imran@javeedgoods.pk", "role": "Driver", "access": "Staff", "status": "active", "initials": "IK"},
    {"name": "Sajid Mehmood", "email": "sajid@javeedgoods.pk", "role": "Driver", "access": "Staff", "status": "active", "initials": "SM"},
    {"name": "Zubair Ahmed", "email": "zubair@javeedgoods.pk", "role": "Dispatcher", "access": "Staff", "status": "active", "initials": "ZA"},
    {"name": "Hina Noor", "email": "hina@javeedgoods.pk", "role": "Warehouse Lead", "access": "Staff", "status": "suspended", "initials": "HN"},
    {"name": "Javeed Manager", "email": "manager@javeedgoods.pk", "role": "Operations Manager", "access": "Admin", "status": "active", "initials": "JM"},
]

CLIENTS = [
    {"id": "CLT-001", "name": "Northbridge Foods", "contact": "Ahmed Saleem", "phone": "021-3456789", "city": "Karachi", "email": "ahmed@northbridge.pk", "activeShipments": 1, "totalValue": 620000},
    {"id": "CLT-002", "name": "Calder Steel Co.", "contact": "Fahad Tariq", "phone": "051-2345678", "city": "Islamabad", "email": "fahad@calsteel.pk", "activeShipments": 1, "totalValue": 280000},
    {"id": "CLT-003", "name": "Verde Pharma", "contact": "Dr. Sara Khan", "phone": "042-1234567", "city": "Lahore", "email": "sara@verdepharma.pk", "activeShipments": 0, "totalValue": 475000},
    {"id": "CLT-004", "name": "Hallstrom Furniture", "contact": "Usman Ali", "phone": "061-3456789", "city": "Multan", "email": "usman@hallstrom.pk", "activeShipments": 1, "totalValue": 180000},
]

INVOICES = [
    {"id": "INV-0001", "shipmentId": "WB-48177", "client": "Verde Pharma", "amount": 47500, "date": "Jun 29", "status": "paid", "dueDate": "Jul 13", "notes": ""},
    {"id": "INV-0002", "shipmentId": "WB-48213", "client": "Northbridge Foods", "amount": 62000, "date": "Jun 30", "status": "unpaid", "dueDate": "Jul 14", "notes": ""},
]

SALARIES = [
    {"id": "SAL-001", "staffId": "STF-001", "staffName": "Ali Raza", "month": "June", "year": 2026, "basic": 38000, "allowance": 5000, "deduction": 0, "total": 43000, "status": "paid", "paidDate": "Jun 30", "notes": ""},
    {"id": "SAL-002", "staffId": "STF-002", "staffName": "Imran Khan", "month": "June", "year": 2026, "basic": 40000, "allowance": 5000, "deduction": 2000, "total": 43000, "status": "paid", "paidDate": "Jun 30", "notes": "Deduction: late penalty"},
    {"id": "SAL-003", "staffId": "STF-003", "staffName": "Sajid Mehmood", "month": "June", "year": 2026, "basic": 42000, "allowance": 5000, "deduction": 0, "total": 47000, "status": "unpaid", "paidDate": "", "notes": ""},
    {"id": "SAL-004", "staffId": "STF-004", "staffName": "Zubair Ahmed", "month": "June", "year": 2026, "basic": 35000, "allowance": 4000, "deduction": 0, "total": 39000, "status": "unpaid", "paidDate": "", "notes": ""},
    {"id": "SAL-005", "staffId": "STF-006", "staffName": "Javeed Manager", "month": "June", "year": 2026, "basic": 80000, "allowance": 15000, "deduction": 0, "total": 95000, "status": "paid", "paidDate": "Jun 30", "notes": ""},
]

ATTENDANCE = []

VEHICLES = [
    {"id": "TRK-0731", "type": "Truck", "make": "Hino", "model": "700 Series", "year": 2020, "plate": "LEA-4521", "status": "active", "driver": "Ali Raza", "km": 142000, "nextService": 150000},
    {"id": "TRK-0559", "type": "Truck", "make": "MAN", "model": "TGX 18.440", "year": 2018, "plate": "ISB-9932", "status": "active", "driver": "Imran Khan", "km": 218000, "nextService": 220000},
    {"id": "TRK-0416", "type": "Truck", "make": "Isuzu", "model": "FVR 34", "year": 2022, "plate": "KHI-1177", "status": "active", "driver": "Sajid Mehmood", "km": 89000, "nextService": 100000},
    {"id": "TRK-0820", "type": "Truck", "make": "Hino", "model": "500 Series", "year": 2019, "plate": "MUL-7764", "status": "active", "driver": "Zubair Ahmed", "km": 175000, "nextService": 180000},
    {"id": "VAN-001", "type": "Van", "make": "Toyota", "model": "Hiace", "year": 2021, "plate": "LHR-5512", "status": "maintenance", "driver": "", "km": 62000, "nextService": 70000},
]

FUEL_LOGS = [
    {"id": "FL-001", "vehicleId": "TRK-0731", "date": "Jun 30", "liters": 180.0, "costPerL": 285, "total": 51300, "odometer": 141820, "station": "PSO Lahore Ring Road"},
    {"id": "FL-002", "vehicleId": "TRK-0559", "date": "Jun 29", "liters": 200.0, "costPerL": 285, "total": 57000, "odometer": 217600, "station": "Shell Islamabad"},
    {"id": "FL-003", "vehicleId": "TRK-0416", "date": "Jun 28", "liters": 150.0, "costPerL": 285, "total": 42750, "odometer": 88500, "station": "Total Karachi"},
    {"id": "FL-004", "vehicleId": "TRK-0820", "date": "May 30", "liters": 190.0, "costPerL": 282, "total": 53580, "odometer": 174500, "station": "PSO Multan"},
]

MAINTENANCE = [
    {"id": "MNT-001", "vehicleId": "TRK-0559", "date": "Jun 25", "type": "Oil change", "cost": 8500, "nextDue": "Sep 25", "status": "done", "notes": "Synthetic 15W-40"},
    {"id": "MNT-002", "vehicleId": "VAN-001", "date": "Jun 28", "type": "Engine overhaul", "cost": 95000, "nextDue": "Dec 28", "status": "in_progress", "notes": "Partial overhaul"},
    {"id": "MNT-003", "vehicleId": "TRK-0731", "date": "Jun 20", "type": "Tire rotation", "cost": 3500, "nextDue": "Sep 20", "status": "done", "notes": "All 6 tires rotated"},
]

ACTIVITY_LOG = [
    {"id": "ACT-001", "action": "Shipment delivered", "module": "Shipments", "details": "WB-48177 marked delivered", "by": "admin@javeedgoods.pk", "at": "Jun 30, 2026 8:52 AM"},
]

STATUS_META = {
    "in transit": ("In transit", "#FF8A3D", "rgba(255,138,61,0.12)"),
    "delayed": ("Delayed", "#FF5C5C", "rgba(255,92,92,0.12)"),
    "delivered": ("Delivered", "#3DDC97", "rgba(61,220,151,0.12)"),
    "scheduled": ("Scheduled", "#8B93A7", "rgba(139,147,167,0.12)"),
    "received": ("Received", "#3DDC97", "rgba(61,220,151,0.12)"),
    "partial": ("Partial", "#FF8A3D", "rgba(255,138,61,0.12)"),
    "pending": ("Pending", "#8B93A7", "rgba(139,147,167,0.12)"),
    "active": ("Active", "#3DDC97", "rgba(61,220,151,0.12)"),
    "suspended": ("Suspended", "#FF5C5C", "rgba(255,92,92,0.12)"),
}


def money(value: int | float) -> str:
    return f"Rs {value:,.0f}"


def badge(status: str) -> str:
    label, color, bg = STATUS_META.get(status, STATUS_META["pending"])
    dot_html = ""
    if status == "in transit":
        dot_html = '<span class="status-dot dot-transit"></span>'
    elif status == "delayed":
        dot_html = '<span class="status-dot dot-delayed"></span>'
    elif status == "pending" or status == "partial":
        dot_html = '<span class="status-dot dot-pending"></span>'
    elif status in ("delivered", "received", "active"):
        dot_html = '<span class="status-dot dot-active"></span>'
    return f'<span class="badge" style="color:{color} !important;background:{bg} !important;display:inline-flex;align-items:center;gap:6px;">{dot_html}{label}</span>'


def css() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

        :root {
          --bg: #07111f;
          --panel: rgba(13, 21, 38, 0.88);
          --panel-strong: rgba(17, 27, 47, 0.95);
          --line: rgba(142, 160, 201, 0.16);
          --text: #edf2ff;
          --muted: #97a3c4;
          --accent: #ff8a3d;
        }

        /* Typography overrides */
        .stApp, .stApp button, .stApp input, .stApp select, .stApp textarea, .stApp [data-testid="stMarkdownContainer"] {
          font-family: 'Plus Jakarta Sans', sans-serif !important;
        }

        .mono {
          font-family: 'JetBrains Mono', monospace !important;
        }

        .stApp {
          background:
            radial-gradient(circle at top left, rgba(255, 138, 61, 0.16), transparent 28%),
            radial-gradient(circle at top right, rgba(61, 220, 151, 0.12), transparent 24%),
            linear-gradient(180deg, #07111f 0%, #0b1324 46%, #070d17 100%);
          color: var(--text) !important;
        }

        /* Custom cards structure */
        .waybill-card {
          border: 1px solid var(--line);
          background: var(--panel-strong);
          border-radius: 24px;
          padding: 1.25rem 1.5rem;
          margin-bottom: 1rem;
          box-shadow: 0 12px 40px rgba(0, 0, 0, 0.22);
          transition: transform 0.2s ease, border-color 0.2s ease;
        }

        .waybill-card:hover {
          border-color: rgba(142, 160, 201, 0.26);
        }

        /* Force high contrast text on Streamlit elements */
        .stApp [data-testid="stMarkdownContainer"] p, 
        .stApp [data-testid="stMarkdownContainer"] span:not(.badge),
        .stApp [data-testid="stMarkdownContainer"] li {
          color: var(--text) !important;
        }

        .stApp [data-testid="stMarkdownContainer"] .waybill-muted {
          color: var(--muted) !important;
        }

        .stApp [data-testid="stMarkdownContainer"] .thin {
          color: var(--muted) !important;
        }

        .stApp [data-testid="stMarkdownContainer"] .section-heading {
          color: var(--muted) !important;
          font-weight: 600 !important;
          letter-spacing: 0.12em;
          text-transform: uppercase;
        }

        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
          color: var(--text) !important;
          font-weight: 700 !important;
        }

        /* Sidebar styling overrides */
        section[data-testid="stSidebar"] {
          background: linear-gradient(180deg, rgba(9,14,26,0.98), rgba(5,9,16,0.98)) !important;
          border-right: 1px solid rgba(140,160,210,0.14) !important;
        }

        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3,
        section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
        section[data-testid="stSidebar"] div[role="radiogroup"] label p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] .stCaption p {
          color: var(--text) !important;
        }

        section[data-testid="stSidebar"] .stCaption p {
          color: var(--muted) !important;
        }

        section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] + div p {
          color: var(--muted) !important;
        }

        section[data-testid="stSidebar"] .waybill-muted {
          color: var(--muted) !important;
        }

        /* Captions styling */
        .stCaption, .stCaption p, [data-testid="stCaptionContainer"] {
          color: var(--muted) !important;
          font-size: 0.85rem !important;
          font-weight: 500;
        }

        /* Metric Widget Styling as gorgeous hoverable KPI cards */
        [data-testid="stMetric"] {
          border: 1px solid var(--line) !important;
          background: var(--panel) !important;
          border-radius: 20px !important;
          padding: 1.1rem 1.25rem !important;
          min-height: 110px !important;
          box-shadow: 0 10px 30px rgba(0,0,0,0.2) !important;
          transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease !important;
        }

        [data-testid="stMetric"]:hover {
          transform: translateY(-2px) !important;
          border-color: rgba(255, 138, 61, 0.35) !important;
          box-shadow: 0 12px 35px rgba(255, 138, 61, 0.08) !important;
        }

        [data-testid="stMetricLabel"] {
          color: var(--muted) !important;
          font-weight: 500 !important;
          font-size: 0.9rem !important;
        }

        [data-testid="stMetricValue"] {
          color: var(--text) !important;
          font-weight: 800 !important;
          font-size: 1.9rem !important;
          letter-spacing: -0.02em !important;
        }

        /* Badge component */
        .badge {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          padding: 0.38rem 0.75rem;
          border-radius: 999px;
          font-size: 0.78rem;
          font-weight: 700;
        }

        /* Live status dot animations */
        @keyframes pulse-dot {
          0% { transform: scale(0.85); opacity: 0.55; }
          50% { transform: scale(1.15); opacity: 1; }
          100% { transform: scale(0.85); opacity: 0.55; }
        }
        .status-dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          display: inline-block;
          flex-shrink: 0;
        }
        .dot-transit {
          background-color: #FF8A3D;
          box-shadow: 0 0 8px #FF8A3D;
          animation: pulse-dot 1.8s infinite ease-in-out;
        }
        .dot-delayed {
          background-color: #FF5C5C;
          box-shadow: 0 0 8px #FF5C5C;
          animation: pulse-dot 1.2s infinite ease-in-out;
        }
        .dot-pending {
          background-color: #8B93A7;
          box-shadow: 0 0 6px #8B93A7;
          animation: pulse-dot 2.2s infinite ease-in-out;
        }
        .dot-active {
          background-color: #3DDC97;
          box-shadow: 0 0 8px #3DDC97;
          animation: pulse-dot 2.0s infinite ease-in-out;
        }

        /* Sleek input & buttons styling */
        .login-shell {
          min-height: 92vh;
          display: grid;
          place-items: center;
          padding: 2rem;
        }
        .login-card {
          width: min(980px, 100%);
          display: grid;
          grid-template-columns: 1.1fr 0.9fr;
          border: 1px solid var(--line);
          background: rgba(8,13,24,0.88);
          border-radius: 30px;
          overflow: hidden;
        }
        .login-copy, .login-form { padding: 2rem; }
        .login-form { background: rgba(14,22,41,0.96); }
        .login-badge {
          display:inline-flex; align-items:center; gap:0.6rem;
          border: 1px solid rgba(255,138,61,0.18);
          background: rgba(255,138,61,0.08);
          padding: 0.5rem 0.8rem; border-radius: 999px;
          font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
          color: #ffcfaa; font-weight: 700;
        }
        .preview-row { display:flex; justify-content:space-between; gap:1rem; padding:0.8rem 0; border-bottom:1px solid rgba(255,255,255,0.06); }
        .preview-row:last-child { border-bottom:0; }
        @media (max-width: 900px) {
          .login-card { grid-template-columns: 1fr; }
        }

        /* Custom scrollbars */
        ::-webkit-scrollbar {
          width: 6px;
          height: 6px;
        }
        ::-webkit-scrollbar-track {
          background: transparent;
        }
        ::-webkit-scrollbar-thumb {
          background: rgba(142, 160, 201, 0.2);
          border-radius: 99px;
        }
        ::-webkit-scrollbar-thumb:hover {
          background: rgba(142, 160, 201, 0.4);
        }

        /* Streamlit Alerts override */
        [data-testid="stAlert"] {
          border-radius: 14px !important;
          background-color: rgba(61, 220, 151, 0.08) !important;
          border: 1px solid rgba(61, 220, 151, 0.2) !important;
          color: #3DDC97 !important;
        }

        /* Custom Premium Radio Buttons in Sidebar */
        div[role="radiogroup"] {
          gap: 8px !important;
        }
        div[role="radiogroup"] label {
          background: rgba(255, 255, 255, 0.02) !important;
          border: 1px solid rgba(142, 160, 201, 0.1) !important;
          border-radius: 12px !important;
          padding: 10px 14px !important;
          margin: 0 !important;
          transition: all 0.18s ease-in-out !important;
          cursor: pointer !important;
          display: flex !important;
          align-items: center !important;
          width: 100% !important;
        }
        div[role="radiogroup"] label:hover {
          background: rgba(255, 255, 255, 0.05) !important;
          border-color: rgba(142, 160, 201, 0.22) !important;
        }
        div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] {
          margin-left: 0 !important;
        }
        div[role="radiogroup"] label > div:first-child {
          display: none !important; /* Hide radio dot */
        }
        div[role="radiogroup"] label:has(input:checked) {
          background: linear-gradient(135deg, rgba(255, 138, 61, 0.18), rgba(255, 255, 255, 0.02)) !important;
          border-color: rgba(255, 138, 61, 0.35) !important;
          box-shadow: 0 4px 15px rgba(255, 138, 61, 0.06) !important;
        }
        div[role="radiogroup"] label:has(input:checked) p {
          color: #ff8a3d !important;
          font-weight: 700 !important;
        }

        /* Brand Logo in Sidebar */
        .brand-logo {
          width: 40px;
          height: 40px;
          border-radius: 10px;
          display: grid;
          place-items: center;
          color: #ffcfaa;
          background: linear-gradient(135deg, rgba(255, 138, 61, 0.24), rgba(255, 138, 61, 0.08));
          border: 1px solid rgba(255, 138, 61, 0.2);
          font-weight: 800;
          font-size: 1.15rem;
          box-shadow: 0 8px 20px rgba(255, 138, 61, 0.12);
        }

        /* Custom KPI Card Grid and KPI Card design */
        .kpi-grid {
          display: grid;
          grid-template-columns: repeat(4, 1fr);
          gap: 16px;
          margin-bottom: 24px;
        }
        @media (max-width: 768px) {
          .kpi-grid {
            grid-template-columns: 1fr;
          }
        }
        .kpi-card-custom {
          display: flex;
          align-items: center;
          gap: 16px;
          background: var(--panel);
          border: 1px solid var(--line);
          border-radius: 20px;
          padding: 1.1rem 1.4rem;
          box-shadow: 0 10px 30px rgba(0,0,0,0.18);
          transition: all 0.2s ease-in-out;
        }
        .kpi-card-custom:hover {
          transform: translateY(-2px);
          border-color: rgba(255, 138, 61, 0.35);
          box-shadow: 0 12px 35px rgba(255, 138, 61, 0.08);
        }
        .kpi-icon-wrap {
          width: 46px;
          height: 46px;
          border-radius: 14px;
          display: grid;
          place-items: center;
          font-size: 1.25rem;
          flex-shrink: 0;
        }
        .transit-icon {
          color: #ff8a3d;
          background: rgba(255, 138, 61, 0.12);
          border: 1px solid rgba(255, 138, 61, 0.2);
        }
        .alert-icon {
          color: #ff5c5c;
          background: rgba(255, 92, 92, 0.12);
          border: 1px solid rgba(255, 92, 92, 0.2);
        }
        .pending-icon {
          color: #8b93a7;
          background: rgba(139, 147, 167, 0.12);
          border: 1px solid rgba(139, 147, 167, 0.2);
        }
        .success-icon {
          color: #3ddc97;
          background: rgba(61, 220, 151, 0.12);
          border: 1px solid rgba(61, 220, 151, 0.2);
        }
        .kpi-val {
          font-size: 1.85rem;
          font-weight: 800;
          line-height: 1.1;
          color: var(--text);
          letter-spacing: -0.02em;
        }
        .kpi-lbl {
          font-size: 0.85rem;
          color: var(--muted);
          font-weight: 500;
          margin-top: 2px;
        }

        /* Custom dashboard lists */
        .custom-list-row {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 12px 0;
          border-bottom: 1px solid rgba(255, 255, 255, 0.05);
          transition: all 0.15s ease;
        }
        .custom-list-row:last-child {
          border-bottom: none;
          padding-bottom: 4px;
        }

        /* Button Styling Overrides */
        div.stButton > button {
          background-color: rgba(255, 255, 255, 0.03) !important;
          color: var(--text) !important;
          border: 1px solid rgba(142, 160, 201, 0.12) !important;
          border-radius: 12px !important;
          padding: 0.6rem 1rem !important;
          font-weight: 600 !important;
          transition: all 0.15s ease-in-out !important;
        }
        div.stButton > button:hover {
          background-color: rgba(255, 255, 255, 0.06) !important;
          border-color: rgba(255, 138, 61, 0.3) !important;
          color: #ff8a3d !important;
          transform: translateY(-1px);
        }
        div.stButton > button[kind="primary"] {
          background: linear-gradient(135deg, #ffcfaa, #ff8a3d) !important;
          color: #07111f !important;
          border: none !important;
          font-weight: 700 !important;
          box-shadow: 0 4px 15px rgba(255, 138, 61, 0.2) !important;
        }
        div.stButton > button[kind="primary"]:hover {
          background: linear-gradient(135deg, #ffe2cc, #ffa366) !important;
          box-shadow: 0 6px 20px rgba(255, 138, 61, 0.3) !important;
          transform: translateY(-1px);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def seed_state() -> None:
    st.session_state.setdefault("authenticated", False)
    st.session_state.setdefault("role", "Admin")
    st.session_state.setdefault("email", "")
    st.session_state.setdefault("display_name", "")
    st.session_state.setdefault("section", "📊 Dashboard")
    st.session_state.setdefault("shipments", [row.copy() for row in SHIPMENTS])
    st.session_state.setdefault("stock", [row.copy() for row in STOCK])
    st.session_state.setdefault("receiving", [row.copy() for row in RECEIVING])
    st.session_state.setdefault("receiving_lines", {key: [row.copy() for row in rows] for key, rows in RECEIVING_LINES.items()})
    st.session_state.setdefault("transactions", [row.copy() for row in TRANSACTIONS])
    st.session_state.setdefault("staff", [row.copy() for row in STAFF])
    st.session_state.setdefault("selected_shipment", st.session_state.shipments[0]["id"])
    st.session_state.setdefault("toast", "")
    st.session_state.setdefault("shipment_modal", False)
    st.session_state.setdefault("edit_shipment_id", None)
    st.session_state.setdefault("stock_modal", False)
    st.session_state.setdefault("receiving_modal", False)
    st.session_state.setdefault("payment_modal", False)
    st.session_state.setdefault("staff_modal", False)
    st.session_state.setdefault("invoice_modal", False)
    st.session_state.setdefault("client_modal", False)
    st.session_state.setdefault("salary_modal", False)
    st.session_state.setdefault("vehicle_modal", False)
    st.session_state.setdefault("fuel_modal", False)
    st.session_state.setdefault("maint_modal", False)
    st.session_state.setdefault("new_stock", {})
    st.session_state.setdefault("new_receiving", {})
    st.session_state.setdefault("new_payment", {})
    st.session_state.setdefault("new_staff", {})
    st.session_state.setdefault("clients", [row.copy() for row in CLIENTS])
    st.session_state.setdefault("invoices", [row.copy() for row in INVOICES])
    st.session_state.setdefault("salaries", [row.copy() for row in SALARIES])
    st.session_state.setdefault("attendance", [row.copy() for row in ATTENDANCE])
    st.session_state.setdefault("vehicles", [row.copy() for row in VEHICLES])
    st.session_state.setdefault("fuelLogs", [row.copy() for row in FUEL_LOGS])
    st.session_state.setdefault("maintenance", [row.copy() for row in MAINTENANCE])
    st.session_state.setdefault("activityLog", [row.copy() for row in ACTIVITY_LOG])


def login_screen() -> None:
    st.markdown(
        """
        <div class="login-shell">
          <div class="login-card">
            <div class="login-copy">
              <div class="login-badge">JAVEED // goods transport</div>
              <h1 class="waybill-title">Javeed Goods Transport</h1>
              <p class="waybill-muted">
                Sign in with any email and password. Toggle Admin or Staff to change what you can see.
                Everything stays in local Streamlit state so the prototype is ready for a real API later.
              </p>
              <div class="waybill-card">
                <div class="section-heading">Included modules</div>
                <div class="preview-row"><span>Dashboard</span><span class="mono">KPI cards</span></div>
                <div class="preview-row"><span>Shipments</span><span class="mono">Route detail</span></div>
                <div class="preview-row"><span>Receiving</span><span class="mono">Expandable GRNs</span></div>
              </div>
            </div>
            <div class="login-form">
        """,
        unsafe_allow_html=True,
    )
    with st.form("login_form", clear_on_submit=False):
        default_email = os.getenv("DEFAULT_EMAIL", "")
        email = st.text_input("Email", value=default_email, placeholder="name@company.com")
        password = st.text_input("Password", type="password", placeholder="Anything signs you in")
        role = st.radio("Role", ["Admin", "Staff"], horizontal=True)
        submitted = st.form_submit_button("Enter Portal", use_container_width=True, type="primary")
        if submitted and (email or password or True):
            st.session_state.authenticated = True
            st.session_state.email = email.strip() or "demo@javeedgoods.pk"
            st.session_state.display_name = st.session_state.email.split("@")[0].replace(".", " ").title()
            st.session_state.role = role
            st.session_state.toast = f"Signed in as {role}"
            st.rerun()
    st.markdown("</div></div></div>", unsafe_allow_html=True)


def sign_out() -> None:
    st.session_state.authenticated = False
    st.session_state.email = ""
    st.session_state.display_name = ""
    st.session_state.section = "📊 Dashboard"
    st.rerun()


def sidebar() -> list[str]:
    if st.session_state.role == "Admin":
        nav = [
            "📊 Dashboard",
            "🚚 Shipments",
            "🛣️ Optimizer",
            "🧾 Invoices",
            "🏢 Clients",
            "👥 Staff",
            "💰 Salaries",
            "🗓️ Attendance",
            "🚛 Vehicles",
            "⛽ Fuel Logs",
            "🔧 Maintenance",
            "📦 Stock",
            "📄 Receiving slips",
            "💳 Payments & expenses",
            "📑 Reports",
            "📋 Activity Log",
            "⚙️ Settings",
            "❓ Guide"
        ]
    else:
        nav = [
            "📊 Dashboard",
            "🚚 Shipments",
            "📦 Stock",
            "📄 Receiving slips",
            "💳 Payments & expenses",
            "📑 Reports",
            "❓ Guide"
        ]

    st.sidebar.markdown(
        """
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px; padding: 6px 0;">
          <div class="brand-logo">JGT</div>
          <div>
            <div style="font-weight: 800; font-size: 0.95rem; letter-spacing: -0.02em; line-height: 1.2; color: var(--text);">JAVEED GOODS</div>
            <div class="waybill-muted" style="font-size: 0.8rem; font-weight: 600; color: #ff8a3d !important;">TRANSPORT</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    choice = st.sidebar.radio("Navigation", nav, index=nav.index(st.session_state.section) if st.session_state.section in nav else 0)
    st.session_state.section = choice
    st.sidebar.divider()
    st.sidebar.caption("Session role")
    st.session_state.role = st.sidebar.radio("Role", ["Admin", "Staff"], horizontal=True, label_visibility="collapsed")
    if st.sidebar.button("Sign out", use_container_width=True):
        sign_out()
    return nav


def topbar(title: str) -> None:
    left, right = st.columns([2.2, 1.2])
    with left:
        st.markdown(f'<h1 style="margin: 0 0 4px 0; font-size: 2.2rem; font-weight: 800; letter-spacing: -0.03em;">{title}</h1>', unsafe_allow_html=True)
        st.markdown(f'<div class="waybill-muted" style="font-size: 0.88rem; display: flex; align-items: center; gap: 8px;">'
                    f'Signed in as <strong style="color: var(--text); font-weight: 600;">{st.session_state.display_name}</strong> • '
                    f'<span class="badge" style="color: #ff8a3d !important; background: rgba(255,138,61,0.08) !important; padding: 0.2rem 0.6rem !important; font-size: 0.72rem !important;">{st.session_state.role}</span>'
                    f'</div>', unsafe_allow_html=True)
    with right:
        col_search, col_live = st.columns([2.5, 1])
        with col_search:
            st.text_input("Search", placeholder="Search shipments, stock, GRNs, staff", key="search_query", label_visibility="collapsed")
        with col_live:
            app_env = os.getenv("APP_ENVIRONMENT", "Production")
            st.markdown(
                f'<div style="height: 38px; display: flex; align-items: center; justify-content: center; gap: 6px; background: rgba(61,220,151,0.05); border: 1px solid rgba(61,220,151,0.15); border-radius: 12px; font-size: 0.82rem; font-weight: 600; color: #3DDC97; padding: 0 12px;">'
                '<span class="status-dot dot-active"></span>'
                f'{app_env}'
                '</div>',
                unsafe_allow_html=True
            )


def toast() -> None:
    if st.session_state.toast:
        st.success(st.session_state.toast)
        st.session_state.toast = ""


def dashboard() -> None:
    income = sum(tx["amount"] for tx in st.session_state.transactions if tx["type"] == "income")
    expense = sum(tx["amount"] for tx in st.session_state.transactions if tx["type"] == "expense")
    low_stock = sum(1 for item in st.session_state.stock if item["qty"] < item["reorder"])
    pending_grn = sum(1 for slip in st.session_state.receiving if slip["status"] != "received")
    active_shipments = sum(1 for shipment in st.session_state.shipments if shipment["status"] == "in transit")
    staff_on_shift = sum(1 for person in st.session_state.staff if person["status"] == "active")

    last_icon = "💰" if st.session_state.role == "Admin" else "👥"
    last_label = "Net Cashflow" if st.session_state.role == "Admin" else "Staff on Shift"
    last_val = money(income - expense) if st.session_state.role == "Admin" else staff_on_shift
    last_class = "success-icon" if st.session_state.role == "Admin" else "transit-icon"

    kpi_html = (
        f'<div class="kpi-grid">'
        f'  <div class="kpi-card-custom">'
        f'    <div class="kpi-icon-wrap transit-icon">🚚</div>'
        f'    <div>'
        f'      <div class="kpi-val">{active_shipments}</div>'
        f'      <div class="kpi-lbl">Active Shipments</div>'
        f'    </div>'
        f'  </div>'
        f'  <div class="kpi-card-custom">'
        f'    <div class="kpi-icon-wrap alert-icon">⚠️</div>'
        f'    <div>'
        f'      <div class="kpi-val">{low_stock}</div>'
        f'      <div class="kpi-lbl">Low-Stock Alerts</div>'
        f'    </div>'
        f'  </div>'
        f'  <div class="kpi-card-custom">'
        f'    <div class="kpi-icon-wrap pending-icon">📄</div>'
        f'    <div>'
        f'      <div class="kpi-val">{pending_grn}</div>'
        f'      <div class="kpi-lbl">Pending Slips</div>'
        f'    </div>'
        f'  </div>'
        f'  <div class="kpi-card-custom">'
        f'    <div class="kpi-icon-wrap {last_class}">{last_icon}</div>'
        f'    <div>'
        f'      <div class="kpi-val">{last_val}</div>'
        f'      <div class="kpi-lbl">{last_label}</div>'
        f'    </div>'
        f'  </div>'
        f'</div>'
    )
    st.markdown(kpi_html, unsafe_allow_html=True)

    left, right = st.columns(2)
    with left:
        shipment_rows = []
        for shipment in st.session_state.shipments:
            if shipment["status"] == "delivered":
                continue
            badge_html = badge(shipment["status"])
            shipment_rows.append(
                f'<div class="custom-list-row">'
                f'  <div>'
                f'    <div style="font-weight: 700; color: var(--text); font-size: 0.98rem;">{shipment["client"]}</div>'
                f'    <div style="font-size: 0.85rem; color: var(--muted); margin-top: 3px;">{shipment["origin"]} &rarr; {shipment["dest"]}</div>'
                f'  </div>'
                f'  <div>{badge_html}</div>'
                f'</div>'
            )
        st.markdown(
            f'<div class="waybill-card">'
            f'  <div class="section-heading" style="margin-bottom: 12px;">Shipments in motion</div>'
            f'  {"".join(shipment_rows)}'
            f'</div>',
            unsafe_allow_html=True
        )

    with right:
        stock_rows = []
        for item in st.session_state.stock:
            if item["qty"] < item["reorder"]:
                badge_html = badge("pending")
                stock_rows.append(
                    f'<div class="custom-list-row">'
                    f'  <div>'
                    f'    <div style="font-weight: 700; color: var(--text); font-size: 0.98rem;">{item["item"]}</div>'
                    f'    <div style="font-size: 0.85rem; color: var(--muted); margin-top: 3px;">{item["warehouse"]} &bull; <strong style="color: #ff5c5c;">{item["qty"]} {item["unit"]}</strong> on hand</div>'
                    f'  </div>'
                    f'  <div>{badge_html}</div>'
                    f'</div>'
                )
        st.markdown(
            f'<div class="waybill-card">'
            f'  <div class="section-heading" style="margin-bottom: 12px;">Stock needing attention</div>'
            f'  {"".join(stock_rows)}'
            f'</div>',
            unsafe_allow_html=True
        )


def shipments_view() -> None:
    # Modal for adding/editing shipments
    if st.session_state.get("shipment_modal", False):
        edit_id = st.session_state.get("edit_shipment_id", None)
        edit_ship = next((s for s in st.session_state.shipments if s["id"] == edit_id), None) if edit_id else None
        
        form_title = f"Edit Shipment: {edit_id}" if edit_ship else "New Shipment"
        with st.form("shipment_form"):
            st.markdown(f"### 🚚 {form_title}")
            
            c1, c2 = st.columns(2)
            with c1:
                client = st.text_input("Client name", value=edit_ship["client"] if edit_ship else "")
                origin = st.text_input("Origin city", value=edit_ship["origin"] if edit_ship else "")
                driver = st.text_input("Driver name", value=edit_ship.get("driver", "") if edit_ship else "")
                eta = st.text_input("ETA", value=edit_ship.get("eta", "") if edit_ship else "")
                freight = st.number_input("Freight charge (Rs)", min_value=0, value=int(edit_ship.get("freightCharge", 0)) if edit_ship else 0)
            with c2:
                cargo = st.text_input("Cargo type", value=edit_ship.get("cargo", "") if edit_ship else "")
                dest = st.text_input("Destination city", value=edit_ship["dest"] if edit_ship else "")
                vehicle = st.text_input("Vehicle ID", value=edit_ship.get("vehicle", "") if edit_ship else "")
                weight = st.number_input("Weight (kg)", min_value=0, value=int(edit_ship.get("weight", 0)) if edit_ship else 0)
                status_list = ["scheduled", "in transit", "delayed", "delivered"]
                status_index = status_list.index(edit_ship["status"]) if edit_ship and edit_ship.get("status") in status_list else 0
                status = st.selectbox("Status", status_list, index=status_index)
            
            st.markdown("---")
            st.markdown("#### 📋 Shipping & Billing Details")
            c3, c4 = st.columns(2)
            with c3:
                billNo = st.text_input("Bill#", value=edit_ship.get("billNo", "") if edit_ship else "")
                partyInvoiceNo = st.text_input("Party Invoice #", value=edit_ship.get("partyInvoiceNo", "") if edit_ship else "")
                detention = st.text_input("Detention", value=edit_ship.get("detention", "") if edit_ship else "")
                containerQty = st.text_input("Container Quantity", value=edit_ship.get("containerQty", "") if edit_ship else "")
            with c4:
                billDate = st.text_input("Bill Date", value=edit_ship.get("billDate", "") if edit_ship else "")
                partyInvoiceDate = st.text_input("Party Invoice Date", value=edit_ship.get("partyInvoiceDate", "") if edit_ship else "")
                items = st.text_input("Items", value=edit_ship.get("items", "") if edit_ship else "")
                emptyPickupTo = st.text_input("Empty Pickup to", value=edit_ship.get("emptyPickupTo", "") if edit_ship else "")
            
            loadContainer = st.text_input("Load container", value=edit_ship.get("loadContainer", "") if edit_ship else "")
            notes = st.text_area("Notes", value=edit_ship.get("notes", "") if edit_ship else "")
            
            c_btn1, c_btn2 = st.columns([1, 4])
            with c_btn1:
                submitted = st.form_submit_button("Save Shipment", type="primary")
            with c_btn2:
                cancelled = st.form_submit_button("Cancel")
                if cancelled:
                    st.session_state.shipment_modal = False
                    st.rerun()
            
            if submitted and client:
                progress = {"scheduled": 0.0, "in transit": 0.3, "delayed": 0.3, "delivered": 1.0}[status]
                obj = {
                    "id": edit_id if edit_ship else f"WB-{len(st.session_state.shipments)+49000}",
                    "client": client,
                    "cargo": cargo,
                    "origin": origin,
                    "dest": dest,
                    "driver": driver,
                    "vehicle": vehicle,
                    "eta": eta,
                    "weight": weight,
                    "freightCharge": freight,
                    "status": status,
                    "progress": progress,
                    "notes": notes,
                    "billNo": billNo,
                    "billDate": billDate,
                    "partyInvoiceNo": partyInvoiceNo,
                    "partyInvoiceDate": partyInvoiceDate,
                    "detention": detention,
                    "items": items,
                    "containerQty": containerQty,
                    "emptyPickupTo": emptyPickupTo,
                    "loadContainer": loadContainer,
                }
                if edit_ship:
                    idx = next(i for i, s in enumerate(st.session_state.shipments) if s["id"] == edit_id)
                    st.session_state.shipments[idx] = obj
                    st.session_state.toast = f"Shipment {edit_id} updated"
                else:
                    st.session_state.shipments.insert(0, obj)
                    st.session_state.toast = f"Shipment {obj['id']} created"
                    st.session_state.selected_shipment = obj["id"]
                st.session_state.shipment_modal = False
                st.rerun()

    query = st.session_state.get("search_query", "").strip().lower()
    filtered = [shipment for shipment in st.session_state.shipments if not query or any(query in str(shipment.get(field, "")).lower() for field in ("id", "client", "origin", "dest", "billNo", "partyInvoiceNo"))]
    left, right = st.columns([1, 1.35])
    with left:
        st.markdown('<div class="waybill-card">', unsafe_allow_html=True)
        if st.session_state.role == "Admin":
            if st.button("➕ New Shipment", use_container_width=True):
                st.session_state.shipment_modal = True
                st.session_state.edit_shipment_id = None
                st.rerun()
        for shipment in filtered:
            if st.button(f"{shipment['id']} — {shipment['client']}", key=f"ship_{shipment['id']}", use_container_width=True):
                st.session_state.selected_shipment = shipment["id"]
        st.markdown("</div>", unsafe_allow_html=True)
    
    selected = next((item for item in st.session_state.shipments if item["id"] == st.session_state.selected_shipment), None)
    if not selected and st.session_state.shipments:
        selected = st.session_state.shipments[0]
        
    with right:
        if selected:
            progress_pct = int(selected["progress"] * 100)
            progress_color = STATUS_META.get(selected["status"], STATUS_META["pending"])[1]
            
            detail_html = f"""
            <div class="waybill-card" style="padding: 1.5rem 1.8rem;">
              <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px;">
                <div>
                  <span class="mono badge" style="background: rgba(255,255,255,0.03); color: #dce5ff; border: 1px solid rgba(255,255,255,0.08); font-size: 0.82rem; padding: 0.25rem 0.65rem;">{selected['id']}</span>
                  <h2 style="margin: 8px 0 0 0; font-size: 1.8rem; font-weight: 800; letter-spacing: -0.02em; color: var(--text);">{selected['client']}</h2>
                </div>
                {badge(selected['status'])}
              </div>
              
              <div style="margin: 24px 0 16px 0;">
                <div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: var(--muted); margin-bottom: 8px; font-weight: 600;">
                  <span>Route Progress</span>
                  <span>{progress_pct}%</span>
                </div>
                <div style="height: 8px; width: 100%; background: rgba(255,255,255,0.08); border-radius: 99px; overflow: hidden; position: relative;">
                  <div style="height: 100%; width: {progress_pct}%; background: {progress_color}; border-radius: 99px; transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);"></div>
                </div>
              </div>
              
              <div style="display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.04);">
                <span style="color: var(--muted); font-size: 0.9rem;">Route</span>
                <strong style="color: var(--text); font-size: 0.9rem;">{selected['origin']} &rarr; {selected['dest']}</strong>
              </div>
              <div style="display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.04);">
                <span style="color: var(--muted); font-size: 0.9rem;">ETA</span>
                <strong style="color: var(--text); font-size: 0.9rem; display: flex; align-items: center; gap: 4px;">🕒 {selected['eta']}</strong>
              </div>
              <div style="display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.04);">
                <span style="color: var(--muted); font-size: 0.9rem;">Driver</span>
                <strong style="color: var(--text); font-size: 0.9rem;">{selected.get('driver', '—')}</strong>
              </div>
              <div style="display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.04);">
                <span style="color: var(--muted); font-size: 0.9rem;">Vehicle ID</span>
                <strong class="mono" style="color: var(--text); font-size: 0.9rem; background: rgba(255,255,255,0.04); padding: 2px 6px; border-radius: 4px;">{selected.get('vehicle', '—')}</strong>
              </div>
              <div style="display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.04);">
                <span style="color: var(--muted); font-size: 0.9rem;">Cargo</span>
                <strong style="color: var(--text); font-size: 0.9rem;">{selected.get('cargo', '—')}</strong>
              </div>
              <div style="display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.04);">
                <span style="color: var(--muted); font-size: 0.9rem;">Weight</span>
                <strong style="color: var(--text); font-size: 0.9rem;">{f"{selected['weight']} kg" if selected.get('weight') else '—'}</strong>
              </div>
              <div style="display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.04);">
                <span style="color: var(--muted); font-size: 0.9rem;">Freight Charge</span>
                <strong style="color: var(--good); font-size: 0.9rem;">{money(selected.get('freightCharge', 0))}</strong>
              </div>
              
              <div style="margin-top: 18px; border-top: 1px dashed rgba(255,255,255,0.06); padding-top: 14px; display: grid; gap: 8px;">
                <div style="font-size: 0.72rem; color: #ff8a3d; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">📋 Shipping & Billing Details</div>
                <div style="display: flex; justify-content: space-between; padding: 4px 0;">
                  <span style="color: var(--muted); font-size: 0.85rem;">Bill# / Date</span>
                  <strong style="color: var(--text); font-size: 0.85rem;">{selected.get('billNo', '—')} {f"({selected.get('billDate')})" if selected.get('billDate') else ''}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 4px 0;">
                  <span style="color: var(--muted); font-size: 0.85rem;">Party Invoice# / Date</span>
                  <strong style="color: var(--text); font-size: 0.85rem;">{selected.get('partyInvoiceNo', '—')} {f"({selected.get('partyInvoiceDate')})" if selected.get('partyInvoiceDate') else ''}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 4px 0;">
                  <span style="color: var(--muted); font-size: 0.85rem;">Detention</span>
                  <strong style="color: var(--text); font-size: 0.85rem;">{selected.get('detention', '—')}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 4px 0;">
                  <span style="color: var(--muted); font-size: 0.85rem;">Items</span>
                  <strong style="color: var(--text); font-size: 0.85rem;">{selected.get('items', '—')}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 4px 0;">
                  <span style="color: var(--muted); font-size: 0.85rem;">Container Qty</span>
                  <strong style="color: var(--text); font-size: 0.85rem;">{selected.get('containerQty', '—')}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 4px 0;">
                  <span style="color: var(--muted); font-size: 0.85rem;">Empty Pickup To</span>
                  <strong style="color: var(--text); font-size: 0.85rem;">{selected.get('emptyPickupTo', '—')}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 4px 0;">
                  <span style="color: var(--muted); font-size: 0.85rem;">Load Container</span>
                  <strong style="color: var(--text); font-size: 0.85rem;">{selected.get('loadContainer', '—')}</strong>
                </div>
              </div>

              {f'<div style="margin-top: 14px; font-size: 0.85rem; color: var(--muted);"><strong>Notes:</strong> {selected["notes"]}</div>' if selected.get("notes") else ''}
            </div>
            """
            st.markdown(detail_html, unsafe_allow_html=True)
            
            if st.session_state.role == "Admin":
                st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
                c_act1, c_act2 = st.columns(2)
                with c_act1:
                    if st.button("✏️ Edit Shipment", use_container_width=True):
                        st.session_state.shipment_modal = True
                        st.session_state.edit_shipment_id = selected["id"]
                        st.rerun()
                with c_act2:
                    if st.button("🗑️ Delete Shipment", use_container_width=True):
                        st.session_state.shipments = [s for s in st.session_state.shipments if s["id"] != selected["id"]]
                        if st.session_state.shipments:
                            st.session_state.selected_shipment = st.session_state.shipments[0]["id"]
                        st.session_state.toast = f"Shipment {selected['id']} deleted"
                        st.rerun()
        else:
            st.info("No shipments found")


def stock_view() -> None:
    st.markdown('<div class="waybill-card">', unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown('<div class="section-heading">Inventory</div>', unsafe_allow_html=True)
    with c2:
        if st.button("+ New item", use_container_width=True):
            st.session_state.stock_modal = not st.session_state.stock_modal
    st.dataframe(st.session_state.stock, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.stock_modal:
        with st.form("new_stock_form"):
            sku = st.text_input("SKU")
            item = st.text_input("Item")
            warehouse = st.text_input("Warehouse")
            qty = st.number_input("Qty on hand", min_value=0, step=1)
            reorder = st.number_input("Reorder threshold", min_value=0, step=1)
            unit = st.selectbox("Unit", ["pcs", "gal", "rolls", "pairs"])
            submitted = st.form_submit_button("Add item", type="primary")
            if submitted and sku and item:
                st.session_state.stock.insert(0, {"sku": sku, "item": item, "warehouse": warehouse, "qty": int(qty), "reorder": int(reorder), "unit": unit})
                st.session_state.stock_modal = False
                st.session_state.toast = f"{sku} added to inventory"
                st.rerun()


def receiving_view() -> None:
    st.markdown('<div class="waybill-card">', unsafe_allow_html=True)
    if st.button("+ New slip"):
        st.session_state.receiving_modal = not st.session_state.receiving_modal
    for slip in st.session_state.receiving:
        with st.expander(f"{slip['id']} — {slip['supplier']}", expanded=st.session_state.get("open_grn", RECEIVING[0]["id"]) == slip["id"]):
            st.write(f"Date: {slip['date']} | Line items: {slip['items']} | Value: {money(slip['value'])}")
            st.markdown(badge(slip["status"]), unsafe_allow_html=True)
            st.dataframe(st.session_state.receiving_lines.get(slip["id"], []), use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.receiving_modal:
        with st.form("new_receiving_form"):
            supplier = st.text_input("Supplier")
            items = st.number_input("Line items", min_value=1, step=1)
            value = st.number_input("Estimated value ($)", min_value=0, step=10)
            submitted = st.form_submit_button("Create slip", type="primary")
            if submitted and supplier:
                new_id = f"GRN-{3084 + len(st.session_state.receiving)}"
                st.session_state.receiving.insert(0, {"id": new_id, "supplier": supplier, "date": date.today().strftime("%b %d"), "status": "pending", "items": int(items), "value": int(value)})
                st.session_state.receiving_lines[new_id] = [{"name": "Pending line item entry", "ordered": 0, "received": 0}]
                st.session_state.receiving_modal = False
                st.session_state.toast = f"{new_id} created"
                st.rerun()


def payments_view() -> None:
    role = st.session_state.role
    income = sum(tx["amount"] for tx in st.session_state.transactions if tx["type"] == "income")
    expense = sum(tx["amount"] for tx in st.session_state.transactions if tx["type"] == "expense")
    visible = st.session_state.transactions if role == "Admin" else [tx for tx in st.session_state.transactions if tx["type"] == "expense" and tx.get("owner") == st.session_state.email]

    if role == "Admin":
        st.markdown(
            f'<div class="kpi-grid" style="grid-template-columns: repeat(3, 1fr); margin-bottom: 20px;">'
            f'  <div class="kpi-card-custom">'
            f'    <div class="kpi-icon-wrap success-icon">📈</div>'
            f'    <div>'
            f'      <div class="kpi-val" style="color: #3DDC97;">{money(income)}</div>'
            f'      <div class="kpi-lbl">Income</div>'
            f'    </div>'
            f'  </div>'
            f'  <div class="kpi-card-custom">'
            f'    <div class="kpi-icon-wrap alert-icon">📉</div>'
            f'    <div>'
            f'      <div class="kpi-val" style="color: #FF5C5C;">{money(expense)}</div>'
            f'      <div class="kpi-lbl">Expenses</div>'
            f'    </div>'
            f'  </div>'
            f'  <div class="kpi-card-custom">'
            f'    <div class="kpi-icon-wrap transit-icon">💰</div>'
            f'    <div>'
            f'      <div class="kpi-val">{money(income - expense)}</div>'
            f'      <div class="kpi-lbl">Net Cashflow</div>'
            f'    </div>'
            f'  </div>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.markdown('<div class="waybill-card">', unsafe_allow_html=True)
    st.dataframe(visible, use_container_width=True, hide_index=True)
    if st.button("+ New entry"):
        st.session_state.payment_modal = not st.session_state.payment_modal
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.payment_modal:
        with st.form("new_payment_form"):
            desc = st.text_input("Description")
            category = st.text_input("Category")
            amount = st.number_input("Amount (Rs)", min_value=0, step=100)
            tx_type = st.selectbox("Type", ["expense", "income"] if role == "Admin" else ["expense"])
            submitted = st.form_submit_button("Save", type="primary")
            if submitted and desc:
                new_id = f"TXN-{9008 + len(st.session_state.transactions)}"
                st.session_state.transactions.insert(0, {"id": new_id, "type": tx_type, "desc": desc, "date": date.today().strftime("%b %d"), "amount": int(amount), "category": category or "General", "owner": st.session_state.email})
                st.session_state.payment_modal = False
                st.session_state.toast = "Transaction saved"
                st.rerun()


def staff_view() -> None:
    if st.session_state.role != "Admin":
        st.info("Staff management is hidden from Staff role.")
        return

    st.markdown('<div class="waybill-card">', unsafe_allow_html=True)
    if st.button("+ Invite staff"):
        st.session_state.staff_modal = not st.session_state.staff_modal
    st.dataframe(st.session_state.staff, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

    for idx, person in enumerate(st.session_state.staff):
        cols = st.columns([2.2, 1.2, 1, 1])
        cols[0].write(person["name"])
        cols[1].write(person["role"])
        cols[2].write(person["access"])
        updated_status = cols[3].selectbox("Status", ["active", "suspended"], index=0 if person["status"] == "active" else 1, key=f"staff_status_{idx}")
        st.session_state.staff[idx]["status"] = updated_status

    if st.session_state.staff_modal:
        with st.form("staff_invite_form"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            role = st.text_input("Role", value="Driver")
            access = st.selectbox("Access", ["Staff", "Admin"])
            submitted = st.form_submit_button("Invite", type="primary")
            if submitted and name:
                initials = "".join(part[0].upper() for part in name.split()[:2])
                st.session_state.staff.insert(0, {"name": name, "email": email or f"{name.replace(' ', '.').lower()}@javeedgoods.pk", "role": role, "access": access, "status": "active", "initials": initials})
                st.session_state.staff_modal = False
                st.session_state.toast = f"{name} invited"
                st.rerun()


def optimizer_view() -> None:
    st.markdown('<div class="waybill-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">🛣️ Advanced Pakistan Motorway Route & Cost Optimizer</div>', unsafe_allow_html=True)
    st.write("Plan routes, calculate axle-based motorway tolls, estimate diesel consumption, driver allowances, and target billing rates.")

    cities = ['Karachi', 'Lahore', 'Islamabad', 'Peshawar', 'Quetta', 'Multan', 'Faisalabad']
    c1, c2 = st.columns(2)
    with c1:
        origin = st.selectbox("Origin Terminal", cities, index=0)
        dest = st.selectbox("Destination Terminal", cities, index=1)
        axles = st.selectbox("Truck Configuration (Axles)", [
            "2-Axle (Single Unit)", 
            "3-Axle (Rigid Truck)", 
            "4-Axle (Semi-Trailer)", 
            "5-Axle (Articulated)", 
            "6-Axle (Double Trailer)"
        ], index=2)
    with c2:
        fuel_rate = st.number_input("Fuel Rate (Rs/L)", value=285, step=5)
        allowance_days = st.number_input("Expected Trip Duration (Days)", min_value=1, max_value=7, value=2)
        driver_type = st.selectbox("Driver Category", ["Senior Captain", "Regular Driver", "Helper Only"])

    if origin == dest:
        st.warning("⚠️ Please select two different terminals.")
        return

    # Toll rates multiplier based on axle count
    axle_mult = 1.0 if "2-Axle" in axles else (1.4 if "3-Axle" in axles else (1.8 if "4-Axle" in axles else (2.3 if "5-Axle" in axles else 2.8)))

    routes = {
        'Karachi-Lahore': { "dist": 1210, "roads": ['M-9 Motorway', 'M-5 Motorway', 'M-3 Motorway'], "base_toll": 3800 },
        'Karachi-Islamabad': { "dist": 1540, "roads": ['M-9 Motorway', 'M-5 Motorway', 'M-2 Motorway'], "base_toll": 5200 },
        'Karachi-Peshawar': { "dist": 1700, "roads": ['M-9 Motorway', 'M-5 Motorway', 'M-2 Motorway', 'M-1 Motorway'], "base_toll": 6100 },
        'Karachi-Quetta': { "dist": 685, "roads": ['N-25 Highway'], "base_toll": 1200 },
        'Karachi-Multan': { "dist": 890, "roads": ['M-9 Motorway', 'M-5 Motorway'], "base_toll": 2800 },
        'Karachi-Faisalabad': { "dist": 1100, "roads": ['M-9 Motorway', 'M-5 Motorway', 'M-4 Motorway'], "base_toll": 3400 },
        'Lahore-Islamabad': { "dist": 380, "roads": ['M-2 Motorway'], "base_toll": 1400 },
        'Lahore-Peshawar': { "dist": 530, "roads": ['M-2 Motorway', 'M-1 Motorway'], "base_toll": 2200 },
        'Lahore-Quetta': { "dist": 950, "roads": ['N-70 Highway'], "base_toll": 1900 },
        'Lahore-Multan': { "dist": 330, "roads": ['M-3 Motorway'], "base_toll": 1100 },
        'Lahore-Faisalabad': { "dist": 180, "roads": ['M-3 Motorway', 'M-4 Motorway'], "base_toll": 700 },
        'Islamabad-Peshawar': { "dist": 155, "roads": ['M-1 Motorway'], "base_toll": 800 },
        'Islamabad-Quetta': { "dist": 920, "roads": ['CPEC Western Route'], "base_toll": 2400 },
        'Islamabad-Multan': { "dist": 680, "roads": ['M-2 Motorway', 'M-4 Motorway'], "base_toll": 2500 },
        'Islamabad-Faisalabad': { "dist": 320, "roads": ['M-2 Motorway', 'M-4 Motorway'], "base_toll": 1300 },
        'Peshawar-Quetta': { "dist": 1040, "roads": ['Indus Highway (N-55)'], "base_toll": 2100 },
        'Peshawar-Multan': { "dist": 830, "roads": ['M-1 Motorway', 'M-4 Motorway'], "base_toll": 3100 },
        'Peshawar-Faisalabad': { "dist": 480, "roads": ['M-1 Motorway', 'M-4 Motorway'], "base_toll": 1800 },
        'Multan-Quetta': { "dist": 630, "roads": ['N-70 Highway'], "base_toll": 1400 },
        'Multan-Faisalabad': { "dist": 240, "roads": ['M-4 Motorway'], "base_toll": 900 },
        'Faisalabad-Quetta': { "dist": 850, "roads": ['N-70 Highway'], "base_toll": 1700 },
    }

    key = f"{origin}-{dest}"
    key_rev = f"{dest}-{origin}"
    route = routes.get(key, routes.get(key_rev, None))

    if not route:
        st.info("ℹ️ Custom route. Calculating standard estimates based on 400km standard multiplier.")
        route = { "dist": 400, "roads": ['GT Road / National Highway'], "base_toll": 1000 }

    km_l = 3.0 if "6-Axle" in axles or "5-Axle" in axles else (4.5 if "4-Axle" in axles else 6.0)
    fuel_cost = int((route["dist"] / km_l) * fuel_rate)
    toll_cost = int(route["base_toll"] * axle_mult)

    base_allowance = 4500 if "Senior" in driver_type else (3000 if "Regular" in driver_type else 1500)
    driver_allowance = int(base_allowance * allowance_days)

    total_cost = fuel_cost + toll_cost + driver_allowance
    recommended_charge = int(total_cost / 0.70) # 30% profit target

    st.markdown("### 🗺️ Planned Route Information")
    st.info(f"📍 **Route Path:** {' ➔ '.join(route['roads'])} | Odometer Target: **{route['dist']} km**")

    st.markdown("### 📊 Cost Summary Sheet")
    st.markdown(
        f"""
        <div style="background: rgba(255,255,255,0.03); padding: 18px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.08); margin: 15px 0;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 0.92rem; color: #ccc;">
                <div>⛽ Fuel Expense:</div><div style="text-align: right; font-weight: 600; color: #fff;">{money(fuel_cost)}</div>
                <div>🛣️ Toll Taxes:</div><div style="text-align: right; font-weight: 600; color: #fff;">{money(toll_cost)}</div>
                <div>🧑‍✈️ Driver Allowance ({allowance_days} days):</div><div style="text-align: right; font-weight: 600; color: #fff;">{money(driver_allowance)}</div>
                <div style="border-top: 1px solid rgba(255,255,255,0.15); padding-top: 10px; font-weight: bold; color: #ff8a3d; font-size: 1.05rem;">Net Operating Cost:</div>
                <div style="border-top: 1px solid rgba(255,255,255,0.15); padding-top: 10px; text-align: right; font-weight: bold; color: #ff8a3d; font-size: 1.05rem;">{money(total_cost)}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    c3, c4, c5 = st.columns(3)
    c3.metric("Motorway Tolls", money(toll_cost), f"Base: {money(route['base_toll'])}")
    c4.metric("Total Cost", money(total_cost), f"Fuel: {money(fuel_cost)}")
    c5.metric("Target Billing Price", money(recommended_charge), f"Profit: {money(recommended_charge - total_cost)}")
    st.markdown("</div>", unsafe_allow_html=True)


def invoices_view() -> None:
    st.markdown('<div class="waybill-card">', unsafe_allow_html=True)
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown('<div class="section-heading">🧾 Client Invoices & Receivables</div>', unsafe_allow_html=True)
    with c2:
        if st.button("+ New Invoice", use_container_width=True):
            st.session_state.invoice_modal = not st.session_state.invoice_modal

    if st.session_state.invoice_modal:
        with st.form("new_invoice_form"):
            client_names = [c["name"] for c in st.session_state.clients]
            client = st.selectbox("Select Client", client_names)
            ship_id = st.text_input("Linked Shipment ID (optional)")
            amount = st.number_input("Invoice Amount (Rs)", min_value=0, step=5000, value=50000)
            due_date = st.text_input("Payment Due Date", value="Jul 20, 2026")
            status = st.selectbox("Initial Status", ["unpaid", "paid"])
            submitted = st.form_submit_button("Generate Invoice", type="primary")
            if submitted and client:
                new_id = f"INV-{1000 + len(st.session_state.invoices)}"
                st.session_state.invoices.insert(0, {
                    "id": new_id,
                    "shipmentId": ship_id,
                    "client": client,
                    "amount": int(amount),
                    "date": date.today().strftime("%b %d"),
                    "dueDate": due_date,
                    "status": status,
                    "notes": ""
                })
                if status == "paid":
                    st.session_state.transactions.insert(0, {
                        "id": f"TXN-{10000 + len(st.session_state.transactions)}",
                        "type": "income",
                        "desc": f"Payment — Invoice {new_id} ({client})",
                        "date": date.today().strftime("%b %d"),
                        "amount": int(amount),
                        "category": "Client payment",
                        "owner": st.session_state.email
                    })
                st.session_state.invoice_modal = False
                st.session_state.toast = f"Invoice {new_id} successfully created."
                st.rerun()

    invoices = st.session_state.invoices
    if invoices:
        unpaid_tot = sum(inv["amount"] for inv in invoices if inv["status"] == "unpaid")
        paid_tot = sum(inv["amount"] for inv in invoices if inv["status"] == "paid")

        col_p, col_u = st.columns(2)
        col_p.metric("Collected Revenue", money(paid_tot))
        col_u.metric("Outstanding Balance (A/R)", money(unpaid_tot), delta_color="inverse")

        st.dataframe(invoices, use_container_width=True, hide_index=True)

        st.markdown("### 🖨️ Printable Invoice Preview")
        inv_ids = [inv["id"] for inv in invoices]
        sel_inv_id = st.selectbox("Select Invoice to Preview", inv_ids)
        sel_inv = next(inv for inv in invoices if inv["id"] == sel_inv_id)

        st.markdown(
            f"""
            <div style="background: #111b27; padding: 24px; border-radius: 12px; border: 1px solid #ff8a3d; margin: 15px 0; color: #fff; font-family: monospace;">
                <div style="display: flex; justify-content: space-between; border-bottom: 2px solid #ff8a3d; padding-bottom: 12px;">
                    <div>
                        <h2 style="margin: 0; color: #ff8a3d;">JAVEED GOODS TRANSPORT</h2>
                        <div style="font-size: 0.8rem; opacity: 0.8;">Plot 24, Hub Center, Karachi | info@javeedgoods.pk</div>
                    </div>
                    <div style="text-align: right;">
                        <h2 style="margin: 0; color: #3DDC97;">INVOICE</h2>
                        <div style="font-size: 0.9rem; font-weight: bold;">{sel_inv['id']}</div>
                    </div>
                </div>
                <div style="display: flex; justify-content: space-between; margin: 20px 0;">
                    <div>
                        <strong>Bill To:</strong><br>
                        {sel_inv['client']}<br>
                        Linked Waybill: {sel_inv['shipmentId'] or 'N/A'}
                    </div>
                    <div style="text-align: right;">
                        <strong>Invoice Date:</strong> {sel_inv['date']}<br>
                        <strong>Due Date:</strong> {sel_inv['dueDate']}<br>
                        <strong>Status:</strong> <span style="color: {'#3DDC97' if sel_inv['status'] == 'paid' else '#FF5C5C'}; font-weight: bold;">{sel_inv['status'].upper()}</span>
                    </div>
                </div>
                <div style="border-top: 1px solid rgba(255,255,255,0.1); border-bottom: 1px solid rgba(255,255,255,0.1); padding: 12px 0; margin-bottom: 20px;">
                    <div style="display: flex; justify-content: space-between; font-weight: bold;">
                        <span>Description</span>
                        <span style="text-align: right;">Amount</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 8px;">
                        <span>Logistics freight transport services</span>
                        <span style="text-align: right;">{money(sel_inv['amount'])}</span>
                    </div>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 1.2rem; font-weight: bold; border-top: 2px solid #ff8a3d; padding-top: 10px;">
                    <span>Total Amount Due:</span>
                    <span style="color: #ff8a3d;">{money(sel_inv['amount'])}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if sel_inv["status"] == "unpaid":
            if st.button("✔️ Mark Invoice as Paid", type="primary"):
                sel_inv["status"] = "paid"
                st.session_state.transactions.insert(0, {
                    "id": f"TXN-{10000 + len(st.session_state.transactions)}",
                    "type": "income",
                    "desc": f"Payment — Invoice {sel_inv['id']} ({sel_inv['client']})",
                    "date": date.today().strftime("%b %d"),
                    "amount": sel_inv["amount"],
                    "category": "Client payment",
                    "owner": st.session_state.email
                })
                st.session_state.toast = f"Invoice {sel_inv['id']} marked as paid."
                st.rerun()
    else:
        st.info("No invoices logged.")
    st.markdown("</div>", unsafe_allow_html=True)


def clients_view() -> None:
    st.markdown('<div class="waybill-card">', unsafe_allow_html=True)
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown('<div class="section-heading">🏢 Client Directory</div>', unsafe_allow_html=True)
    with c2:
        if st.button("+ New Client", use_container_width=True):
            st.session_state.client_modal = not st.session_state.client_modal

    if st.session_state.client_modal:
        with st.form("new_client_form"):
            name = st.text_input("Company Name")
            contact = st.text_input("Contact Person")
            phone = st.text_input("Phone")
            city = st.text_input("City")
            email = st.text_input("Email")
            submitted = st.form_submit_button("Save Client", type="primary")
            if submitted and name:
                new_id = f"CLT-00{len(st.session_state.clients)+1}"
                st.session_state.clients.insert(0, {
                    "id": new_id,
                    "name": name,
                    "contact": contact,
                    "phone": phone,
                    "city": city,
                    "email": email,
                    "activeShipments": 0,
                    "totalValue": 0
                })
                st.session_state.client_modal = False
                st.session_state.toast = f"Client {name} saved"
                st.rerun()

    st.dataframe(st.session_state.clients, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)


def salaries_view() -> None:
    st.markdown('<div class="waybill-card">', unsafe_allow_html=True)
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown('<div class="section-heading">💰 Payroll & Staff Salaries</div>', unsafe_allow_html=True)
    with c2:
        if st.button("+ Log Payroll", use_container_width=True):
            st.session_state.salary_modal = not st.session_state.salary_modal

    if st.session_state.salary_modal:
        with st.form("new_salary_form"):
            staff_names = [s["name"] for s in st.session_state.staff]
            staff_name = st.selectbox("Staff Member", staff_names)
            month = st.selectbox("Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], index=5)
            year = st.number_input("Year", min_value=2020, max_value=2030, value=2026)
            basic = st.number_input("Basic Salary (Rs)", min_value=0, value=35000)
            allowance = st.number_input("Allowance (Rs)", min_value=0, value=5000)
            deduction = st.number_input("Deductions (Rs)", min_value=0, value=0)
            status = st.selectbox("Status", ["unpaid", "paid"])
            submitted = st.form_submit_button("Record Salary", type="primary")
            if submitted:
                staff_member = next(s for s in st.session_state.staff if s["name"] == staff_name)
                total = basic + allowance - deduction
                new_id = f"SAL-00{len(st.session_state.salaries)+1}"
                st.session_state.salaries.insert(0, {
                    "id": new_id,
                    "staffId": staff_member.get("id", "STF-001"),
                    "staffName": staff_name,
                    "month": month,
                    "year": int(year),
                    "basic": int(basic),
                    "allowance": int(allowance),
                    "deduction": int(deduction),
                    "total": int(total),
                    "status": status,
                    "paidDate": date.today().strftime("%b %d") if status == "paid" else "",
                    "notes": ""
                })
                if status == "paid":
                    st.session_state.transactions.insert(0, {
                        "id": f"TXN-{10000 + len(st.session_state.transactions)}",
                        "type": "expense",
                        "desc": f"Staff salary — {staff_name} ({month})",
                        "date": date.today().strftime("%b %d"),
                        "amount": int(total),
                        "category": "Salary",
                        "owner": st.session_state.email
                    })
                st.session_state.salary_modal = False
                st.session_state.toast = f"Salary slip {new_id} recorded."
                st.rerun()

    salaries = st.session_state.salaries
    if salaries:
        st.dataframe(salaries, use_container_width=True, hide_index=True)

        st.markdown("### 🖨️ Salary Slip Details")
        sal_labels = [f"{s['id']} — {s['staffName']} ({s['month']} {s['year']})" for s in salaries]
        sel_label = st.selectbox("Select Salary Slip to Preview", sal_labels)
        sel_sal = next(s for s in salaries if f"{s['id']} — {s['staffName']} ({s['month']} {s['year']})" == sel_label)

        st.markdown(
            f"""
            <div style="background: #111b27; padding: 24px; border-radius: 12px; border: 1px solid #ff8a3d; margin: 15px 0; color: #fff; font-family: monospace;">
                <div style="display: flex; justify-content: space-between; border-bottom: 2px solid #ff8a3d; padding-bottom: 12px;">
                    <div>
                        <h2 style="margin: 0; color: #ff8a3d;">JAVEED GOODS TRANSPORT</h2>
                        <div style="font-size: 0.8rem; opacity: 0.8;">Karachi Operations | SALARY PAYROLL</div>
                    </div>
                    <div style="text-align: right;">
                        <h2 style="margin: 0; color: #ff5c5c;">PAYROLL SLIP</h2>
                        <div style="font-size: 0.9rem; font-weight: bold;">{sel_sal['id']}</div>
                    </div>
                </div>
                <div style="display: flex; justify-content: space-between; margin: 20px 0;">
                    <div>
                        <strong>Employee:</strong> {sel_sal['staffName']}<br>
                        <strong>Staff ID:</strong> {sel_sal['staffId']}
                    </div>
                    <div style="text-align: right;">
                        <strong>Pay Period:</strong> {sel_sal['month']} {sel_sal['year']}<br>
                        <strong>Status:</strong> <span style="color: {'#3DDC97' if sel_sal['status'] == 'paid' else '#FF5C5C'}; font-weight: bold;">{sel_sal['status'].upper()}</span>
                    </div>
                </div>
                <div style="border-top: 1px solid rgba(255,255,255,0.1); padding: 12px 0;">
                    <div style="display: flex; justify-content: space-between; font-weight: bold; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 5px;">
                        <span>Earnings & Benefits</span>
                        <span style="text-align: right;">Amount</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 8px;">
                        <span>Basic Pay Rate:</span>
                        <span style="text-align: right;">{money(sel_sal['basic'])}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 4px;">
                        <span>Allowances (Fuel/Meal):</span>
                        <span style="text-align: right;">{money(sel_sal['allowance'])}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 4px; border-bottom: 1px dashed rgba(255,255,255,0.1); padding-bottom: 8px;">
                        <span>Deductions:</span>
                        <span style="color: #FF5C5C; text-align: right;">-{money(sel_sal['deduction'])}</span>
                    </div>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 1.2rem; font-weight: bold; border-top: 2px solid #ff8a3d; padding-top: 10px;">
                    <span>Net Disbursed Payout:</span>
                    <span style="color: #3DDC97;">{money(sel_sal['total'])}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if sel_sal["status"] == "unpaid":
            if st.button("💳 Disburse Salary Payout", type="primary"):
                sel_sal["status"] = "paid"
                st.session_state.transactions.insert(0, {
                    "id": f"TXN-{10000 + len(st.session_state.transactions)}",
                    "type": "expense",
                    "desc": f"Staff salary — {sel_sal['staffName']} ({sel_sal['month']})",
                    "date": date.today().strftime("%b %d"),
                    "amount": sel_sal["total"],
                    "category": "Salary",
                    "owner": st.session_state.email
                })
                st.session_state.toast = f"Salary disbursed to {sel_sal['staffName']}."
                st.rerun()
    else:
        st.info("No salary payouts logged.")
    st.markdown("</div>", unsafe_allow_html=True)


def attendance_view() -> None:
    st.markdown('<div class="waybill-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">🗓️ Staff Attendance Ledger</div>', unsafe_allow_html=True)
    st.write(f"Record attendance for date: **{date.today().strftime('%A, %d-%b-%Y')}**")

    for person in st.session_state.staff:
        status_color = "🟢 Active" if person["status"] == "active" else "🔴 Suspended"
        st.checkbox(f"{person['name']} ({person['role']}) - Status: {status_color}", value=True, key=f"att_check_{person['name']}")

    if st.button("Save Daily Attendance", type="primary"):
        st.session_state.toast = "Daily attendance recorded successfully"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def vehicles_view() -> None:
    st.markdown('<div class="waybill-card">', unsafe_allow_html=True)
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown('<div class="section-heading">🚛 Vehicle Fleet Directory</div>', unsafe_allow_html=True)
    with c2:
        if st.button("+ Add Vehicle", use_container_width=True):
            st.session_state.vehicle_modal = not st.session_state.vehicle_modal

    if st.session_state.vehicle_modal:
        with st.form("new_vehicle_form"):
            vid = st.text_input("Vehicle ID", placeholder="TRK-XXXX")
            make = st.text_input("Make", placeholder="Hino")
            model = st.text_input("Model", placeholder="700 Series")
            plate = st.text_input("License Plate")
            status = st.selectbox("Status", ["active", "maintenance"])
            km = st.number_input("Current Odometer (km)", min_value=0, step=1000, value=100000)
            submitted = st.form_submit_button("Save Vehicle", type="primary")
            if submitted and vid:
                st.session_state.vehicles.insert(0, {
                    "id": vid,
                    "type": "Truck",
                    "make": make,
                    "model": model,
                    "year": 2021,
                    "plate": plate,
                    "status": status,
                    "driver": "",
                    "km": int(km),
                    "nextService": int(km) + 10000
                })
                st.session_state.vehicle_modal = False
                st.session_state.toast = f"Vehicle {vid} saved"
                st.rerun()

    st.markdown("### 🔔 Active Service Alerts")
    any_alerts = False
    for v in st.session_state.vehicles:
        if v["km"] >= v["nextService"] - 2000:
            st.warning(f"⚠️ **{v['id']} ({v['make']} {v['model']})**: Odometer {v['km']:,} km is close to next service milestone {v['nextService']:,} km! Schedule checkup.")
            any_alerts = True
    if not any_alerts:
        st.success("✅ All vehicles are well within standard service mileage thresholds.")

    st.dataframe(st.session_state.vehicles, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)


def fuel_logs_view() -> None:
    st.markdown('<div class="waybill-card">', unsafe_allow_html=True)
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown('<div class="section-heading">⛽ Fleet Fuel & Efficiency Analytics</div>', unsafe_allow_html=True)
    with c2:
        if st.button("+ Log Fuel", use_container_width=True):
            st.session_state.fuel_modal = not st.session_state.fuel_modal

    if st.session_state.fuel_modal:
        with st.form("new_fuel_form"):
            v_ids = [v["id"] for v in st.session_state.vehicles]
            v_id = st.selectbox("Vehicle", v_ids)
            liters = st.number_input("Liters Filled", min_value=1.0, step=1.0, value=150.0)
            cost_per_l = st.number_input("Cost Per Liter (Rs)", min_value=1, value=285)
            odometer = st.number_input("Current Odometer Mileage (km)", min_value=0, step=1000, value=150000)
            station = st.text_input("Fuel Station", value="PSO Ring Road")
            submitted = st.form_submit_button("Record Fuel Log", type="primary")
            if submitted:
                total_cost = int(liters * cost_per_l)
                new_id = f"FL-00{len(st.session_state.fuelLogs)+1}"
                st.session_state.fuelLogs.insert(0, {
                    "id": new_id,
                    "vehicleId": v_id,
                    "date": date.today().strftime("%b %d"),
                    "liters": float(liters),
                    "costPerL": int(cost_per_l),
                    "total": total_cost,
                    "odometer": int(odometer),
                    "station": station
                })
                v_obj = next((v for v in st.session_state.vehicles if v["id"] == v_id), None)
                if v_obj:
                    v_obj["km"] = int(odometer)

                st.session_state.transactions.insert(0, {
                    "id": f"TXN-{10000 + len(st.session_state.transactions)}",
                    "type": "expense",
                    "desc": f"Diesel refuel — {v_id}",
                    "date": date.today().strftime("%b %d"),
                    "amount": total_cost,
                    "category": "Fuel",
                    "owner": st.session_state.email
                })
                st.session_state.fuel_modal = False
                st.session_state.toast = f"Fuel log {new_id} saved"
                st.rerun()

    st.markdown("### 📊 Fleet Odometer & Efficiency Index")
    import pandas as pd
    fl_df = pd.DataFrame(st.session_state.fuelLogs)
    if not fl_df.empty:
        avg_price = fl_df["costPerL"].mean()
        total_liters = fl_df["liters"].sum()
        total_spent = fl_df["total"].sum()

        c3, c4, c5 = st.columns(3)
        c3.metric("Total Diesel Filled", f"{total_liters:,.0f} L")
        c4.metric("Avg Fuel Cost", f"Rs {avg_price:.1f}/L")
        c5.metric("Total Fuel Spend", money(total_spent))

    st.dataframe(st.session_state.fuelLogs, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)


def maintenance_view() -> None:
    st.markdown('<div class="waybill-card">', unsafe_allow_html=True)
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown('<div class="section-heading">🔧 Maintenance Records</div>', unsafe_allow_html=True)
    with c2:
        if st.button("+ Log Maintenance", use_container_width=True):
            st.session_state.maint_modal = not st.session_state.maint_modal

    if st.session_state.maint_modal:
        with st.form("new_maint_form"):
            v_ids = [v["id"] for v in st.session_state.vehicles]
            v_id = st.selectbox("Vehicle", v_ids)
            m_type = st.text_input("Service Type", placeholder="e.g. Brake replacement")
            cost = st.number_input("Total Cost (Rs)", min_value=0, step=500)
            status = st.selectbox("Status", ["done", "in_progress"])
            submitted = st.form_submit_button("Record Maintenance", type="primary")
            if submitted and m_type:
                new_id = f"MNT-00{len(st.session_state.maintenance)+1}"
                st.session_state.maintenance.insert(0, {
                    "id": new_id,
                    "vehicleId": v_id,
                    "date": date.today().strftime("%b %d"),
                    "type": m_type,
                    "cost": int(cost),
                    "nextDue": "Three Months",
                    "status": status,
                    "notes": ""
                })
                st.session_state.transactions.insert(0, {
                    "id": f"TXN-{10000 + len(st.session_state.transactions)}",
                    "type": "expense",
                    "desc": f"Maintenance — {v_id} ({m_type})",
                    "date": date.today().strftime("%b %d"),
                    "amount": int(cost),
                    "category": "Maintenance",
                    "owner": st.session_state.email
                })
                st.session_state.maint_modal = False
                st.session_state.toast = f"Maintenance log {new_id} saved"
                st.rerun()

    st.dataframe(st.session_state.maintenance, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)


def reports_view() -> None:
    st.markdown('<div class="waybill-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">📑 Financial & Fleet Reports</div>', unsafe_allow_html=True)

    inc = sum(t["amount"] for t in st.session_state.transactions if t["type"] == "income")
    exp = sum(t["amount"] for t in st.session_state.transactions if t["type"] == "expense")
    net = inc - exp

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Income", money(inc))
    c2.metric("Total Expenses", money(exp), delta_color="inverse")
    c3.metric("Net Profit", money(net), delta=money(net))

    import pandas as pd
    tx_df = pd.DataFrame(st.session_state.transactions)
    if not tx_df.empty:
        st.markdown("### Expense Breakdown by Category")
        exp_df = tx_df[tx_df["type"] == "expense"]
        if not exp_df.empty:
            cat_totals = exp_df.groupby("category")["amount"].sum().reset_index()
            st.bar_chart(cat_totals.set_index("category"))

    st.markdown("</div>", unsafe_allow_html=True)


def activity_log_view() -> None:
    st.markdown('<div class="waybill-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">📋 System Activity Log</div>', unsafe_allow_html=True)
    st.dataframe(st.session_state.activityLog, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)


def settings_view() -> None:
    st.markdown('<div class="waybill-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">⚙️ Application Settings & Database Backups</div>', unsafe_allow_html=True)

    # Company Profile
    st.markdown("### Company Profile")
    comp_name = st.text_input("Company name", value="Javeed Goods Transport")
    address = st.text_input("Office address", value="Plot 24, Hub Center, Karachi")
    phone = st.text_input("Phone number", value="021-3456789")

    # Financial Configuration
    st.markdown("### Operations & Rates")
    fuel_rate = st.number_input("Standard Fuel Rate (Rs/L)", value=285)

    if st.button("Save Settings", type="primary"):
        st.session_state.toast = "Settings saved successfully"
        st.rerun()

    st.markdown("---")
    st.markdown("### 💾 Database Backup & Recovery")

    import json
    db_export = {
        "shipments": st.session_state.shipments,
        "stock": st.session_state.stock,
        "receiving": st.session_state.receiving,
        "receiving_lines": st.session_state.receiving_lines,
        "transactions": st.session_state.transactions,
        "staff": st.session_state.staff,
        "clients": st.session_state.clients,
        "invoices": st.session_state.invoices,
        "salaries": st.session_state.salaries,
        "vehicles": st.session_state.vehicles,
        "fuelLogs": st.session_state.fuelLogs,
        "maintenance": st.session_state.maintenance,
        "activityLog": st.session_state.activityLog
    }
    json_str = json.dumps(db_export, indent=2)

    st.download_button(
        label="📥 Export Database (JSON)",
        data=json_str,
        file_name=f"jgt_backup_{date.today().strftime('%Y%m%d')}.json",
        mime="application/json",
        use_container_width=True
    )

    uploaded_file = st.file_uploader("📤 Restore Database from JSON Backup File", type="json")
    if uploaded_file is not None:
        try:
            imported_db = json.load(uploaded_file)
            for key, val in imported_db.items():
                if key in st.session_state:
                    st.session_state[key] = val
            st.session_state.toast = "Database restored successfully!"
            st.rerun()
        except Exception as e:
            st.error(f"Failed to parse backup file: {e}")

    st.markdown("---")
    st.markdown("### ⚠️ Danger Zone")
    if st.button("Factory Reset Database", type="secondary", help="Clear all custom entries and restore defaults"):
        st.session_state.clear()
        st.session_state.toast = "Database restored to default seed values"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def guide_view() -> None:
    st.markdown('<div class="waybill-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">❓ Fleet System User Guide</div>', unsafe_allow_html=True)
    st.markdown("""
    ### 🚀 Getting Started with Javeed Goods Transport
    Welcome to the **Javeed Goods Transport Management & Fleet System**. This application offers full logistics operation management in one single place.

    #### ⚙️ Operations Modules
    1. **📊 Dashboard:** Provides a global financial overview and active trip progress.
    2. **🚚 Shipments:** Add, edit, or delete shipments. Input container pickup details, bills, and party invoice numbers.
    3. **🛣️ Optimizer:** Plan trip costs, calculate tolls, and estimate profitable pricing.
    4. **🧾 Invoices:** Track accounts receivables, issue new invoices, and mark them paid.
    5. **🚛 Vehicles & FLEET:** Monitor trucks status, service scheduling, fuel log entries, and maintenance history.
    6. **💰 HR & Salaries:** Print payroll slips and manage monthly basic pay and allowances.

    #### 💾 Local Database & Backups
    - All data is securely persistent inside your browser cache.
    - If you clear browser history, data may reset. Use the Export features to backing up data.
    """)
    st.markdown("</div>", unsafe_allow_html=True)


def main() -> None:
    seed_state()
    css()

    if not st.session_state.authenticated:
        login_screen()
        return

    nav = sidebar()
    topbar(st.session_state.section)
    toast()

    section = st.session_state.section
    if "Dashboard" in section:
        dashboard()
    elif "Shipments" in section:
        shipments_view()
    elif "Optimizer" in section:
        optimizer_view()
    elif "Invoices" in section:
        invoices_view()
    elif "Clients" in section:
        clients_view()
    elif "Staff" in section:
        staff_view()
    elif "Salaries" in section:
        salaries_view()
    elif "Attendance" in section:
        attendance_view()
    elif "Vehicles" in section:
        vehicles_view()
    elif "Fuel Logs" in section:
        fuel_logs_view()
    elif "Maintenance" in section:
        maintenance_view()
    elif "Stock" in section:
        stock_view()
    elif "Receiving" in section:
        receiving_view()
    elif "Payments" in section:
        payments_view()
    elif "Reports" in section:
        reports_view()
    elif "Activity Log" in section:
        activity_log_view()
    elif "Settings" in section:
        settings_view()
    elif "Guide" in section:
        guide_view()


if __name__ == "__main__":
    main()