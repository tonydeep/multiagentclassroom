/**
 * API client for communicating with the FastAPI backend.
 */

import type { Problem, Session } from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Fetch all available problems.
 */
export async function getProblems(): Promise<Problem[]> {
  const response = await fetch(`${API_URL}/api/problems`);

  if (!response.ok) {
    throw new Error('Failed to fetch problems');
  }

  return response.json();
}

/**
 * Create a new learning session.
 */
export async function createSession(
  problemId: string,
  userName: string = 'Student'
): Promise<Session> {
  const response = await fetch(`${API_URL}/api/sessions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      problem_id: problemId,
      user_name: userName,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to create session');
  }

  return response.json();
}

/**
 * Get session data.
 */
export async function getSession(sessionId: string): Promise<any> {
  const response = await fetch(`${API_URL}/api/sessions/${sessionId}`);

  if (!response.ok) {
    throw new Error('Failed to fetch session');
  }

  return response.json();
}
