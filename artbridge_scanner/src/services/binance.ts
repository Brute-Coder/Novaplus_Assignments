import axios from "axios";
import { MarketPrice } from "../types/market";

export class BinanceService {
  private static BASE_URL = "https://api.binance.com/api/v3";

  static async getPrices(symbols: string[]): Promise<MarketPrice[]> {
    try {
      const response = await axios.get(`${this.BASE_URL}/ticker/price`);
      const allPrices = response.data;

      const data = allPrices
        .filter((price: any) => symbols.includes(price.symbol))
        .map((price: any) => ({
          symbol: price.symbol,
          price: parseFloat(price.price),
          timestamp: Date.now(),
        }));

      console.log(data);

      return data;
    } catch (error) {
      console.error("Error fetching Binance prices:", error);
      return [];
    }
  }
}
