'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Problem } from '@/types';
import { getProblems, createSession } from '@/lib/api';
import { ProblemCard } from '@/components/ProblemCard';

export default function Home() {
  const router = useRouter();
  const [problems, setProblems] = useState<Problem[]>([]);
  const [selectedProblemId, setSelectedProblemId] = useState<string | null>(null);
  const [userName, setUserName] = useState('Student');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load problems on mount
  useEffect(() => {
    async function loadProblems() {
      try {
        const data = await getProblems();
        setProblems(data);
      } catch (err) {
        console.error('Failed to load problems:', err);
        setError('Không thể tải danh sách bài toán');
      }
    }

    loadProblems();
  }, []);

  // Start session
  async function handleStartSession() {
    if (!selectedProblemId) {
      setError('Vui lòng chọn một bài toán');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const session = await createSession(selectedProblemId, userName);
      router.push(`/chat/${session.session_id}`);
    } catch (err: any) {
      console.error('Failed to create session:', err);
      setError(err.message || 'Không thể tạo phiên học');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gradient-primary p-6">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center text-white mb-12">
          <h1 className="text-5xl font-bold mb-4 drop-shadow-lg">
            🎓 Multi-Agent Classroom
          </h1>
          <p className="text-xl opacity-90">
            Powered by Claude Agent SDK • FastAPI • Next.js
          </p>
        </div>

        {/* Main Content */}
        <div className="bg-white rounded-2xl shadow-2xl p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">
            Chọn bài toán để bắt đầu
          </h2>

          {/* Problem Selection */}
          <div className="space-y-4 mb-8">
            {problems.map((problem) => (
              <ProblemCard
                key={problem.id}
                problem={problem}
                selected={selectedProblemId === problem.id}
                onClick={() => setSelectedProblemId(problem.id)}
              />
            ))}
          </div>

          {/* User Name Input */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Tên của bạn
            </label>
            <input
              type="text"
              value={userName}
              onChange={(e) => setUserName(e.target.value)}
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:outline-none focus:border-primary-500 transition-colors"
              placeholder="Nhập tên của bạn..."
            />
          </div>

          {/* Error Message */}
          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
              {error}
            </div>
          )}

          {/* Start Button */}
          <button
            onClick={handleStartSession}
            disabled={!selectedProblemId || loading}
            className="w-full py-4 px-6 bg-gradient-primary text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transform hover:scale-[1.02] transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
          >
            {loading ? 'Đang khởi tạo...' : 'Bắt đầu học'}
          </button>
        </div>

        {/* Footer */}
        <div className="text-center text-white mt-8 opacity-75">
          <p className="text-sm">
            Built with FastAPI, Next.js 14, TypeScript, and Tailwind CSS
          </p>
        </div>
      </div>
    </div>
  );
}
