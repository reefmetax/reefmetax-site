---
title: US Stocks Go 23/5 on December 6: What Changes Overnight and Where Pyth Fits
date: 2026-11-25
description: A plain-English guide to the new 23 hours a day, five days a week US stock schedule starting Sunday, December 6, 2026, what stays different at night, and how Pyth already prices stocks across every session.
faq:
  - q: When does 23/5 trading for US stocks start?
    a: On Sunday, December 6, 2026, five US exchanges (24X, Nasdaq, NYSE Arca, Cboe EDGX and MEMX) start trading US stocks 23 hours a day, five days a week. The consolidated tape runs from 9 p.m. ET Sunday to 8 p.m. ET Friday, with a one-hour pause from 8 to 9 p.m. Monday through Thursday.
  - q: What are the rules for the overnight stock session?
    a: The overnight session runs from 9 p.m. to 4 a.m. ET. All five exchanges require limit orders only, price bands sit 20% below and above reference prices and stay fixed all session, overnight markets may be unlinked, and the Order Protection Rule applies only in regular hours. Nobody is required to trade overnight.
  - q: How does Pyth price US stocks outside regular market hours?
    a: Pyth says it has published 24/5 US equity prices since September 2025, covering overnight, pre-market, regular and after-hours trading from Sunday 8 p.m. to Friday 8 p.m. ET under a single feed ID. Overnight prices come from Blue Ocean ATS and other venues that trade during those hours.
---
For as long as most of us have been watching markets, US stocks have basically gone to sleep at night. That changes on Sunday, December 6. Five US exchanges will start trading stocks 23 hours a day, five days a week, and Pyth Network spent this week explaining what that means. Here is the plain-English version, with every number pulled from Pyth's own posts and blog.

## What is actually changing

The key thing to understand: overnight stock trading is not new. Alternative trading systems, or ATSs, already run overnight sessions. What is new is that the trading moves onto public exchanges and onto the official consolidated tape, which is the feed that reports every US stock trade.

