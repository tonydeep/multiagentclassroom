/**
 * TypeScript type definitions for the Multi-Agent Classroom.
 */

export interface Problem {
  id: string;
  title: string;
  problem: string;
}

export interface Session {
  session_id: string;
  problem: Problem;
  participants: string[];
  created_at?: string;
}

export interface Message {
  id: string;
  sender: string;
  text: string;
  timestamp: number;
  source: 'user' | 'agent' | 'system';
}

export type AgentStatus = 'idle' | 'thinking' | 'typing';

export interface AgentStatusUpdate {
  agent_name: string;
  status: AgentStatus;
}

export interface WebSocketMessage {
  type: 'connected' | 'agent_status' | 'new_message' | 'system_status' | 'error';
  data: any;
}

export interface NewMessageData {
  source: 'user' | 'agent';
  content: {
    text: string;
    sender_name: string;
  };
}

export interface SystemStatusData {
  message: string;
  level?: 'info' | 'warning' | 'error';
}
