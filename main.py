from dotenv import load_dotenv
from core.graph import build_graph

load_dotenv()

fake_diff = """
+ import subprocess
+ password = "admin123"
+ def run_query(user_input):
+     query = "SELECT * FROM users WHERE id = " + user_input
+     return db.execute(query)
"""

graph = build_graph()

# State'i başlatıyoruz — sadece pr_diff var, gerisini agent dolduracak
initial_state = {
    "pr_diff": fake_diff,
    "security_findings": [],
    "summary": ""
}

print("Running pipeline...\n")
result = graph.invoke(initial_state)

print(f"Summary: {result['summary']}\n")
print(f"Found {len(result['security_findings'])} issue(s):\n")

for i, finding in enumerate(result["security_findings"], 1):
    print(f"[{i}] Severity {finding['severity']}/10 — Line {finding['line']}")
    print(f"    Issue:      {finding['issue']}")
    print(f"    Suggestion: {finding['suggestion']}\n")