
import { useEffect, useRef } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { decodePolyline } from "@/lib/polyline";

interface DashboardMapProps {
  traces: { trace: string; name: string }[];
  center?: [number, number];
}

const DashboardMap = ({ traces, center = [48.8566, 2.3522] }: DashboardMapProps) => {
  const mapContainer = useRef<HTMLDivElement>(null);
  const mapInstance = useRef<L.Map | null>(null);
  const layersRef = useRef<L.LayerGroup | null>(null);

  useEffect(() => {
    if (!mapContainer.current || mapInstance.current) return;

    const map = L.map(mapContainer.current, {
      zoomControl: false,
    }).setView(center, 12);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution: '© OpenStreetMap contributors',
    }).addTo(map);

    L.control.zoom({ position: "topright" }).addTo(map);

    mapInstance.current = map;
    layersRef.current = L.layerGroup().addTo(map);

    return () => {
      map.remove();
      mapInstance.current = null;
    };
  }, [center]);

  useEffect(() => {
    if (!mapInstance.current || !layersRef.current) return;

    const map = mapInstance.current;
    const layers = layersRef.current;

    layers.clearLayers();

    if (traces.length === 0) return;

    const allCoordinates: L.LatLngExpression[] = [];
    const colors = ["#FF5733", "#33FF57", "#3357FF", "#FF33A1", "#A133FF"];

    traces.forEach((traceData, index) => {
      const coordinates = decodePolyline(traceData.trace);
      allCoordinates.push(...coordinates);

      const polyline = L.polyline(coordinates, {
        color: "#4285F4", // Set all traces to blue
        weight: 5, // Make traces thicker
        opacity: 0.7,
      });

      polyline.bindPopup(traceData.name);
      polyline.addTo(layers);
    });

    if (allCoordinates.length > 0) {
      const bounds = L.latLngBounds(allCoordinates);
      map.fitBounds(bounds, { padding: [50, 50] });
    }
  }, [traces]);

  return (
    <div className="relative w-full h-full">
      <div ref={mapContainer} className="absolute inset-0 z-0" />
    </div>
  );
};

export default DashboardMap;
