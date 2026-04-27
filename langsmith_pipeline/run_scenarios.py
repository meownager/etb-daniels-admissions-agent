"""
run_scenarios.py
----------------
Run the 4 April-4 test scenarios through the LangSmith-traced pipeline.

Each scenario invocation creates a trace in your LangSmith dashboard at:
  https://smith.langchain.com/

Open the dashboard after running to see:
  - The retrieval step (which chunks were pulled)
  - The LLM call (full prompt + response)
  - Latency, token counts, cost per call

Use the scenario_id metadata to filter traces in the dashboard.
"""
import os
from dotenv import load_dotenv
from agent import build_agent

load_dotenv()


SCENARIOS = [
    {
        "id": "HP1",
        "name": "Fintech to financial management",
        "input": (
            "I have 3 years of work experience in fintech and now I want to "
            "move into financial management as it is in high demand. "
            "What programs should I look for?"
        ),
        "expected": (
            "Recommends MSF; mentions Goldman/JP Morgan/Capital One employers; "
            "asks full-time vs online slot-fill"
        ),
    },
    {
        "id": "FC1",
        "name": "MBA GMAT waiver",
        "input": "Does the MBA program waive the GMAT requirements?",
        "expected": (
            "Mentions BOTH MBA programs; STEM-degree path for One-Year MBA; "
            "automatic 3-year-experience waiver for Online MBA; asks which one"
        ),
    },
    {
        "id": "HP2",
        "name": "Supply chain professional",
        "input": (
            "I've been working in the supply chain industry for 2 years now "
            "and I want to do something more strategic, but I'm not yet sure "
            "where to start."
        ),
        "expected": "Asks deeper-or-different clarifier before routing to programs",
    },
    {
        "id": "FC2",
        "name": "Vague opener",
        "input": "I'm thinking about going back to school.",
        "expected": "Asks grad vs undergrad first; does NOT ask experience or career",
    },
]


def main():
    project = os.getenv("LANGSMITH_PROJECT", "etb-daniels-admissions")
    print(f"Running {len(SCENARIOS)} scenarios — traces will appear in LangSmith")
    print(f"Project: {project}")
    print(f"Dashboard: https://smith.langchain.com/\n")

    chain = build_agent()

    for scenario in SCENARIOS:
        print("=" * 70)
        print(f"[{scenario['id']}] {scenario['name']}")
        print("=" * 70)
        print(f"INPUT:\n  {scenario['input']}\n")
        print(f"EXPECTED:\n  {scenario['expected']}\n")
        print("AGENT RESPONSE:")

        # The `metadata` config tags this trace so you can filter in LangSmith
        response = chain.invoke(
            scenario["input"],
            config={
                "metadata": {
                    "scenario_id": scenario["id"],
                    "scenario_name": scenario["name"],
                },
                "run_name": f"scenario_{scenario['id']}",
            },
        )
        print(response)
        print("\n")

    print("=" * 70)
    print("✅ All scenarios complete. Open LangSmith to inspect traces:")
    print("   https://smith.langchain.com/")
    print("=" * 70)


if __name__ == "__main__":
    main()
