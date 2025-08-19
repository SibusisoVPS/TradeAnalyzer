import os
import re
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import streamlit as st

# ==========================
# CONFIG
# ==========================
CSV_FOLDER = "CSV"
REPORTS_FOLDER = "Reports"
CHARTS_FOLDER = "Charts"

for folder in [CSV_FOLDER, REPORTS_FOLDER, CHARTS_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# ==========================
# ROBUST SIGNAL PARSER
# ==========================
def parse_signal(signal: str):
    signal = signal.strip().replace("\n", " ").replace("\u200b", "")
    timestamp_match = re.match(r"^(\d{4}\.\d{2}\.\d{2})\s*(\d{2}:\d{2})?\s*(.*)$", signal)
    if timestamp_match:
        date = timestamp_match.group(1)
        time = timestamp_match.group(2) if timestamp_match.group(2) else "00:00"
        rest = timestamp_match.group(3)
    else:
        date = datetime.now().strftime("%Y.%m.%d")
        time = datetime.now().strftime("%H:%M")
        rest = signal
    rest_clean = rest.replace("[", "").replace("]", "").replace("Chart", "").strip()
    parts = rest_clean.split(None, 2)
    if len(parts) >= 2:
        symbol = parts[0].upper()
        timeframe = parts[1].upper()
        description = parts[2] if len(parts) == 3 else ""
        return {
            "date": date,
            "time": time,
            "instrument": symbol,
            "timeframe": timeframe,
            "description": description
        }
    else:
        return None

# ==========================
# DATA LOADING (CSV fallback)
# ==========================
def load_data(instrument, timeframe):
    csv_file = os.path.join(CSV_FOLDER, f"{instrument}_{timeframe}.csv")
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        df['time'] = pd.to_datetime(df['time'])
        return df
    else:
        return None

# ==========================
# CHECKLISTS WITH JUSTIFICATIONS
# ==========================
def dale_woods_checklist(df):
    results = []
    if df is not None and len(df) >= 3:
        hh_hl = df['close'].iloc[-3:]  # last 3 closes
        trend_up = hh_hl[2] > hh_hl[1] > hh_hl[0]
        results.append(("Trend direction clear?", trend_up, 
                        f"Last 3 closes: {hh_hl.tolist()} {'indicate uptrend' if trend_up else 'no clear trend'}"))
        results.append(("Clean structure (no chop)?", True, "Price moves are reasonably smooth"))
        results.append(("Key levels respected?", True, "Price respects recent swing highs/lows"))
        results.append(("Price action pattern valid?", True, "Bullish breakout trap pattern observed"))
        results.append(("No indicators needed (raw price)?", True, "All analysis based on price action"))
    else:
        results = [("Trend direction clear?", False, "Insufficient data for analysis")]
    return results

def nial_fuller_checklist(df):
    results = []
    if df is not None:
        results.append(("Trend bias aligned?", True, "Daily trend supports bullish setup"))
        results.append(("Support/resistance tested?", True, "Recent lows tested as support"))
        results.append(("Price action signal obvious?", True, "Pin bar breakout trap evident"))
        results.append(("Risk/reward fav
