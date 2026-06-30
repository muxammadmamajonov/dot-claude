---
name: blockchain
description: >
  Activate when the project involves blockchain, smart contracts, DeFi, NFTs, DAOs, wallets,
  token standards, or on-chain/off-chain hybrid systems. Triggers on: keywords like "smart contract",
  "Solidity", "Rust (Anchor/CosmWasm)", "EVM", "Ethereum", "Solana", "Cosmos", "wallet",
  "Web3", "DeFi", "NFT", "DAO", "token", "gas", "ABI", "IPFS", "multisig", "on-chain",
  "off-chain", "oracle", "bridge", "L2", "rollup", "Hardhat", "Foundry", "Anchor".
---

# Blockchain Application Development

## When to use
- Writing, testing, or auditing smart contracts (EVM / Solana / Cosmos)
- Building a wallet integration (EOA, multisig, smart-account / ERC-4337)
- Designing the on-chain vs off-chain data split for a dApp
- Implementing token standards (ERC-20, ERC-721, ERC-1155, SPL)
- Building DeFi protocols (AMM, lending, staking, yield)
- Integrating oracles, bridges, or cross-chain messaging
- Setting up a smart-contract deployment and upgrade pipeline

## Workflow

1. **Decide what must be on-chain vs off-chain** — the most important architectural decision:
   | On-chain (contract state) | Off-chain (backend / IPFS) |
   |--------------------------|---------------------------|
   | Asset ownership, balances | Media files, metadata JSON |
   | Governance votes | User profiles, social graph |
   | Settlement / finality | Order books, price feeds (use oracle) |
   | Access control rules | Application business logic |
   | Escrow / locked funds | Notifications, emails |
   Every byte of on-chain storage costs gas indefinitely; keep state minimal.

2. **Choose the chain and toolchain**:
   | Chain | Language | Toolchain |
   |-------|----------|-----------|
   | Ethereum / EVM-compatible | Solidity | Hardhat or Foundry |
   | Solana | Rust (Anchor) | Anchor CLI + Bankrun |
   | Cosmos / CosmWasm | Rust | CosmWasm + cw-multi-test |
   | StarkNet | Cairo | Scarb + Starknet Foundry |
   Prefer Foundry for EVM: faster compilation, fuzz testing built-in, Solidity test files.

3. **Smart contract design principles**:
   - Single responsibility: one contract = one concern. Separate logic, storage, and access control.
   - Use OpenZeppelin (EVM) or battle-tested crates (Solana/Cosmos) for standard patterns — never re-implement ERC-20, ownership, or reentrancy guards from scratch.
   - Emit events for every state change; off-chain indexers (The Graph, custom) depend on them.
   - Define explicit storage layout; document every storage slot if upgradeability is needed.
   - Mark all entry points with correct visibility (`external` vs `public`); make internal helpers `internal` or `private`.

4. **Upgradeability** — choose a pattern before deployment:
   | Pattern | Mechanism | Risk |
   |---------|-----------|------|
   | Immutable | No proxy | Safest; no upgrades possible |
   | Transparent proxy (OZ) | `delegatecall` to implementation | Storage collision risk |
   | UUPS | Upgrade logic in implementation | Implementation must include upgrade fn |
   | Beacon proxy | All proxies point to beacon | Good for many instances |
   If upgradeability is chosen: document upgrade governance (multisig, timelock, DAO vote), never allow a single EOA to upgrade unilaterally.

5. **Security — check before every deployment**:
   - **Reentrancy**: follow Checks-Effects-Interactions (CEI) pattern; use `ReentrancyGuard` on all external-call functions.
   - **Integer overflow/underflow**: use Solidity ≥0.8 (built-in checks) or SafeMath; never use unchecked blocks around arithmetic that operates on user-supplied values.
   - **Access control**: every privileged function must have `onlyOwner`, `onlyRole`, or equivalent guard.
   - **Oracle manipulation**: never use spot price from a DEX as an oracle; use time-weighted average price (TWAP) or Chainlink.
   - **Front-running**: use commit-reveal schemes or private mempools (Flashbots Protect) for sensitive operations.
   - **Signature replay**: include `chainId`, `nonce`, and contract address in every signed message (EIP-712).
   - **Denial of service**: avoid unbounded loops over user-supplied arrays; cap iteration count.
   - Run `slither` and `mythril` (EVM) or `cargo audit` (Rust) as part of CI before every deploy.

6. **Testing — non-negotiable layers**:
   - **Unit tests**: every function, every revert condition. Aim for 100% line coverage on contract code.
   - **Fuzz tests** (Foundry `forge fuzz` / Echidna): invariant testing — e.g., `totalSupply == sum of all balances` always holds.
   - **Integration tests**: full user flows on a local fork of mainnet (`anvil --fork-url`).
   - **Invariant / stateful fuzzing**: define protocol invariants and let the fuzzer find violations.
   - **Gas snapshot tests**: `forge snapshot`; fail CI if gas usage increases beyond threshold unexpectedly.
   - Never deploy to mainnet a contract that has not been tested on a public testnet (Sepolia, Goerli, devnet).

7. **Deployment pipeline**:
   a. Compile and run full test suite (fail on any test failure).
   b. Run static analysis (`slither --fail-high`).
   c. Deploy to local fork → verify ABI and events match expectations.
   d. Deploy to testnet → run integration tests against live testnet.
   e. Submit for external audit if TVL > $500 K or protocol handles user funds.
   f. Deploy to mainnet via a multisig (Gnosis Safe) with a timelock (≥48 h for parameter changes, ≥7 days for upgrades).
   g. Verify source code on Etherscan / Sourcify immediately after deployment.
   h. Document deployed addresses, commit hash, and constructor args in `deployments/<network>.json`.

