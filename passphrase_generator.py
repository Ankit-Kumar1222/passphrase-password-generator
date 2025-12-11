import hashlib
import random
import re
import requests

# ---------------------------
# Leet (alphabet → numbers)
# ---------------------------
LEET = {
    "a": "4", "A": "4",
    "e": "3", "E": "3",
    "i": "1", "I": "1",
    "o": "0", "O": "0",
    "s": "5", "S": "5",
    "t": "7", "T": "7"
}

SPECIALS = ["!", "@", "#", "$", "%", "^", "&", "*", "?", "+", "_"]

# ----------------------------------------------------
# Step 1: Deterministic hashing → Seed for randomness
# ----------------------------------------------------
def deterministic_random(passphrase):
    h = hashlib.sha256(passphrase.encode()).hexdigest()
    seed = int(h, 16)
    return random.Random(seed)

# ----------------------------------------------------
# Step 2: Light leet transform for EASY mode
# ----------------------------------------------------
def easy_leet(word, rng):
    new = ""
    for ch in word:
        if ch in LEET and rng.random() < 0.3:   # Light replacement
            new += LEET[ch]
        else:
            new += ch
    return new

# ----------------------------------------------------
# Step 3: Heavy leet transform + mixing for HARD mode
# ----------------------------------------------------
def hard_leet(word, rng):
    new = ""
    for ch in word:
        if ch in LEET and rng.random() < 0.6:   # More aggressive
            new += LEET[ch]
        else:
            new += ch
    return new

# ----------------------------------------------------
# Step 4: Generate password from passphrase
# ----------------------------------------------------
def generate_password(passphrase, mode="easy"):
    rng = deterministic_random(passphrase)

    # Break into parts
    parts = re.split(r"[^A-Za-z0-9]+", passphrase)
    parts = [p for p in parts if p]

    if not parts:
        return "Invalid passphrase"

    # Apply leet transformations
    if mode == "easy":
        parts = [easy_leet(p, rng) for p in parts]
        sep = rng.choice(SPECIALS)
        pwd = sep.join(parts)

        # Add numbers if passphrase contains age/year
        digits = "".join(re.findall(r"\d+", passphrase))
        if digits:
            if rng.random() < 0.5:
                pwd = digits + sep + pwd
            else:
                pwd = pwd + sep + digits

    else:  # HARD MODE
        parts = [hard_leet(p, rng) for p in parts]

        # Insert special chars in between randomly
        pwd = ""
        for p in parts:
            pwd += p
            pwd += rng.choice(SPECIALS)

        # Mix the password slightly but keep it recognizable
        pwd_list = list(pwd)
        rng.shuffle(pwd_list)
        pwd = "".join(pwd_list)

        # Add numeric tail derived from hash
        h = hashlib.sha1(passphrase.encode()).hexdigest()
        tail = str(int(h[:6], 16) % 10000)
        pwd = pwd + rng.choice(SPECIALS) + tail

    # Ensure minimum length
    if len(pwd) < 10:
        extra = hashlib.md5(passphrase.encode()).hexdigest()[:10-len(pwd)]
        pwd += extra

    return pwd

# ----------------------------------------------------
# Step 5: Have I Been Pwned — k-Anonymity Breach Check
# ----------------------------------------------------
def hibp_breach_count(password):
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix = sha1[:5]
    suffix = sha1[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"

    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None

        hashes = r.text.splitlines()

        for line in hashes:
            hash_suffix, count = line.split(":")
            if hash_suffix == suffix:
                return int(count)

        return 0    # not found in breach
    except:
        return None

# ----------------------------------------------------
# MAIN PROGRAM (Simple CLI)
# ----------------------------------------------------
if __name__ == "__main__":
    print("\n=== Passphrase-Based Password Generator ===\n")
    passphrase = input("Enter your passphrase: ").strip()
    mode = input("Choose mode (easy / hard): ").strip().lower()

    if mode not in ["easy", "hard"]:
        mode = "easy"

    password = generate_password(passphrase, mode)
    print("\nGenerated Password:", password)

    print("\nChecking databreach (HaveIBeenPwned)...")
    count = hibp_breach_count(password)

    if count is None:
        print("HIBP Check Error (network issue).")
    elif count == 0:
        print("✔ SAFE: Password not found in leaked databases.")
    else:
        print(f"⚠ WARNING: This password appears in {count} breaches!")

    print("\nDone.\n")
