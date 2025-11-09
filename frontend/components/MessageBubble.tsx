/**
 * Message bubble component.
 */

import { Message } from '@/types';
import { cn } from '@/lib/utils';
import { formatTime } from '@/lib/utils';

interface MessageBubbleProps {
  message: Message;
  userName: string;
}

const agentColors: Record<string, string> = {
  Harry: 'bg-red-500',
  Hermione: 'bg-blue-500',
  Ron: 'bg-orange-500',
};

export function MessageBubble({ message, userName }: MessageBubbleProps) {
  const isUser = message.source === 'user';
  const isSystem = message.source === 'system';

  if (isSystem) {
    return (
      <div className="flex justify-center my-4 animate-slide-in">
        <div className="px-4 py-2 bg-yellow-50 border border-yellow-200 rounded-lg text-sm text-yellow-800 italic max-w-md text-center">
          {message.text}
        </div>
      </div>
    );
  }

  return (
    <div
      className={cn(
        'flex mb-4 animate-slide-in',
        isUser ? 'justify-end' : 'justify-start'
      )}
    >
      <div className={cn('max-w-[80%]', isUser && 'order-2')}>
        {!isUser && (
          <div className="flex items-center gap-2 mb-1">
            <div
              className={cn(
                'w-6 h-6 rounded-full',
                agentColors[message.sender] || 'bg-gray-400'
              )}
            />
            <span className="text-sm font-medium text-gray-700">
              {message.sender}
            </span>
            <span className="text-xs text-gray-400">
              {formatTime(message.timestamp)}
            </span>
          </div>
        )}

        <div
          className={cn(
            'px-4 py-3 rounded-2xl',
            isUser
              ? 'bg-gradient-primary text-white rounded-br-sm'
              : 'bg-white border border-gray-200 rounded-bl-sm'
          )}
        >
          <p className={cn('text-sm', isUser ? 'text-white' : 'text-gray-800')}>
            {message.text}
          </p>
        </div>

        {isUser && (
          <div className="flex justify-end mt-1">
            <span className="text-xs text-gray-400">
              {formatTime(message.timestamp)}
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
