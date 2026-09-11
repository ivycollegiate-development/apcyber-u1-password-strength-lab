# Password Strength Lab

**AP Cybersecurity — Unit 1: Introduction to Security**

You are a penetration tester. Your client dumped 8 password hashes from an old
server. Your job: crack as many as you can, then explain to the client why the
strong ones survived.

---

## Setup — what each step does and why it matters

### Step 1: Fork this repository

Click the **`Fork`** button at the top-right of this page, then click
**`Create fork`**. Leave every option as its default.

- **What this does:** creates a complete copy of this lab under *your* GitHub
  account. After this, `github.com/ivycollegiate-development/password-strength-lab`
  is the *upstream* (the teacher's copy) and
  `github.com/<your-username>/password-strength-lab` is *your* copy.
- **Why this is necessary:** you don't have permission to edit the teacher's
  repository. The fork gives you a copy you fully own, and — crucially — your
  completed work, commits, and results live in *your* copy, where the grading
  workflow runs. Without forking first, none of the later steps work.

### Step 2: Clone your fork to your computer

Copy *your fork's* URL from your browser's address bar. On your machine, run:

```
git clone https://github.com/<your-username>/password-strength-lab.git
cd password-strength-lab
```

Replace `<your-username>` with your actual GitHub username.

- **What this does:** makes a full working copy of your fork on the computer
  you're sitting at, and moves your terminal into that folder.
- **Why this is necessary:** `git clone` downloads the files (crack.py, the
  hashes, this README). The `cd` moves you inside the folder — every later
  command assumes you are already inside it. If you skip the `cd`, the next
  commands will fail with "no such file or directory."

**Check yourself:** run `pwd` and `ls`. You should see the lab files
(`crack.py`, `README.md`, `hashed_passwords.txt`) listed. If you don't, you are
in the wrong folder — go back and `cd` into `password-strength-lab`.

### Step 3: Run the cracker

```
python3 crack.py
```

- **What this does:** reads `hashed_passwords.txt` and attacks all 8 hashes in
  five escalating stages:
  1. **Dictionary attack** — tries the most common passwords first
     ("123456", "password", "letmein"). Instant.
  2. **Pattern attack** — common human patterns: years, capital letters,
     symbols, digits, leetspeak substitutions ("summer2026", "F00tb4ll&3").
  3. **Compound words** — Word$Word constructions ("Dragon$Fly").
  4. **Passphrase combos** — word-based passphrases
     ("correct-horse-battery-staple").
  5. **Brute force** — tries everything up to 5 characters. This stage is
     deliberately slow; watch how much *time* it burns to test so few
     possibilities.
- **Why this matters:** *when* a password falls tells you as much as *whether*
  it falls. A password cracked in 0.000s (dictionary stage) is catastrophically
  weak no matter how many symbols it contains. A password that survives all
  five stages is the strong one.
- **Let it finish.** Stage 5 takes about a minute. The final summary table is
  the output you need — 7 passwords cracked, 1 not cracked.

### Step 4: Record your results in README.md

Open `README.md` in your editor (or on GitHub). Find the results table and
fill in **every cell of all 8 rows**. It looks like this when blank — this is
what you will fill in:

| # | Algorithm | Cracked? (yes/no) | Password (if cracked) | Crack stage | Time (s) |
|---|-----------|-------------------|-----------------------|-------------|----------|
| 1 | MD5       |CRACKED            |123456                 |0.000        |          |
| 2 | MD5       |CRACKED            |password               |0.000        |          |
| 3 | SHA-1     |CRACKED            |letmein                |0.000        |          |
| 4 | SHA-1     |CRACKED            |summer2026             |0.021        |          |
| 5 | SHA-256   |CRACKED            |Dragon$Fly             |             |0.040     |
| 6 | SHA-256   |CRACKED            |F00tb4ll&3             |             |0.017     |
| 7 | SHA-1     |CRACKED            |correct-horse-battery-staple|0.066   |          |
| 8 | SHA-256   |NOT CRACKED        |                       |             |          |

For example, a completed row for a password that fell to the dictionary attack
would read:

| 1 | MD5       | yes               | 123456                | 1           | 0.000    |

For the row that says `NOT CRACKED` when the cracker finishes, put `no` in the
Cracked? column and a dash (`—`) in the Password, Crack stage, and Time
columns.

**Important:** save the file (`Ctrl+S` / `Cmd+S`) before moving on. The grading
robot reads the file on GitHub — if you didn't save locally, GitHub sees
nothing.

### Step 5: Save, commit, and push your report — this is the step people skip

Filling in the table in your editor changes the file **only on your computer**.
GitHub does not see it yet. Three separate actions move it from your editor to
your graded repository. Run these in the terminal, one at a time:

```
git add README.md
```
- **What this does:** stages the file — tells git "I want this file's current
  saved contents included in my next commit."
- **Why this is necessary:** git never snapshots files automatically. Without
  `git add`, your edits are invisible to every later git command. `git add` is
  the bridge between "I saved a file in my editor" and "git knows this changed."
  If you edited more than README.md, use `git add .` (with the dot) to stage
  everything.

```
git commit -m "Complete password strength lab results"
```
- **What this does:** saves a permanent snapshot of the staged changes into
  your local repository history, labeled with the message after `-m`.
- **Why this is necessary:** a commit is the unit of recorded work. This is the
  moment your results are actually *recorded* — locally. But your local
  repository is still private to your machine; GitHub doesn't know it exists.

```
git push origin main
```
- **What this does:** uploads every commit from your computer to your fork on
  GitHub (`origin` = your fork's URL, `main` = the branch).
- **Why this is necessary:** **this is the step that makes your work real.**
  Until you push, GitHub has the old blank README, the grading workflow never
  sees your table, and your work exists only on your laptop. Push is the final
  delivery.

**Verify it worked — do not skip this:**
1. Go to `https://github.com/<your-username>/password-strength-lab` in your
   browser and refresh the page. You should see YOUR table, not the blank one.
   If you still see the blank template, the push didn't land — re-run the three
   commands above from the lab folder.
2. Click the **`Actions`** tab at the top of your fork. You should see a
   workflow run for your push — click into it and confirm it ends with
   **`PASS: results table complete`**. A red ✗ means the grader found a
   problem — most often an unfilled cell, meaning you didn't save before
   committing.

---

## Reflection questions

Answer below the table, in complete sentences, then save + commit + push
again (same three commands as Step 5).

1. Which passwords cracked in under one second? What do they have in common?
2. Hash #8 survived every attack. Look at what a 16-character random password
   costs to brute force. Why is length + randomness so expensive?
3. Rank the three hash algorithms from weakest to strongest. Does a stronger
   hash make a weak *password* safe? Use your results to justify your answer.
4. A classmate says: "My password has a capital letter, a symbol, and a digit,
   so it can't be cracked." Use your results to agree or disagree.
5. Name the single most important change you would make to a password you
   actually use, based on this lab.

---

## How you're graded

The `grade` workflow runs automatically on every push to your fork and checks:
- all 8 result rows exist,
- the Cracked? column says yes or no in every row.

If any check fails, the workflow shows a red ✗ — fix README.md, save, then
`git add` → `git commit` → `git push` again.

---

## Ethics

Everything here is for learning on passwords created for this lab. Never attempt
to crack accounts, hashes, or systems you do not own or do not have written
permission to test.