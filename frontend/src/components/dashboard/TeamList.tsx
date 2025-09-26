import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Users, X, Github, Linkedin, GraduationCap, Mail } from "lucide-react";

export interface StartupInfo {
  name: string;
  product: string;
  founded: string;
  mission: string;
  businessModel: string;
  pitchDeck?: File;
  isManual: boolean;
}

export interface Prospect {
  id: string;
  name: string;
  email: string;
  github?: string;
  linkedin: string;
  university?: string;
  notes?: string;
}

interface TeamListProps {
  prospects: Prospect[];
  onRemoveProspect: (id: string) => void;
}

export function TeamList({ prospects, onRemoveProspect }: TeamListProps) {
  if (prospects.length === 0) {
    return (
      <Card className="shadow-hover glass-card animate-fade-in">
        <CardHeader className="bg-gradient-surface rounded-t-lg">
          <CardTitle className="flex items-center gap-3 text-xl">
            <div className="p-2 rounded-lg bg-gradient-primary shadow-accent">
              <Users className="h-5 w-5 text-primary-foreground" />
            </div>
            Team List
          </CardTitle>
        </CardHeader>
        <CardContent className="p-8">
          <div className="text-center py-12 text-muted-foreground">
            <div className="w-20 h-20 mx-auto mb-6 rounded-full bg-gradient-surface flex items-center justify-center shadow-card">
              <Users className="h-10 w-10 opacity-50" />
            </div>
            <p className="text-lg font-medium mb-2">No prospects added yet</p>
            <p className="text-sm">Add prospects above to start building your analysis team</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="shadow-hover glass-card animate-scale-in">
      <CardHeader className="bg-gradient-surface rounded-t-lg">
        <CardTitle className="flex items-center gap-3 text-xl">
          <div className="p-2 rounded-lg bg-gradient-success shadow-accent">
            <Users className="h-5 w-5 text-success-foreground" />
          </div>
          Team List ({prospects.length})
        </CardTitle>
      </CardHeader>
      <CardContent className="p-8">
        <div className="space-y-6">
          {prospects.map((prospect, index) => (
            <div 
              key={prospect.id} 
              className="flex items-start justify-between p-6 bg-gradient-glass rounded-xl border border-border/30 shadow-card hover:shadow-hover transition-all duration-300 hover:scale-102 animate-fade-in"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className="flex-1">
                <div className="mb-2">
                  <h4 className="font-medium text-foreground">{prospect.name}</h4>
                </div>
                
                <div className="flex items-center gap-4 text-sm text-muted-foreground">
                  <div className="flex items-center gap-1">
                    <Mail className="h-3 w-3" />
                    {prospect.email}
                  </div>
                  {prospect.university && (
                    <div className="flex items-center gap-1">
                      <GraduationCap className="h-3 w-3" />
                      {prospect.university}
                    </div>
                  )}
                  {prospect.github && (
                    <div className="flex items-center gap-1">
                      <Github className="h-3 w-3" />
                      GitHub
                    </div>
                  )}
                  {prospect.linkedin && (
                    <div className="flex items-center gap-1">
                      <Linkedin className="h-3 w-3" />
                      LinkedIn
                    </div>
                   )}
                 </div>
                
                {prospect.notes && (
                  <p className="text-sm text-muted-foreground mt-2 truncate">{prospect.notes}</p>
                )}
              </div>
              
              <Button
                variant="ghost"
                size="sm"
                onClick={() => onRemoveProspect(prospect.id)}
                className="text-destructive hover:text-destructive hover:bg-destructive/20 transition-all duration-300 hover:scale-[1.05] rounded-lg"
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}