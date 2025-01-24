# Founding Developer - Full Stack Engineer Assessment

Welcome to the submission repository for the Full Stack Engineer assessment. This repository contains two projects:

1. **CEX/DEX Price Arbitrage Scanner**
2. **AI-Powered Price Predictor**

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Installation Instructions](#installation-instructions)
3. [Usage Guide](#usage-guide)
4. [Technical Implementation Details](#technical-implementation-details)
5. [Potential Improvements](#potential-improvements)

---

## Project Overview

### 1. **CEX/DEX Price Arbitrage Scanner**
A tool to identify arbitrage opportunities between Binance (CEX) and Solana DEX markets for the SOL/USDC trading pair.

#### Features:
- Fetches real-time prices from Binance API and Solana DEX.
- Accounts for fees (Binance maker/taker fees, Solana swap fees, and transaction costs).
- Displays profitable arbitrage opportunities after accounting for fees.

#### Notes:
- Built using React for the frontend.
- Only the SOL/USDC trading pair is supported.
- The environment is hardcoded for simplicity.

### 2. **AI-Powered Price Predictor**
An AI-powered system to predict cryptocurrency price trends using Binance historical data.

#### Features:
- Fetches historical price data from Binance API.
- Generates up/down predictions with confidence scores using AI.
- Backtesting framework validates model accuracy.
- Displays performance metrics and visualization.

#### Notes:
- Implemented using Python and Streamlit.
- Requires Binance API key and secret for operation.

---

## Installation Instructions

### Prerequisites
- [Node.js](https://nodejs.org/) (v16 or later)
- [Python](https://www.python.org/) (v3.8 or later)
- [Streamlit](https://streamlit.io/) for the AI-powered price predictor
- API keys for Binance ([Create Binance API keys](https://www.binance.com/en/support/faq/360002502072))

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo-url.git
   cd your-repo-folder
   ```

2. Install dependencies:
   - For the Arbitrage Scanner:
     ```bash
     npm install
     ```
   - For the Price Predictor:
     ```bash
     pip install -r requirements.txt
     ```

3. Set up environment variables:
   - For **Arbitrage Scanner**, environment details are hardcoded.
   - For **Price Predictor**, create a `.env` file with the following:
     ```
     BINANCE_API_KEY=<your-binance-api-key>
     BINANCE_API_SECRET=<your-binance-api-secret>
     ```

4. Run the projects:
   - **Arbitrage Scanner:**
     ```bash
     npm start
     ```
   - **Price Predictor:**
     ```bash
     streamlit run price_predictor.py
     ```

---

## Usage Guide

### Arbitrage Scanner
- Navigate to `http://localhost:3000` after starting the project.
- View live arbitrage opportunities for the SOL/USDC trading pair in the UI.

### Price Predictor
- Run `price_predictor.py` using Streamlit.
- Open the Streamlit app in your browser to interact with the model, view predictions, and backtesting metrics.

---

## Technical Implementation Details

### Arbitrage Scanner
- **Frontend Framework:**
  - Built using React for an interactive UI.
- **APIs Used:**
  - Binance API for CEX price data.
  - Solana RPC for DEX price data.
- **Fee Handling:**
  - Binance fees (maker/taker) are hardcoded.
  - Solana fees are approximated and hardcoded.
- **Core Logic:**
  - Fetches real-time price data via REST APIs.
  - Calculates arbitrage profitability after accounting for fees.

### Price Predictor
- **Data Collection:**
  - Historical price data fetched via Binance API.
- **AI Implementation:**
  - Model: LSTM implemented using TensorFlow/Keras.
  - Framework: Streamlit for interactive frontend.
- **Backtesting Framework:**
  - Simulates trades on historical data.
  - Calculates and visualizes accuracy and profitability metrics.

---

## Potential Improvements

1. **Arbitrage Scanner:**
   - Support additional trading pairs beyond SOL/USDC.
   - Improve scalability by incorporating WebSocket for live price updates.
   - Dynamically fetch Solana swap fees for improved accuracy.

2. **Price Predictor:**
   - Explore advanced models (e.g., transformers) for better predictions.
   - Automate data collection for continuous model updates.
   - Add multi-currency support and detailed performance analysis.

---

Feel free to reach out if you have any questions or feedback!

