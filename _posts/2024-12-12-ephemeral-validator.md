---
layout: post
title: "Open Sourcing the MagicBlock Ephemeral Validator"
categories: [Announcement]
image: assets/images/ephemeral_validator.jpg
tags: []
---

Today, we’re excited to announce the open sourcing of the [MagicBlock Ephemeral Validator](https://github.com/magicblock-labs/ephemeral-validator), a non-voting and lightweight SVM-runtime that brings real-time, elastic compute to Solana.

> TLDR: You can now write your entire Web2 server logic on Solana and execute arbitrary account updates on Just-In-Time (JIT) SVM instances, which run in parallel with Solana and replace centralized servers. Ephemeral Validators are designed to to use the SVM as a serverless, elastic compute environment for real-time use cases while keeping all smart contracts and state on Mainnet. Forget traditional servers. Just build on Solana and use MagicBlock to access real-time, elastic compute when you need it.


## Why We Built It

Short version: to bring **real-time**, **elastic compute ** to Solana.

Long version: We believe Solana will become the kernel for global finance. As applications mature and users demand real-time interactions, we see the potential to unlock new experiences that are natively composable with Solana state and run entirely on the SVM instead of a centralized server. While Solana provides exceptional throughput, use cases such as fully onchain games, decentralized social networks or trustless high-frequency financial products require even more scalability. With Ephemeral Rollups, developers can implement the entire logic of these apps on Solana and execute computations that would normally run on a server in a temporary, specialized SVM environment, gaining persistence, composability and verifiability for their applications.

## What Is the MagicBlock Ephemeral Validator?

The MagicBlock Ephemeral Validator is a non-voting, lightweight SVM-runtime that clones accounts and programs just-in-time (JIT) and settles state to a reference cluster. An Ephemeral validator can run as close as possible to the users to reduce networking latency and it can be run as a sidecar to the Mainnet Validator Clients, standalone or by users themselves given the [lowered hardware requirements](https://x.com/PiccoGabriele/status/1828464238442226032). Node operators can increase their profitability processing the transactions that would otherwise be implemented in a traditional server or would make little sense to run on Mainnet because they are uneconomical or for latency & runtime limitations.
There are 3 main components that the Ephemeral Validator interface with


## The Ephemeral execution environment

Ephemeral validators don’t participate in consensus nor can create new Accounts. Ephemeral Validator can only process state transitions on accounts delegated to the delegation program. Once an account has been delegated onchain, the Ephemeral Node clones the account and all the programs associated with it. The delegated state is natively locked on Solana and can be modified in the Ephemeral environment. Since the consensus is postponed to the commitment stage, the slot time can be arbitrarily short. Transactions are processed on a first-come-first-served (FCFS) basis and intra-slot updates allow users to subscribe to real-time data, minimising end-to-end latency. Ephemeral rollups open a new design space to scale elastically, where ordering and sequencing can be implemented as part of the smart contract logic. Additionally, even the same smart contract can dynamically execute some instruction in the ER (a fast-pace action), while some other on mainnet (e.g. depositing liquidity, doing a swap, minting, dispatching a reward, ..). Lastly, the ability to run dedicated  runtime leaves the design space open for further customization for application specific use-cases (e.g. a free ticking or randomness) that wouldn’t be possible or make sense to run on Mainnet.

![Ephemeral Validator Architecture](/assets/images/ephemeral_validator_diagram.png)

----------------------------------------------

## A supercharged development environment

The Ephemeral Validator has been optimized for execution and it can be used as a supercharged development environment. Check out [luzid.app](https://luzid.app/) if you want to develop at blazing speed!

## What’s Next

By open-sourcing the validator, we aim to foster collaboration among developers and accelerate adoption of real-time onchain applications.
This release is just the beginning. In the coming months, we plan to:

- Introduce further optimizations to enhance the validator’s performance.
- Provide more in-depth documentation and tutorials for developers.
- Launch community initiatives, including hackathons and grants 

----------------------------------------------

## Join the Conversation

We’re thrilled to share this milestone with you and can’t wait to see what the community builds with the MagicBlock Ephemeral Validator. Share your thoughts, feedback, and projects with us on [Twitter](https://x.com/magicblock), [Discord](https://discord.com/invite/MBkdC3gxcv), or [GitHub](https://github.com/magicblock-labs).

