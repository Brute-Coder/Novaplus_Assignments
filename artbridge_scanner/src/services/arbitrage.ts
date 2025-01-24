import Decimal from "decimal.js";
import { ArbitrageOpportunity, Fees, MarketPrice } from "../types/market";

export class ArbitrageService {
  private static readonly fees: Fees = {
    binanceMaker: 0.001, // 0.1%
    binanceTaker: 0.001, // 0.1%
    solanaDex: 0.003, // 0.3%
    solanaNetwork: 0.000005, // Approximate SOL fee in USDC
  };

  static calculateArbitrage(
    binancePrice: MarketPrice,
    solanaPrice: MarketPrice,
    tradeAmount: number = 1000 // Default trade size in USDC
  ): ArbitrageOpportunity | null {
    const bPrice = new Decimal(binancePrice.price);
    const sPrice = new Decimal(solanaPrice.price);

    // Calculate total fees
    const binanceFee = bPrice.mul(this.fees.binanceTaker);
    const solanaFee = sPrice.mul(this.fees.solanaDex);
    const networkFee = new Decimal(this.fees.solanaNetwork);

    // Calculate price difference
    const priceDiff = sPrice.sub(bPrice);
    const percentageDiff = priceDiff.div(bPrice).mul(100);

    // Calculate potential profit
    const grossProfit = priceDiff.mul(tradeAmount);
    const totalFees = binanceFee
      .add(solanaFee)
      .add(networkFee)
      .mul(tradeAmount);
    const netProfit = grossProfit.sub(totalFees);

    console.log("netProfit --> ", netProfit.valueOf());

    // Only return opportunities that are profitable after fees

    return {
      symbol: binancePrice.symbol,
      binancePrice: bPrice.toNumber(),
      solanaPrice: sPrice.toNumber(),
      priceDifference: priceDiff.toNumber(),
      percentageDifference: percentageDiff.toNumber(),
      estimatedProfit: netProfit.toNumber(),
      timestamp: Date.now(),
    };

    return null;
  }
}
