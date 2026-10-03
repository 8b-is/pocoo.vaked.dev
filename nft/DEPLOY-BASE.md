# Deploying VAKED to Base (Coinbase L2) — local step-by-step

"Deploying to Coinbase" means deploying the VAKED contract to **Base**,
Coinbase's Ethereum L2 (chain id **8453**). Once it is deployed, the token
appears on Basescan, can be imported into Coinbase Wallet, and works with any
wallet connected to Base. (Being listed on the Coinbase *exchange* is a
separate internal process — no self-serve deploy triggers it.)

This is the Base twin of `DEPLOY.md` (which targets Polygon). Same contract,
same committed bytecode, same zero-dependency tooling — the only difference is
the chain selector. Everything below runs locally; the browser site never
loads any of it.

Endpoints (verified live from this machine):

| Network | CHAIN_ID | RPC | Explorer |
|---|---|---|---|
| Base mainnet | `8453` | `https://mainnet.base.org` | https://basescan.org |
| Base Sepolia (test) | `84532` | `https://sepolia.base.org` | https://sepolia.basescan.org |

> A Base deployment is a **separate contract instance** from the Polygon one:
> two chains, two supplies, same rules. The fair-launch invariants (no
> premine, no team allocation, 21,000,000 cap, PoW-only mint) hold per
> deployment. The deployer key also starts at nonce 0 on the new chain.

---

## 0. Rehearse on Base Sepolia first (free)

Deploy once to the testnet before spending anything. Fund the deployer
address with Base Sepolia ETH (any Base Sepolia faucet), then run steps 1–4
with `CHAIN_ID=84532`.

## 1. Compile (only if VAKED.sol changed)

`nft/VAKED.bin` is committed, so the deploy step below works as-is. To
recompile from source, follow `DEPLOY.md` step 1 (scratch dir, `solc 0.8.28`
+ `@openzeppelin/contracts 5.0.2`, `--optimize --optimize-runs 200`) and
re-copy the output to `nft/VAKED.bin`.

## 2. Dry run — sign, print, send nothing

```bash
# Base mainnet dry run (no funds move)
CHAIN_ID=8453 PRIVATE_KEY=0x... node nft/deploy.js --vaked

# Base Sepolia dry run (rehearsal)
CHAIN_ID=84532 PRIVATE_KEY=0x... node nft/deploy.js --vaked
```

Expect: `=== VAKED (Mineable ERC-20) deployment (Base mainnet, chain id 8453) ===`,
the predicted contract address, the gas estimate, and the signed raw tx —
with `rpc: https://mainnet.base.org`. Nothing is broadcast.

## 3. Fund the deployer on Base

Send ETH to the deployer address on Base (an exchange withdrawal that
supports Base, or any bridge that supports it). A VAKED deploy is ~1.9M gas;
on Base that is cents, not dollars.

## 4. Broadcast

```bash
CHAIN_ID=8453 PRIVATE_KEY=0x... node nft/deploy.js --vaked --broadcast
```

The runner prints the tx hash and the explorer links
(`https://basescan.org/tx/…` and `https://basescan.org/address/…`).

## 5. Verify the source on Base

- **Sourcify**: choose Base (chain id 8453), paste the deployed address —
  OpenZeppelin 5.0.2 metadata resolves automatically.
- **Basescan**: `Verify and Publish` — Solidity (single file), compiler
  **v0.8.28**, license **MIT**, optimization **Yes (runs 200)**, EVM
  **cancun**. Flatten with `sol-merger` as in `DEPLOY.md` step 4.

## 6. Prove mining works before renouncing

Run a couple of live mints against the Base contract with the CLI miner:

```bash
cd miner
node mine.js --rpc https://mainnet.base.org --contract 0x<BASE_VAKED> --key 0x...
```

(50 VAKED per mint at launch difficulty — about a minute of CPU each.)

## 7. Renounce ownership

Only **after** mints are proven. `renounceOwnership()` selector is
`0x715018a6`:

```bash
node -e "
import('./art/chain.js').then(async ({ chain }) => {
  const priv = process.env.PRIVATE_KEY;
  const vakedAddr = '0x<BASE_VAKED>';
  const rpcUrl = 'https://mainnet.base.org';
  const from = chain.privateToAddress(priv);
  const call = async (method, params) => (await (await fetch(rpcUrl, {
    method: 'POST', headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ jsonrpc: '2.0', id: 1, method, params }),
  })).json()).result;
  const nonce = await call('eth_getTransactionCount', [from, 'pending']);
  const gasPrice = await call('eth_gasPrice', []);
  const tx = chain.signLegacyTx({
    nonce, gasPrice, gasLimit: '0x186a0', to: vakedAddr, value: '0x0',
    data: '0x715018a6', priv, chainId: 8453,
  });
  console.log(await call('eth_sendRawTransaction', [tx]));
});"
```

Then confirm `owner()` returns `0x0000000000000000000000000000000000000000`.

## 8. Point the surfaces at Base (optional)

The in-browser miner ships Polygon-wired. For a Base build of
`demos/miner.html`, flip four constants:

| constant | Polygon (now) | Base |
|---|---|---|
| `VAKED_CONTRACT` | `0x2Ae7DA71…` | the new Base address |
| `POLYGON_CHAIN_ID` | `'0x89'` | `'0x2105'` |
| `PUBLIC_RPC` | `https://polygon.drpc.org` | `https://mainnet.base.org` |
| `EXPLORER` | `https://polygonscan.com` | `https://basescan.org` |

(plus the `chainName` in `ensurePolygon()` → `'Base'`). The whitepaper
contract link and the Sourcify badge in `SECURITY.md` should follow.

## 9. See it with your address (wallets)

- **Coinbase Wallet**: switch the network to Base, then paste the token
  address under "Add token" — balances, transfers, and the token page show
  once you hold any (mine some first).
- **MetaMask**: Add network → Base (`8453`,
  `https://mainnet.base.org`, symbol `ETH`) → Import tokens → paste address.
- **Basescan**: `https://basescan.org/token/0x<BASE_VAKED>` — holders and
  transfers are public there.

## Caveats, honest

- "Deploy to Coinbase" = **Base L2**, not the Coinbase exchange listing.
- Gas is paid in ETH on Base (not POL as on Polygon).
- Do not renounce in the same transaction as deployment; there is no rescue
  path once ownership is gone.
- Verify before renouncing; renounce before announcing.

*VAKED on Base · nft/DEPLOY-BASE.md · the constellation · 0 + 1 · vaked.dev*
