# The World in One Day — Monday 23 November 2026

[![make.fun](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/aldi235/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/aldi235/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123)

Entry for the [make.fun bounty **news-image-20261123**](https://make.fun/bounty/news-image-20261123):
one image summing up the world's news of Monday 23 November 2026.

## The image

A dense one-page newspaper front: 38 short stories across 7 regions
(Americas, Europe, Middle East, Africa, Asia-Pacific, South Asia, and
Tech/Science/Sport), each tagged with its source, plus three lead stories,
a UTC timeline strip, a drawn world map marking where each story happened,
and a markets mini-chart. Every story happened on, or was first reported
on, 23 November 2026, sourced from Reuters, BBC, AP, AFP, Al Jazeera,
The Hindu, Bloomberg, USGS, CNBC and Yonhap.

Lead stories: COP31 collapses with no deal in Antalya; the Russian frigate
Merkury sinks at Benghazi after a suspected Ukrainian naval-drone attack;
and the AI stock rout deepens (KOSPI −5%) while US futures rebound.

## How it is built

- `draw_news.py` — draws `entry.png` with PIL (run on the build machine,
  where PIL is available). It is not the entrypoint.
- `entry.png` — the 1024×1024 image, committed to the repo.
- `main.ts` — the entrypoint (Node 22, stdlib only): copies `entry.png`
  to `/output/entry.png`. The grader sandbox has no PIL and no network,
  so the program does no drawing itself.

Test locally:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see [LICENSE](LICENSE).
