Project Name:
- Fuzzer

Project Team:
DANIEL CHO dc9865@rit.edu

Installation
Clone this repository to an empty directory
Install all dependencies (Use pip3)

Dependencies
Python 3.5
Beautiful soup (pip3 install beautifulsoup4)
Mechanical soup (pip3 install mechanicalsoup)

Example usage for discovery:
# Discover inputs, default extensions, no login
  python fuzz.py discover http://localhost:8080 --common-words=mywords.txt

# Discover inputs to DVWA using our hard-coded authentication, port 8080
  python fuzz.py discover http://localhost:8080 --custom-auth=dvwa --extensions=extensions.txt --common-words=mywords.txt

# Discover and Test DVWA, port 8000, default extensions: sanitized characters, extensions and slow threshold
  python fuzz.py test http://localhost:8000 --custom-auth=dvwa --common-words=words.txt --vectors=vectors.txt --sensitive=creditcards.txt
