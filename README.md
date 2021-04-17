# cryptoX
## Introduction
An automated Cryptocurrency-Index including X currencies sorted by market cap.
## APIs
Used APIs: CoinMarketCap, Crypto Fear & Greed Index by Alternative.me and Binance.
### API Keys
API Keys should be stored as environment variables;
- CoinMarketCap Key: `CMC_API_KEY`
- Binance API Key: `BINANCE_API_KEY` 
- Binance Secret Key: `BINANCE_SECRET_KEY`
## Errors
`APIError(code=-1021): Timestamp for this request was 1000ms ahead of the server's time.` - resync OS clock