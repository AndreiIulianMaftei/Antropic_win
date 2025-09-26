import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Building2, CheckCircle } from "lucide-react";
import { StartupInfoModal } from "./StartupInfoModal";
import { StartupInfo } from "./TeamList";
import { useToast } from "@/hooks/use-toast";

interface StartupInfoSectionProps {
  onStartupInfoSave: (info: StartupInfo) => void;
}

export function StartupInfoSection({ onStartupInfoSave }: StartupInfoSectionProps) {
  const [startupInfo, setStartupInfo] = useState<StartupInfo | undefined>(undefined);
  const [showStartupModal, setShowStartupModal] = useState(false);
  const { toast } = useToast();

  const handleStartupInfoSave = (info: StartupInfo) => {
    setStartupInfo(info);
    onStartupInfoSave(info);
    toast({
      title: "Startup Information Saved",
      description: "Your startup details have been saved successfully.",
    });
  };

  return (
    <Card className="shadow-hover glass-card animate-fade-in">
      <CardHeader className="bg-gradient-surface rounded-t-lg">
        <CardTitle className="flex items-center gap-3 text-xl">
          <div className="p-2 rounded-lg bg-gradient-primary shadow-accent">
            <Building2 className="h-5 w-5 text-primary-foreground" />
          </div>
          Startup Information
        </CardTitle>
      </CardHeader>
      <CardContent className="p-8">
        <div className="space-y-4">
          <p className="text-sm text-muted-foreground">
            Add your startup's basic information to enhance the analysis quality for all prospects.
          </p>
          
          <div className="flex items-center gap-4">
            <Button
              variant={startupInfo ? "outline" : "default"}
              onClick={() => setShowStartupModal(true)}
              className={`flex-1 transition-all duration-300 ${startupInfo ? 'hover:shadow-accent hover:scale-[1.02]' : 'bg-gradient-primary hover:shadow-glow hover:scale-[1.02]'} py-6 text-lg font-semibold`}
            >
              {startupInfo ? "Edit Startup Information" : "Add Startup Information"}
            </Button>
            
            {startupInfo && (
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <CheckCircle className="h-4 w-4 text-green-600" />
                <span>Information saved</span>
              </div>
            )}
          </div>

          {startupInfo && (
            <div className="bg-gradient-glass rounded-xl p-6 space-y-3 border border-border/30 shadow-card animate-scale-in">
              <h4 className="font-semibold text-lg text-foreground">{startupInfo.name || "Startup Name"}</h4>
              <p className="text-sm text-muted-foreground line-clamp-3 leading-relaxed">
                {startupInfo.mission || "Mission statement..."}
              </p>
            </div>
          )}
        </div>

        <StartupInfoModal
          open={showStartupModal}
          onOpenChange={setShowStartupModal}
          onSave={handleStartupInfoSave}
          initialData={startupInfo}
        />
      </CardContent>
    </Card>
  );
}