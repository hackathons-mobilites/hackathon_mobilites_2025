/**
 * Type definitions for weekly puzzle game
 */

/**
 * Weekly puzzle data for a company
 */
export interface WeeklyPuzzle {
  company_name: string;
  puzzle_id: string;
  image_b64: string; // Base64 encoded image data URL
  unlocked_tiles: string[]; // Array of tile IDs in format "row_col"
  attempts_left: number;
  total_tiles: number;
  progress_percentage: number;
  contributors?: Contributor[];
}

/**
 * User who contributed to unlocking puzzle pieces
 */
export interface Contributor {
  user_id: string;
  username: string;
  avatar?: string;
  pieces_unlocked: number;
}

/**
 * Puzzle guess attempt
 */
export interface PuzzleGuess {
  userId: string;
  guess: string;
}

/**
 * Puzzle guess response
 */
export interface PuzzleGuessResponse {
  correct: boolean;
  attempts_left: number;
  message: string;
  reward_unlocked?: boolean;
}
