# passphrase-password-generator
=============================================
 Passphrase-Based Password Generator (Python)
=============================================

This project generates strong, memorable passwords using a natural 
passphrase (example: "my grandfather ramesh 72 delhi").

The password generator supports two modes:
--------------------------------------------
1) EASY MODE
   - Only light letter→number replacements (leet)
   - Adds one special character between words
   - Keeps the structure easy to remember

2) HARD MODE
   - Heavy letter→number replacements
   - Adds multiple special characters randomly
   - Shuffles parts of the password
   - Adds numeric tail based on SHA-1 hash
   - Much stronger password

Features:
---------
✔ Converts passphrase into a memorable but strong password  
✔ Deterministic → Same passphrase always gives same password  
✔ Letter→Number mapping: a→4, e→3, i→1, o→0, s→5, t→7  
✔ Detects digits (like age or year) and includes them smartly  
✔ Inserts special characters like !, @, $, %, ^  
✔ Checks generated password in data breaches using  
   “Have I Been Pwned” (k-anonymity API)  
✔ Minimum 10-character password enforced  

Requirements:
-------------
- Python 3.x  
- requests library  

Install dependencies:
----------------------
pip install -r requirements.txt

How to run:
-----------
python passphrase_generator.py

Then enter:
-----------
Enter your passphrase: my grandfather ramesh 72 delhi
Choose mode (easy / hard): easy

Example output:
---------------
Generated Password: R4mesh$Delh1$72

✔ SAFE: Password not found in leaked databases.

Files included:
---------------
- passphrase_generator.py   → main Python program
- README.txt                → project documentation
- requirements.txt          → Python dependencies

Notes:
------
- Only the GENERATED PASSWORD is checked in the breach database.
- Your original passphrase is NEVER sent to the internet.
- Hard mode passwords are much more secure but still recallable.

License:
--------
Free to use for learning, portfolios, and projects.
