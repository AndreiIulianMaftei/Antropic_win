import { Target } from "lucide-react";
import logoImage from "@/assets/logo.png";
export function DashboardHeader() {
  return <header className="bg-gradient-hero text-primary-foreground shadow-glass relative overflow-hidden animate-fade-in">
      {/* Background decoration */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent -skew-y-1 transform origin-top-left"></div>
      
      <div className="max-w-7xl mx-auto px-6 py-12 relative">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-6">
            <div className="w-16 h-16 rounded-xl bg-white/15 backdrop-blur-sm p-1 shadow-glow animate-glow flex items-center justify-center">
              <img
                src={logoImage}
                alt="Unicorn Radar Logo"
                className="w-full h-full object-contain rounded-lg"
              />
            </div>
            <div className="animate-slide-up">
              <h1 className="text-4xl font-bold tracking-tight mb-2 bg-gradient-to-r from-white to-white/90 bg-clip-text text-transparent drop-shadow-sm">
                Unicorn Radar
              </h1>
              <p className="text-primary-foreground/90 text-base font-medium">
                VC Investment Intelligence Platform
              </p>
            </div>
          </div>
        </div>
      </div>
    </header>;
}