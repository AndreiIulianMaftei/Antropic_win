import { useState } from "react";
import { DashboardHeader } from "@/components/dashboard/Header";
import { StartupInfoSection } from "@/components/dashboard/StartupInfoSection";
import { AddProspectForm } from "@/components/dashboard/AddProspectForm";
import { AnalysisButton } from "@/components/dashboard/AnalysisButton";
import { TeamList, Prospect, StartupInfo } from "@/components/dashboard/TeamList";

const Index = () => {
  const [prospects, setProspects] = useState<Prospect[]>([
    {
      id: "1",
      name: "Sarah Chen",
      email: "sarah.chen@email.com",
      github: "https://github.com/sarahchen",
      linkedin: "https://linkedin.com/in/sarahchen",
      university: "Stanford University",
      notes: "AI/ML expert with 5 years experience at Google"
    },
    {
      id: "2", 
      name: "Marcus Rodriguez",
      email: "marcus.r@email.com",
      github: "https://github.com/marcusr",
      linkedin: "https://linkedin.com/in/marcusrodriguez",
      university: "MIT",
      notes: "Full-stack engineer, previously at Meta"
    }
  ]);
  const [startupInfo, setStartupInfo] = useState<StartupInfo | undefined>({
    name: "TechFlow",
    product: "AI-powered workflow automation platform",
    founded: "2024",
    mission: "Streamline business processes using intelligent automation",
    businessModel: "SaaS subscription model targeting enterprise clients",
    isManual: true
  });

  const handleAddProspect = (prospect: Prospect) => {
    setProspects(prev => [...prev, prospect]);
  };

  const handleRemoveProspect = (id: string) => {
    setProspects(prev => prev.filter(p => p.id !== id));
  };

  const handleStartupInfoSave = (info: StartupInfo) => {
    setStartupInfo(info);
  };

  return (
    <div className="min-h-screen bg-background">
      <DashboardHeader />
      
      <main className="max-w-7xl mx-auto px-6 py-8">
        <div className="mb-8">
          <StartupInfoSection onStartupInfoSave={handleStartupInfoSave} />
        </div>
        
        <div className="mb-8">
          <AddProspectForm onAddProspect={handleAddProspect} />
        </div>
        
        <div className="mb-8">
          <TeamList prospects={prospects} onRemoveProspect={handleRemoveProspect} />
        </div>
        
        <div>
          <AnalysisButton startupInfo={startupInfo} prospects={prospects} hasProspects={prospects.length > 0} />
        </div>
      </main>
    </div>
  );
};

export default Index;
