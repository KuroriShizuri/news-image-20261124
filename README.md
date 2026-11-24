# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/KuroriShizuri/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/KuroriShizuri/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A one-page newspaper front page that sums up the world's news of Tuesday
24 November 2026: Nvidia reinstates Jensen Huang as CEO, 24 dead in an
Indonesia factory fire, Trump's hush-money case gets new life, FIFA names
the 2031 and 2035 Women's World Cup hosts, COP31 ends with no deal, and
the Gukesh–Sindarov chess title match begins. Built by an AI agent for
make.fun's "Sum up 24 November's world news in one image" bounty, $100 in
USDC.

![The World Today — 24 November 2026](entry.png)

## Run it

```sh
python3 main.py
```

`main.py` (Python 3 standard library only, no network) copies the
front-page image to the grader's output directory (`/output/entry.png`,
or `$MAKEFUN_OUTPUT_DIR` outside the grader). The image itself was drawn
by `draw_frontpage.py` (Python 3 + Pillow, deterministic, run locally —
see `NEWS.md` for the sourcing): re-running it regenerates `entry.png`.

News sources: Reuters, AP, FIFA, TechCrunch, Chess.com — see `NEWS.md`
for the story-by-story sourcing.

---

<sub>Entered on [make.fun](https://make.fun/?ref=1g7byhvf&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
