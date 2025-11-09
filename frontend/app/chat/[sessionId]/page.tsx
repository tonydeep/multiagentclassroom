'use client';

import { useState, useEffect, useRef } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useWebSocket } from '@/hooks/useWebSocket';
import { AgentBadge } from '@/components/AgentBadge';
import { MessageBubble } from '@/components/MessageBubble';

export default function ChatPage() {
  const params = useParams();
  const router = useRouter();
  const sessionId = params.sessionId as string;

  const [userName, setUserName] = useState('Student');
  const [messageInput, setMessageInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const { isConnected, agentStatuses, messages, sendMessage } = useWebSocket(sessionId);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Handle send message
  function handleSendMessage() {
    const text = messageInput.trim();
    if (!text) return;

    sendMessage(userName, text);
    setMessageInput('');
  }

  // Handle key press
  function handleKeyPress(e: React.KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  }

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-primary text-white px-6 py-4 shadow-lg">
        <div className="max-w-6xl mx-auto">
          <div className="flex items-center justify-between mb-2">
            <h1 className="text-2xl font-bold">Multi-Agent Classroom</h1>
            <button
              onClick={() => router.push('/')}
              className="px-4 py-2 bg-white/20 hover:bg-white/30 rounded-lg transition-colors"
            >
              ← Quay lại
            </button>
          </div>
          <div className="flex items-center gap-3 text-sm">
            <span className="opacity-75">Session:</span>
            <code className="px-2 py-1 bg-white/20 rounded font-mono text-xs">
              {sessionId.substring(0, 8)}...
            </code>
            {isConnected ? (
              <span className="flex items-center gap-1">
                <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
                Connected
              </span>
            ) : (
              <span className="flex items-center gap-1">
                <span className="w-2 h-2 bg-red-400 rounded-full" />
                Disconnected
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Agent Status Bar */}
      <div className="bg-white border-b border-gray-200 px-6 py-3">
        <div className="max-w-6xl mx-auto flex gap-4">
          <AgentBadge name="Harry" status={agentStatuses.Harry} />
          <AgentBadge name="Hermione" status={agentStatuses.Hermione} />
          <AgentBadge name="Ron" status={agentStatuses.Ron} />
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-6 py-6">
        <div className="max-w-6xl mx-auto">
          {messages.length === 0 && (
            <div className="text-center text-gray-500 mt-12">
              <p className="text-lg mb-2">Chào mừng đến với lớp học!</p>
              <p>
                Ba trợ lý AI (Harry, Hermione, và Ron) sẽ giúp bạn giải bài toán.
              </p>
            </div>
          )}

          {messages.map((message) => (
            <MessageBubble
              key={message.id}
              message={message}
              userName={userName}
            />
          ))}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="bg-white border-t border-gray-200 px-6 py-4 shadow-lg">
        <div className="max-w-6xl mx-auto">
          <div className="flex gap-3">
            <input
              type="text"
              value={messageInput}
              onChange={(e) => setMessageInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Nhập câu hỏi hoặc ý kiến của bạn..."
              disabled={!isConnected}
              className="flex-1 px-4 py-3 border-2 border-gray-200 rounded-full focus:outline-none focus:border-primary-500 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            />
            <button
              onClick={handleSendMessage}
              disabled={!isConnected || !messageInput.trim()}
              className="px-8 py-3 bg-gradient-primary text-white font-semibold rounded-full shadow-lg hover:shadow-xl transform hover:scale-[1.05] transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
            >
              Gửi
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
