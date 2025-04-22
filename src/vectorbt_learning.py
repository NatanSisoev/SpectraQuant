import vectorbt as vb

btc_price = vb.YFData.download(
    "BTC-USD",
    missing_index="drop",
).get("Close")

# print(btc_price)

rsi = vb.RSI.run(btc_price, window=14)
print(rsi)

entries = rsi.rsi_crossed_below(30)
exits   = rsi.rsi_crossed_above(70)

pf = vb.Portfolio.from_signals(btc_price, entries, exits)

print(pf.stats())
