import { Connection, PublicKey } from "@solana/web3.js";
import { Market } from "@project-serum/serum";
import { Buffer } from "buffer";

if (typeof window !== "undefined") {
  (window as any).Buffer = Buffer;
}

const connection = new Connection(
  "https://solana-mainnet.g.alchemy.com/v2/B-KDMIoxs3QAtmDWWHjy3YoYBFvUm-AZ",
  "confirmed"
);
export async function fetchSolanaDexData() {
  const marketAddress = new PublicKey(
    "HWHvQhFmJB3NUcu1aihKmrKegfVxBEHzwVX6yZCKEsi1"
  );
  const programPubkey = new PublicKey(
    "9xQeWvG816bUx9EPjHmaT23yvVM2ZWbrrpZb9PusVFin"
  );

  const market = await Market.load(
    connection,
    marketAddress,
    {},
    programPubkey
  );

  const bids = await market.loadBids(connection);
  const asks = await market.loadAsks(connection);

  const bestBid = bids.getL2(1)[0]?.[0] || 0;
  const bestAsk = asks.getL2(1)[0]?.[0] || 0;

  const midPrice = (bestBid + bestAsk) / 2;

  return {
    symbol: market.address.toBase58(),
    price: midPrice,
    timestamp: Date.now(),
  };
}
