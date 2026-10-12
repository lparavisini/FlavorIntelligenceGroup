import re

# 1. Read the file
with open('publications.html') as f:
    content = f.read()

# 2. Find the <ul class="pub-list"> section — this captures everything
#    between the opening and closing tags
match = re.search(r'(<ul class="pub-list">\n)(.*?)(\n\s*</ul>)', content, re.DOTALL)
ul_open, body, ul_close = match.group(1), match.group(2), match.group(3)

# 3. Split that section into a list of individual <li>...</li> blocks
entries = re.findall(r'(\s*<li class="pub-entry">.*?</li>)', body, re.DOTALL)

# 4. A function that pulls the year out of one entry's text
#    (looks for a 4-digit number starting with 19 or 20)
def get_year(entry):
    years = re.findall(r'\b(?:19|20)\d{2}\b', entry)
    return int(years[-1]) if years else 0

# 5. Sort the entries by year, newest first
#    reverse=True means descending order
entries_sorted = sorted(entries, key=get_year, reverse=True)

# 6. Rebuild the file: same opening/closing, but reordered entries in between
new_body = '\n'.join(entries_sorted)
new_content = content[:match.start()] + ul_open + new_body + ul_close + content[match.end():]

# 7. Save it
with open('publications.html', 'w') as f:
    f.write(new_content)

print(f"Reordered {len(entries_sorted)} entries, most recent first.")
