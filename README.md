# Bessent on Nvidia's "Singapore" sales: the post, its references and its data

On Nov 15, 2026 the US Treasury Secretary, Scott Bessent, said on Fox News that Nvidia's accounts show its Chinese sales
crashing and its Singaporean sales going "through the roof", that Nvidia "stopped publishing" them, and that he had seen
reporting that only 1% of the chips sold in Singapore remained there. This repository holds a post that goes through
those 21 seconds, the documents it cites, and the data behind its figure and tables.

The post was published on X on Nov 19, 2026: https://x.com/kevinnbass/status/2123219344976941482. The text here is
the text as published; the reference list is below it in `post/POST_with_references.txt`.

## What is here

| Folder | What it holds |
|---|---|
| `post/POST_with_references.txt` | The post with numbered references ([1], [1,2]) and a reference list at the end. |
| `post/POST_original.txt` | The post as written, before the references were added. The only difference is the markers. |
| `post/references.tsv` | Each reference: its number, how it is held, its citation and address, and the folder of its copy. |
| `post/quote_check.tsv` | Every quotation in the post, with the reference whose saved text contains it. |
| `post/support_check.tsv` | For claims that are not quotations: the words of the cited source that carry them. |
| `post/tables_in_post.tsv` | Every figure in the post's tables, with the references of its table. |
| `figure/` | The figure (Nvidia's revenue by region on both bases) as a web page, its data, and the list of its 22 documents. |
| `docs/index.html` | The same figure as a stand-alone page. |
| `data/press_items.tsv`, `data/press_counts.tsv` | 201 dated press items, statements and letters on the Singapore line, each marked by how it reads the line; counts by period. |
| `data/peers_*.csv` | Singapore revenue lines of other chip companies, with the address each figure was read at. |
| `data/nvidia_geo_revenue.csv` | Nvidia's geographic revenue rows as filed, with the filing each comes from. |
| `transcript/` | The passage of the interview, as transcribed. |
| `sources/documents/` | Filings, rules and official statements: the saved original and its text. |
| `sources/press_and_analysis/` | News stories and analysts' pages the post cites: their addresses and the hashes of the copies checked (no text). |
| `scripts/check_repo.py` | Re-runs the checks from the files here. |

## How the references are held

The post has {n_refs} references. {n_saved} are held here as saved copies. {n_read} are other companies' annual reports,
which were read on sec.gov and are not held as copies: their figures are in `post/tables_in_post.tsv` and `data/`, each
with the address it was read at. The rest are the figure, the press list and the interview, which are in this repository
as data and a transcript.

Hand-saved copies of newspaper pages carry the address printed in the page header, which can be cut short; where it is,
the reference gives no link.

## Checking it

```
python3 scripts/check_repo.py
```

It confirms that taking the markers out of the referenced post gives back the post as written, that every quotation is in
the saved text of the reference it is cited to, that the supporting words for the other claims are in their sources, and
that every row of the figure's data sums to its total. A deliberately false line must fail.

## Limits

- **The interview.** The words are from Fox's captions and a speech program, not from an official transcript.
- **The press list.** It is what searches and hand-saving found, not a census of the press. Whether an article that prints
  the caveat under a misleading headline misreads the line is a judgement; the marks record that judgement.
- **Other companies' figures.** Read on sec.gov, not held as saved copies.
- **The figure.** No single filing contains its tables: each filing gives its own quarter and the same quarter a year
  earlier. Quarters Nvidia did not report on their own are got by subtraction. The composite panel joins two different
  measures, and the page says so.
- **What the figures cannot show.** Both of Nvidia's tables count where its direct customers are billed or headquartered.
  Neither shows where goods were shipped.

## The copies

The filings, rules and official statements are public documents. The news stories and analysts' pages, and the two
earnings-call transcripts, belong to their publishers and are not copied here: each has a `meta.json` with its address
and the hash of the copy the quotations were checked against. The check script counts those quotations as "not held here".
