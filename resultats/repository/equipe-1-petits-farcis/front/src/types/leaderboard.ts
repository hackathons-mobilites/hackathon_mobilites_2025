/**
 * Type definitions for leaderboard data
 */

/**
 * Employee ranking entry
 */
export interface EmployeeRanking {
  rank: number;
  user_id: string;
  user: string;
  avatar?: string;
  points: number;
  pieces: number;
  delta?: number; // Change from previous week
  level?: string; // e.g., "Executive", "Manager"
}

/**
 * Company ranking entry
 */
export interface CompanyRanking {
  rank: number;
  company_id: string;
  company: string;
  logo?: string;
  score: number;
  delta?: number; // Change from previous week
  league?: string; // e.g., "Gold", "Silver", "Bronze"
}

/**
 * Complete leaderboard data
 */
export interface LeaderboardData {
  employee_ranking: EmployeeRanking[];
  company_ranking: CompanyRanking[];
  current_user?: {
    rank: number;
    points: number;
    pieces: number;
  };
}

/**
 * Leaderboard time period filter
 */
export type LeaderboardPeriod = 'today' | 'week' | 'month' | 'all-time';
