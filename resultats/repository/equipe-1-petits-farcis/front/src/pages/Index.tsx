import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Map, Puzzle as PuzzleIcon, Trophy, Leaf, LayoutDashboard } from "lucide-react";
import { useNavigate } from "react-router-dom";

/**
 * Page d'accueil - Hub de navigation
 * 
 * Point d'entrée principal avec navigation vers trois fonctionnalités principales :
 * 1. Recherche d'itinéraire
 * 2. Puzzle de la semaine
 * 3. Classements
 */

const Index = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: <Map className="w-12 h-12 text-primary" />,
      title: "Recherche d'Itinéraire",
      description: "Trouvez des itinéraires écologiques et gagnez des pièces de puzzle",
      path: "/routes",
    },
    {
      icon: <PuzzleIcon className="w-12 h-12 text-primary" />,
      title: "Puzzle de la Semaine",
      description: "Collaborez pour résoudre le cadeau mystère",
      path: "/puzzle",
    },
    {
      icon: <Trophy className="w-12 h-12 text-primary" />,
      title: "Classements",
      description: "Rivalisez avec vos collègues et d'autres entreprises",
      path: "/leaderboard",
    },
    {
      icon: <LayoutDashboard className="w-12 h-12 text-primary" />,
      title: "Tableaux de Bord",
      description: "Visualisez les performances de mobilité",
      path: "/dashboard",
    },
  ];

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="bg-primary text-white p-8">
        <div className="max-w-6xl mx-auto">
          <div className="flex items-center gap-4 mb-4">
            <Leaf className="w-16 h-16" />
            <div>
              <h1 className="text-4xl font-bold">Défi Éco-Mobilité IDFM</h1>
              <p className="text-lg text-white/90 mt-2">
                Décarbonez vos trajets, un voyage à la fois
              </p>
            </div>
          </div>
          
          <div className="grid grid-cols-3 gap-4 mt-6 text-center">
            <div>
              <p className="text-3xl font-bold">2,850</p>
              <p className="text-sm text-white/80">Vos Points</p>
            </div>
            <div>
              <p className="text-3xl font-bold">23</p>
              <p className="text-sm text-white/80">Pièces de Puzzle</p>
            </div>
            <div>
              <p className="text-3xl font-bold">#1</p>
              <p className="text-sm text-white/80">Classement Entreprise</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Navigation */}
      <main className="max-w-6xl mx-auto p-8">
        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-2">Que souhaitez-vous faire ?</h2>
          <p className="text-muted-foreground">
            Choisissez une activité pour continuer votre parcours d'éco-mobilité
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature) => (
            <Card
              key={feature.path}
              className="group cursor-pointer transition-all duration-300 hover:shadow-lg overflow-hidden flex flex-col"
              onClick={() => navigate(feature.path)}
            >
              <div
                className="p-8 text-center flex-grow"
              >
                <div className="mb-4 inline-block">
                  {feature.icon}
                </div>
                <h3 className="text-2xl font-bold mb-2">{feature.title}</h3>
                <p className="text-muted-foreground text-sm">{feature.description}</p>
              </div>
              
              <div className="p-6 bg-card">
                <Button
                  className="w-full bg-primary hover:bg-primary/90 text-white"
                >
                  Commencer →
                </Button>
              </div>
            </Card>
          ))}
        </div>

        {/* How it Works */}
        <Card className="mt-12 p-8 bg-secondary/30">
          <h3 className="text-xl font-bold mb-4">Comment ça marche</h3>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="flex gap-4">
              <div className="w-10 h-10 rounded-full bg-primary text-white flex items-center justify-center font-bold flex-shrink-0">
                1
              </div>
              <div>
                <h4 className="font-semibold mb-1">Choisissez des itinéraires écologiques</h4>
                <p className="text-sm text-muted-foreground">
                  Sélectionnez des options de transport plus écologiques pour vos trajets quotidiens
                </p>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="w-10 h-10 rounded-full bg-primary text-white flex items-center justify-center font-bold flex-shrink-0">
                2
              </div>
              <div>
                <h4 className="font-semibold mb-1">Gagnez des pièces de puzzle</h4>
                <p className="text-sm text-muted-foreground">
                  Effectuez des trajets pour débloquer les pièces du puzzle hebdomadaire de votre entreprise
                </p>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="w-10 h-10 rounded-full bg-primary text-white flex items-center justify-center font-bold flex-shrink-0">
                3
              </div>
              <div>
                <h4 className="font-semibold mb-1">Montez dans le classement</h4>
                <p className="text-sm text-muted-foreground">
                  Rivalisez avec vos collègues et d'autres entreprises pour des récompenses
                </p>
              </div>
            </div>
          </div>
        </Card>
      </main>

      {/* Footer */}
      <footer className="bg-card mt-16 p-6 text-center text-sm text-muted-foreground border-t">
        <p>
          🌱 Ensemble, nous réduisons les émissions de carbone, un trajet à la fois
        </p>
        <p className="mt-2">
          Développé avec React, TypeScript & Tailwind CSS
        </p>
      </footer>
    </div>
  );
};

export default Index;
