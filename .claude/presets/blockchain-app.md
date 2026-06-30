# Blockchain / Web3 Preset

## Project type

Decentralised applications (dApps), smart contracts, and Web3 infrastructure. Common variants:

- **DeFi protocol** — AMMs, lending/borrowing, yield aggregators, stablecoins, options vaults.
- **NFT platform** — minting, marketplace, royalty splits, metadata storage.
- **DAO / governance** — on-chain voting, token-weighted proposals, timelock execution.
- **Layer-2 / rollup** — custom chains, bridging, sequencer infrastructure.
- **Web3 SaaS** — off-chain backend with on-chain settlement or attestation (e.g. credential issuance, supply-chain provenance).
- **Wallet / key management** — custodial or non-custodial wallet product, MPC signing, hardware wallet integration.
- **Cross-chain bridge** — asset transfer between chains with relayer/oracle network.

## Typical use cases

- Token launch with vesting schedules and cliff cliffs.
- Decentralised exchange (DEX) with liquidity pools and swap routing.
- On-chain lending protocol with collateral and liquidation logic.
- NFT collection with provenance, royalties, and secondary marketplace.
- DAO treasury management with multi-sig and on-chain proposals.
- Supply-chain traceability anchored to a public ledger.
- Subscription or micropayment protocol using ERC-20 or native tokens.
- Identity and credential verification (DIDs, Verifiable Credentials, SBTs).

## Required discovery questions

1. Which chain(s) are you targeting? (Ethereum mainnet, L2s — Arbitrum, Optimism, Base, zkSync — Solana, Cosmos, other.) Is cross-chain deployment required from day one?
2. What is the estimated TVL or transaction volume, and what are the gas/fee cost constraints for end users?
3. Will the contracts be upgradeable? (Proxy pattern — transparent, UUPS, beacon — or immutable with migration strategy.) Who controls the upgrade key?
4. What is the governance / admin key structure? (EOA, multi-sig, DAO timelock, Safe.) What is the minimum multi-sig threshold?
5. Is there a token? If so: native utility, governance, or revenue-sharing? Any vesting, lockup, or emission schedule?
6. What external oracles or off-chain data does the protocol depend on? (Chainlink price feeds, TWAP, custom oracle, API3.)
7. What is the legal and regulatory posture? (Is KYC/AML required? Geographic restrictions? Are the tokens securities in any jurisdiction the team operates in?)
8. What is the planned audit budget and timeline? (Professional audit is non-negotiable before mainnet launch with real value.)
9. What is the incident response plan if a vulnerability is found post-launch? (Pause mechanism, emergency withdrawal, bug bounty programme.)
10. What off-chain components are needed? (Indexer, subgraph, relayer, backend API, IPFS/Arweave storage, frontend.)

## Recommended agents

**Core**
- `.claude/agents/core/orchestrator.md` — flow control and gate enforcement.
- `.claude/agents/core/solution-architect.md` — on-chain/off-chain boundary design, upgrade strategy.
- `.claude/agents/core/requirements-engineer.md` — formal invariants and economic security properties.

**Engineering**
- `.claude/agents/domain/blockchain-domain-expert.md` — Solidity/Rust contract logic, gas optimisation, invariant documentation.
- `.claude/agents/engineering/backend-engineer.md` — indexers, relayers, off-chain services.
- `.claude/agents/engineering/frontend-engineer.md` — wallet connection, transaction UX, on-chain state display.

**Quality**
- `.claude/agents/quality/security-auditor.md` — reentrancy, integer overflow, access control, oracle manipulation, MEV exposure.
- `.claude/agents/quality/qa-engineer.md` — fuzz testing, fork tests, formal verification planning.
- `.claude/agents/quality/production-readiness-auditor.md` — monitoring, incident response, guardian/pause mechanism.

**Domain**
- `.claude/agents/domain/blockchain-domain-expert.md` — protocol economics, tokenomics, governance design, audit readiness.

## Recommended skills

- `.claude/skills/blockchain/SKILL.md` — smart contract patterns, upgrade proxies, gas optimisation, audit preparation.
- `.claude/skills/security/SKILL.md` — threat model for on-chain contracts (attack surface differs from web apps).
- `.claude/skills/backend/SKILL.md` — off-chain indexer, relayer, and API services.
- `.claude/skills/testing/SKILL.md` — Foundry fuzz/invariant tests, fork simulation, Hardhat integration tests.
- `.claude/skills/devops/SKILL.md` — deployment scripts, environment separation (testnet → mainnet), key management.
- `.claude/skills/production-readiness/SKILL.md` — on-chain monitoring (Tenderly, Forta), alerting on anomalous activity.
- `.claude/skills/data-platform/SKILL.md` — subgraph / indexer design for on-chain event queries.

## Recommended stack options

