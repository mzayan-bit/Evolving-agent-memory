"""Validate literature artifact structure using only the Python standard library."""
import csv
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
LIT = ROOT / 'literature'
rows = list(csv.DictReader((LIT / 'master_paper_matrix.csv').open()))
assert len(rows) == 100
assert len({r['paper_id'] for r in rows}) == len(rows)
assert all(None not in r and all(v is not None for v in r.values()) for r in rows)
assert all(r['title'] and r['authors'] and r['paper_url'] for r in rows)
assert len(list((LIT / 'deep_reads').glob('*.md'))) == 25
required = ['Research Problem', 'Why This Paper Exists', 'Method', 'Memory Lifecycle Covered',
            'Representation', 'Controller / Decision Policy', 'Datasets', 'Baselines', 'Metrics',
            'Main Findings', 'Ablations', 'What It Actually Solves', 'What It Does NOT Solve',
            'Author-Stated Limitations', 'Additional Limitations We Observe',
            'Relationship to Other Papers', 'Relevance to EvoMem',
            'Does It Threaten Our Proposed Novelty?', 'Evidence']
for p in (LIT / 'deep_reads').glob('*.md'):
    text = p.read_text()
    assert text.startswith('# Citation')
    assert all('## ' + h in text for h in required), p
bib = (LIT / 'references.bib').read_text()
assert len(re.findall(r'^@misc\{', bib, re.M)) == 100
for p in ROOT.rglob('*.json'):
    json.loads(p.read_text())
for p in ROOT.rglob('*.md'):
    for href in re.findall(r'\]\(([^\s)]+)\)', p.read_text()):
        if ':' in href or href.startswith('#'):
            continue
        target = (p.parent / href.split('#')[0]).resolve()
        assert target.exists(), (p, href)
report = ROOT / 'RESEARCH_GAP_REPORT.md'
if report.exists():
    nums = [int(n) for n in re.findall(r'^## (\d+)\.', report.read_text(), re.M)]
    assert nums == list(range(1, 21)), nums
stats = json.loads((LIT / 'review_stats.json').read_text())
assert stats['retained_unique_works'] == len(rows)
assert sum(stats['first_public_year_distribution'].values()) == len(rows)
assert stats['deep_reads'] + stats['targeted_additional'] + stats['screened_only'] == len(rows)
print('PASS: 100 unique CSV/BibTeX records, 25 complete deep-read structures, JSON, relative links and report sections.')
