import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import data from "@/data/mockInterCompanyData.json";

const InterCompanyDashboard = () => {
  const { emissionsComparison, modalShareComparison } = data;

  const companies = Object.keys(modalShareComparison[0]).filter(key => key !== 'mode');
  const colors = ["hsl(var(--primary))", "hsl(208, 65%, 75%))", "hsl(208, 65%, 35%))", "hsl(var(--secondary-foreground))", "hsl(var(--muted-foreground))"];

  return (
    <div className="grid gap-4 md:grid-cols-1 lg:grid-cols-2">
      <Card className="col-span-1 bg-transparent border">
        <CardHeader>
          <CardTitle className="text-primary">Comparaison des Émissions de CO2 (kg CO2)</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={emissionsComparison}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="company" />
              <YAxis />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'hsl(var(--card))',
                  borderColor: 'hsl(var(--border))',
                }}
              />
              <Legend />
              <Bar dataKey="co2" fill="hsl(var(--primary))" name="Émissions de CO2" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      <Card className="col-span-1 bg-transparent border">
        <CardHeader>
          <CardTitle className="text-primary">Comparaison de la Part Modale (%)</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={modalShareComparison} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis type="category" dataKey="mode" width={110} />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'hsl(var(--card))',
                  borderColor: 'hsl(var(--border))',
                }}
              />
              <Legend />
              {companies.map((company, index) => (
                <Bar key={company} dataKey={company} stackId="a" fill={colors[index % colors.length]} name={company} />
              ))}
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  );
};

export default InterCompanyDashboard;