| Stack | Rationale |
|-------|-----------|
| **Solidity + Foundry + OpenZeppelin + The Graph** | Industry-standard: Foundry for fast fuzz/fork tests; OpenZeppelin audited base contracts; The Graph for decentralised indexing. See `.claude/stack-matrix/backend.md`. |
| **Solidity + Hardhat + Ethers.js + Tenderly** | Mature ecosystem, JavaScript-native tests; Tenderly for transaction simulation, gas profiling, and real-time alerting. |
| **Rust (Anchor) + Solana + Metaplex** | High-throughput, low-fee; Anchor provides safe account constraints; Metaplex for NFT standards. Choose when Solana's parallel execution model matches the use case. |
| **Rust (CosmWasm) + Cosmos SDK** | App-chain sovereignty; IBC for cross-chain composability; strong formal verification tooling (Coq/k-framework). |

## Required checklists

- `.claude/checklists/security.md` — extend with: reentrancy guards on all external calls, integer arithmetic safe (unchecked blocks justified), access control on every privileged function, no tx.origin for auth, oracle manipulation scenarios modelled, MEV exposure documented.
- `.claude/checklists/qa.md` — extend with: Foundry invariant/fuzz tests pass, fork-test against mainnet state, all revert paths tested, deployment script dry-run on testnet.
- `.claude/checklists/production.md` — extend with: external audit report reviewed and all critical/high findings resolved, multi-sig deployed and signers confirmed, pause/guardian mechanism tested, bug bounty live before mainnet.
- `.claude/checklists/performance.md` — extend with: gas cost per function benchmarked, no unbounded loops, storage layout optimised (slot packing), calldata minimised.

## MVP scope pattern

**In the first cut:**
- Single-chain deployment (one testnet, then one mainnet).
- Core protocol logic only: the minimum set of contracts to demonstrate the primary value proposition.
- Immutable contracts or a simple Ownable upgrade authority (document explicitly; upgrade governance can be added later).
- A minimal off-chain indexer (The Graph subgraph or a simple event listener writing to Postgres).
- A read/write frontend that connects to MetaMask/WalletConnect, reads on-chain state, and submits transactions.
- Full test suite: unit tests, fuzz tests, and one fork test against a realistic mainnet state snapshot.
- One professional security audit before any real-value mainnet deployment.

**Deferred to later:**
- Multi-chain deployment and bridging.
- DAO governance / on-chain voting (start with a multi-sig).
- Advanced tokenomics (emissions, staking rewards, fee distribution).
- Decentralised frontend (IPFS hosting, ENS).
- Formal verification.
- Protocol insurance / coverage integration.
- Cross-protocol composability (integrations with other DeFi primitives).

## Production risks

| Risk | Priority | Notes |
|------|----------|-------|
| Reentrancy attack draining funds | P0 | Follow checks-effects-interactions; use ReentrancyGuard on all state-changing external calls; audit required. |
| Private key / deployer EOA compromise | P0 | Transfer ownership to multi-sig immediately after deploy; no single EOA controlling production contracts. |
| No pause/emergency mechanism | P0 | Implement a guardian role that can pause critical functions; test the pause path before launch. |
| Oracle price manipulation (flash loan attack) | P0 | Use TWAP not spot price; enforce minimum liquidity; consult oracle documentation on staleness and deviation. |
| Upgrade proxy admin key held by a single EOA | P0 | Admin key must be a multi-sig with ≥ 3-of-5 threshold; timelock for non-emergency upgrades. |
| Unbounded loops hitting block gas limit | P1 | Use pagination or off-chain computation for iteration; test with realistic data sizes. |
| Integer overflow / underflow | P1 | Use Solidity ≥ 0.8 checked arithmetic; document any unchecked blocks with explicit justification. |
| Proxy storage collision | P1 | Use EIP-1967 storage slots; never use unstructured storage unless you know exactly what you're doing; Foundry storage layout tests. |
| Front-running / MEV extraction hurts users | P1 | Add commit-reveal or slippage guards where relevant; document MEV exposure in the threat model. |
| Regulatory action / token classified as security | P1 | Legal opinion obtained before public launch in relevant jurisdictions; geo-restrictions enforced on frontend. |
| Missing audit before mainnet with real funds | P0 | Non-negotiable gate: no real-value mainnet without at least one external audit and all critical/high findings resolved. |
| Subgraph/indexer downtime causing frontend outage | P2 | Fallback to direct RPC reads for critical state; alert on subgraph sync lag. |

## Launch requirements

- All smart contracts audited by at least one reputable external firm; all critical and high severity findings resolved or formally accepted with written justification.
- Multi-sig deployed and all signers have tested signing and executing a transaction.
- Pause/guardian mechanism tested on testnet.
- Deployment scripts idempotent and dry-run verified on a fork of mainnet.
- On-chain monitoring active (Tenderly alerts, Forta bots, or equivalent) for: large transfers, admin actions, failed transactions above threshold.
- Bug bounty programme live on Immunefi or equivalent before mainnet launch.
- Frontend points to correct mainnet contract addresses; ABI verified on Etherscan/block explorer.
- Legal review completed: token classification opinion, terms of service, geo-restrictions implemented.
- Incident response runbook documented: how to trigger pause, how to communicate a vulnerability, who holds the guardian key.
- Treasury / protocol fee address is a multi-sig, not an EOA.
