import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Brain } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { useNavigate } from "react-router-dom";
import { StartupInfo, Prospect } from "./TeamList";

interface PredictionPanelProps {
  startupInfo: StartupInfo,
  prospects: Prospect[],
  hasProspects: boolean,
}

export function AnalysisButton({ startupInfo, prospects, hasProspects }: PredictionPanelProps) {
  const { toast } = useToast();
  const navigate = useNavigate();


  const startPrediction = async () => {
    toast({
      title: "Starting Fetch",
      description: ""
    });
    
    try {
      const response = await fetch('http://127.0.0.1:8000/api/analyse', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'  // Added this header
        },
        body: JSON.stringify({
          data: {
            startupInfo: startupInfo,
            teamList: prospects
          }
        })
      });

      if (response.ok) {
        const result = await response.json();
        console.log('Success:', result);
        
        toast({
          title: "Analysis Complete",
          description: "Redirecting to report..."
        });
        
        // Navigate to report page with results
        console.log(JSON.stringify(result));
        navigate("/ReportPending", { state: { analysisResult: result } });
      }

    } catch (e) {
      console.log(e);
    }
  };

  return <div className="space-y-6">
    <Card className="shadow-hover glass-card animate-scale-in relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0 bg-gradient-to-br from-accent/5 via-transparent to-primary/5"></div>

      <CardContent className="p-8 relative">
        <div className="text-center mb-6">
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-primary shadow-glow flex items-center justify-center animate-glow">
            <Brain className="h-8 w-8 text-primary-foreground" />
          </div>
          <h3 className="text-xl font-semibold mb-2">AI-Powered Analysis</h3>
          <p className="text-muted-foreground">Launch intelligent research on your prospect team</p>
        </div>

        <Button
          onClick={startPrediction}
          disabled={!hasProspects}
          className={`w-full transition-all duration-500 py-8 text-xl font-bold ${hasProspects
              ? 'bg-gradient-hero hover:shadow-glow hover:scale-[1.02] animate-glow'
              : 'opacity-50 cursor-not-allowed'
            }`}
        >
          <Brain className="h-6 w-6 mr-3" />
          {hasProspects ? "Start Smart Analysis" : "Add Team Members First"}
        </Button>
      </CardContent>
    </Card>
  </div>;
}