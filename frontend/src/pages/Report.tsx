import { useLocation, useNavigate } from "react-router-dom";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { ArrowLeft, TrendingUp, Users, Zap, BookOpen, Star, MessageSquare } from "lucide-react";

interface FounderHighlight {
  name: string;
  highlights: string[];
  comments?: string;
}

interface InterviewHighlight {
  question: string;
  summary: string;
  keyInsights: string[];
  score: number;
  person: string;
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
  interviewHighlights: InterviewHighlight[];
}

const Report = () => {
  const location = useLocation();
  const navigate = useNavigate();
  
  // Get analysis result from navigation state or use mock data
  const analysisResultNoType = location.state?.analysisResult;

  const analysisResult: AnalysisResult = analysisResultNoType;

  console.log("AnalysisResult is", analysisResult);

  const getScoreColor = (score: number) => {
    if (score >= 8) return "text-green-600";
    if (score >= 6) return "text-yellow-600";
    return "text-red-600";
  };

  const getScoreBadgeVariant = (score: number) => {
    if (score >= 8) return "default";
    if (score >= 6) return "secondary";
    return "destructive";
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
              <h1 className="text-2xl font-bold">Analysis Report</h1>
              <p className="text-muted-foreground">AI-powered team evaluation results</p>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Overall Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="glass-card">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium flex items-center gap-2">
                <Star className="h-4 w-4 text-primary" />
                Overall Score
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-baseline gap-2">
                <span className={`text-3xl font-bold ${getScoreColor(analysisResult.overallScore)}`}>
                  {analysisResult.overallScore}
                </span>
                <span className="text-muted-foreground">/10</span>
              </div>
              <Progress value={analysisResult.overallScore * 10} className="mt-2" />
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

          <Card className="glass-card">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium flex items-center gap-2">
                <Users className="h-4 w-4 text-primary" />
                Team Synergy
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-baseline gap-2">
                <span className={`text-3xl font-bold ${getScoreColor(analysisResult.teamSynergy)}`}>
                  {analysisResult.teamSynergy}
                </span>
                <span className="text-muted-foreground">/10</span>
              </div>
              <Progress value={analysisResult.teamSynergy * 10} className="mt-2" />
            </CardContent>
          </Card>

          <Card className="glass-card">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium flex items-center gap-2">
                <TrendingUp className="h-4 w-4 text-primary" />
                Complementary Score
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-baseline gap-2">
                <span className={`text-3xl font-bold ${getScoreColor(analysisResult.complementaryScore)}`}>
                  {analysisResult.complementaryScore}
                </span>
                <span className="text-muted-foreground">/10</span>
              </div>
              <Progress value={analysisResult.complementaryScore * 10} className="mt-2" />
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

        {/* Interview Highlights */}
        <Card className="glass-card mt-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <MessageSquare className="h-5 w-5 text-primary" />
              Interview Highlights
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              {analysisResult.interviewHighlights.map((interview, index) => (
                <div key={index} className="border rounded-lg p-6 bg-card/50">
                  <div className="flex items-start justify-between mb-4">
                    <h3 className="text-lg font-semibold text-foreground flex-1">
                      {interview.question}
                    </h3>
                    <div className="flex items-center gap-2 ml-4">
                      <Badge variant="outline">{interview.person}</Badge>
                      <Badge variant={getScoreBadgeVariant(interview.score)}>
                        {interview.score}/10
                      </Badge>
                    </div>
                  </div>
                  
                  <div className="space-y-3">
                    <div>
                      <h4 className="text-sm font-medium text-muted-foreground mb-2">Summary</h4>
                      <p className="text-sm bg-accent/50 rounded-lg p-3 border">
                        {interview.summary}
                      </p>
                    </div>
                    
                    <div>
                      <h4 className="text-sm font-medium text-muted-foreground mb-2">Key Insights</h4>
                      <ul className="space-y-1">
                        {interview.keyInsights.map((insight, insightIndex) => (
                          <li key={insightIndex} className="flex items-start gap-2">
                            <div className="w-1.5 h-1.5 rounded-full bg-primary mt-2 flex-shrink-0" />
                            <span className="text-sm">{insight}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  );
};

export default Report;