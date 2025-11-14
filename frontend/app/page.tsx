'use client';

import { useState } from 'react';
import { apiClient, OrderResponse, RiskManagedOrderRequest } from '@/lib/api';
import OrderForm from '@/components/OrderForm';
import OrderResults from '@/components/OrderResults';

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<OrderResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (data: RiskManagedOrderRequest, side: 'buy' | 'sell') => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = side === 'buy' 
        ? await apiClient.placeBuyOrder(data)
        : await apiClient.placeSellOrder(data);
      
      setResult(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to place order');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-purple-600 via-blue-600 to-indigo-700">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-2 drop-shadow-lg">
            🚀 Crypto Trading System
          </h1>
          <p className="text-xl text-white/90">
            Risk-managed trading with automatic stop loss
          </p>
        </div>

        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-xl shadow-2xl p-6 md:p-8 mb-6">
            <OrderForm onSubmit={handleSubmit} loading={loading} />
          </div>

          {error && (
            <div className="bg-white rounded-xl shadow-2xl p-6 mb-6">
              <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-red-800 font-semibold">Error</p>
                <p className="text-red-700 mt-2">{error}</p>
              </div>
            </div>
          )}

          {result && (
            <div className="bg-white rounded-xl shadow-2xl p-6 md:p-8">
              <OrderResults result={result} />
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
