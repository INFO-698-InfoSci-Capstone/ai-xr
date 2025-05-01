import React from 'react';
import { DivideIcon as LucideIcon } from 'lucide-react';

interface Step {
  title: string;
  icon: LucideIcon;
}

interface ProgressBarProps {
  steps: Step[];
  currentStep: number;
}

const ProgressBar: React.FC<ProgressBarProps> = ({ steps, currentStep }) => {
  return (
    <div className="w-full">
      <div className="flex items-center justify-between">
        {steps.map((step, index) => {
          const Icon = step.icon;
          const isActive = index <= currentStep;
          const isCompleted = index < currentStep;

          return (
            <React.Fragment key={step.title}>
              <div className="flex flex-col items-center">
                <div
                  className={`w-12 h-12 rounded-full flex items-center justify-center transition-all duration-200 ${
                    isActive
                      ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white'
                      : 'bg-white/10 text-white/40'
                  }`}
                >
                  <Icon className="h-6 w-6" />
                </div>
                <p
                  className={`mt-3 text-sm transition-colors duration-200 ${
                    isActive ? 'text-white' : 'text-white/40'
                  }`}
                >
                  {step.title}
                </p>
              </div>
              {index < steps.length - 1 && (
                <div
                  className={`flex-1 h-0.5 mx-4 transition-colors duration-200 ${
                    isCompleted ? 'bg-gradient-to-r from-purple-600 to-pink-600' : 'bg-white/10'
                  }`}
                />
              )}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
};

export default ProgressBar;