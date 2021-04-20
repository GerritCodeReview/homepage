---
title: "Consistency on Demand"
permalink: design-docs/consistency-on-demand-use-cases.html
hide_sidebar: true
hide_navtoggle: true
toc: false
---

# <a id="setup"> Multi-Master setup vs Multi-primary setup
This design is aiming to solve a problem that is common in multi-master setups:
those setups have replication lags of up to a few hours, which can cause to
inconsistent state which can lead to corrupt releases. Such problems are less
common or non existent for other setups.

# <a id="use-cases"> Use-cases

1. Support automation users such that they can ensure that replication lag does
not cause an inconsistent state that could lead to corrupt releases.
2. Come up with a reliable way to handle common replication lag symptoms of
Gerrit.

# <a id="non-goals"> Non Goals

1. A replication SLO for Gerrit data.
2. A mechanism for clients to fix or hide existing replication lag.

## <a id="acceptance-criteria"> Acceptance Criteria

Clear documentation on how to achieve the use-cases is available for the users.

## <a id="background"> Background

There are multiple automation systems that manage flow of changes across
branches. Some of these systems issue sequences of commands, where the output of
one command depends on the previous one. Load balancing combined with
replication lag can create many failures.

Consider the following sequence:

1. Create branch B on repo R1 & R2
2. Cherry-pick existing change C1 to B on R1 (fails if B has not yet replicated
to R1).
3. Set topic T to C1’ and C2’ (Fails if C1’ or C2’ haven’t replicated (404)).
4. Vote +2 on C1’ and C2’ (Fails if C1’ or C2’ creation hasn’t replicated (404).
5. Submit C1’, submitting C2’ through topic T (Fails if creation hasn’t
replicated (404), C1 topic set hasn’t replicated (409), C1’ or C2’ vote hasn’t
replicated (409), may succeed without submitting C2 if “set topic” hasn’t
replicated to the currently used change index.

Automation systems can try to paper this over with wait and retry, but it’s hard
to ensure errors are really due to replication. For example 404 can also be due
to a permission configuration error, and 409 can also be due to some other party
removing a +2 vote.

Due to topic submit, Gerrit API calls can affect multiple repositories.
Bots can manage submission across the entire host (and also multiple hosts).
In other words, a submit operation can touch O(1000) repositories.

## <a id="previous-work"> Previous Work

Internally within Google, we have contemplated Consistency-On-Demand.
After many variations, we concluded that there is more value in a public version.
