"""
Storage service for managing puzzle data and user attempts using CSV files.
"""
import csv
import os
import random
from datetime import datetime
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import config from routes
from routes import config

# Data file paths
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
GAME_DATA_FILE = os.path.join(DATA_DIR, 'game_data.csv')
USER_GUESSES_FILE = os.path.join(DATA_DIR, 'user_guesses.csv')
PUZZLE_ANSWERS_FILE = os.path.join(DATA_DIR, 'puzzle_answers.csv')


def get_tile_position_category(row: int, col: int, grid_size: int) -> str:
    """
    Determine the position category of a tile (border, middle, or center).
    
    Args:
        row: Row index of the tile
        col: Column index of the tile
        grid_size: Size of the grid
        
    Returns:
        'border', 'middle', or 'center'
    """
    # Calculate distance from edges
    dist_from_edge = min(row, col, grid_size - 1 - row, grid_size - 1 - col)
    
    # Define zones based on distance from edge
    if dist_from_edge == 0:
        return 'border'
    elif dist_from_edge == 1 or dist_from_edge == 2:
        return 'middle'
    else:
        return 'center'


def get_tile_unrevealed_weight(tile: str, grid_size: int) -> float:
    """
    Get the probability weight for a tile to remain unrevealed based on its position.
    
    Args:
        tile: Tile identifier in format "row_col"
        grid_size: Size of the grid
        
    Returns:
        Probability weight for the tile to be unrevealed
    """
    row, col = map(int, tile.split('_'))
    category = get_tile_position_category(row, col, grid_size)
    return config.TILE_UNREVEALED_PROBABILITIES[category]


def ensure_data_files():
    """Ensure CSV files exist with proper headers."""
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Ensure game_data.csv exists
    if not os.path.exists(GAME_DATA_FILE):
        with open(GAME_DATA_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['company_name', 'puzzle_id', 'nbr_of_unlocked_tiles', 'unrevealed_tiles'])
    
    # Ensure user_guesses.csv exists
    if not os.path.exists(USER_GUESSES_FILE):
        with open(USER_GUESSES_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['user_id', 'company_name', 'puzzle_id', 'guess_date', 'attempts_today'])
    
    # Ensure puzzle_answers.csv exists
    if not os.path.exists(PUZZLE_ANSWERS_FILE):
        with open(PUZZLE_ANSWERS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['company_name', 'puzzle_id', 'correct_answer'])


def save_puzzle_clues(company_name: str, puzzle_id: str, 
                      nbr_of_unlocked_tiles: int, grid_size: int = 5) -> bool:
    """
    Save or update puzzle clues count for a company.
    Automatically manages which tiles are revealed/unrevealed.
    
    Args:
        company_name: Name of the company
        puzzle_id: Unique puzzle identifier
        nbr_of_unlocked_tiles: Number of tiles to unlock (incremental)
        grid_size: Size of the grid (default 5 for 5x5 grid)
        
    Returns:
        True if successful, False otherwise
    """
    ensure_data_files()
    
    try:
        # Total tiles based on grid_size
        total_tiles = grid_size * grid_size
        
        # Read all existing data
        all_rows = []
        existing_entry = None
        entry_index = -1
        
        with open(GAME_DATA_FILE, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader):
                all_rows.append(row)
                if row['company_name'] == company_name and row['puzzle_id'] == puzzle_id:
                    existing_entry = row
                    entry_index = idx
        
        # Get currently revealed tiles (tiles NOT in unrevealed list)
        if existing_entry and existing_entry.get('unrevealed_tiles'):
            # Parse existing unrevealed tiles
            existing_unrevealed = set(existing_entry['unrevealed_tiles'].split(',')) if existing_entry['unrevealed_tiles'] else set()
            # All tiles that are NOT unrevealed are revealed
            all_tiles = {f"{i//grid_size}_{i%grid_size}" for i in range(total_tiles)}
            currently_revealed = all_tiles - existing_unrevealed
        else:
            currently_revealed = set()
        
        # Calculate how many new tiles to reveal
        current_revealed_count = len(currently_revealed)
        new_revealed_count = min(current_revealed_count + nbr_of_unlocked_tiles, total_tiles)
        tiles_to_add = new_revealed_count - current_revealed_count
        
        # Get all tiles that are still unrevealed
        all_tiles = {f"{i//grid_size}_{i%grid_size}" for i in range(total_tiles)}
        available_to_reveal = list(all_tiles - currently_revealed)
        
        # Randomly select tiles to reveal from available tiles using weighted probabilities
        # Tiles with higher unrevealed weight are LESS likely to be revealed
        if tiles_to_add > 0 and available_to_reveal:
            # Calculate inverse weights (lower unrevealed probability = higher reveal probability)
            weights = [1.0 / get_tile_unrevealed_weight(tile, grid_size) for tile in available_to_reveal]
            
            # Use weighted random selection
            tiles_to_reveal_count = min(tiles_to_add, len(available_to_reveal))
            newly_revealed = set(random.choices(available_to_reveal, weights=weights, k=tiles_to_reveal_count))
            
            # Ensure we don't have duplicates (extremely rare with choices, but let's be safe)
            while len(newly_revealed) < tiles_to_reveal_count and len(newly_revealed) < len(available_to_reveal):
                remaining = [t for t in available_to_reveal if t not in newly_revealed]
                remaining_weights = [1.0 / get_tile_unrevealed_weight(tile, grid_size) for tile in remaining]
                additional = random.choices(remaining, weights=remaining_weights, k=1)[0]
                newly_revealed.add(additional)
            
            currently_revealed.update(newly_revealed)
        
        # Calculate unrevealed tiles (all tiles minus revealed ones)
        unrevealed = sorted(list(all_tiles - currently_revealed))
        
        # Create updated entry
        updated_entry = {
            'company_name': company_name,
            'puzzle_id': puzzle_id,
            'nbr_of_unlocked_tiles': str(len(currently_revealed)),
            'unrevealed_tiles': ','.join(unrevealed)
        }
        
        # Update the last matching entry or append new one
        if entry_index >= 0:
            all_rows[entry_index] = updated_entry
        else:
            all_rows.append(updated_entry)
        
        # Write everything back
        with open(GAME_DATA_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['company_name', 'puzzle_id', 'nbr_of_unlocked_tiles', 
                                                   'unrevealed_tiles'])
            writer.writeheader()
            writer.writerows(all_rows)
        
        logger.info(f"Saved clues for {company_name} - {puzzle_id}: {len(currently_revealed)} total tiles revealed (added {tiles_to_add} random tiles)")
        return True
        
    except Exception as e:
        logger.error(f"Error saving puzzle clues: {e}")
        return False


