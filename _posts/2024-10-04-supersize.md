---
layout: post
title: "Supersize: a next-gen real-time PvP game on Solana"
categories: [Announcement]
image: assets/images/supersize.png
tags: [featured]
---

Supersize is a next-generation gaming platform (available at [Supersize.gg](http://supersize.gg:3000/)) pushing the boundaries of fully onchain gaming on Solana with a simple, powerful vision: financial markets meet .io style game. Supersize is developing a real-time multiplayer experience where users compete for resources in a customizable PvP setting. The game is built entirely onchain (state and logic) and blends financial incentives, UGC and the simplicity of agar.io to create truly innovative game dynamics. The challenge? Creating an entirely onchain experience that could run with real-time latency and impeccable UX without composability fragmentation.

## Challenge: real-time latency without fragmenting Solana liquidity and state

Supersize required a framework that could handle:

- Real-time latency for an ever growing number of concurrent players
- Composability with Solana liquidity and smart contracts
- Seamless user experience despite all interactions being onchain transactions

Supersize knew that traditional L2 architecture would struggle to meet these needs due to  well-known issues of liquidity fragmentation and the inability to offer consistent real time latency to a globally distributed audience.

## Solution: Leveraging BOLT ECS + Ephemeral Rollups

Supersize turned to MagicBlock and leveraged [BOLT](https://docs.magicblock.gg/Build/Bolt/introduction) ECS (Entity-Component-System) and Ephemeral Rollups to bring its vision to life. BOLT is an ECS framework built on top of Anchor that enabled Supersize to efficiently structure game logic on Solana, leaving space for the introduction of new systems to extend and modify the game. MagicBlock’s Ephemeral Rollups provided the low-latency performance needed for real-time interactions, while keeping liquidity and all the smart contract on Solana. Additionally, by means of co-location, Ephemeral Rollups further reduce the networking latency (~30ms end-to-end) offering performances on par with traditional multiplayer game servers.

## Results: A Seamless, Fully On-Chain Gaming Experience

Using BOLT ECS and Ephemeral Rollups, Supersize was able to deliver a fully onchain game that matched all their criteria with:
    
- High scalability and real-time latency: Supersize can elastically scale to support more players who interact with each others in real-time
- Solana liquidity and composability: the game is built on Solana and can leverage SOL, BONK, LST or any other token without bridging.
- Modularity: Supersize can compose with any smart contract and rapidly introduce new game mechanics or upgrades without having to redeploy the entire game architecture.
- UX: Thanks to Ephemeral Rollups the gameplay is fast and offers players a seamless, gasless and uninterrupted experience.

> Coming from EVM, I was ready to make big compromises to build Supersize fully onchain. But, by leveraging Magicblock’s stack to build directly on Solana, not only does Supersize not compromise on UX, but it also synergizes elegantly with the broader Solana ecosystem." 

Lewis Arnsten, Supersize founder

> I am extremely excited to see Supersize advancing the narrative of what is possible with FOCG. I am extremely bullish on Solana-first experiences that tap into the liquidity and existing primitives of the chain without sacrificing a seamless user experience"

Andrea Fortugno, MagicBlock cofounder & CEO 

## About MagicBlock
MagicBlock is a high-performance engine for fully onchain games and applications. With Ephemeral Rollups, MagicBlock empowers developers to build real-time and composable decentralized applications.
Learn more at [MagicBlock](https://docs.magicblock.gg/).

