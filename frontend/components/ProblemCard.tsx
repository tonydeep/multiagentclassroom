/**
 * Problem card component for selection.
 */

import { Problem } from '@/types';
import { cn } from '@/lib/utils';

interface ProblemCardProps {
  problem: Problem;
  selected: boolean;
  onClick: () => void;
}

export function ProblemCard({ problem, selected, onClick }: ProblemCardProps) {
  return (
    <div
      onClick={onClick}
      className={cn(
        'p-6 rounded-xl border-2 cursor-pointer transition-all duration-200',
        'hover:scale-[1.02] hover:shadow-lg',
        selected
          ? 'border-primary-500 bg-primary-50 shadow-md'
          : 'border-gray-200 bg-white hover:border-primary-300'
      )}
    >
      <h3 className="text-xl font-semibold text-gray-900 mb-2">
        {problem.title}
      </h3>
      <p className="text-gray-600 whitespace-pre-line">
        {problem.problem}
      </p>
    </div>
  );
}
