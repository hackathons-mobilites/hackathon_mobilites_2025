import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, Trophy, TrendingUp, TrendingDown, Medal } from "lucide-react";
import { useNavigate } from "react-router-dom";
import mockData from "@/data/mockLeaderboard.json";
import { EmployeeRanking, CompanyRanking } from "@/types/leaderboard";

/**
 * Page des classements
 * 
 * Deux types de classements :
 * 1. Classement des employés au sein de l'entreprise
 * 2. Classement des entreprises (ligues)
 */

const Leaderboard = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<"employees" | "companies">("employees");

  const employeeRankings = mockData.employee_ranking as EmployeeRanking[];
  const companyRankings = mockData.company_ranking as CompanyRanking[];

  const getRankBadgeClass = (rank: number) => {
    if (rank === 1) return "rank-badge rank-1";
    if (rank === 2) return "rank-badge rank-2";
    if (rank === 3) return "rank-badge rank-3";
    return "rank-badge bg-muted text-muted-foreground";
  };

  const getDeltaIcon = (delta?: number) => {
    if (!delta) return null;
    if (delta > 0) return <TrendingUp className="w-4 h-4 text-green-600" />;
    if (delta < 0) return <TrendingDown className="w-4 h-4 text-red-600" />;
    return null;
  };

  const getLeagueBadge = (league?: string) => {
    if (!league) return null;
    return (
      <Badge className="bg-primary/20 text-primary">
        {league}
      </Badge>
    );
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="bg-primary text-white p-6">
        <div className="max-w-6xl mx-auto">
          <div className="flex items-center gap-4 mb-4">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => navigate("/")}
              className="text-white hover:bg-white/20"
            >
              <ArrowLeft className="w-5 h-5" />
            </Button>
            <div>
              <h1 className="text-3xl font-bold flex items-center gap-3">
                <Trophy className="w-8 h-8" />
                Classements
              </h1>
              <p className="text-sm text-white/80 mt-1">
                Rivalisez avec vos collègues et d'autres entreprises
              </p>
            </div>
          </div>

          {/* Current User Stats */}
          {mockData.current_user && activeTab === "employees" && (
            <Card className="bg-white/10 p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className={getRankBadgeClass(mockData.current_user.rank)}>
                    {mockData.current_user.rank}
                  </div>
                  <div>
                    <p className="text-sm text-white/80">Votre Rang</p>
                    <p className="text-2xl font-bold">#{mockData.current_user.rank}</p>
                  </div>
                </div>
                <div className="flex gap-6 text-right">
                  <div>
                    <p className="text-sm text-white/80">Points</p>
                    <p className="text-xl font-bold">{mockData.current_user.points}</p>
                  </div>
                  <div>
                    <p className="text-sm text-white/80">Pièces</p>
                    <p className="text-xl font-bold">{mockData.current_user.pieces}</p>
                  </div>
                </div>
              </div>
            </Card>
          )}
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto p-6">
        <Tabs value={activeTab} onValueChange={(v) => setActiveTab(v as any)}>
          <TabsList className="grid w-full max-w-md mx-auto grid-cols-2 mb-6">
            <TabsTrigger value="employees">Employés</TabsTrigger>
            <TabsTrigger value="companies">Entreprises</TabsTrigger>
          </TabsList>

          {/* Employee Rankings */}
          <TabsContent value="employees">
            <div className="space-y-3">
              {employeeRankings.map((employee) => (
                <Card
                  key={employee.user_id}
                  className="p-4 transition-all duration-300 hover:shadow-lg animate-fade-in"
                  style={{ animationDelay: `${employee.rank * 50}ms` }}
                >
                  <div className="flex items-center justify-between">
                    {/* Left: Rank & User Info */}
                    <div className="flex items-center gap-4 flex-1">
                      <div className={getRankBadgeClass(employee.rank)}>
                        {employee.rank}
                      </div>

                      <div className="flex items-center gap-3">
                        <div className="w-12 h-12 rounded-full bg-primary flex items-center justify-center text-white font-bold text-lg">
                          {employee.user.charAt(0)}
                        </div>
                        <div>
                          <p className="font-semibold text-lg flex items-center gap-2">
                            {employee.user}
                            {employee.rank === 1 && (
                              <Medal className="w-5 h-5 text-primary" />
                            )}
                          </p>
                          <p className="text-sm text-muted-foreground">
                            {employee.level}
                          </p>
                        </div>
                      </div>
                    </div>

                    {/* Right: Stats */}
                    <div className="flex items-center gap-6">
                      <div className="text-right">
                        <p className="text-2xl font-bold text-primary">
                          {employee.points.toLocaleString()}
                        </p>
                        <p className="text-xs text-muted-foreground">Points</p>
                      </div>

                      <div className="text-right">
                        <p className="text-xl font-bold text-primary">
                          {employee.pieces}
                        </p>
                        <p className="text-xs text-muted-foreground">Pièces</p>
                      </div>

                      {employee.delta !== undefined && employee.delta !== 0 && (
                        <div className="flex items-center gap-1">
                          {getDeltaIcon(employee.delta)}
                          <span className="text-sm font-medium">
                            {Math.abs(employee.delta)}
                          </span>
                        </div>
                      )}
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          </TabsContent>

          {/* Company Rankings */}
          <TabsContent value="companies">
            <div className="space-y-3">
              {companyRankings.map((company) => (
                <Card
                  key={company.company_id}
                  className="p-4 transition-all duration-300 hover:shadow-lg animate-fade-in"
                  style={{ animationDelay: `${company.rank * 50}ms` }}
                >
                  <div className="flex items-center justify-between">
                    {/* Left: Rank & Company Info */}
                    <div className="flex items-center gap-4 flex-1">
                      <div className={getRankBadgeClass(company.rank)}>
                        {company.rank}
                      </div>

                      <div className="flex items-center gap-3">
                        <div className="w-12 h-12 rounded-lg bg-primary flex items-center justify-center text-white font-bold text-xl">
                          {company.company.substring(0, 2).toUpperCase()}
                        </div>
                        <div>
                          <p className="font-semibold text-lg flex items-center gap-2">
                            {company.company}
                            {company.rank === 1 && (
                              <Trophy className="w-5 h-5 text-primary" />
                            )}
                          </p>
                          {company.league && getLeagueBadge(company.league)}
                        </div>
                      </div>
                    </div>

                    {/* Right: Stats */}
                    <div className="flex items-center gap-6">
                      <div className="text-right">
                        <p className="text-3xl font-bold text-primary">
                          {company.score.toLocaleString()}
                        </p>
                        <p className="text-xs text-muted-foreground">Score Total</p>
                      </div>

                      {company.delta !== undefined && company.delta !== 0 && (
                        <div className="flex items-center gap-1">
                          {getDeltaIcon(company.delta)}
                          <span className="text-sm font-medium">
                            {Math.abs(company.delta)}
                          </span>
                        </div>
                      )}
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
};

export default Leaderboard;
