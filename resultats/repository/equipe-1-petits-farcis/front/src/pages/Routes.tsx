import { useState, useEffect, useCallback } from "react";
import { Button } from "@/components/ui/button";
import { RouteCard } from "@/components/RouteCard";
import { RouteMap } from "@/components/RouteMap";
import { Route } from "@/types/route";
import { Play, ArrowLeft, MapPin, XCircle } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { toast } from "sonner";
import config from "@/config";
import mockRoutes from "@/data/mockRoutes.json";

/**
 * Page des Itinéraires
 * 
 * Vue principale pour la recherche et la sélection d'itinéraires
 * - Barre latérale gauche : Liste des itinéraires disponibles
 * - Droite : Carte interactive avec visualisation de l'itinéraire
 * - Survoler pour prévisualiser l'itinéraire sur la carte
 * - Cliquer pour sélectionner et voir les détails
 */

const Routes = () => {
  const navigate = useNavigate();
  const [routes, setRoutes] = useState<Route[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedRouteId, setSelectedRouteId] = useState<string | null>(null);
  const [origin, setOrigin] = useState<{ lat: number; lng: number } | null>(null);
  const [destination, setDestination] = useState<{ lat: number; lng: number } | null>(null);

  const handleMapClick = useCallback((lat: number, lng: number) => {
    if (!origin) {
      setOrigin({ lat, lng });
      toast.info("Point de départ sélectionné", { description: `Lat: ${lat.toFixed(4)}, Lng: ${lng.toFixed(4)}` });
    } else if (!destination) {
      setDestination({ lat, lng });
      toast.info("Point d'arrivée sélectionné", { description: `Lat: ${lat.toFixed(4)}, Lng: ${lng.toFixed(4)}` });
    } else {
      // If both are set, clear and set new origin
      setOrigin({ lat, lng });
      setDestination(null);
      toast.info("Nouveau point de départ sélectionné", { description: `Lat: ${lat.toFixed(4)}, Lng: ${lng.toFixed(4)}` });
    }
  }, [origin, destination]);

  const clearSelection = () => {
    setOrigin(null);
    setDestination(null);
    setRoutes([]);
    setSelectedRouteId(null);
    setError(null);
    toast.info("Sélection effacée", { description: "Veuillez sélectionner de nouveaux points." });
  };

  useEffect(() => {
    const fetchRoutes = async () => {
      if (!origin || !destination) {
        setRoutes([]);
        setSelectedRouteId(null);
        return;
      }

      setLoading(true);
      setError(null);
      try {
        let data;
        if (config.useMockData) {
          data = mockRoutes;
        } else {
          const response = await fetch(`${config.backend.journeys.baseUrl}/journeys`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              from: { lon: origin.lng.toString(), lat: origin.lat.toString() },
              to: { lon: destination.lng.toString(), lat: destination.lat.toString() },
              datetime: "20251121T073000", // TODO: Make this dynamic
            }),
          });

          if (!response.ok) {
            throw new Error('Failed to fetch routes');
          }
          data = await response.json();
        }

        const journeysWithId = data.journeys.map((journey: any, index: number) => {
          const departure = new Date(journey.departure.replace(/(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(\d{2})/, '$1-$2-$3T$4:$5:$6'));
          const arrival = new Date(journey.arrival.replace(/(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(\d{2})/, '$1-$2-$3T$4:$5:$6'));
          const totalDuration = (arrival.getTime() - departure.getTime()) / 1000;

          return {
            ...journey,
            id: `journey-${index}`,
            totalCO2: journey.co2,
            totalDuration: totalDuration,
            puzzlePieces: journey.number_of_gifts,
          }
        });
        setRoutes(journeysWithId);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An unknown error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchRoutes();
  }, [origin, destination]);

  const selectedRoute = routes.find((r) => r.id === selectedRouteId);

  const displayRoute = selectedRoute;

  const handleStartTrip = () => {
    if (!selectedRoute) return;

    // Mock trip completion
    toast.success("Trajet terminé !", {
      description: `Vous avez gagné ${selectedRoute.puzzlePieces} pièces de puzzle ! 🧩`,
    });

    // Simulate API call
    console.log("POST /api/trip/complete", {
      tripId: selectedRoute.id,
      unlocked_pieces: ["piece_3", "piece_7"],
    });
  };

  return (
    <div className="h-screen flex flex-col bg-background">
      {/* Header */}
      <header className="bg-primary text-white p-3">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => navigate("/")}
              className="text-white hover:bg-white/20"
            >
              <ArrowLeft className="w-5 h-5" />
            </Button>
            <div>
              <h1 className="text-xl font-semibold">Recherche d'Itinéraire</h1>
              <p className="text-xs text-white/90">
                Choisissez votre trajet écologique
              </p>
            </div>
          </div>
          <div className="text-right text-xs">
            <p className="opacity-90">Paris, Île-de-France</p>
            <p className="opacity-70">Aujourd'hui, 07:32</p>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Sidebar - Route List */}
        <aside className="w-[380px] bg-white p-3 overflow-y-auto border-r">
          <div className="space-y-2">
            <div className="mb-3">
              <h2 className="text-base font-semibold text-foreground mb-1">Itinéraires Disponibles</h2>
              {(!origin || !destination) && !loading && (
                <p className="text-xs text-muted-foreground">Veuillez sélectionner un point de départ et d'arrivée sur la carte.</p>
              )}
              {loading && origin && destination && <p className="text-xs text-muted-foreground">Chargement des itinéraires...</p>}
              {error && <p className="text-xs text-red-500">{error}</p>}
              {!loading && !error && (origin && destination) && (
                <p className="text-xs text-muted-foreground">
                  {routes.length} options écologiques
                </p>
              )}
            </div>

            {routes.map((route) => (
              <RouteCard
                key={route.id}
                routeId={route.id!}
                departure={route.departure}
                arrival={route.arrival}
                totalDuration={route.totalDuration!}
                totalCO2={route.totalCO2!}
                puzzlePieces={route.puzzlePieces!}
                paths={route.paths}
                isSelected={selectedRouteId === route.id}
                onHover={() => {}}
                onLeave={() => {}}
                onClick={() => {
                  setSelectedRouteId(prevId => prevId === route.id ? null : route.id!);
                }}
              />
            ))}
          </div>
        </aside>

        {/* Map View */}
        <main className="flex-1 relative bg-gray-100">
          <RouteMap
            paths={displayRoute?.paths || []}
            gifts={displayRoute?.gifts || []}
            center={[48.8566, 2.3522]}
            onMapClick={handleMapClick}
            origin={origin || undefined}
            destination={destination || undefined}
          />
          
          {/* Selection Status and Clear Button */}
          {(origin || destination) && (
            <div className="absolute top-4 left-1/2 transform -translate-x-1/2 z-[1000] flex items-center space-x-2 bg-background p-2 rounded-lg shadow-md">
              {origin && (
                <span className="text-sm text-green-600 flex items-center">
                  <MapPin className="w-4 h-4 mr-1" /> Départ: {origin.lat.toFixed(3)}, {origin.lng.toFixed(3)}
                </span>
              )}
              {destination && (
                <span className="text-sm text-red-600 flex items-center">
                  <MapPin className="w-4 h-4 mr-1" /> Arrivée: {destination.lat.toFixed(3)}, {destination.lng.toFixed(3)}
                </span>
              )}
              <Button variant="ghost" size="icon" onClick={clearSelection} className="text-muted-foreground hover:text-foreground">
                <XCircle className="w-5 h-5" />
              </Button>
            </div>
          )}
          
          {/* Start Trip Button */}
          {selectedRoute && (
            <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-slide-in z-[1000]">
              <Button
                size="lg"
                onClick={handleStartTrip}
                className="bg-primary hover:bg-primary/90 text-white shadow-xl hover:shadow-2xl transition-all duration-300 hover:scale-105 font-semibold"
              >
                <Play className="w-5 h-5 mr-2" />
                Commencer le trajet & Gagner {selectedRoute.puzzlePieces} Pièces
              </Button>
            </div>
          )}
        </main>
      </div>
    </div>
  );
};

export default Routes;
