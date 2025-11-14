GRID_SIZE = 10  # 10x10 grid = 100 tiles

# Tile reveal probability distribution based on position
# Tiles closer to borders are more likely to remain unrevealed (hidden)
TILE_UNREVEALED_PROBABILITIES = {
    'border': 0.05,      # 5% probability for border tiles to be unrevealed
    'middle': 0.2,      # 20% probability for middle ring tiles to be unrevealed
    'center': 0.75       # 75% probability for center tiles to be unrevealed
}