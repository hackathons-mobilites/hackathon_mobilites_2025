/**
 * Polyline decoder utility
 * Decodes Google's encoded polyline format to lat/lng coordinates
 * 
 * @see https://developers.google.com/maps/documentation/utilities/polylinealgorithm
 */

export interface LatLng {
  lat: number;
  lng: number;
}

/**
 * Decode an encoded polyline string to an array of lat/lng coordinates
 * 
 * @param encoded - The encoded polyline string
 * @param precision - Number of decimal places (default: 5)
 * @returns Array of {lat, lng} coordinates
 */
export function decodePolyline(encoded: string, precision: number = 5): LatLng[] {
  const coordinates: LatLng[] = [];
  let index = 0;
  let lat = 0;
  let lng = 0;
  const factor = Math.pow(10, precision);

  while (index < encoded.length) {
    // Decode latitude
    let byte = 0;
    let shift = 0;
    let result = 0;

    do {
      byte = encoded.charCodeAt(index++) - 63;
      result |= (byte & 0x1f) << shift;
      shift += 5;
    } while (byte >= 0x20);

    const deltaLat = ((result & 1) ? ~(result >> 1) : (result >> 1));
    lat += deltaLat;

    // Decode longitude
    shift = 0;
    result = 0;

    do {
      byte = encoded.charCodeAt(index++) - 63;
      result |= (byte & 0x1f) << shift;
      shift += 5;
    } while (byte >= 0x20);

    const deltaLng = ((result & 1) ? ~(result >> 1) : (result >> 1));
    lng += deltaLng;

    coordinates.push({
      lat: lat / factor,
      lng: lng / factor,
    });
  }

  return coordinates;
}

/**
 * Encode an array of lat/lng coordinates to a polyline string
 * 
 * @param coordinates - Array of {lat, lng} coordinates
 * @param precision - Number of decimal places (default: 5)
 * @returns Encoded polyline string
 */
export function encodePolyline(coordinates: LatLng[], precision: number = 5): string {
  const factor = Math.pow(10, precision);
  let encoded = '';
  let prevLat = 0;
  let prevLng = 0;

  for (const coord of coordinates) {
    const lat = Math.round(coord.lat * factor);
    const lng = Math.round(coord.lng * factor);

    encoded += encodeValue(lat - prevLat);
    encoded += encodeValue(lng - prevLng);

    prevLat = lat;
    prevLng = lng;
  }

  return encoded;
}

function encodeValue(value: number): string {
  let encoded = '';
  let num = value < 0 ? ~(value << 1) : (value << 1);

  while (num >= 0x20) {
    encoded += String.fromCharCode((0x20 | (num & 0x1f)) + 63);
    num >>= 5;
  }

  encoded += String.fromCharCode(num + 63);
  return encoded;
}
