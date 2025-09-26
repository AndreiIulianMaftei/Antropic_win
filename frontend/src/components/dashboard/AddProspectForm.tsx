import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { UserPlus, Github, Linkedin, Mail, GraduationCap } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { Prospect } from "./TeamList";

interface AddProspectFormProps {
  onAddProspect: (prospect: Prospect) => void;
}

const TOP_UNIVERSITIES = [
  "Harvard University", "Stanford University", "Massachusetts Institute of Technology",
  "Max Planck Institute for Molecular Genetics", "Universidade de São Paulo",
  "University of Cambridge", "University of Oxford", "California Institute of Technology",
  "University of Chicago", "Princeton University", "Yale University", "Columbia University",
  "University of Pennsylvania", "Cornell University", "University of California Berkeley",
  "University of California Los Angeles", "University of Michigan", "New York University",
  "London School of Economics", "Imperial College London", "University College London",
  "Carnegie Mellon University", "Northwestern University", "Johns Hopkins University",
  "Duke University", "University of Toronto", "University of Edinburgh", 
  "King's College London", "University of Melbourne", "University of Sydney",
  "Australian National University", "University of British Columbia", "McGill University",
  "University of Tokyo", "Kyoto University", "National University of Singapore",
  "Nanyang Technological University", "Peking University", "Tsinghua University",
  "ETH Zurich",
  "Sorbonne University", "Sciences Po", "Technical University of Munich",
  "University of Amsterdam", "Delft University of Technology", "KTH Royal Institute",
  "Stockholm School of Economics", "INSEAD", "London Business School", "IESE Business School"
];

export function AddProspectForm({ onAddProspect }: AddProspectFormProps) {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    github: "",
    linkedin: "",
    university: "",
    notes: "",
  });
  const { toast } = useToast();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const newProspect: Prospect = {
      id: Date.now().toString(),
      name: formData.name,
      email: formData.email,
      github: formData.github,
      linkedin: formData.linkedin,
      university: formData.university,
      notes: formData.notes,
    };
    
    onAddProspect(newProspect);
    
    toast({
      title: "Prospect Added",
      description: `${formData.name} has been added to your team list.`,
    });
    
    // Reset form
    setFormData({ name: "", email: "", github: "", linkedin: "", university: "", notes: "" });
  };

  return (
    <Card className="shadow-hover glass-card animate-scale-in">
      <CardHeader className="bg-gradient-surface rounded-t-lg">
        <CardTitle className="flex items-center gap-3 text-xl">
          <div className="p-2 rounded-lg bg-gradient-primary shadow-accent">
            <UserPlus className="h-5 w-5 text-primary-foreground" />
          </div>
          Add New Prospect
        </CardTitle>
      </CardHeader>
      <CardContent className="p-8">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Basic Information */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="name">Founder Name</Label>
              <Input
                id="name"
                placeholder="Enter founder's name"
                value={formData.name}
                onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="email" className="flex items-center gap-2">
                <Mail className="h-4 w-4" />
                Email
              </Label>
              <Input
                id="email"
                type="email"
                placeholder="founder@startup.com"
                value={formData.email}
                onChange={(e) => setFormData(prev => ({ ...prev, email: e.target.value }))}
                required
              />
            </div>
          </div>

          {/* University Selection */}
          <div className="space-y-2">
            <Label htmlFor="university" className="flex items-center gap-2">
              <GraduationCap className="h-4 w-4" />
              Affiliated University
            </Label>
            <Select value={formData.university} onValueChange={(value) => setFormData(prev => ({ ...prev, university: value }))}>
              <SelectTrigger>
                <SelectValue placeholder="Select a university" />
              </SelectTrigger>
              <SelectContent>
                {TOP_UNIVERSITIES.map((university) => (
                  <SelectItem key={university} value={university}>
                    {university}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Social Links */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="github" className="flex items-center gap-2">
                <Github className="h-4 w-4" />
                GitHub Profile
              </Label>
              <Input
                id="github"
                placeholder="https://github.com/username"
                value={formData.github}
                onChange={(e) => setFormData(prev => ({ ...prev, github: e.target.value }))}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="linkedin" className="flex items-center gap-2">
                <Linkedin className="h-4 w-4" />
                LinkedIn Profile
              </Label>
              <Input
                id="linkedin"
                placeholder="https://linkedin.com/in/username"
                value={formData.linkedin}
                onChange={(e) => setFormData(prev => ({ ...prev, linkedin: e.target.value }))}
                required
              />
            </div>
          </div>

          {/* Notes Field - Always Available */}
          <div className="space-y-2">
            <Label htmlFor="notes">Initial Notes</Label>
            <Textarea
              id="notes"
              placeholder="Add any initial observations or notes about the prospect..."
              value={formData.notes}
              onChange={(e) => setFormData(prev => ({ ...prev, notes: e.target.value }))}
              className="min-h-[100px]"
            />
          </div>
          
          <Button type="submit" className="w-full bg-gradient-primary hover:shadow-glow transition-all duration-500 transform hover:scale-[1.02] text-lg py-6 font-semibold">
            Add to Team List
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}