According to [Pyth's thread](https://x.com/PythNetwork/status/2125244000924041642), the new trading day looks like this (all times ET):

- **Overnight:** 9 p.m. to 4 a.m. (new on exchanges)
- **Pre-market:** 4 a.m. to 9:30 a.m.
- **Regular:** 9:30 a.m. to 4 p.m.
- **After-hours:** 4 p.m. to 8 p.m.

The tape runs from 9 p.m. Sunday to 8 p.m. Friday, with a one-hour pause from 8 to 9 p.m. Monday through Thursday. That one-hour gap is why it is called 23/5 and not 24/5.

## Why everyone starts on the same day

Pyth's explainer notes that the SEC approved overnight sessions on five exchanges one at a time: 24X in November 2024, Nasdaq in April 2026, NYSE Arca and Cboe EDGX in May 2026, and MEMX in September 2026. Those approvals were conditional on the consolidated tape being ready, so all five launch together. The US equities clearinghouse, NSCC, has already been running on 24x5 hours since June 29.

## Overnight trading is already growing

This is not a market starting from zero. Per [Pyth's thread](https://x.com/PythNetwork/status/2125244010474434786), citing SEC staff data, the overnight session was 0.9% of NMS share volume and 0.8% of dollar volume in August, with share volume up 359% year over year. Foreign accounts made up about 37% of overnight share volume in the second quarter.

It keeps building, too. [Pyth also shared](https://x.com/PythNetwork/status/2125244014702240128) that three overnight ATSs traded $41.8 billion in the week of November 9, after $41.2 billion the week before. That was the first time Sapinover's data series showed two $40 billion weeks in a row. SOXL, NVDA, SOXS, MU and QQQ led the activity.

## What stays different at night

Overnight trading will not feel exactly like the daytime session. [Pyth listed the guardrails](https://x.com/PythNetwork/status/2125244016715346233):

- **Limit orders only.** You have to name your price. No market orders overnight.
- **Static 20% price bands.** These stay fixed for the whole session instead of moving with the price.
- **Markets may be unlinked.** Brokers must warn customers about this, and the Order Protection Rule only applies in regular hours.
- **Concentrated liquidity.** In August, the top ten stocks were 43.4% of overnight share volume, versus 10.3% in regular hours.

In simple terms: fewer stocks trade actively at night, and the rules are built to keep things orderly while liquidity is thinner. Pyth's blog also points out that nobody is required to trade overnight, and most firms are expected to start slowly.

## Where Pyth fits in

Here is why this matters for the Pyth community. Any app that reads a stock price, like a broker, a trading app, a risk desk, a perp venue, a lending protocol or a prediction market, needs that price whenever its users are active, not only when the opening bell rings.

[Pyth says](https://x.com/PythNetwork/status/2125244018422329499) it publishes 24/5 US equity prices across overnight, pre-market, regular and after-hours sessions under a single feed ID. Its explainer adds that this has been live since September 2025, and that overnight prices come from Blue Ocean ATS and other venues that actively trade during those hours. Its takeaway: December 6 adds exchange liquidity to a session that already trades. It does not create the session.

The demand outside regular hours is already showing up onchain. In its research on the 25 most traded US single-stock perps, [Pyth reported](https://x.com/PythNetwork/status/2122707410498298051) that half of that volume now trades while NYSE and Nasdaq are closed. In October, those 25 names traded $270.7 billion, with 49.8% of it off-hours. And in its October report, [Pyth said](https://x.com/PythNetwork/status/2122359012520010002) it priced 95.9% of the $384 billion in equity perps volume that month.

A couple of other November launches fit the same always-on theme:

- **Anthropic ($ANT).** On November 19, [Pyth announced](https://x.com/PythNetwork/status/2123464696795660438) its Anthropic 24/5 feed and 24/7 index were live for exchanges, prediction markets and agents.
- **LayerZero ATLAS.** [Pyth shared](https://x.com/PythNetwork/status/2123083024128430316) that Pyth market data will be available from day one on ATLAS, a headless exchange on LayerZero's Zero chain launching November 30.

If you are new to oracles and want the background on why price data matters this much, my [Pyth explainer](https://reefmetax.com/articles/pyth-network-price-oracles-explained/) covers the basics.

## The bottom line

December 6 is a real milestone for US markets. Stocks will trade on exchanges almost around the clock on weekdays, with tighter rules at night. For builders and traders, it puts a spotlight on something Pyth has been focused on for a while: having a usable price whenever the market is moving.

Not financial advice. Do your own research.

Thanks for reading, and if this helped you understand the switch, pass it along to someone who still thinks the stock market clocks out at 4 p.m.

## Sources

- Pyth Network on X, [23/5 trading thread](https://x.com/PythNetwork/status/2125244000924041642), [new trading day schedule](https://x.com/PythNetwork/status/2125244005260902430), [exchange approvals](https://x.com/PythNetwork/status/2125244006812598329), [overnight growth, SEC data](https://x.com/PythNetwork/status/2125244010474434786), [overnight ATS volume](https://x.com/PythNetwork/status/2125244014702240128), [overnight guardrails](https://x.com/PythNetwork/status/2125244016715346233), [24/5 feed](https://x.com/PythNetwork/status/2125244018422329499)
- Pyth Network blog, [23/5 trading: what changes for US stocks on December 6](https://www.pyth.network/blog/23-5-trading-what-changes-for-us-stocks-on-december-6)
- Pyth Network on X, [US stock perps research](https://x.com/PythNetwork/status/2122707410498298051), [October equity perps volume](https://x.com/PythNetwork/status/2122359012520010002)
- Pyth Network on X, [Anthropic ($ANT) feed live](https://x.com/PythNetwork/status/2123464696795660438), [LayerZero ATLAS](https://x.com/PythNetwork/status/2123083024128430316)
