# Artifact validation

Date:19 September 2026. This verifies research artifacts, not the correctness of independent experimental reproductions; none was run.

- 100 unique retained paper IDs with title/author/date/version metadata;38 CSV fields, structurally parsed with quoted cells.
- 25 deep-read files with all requested headings.
- 100 BibTeX entries parsed; first-public year and pinned arXiv URL retained without fabricated conference fields.
- 20 numbered report sections plus references.
- Markdown parsed to HTML with tables enabled; local relative links checked for existence. Large master matrix uses a compact index plus per-paper fields rather than an unreadable full-width table.
- 104 source records screened; duplicate MemOS treatment, accidental physics lead and two lower-priority records excluded/grouped. No inspected revision is after19 September 2026.
- 134 primary/canonical/code URLs checked by HTTP GET:132 returned200. All100 pinned arXiv paper URLs returned200.
- Exceptions: ACM DOI10.1145/3748302 returned403 (access restriction; bibliographic metadata was separately identified). The paper-linked TOKI repository returned404; the matrix explicitly marks its code as unavailable/unverified. These are not silently counted as working links.
- Code/project associations come from paper text/metadata; source licenses, exact code commits and experiment reproducibility were not audited.
- Numerical spot checks included Mem-alpha and Memory-R1 GPU requirements, StateAuditor strict versus privileged protocols, MemTX backbone-dependent task success, rollback recovery/recurrence and Hindsight's unresolved retrieval-budget placeholder.
- No EvoMem controller, pipeline, benchmark generator or experiment was implemented. Only a standard-library artifact validator was added as executable research-support code.

Re-run `python research/scripts/validate_artifacts.py` from a checkout. HTTP outcomes are preserved in [url_verification.json](url_verification.json); source versions/hashes in [source_manifest.json](source_manifest.json). HTTP reachability is not evidence that every scientific claim is correct.
