# Crypto Trading System - Frontend

Next.js frontend application for the Crypto Trading System API.

## Features

- 🎨 Modern, responsive UI with Tailwind CSS
- 📊 Real-time order placement
- 📈 Calculated values display
- 🎯 BUY/SELL order support
- ⚡ Fast API integration
- 📱 Mobile-friendly design

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn
- Backend API running on `http://localhost:8000`

### Installation

```bash
# Install dependencies
npm install
```

### Environment Setup

Create a `.env.local` file in the frontend directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Development

```bash
# Start development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build for Production

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── app/                    # Next.js app directory
│   ├── page.tsx           # Main page
│   ├── layout.tsx         # Root layout
│   └── globals.css        # Global styles
├── components/            # React components
│   ├── OrderForm.tsx     # Order placement form
│   └── OrderResults.tsx  # Results display
├── lib/                   # Utilities
│   └── api.ts            # API client
└── package.json
```

## Usage

1. Fill in the order form:
   - Product Symbol (e.g., BTCUSD) or Product ID
   - Risk Per Trade amount
   - Timeframe and candles count
   - Optional parameters

2. Click "Place BUY Order" or "Place SELL Order"

3. View the results including:
   - Calculated stop loss price
   - Position size in lots and base currency
   - Order details

## API Integration

The frontend communicates with the FastAPI backend through the API client in `lib/api.ts`. The API base URL can be configured via the `NEXT_PUBLIC_API_URL` environment variable.

## Technologies

- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Axios** - HTTP client (via fetch API)
