import { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Switch } from "@/components/ui/switch";
import { Building2, Upload, FileText } from "lucide-react";
import { StartupInfo } from "./TeamList";

interface StartupInfoModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSave: (startupInfo: StartupInfo) => void;
  initialData?: StartupInfo;
}

export function StartupInfoModal({ open, onOpenChange, onSave, initialData }: StartupInfoModalProps) {
  const [formData, setFormData] = useState<StartupInfo>(
    initialData || {
      name: "",
      product: "",
      founded: "",
      mission: "",
      businessModel: "",
      isManual: true,
    }
  );
  const [pitchDeck, setPitchDeck] = useState<File | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const finalData = { ...formData };
    if (pitchDeck && !formData.isManual) {
      finalData.pitchDeck = pitchDeck;
    }
    onSave(finalData);
    onOpenChange(false);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setPitchDeck(file);
    }
  };

  const questions = [
    {
      key: "name" as keyof StartupInfo,
      label: "Startup Name",
      question: "Startup name:",
    },
    {
      key: "product" as keyof StartupInfo,
      label: "Product or Service",
      question: "What product or service does the startup offer?",
    },
    {
      key: "founded" as keyof StartupInfo,
      label: "Founded",
      question: "When and where was the startup founded?",
    },
    {
      key: "mission" as keyof StartupInfo,
      label: "Mission",
      question: "What is the startup's mission or main goal?",
    },
    {
      key: "businessModel" as keyof StartupInfo,
      label: "Business Model",
      question: "What is the startup's business model or how does it make money?",
    },
  ];

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-3xl max-h-[85vh] overflow-y-auto bg-card border border-border shadow-hover animate-scale-in">
        <DialogHeader className="pb-6">
          <DialogTitle className="flex items-center gap-3 text-2xl">
            <div className="p-2 rounded-lg bg-gradient-primary shadow-accent">
              <Building2 className="h-6 w-6 text-primary-foreground" />
            </div>
            Startup Information
          </DialogTitle>
        </DialogHeader>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Toggle between Upload and Manual */}
          <div className="space-y-4">
            <Label className="text-sm font-medium">Information Method</Label>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <Upload className="h-4 w-4" />
                <span className="text-sm">Upload Pitchdeck</span>
                <Switch
                  checked={formData.isManual}
                  onCheckedChange={(checked) => setFormData(prev => ({ ...prev, isManual: checked }))}
                />
                <span className="text-sm">Manual Entry</span>
                <FileText className="h-4 w-4" />
              </div>
            </div>
          </div>

          {/* File Upload Section */}
          {!formData.isManual && (
            <div className="space-y-2">
              <Label htmlFor="pitchDeck" className="text-sm font-medium">
                Upload Pitch Deck
              </Label>
              <Input
                id="pitchDeck"
                type="file"
                accept=".pdf,.ppt,.pptx"
                onChange={handleFileChange}
                className="cursor-pointer"
              />
              <p className="text-xs text-muted-foreground">
                Supported formats: PDF, PPT, PPTX
              </p>
              {pitchDeck && (
                <p className="text-sm text-primary">
                  ✓ {pitchDeck.name} selected
                </p>
              )}
            </div>
          )}

          {/* Manual Entry Section */}
          {formData.isManual && (
            <>
              {questions.map((q) => (
                <div key={q.key} className="space-y-2">
                  <Label htmlFor={q.key} className="text-sm font-medium">
                    {q.label}
                  </Label>
                  <p className="text-sm text-muted-foreground mb-2">{q.question}</p>
                   {q.key === "name" ? (
                    <Input
                      id={q.key}
                      placeholder={`Enter ${q.label.toLowerCase()}...`}
                      value={formData[q.key] as string}
                      onChange={(e) => setFormData(prev => ({ ...prev, [q.key]: e.target.value }))}
                      required
                    />
                  ) : (
                    <Textarea
                      id={q.key}
                      placeholder={`Enter ${q.label.toLowerCase()}...`}
                      value={formData[q.key] as string}
                      onChange={(e) => setFormData(prev => ({ ...prev, [q.key]: e.target.value }))}
                      className="min-h-[80px]"
                      required
                    />
                  )}
                </div>
              ))}
            </>
          )}
          
          <div className="flex gap-4 pt-6">
            <Button type="submit" className="flex-1 bg-gradient-primary hover:shadow-glow transition-all duration-300 hover:scale-[1.02] py-6 text-lg font-semibold">
              Save Startup Information
            </Button>
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)} className="hover:shadow-accent transition-all duration-300 hover:scale-[1.02] py-6 px-8">
              Cancel
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}