import re, sys, os

# Skip the results-table check on the template (upstream) repo's own pushes:
# the master README is intentionally blank; students' forks fill it in.
branch = os.environ.get("GITHUB_REF_NAME", "")
repo_full = os.environ.get("GITHUB_REPOSITORY", "")
TEMPLATE_REPO = "ivycollegiate-development/password-strength-lab"
if repo_full == TEMPLATE_REPO and branch == "main":
    print(f"template repo push ({repo_full}@{branch}) — skipping results-table check")
    sys.exit(0)

md = open("README.md").read()
rows = re.findall(r"^\|\s*(\d+)\s*\|", md, re.M)
if len(rows) < 8:
    print(f"FAIL: expected 8 numbered result rows, found {len(rows)}")
    sys.exit(1)
answered = 0
for line in md.splitlines():
    m = re.match(r"^\|\s*\d+\s*\|", line)
    if not m:
        continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    # cells: [#][algo][cracked?][password][stage][time]
    if len(cells) >= 3 and cells[2].lower() in ("yes", "no"):
        answered += 1
print(f"answered rows (yes/no filled): {answered}/8")
if answered < 8:
    print("FAIL: fill in the Cracked? column (yes/no) for all 8 rows")
    sys.exit(1)
print("PASS: results table complete")
