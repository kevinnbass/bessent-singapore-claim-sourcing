"""Re-run the checks from the files in this repository alone.  Run: python3 scripts/check_repo.py
1. the post with references, with the [n] markers taken out, is the post as sent (less its one old marker "[58]")
2. every marker has a reference and every reference is cited
3. every quotation of post/quote_check.tsv is in the saved text of the reference it is cited to
4. every line of post/support_check.tsv is in the saved text of its reference
5. every row of the figure's data sums to its total
A control (words that are in no source) must fail, or the script stops."""
import csv, html, re, sys
from pathlib import Path
R = Path(__file__).resolve().parents[1]

def norm(t):
    for a, b in (('ﬁ', 'fi'), ('ﬂ', 'fl'), ('ﬀ', 'ff'), ('ﬃ', 'ffi'), ('ﬄ', 'ffl'), ('’', "'"), ('‘', "'"),
                 ('ʼ', "'"), ('“', '"'), ('”', '"'), (' ', ' '), ('–', '-'), ('—', '-'), ('­', '')):
        t = t.replace(a, b)
    return re.sub(r'\s+', ' ', t)

def bare(t): return re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9 ]+', ' ', norm(t).lower())).strip()

def rows(name): return list(csv.DictReader(open(R / 'post' / name, encoding='utf-8'), delimiter='\t'))

refs = {int(r['number']): r for r in rows('references.tsv')}
_t = {}
def text(n):
    if n in _t: return _t[n]
    t = ''
    for i in refs[n]['saved_ids'].split():
        if i.startswith('fox-smf'):
            t += ' ' + re.sub(r' ?\[speech model[^\]]*\]', '', norm((R / 'transcript/bessent_fox_20261115_passage.md').read_text(encoding='utf-8')))
            continue
        for d in R.glob(f'sources/*/{i}'):
            for name in ('text.txt', 'text.article.txt'):
                if (d / name).exists(): t += ' ' + (d / name).read_text(encoding='utf-8', errors='replace')
            if len(t.strip()) < 2000:      # a page whose words sit in the saved original, not in the extracted text
                for b in d.glob('body.htm*'):
                    raw = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', b.read_text(encoding='utf-8', errors='replace'), flags=re.S)
                    t += ' ' + html.unescape(re.sub(r'<[^>]+>', ' ', raw))
    _t[n] = norm(t); return _t[n]

def has(n, words, loose=False):
    return (bare(words) in bare(text(n))) if loose else (norm(words).lower() in text(n).lower())

bad = []
full = (R / 'post/POST_with_references.txt').read_text(encoding='utf-8')
body = full.split('\n\n\nReferences\n', 1)[0] + '\n'
orig = (R / 'post/POST_original.txt').read_text(encoding='utf-8')
if re.sub(r' \[\d+(?:,\d+)*\]', '', body) != orig.replace(' [58]', ''): bad.append('1: the text was changed')
cited = {int(x) for m in re.finditer(r' \[(\d+(?:,\d+)*)\]', body) for x in m.group(1).split(',')}
listed = {int(m.group(1)) for m in re.finditer(r'^\[(\d+)\] ', full.split('\n\n\nReferences\n', 1)[1], flags=re.M)}
if cited != listed or cited != set(refs): bad.append(f'2: markers and references do not match: {sorted(cited ^ listed)}')
nq = absent = 0
for r in rows('quote_check.tsv'):
    if r['result'].startswith('his own words'): continue
    nums = [int(x) for x in re.findall(r'\[(\d+)\]', r['result'])]
    q = re.sub(r' \[sic\]$', '', norm(r['quotation'])).rstrip('.').strip()
    parts = [p.strip(' .') for p in re.split(r'\.\.\.', q) if len(p.strip(' .')) > 8]
    if r['result'].startswith('WORDS DIFFER'):
        print('   noted, not checked:', r['result'], '|', r['quotation'][:70]); continue
    loose = 'punctuation' in r['result']
    held = [n for n in nums if refs[n]['saved_ids'] and text(n).strip()]
    if not held: absent += 1; continue
    nq += 1
    if not any(all(has(n, p, loose) for p in parts) for n in held): bad.append('3: quotation not found: ' + r['quotation'][:80])
ns = 0
for r in rows('support_check.tsv'):
    if not text(int(r['reference'])).strip(): absent += 1; continue
    ns += 1
    if not has(int(r['reference']), r['words_of_the_source']): bad.append('4: words not found: ' + r['words_of_the_source'][:80])
if has(min(n for n in refs if refs[n]['saved_ids'] and 'fox' not in refs[n]['saved_ids'] and text(n).strip()), 'these words are in no source at all, by design'): bad.append('control: the check cannot fail')
for r in csv.DictReader(open(R / 'figure/nvidia_region_quarterly_both_bases.csv', encoding='utf-8')):
    s = sum(int(r[k]) for k in ('united_states', 'singapore', 'taiwan', 'china_incl_hong_kong', 'other') if r[k] not in ('', 'NA', 'None'))
    if s != int(r['total']): bad.append('5: a figure row does not sum: ' + r['quarter_ended'])
print(f'markers {len(cited)} numbers, references {len(refs)}, quotations checked {nq}, supporting lines checked {ns}, not held in this copy {absent}')
if bad:
    print('FAILED'); print('\n'.join(bad)); sys.exit(1)
print('all checks pass')
