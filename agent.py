from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from data_loader import load_data
from tools import analyze_trends, detect_anomalies, simulate_price_change, simulate_promo
from memory import Memory

load_dotenv()


class CPGDecisionAgent:
    def __init__(self):
        self.df = load_data()
        self.memory = Memory()

        # LLM initialization (used only when needed)
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3
        )

    # -----------------------------
    # Improved Tool Selection Logic
    # -----------------------------
    def select_tool(self, query: str) -> str:
        query = query.lower()

        if any(word in query for word in ["trend", "category", "performance"]):
            return "trend"

        elif any(word in query for word in ["anomaly", "spike", "abnormal", "unusual", "outlier"]):
            return "anomaly"

        elif any(word in query for word in ["price", "increase", "decrease"]):
            return "price"

        elif any(word in query for word in ["promo", "promotion", "discount"]):
            return "promo"

        else:
            return "llm"

    # -----------------------------
    # Main Agent Execution
    # -----------------------------
    def run(self, query: str):

        tool = self.select_tool(query)

        # ---------------- TREND TOOL ----------------
        if tool == "trend":
            monthly, summary = analyze_trends(self.df)

            return {
                "type": "trend",
                "monthly": monthly,
                "summary": summary
            }

        # ---------------- ANOMALY TOOL ----------------
        elif tool == "anomaly":
            anomalies = detect_anomalies(self.df)

            return {
                "type": "anomaly",
                "data": anomalies
            }

        # ---------------- PRICE TOOL ----------------
        elif tool == "price":
            impact = simulate_price_change(self.df)

            return {
                "type": "price",
                "impact": impact
            }

        # ---------------- PROMO TOOL ----------------
        elif tool == "promo":
            impact = simulate_promo(self.df)

            return {
                "type": "promo",
                "impact": impact
            }

        # ---------------- LLM FALLBACK ----------------
        else:
            memory_text = "\n".join(self.memory.get())

            prompt = f"""
You are a Senior CPG Strategy Consultant.

Business Question:
{query}

Previous Conversation:
{memory_text}

Generate:
1. Key Insight
2. Business Impact
3. Recommendation

Keep it executive-level and concise.
"""

            try:
                response = self.llm.invoke(prompt)
                answer = response.content

            except Exception:
                # Graceful fallback if quota exceeded
                answer = (
                    "LLM service unavailable (API quota exceeded or billing issue).\n\n"
                    "Please check OpenAI billing settings or use tool-based queries "
                    "(trend, anomaly, price simulation, promo simulation)."
                )

            self.memory.add("User", query)
            self.memory.add("Assistant", answer)

            return {
                "type": "llm",
                "text": answer
            }
