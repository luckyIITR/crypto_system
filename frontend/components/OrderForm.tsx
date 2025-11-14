'use client';

import { useState, FormEvent } from 'react';
import { RiskManagedOrderRequest } from '@/lib/api';

interface OrderFormProps {
  onSubmit: (data: RiskManagedOrderRequest, side: 'buy' | 'sell') => void;
  loading: boolean;
}

export default function OrderForm({ onSubmit, loading }: OrderFormProps) {
  const [formData, setFormData] = useState<RiskManagedOrderRequest>({
    product_symbol: 'BTCUSD',
    risk_per_trade: 50,
    timeframe: '5m',
    candles_count: 5,
  });

  const [useProductId, setUseProductId] = useState(false);

  const handleSubmit = (e: FormEvent, side: 'buy' | 'sell') => {
    e.preventDefault();
    
    // Prepare data - only include product_id OR product_symbol
    const submitData: RiskManagedOrderRequest = {
      risk_per_trade: formData.risk_per_trade,
      timeframe: formData.timeframe,
      candles_count: formData.candles_count,
      reduce_only: formData.reduce_only,
      time_in_force: formData.time_in_force,
      client_order_id: formData.client_order_id,
    };

    if (useProductId && formData.product_id) {
      submitData.product_id = formData.product_id;
    } else {
      submitData.product_symbol = formData.product_symbol;
    }

    onSubmit(submitData, side);
  };

  return (
    <form className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900">Place Order</h2>

      <div className="flex items-center space-x-2">
        <input
          type="checkbox"
          id="useProductId"
          checked={useProductId}
          onChange={(e) => setUseProductId(e.target.checked)}
          className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
        />
        <label htmlFor="useProductId" className="text-sm text-gray-700">
          Use Product ID instead of Symbol
        </label>
      </div>

      {useProductId ? (
        <div>
          <label htmlFor="product_id" className="block text-sm font-medium text-gray-700 mb-2">
            Product ID *
          </label>
          <input
            id="product_id"
            type="number"
            value={formData.product_id || ''}
            onChange={(e) =>
              setFormData({ ...formData, product_id: parseInt(e.target.value) || undefined })
            }
            required
            placeholder="e.g., 27"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-black"
          />
        </div>
      ) : (
        <div>
          <label htmlFor="product_symbol" className="block text-sm font-medium text-gray-700 mb-2">
            Product Symbol *
          </label>
          <select
            id="product_symbol"
            value={formData.product_symbol || ''}
            onChange={(e) =>
              setFormData({ ...formData, product_symbol: e.target.value })
            }
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-black"
          >
            <option value="BTCUSD">BTCUSD</option>
            <option value="ETHUSD">ETHUSD</option>
          </select>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label htmlFor="risk_per_trade" className="block text-sm font-medium text-gray-700 mb-2">
            Risk Per Trade ($) *
          </label>
          <input
            id="risk_per_trade"
            type="number"
            step="0.01"
            min="0.01"
            value={formData.risk_per_trade}
            onChange={(e) =>
              setFormData({ ...formData, risk_per_trade: parseFloat(e.target.value) })
            }
            required
            placeholder="100.00"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-black"
          />
        </div>

        <div>
          <label htmlFor="timeframe" className="block text-sm font-medium text-gray-700 mb-2">
            Timeframe
          </label>
          <select
            id="timeframe"
            value={formData.timeframe}
            onChange={(e) =>
              setFormData({ ...formData, timeframe: e.target.value })
            }
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-black"
          >
            <option value="1m">1 Minute</option>
            <option value="5m">5 Minutes</option>
            <option value="15m">15 Minutes</option>
            <option value="1h">1 Hour</option>
            <option value="4h">4 Hours</option>
            <option value="1d">1 Day</option>
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label htmlFor="candles_count" className="block text-sm font-medium text-gray-700 mb-2">
            Candles Count
          </label>
          <input
            id="candles_count"
            type="number"
            min="1"
            max="100"
            value={formData.candles_count}
            onChange={(e) =>
              setFormData({ ...formData, candles_count: parseInt(e.target.value) })
            }
            placeholder="5"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-black"
          />
        </div>

        <div>
          <label htmlFor="time_in_force" className="block text-sm font-medium text-gray-700 mb-2">
            Time in Force
          </label>
          <select
            id="time_in_force"
            value={formData.time_in_force || ''}
            onChange={(e) =>
              setFormData({ ...formData, time_in_force: e.target.value || undefined })
            }
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-black"
          >
            <option value="">Default</option>
            <option value="GTC">Good Till Cancel (GTC)</option>
            <option value="IOC">Immediate Or Cancel (IOC)</option>
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label htmlFor="reduce_only" className="block text-sm font-medium text-gray-700 mb-2">
            Reduce Only
          </label>
          <select
            id="reduce_only"
            value={formData.reduce_only || ''}
            onChange={(e) =>
              setFormData({ ...formData, reduce_only: e.target.value || undefined })
            }
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-black"
          >
            <option value="">No</option>
            <option value="true">Yes</option>
          </select>
        </div>

        <div>
          <label htmlFor="client_order_id" className="block text-sm font-medium text-gray-700 mb-2">
            Client Order ID (optional)
          </label>
          <input
            id="client_order_id"
            type="text"
            maxLength={32}
            value={formData.client_order_id || ''}
            onChange={(e) =>
              setFormData({ ...formData, client_order_id: e.target.value || undefined })
            }
            placeholder="Custom order identifier"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-black"
          />
        </div>
      </div>

      <div className="flex flex-col sm:flex-row gap-4 pt-4">
        <button
          type="button"
          onClick={(e) => handleSubmit(e, 'buy')}
          disabled={loading}
          className="flex-1 px-6 py-3 bg-gradient-to-r from-green-500 to-emerald-600 text-white font-semibold rounded-lg hover:from-green-600 hover:to-emerald-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
        >
          {loading ? 'Placing...' : '🔼 Place BUY Order'}
        </button>
        <button
          type="button"
          onClick={(e) => handleSubmit(e, 'sell')}
          disabled={loading}
          className="flex-1 px-6 py-3 bg-gradient-to-r from-red-500 to-rose-600 text-white font-semibold rounded-lg hover:from-red-600 hover:to-rose-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
        >
          {loading ? 'Placing...' : '🔽 Place SELL Order'}
        </button>
      </div>

      {loading && (
        <div className="flex flex-col items-center justify-center py-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <p className="mt-4 text-gray-600">Placing order...</p>
        </div>
      )}
    </form>
  );
}

