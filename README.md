# Password Strength Lab

**AP Cybersecurity — Unit 1: Introduction to Security**

You are a penetration tester. Your client dumped 8 password hashes from an old
server. Your job: crack as many as you can, then explain to the client why the
strong ones survived.

## Setup

1. **Fork this repository** (button: `Fork`) so you have your own copy.
2. Clone **your fork**:
   ```
   git clone https://github.com/<your-username>/password-strength-lab.git
   cd password-strength-lab
   ```
3. Run the cracker:
   ```
   python3 crack.py
   ```

The cracker attacks in stages: dictionary, patterns (years, capitals, symbols,
digits, leetspeak), compound words, passphrase combos, then brute force.
Watch the clock — *when* each password falls tells you as much as *whether* it falls.

## Your task

Run the cracker, then fill in the table below in **your fork's README**.

| # | Algorithm | Cracked? (yes/no) | Password (if cracked) | Crack stage | Time (s) |
|---|-----------|-------------------|-----------------------|-------------|----------|
| 1 | MD5       |                   |                       |             |          |
| 2 | MD5       |                   |                       |             |          |
| 3 | SHA-1     |                   |                       |             |          |
| 4 | SHA-1     |                   |                       |             |          |
| 5 | SHA-256   |                   |                       |             |          |
| 6 | SHA-256   |                   |                       |             |          |
| 7 | SHA-1     |                   |                       |             |          |
| 8 | SHA-256   |                   |                       |             |          |

## Reflection questions

Answer below the table, in complete sentences.

1. Which passwords cracked in under one second? What do they have in common?
2. Hash #8 survived every attack. Look at what a 16-character random password
   costs to brute force. Why is length + randomness so expensive?
3. Rank the three hash algorithms from weakest to strongest. Does a stronger
   hash make a weak *password* safe? Use your results to justify your answer.
4. A classmate says: "My password has a capital letter, a symbol, and a digit,
   so it can't be cracked." Use your results to agree or disagree.
5. Name the single most important change you would make to a password you
   actually use, based on this lab.

## How you're graded

- Fill in all 8 table rows (Cracked? column must say yes or no) and answer the
  5 reflection questions.
- Commit and push to **your fork**. The `grade` workflow runs automatically and
  checks that your table is complete.

## Ethics

Everything here is for learning on passwords created for this lab. Never attempt
to crack accounts, hashes, or systems you do not own or do not have written
permission to test.
