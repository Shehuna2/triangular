async def filter_pairs_by_liquidity(pairs, threshold, client):
    """Filters trading pairs based on liquidity."""
    filtered = []
    for pair in pairs:
        liquidity = await get_real_time_liquidity(pair, client)
        if liquidity >= threshold:
            filtered.append(pair)
    return filtered
