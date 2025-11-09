/**
 * Agent status badge component.
 */

import { AgentStatus } from '@/types';
import { cn } from '@/lib/utils';

interface AgentBadgeProps {
  name: string;
  status: AgentStatus;
}

const agentColors: Record<string, string> = {
  Harry: 'bg-red-500',
  Hermione: 'bg-blue-500',
  Ron: 'bg-orange-500',
};

export function AgentBadge({ name, status }: AgentBadgeProps) {
  const color = agentColors[name] || 'bg-gray-500';

  return (
    <div className="flex items-center gap-2 px-4 py-2 bg-white rounded-full shadow-sm">
      <div
        className={cn(
          'w-3 h-3 rounded-full',
          status === 'idle' && 'bg-gray-400',
          status === 'thinking' && 'bg-yellow-400 animate-pulse-slow',
          status === 'typing' && 'bg-green-500 animate-pulse-slow'
        )}
      />
      <span className="text-sm font-medium text-gray-700">{name}</span>
    </div>
  );
}
