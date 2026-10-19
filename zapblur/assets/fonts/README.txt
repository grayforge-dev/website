# Fonts

Self-hosted so that the pages make no request to any other host.

| Files | Family | Weight | Source |
|---|---|---|---|
| `IBMPlexSansKR-Regular-00.woff2` ... `-93` | IBM Plex Sans KR | 400 | npm `@ibm/plex-sans-kr` 1.1.0, `fonts/split/woff2/hinted/` |
| `IBMPlexSansKR-SemiBold-00.woff2` ... `-93` | IBM Plex Sans KR | 600 | same |
| `IBMPlexMono-Medium.woff2` | IBM Plex Mono | 500 | npm `@ibm/plex-mono` 2.5.0, `fonts/complete/woff2/` (the wordmark and the numbers; the 400 weight is not used on these pages) |

Plex Sans KR is IBM's own split build: 94 slices a weight, each with the `unicode-range` IBM published (copied into `../zapblur.css`),
so the browser fetches only the slices that hold the characters of the page it shows. The files are IBM's, byte for byte (nothing is
subset, converted or renamed here): the Reserved Font Name "Plex" only restricts modified versions. License: SIL Open Font License
1.1, Copyright 2017 IBM Corp. (`OFL-IBMPlexSansKR.txt`, `OFL-IBMPlexMono.txt`, the texts that ship in the npm packages). Keep both
license files next to the fonts. `SHA256SUMS` has the hash of every font file.
