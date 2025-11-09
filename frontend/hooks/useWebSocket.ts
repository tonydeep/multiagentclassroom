/**
 * React hook for WebSocket communication.
 */

import { useEffect, useRef, useState, useCallback } from 'react';
import { WebSocketManager } from '@/lib/websocket';
import type { WebSocketMessage, AgentStatus, Message } from '@/types';

export function useWebSocket(sessionId: string | null) {
  const wsRef = useRef<WebSocketManager | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [agentStatuses, setAgentStatuses] = useState<Record<string, AgentStatus>>({
    Harry: 'idle',
    Hermione: 'idle',
    Ron: 'idle',
  });
  const [messages, setMessages] = useState<Message[]>([]);

  // Initialize WebSocket
  useEffect(() => {
    if (!sessionId) return;

    const ws = new WebSocketManager(sessionId);
    wsRef.current = ws;

    // Connect
    ws.connect();

    // Handle messages
    const unsubscribe = ws.onMessage((message: WebSocketMessage) => {
      switch (message.type) {
        case 'connected':
          setIsConnected(true);
          break;

        case 'agent_status':
          const { agent_name, status } = message.data;
          setAgentStatuses(prev => ({
            ...prev,
            [agent_name]: status,
          }));
          break;

        case 'new_message':
          const { source, content } = message.data;
          setMessages(prev => [
            ...prev,
            {
              id: `${Date.now()}-${Math.random()}`,
              sender: content.sender_name,
              text: content.text,
              timestamp: Date.now() / 1000,
              source,
            },
          ]);
          break;

        case 'system_status':
          setMessages(prev => [
            ...prev,
            {
              id: `${Date.now()}-${Math.random()}`,
              sender: 'System',
              text: message.data.message,
              timestamp: Date.now() / 1000,
              source: 'system',
            },
          ]);
          break;

        case 'error':
          console.error('WebSocket error:', message.data.error);
          setMessages(prev => [
            ...prev,
            {
              id: `${Date.now()}-${Math.random()}`,
              sender: 'System',
              text: `Lỗi: ${message.data.error}`,
              timestamp: Date.now() / 1000,
              source: 'system',
            },
          ]);
          break;
      }
    });

    // Cleanup
    return () => {
      unsubscribe();
      ws.disconnect();
    };
  }, [sessionId]);

  // Send message function
  const sendMessage = useCallback((senderName: string, messageText: string) => {
    if (wsRef.current?.isConnected()) {
      // Add user message optimistically
      setMessages(prev => [
        ...prev,
        {
          id: `${Date.now()}-${Math.random()}`,
          sender: senderName,
          text: messageText,
          timestamp: Date.now() / 1000,
          source: 'user',
        },
      ]);

      // Send to server
      wsRef.current.sendMessage(senderName, messageText);
    }
  }, []);

  return {
    isConnected,
    agentStatuses,
    messages,
    sendMessage,
  };
}