8. **Wallet & frontend integration**:
   - Use `viem` (TypeScript) or `ethers.js v6`; avoid `web3.js` (deprecated).
   - Support both EOA wallets (MetaMask) and smart accounts (ERC-4337 via Biconomy, Alchemy AA).
   - Never store private keys in the browser or in any server-side code — use hardware wallets for admin ops.
   - Use `eth_call` for read-only simulation before submitting a transaction; show the user expected outcome and gas estimate.
   - Handle wallet errors explicitly: user rejection, insufficient gas, nonce mismatch, chain mismatch.
   - Sign messages with EIP-712 typed data; display human-readable fields in MetaMask — never raw bytes.

9. **Indexing & off-chain data**:
   - Index contract events with The Graph (subgraph) or a custom indexer (Ponder, Envio).
   - Store NFT metadata JSON on IPFS (pin via Pinata or NFT.Storage) or Arweave — never on a centralized server.
   - Use an oracle (Chainlink, Pyth, UMA) for any off-chain price or data feed the contract depends on.
   - Off-chain backend that writes to the contract must use a hot wallet with a minimal ETH balance; rotate keys regularly.

10. **Post-deployment operations**:
    - Monitor contract events in real time; alert on unexpected large transfers, pauses, or admin actions.
    - Publish a bug bounty (Immunefi) before or alongside mainnet launch.
    - Maintain an incident response runbook: who can pause the contract, how to drain funds to safety, communication plan.
    - Do NOT disable the pause mechanism or remove multisig signers without a governance vote and timelock.

## Standards

**Do:**
- Use `uint256` as the default integer type on EVM; avoid smaller types unless packing structs in storage.
- Emit events with indexed parameters for the fields most likely to be filtered (address, tokenId).
- Write NatSpec (`@notice`, `@param`, `@return`) on every public/external function.
- Pin Solidity compiler version exactly (`pragma solidity 0.8.24;`), not with a caret.
- Use `immutable` for values set once in the constructor and never changed; cheaper than `storage`.

**Do not:**
- Use `transfer()` or `send()` for ETH transfers — use `call{value: ...}("")` with a success check.
- Store sensitive off-chain data (email, KYC) on-chain or in calldata — it is public and permanent.
- Deploy contracts with `selfdestruct` unless there is an explicit business reason; it breaks proxy assumptions.
- Use `block.timestamp` for randomness or precise timing — it can be manipulated by validators within ~12 s.
- Use `tx.origin` for authorization — always use `msg.sender`.
- Run `rm -rf` on build artifacts or deployment records without backing up `deployments/` first.

## Common mistakes to avoid

- **Reentrancy on ETH withdrawals**: the classic DAO hack. Always update state before external calls (CEI). Use `ReentrancyGuard` as belt-and-suspenders.
- **Incorrect decimals assumption**: ERC-20 tokens have variable decimals (6 for USDC, 18 for most). Never hardcode `1e18`; read `token.decimals()`.
- **Unbounded array gas limit**: iterating over a user-grown array can exceed the block gas limit and permanently lock funds. Cap array sizes or use pagination patterns.
- **Missing event emission**: off-chain indexers miss state changes; UX breaks silently. Every state-mutating function must emit an event.
- **Front-running on reveal**: NFT mints with predictable randomness (block hash at mint time) are trivially exploited. Use Chainlink VRF or commit-reveal.
- **Forgetting `chainId` in signatures**: EIP-712 signatures without `chainId` are replayable on every EVM chain.
- **Deploying without source verification**: unverified contracts on Etherscan erode user trust and make audits harder.
- **Single admin key**: a single EOA with upgrade/pause power is a single point of failure and a high-value target. Always use a multisig.

## Output format

A typical EVM blockchain project (Foundry):

```
contracts/
  src/
    <Protocol>.sol
    interfaces/
      I<Protocol>.sol
    libraries/
      <Lib>.sol
  test/
    <Protocol>.t.sol       # Unit + fuzz tests
    invariants/
      <Protocol>.invariant.sol
  script/
    Deploy.s.sol
    Upgrade.s.sol
foundry.toml
deployments/
  mainnet.json             # address, tx hash, block, commit SHA
  sepolia.json
.env.example               # PRIVATE_KEY, RPC_URL placeholders — never commit .env
frontend/
  src/
    hooks/
      use<Protocol>.ts     # viem contract hooks
    abis/
      <Protocol>.json      # auto-generated from build artifacts
docs/
  architecture.md
  invariants.md
  incident-response.md
```

Reference architecture template: `.claude/templates/architecture.md`

## Related checklists
- `.claude/checklists/security.md` — reentrancy, access control, oracle safety, key management
- `.claude/checklists/launch.md` — audit submission, bug bounty, multisig setup, monitoring
- `.claude/checklists/performance.md` — gas optimization, storage packing, calldata minimization

## Related agents
- `.claude/agents/core/orchestrator.md` — overall project flow
- `.claude/agents/stack/backend/` — off-chain backend and indexer
- `.claude/agents/stack/web/` — dApp frontend (wallet connection, transaction UX)
- `.claude/agents/quality/` — testing strategy including fuzz and invariant tests
- `.claude/agents/engineering/` — feature implementation workflow
