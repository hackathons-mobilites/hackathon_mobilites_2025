/**
 * Type definitions for route and trip data
 */

export type TransportMode = 'walking' | 'RER' | 'Metro' | 'Bus' | 'Tramway';

/**
 * Single path segment within a route
 */
export interface PathSegment {
  mode: TransportMode;
  shape: string; // Encoded polyline
  line: string | null; // Line number/name (null for walking)
  departure: string; // ISO 8601 datetime
  arrival: string; // ISO 8601 datetime
  duration_s: number; // Duration in seconds
  distance_m: number; // Distance in meters
  color: string | null; // Hex color code (without #) for transit lines
  co2: number; // CO2 emissions in grams
}

/**
 * Gift/reward marker on the map
 */
export interface Gift {
  id: string;
  lat: number;
  lon: number;
  name?: string;
  description?: string;
}

/**
 * Complete route with all segments
 */
export interface Route {
  id?: string; // Unique route identifier
  departure: string; // ISO 8601 datetime
  arrival: string; // ISO 8601 datetime
  paths: PathSegment[];
  gifts: Gift[];
  totalCO2?: number; // Total CO2 emissions
  totalDuration?: number; // Total duration in seconds
  totalDistance?: number; // Total distance in meters
  puzzlePieces?: number; // Number of puzzle pieces earned
  ecoScore?: number; // Ecological score 0-100
}

/**
 * Trip completion response
 */
export interface TripCompletionResponse {
  tripId: string;
  unlocked_pieces: string[];
  points_earned: number;
  total_points: number;
}
