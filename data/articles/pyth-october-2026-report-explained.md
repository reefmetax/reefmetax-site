---
title: Pyth's October 2026 Report in Plain English: $13.67M ARR, Treasury Curves and the Kalshi Midterms Index
date: 2026-11-04
description: What the numbers in Pyth's October 2026 report mean, what shipped across Pyth Pro and Pyth Indices, and how Pyth became the data source for Kalshi's KPOW Midterms index.
---
Pyth dropped its [October 2026 report](https://x.com/PythNetwork/status/2117617814869622985) on November 3, and the same day it showed up as the data source behind Kalshi's new midterms index. That is a lot of news in one week, so here is a plain-English walk through what the report says and why people in the community are talking about it. Every number below comes straight from Pyth's own posts.

## The headline numbers

ARR stands for annual recurring revenue. It is the yearly value of paid subscriptions if they kept running at the current rate, a common way to measure a subscription business. Here is what the report shows for October:

- **ARR:** $13.67 million at the end of October, up 18.9% from the $11.49 million in the September report.
- **Gross new ARR:** $2.49 million added during the month, with 29% coming through the self-serve checkout.
- **Net new ARR:** $2.17 million, and 44.6% of gross new ARR came from existing customers expanding what they pay for.
- **Self-serve new ARR:** $725K, which Pyth says is 1.5x September.
- **Paying accounts:** 332.

The part I like is that almost half of the new revenue came from accounts that were already paying. That tells you existing customers found enough value to buy more.

## Pyth Terminal is pulling people in

Pyth Terminal is the place where people explore and compare Pyth's data before they plug it into an app. In October it had 124,705 unique visitors, up 19% month over month, and 4,451 signups, up 37%. The report counted 591,621 feed views across the Terminal, and 482,177 of those were Pyth Indices feeds.

## What shipped on Pyth Pro

Pyth Pro is the paid subscription for institutional-grade market data. It ended October with 3,927 symbols in its catalog, and 114 new feed IDs were first recorded during the month. A few highlights:

- [Four Korean stocks](https://x.com/PythNetwork/status/2112914364412166394), SK Hynix, Samsung Electronics, Hyundai Motor and Samsung Electro-Mechanics, now publish prices through Korea's post-market session, which adds four more hours of live prices each trading day.
- [More markets were added](https://x.com/PythNetwork/status/2116201796234629388), including expanded China equity coverage, more Japanese equities, more energy commodity futures and VIX futures. Pyth also posted that [21 Japanese equities](https://x.com/PythNetwork/status/2117293207344263578), including Toyota, Sony and Nintendo, are available through Pyth Pro.
- Pyth Pro MCP Server 1.1 made it easier for AI agents to find feeds and pull historical prices, and the report says Exa is testing Pyth as a market data layer for agentic search, in an early testing phase.

## Pyth Indices and the Treasury curve

Pyth Indices grew from 50 to 77 stable feeds in October, with 31 more marked as coming soon, and reached $2.88 million in ARR across 21 clients. New indices included AMD, Marvell, Alibaba, SPY, QQQ, EWZ and a diesel index.

The biggest addition was the [US Treasury par curve in real time](https://x.com/PythNetwork/status/2115814815759561164). That is 14 constant-maturity feeds covering the 2, 3, 5, 7, 10, 20 and 30 year maturities, each with a par yield and a discount factor. In simple terms, apps can now follow the shape of US interest rates through the trading session without tracking individual bonds.

Pyth also made corporate action data available for supported US stocks. That means records of cash dividends and stock splits, with dates, amounts and ratios, sourced from Exchange Data International. If a stock splits, an app can see why the price changed instead of guessing.

## The Kalshi Midterms Index

On November 3, Kalshi Research [introduced KPOW Midterms](https://x.com/KalshiResearch/status/2117636019604389956), which it called the first tradable political index on Kalshi. It combines each party's performance in the midterms into one measure of political power. Pyth [posted that the index](https://x.com/PythNetwork/status/2117637504924831775) is sourced and published exclusively by Pyth, and every contract on it settles to Pyth's values.

Pyth also published a [piece on how the index settles](https://x.com/PythNetwork/status/2117708069366825304), saying settlement references values published by Pyth, with price checks on inputs and time-weighted settlement built into the method. For anyone who read my [Pyth explainer](https://reefmetax.com/articles/pyth-network-price-oracles-explained/), this is the oracle idea in action: a market needs one trusted number to settle on, and Pyth is supplying it.

## A few more things from the last few weeks

- Pyth said its data powered [more than $2 trillion in notional volume](https://x.com/PythNetwork/status/2113345177293295870) on traditional assets across offshore derivatives venues in Q3, with around $1.3 trillion of that in equity perps.
- On ICE's Q3 earnings call, Chair and CEO Jeff Sprecher [cited Pyth data on oil perpetuals](https://x.com/PythNetwork/status/2116138323915988998).
- The PIRB crew had fun with it too, posting a [DAO reaction meme](https://x.com/thePIRB/status/2117675725931131174) to the $13.67M number.

## The takeaway

October was a month of steady building: more paying customers, more markets, rates data, and a brand new kind of market settling on Pyth prices. This is not financial advice and I am not making any calls, I just love seeing the projects we follow ship real things.

Thanks for reading, pack. If you have a question about Pyth you want me to cover next, drop it in my replies on X.

## Sources

- Pyth Network on X, [October 2026 report](https://x.com/PythNetwork/status/2117617814869622985), [KPOW Midterms](https://x.com/PythNetwork/status/2117637504924831775), [Kalshi settlement article](https://x.com/PythNetwork/status/2117708069366825304), [Treasury curve](https://x.com/PythNetwork/status/2115814815759561164), [Korean stocks](https://x.com/PythNetwork/status/2112914364412166394), [new Pyth Pro markets](https://x.com/PythNetwork/status/2116201796234629388), [Japanese equities](https://x.com/PythNetwork/status/2117293207344263578), [Q3 offshore volume](https://x.com/PythNetwork/status/2113345177293295870), [ICE earnings call](https://x.com/PythNetwork/status/2116138323915988998)
- Kalshi Research on X, [Introducing KPOW Midterms](https://x.com/KalshiResearch/status/2117636019604389956)
- PIRB on X, [ARR meme](https://x.com/thePIRB/status/2117675725931131174)
