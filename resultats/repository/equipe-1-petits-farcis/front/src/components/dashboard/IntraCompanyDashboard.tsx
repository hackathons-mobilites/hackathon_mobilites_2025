import {CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis, PieChart, Pie, Cell, BarChart, Bar} from 'recharts';
import {Card, CardContent, CardHeader, CardTitle} from "@/components/ui/card";
import data from "@/data/mockIntraCompanyData.json";
import odData from "@/data/mockOD.json";
import DashboardMap from './DashboardMap';
import { encodePolyline } from "@/lib/polyline";

const RADIAN = Math.PI / 180;

const IntraCompanyDashboard = () => {
    const {
        co2SavedCurrentMonth,
        co2SavedTrend,
        modalShiftLastMonth,
        modalShiftCurrentMonth,
        bikeTripsThisMonth,
        intermodalTripsThisMonth,
        bikeDistanceThisMonth,
        modalShiftTrend
    } = data;
    const colors = {
        "Voiture": "hsl(var(--muted-foreground))",
        "TC": "hsl(var(--primary))",
        "Velo": "hsl(208, 65%, 75%)",
        "Mobilité Partagée": "hsl(var(--secondary-foreground))"
    };

    const pieChartColors = ["#88CCEE", "#CC6677", "#DDCC77", "#117733"]; // Softer, colorblind-friendly palette

    const modalShiftLastMonthData = Object.entries(modalShiftLastMonth).map(([name, value]) => ({
        name,
        value,
    }));

    const modalShiftCurrentMonthData = Object.entries(modalShiftCurrentMonth).map(([name, value]) => ({
        name,
        value,
    }));

    const formattedOdData = odData.map(item => ({
        name: item.name,
        trace: encodePolyline([item.origin, item.destination])
    }));

    const modeIcons: { [key: string]: string } = {
        "Voiture": "🚗",
        "TC": "🚌",
        "Velo": "🚲",
        "Mobilité Partagée": "🤝"
    };

    const renderCustomizedLegend = (props: any) => {
        const { payload } = props;

        return (
            <ul className="recharts-default-legend" style={{ padding: 0, margin: 0 }}>
                {payload.map((entry: any, index: number) => (
                    <li
                        key={`item-${index}`}
                        style={{ display: 'flex', alignItems: 'center', marginBottom: '4px' }}
                    >
                        <div
                            className="recharts-legend-icon"
                            style={{
                                width: '10px',
                                height: '10px',
                                borderRadius: '50%',
                                backgroundColor: entry.color,
                                marginRight: '8px',
                            }}
                        ></div>
                        <span>{entry.value}</span>
                    </li>
                ))}
            </ul>
        );
    };

    const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent }: any) => {
        const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
        const x = cx + radius * Math.cos(-midAngle * RADIAN);
        const y = cy + radius * Math.sin(-midAngle * RADIAN);

        return (
            <text x={x} y={y} fill="white" textAnchor={x > cx ? 'start' : 'end'} dominantBaseline="central">
                {`${(percent * 100).toFixed(0)}%`}
            </text>
        );
    };

    return (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3 bg-blue-50">


            <Card className="bg-transparent border">
                <CardHeader>
                    <CardTitle className="text-primary">Report Modal - Mois Dernier</CardTitle>
                </CardHeader>
                <CardContent>
                    <ResponsiveContainer width="100%" height={280}>
                        <PieChart>
                            <Pie
                                data={modalShiftLastMonthData}
                                cx="50%"
                                cy="55%"
                                outerRadius={90}
                                fill="#8884d8" // This will be updated in the next step
                                dataKey="value"
                                label={renderCustomizedLabel}
                                labelLine={false}
                            >
                                {modalShiftLastMonthData.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={pieChartColors[index % pieChartColors.length]}/>
                                ))}
                            </Pie>
                            <Tooltip
                                contentStyle={{
                                    backgroundColor: 'hsl(var(--card))',
                                    borderColor: 'hsl(var(--border))',
                                }}
                            />
                            <Legend content={renderCustomizedLegend}/>
                        </PieChart>
                    </ResponsiveContainer>
                </CardContent>
            </Card>

            <Card className="bg-transparent border">
                <CardHeader>
                    <CardTitle className="text-primary">Report Modal - Mois Actuel</CardTitle>
                </CardHeader>
                <CardContent>
                    <ResponsiveContainer width="100%" height={280}>
                        <PieChart>
                            <Pie
                                data={modalShiftCurrentMonthData}
                                cx="50%"
                                cy="55%"
                                outerRadius={90}
                                fill={pieChartColors[0]}
                                dataKey="value"
                                label={renderCustomizedLabel}
                                labelLine={false}
                            >
                                {modalShiftCurrentMonthData.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={pieChartColors[index % pieChartColors.length]}/>
                                ))}
                            </Pie>
                            <Tooltip
                                contentStyle={{
                                    backgroundColor: 'hsl(var(--card))',
                                    borderColor: 'hsl(var(--border))',
                                }}
                            />
                            <Legend content={renderCustomizedLegend}/>
                        </PieChart>
                    </ResponsiveContainer>
                </CardContent>
            </Card>

            <Card className="bg-transparent border">
                <CardHeader>
                    <CardTitle className="text-primary">Chiffres Clés</CardTitle>
                </CardHeader>
                <CardContent className="flex flex-col">
                    <div className="flex flex-wrap items-baseline mb-2">
                        <p className="text-xl font-semibold">CO2 Sauvé ce mois-ci: </p>
                        <p className="text-3xl font-bold text-primary">{co2SavedCurrentMonth} kg</p>
                    </div>
                    <div className="flex flex-wrap items-baseline mb-2">
                        <p className="text-xl font-semibold">Nombre de trajets Vélo: </p>
                        <p className="text-3xl font-bold text-primary">{bikeTripsThisMonth}</p>
                    </div>
                    <div className="flex flex-wrap items-baseline mb-2">
                        <p className="text-xl font-semibold">Nombre de trajets Intermodaux: </p>
                        <p className="text-3xl font-bold text-primary">{intermodalTripsThisMonth}</p>
                    </div>
                    <div className="flex flex-wrap items-baseline">
                        <p className="text-xl font-semibold">Distance Vélo ce mois-ci: </p>
                        <p className="text-3xl font-bold text-primary">{bikeDistanceThisMonth} km</p>
                    </div>
                </CardContent>
            </Card>

            <Card className="col-span-3 bg-transparent border">
                <CardHeader>
                    <CardTitle className="text-primary">Tendance CO2 Sauvé</CardTitle>
                </CardHeader>
                <CardContent>
                    <ResponsiveContainer width="100%" height={250}>
                        <BarChart data={co2SavedTrend}>
                            <CartesianGrid strokeDasharray="3 3"/>
                            <XAxis dataKey="month"/>
                            <YAxis/>
                            <Tooltip
                                contentStyle={{
                                    backgroundColor: 'hsl(var(--card))',
                                    borderColor: 'hsl(var(--border))',
                                }}
                            />
                            <Legend/>
                            <Bar dataKey="co2Saved" fill="#66BB66"/>
                        </BarChart>
                    </ResponsiveContainer>
                </CardContent>
            </Card>

            

            

                                    <Card className="col-span-3 bg-transparent border flex flex-col min-h-[400px]">

            

            

                                        <CardHeader>

            

            

                                            <CardTitle className="text-primary">OD des Utilisateurs</CardTitle>

            

            

                                        </CardHeader>

            

            

                                        <CardContent className="flex-1">

            

            

                                            <DashboardMap traces={formattedOdData}/>

            

            

                                        </CardContent>

            

            

                                    </Card>
        </div>
    );
};

export default IntraCompanyDashboard;