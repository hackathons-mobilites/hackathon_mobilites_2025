import { useEffect, useRef } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { decodePolyline } from "@/lib/polyline";
import { Gift as GiftType, PathSegment } from "@/types/route";

interface RouteMapProps {
  routeShape?: string;
  gifts: GiftType[];
  center?: [number, number];
  paths?: PathSegment[];
  onMapClick?: (lat: number, lng: number) => void;
  origin?: { lat: number; lng: number };
  destination?: { lat: number; lng: number };
}

export const RouteMap = ({ gifts, center = [48.8566, 2.3522], paths = [], onMapClick, origin, destination }: RouteMapProps) => {
  const mapContainer = useRef<HTMLDivElement>(null);
  const mapInstance = useRef<L.Map | null>(null);
  const layersRef = useRef<L.LayerGroup | null>(null);
  const originMarkerRef = useRef<L.Marker | null>(null);
  const destinationMarkerRef = useRef<L.Marker | null>(null);

  useEffect(() => {
    if (!mapContainer.current || mapInstance.current) return;

    // Initialize map
    const map = L.map(mapContainer.current, {
      zoomControl: false,
    }).setView(center, 13);

    // Add OpenStreetMap tiles
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution: '© OpenStreetMap contributors',
    }).addTo(map);

    // Add zoom control to top right
    L.control.zoom({ position: "topright" }).addTo(map);

    mapInstance.current = map;
    layersRef.current = L.layerGroup().addTo(map);

    if (onMapClick) {
      map.on('click', (e: L.LeafletMouseEvent) => {
        onMapClick(e.latlng.lat, e.latlng.lng);
      });
    }

    return () => {
      map.remove();
      mapInstance.current = null;
    };
  }, [center, onMapClick]);

  // Update route display when paths change
  useEffect(() => {
    if (!mapInstance.current || !layersRef.current) return;

    const map = mapInstance.current;
    const layers = layersRef.current;

    // Clear previous layers
    layers.clearLayers();

    if (paths.length === 0) return;

    const allCoordinates: L.LatLngExpression[] = [];

    // Draw each path segment
    paths.forEach((path, index) => {
      if (!path.shape) return;

      const coordinates = decodePolyline(path.shape);
      allCoordinates.push(...coordinates);

      let color = "#5091CB"; // Default primary blue
      let weight = 5;
      let opacity = 0.8;

      // Customize style based on mode
      if (path.mode === "walking") {
        color = "#8B9A9F";
        weight = 3;
        opacity = 0.6;
      } else if (path.mode === "RER" || path.mode === "Metro") {
        color = path.color ? `#${path.color}` : "#5091CB";
        weight = 6;
        opacity = 0.9;
      } else if (path.mode === "Bus") {
        color = path.color ? `#${path.color}` : "#00643C";
        weight = 5;
        opacity = 0.85;
      }

      const polyline = L.polyline(coordinates, {
        color,
        weight,
        opacity,
        lineJoin: "round",
        lineCap: "round",
      });

      polyline.addTo(layers);

      // Add start marker for first segment
      if (index === 0 && coordinates.length > 0) {
        const startMarker = L.divIcon({
          html: `
            <div style="display: flex; flex-direction: column; align-items: center;">
              <div style="width: 18px; height: 18px; background-color: #fff; border: 3px solid #4CAF50; border-radius: 50%; box-shadow: 0 2px 5px rgba(0,0,0,0.3);"></div>
              <div style="width: 5px; height: 8px; background-color: #4CAF50; margin-top: -1px;"></div>
              <div style="width: 16px; height: 16px; background-color: rgba(76, 175, 80, 0.3); border-radius: 50%; margin-top: -8px; animation: pulse 2s infinite;"></div>
              <style>
                @keyframes pulse {
                  0%, 100% { transform: scale(0.8); opacity: 0.7; }
                  50% { transform: scale(1.5); opacity: 0.3; }
                }
              </style>
            </div>
          `,
          className: "custom-marker",
          iconSize: [30, 40],
          iconAnchor: [15, 34],
        });
        L.marker(coordinates[0], { icon: startMarker }).addTo(layers);
      }

      // Add end marker for last segment
      if (index === paths.length - 1 && coordinates.length > 0) {
        const endMarker = L.divIcon({
          html: `
            <div style="display: flex; flex-direction: column; align-items: center;">
              <div style="width: 18px; height: 18px; background-color: #fff; border: 3px solid #E91E63; border-radius: 50%; box-shadow: 0 2px 5px rgba(0,0,0,0.3);"></div>
              <div style="width: 5px; height: 8px; background-color: #E91E63; margin-top: -1px;"></div>
              <div style="width: 16px; height: 16px; background-color: rgba(233, 30, 99, 0.3); border-radius: 50%; margin-top: -8px; animation: pulse 2s infinite;"></div>
            </div>
          `,
          className: "custom-marker",
          iconSize: [30, 40],
          iconAnchor: [15, 34],
        });
        L.marker(coordinates[coordinates.length - 1], { icon: endMarker }).addTo(layers);
      }
    });

    // Add gift markers
    gifts.forEach((gift) => {
      const giftIcon = L.divIcon({
        html: `
          <div style="background-color: hsl(var(--primary)); border-radius: 50%; padding: 5px; box-shadow: 0 2px 8px rgba(0,0,0,0.3);">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="8" width="18" height="4" rx="1"/>
              <path d="M12 8v13"/>
              <path d="M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7"/>
              <path d="M7.5 8a2.5 2.5 0 0 1 0-5A2.5 2.5 0 0 1 12 5.5V8"/>
              <path d="M16.5 8a2.5 2.5 0 0 0 0-5A2.5 2.5 0 0 0 12 5.5V8"/>
            </svg>
          </div>
        `,
        className: "gift-marker",
        iconSize: [28, 28],
        iconAnchor: [14, 14],
      });

      const marker = L.marker([gift.lat, gift.lon], { icon: giftIcon }).addTo(layers);
      
      if (gift.name || gift.description) {
        marker.bindPopup(`
          <div style="font-family: system-ui, sans-serif;">
            <strong style="color: hsl(var(--primary));">${gift.name || "Reward"}</strong>
            ${gift.description ? `<p style="margin-top: 4px; font-size: 12px;">${gift.description}</p>` : ""}
          </div>
        `);
      }
    });

    // Fit bounds if we have coordinates
    if (allCoordinates.length > 0) {
      const bounds = L.latLngBounds(allCoordinates);
      map.fitBounds(bounds, { padding: [50, 50] });
    }
  }, [paths, gifts]);

  // Effect for origin and destination markers
  useEffect(() => {
    if (!mapInstance.current || !layersRef.current) return;

    const map = mapInstance.current;
    const layers = layersRef.current;

    // Clear existing O/D markers
    if (originMarkerRef.current) {
      layers.removeLayer(originMarkerRef.current);
      originMarkerRef.current = null;
    }
    if (destinationMarkerRef.current) {
      layers.removeLayer(destinationMarkerRef.current);
      destinationMarkerRef.current = null;
    }

    // Add origin marker
    if (origin) {
      const originIcon = L.divIcon({
        html: `
          <div style="display: flex; flex-direction: column; align-items: center;">
            <div style="width: 18px; height: 18px; background-color: #fff; border: 3px solid #4CAF50; border-radius: 50%; box-shadow: 0 2px 5px rgba(0,0,0,0.3);"></div>
            <div style="width: 5px; height: 8px; background-color: #4CAF50; margin-top: -1px;"></div>
          </div>
        `,
        className: "origin-marker",
        iconSize: [30, 40],
        iconAnchor: [15, 34],
      });
      originMarkerRef.current = L.marker([origin.lat, origin.lng], { icon: originIcon }).addTo(layers);
    }

    // Add destination marker
    if (destination) {
      const destinationIcon = L.divIcon({
        html: `
          <div style="display: flex; flex-direction: column; align-items: center;">
            <div style="width: 18px; height: 18px; background-color: #fff; border: 3px solid #E91E63; border-radius: 50%; box-shadow: 0 2px 5px rgba(0,0,0,0.3);"></div>
            <div style="width: 5px; height: 8px; background-color: #E91E63; margin-top: -1px;"></div>
          </div>
        `,
        className: "destination-marker",
        iconSize: [30, 40],
        iconAnchor: [15, 34],
      });
      destinationMarkerRef.current = L.marker([destination.lat, destination.lng], { icon: destinationIcon }).addTo(layers);
    }
  }, [origin, destination]);

  return (
    <div className="relative w-full h-full">
      <div ref={mapContainer} className="absolute inset-0 z-0" />
    </div>
  );
};
