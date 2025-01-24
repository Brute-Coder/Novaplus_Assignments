export interface MarketPrice {
  symbol: string;
  price: number;
  timestamp: number;
}

export interface ArbitrageOpportunity {
  symbol: string;
  binancePrice: number;
  solanaPrice: number;
  priceDifference: number;
  percentageDifference: number;
  estimatedProfit: number;
  timestamp: number;
}

export interface Fees {
  binanceMaker: number;
  binanceTaker: number;
  solanaDex: number;
  solanaNetwork: number;
}