from stock import Stock


appl = Stock("AAPL", start="2025-09-29", end="2026-09-28")
nlfx = Stock(symbol="nflx", start="2025-09-29", end="2026-09-28")

print(appl.data)
fig = appl.plot_performance()
fig.show()
