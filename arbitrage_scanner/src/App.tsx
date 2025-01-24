import { useEffect, useState } from 'react';
import { ArrowUpDown, RefreshCw } from 'lucide-react';
import { ArbitrageOpportunity } from './types/market';
import { BinanceService } from './services/binance';
import { ArbitrageService } from './services/arbitrage';
import { fetchSolanaDexData } from './services/solana-alchemy'

const MARKET_ADDRESSES = {
  'SOLUSDC': '9wFFyRfZBsuAha4YcuxcXLKwMxJR43S7fPfQLusDBzvT'
};

function App() {
  const [opportunities, setOpportunities] = useState<ArbitrageOpportunity[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const scanMarkets = async () => {
    try {
      setLoading(true);
      setError(null);

      const tradingPairs = Object.keys(MARKET_ADDRESSES);
      const binancePrices = await BinanceService.getPrices(tradingPairs);

      const opportunities: ArbitrageOpportunity[] = [];

      const solanaPrice = await fetchSolanaDexData();
      console.log(solanaPrice)
      if (solanaPrice) {
        const opportunity = ArbitrageService.calculateArbitrage(
          binancePrices[0],
          {
            ...solanaPrice,
            symbol: binancePrices[0].symbol
          }

        );
        if (opportunity) {
          opportunities.push(opportunity);
        }
      }

      setOpportunities(opportunities);
    } catch (err) {
      setError('Failed to scan markets. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    scanMarkets();
    const interval = setInterval(scanMarkets, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="p-6">
            <div className="flex justify-between items-center mb-6">
              <h1 className="text-2xl font-bold text-gray-900">
                Crypto Arbitrage Scanner
              </h1>
              <button
                onClick={scanMarkets}
                disabled={loading}
                className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
              >
                <RefreshCw className="w-4 h-4 mr-2" />
                Refresh
              </button>
            </div>

            {error && (
              <div className="mb-4 p-4 bg-red-100 text-red-700 rounded-md">
                {error}
              </div>
            )}

            {loading ? (
              <div className="flex justify-center items-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600" />
              </div>
            ) : opportunities.length > 0 ? (
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Trading Pair
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Binance Price
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Solana DEX Price
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Difference %
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Est. Profit
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {opportunities.map((opp) => (
                      <tr key={opp.symbol}>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center">
                            <ArrowUpDown className="w-4 h-4 mr-2 text-gray-400" />
                            {opp.symbol}
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          ${opp.binancePrice.toFixed(6)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          ${opp.solanaPrice.toFixed(6)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`px-2 py-1 rounded-full text-xs ${opp.percentageDifference > 0
                            ? 'bg-green-100 text-green-800'
                            : 'bg-red-100 text-red-800'
                            }`}>
                            {opp.percentageDifference.toFixed(2)}%
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          ${opp.estimatedProfit.toFixed(2)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div className="text-center py-12">
                <p className="text-gray-500">
                  No arbitrage opportunities found at the moment.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;