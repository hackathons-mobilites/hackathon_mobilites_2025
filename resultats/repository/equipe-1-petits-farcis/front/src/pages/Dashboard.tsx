import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import IntraCompanyDashboard from "@/components/dashboard/IntraCompanyDashboard";
import InterCompanyDashboard from "@/components/dashboard/InterCompanyDashboard";

const DashboardPage = () => {
  return (
    <div className="container mx-auto p-4 bg-secondary/50 min-h-screen">
      <h1 className="text-3xl font-bold mb-4 text-primary">Tableaux de Bord de Mobilité</h1>
      <Tabs defaultValue="intra-company">
        <TabsList>
          <TabsTrigger value="intra-company">Intra-entreprise</TabsTrigger>
          <TabsTrigger value="inter-company">Inter-entreprises</TabsTrigger>
        </TabsList>
        <TabsContent value="intra-company">
          <IntraCompanyDashboard />
        </TabsContent>
        <TabsContent value="inter-company">
          <InterCompanyDashboard />
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default DashboardPage;
