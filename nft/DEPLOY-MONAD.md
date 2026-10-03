# Deploying VAKED to Monad — local step-by-step

Monad mainnet is live (chain id **143**, verified from this machine:
`eth_chainId` → `143`). Important, so nobody plans around a myth: **Monad
mainnet charges gas** — this machine measured **~102 gwei** live. A VAKED
mint (~100–150k gas) costs on the order of **0.01 MON**, and a deploy ~1.9M
gas. It is cheap, but not free, and you still need MON.

The genuinely free path is **Monad Testnet** (chain id **10143**): testnet
MON comes from the official faucet, so deploying, mining, and minting there
cost nothing.

| Network | CHAIN_ID | RPC | Explorer |
|---|---|---|---|
| Monad mainnet | `143` | `https://rpc.monad.xyz` (alt `https://rpc1.monad.xyz`) | https://monadscan.com |
| Monad Testnet (free) | `10143` | `https://testnet-rpc.monad.xyz` | https://testnet.monadexplorer.com |

Faucet (testnet MON): https://faucet.monad.xyz

> A Monad deployment is a separate contract instance from the Polygon one —
> two chains, two supplies, same rules (no premine, 21,000,000 cap,
> PoW-only mint). The deployer key starts at nonce 0 on Monad.

---

## 0. Rehearse on Monad Testnet first (free)

Get testnet MON from https://faucet.monad.xyz for the deployer address, then
run steps 1–4 with `CHAIN_ID=10143`. Everything below works identically on
mainnet — only the CHAIN_ID and the funding source change.

## 1. Compile (only if VAKED.sol changed)

`nft/VAKED.bin` is committed, so step 2 works as-is. To recompile from
source, follow `DEPLOY.md` step 1 (scratch dir, `solc 0.8.28` +
`@openzeppelin/contracts 5.0.2`, `--optimize --optimize-runs 200`) and copy
the output to `nft/VAKED.bin`.

## 2. Dry run — sign, print, send nothing

```bash
# Monad Testnet (free rehearsal)
CHAIN_ID=10143 PRIVATE_KEY=0x... node nft/deploy.js --vaked

# Monad mainnet
CHAIN_ID=143 PRIVATE_KEY=0x... node nft/deploy.js --vaked
```

Expect `=== VAKED (Mineable ERC-20) deployment (Monad Testnet, chain id 10143) ===`
(or `Monad mainnet, chain id 143`), the predicted contract address, and
`rpc: https://testnet-rpc.monad.xyz` / `https://rpc.monad.xyz`. Nothing is
broadcast.

## 3. Fund the deployer

- Testnet: faucet MON (free).
- Mainnet: send MON to the deployer address on Monad.

## 4. Broadcast

```bash
CHAIN_ID=10143 PRIVATE_KEY=0x... node nft/deploy.js --vaked --broadcast   # testnet
CHAIN_ID=143   PRIVATE_KEY=0x... node nft/deploy.js --vaked --broadcast   # mainnet
```

The runner prints the tx hash and explorer links
(`https://testnet.monadexplorer.com/…` or `https://monadscan.com/…`).

## 5. Verify the source

- **Sourcify**: choose Monad / Monad Testnet, paste the deployed address.
- **Monadscan** (mainnet): `Verify and Publish` — Solidity (single file),
  compiler **v0.8.28**, license **MIT**, optimization **Yes (runs 200)**, EVM
  **cancun**.

## 6. Mine it — CLI or the browser page

CLI (any EVM chain):

```bash
cd miner
node mine.js --rpc https://testnet-rpc.monad.xyz --contract 0x<MONAD_VAKED> --key 0x...   # testnet
node mine.js --rpc https://rpc.monad.xyz         --contract 0x<MONAD_VAKED> --key 0x...   # mainnet
```

Browser: open https://pocoo.vaked.dev/demos/miner, pick **Monad Testnet**
(or Monad mainnet) in the new Network selector, paste the contract address
into the contract field, connect the wallet, mine, and hit
**Submit mint(nonce)** — the page switches the wallet to the right chain
automatically (or adds it).

## 7. Renounce ownership (when ready)

Only after mints are proven. `renounceOwnership()` selector is `0x715018a6`:

```bash
node -e "
import('./art/chain.js').then(async ({ chain }) => {
  const priv = process.env.PRIVATE_KEY;
  const vakedAddr = '0x<MONAD_VAKED>';
  const rpcUrl = 'https://testnet-rpc.monad.xyz';   // or https://rpc.monad.xyz
  const chainId = 10143;                            // or 143 for mainnet
  const from = chain.privateToAddress(priv);
  const call = async (method, params) => (await (await fetch(rpcUrl, {
    method: 'POST', headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ jsonrpc: '2.0', id: 1, method, params }),
  })).json()).result;
  const nonce = await call('eth_getTransactionCount', [from, 'pending']);
  const gasPrice = await call('eth_gasPrice', []);
  const tx = chain.signLegacyTx({
    nonce, gasPrice, gasLimit: '0x186a0', to: vakedAddr, value: '0x0',
    data: '0x715018a6', priv, chainId,
  });
  console.log(await call('eth_sendRawTransaction', [tx]));
});"
```

## 8. See it with your address

- **Wallets**: add the Monad network (or let the miner page add it), then
  import the token by address — MON is the gas token, so a testnet MON
  balance from the faucet is all the "money" the whole loop needs.
- **Explorers**: `https://monadscan.com/token/0x<addr>` (mainnet) /
  `https://testnet.monadexplorer.com/token/0x<addr>` (testnet).

## Caveats, honest

- Monad mainnet is **not** a zero-fee chain (live: ~102 gwei). What is free
  is the testnet, because the faucet MON is free.
- Testnet tokens have no value; the mainnet contract is the real one, but
  only when you can spare a few cents of MON.
- One mint per round still holds: the challenge rotates after every
  successful mint, on every chain.

*VAKED on Monad · nft/DEPLOY-MONAD.md · the constellation · 0 + 1 · vaked.dev*
