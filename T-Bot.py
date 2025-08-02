import random
import time
money = 10000
days = 365
start_money = money
# Transaction fee per trade
transaction_fee_rate = 0

# Generate stock prices with drift and volatility
def generate_prices(days):
    stocks = [
        "^GSPC", "LTC", "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "DX-Y.NYB", "^XDN",
        "^DJI", "GC=F", "AMD", "RTX", "IBM", "ETH-USD", "SOL", "BTC-USD", "WBD", "INTC", "^XDA"
    ]
    prices = {stock: [] for stock in stocks}
    for stock in stocks:
        base = random.uniform(100,200)
        price = base
        daily_drift = 0.05
        daily_volatility = base * 0.01
        while len(prices[stock]) < days:
            price += daily_drift + random.uniform(-daily_volatility, daily_volatility)
            prices[stock].append(max(price, 0.01))
    return prices

# Compute RSI values
def compute_rsi(prices, window=14):
    rsi = []
    for i in range(len(prices)):
        if i < window:
            rsi.append(50)
            continue
        delta = [prices[j] - prices[j - 1] for j in range(i - window + 1, i + 1)]
        gain = sum(x for x in delta if x > 0) / window
        loss = -sum(x for x in delta if x < 0) / window
        rs = gain / loss if loss != 0 else 0
        rsi_val = 100 - (100 / (1 + rs)) if loss != 0 else 100
        rsi.append(rsi_val)
    return rsi

# Start simulation
prices = generate_prices(days)
rsi_dict = {stock: compute_rsi(prices[stock]) for stock in prices}
positions = {stock: {'shares': 0, 'avg_price': 0} for stock in prices}
active_stocks = set(prices)
profits = 0

# Simulation loop
for i in range(days):
    for stock in list(active_stocks):
        price = prices[stock][i]
        rsi = rsi_dict[stock][i]

        if money <= 0:
            break

        # Buy logic
        if rsi < 40:
            max_shares = int(money // price)
            if max_shares > 0:
                cost = max_shares * price * (1 + transaction_fee_rate)
                money -= cost
                prev_shares = positions[stock]['shares']
                prev_avg = positions[stock]['avg_price']
                new_avg = (prev_avg * prev_shares + cost) / (prev_shares + max_shares)
                positions[stock]['shares'] += max_shares
                positions[stock]['avg_price'] = new_avg
                print(f"BUY {max_shares} shares of {stock} at {price:.2f} (RSI: {rsi:.2f})")

        # Sell logic
        elif rsi > 60 and positions[stock]['shares'] > 0:
            shares = positions[stock]['shares']
            avg_price = positions[stock]['avg_price']
            revenue = shares * price * (1 - transaction_fee_rate)
            profit = revenue - (shares * avg_price)
            profits += profit
            money += revenue
            print(f"SELL {shares} shares of {stock} at {price:.2f} (RSI: {rsi:.2f}) | Profit: {profit:.2f}")
            positions[stock] = {'shares': 0, 'avg_price': 0}

    # Weekly summary
    if (i + 1) % 7 == 0 or i == days - 1:
        week_number = (i + 1) // 7
        portfolio_value = sum(positions[s]['shares'] * prices[s][i] for s in positions)
        print(f"\n Weekly Summary - Week {week_number}")
        print(f"Money: {money:.2f} | Portfolio Value: {portfolio_value:.2f} | Total Profit: {round((money + portfolio_value) - start_money, 2)}")
        time.sleep(1)

# Final sell of all stocks
for stock in positions:
    shares = positions[stock]['shares']
    if shares > 0:
        price = prices[stock][-1]
        avg_price = positions[stock]['avg_price']
        revenue = shares * price * (1 - transaction_fee_rate)
        profit = revenue - (shares * avg_price)
        profits += profit
        money += revenue
        print(f"FINAL SELL {shares} shares of {stock} at {price:.2f} | Profit: {profit:.2f}")

# Final summary
print(f"\nSimulation ended. Final Money: {money:.2f} | Total Profits: {round(money-start_money,2)}")