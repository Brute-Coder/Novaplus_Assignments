import pandas as pd
import numpy as np
from binance.client import Client
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.metrics import accuracy_score, precision_score, recall_score
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class CryptoPricePredictor:
    def __init__(self, api_key=None, api_secret=None):
        """Initialize the predictor with optional Binance API credentials"""
        self.client = Client(api_key, api_secret) if api_key and api_secret else None
        self.scaler = MinMaxScaler()
        self.model = None
        self.sequence_length = 60  # Look back 60 periods
        
    def fetch_historical_data(self, symbol, interval, start_str, end_str=None):
        """Fetch historical data from Binance"""
        if not self.client:
            raise ValueError("Binance API credentials not provided")
            
        klines = self.client.get_historical_klines(
            symbol, interval, start_str, end_str
        )
        
        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_volume', 'trades', 'taker_buy_base',
            'taker_buy_quote', 'ignored'
        ])
        
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        df = df.astype(float)
        return df[['close', 'volume', 'high', 'low']]
    
    def prepare_data(self, df, test_size=0.2):
        """Prepare data for LSTM model"""
        # Calculate additional features
        df['returns'] = df['close'].pct_change()
        df['volatility'] = df['returns'].rolling(window=20).std()
        df['rsi'] = self._calculate_rsi(df['close'])
        df.dropna(inplace=True)
        
        # Scale features
        scaled_data = self.scaler.fit_transform(df)
        
        # Create sequences
        X, y = [], []
        for i in range(len(scaled_data) - self.sequence_length):
            X.append(scaled_data[i:i + self.sequence_length])
            # 1 if price goes up, 0 if down
            y.append(1 if scaled_data[i + self.sequence_length][0] > 
                    scaled_data[i + self.sequence_length - 1][0] else 0)
        
        X, y = np.array(X), np.array(y)
        
        # Split into train/test
        split = int(len(X) * (1 - test_size))
        X_train, X_test = X[:split], X[split:]
        y_train, y_test = y[:split], y[split:]
        
        return (X_train, y_train), (X_test, y_test)
    
    def build_model(self):
        """Build LSTM model architecture"""
        self.model = Sequential([
            LSTM(100, return_sequences=True, input_shape=(self.sequence_length, 6)),
            Dropout(0.2),
            LSTM(50, return_sequences=False),
            Dropout(0.2),
            Dense(25, activation='relu'),
            Dense(1, activation='sigmoid')
        ])
        
        self.model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
    def train(self, X_train, y_train, epochs=50, batch_size=32, validation_split=0.1):
        """Train the model"""
        return self.model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            verbose=1
        )
    
    def backtest(self, X_test, y_test):
        """Perform backtesting and calculate metrics"""
        predictions_prob = self.model.predict(X_test)
        predictions = (predictions_prob > 0.5).astype(int)
        
        results = {
            'accuracy': accuracy_score(y_test, predictions),
            'precision': precision_score(y_test, predictions),
            'recall': recall_score(y_test, predictions)
        }
        
        # Calculate profit/loss assuming equal position sizes
        pnl = []
        position = 0
        for i, pred in enumerate(predictions):
            if pred == 1:  # Long position
                position = 1
            else:  # Short position
                position = -1
            
            # Calculate returns
            actual_return = y_test[i]
            trade_pnl = position * actual_return
            pnl.append(trade_pnl)
        
        results['cumulative_returns'] = np.cumsum(pnl)
        return results
    
    def visualize_results(self, history, backtest_results):
        """Visualize training history and backtesting results"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Plot training history
        ax1.plot(history.history['accuracy'], label='Training Accuracy')
        ax1.plot(history.history['val_accuracy'], label='Validation Accuracy')
        ax1.set_title('Model Accuracy')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Accuracy')
        ax1.legend()
        
        # Plot cumulative returns
        ax2.plot(backtest_results['cumulative_returns'], label='Cumulative Returns')
        ax2.set_title('Backtest Performance')
        ax2.set_xlabel('Trade')
        ax2.set_ylabel('Cumulative Return')
        ax2.legend()
        
        plt.tight_layout()
        return fig
    
    def _calculate_rsi(self, prices, period=14):
        """Calculate Relative Strength Index"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def predict_next(self, current_data):
        """Predict the next price movement with probability"""
        scaled_data = self.scaler.transform(current_data[-self.sequence_length:])
        X = np.array([scaled_data])
        probability = self.model.predict(X)[0][0]
        prediction = 1 if probability > 0.5 else 0
        return prediction, probability