from dotenv import load_dotenv
from core.graph import build_graph
from core.github_client import get_pr_diff, post_pr_comment
import os

load_dotenv()

# --- Config ---
# In GitHub Actions these come from environment variables
# For local testing, set them manually here
REPO_NAME = os.getenv("REPO_NAME", "your-username/your-repo")
PR_NUMBER = int(os.getenv("PR_NUMBER", "1"))
USE_FAKE_DIFF = os.getenv("USE_FAKE_DIFF", "true").lower() == "true"

# --- Get PR diff ---
if USE_FAKE_DIFF:
    pr_diff = """
+ import subprocess
+ password = "admin123"
+ def run_query(user_input):
+     query = "SELECT * FROM users WHERE id = " + user_input
+     return db.execute(query)
+
+ def calculate_total(items):
+     total = 0
+     for item in items:
+         for price in item["prices"]:
+             total += price
+     return total
+
+ def x(a, b):
+     return a+b
"""
    print("Using fake diff for local testing\n")
else:
    print(f"Fetching PR #{PR_NUMBER} from {REPO_NAME}...\n")
    pr_diff = get_pr_diff(REPO_NAME, PR_NUMBER)

# --- Run pipeline ---
graph = build_graph()

initial_state = {
    "pr_diff": pr_diff,
    "security_findings": [],
    "performance_findings": [],
    "style_findings": [],
    "test_findings": [],
    "security_summary": "",
    "performance_summary": "",
    "style_summary": "",
    "test_summary": "",
    "conflicts": [],
    "critical_issues": [],
    "should_autofix": False,
    "overall_summary": ""
}

print("Running pipeline...\n")
result = graph.invoke(initial_state)

# --- Print to terminal ---
print(f"Overall: {result['overall_summary']}")
print(f"Critical issues: {result['critical_issues']}")
print(f"Auto-fix needed: {result['should_autofix']}\n")

# --- Post to GitHub PR (only in CI, not local) ---
if not USE_FAKE_DIFF:
    print("Posting comment to GitHub PR...")
    post_pr_comment(REPO_NAME, PR_NUMBER, result)
else:
    print("Skipping GitHub comment (local mode)")
    print("\n--- Preview of PR comment ---\n")
    from core.github_client import _build_markdown_comment
    print(_build_markdown_comment(result))