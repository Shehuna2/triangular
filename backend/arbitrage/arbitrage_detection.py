from itertools import permutations

def detect_arbitrage_opportunities(pairs, prices):
    """Find arbitrage opportunities using filtered pairs."""
    opportunities = []
    paths = generate_arbitrage_paths(pairs)
    for path in paths:
        rates = [prices.get(path[0], 0), 1 / prices.get(path[1], 0), prices.get(path[2], 0)]
        profit = calculate_profit(rates)
        if profit > 0:
            opportunities.append((path, profit))
    return opportunities

def generate_arbitrage_paths(pairs):
    """Generate possible 3-hop arbitrage paths."""
    return [p for p in permutations(pairs, 3)]
