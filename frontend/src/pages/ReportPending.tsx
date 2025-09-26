import { useLocation, useNavigate } from "react-router-dom";
import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { ArrowLeft, TrendingUp, Users, Zap, BookOpen, Star, MessageSquare, Clock, Loader2 } from "lucide-react";

interface FounderHighlight {
  name: string;
  highlights: string[];
  comments?: string;
}

interface AnalysisResult {
  overallScore: number;
  disruptionProbability: number;
  teamSynergy: number;
  complementaryScore: number;
  researchDepth: {
    hIndex: number;
  };
  founderHighlights: FounderHighlight[];
}

const ReportPending = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  
  // Get analysis result from navigation state
  const analysisResultNoType = location.state?.analysisResult;
  const analysisResult: AnalysisResult = analysisResultNoType;

  const handleRefreshInterview = () => {
    setIsLoading(true);
    setTimeout(() => {
      navigate("/reportDone", { state: { analysisResult } });
    }, 9000); // 9 second delay
  };

  const getScoreColor = (score: number) => {
    if (score >= 8) return "text-green-600";
    if (score >= 6) return "text-yellow-600";
    return "text-red-600";
  };

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b bg-card/50 backdrop-blur">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center gap-4">
            <Button 
              variant="ghost" 
              onClick={() => navigate("/")}
              className="gap-2"
            >
              <ArrowLeft className="h-4 w-4" />
              Back to Dashboard
            </Button>
            <div>
              <h1 className="text-2xl font-bold">Analysis Report - In Progress</h1>
              <p className="text-muted-foreground">AI-powered team evaluation results</p>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Overall Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {/* Overall Score - Blurred */}
          <Card className="glass-card relative">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium flex items-center gap-2">
                <Star className="h-4 w-4 text-primary" />
                Overall Score
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="blur-sm">
                <div className="flex items-baseline gap-2">
                  <span className="text-3xl font-bold text-muted-foreground">
                    {analysisResult.overallScore}
                  </span>
                  <span className="text-muted-foreground">/10</span>
                </div>
                <Progress value={analysisResult.overallScore * 10} className="mt-2" />
              </div>
              <div className="absolute inset-0 flex items-center justify-center">
                <Badge variant="secondary" className="bg-background/80 backdrop-blur">
                  <Clock className="h-3 w-3 mr-1" />
                  Pending
                </Badge>
              </div>
            </CardContent>
          </Card>

          <Card className="glass-card">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium flex items-center gap-2">
                <Zap className="h-4 w-4 text-primary" />
                Disruption Probability
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-baseline gap-2">
                <span className={`text-3xl font-bold ${getScoreColor(analysisResult.disruptionProbability)}`}>
                  {analysisResult.disruptionProbability}
                </span>
                <span className="text-muted-foreground">/10</span>
              </div>
              <Progress value={analysisResult.disruptionProbability * 10} className="mt-2" />
            </CardContent>
          </Card>

          {/* Team Synergy - Blurred */}
          <Card className="glass-card relative">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium flex items-center gap-2">
                <Users className="h-4 w-4 text-primary" />
                Team Synergy
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="blur-sm">
                <div className="flex items-baseline gap-2">
                  <span className="text-3xl font-bold text-muted-foreground">
                    {analysisResult.teamSynergy}
                  </span>
                  <span className="text-muted-foreground">/10</span>
                </div>
                <Progress value={analysisResult.teamSynergy * 10} className="mt-2" />
              </div>
              <div className="absolute inset-0 flex items-center justify-center">
                <Badge variant="secondary" className="bg-background/80 backdrop-blur">
                  <Clock className="h-3 w-3 mr-1" />
                  Pending
                </Badge>
              </div>
            </CardContent>
          </Card>

          {/* Complementary Score - Blurred */}
          <Card className="glass-card relative">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium flex items-center gap-2">
                <TrendingUp className="h-4 w-4 text-primary" />
                Complementary Score
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="blur-sm">
                <div className="flex items-baseline gap-2">
                  <span className="text-3xl font-bold text-muted-foreground">
                    {analysisResult.complementaryScore}
                  </span>
                  <span className="text-muted-foreground">/10</span>
                </div>
                <Progress value={analysisResult.complementaryScore * 10} className="mt-2" />
              </div>
              <div className="absolute inset-0 flex items-center justify-center">
                <Badge variant="secondary" className="bg-background/80 backdrop-blur">
                  <Clock className="h-3 w-3 mr-1" />
                  Pending
                </Badge>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Research Depth */}
        <Card className="glass-card mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BookOpen className="h-5 w-5 text-primary" />
              Research Depth
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-4">
              <div>
                <div className="text-sm text-muted-foreground">H-Index</div>
                <div className="text-4xl font-bold text-primary">{analysisResult.researchDepth.hIndex}</div>
              </div>
              <div className="text-sm text-muted-foreground">
                The H-Index measures the productivity and citation impact of the team's published work.
                A higher H-Index indicates more influential research contributions.
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Founder Highlights */}
        <Card className="glass-card">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Users className="h-5 w-5 text-primary" />
              Founder Highlights
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              {analysisResult.founderHighlights.map((founder, index) => (
                <div key={index} className="border rounded-lg p-6 bg-card/50">
                  <div className="flex items-center gap-2 mb-4">
                    <h3 className="text-lg font-semibold">{founder.name}</h3>
                    <Badge variant="secondary">Founder</Badge>
                  </div>
                  
                  <div className="space-y-3">
                    <div>
                      <h4 className="text-sm font-medium text-muted-foreground mb-2">Key Highlights</h4>
                      <ul className="space-y-1">
                        {founder.highlights.map((highlight, hIndex) => (
                          <li key={hIndex} className="flex items-start gap-2">
                            <div className="w-1.5 h-1.5 rounded-full bg-primary mt-2 flex-shrink-0" />
                            <span className="text-sm">{highlight}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                    
                    {founder.comments && (
                      <div>
                        <h4 className="text-sm font-medium text-muted-foreground mb-2">Analysis Comments</h4>
                        <p className="text-sm bg-accent/50 rounded-lg p-3 border">
                          {founder.comments}
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Interview Highlights - Pending State */}
        <Card className="glass-card mt-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <MessageSquare className="h-5 w-5 text-primary" />
              Interview Highlights
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-center py-12">
              <Clock className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">Interviews for each Team Member are still being conducted</h3>
              <p className="text-muted-foreground mb-6">
                Our AI is currently conducting detailed interviews with each team member. 
                This process will provide insights into team dynamics, leadership qualities, and strategic thinking.
              </p>
              <Button 
                onClick={handleRefreshInterview}
                disabled={isLoading}
                className="gap-2"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Processing Interviews...
                  </>
                ) : (
                  <>
                    <MessageSquare className="h-4 w-4" />
                    Refresh Interview Results
                  </>
                )}
              </Button>
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  );
};

export default ReportPending;