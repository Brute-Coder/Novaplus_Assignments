import { Connection, PublicKey } from "@solana/web3.js";
import { Market } from "@project-serum/serum";
import { MarketPrice } from "../types/market";

export class SolanaService {
  private connection: Connection;

  constructor() {
    this.connection = new Connection(
      "https://api.mainnet-beta.solana.com",
      "confirmed"
    );
  }

  async getPrice(marketAddress: string): Promise<MarketPrice | null> {
    try {
      const marketPubkey = new PublicKey(
        "HWHvQhFmJB3NUcu1aihKmrKegfVxBEHzwVX6yZCKEsi1"
      );
      const market = await Market.load(
        this.connection,
        marketPubkey,
        {},
        new PublicKey("9xQeWvG816bUx9EPjHmaT23yvVM2ZWbrrpZb9PusVFin")
      );

      const bids = await market.loadBids(this.connection);
      const asks = await market.loadAsks(this.connection);

      const bestBid = bids.getL2(1)[0]?.[0] || 0;
      const bestAsk = asks.getL2(1)[0]?.[0] || 0;

      if (bestBid === 0 || bestAsk === 0) return null;

      const midPrice = (bestBid + bestAsk) / 2;

      return {
        symbol: market.address.toBase58(),
        price: midPrice,
        timestamp: Date.now(),
      };
    } catch (error) {
      console.error("Error fetching Solana market price:", error);
      return null;
    }
  }
}
