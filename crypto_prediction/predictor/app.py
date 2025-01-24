import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import yfinance as yf  # As backup data source if no Binance API keys
# from predictor.crypto_predictor import CryptoPricePredictor  # Our previous class
from crypto_predictor import CryptoPricePredictor

def main():
    st.set_page_config(page_title="Crypto Price Predictor", layout="wide")
    st.title("Cryptocurrency Price Prediction System")

    # Sidebar for configuration
    st.sidebar.header("Configuration")
    
    # API Configuration
    use_binance = st.sidebar.checkbox("Use Binance API")
    api_key = None
    api_secret = None
    
    if use_binance:
        api_key = st.sidebar.text_input("Binance API Key", type="password")
        api_secret = st.sidebar.text_input("Binance API Secret", type="password")

    # Trading pair selection
    symbol = st.sidebar.selectbox(
        "Select Trading Pair",
        ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "DOGEUSDT"]
    )

    # Time frame selection
    timeframe = st.sidebar.selectbox(
        "Select Timeframe",
        ["1h", "4h", "1d"]
    )

    # Training period
    training_period = st.sidebar.slider(
        "Training Period (months)",
        min_value=1,
        max_value=24,
        value=6
    )

    # Model parameters
    st.sidebar.header("Model Parameters")
    epochs = st.sidebar.slider("Training Epochs", 10, 200, 50)
    sequence_length = st.sidebar.slider("Sequence Length", 30, 100, 60)
    
    # Initialize predictor
    predictor = CryptoPricePredictor(api_key, api_secret)
    predictor.sequence_length = sequence_length

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("Historical Data & Predictions")
        
        if st.button("Fetch Data & Train Model"):
            try:
                with st.spinner("Fetching data..."):
                    if use_binance and api_key and api_secret:
                        data = predictor.fetch_historical_data(
                            symbol, 
                            timeframe, 
                            f"{training_period} months ago"
                        )
                    else:
                        # Fallback to yfinance if no Binance credentials
                        ticker = symbol.replace("USDT", "-USD")
                        data = yf.download(
                            ticker,
                            start=datetime.now() - timedelta(days=30*training_period),
                            interval=timeframe
                        )
                        data = data[['Close', 'Volume', 'High', 'Low']]
                        data.columns = data.columns.str.lower()

                st.write("Data Preview:")
                st.dataframe(data.head())

                with st.spinner("Training model..."):
                    # Prepare and train model
                    (X_train, y_train), (X_test, y_test) = predictor.prepare_data(data)
                    predictor.build_model()
                    history = predictor.train(X_train, y_train, epochs=epochs)

                    # Backtest
                    results = predictor.backtest(X_test, y_test)

                    # Display metrics
                    st.header("Model Performance")
                    metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
                    metrics_col1.metric("Accuracy", f"{results['accuracy']:.2%}")
                    metrics_col2.metric("Precision", f"{results['precision']:.2%}")
                    metrics_col3.metric("Recall", f"{results['recall']:.2%}")

                    # Plot results using Plotly
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        y=history.history['accuracy'],
                        name="Training Accuracy"
                    ))
                    fig.add_trace(go.Scatter(
                        y=history.history['val_accuracy'],
                        name="Validation Accuracy"
                    ))
                    fig.update_layout(
                        title="Model Training History",
                        xaxis_title="Epoch",
                        yaxis_title="Accuracy"
                    )
                    st.plotly_chart(fig)

                    # Plot cumulative returns
                    fig_returns = go.Figure()
                    fig_returns.add_trace(go.Scatter(
                        y=results['cumulative_returns'],
                        name="Cumulative Returns"
                    ))
                    fig_returns.update_layout(
                        title="Backtest Performance",
                        xaxis_title="Trade",
                        yaxis_title="Cumulative Return"
                    )
                    st.plotly_chart(fig_returns)

                    # Save model state in session
                    st.session_state['model'] = predictor
                    st.session_state['latest_data'] = data

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    with col2:
        st.header("Live Predictions")
        if st.button("Get Next Prediction"):
            if 'model' in st.session_state and 'latest_data' in st.session_state:
                prediction, probability = st.session_state['model'].predict_next(
                    st.session_state['latest_data']
                )
                
                # Display prediction
                st.subheader("Next Movement Prediction")
                prediction_text = "🔼 UP" if prediction == 1 else "🔽 DOWN"
                st.markdown(f"### {prediction_text}")
                st.progress(float(probability))
                st.write(f"Confidence: {probability:.2%}")
                
                # Add timestamp
                st.write(f"Prediction made at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                st.warning("Please train the model first!")

if __name__ == "__main__":
    main()