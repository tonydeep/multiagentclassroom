/**
 * WebSocket manager for real-time communication.
 */

import type { WebSocketMessage } from '@/types';

const WS_URL = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000';

export type MessageHandler = (message: WebSocketMessage) => void;
export type ErrorHandler = (error: Event) => void;
export type CloseHandler = (event: CloseEvent) => void;

export class WebSocketManager {
  private ws: WebSocket | null = null;
  private sessionId: string;
  private messageHandlers: Set<MessageHandler> = new Set();
  private errorHandlers: Set<ErrorHandler> = new Set();
  private closeHandlers: Set<CloseHandler> = new Set();
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 2000;

  constructor(sessionId: string) {
    this.sessionId = sessionId;
  }

  /**
   * Connect to the WebSocket server.
   */
  connect(): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      console.log('WebSocket already connected');
      return;
    }

    const wsUrl = `${WS_URL}/ws/${this.sessionId}`;
    console.log('Connecting to WebSocket:', wsUrl);

    this.ws = new WebSocket(wsUrl);

    this.ws.onopen = () => {
      console.log('WebSocket connected');
      this.reconnectAttempts = 0;
    };

    this.ws.onmessage = (event) => {
      try {
        const message: WebSocketMessage = JSON.parse(event.data);
        console.log('WebSocket message received:', message);

        this.messageHandlers.forEach(handler => handler(message));
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      this.errorHandlers.forEach(handler => handler(error));
    };

    this.ws.onclose = (event) => {
      console.log('WebSocket closed:', event.code, event.reason);
      this.closeHandlers.forEach(handler => handler(event));

      // Attempt to reconnect
      if (this.reconnectAttempts < this.maxReconnectAttempts) {
        this.reconnectAttempts++;
        console.log(`Reconnecting... (attempt ${this.reconnectAttempts})`);

        setTimeout(() => {
          this.connect();
        }, this.reconnectDelay * this.reconnectAttempts);
      }
    };
  }

  /**
   * Send a message through the WebSocket.
   */
  send(type: string, data: any): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ type, data }));
    } else {
      console.error('WebSocket is not connected');
    }
  }

  /**
   * Send a chat message.
   */
  sendMessage(senderName: string, message: string): void {
    this.send('send_message', {
      sender_name: senderName,
      message,
    });
  }

  /**
   * End the session.
   */
  endSession(): void {
    this.send('end_session', {});
  }

  /**
   * Add a message handler.
   */
  onMessage(handler: MessageHandler): () => void {
    this.messageHandlers.add(handler);
    return () => this.messageHandlers.delete(handler);
  }

  /**
   * Add an error handler.
   */
  onError(handler: ErrorHandler): () => void {
    this.errorHandlers.add(handler);
    return () => this.errorHandlers.delete(handler);
  }

  /**
   * Add a close handler.
   */
  onClose(handler: CloseHandler): () => void {
    this.closeHandlers.add(handler);
    return () => this.closeHandlers.delete(handler);
  }

  /**
   * Disconnect from the WebSocket.
   */
  disconnect(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  /**
   * Check if WebSocket is connected.
   */
  isConnected(): boolean {
    return this.ws?.readyState === WebSocket.OPEN;
  }
}
