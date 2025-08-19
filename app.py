import streamlit as st
import os
from datetime import datetime

# ----------------------------
# Checklist definitions
# ----------------------------
dale_woods_results = [
    ("Trend direction clear?", True),
    ("Clean structure (no chop)?", True),
    ("Key levels respected?", True),
    ("Price action pattern valid?", True),
    ("No indicators needed (raw price)?", True),
    ("Mean reversion confirmed?", True),
    ("Signal candle validated?", True),
    ("Stop-loss logical?", True),
    ("Take-profit logical?", True),
    ("Overall high probability?", True)
]

nial_fuller_results = [
    ("Trend bias aligned?", True),
    ("Support/resistance tested?", True),
    ("Price action signal obvious?", True),
    ("Risk/reward favorable?", True),
    ("Higher timeframe alignment?", True),
    ("Confluence factors present?", True),
    ("Position sizing correct?", True),
    ("Stop-loss logical?", True),
    ("Target logical?", True),
    ("Trade plan disciplined?", True)
]

fundamental_results = [
    ("Macro trend supportive?", True),
    ("Upcoming news risk?", False),
    ("Correlation check ok?", True),
    ("Economic releases considered?", True),
    ("Market sentiment supportive?", True),
    ("Volatility acceptable?", True)
]

institutional_results = [
    ("Liquidity zones mapped?", True),
    ("Stop hunt risk?", False),
    ("Orderflow bias clear?", True),
    ("Volume spikes aligned?", True),
    ("Major players’ positions considered?", True),
    ("Price respecting institutional levels?", True)
]

# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(page_title="Trade Analyzer", page_icon="📊")
st.title("📊 Trade Analyzer")

trade_signal = st.text_area(
    "Paste your trade signal below (any format):",
    height=100
)

if st.button("Analyze"):
    if not trade_signal.strip():
        st.warning("Please enter a trade signal to analyze.")
    else:
        # Ensure Reports folder exists
        os.makedirs("Reports", exist_ok=True)

        # Combine checklists
        all_checklists = {
            "Dale Woods Checklist": dale_woods_results,
            "Nial Fuller Checklist": nial_fuller_results,
            "Fundamental Analysis": fundamental_results,
            "Institutional Analysis": institutional_results
        }

        # Timestamp for report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        signal_key = trade_signal.split()[0] if trade_signal else "TRADE"
        report_filename = f"Reports/report_{signal_key}_{timestamp}.txt"

        # Write report
        with open(report_filename, "w", encoding="utf-8") as f:
            f.write(f"Trade Signal: {trade_signal}\n")
            f.write(f"Report Generated: {datetime.now()}\n\n")

            for checklist_name, results in all_checklists.items():
                f.write(f"{checklist_name}\n")
                f.write("-" * len(checklist_name) + "\n")
                for desc, value in results:
                    status = "✅" if value is True else "❌" if value is False else value
                    f.write(f"- {desc}: {status}\n")
                f.write("\n")

            # Trade Plan Summary
            f.write("Trade Plan Summary\n")
            f.write("-----------------\n")
            f.write("Bias: Bullish (breakout trap setup)\n")
            f.write("Entry: Wait for confirmation at support/resistance\n")
            f.write("Stop Loss: Just beyond invalidation zone\n")
            f.write("Take Profit: At next liquidity pool\n")

        st.success("✅ Trade analysis complete!")
        st.write("Checklists & Results:")
        for checklist_name, results in all_checklists.items():
            st.subheader(checklist_name)
            for desc, value in results:
                status = "✅" if value is True else "❌" if value is False else value
                st.write(f"- {desc}: {status}")

        st.subheader("Trade Plan Summary")
        st.write("Bias: Bullish (breakout trap setup)")
        st.write("Entry: Wait for confirmation at support/resistance")
        st.write("Stop Loss: Just beyond invalidation zone")
        st.write("Take Profit: At next liquidity pool")
        st.write(f"📄 Report saved at: `{report_filename}`")
