'use client';

import { OrderResponse } from '@/lib/api';

interface OrderResultsProps {
  result: OrderResponse;
}

export default function OrderResults({ result }: OrderResultsProps) {
  const { success, message, calculated_values, market_order } = result;

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900">Order Results</h2>

      {success ? (
        <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
          <p className="text-green-800 font-semibold">✓ {message}</p>
        </div>
      ) : (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-800 font-semibold">✗ Order Failed</p>
          {result.error && <p className="text-red-700 mt-2">{result.error}</p>}
        </div>
      )}

      {calculated_values && (
        <div>
          <h3 className="text-xl font-semibold text-gray-800 mb-4">Calculated Values</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div className="p-4 bg-gray-50 rounded-lg border-l-4 border-blue-500">
              <p className="text-sm text-gray-600 mb-1">Current Price</p>
              <p className="text-lg font-semibold text-gray-900">
                ${calculated_values.current_price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
              </p>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg border-l-4 border-red-500">
              <p className="text-sm text-gray-600 mb-1">Stop Loss Price</p>
              <p className="text-lg font-semibold text-gray-900">
                ${calculated_values.stop_loss_price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
              </p>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg border-l-4 border-purple-500">
              <p className="text-sm text-gray-600 mb-1">SL Points</p>
              <p className="text-lg font-semibold text-gray-900">
                ${calculated_values.sl_points.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
              </p>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg border-l-4 border-yellow-500">
              <p className="text-sm text-gray-600 mb-1">Risk Per Trade</p>
              <p className="text-lg font-semibold text-gray-900">
                ${calculated_values.risk_per_trade.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
              </p>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg border-l-4 border-indigo-500">
              <p className="text-sm text-gray-600 mb-1">Position Size (Lots)</p>
              <p className="text-lg font-semibold text-gray-900">
                {calculated_values.position_size}
              </p>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg border-l-4 border-teal-500">
              <p className="text-sm text-gray-600 mb-1">Position Size (Base Currency)</p>
              <p className="text-lg font-semibold text-gray-900">
                {calculated_values.position_size_base_currency.toFixed(6)}
              </p>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg border-l-4 border-pink-500">
              <p className="text-sm text-gray-600 mb-1">Lot Size</p>
              <p className="text-lg font-semibold text-gray-900">
                {calculated_values.lot_size}
              </p>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg border-l-4 border-cyan-500">
              <p className="text-sm text-gray-600 mb-1">Timeframe</p>
              <p className="text-lg font-semibold text-gray-900">
                {calculated_values.timeframe}
              </p>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg border-l-4 border-orange-500">
              <p className="text-sm text-gray-600 mb-1">Candles Count</p>
              <p className="text-lg font-semibold text-gray-900">
                {calculated_values.candles_count}
              </p>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg border-l-4 border-gray-500">
              <p className="text-sm text-gray-600 mb-1">Side</p>
              <p className={`text-lg font-semibold ${
                calculated_values.side === 'buy' ? 'text-green-600' : 'text-red-600'
              }`}>
                {calculated_values.side.toUpperCase()}
              </p>
            </div>
          </div>
        </div>
      )}

      {market_order && (
        <div className="mt-6">
          <h3 className="text-xl font-semibold text-gray-800 mb-4">Order Details</h3>
          <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <pre className="text-sm text-gray-800 whitespace-pre-wrap overflow-x-auto">
              {JSON.stringify(market_order, null, 2)}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}

