import streamlit as st
from agent import CPGDecisionAgent

st.set_page_config(page_title="CPG Decision Agent")

st.title("Smart CPG Decision Support Agent")

agent = CPGDecisionAgent()

query = st.text_input("Ask a business question:")

if st.button("Analyze"):
    if query:

        result = agent.run(query)

        # ---------------- TREND ----------------
        if result["type"] == "trend":

            st.subheader("📈 Business Summary")

            summary = result["summary"]
            st.metric("Total Revenue", summary["total_revenue"])
            st.metric("Total Units Sold", summary["total_units"])
            st.metric("Top Category", summary["top_category"])

            st.subheader("📊 Monthly Revenue Trends")

            monthly = result["monthly"]

            chart_data = monthly.pivot(
                index="month",
                columns="category",
                values="revenue"
            )

            st.line_chart(chart_data)

        # ---------------- ANOMALY ----------------
        elif result["type"] == "anomaly":

            st.subheader("🚨 Detected Anomalies")
            st.dataframe(result["data"].head(20))

        # ---------------- PRICE ----------------
        elif result["type"] == "price":

            impact = result["impact"]

            st.subheader("💰 Price Impact Simulation")
            st.metric("Original Revenue", impact["original_revenue"])
            st.metric("Projected Revenue", impact["projected_revenue"])
            st.metric("Revenue Change %", f"{impact['revenue_change_pct']}%")

        # ---------------- PROMO ----------------
        elif result["type"] == "promo":

            impact = result["impact"]

            st.subheader("🎯 Promotion Impact Simulation")
            st.metric("Original Revenue", impact["original_revenue"])
            st.metric("Projected Revenue", impact["projected_revenue"])
            st.metric("Revenue Lift %", f"{impact['revenue_lift_pct']}%")

        # ---------------- LLM ----------------
        else:
            st.subheader("📌 Strategy Memo")
            st.write(result["text"])
