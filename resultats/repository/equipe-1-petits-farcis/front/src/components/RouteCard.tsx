import { Leaf, Gift, Footprints, Car, Bike, Train, Bus as BusIcon } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { PathSegment } from "@/types/route";

/**
 * RouteCard Component
 * 
 * Displays a summary card for a single route option with:
 * - Total duration
 * - CO2 emissions
 * - Puzzle pieces earned
 * - Transport modes used
 */

interface RouteCardProps {
  routeId: string;
  departure: string;
  arrival: string;
  totalDuration: number;
  totalCO2: number;
  puzzlePieces: number;
  paths: PathSegment[];
  isSelected: boolean;
  onHover: () => void;
  onLeave: () => void;
  onClick: () => void;
}

export const RouteCard = ({
  departure,
  arrival,
  totalDuration,
  totalCO2,
  puzzlePieces,
  paths,
  isSelected,
  onHover,
  onLeave,
  onClick,
}: RouteCardProps) => {
  const formatTime = (isoString: string) => {
    const date = new Date(isoString.replace(/(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(\d{2})/, '$1-$2-$3T$4:$5:$6'));
    return date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
  };

  const formatDuration = (seconds: number) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    return hours > 0 ? `${hours}h ${minutes}min` : `${minutes}min`;
  };


  const getModeIcon = (mode: string, line?: string | null, color?: string | null) => {
    if (line) {
      return (
        <Badge
          className="px-2 py-0.5 text-[11px] font-bold min-w-[24px] justify-center"
          style={{ 
            backgroundColor: color ? `#${color}` : (mode === "Bus" || mode === "Tramway" ? "#00643C" : "#5091CB"),
            color: "white"
          }}
        >
          {line}
        </Badge>
      );
    }
    
    switch (mode.toLowerCase()) {
      case 'walking':
        return <Footprints className="w-5 h-5" />;
      case 'car':
        return <Car className="w-5 h-5" />;
      case 'bike':
        return <Bike className="w-5 h-5" />;
      case 'rer':
        return <Train className="w-5 h-5" />;
      case 'métro':
        return <Train className="w-5 h-5" />;
      case 'bus':
        return <BusIcon className="w-5 h-5" />;
      default:
        return <span className="text-base">🚉</span>;
    }
  };

  return (
    <Card
      className={`p-3 cursor-pointer transition-all duration-200 border ${
        isSelected
          ? "border-[hsl(208,65%,55%)] bg-[hsl(208,65%,98%)] shadow-md"
          : "border-gray-200 hover:border-[hsl(208,65%,55%)] hover:bg-gray-50"
      }`}
      onMouseEnter={onHover}
      onMouseLeave={onLeave}
      onClick={onClick}
    >
      {/* Header: Time & Duration */}
      <div className="flex items-center justify-between mb-2">
        <span className="font-semibold text-sm text-foreground">
          {formatTime(departure)} → {formatTime(arrival)}
        </span>
        <span className="text-sm font-semibold text-[hsl(208,65%,55%)]">
          {formatDuration(totalDuration)}
        </span>
      </div>

      {/* Transport modes */}
      <div className="flex items-center gap-1 mb-2 flex-wrap">
        {paths.map((path, idx) => (
          <div key={idx} className="flex items-center gap-0.5">
            {getModeIcon(path.mode, path.line, path.color)}
            {idx < paths.length - 1 && <span className="text-muted-foreground text-xs mx-0.5">→</span>}
          </div>
        ))}
      </div>

      {/* Metrics */}
      <div className="flex items-center justify-between text-xs pt-2 border-t border-gray-100">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1 text-muted-foreground">
            <Leaf className="w-3 h-3 text-green-600" />
            <span className="font-medium">{totalCO2.toFixed(0)}g</span>
          </div>
        </div>

        <div className="flex items-center gap-1 font-semibold text-primary">
          <Gift className="w-4 h-4" />
          <span>+{puzzlePieces}</span>
        </div>
      </div>
    </Card>
  );
};
