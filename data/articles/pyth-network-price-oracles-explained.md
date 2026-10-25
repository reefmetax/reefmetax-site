---
title: Pyth Network Explained: What a Price Oracle Is and How Pyth Works
date: 2026-10-25
description: A newcomer's guide to price oracles, the push vs pull idea, and what changed in Pyth's setup after the August 26, 2026 upgrade.
---
Pyth Network is one of the names I see most in the community, and it is easy to nod along without knowing what it does. Here is a simple walkthrough for newcomers.

## Why blockchains need a price oracle

A blockchain can't look up the price of bitcoin or a stock on its own. Apps that need a price, like lending or trading apps, have to get it from somewhere. A price oracle is the service that brings those prices on-chain.

## Push vs pull

Pyth's launch post describes two styles. In a **push** oracle, the oracle operator keeps sending price updates to each blockchain and pays the transaction fees for every one, whether or not anyone is using the price.

A **pull** oracle only updates the on-chain price when someone needs it. With Pyth, prices are signed off-chain, and anyone can fetch the latest signed update and submit it to the on-chain contract. The contract checks that the update is authentic and stores it. An app can then update the price and use it in a single transaction.

That 2022 post argued the pull model scales better, because the oracle itself does not pay a fee for every update on every chain. It was written for the original Pythnet design, so see the section below for what has changed since.

## Where the prices come from

Pyth gets its data from publishers, the entities that submit market data. For Pyth Pro, the docs say the routers combine the publisher inputs into a median price, which resists outliers from any one publisher. They also compute a confidence interval, using the interquartile range, to show how spread out the inputs are.

That confidence number is worth knowing about. It tells an app how tight or loose the price is at that moment.

## What changed on August 26, 2026

If you read older Pyth explainers, some of the architecture has changed. According to the [Pyth docs](https://docs.pyth.network/pro/how-lazer-works), Pyth Core used to run on Pythnet, a dedicated blockchain that gathered publisher prices. That blockchain has now shut down.

Since August 26, 2026, Pyth Core gets its prices from Pyth Pro. The docs list these changes:

- Data sourcing moved from Pythnet to five independent routers.
- Signing moved from the Wormhole guardians to those five routers.
- The quorum went from 13 of 19 signatures to 3 of 5.
- Hermes, the service apps use to fetch updates, kept the same API, and the contracts kept their addresses and interface.

So for developers, the upgrade was designed to need no code changes. For readers, it means older "how Pyth works" posts may describe a setup that no longer exists.

## Two kinds of contracts

The docs say Pyth Pro contracts verify a signed price inside each transaction and store nothing. Pyth Core contracts verify and store a price on-chain so other contracts can read it. The docs list perps and RFQ as typical Pro uses, and lending markets, CDPs and vaults as typical Core uses.

One more detail: the docs describe Pyth Pro as a permissioned service, and say Douro Labs operates its relayer service. That is a fair thing to know when you think about how the system is run.

## The takeaway

An oracle is plumbing. When it works, you never notice it. When you hear "Pyth," think of it as a service that gets market prices to apps that need them, and read the current docs because the setup has changed recently.

This is education only, not a recommendation about any token. Not financial advice. Do your own research.

## Sources

- Pyth Developer Hub, [How Pyth Pro Works](https://docs.pyth.network/pro/how-lazer-works)
- Pyth Developer Hub, [Use Prices on Blockchains](https://docs.pyth.network/price-feeds/core/pull-updates) (Pro vs Core contracts)
- Pyth Network blog, [Pull, Don't Push: A New Price Oracle Architecture](https://www.pyth.network/blog/pyth-a-new-model-to-the-price-oracle) (Dec 13, 2022)
