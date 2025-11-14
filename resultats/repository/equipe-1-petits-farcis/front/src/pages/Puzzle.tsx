import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { ArrowLeft, Search, Users, TrendingUp } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { toast } from "sonner";
import config from "@/config";
import useLocalStorage from "@/hooks/useLocalStorage";
import mockPuzzleReveal from "@/data/mockPuzzleReveal.json";
import puzzle_call_1 from "@/data/puzzle_call_1.json";
import puzzle_call_2 from "@/data/puzzle_call_2.json";
import puzzle_call_3 from "@/data/puzzle_call_3.json";
import puzzle_all_revealed from "@/data/puzzle_all_revealed.json";
import guessTrue from "@/data/guessTrue.json";
import guessWrong from "@/data/guessWrong.json";
import mockLeaderboard from "@/data/mockLeaderboard.json"; // For contributors

/**
 * Page du Puzzle
 * * Jeu de puzzle collaboratif hebdomadaire
 */

const Puzzle = () => {
    const navigate = useNavigate();
    const [guess, setGuess] = useState("");
    const [attemptsLeft, setAttemptsLeft] = useState(3);
    const [isCorrect, setIsCorrect] = useState(false);
    const [puzzleStage, setPuzzleStage] = useState(0);

    const [puzzleImage, setPuzzleImage] = useState("");
    const [unlockedTiles, setUnlockedTiles] = useState<string[]>([]);
    const [totalTiles, setTotalTiles] = useState(16);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);


    const companyName = "TechCorp";
    const puzzleId = "puzzle_colonne_vendome";
    const userId = "user_001";

    useEffect(() => {
        const fetchPuzzleData = async () => {
            try {
                setLoading(true);
                let revealData;
                let cluesData;

                const puzzleStages = [
                    puzzle_call_1,
                    puzzle_call_2,
                    puzzle_call_3,
                ];

                if (config.useMockData) {
                    if (isCorrect) {
                        revealData = puzzle_all_revealed;
                        // When correct, all tiles are considered unlocked for progress display
                        cluesData = { unlocked_tiles: Array.from({ length: 16 }, (_, i) => `${Math.floor(i / 4)}_${i % 4}`), total_tiles: 16 };
                    } else {
                        revealData = puzzleStages[Math.min(puzzleStage, puzzleStages.length - 1)];
                        // For mock data, cluesData can be the same as revealData for simplicity
                        cluesData = revealData;
                    }
                } else {
                    // Existing backend logic for fetching puzzle image and clues
                    const revealResponse = await fetch(`${config.backend.puzzle.baseUrl}/reveal`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ company_name: companyName, puzzle_id: puzzleId }),
                    });
                    if (!revealResponse.ok) throw new Error('Failed to fetch puzzle image');
                    revealData = await revealResponse.json();
                    console.log(revealData.revealed_image_b64);
                    // Fetch clues (unlocked tiles)
                    const cluesResponse = await fetch(`${config.backend.puzzle.baseUrl}/clues`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ company_name: companyName, puzzle_id: puzzleId, nbr_of_unlocked_tiles: 4 }),
                    });
                    if (!cluesResponse.ok) throw new Error('Failed to fetch puzzle clues');
                    cluesData = await cluesResponse.json();
                }

                setPuzzleImage(revealData.revealed_image_b64);
                setUnlockedTiles(cluesData.unlocked_tiles || []);
                setTotalTiles(cluesData.total_tiles || 16);

                // Increment puzzle stage for next refresh, only if not yet fully revealed and not correct
                if (!isCorrect && puzzleStage < puzzleStages.length - 1) {
                    setPuzzleStage(prevStage => prevStage + 1);
                }

            } catch (err) {
                setError(err instanceof Error ? err.message : 'An unknown error occurred');
            } finally {
                setLoading(false);
            }
        };

        fetchPuzzleData();
    }, [isCorrect, puzzleStage]); // Depend on isCorrect and puzzleStage to re-fetch when they change

    const handleGuess = async () => {
        if (!guess.trim()) {
            toast.error("Veuillez entrer une proposition !");
            return;
        }

        try {
            let result;

            if (config.useMockData) {
                if (guess.trim().toLowerCase() === 'place vendome') {
                    result = guessTrue;
                } else {
                    result = guessWrong;
                }
            } else {
                const response = await fetch(`${config.backend.puzzle.baseUrl}/guess`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        user_id: userId,
                        company_name: companyName,
                        puzzle_id: puzzleId,
                        guess: guess.trim(),
                        attempts_left: attemptsLeft,
                    }),
                });

                if (!response.ok) {
                    throw new Error('Failed to submit guess');
                }
                result = await response.json();
            }

            if (result.status === "correct") {
                setIsCorrect(true);
                setPuzzleImage(puzzle_all_revealed.revealed_image_b64); // Immediately show the revealed image
                toast.success("🎉 Correct ! Vous avez trouvé le cadeau mystère !", {
                    description: "Vous avez débloqué une récompense spéciale !",
                });
            } else {
                const newAttempts = attemptsLeft - 1;
                setAttemptsLeft(newAttempts);

                if (newAttempts === 0) {
                    toast.error("Aucune tentative restante !", {
                        description: "Meilleure chance la semaine prochaine !",
                    });
                } else {
                    toast.error("Proposition incorrecte !", {
                        description: `${newAttempts} tentative${newAttempts > 1 ? 's' : ''} restante${newAttempts > 1 ? 's' : ''}`,
                    });
                }
            }
        } catch (err) {
            toast.error(err instanceof Error ? err.message : 'An unknown error occurred');
        }

        setGuess("");
    };

    const progressPercentage = totalTiles > 0 ? (unlockedTiles.length / totalTiles) * 100 : 0;

    const gridSize = 4; // 4x4 grid
    const tiles = Array.from({ length: gridSize * gridSize }, (_, i) => {
        const row = Math.floor(i / gridSize);
        const col = i % gridSize;
        const tileId = `${row}_${col}`;
        return {
            id: tileId,
            unlocked: unlockedTiles.includes(tileId),
        };
    });

    return (
        <div className="min-h-screen bg-background">
            {/* Header */}
            <header className="bg-primary text-primary-foreground p-4">
                <div className="max-w-6xl mx-auto flex items-center justify-between">
                    <div className="flex items-center gap-4">
                        <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => navigate("/")}
                            className="text-primary-foreground hover:bg-primary-foreground/20"
                        >
                            <ArrowLeft className="w-5 h-5" />
                        </Button>
                        <div>
                            <h1 className="text-2xl font-bold">Puzzle de la Semaine</h1>
                            <p className="text-sm text-primary-foreground/80">
                                {companyName}
                            </p>
                        </div>
                    </div>
                    {config.useMockData && (
                        <Button
                            variant="outline"
                            onClick={() => {
                                localStorage.removeItem("puzzle_stage");
                                localStorage.removeItem("puzzle_is_correct");
                                localStorage.removeItem("puzzle_attempts_left");
                                window.location.reload();
                            }}
                            className="text-primary-foreground hover:bg-primary-foreground/20"
                        >
                            Reset Puzzle
                        </Button>
                    )}
                    <div className="text-right">
                        <p className="text-2xl font-bold">{progressPercentage.toFixed(0)}%</p>
                        <p className="text-xs opacity-80">Terminé</p>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="max-w-6xl mx-auto p-6">
                {loading && <p>Chargement du puzzle...</p>}
                {error && <p className="text-red-500">{error}</p>}
                {!loading && !error && (
                    <div className="grid lg:grid-cols-3 gap-6">
                        {/* Puzzle Image */}
                        <div className="space-y-4 lg:col-span-2">
                            <Card className="p-6">
                                <h2 className="text-xl font-semibold mb-4">Image Mystère</h2>

                                <div className="relative aspect-square bg-gray-900 rounded-lg overflow-hidden">
                                    <img
                                        src={puzzleImage}
                                        alt="Puzzle"
                                        className="w-full h-full object-cover"
                                    />


                                </div>

                                <div className="mt-4">
                                    <div className="flex justify-between text-sm mb-2">
                                        <span className="text-muted-foreground">Progression</span>
                                        <span className="font-semibold">
                      {unlockedTiles.length} / {totalTiles} pièces
                    </span>
                                    </div>
                                    <Progress value={progressPercentage} className="h-3" />
                                </div>
                            </Card>
                        </div>

                        {/* Guessing Section */}
                        <div className="space-y-4">
                            <Card className="p-6">
                                <h2 className="text-xl font-semibold mb-2">Devinez le Cadeau Mystère</h2>
                                <p className="text-sm text-muted-foreground mb-4">
                                    Qu'est-ce qui est caché dans l'image ? Faites votre proposition !
                                </p>

                                {!isCorrect ? (
                                    <div className="space-y-3">
                                        <div className="flex gap-2">
                                            <Input
                                                placeholder="Entrez votre proposition..."
                                                value={guess}
                                                onChange={(e) => setGuess(e.target.value)}
                                                onKeyPress={(e) => e.key === "Enter" && handleGuess()}
                                                disabled={attemptsLeft === 0}
                                                className="flex-1"
                                            />
                                            <Button
                                                onClick={handleGuess}
                                                disabled={attemptsLeft === 0 || !guess.trim()}
                                                className="bg-primary hover:bg-primary/90 text-white"
                                            >
                                                <Search className="w-4 h-4 mr-2" />
                                                Deviner
                                            </Button>
                                        </div>

                                        <div className="flex items-center justify-between text-sm">
                                            <span className="text-muted-foreground">Tentatives restantes :</span>
                                            <span className={`font-bold ${attemptsLeft === 0 ? "text-destructive" : "text-primary"}`}>
                        {attemptsLeft} / 3
                      </span>
                                        </div>

                                        {attemptsLeft === 0 && (
                                            <p className="text-sm text-destructive text-center">
                                                Plus de tentatives ! Réessayez la semaine prochaine.
                                            </p>
                                        )}
                                    </div>
                                ) : (
                                    <div className="text-center py-6">
                                        <div className="text-6xl mb-4 animate-bounce">🎉</div>
                                        <h3 className="text-2xl font-bold mb-2">Félicitations !</h3>
                                        <p className="text-muted-foreground">
                                            Vous avez débloqué le cadeau mystère !
                                        </p>
                                    </div>
                                )}
                            </Card>

                            {/* Contributors */}
                            <Card className="p-6">
                                <div className="flex items-center gap-2 mb-4">
                                    <Users className="w-5 h-5 text-primary" />
                                    <h3 className="font-semibold">Top Contributeurs</h3>
                                </div>

                                <div className="space-y-3">
                                    {mockLeaderboard.employee_ranking?.map((contributor, index) => (
                                        <div
                                            key={contributor.user_id}
                                            className="flex items-center justify-between p-3 bg-secondary/50 rounded-lg"
                                        >
                                            <div className="flex items-center gap-3">
                                                <div className="w-10 h-10 rounded-full bg-primary flex items-center justify-center text-white font-bold">
                                                    {contributor.user.charAt(0)}
                                                </div>
                                                <div>
                                                    <p className="font-medium">{contributor.user}</p>
                                                    <p className="text-xs text-muted-foreground">
                                                        {contributor.pieces} pièces
                                                    </p>
                                                </div>
                                            </div>
                                            {index < 3 && (
                                                <div className={`rank-badge bg-primary/80 text-white`}>
                                                    {index + 1}
                                                </div>
                                            )}
                                        </div>
                                    ))}
                                </div>
                            </Card>

                            {/* Stats */}
                            <Card className="p-6 bg-primary/10">
                                <div className="flex items-center gap-2 mb-3">
                                    <TrendingUp className="w-5 h-5 text-primary" />
                                    <h3 className="font-semibold">L'impact de cette semaine</h3>
                                </div>
                                <div className="grid grid-cols-2 gap-4">
                                    <div className="text-center">
                                        <p className="text-3xl font-bold text-primary">
                                            {unlockedTiles.length}
                                        </p>
                                        <p className="text-xs text-muted-foreground">Pièces Débloquées</p>
                                    </div>
                                    <div className="text-center">
                                        <p className="text-3xl font-bold text-primary">
                                            {mockLeaderboard.employee_ranking?.length || 0}
                                        </p>
                                        <p className="text-xs text-muted-foreground">Contributeurs</p>
                                    </div>
                                </div>
                            </Card>
                        </div>
                    </div>
                )}
            </main>
        </div>
    );
};

export default Puzzle;