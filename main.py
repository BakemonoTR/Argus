from dotenv import load_dotenv
from core.graph import build_graph
from core.github_client import get_pr_diff, post_pr_comment
from github import Github
import os

load_dotenv()

REPO_NAME = os.getenv("REPO_NAME", "your-username/autonomous-quality-pipeline")
PR_NUMBER = int(os.getenv("PR_NUMBER", "1"))
USE_FAKE_DIFF = os.getenv("USE_FAKE_DIFF", "true").lower() == "true"

if USE_FAKE_DIFF:
    pr_diff = """
+ import subprocess
+ password = "admin123"
+ API_KEY = "sk-1234567890abcdef"
+ def run_query(user_input):
+     query = "SELECT * FROM users WHERE id = " + user_input
+     return db.execute(query)
+
+ def find_duplicates(items):
+     duplicates = []
+     for i in items:
+         for j in items:
+             if i == j:
+                 duplicates.append(i)
+     return duplicates
"""
    files_changed = []
    print("Using fake diff for local testing\n")
else:
    print(f"Fetching PR #{PR_NUMBER} from {REPO_NAME}...\n")
    pr_diff = get_pr_diff(REPO_NAME, PR_NUMBER)

    # Get list of changed files
    g = Github(os.getenv("GITHUB_TOKEN"))
    repo = g.get_repo(REPO_NAME)
    pr = repo.get_pull(PR_NUMBER)
    files_changed = [f.filename for f in pr.get_files()]

    # Pass source branch to env so autofix_node can use it
    os.environ["SOURCE_BRANCH"] = pr.head.ref

graph = build_graph()

initial_state = {
    "pr_diff": pr_diff,
    "files_changed": files_changed,
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

print(f"Overall: {result['overall_summary']}")
print(f"Critical issues: {result['critical_issues']}")
print(f"Auto-fix needed: {result['should_autofix']}\n")

if not USE_FAKE_DIFF:
    print("Posting comment to GitHub PR...")
    post_pr_comment(REPO_NAME, PR_NUMBER, result)
else:
    print("Skipping GitHub comment (local mode)")
    from core.github_client import _build_markdown_comment
    print(_build_markdown_comment(result))