def get_puzzle_data(company_name: str, puzzle_id: str) -> Optional[Dict]:
    """
    Retrieve puzzle data for a company.
    Returns the matching entry for company_name and puzzle_id.
    
    Args:
        company_name: Name of the company
        puzzle_id: Unique puzzle identifier
        
    Returns:
        Dictionary with puzzle data or None if not found
    """
    ensure_data_files()
    
    try:
        with open(GAME_DATA_FILE, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['company_name'] == company_name and row['puzzle_id'] == puzzle_id:
                    # Parse unrevealed_tiles back to list
                    if row.get('unrevealed_tiles'):
                        row['unrevealed_tiles'] = row['unrevealed_tiles'].split(',')
                    else:
                        row['unrevealed_tiles'] = []
                    
                    row['nbr_of_unlocked_tiles'] = int(row.get('nbr_of_unlocked_tiles', 0))
                    logger.info(f"Retrieved puzzle data for {company_name} - {puzzle_id}")
                    return row
        
        logger.warning(f"Puzzle not found: {company_name} - {puzzle_id}")
        return None
        
    except Exception as e:
        logger.error(f"Error retrieving puzzle data: {e}")
        return None


def reveal_full_image(company_name: str, puzzle_id: str, grid_size: int = 5) -> bool:
    """
    Reveal the full image by clearing unrevealed_tiles.
    Called when a user finds the correct answer.
    
    Args:
        company_name: Name of the company
        puzzle_id: Unique puzzle identifier
        grid_size: Size of the grid (default 5 for 5x5 grid)
        
    Returns:
        True if successful, False otherwise
    """
    ensure_data_files()
    
    try:
        # Calculate total tiles based on grid_size
        total_tiles = grid_size * grid_size
        
        # Read all existing data
        all_rows = []
        entry_index = -1
        
        with open(GAME_DATA_FILE, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader):
                all_rows.append(row)
                if row['company_name'] == company_name and row['puzzle_id'] == puzzle_id:
                    entry_index = idx
        
        if entry_index >= 0:
            # Clear unrevealed_tiles and set all tiles as revealed
            all_rows[entry_index]['nbr_of_unlocked_tiles'] = str(total_tiles)
            all_rows[entry_index]['unrevealed_tiles'] = ''
            
            # Write everything back
            with open(GAME_DATA_FILE, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['company_name', 'puzzle_id', 'nbr_of_unlocked_tiles', 
                                                       'unrevealed_tiles'])
                writer.writeheader()
                writer.writerows(all_rows)
            
            logger.info(f"Revealed full image for {company_name} - {puzzle_id}")
            return True
        else:
            logger.warning(f"Puzzle not found to reveal: {company_name} - {puzzle_id}")
            return False
        
    except Exception as e:
        logger.error(f"Error revealing full image: {e}")
        return False


def save_puzzle_answer(company_name: str, puzzle_id: str, correct_answer: str) -> bool:
    """
    Save the correct answer for a puzzle.
    
    Args:
        company_name: Name of the company
        puzzle_id: Unique puzzle identifier
        correct_answer: The correct answer for the puzzle
        
    Returns:
        True if successful, False otherwise
    """
    ensure_data_files()
    
    try:
        # Read all existing answers
        all_rows = []
        entry_index = -1
        
        with open(PUZZLE_ANSWERS_FILE, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader):
                all_rows.append(row)
                if row['company_name'] == company_name and row['puzzle_id'] == puzzle_id:
                    entry_index = idx
        
        # Create entry
        answer_entry = {
            'company_name': company_name,
            'puzzle_id': puzzle_id,
            'correct_answer': correct_answer
        }
        
        # Update existing or append new
        if entry_index >= 0:
            all_rows[entry_index] = answer_entry
        else:
            all_rows.append(answer_entry)
        
        # Write back
        with open(PUZZLE_ANSWERS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['company_name', 'puzzle_id', 'correct_answer'])
            writer.writeheader()
            writer.writerows(all_rows)
        
        logger.info(f"Saved correct answer for {company_name} - {puzzle_id}")
        return True
        
    except Exception as e:
        logger.error(f"Error saving puzzle answer: {e}")
        return False


def get_correct_answer(company_name: str, puzzle_id: str) -> Optional[str]:
    """
    Get the correct answer for a puzzle.
    
    Args:
        company_name: Name of the company
        puzzle_id: Unique puzzle identifier
        
    Returns:
        Correct answer string or None if not found
    """
    ensure_data_files()
    
    try:
        with open(PUZZLE_ANSWERS_FILE, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['company_name'] == company_name and row['puzzle_id'] == puzzle_id:
                    logger.info(f"Retrieved correct answer for {company_name} - {puzzle_id}")
                    return row['correct_answer']
        
        logger.warning(f"Correct answer not found: {company_name} - {puzzle_id}")
        return None
        
    except Exception as e:
        logger.error(f"Error retrieving correct answer: {e}")
        return None


def get_user_attempts(user_id: str, company_name: str, puzzle_id: str) -> int:
    """
    Get the number of attempts a user has made today for a specific puzzle.
    
    Args:
        user_id: Unique user identifier
        company_name: Name of the company
        puzzle_id: Unique puzzle identifier
        
    Returns:
        Number of attempts made today
    """
    ensure_data_files()
    today = datetime.now().strftime('%Y-%m-%d')
    
    try:
        with open(USER_GUESSES_FILE, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if (row['user_id'] == user_id and 
                    row['company_name'] == company_name and 
                    row['puzzle_id'] == puzzle_id and 
                    row['guess_date'] == today):
                    return int(row['attempts_today'])
        
        return 0
        
    except Exception as e:
        logger.error(f"Error getting user attempts: {e}")
        return 0


def record_user_attempt(user_id: str, company_name: str, puzzle_id: str) -> bool:
    """
    Record a user's guess attempt.
    
    Args:
        user_id: Unique user identifier
        company_name: Name of the company
        puzzle_id: Unique puzzle identifier
        
    Returns:
        True if successful, False otherwise
    """
    ensure_data_files()
    today = datetime.now().strftime('%Y-%m-%d')
    
    try:
        # Read existing attempts
        attempts = []
        user_found = False
        
        with open(USER_GUESSES_FILE, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if (row['user_id'] == user_id and 
                    row['company_name'] == company_name and 
                    row['puzzle_id'] == puzzle_id and 
                    row['guess_date'] == today):
                    # Increment attempts for today
                    row['attempts_today'] = str(int(row['attempts_today']) + 1)
                    user_found = True
                attempts.append(row)
        
        # Add new record if user hasn't attempted today
        if not user_found:
            attempts.append({
                'user_id': user_id,
                'company_name': company_name,
                'puzzle_id': puzzle_id,
                'guess_date': today,
                'attempts_today': '1'
            })
        
        # Write back to file
        with open(USER_GUESSES_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['user_id', 'company_name', 'puzzle_id', 
                                                   'guess_date', 'attempts_today'])
            writer.writeheader()
            writer.writerows(attempts)
        
        logger.info(f"Recorded attempt for user {user_id}")
        return True
        
    except Exception as e:
        logger.error(f"Error recording user attempt: {e}")
        return False
