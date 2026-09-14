"use client";

import React, { useEffect, useState } from "react";
import { format } from "date-fns";
import ReactMarkdown from "react-markdown";

// Types
interface Review {
  reviewId: string;
  content: string;
  score: number;
  thumbsUpCount: number;
  at: string;
}

interface Theme {
  name: string;
  description: string;
  review_count: number;
  avg_rating: number;
  top_quote: string;
}

interface Pulse {
  filename: string;
  content: string;
}

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState("pulse");
  const [reviews, setReviews] = useState<Review[]>([]);
  const [themes, setThemes] = useState<Theme[]>([]);
  const [pulse, setPulse] = useState<Pulse | null>(null);
  const [loading, setLoading] = useState(true);
  const [triggering, setTriggering] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

  const fetchData = async (showLoading = true) => {
    if (showLoading) setLoading(true);
    try {
      const [reviewsRes, themesRes, pulseRes] = await Promise.all([
        fetch(`${API_URL}/reviews`),
        fetch(`${API_URL}/themes`),
        fetch(`${API_URL}/pulse/latest`),
      ]);

      if (reviewsRes.ok) setReviews(await reviewsRes.json());
      if (themesRes.ok) {
        const themesData = await themesRes.json();
        setThemes(themesData.themes || []);
      }
      if (pulseRes.ok) setPulse(await pulseRes.json());
    } catch (err) {
      console.error("Failed to fetch data:", err);
      if (showLoading) setError("Failed to connect to the backend API.");
    } finally {
      if (showLoading) setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [API_URL]);

  const triggerPipeline = async () => {
    setTriggering(true);
    try {
      const res = await fetch(`${API_URL}/pulse/trigger`, { method: "POST" });
      if (res.ok) {
        // Poll for updates every 4 seconds for 6 minutes total (90 attempts)
        let attempts = 0;
        const maxAttempts = 90;
        
        const pollInterval = setInterval(async () => {
          attempts++;
          await fetchData(false); // fetch without triggering the main loading spinner
          
          if (attempts >= maxAttempts) {
            clearInterval(pollInterval);
            setTriggering(false);
          }
        }, 4000);
      } else {
        alert("Failed to trigger pipeline.");
        setTriggering(false);
      }
    } catch (err) {
      console.error(err);
      alert("Error triggering pipeline.");
      setTriggering(false);
    }
  };

  return (
    <div className="min-h-screen bg-background text-text-primary">
      {/* Header */}
      <header className="fixed top-0 w-full z-50 bg-surface/90 backdrop-blur-xl border-b border-border">
        <div className="max-w-[1440px] mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="w-8 h-8 rounded-lg bg-primary/20 flex items-center justify-center font-bold text-primary">
              G
            </div>
            <div>
              <h1 className="text-lg font-semibold tracking-tight leading-none text-text-primary">Groww Pulse</h1>
              <p className="text-xs text-text-secondary mt-1">AI-Powered Review Intelligence</p>
            </div>
          </div>
          
          <nav className="flex items-center space-x-4">
            <div className="flex space-x-2">
              {["pulse", "themes", "reviews"].map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors ${
                    activeTab === tab
                      ? "bg-primary text-background"
                      : "text-text-secondary hover:text-text-primary hover:bg-surface-floating"
                  }`}
                >
                  {tab.charAt(0).toUpperCase() + tab.slice(1)}
                </button>
              ))}
            </div>
            <div className="w-px h-6 bg-border"></div>
            <button 
              onClick={triggerPipeline} 
              disabled={triggering}
              className="px-4 py-1.5 bg-ai/10 text-ai border border-ai/20 hover:bg-ai/20 disabled:opacity-50 rounded-lg text-sm font-semibold transition-all flex items-center gap-2"
            >
              {triggering ? (
                <>
                  <div className="w-3 h-3 border-2 border-ai border-t-transparent rounded-full animate-spin"></div>
                  Triggering...
                </>
              ) : (
                <>
                  ⚡ Trigger Now
                </>
              )}
            </button>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="pt-24 pb-12 max-w-[1440px] mx-auto px-6">
        {loading ? (
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
          </div>
        ) : error ? (
          <div className="p-4 bg-danger/10 border border-danger/20 rounded-lg text-danger">
            {error}
          </div>
        ) : (
          <div className="space-y-6">
            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-surface border border-border rounded-xl p-4">
                <h3 className="text-sm text-text-secondary mb-1">Total Reviews Analysed</h3>
                <p className="text-2xl font-bold">{reviews.length}</p>
              </div>
              <div className="bg-surface border border-border rounded-xl p-4">
                <h3 className="text-sm text-text-secondary mb-1">Average Sentiment</h3>
                <p className="text-2xl font-bold">
                  {(reviews.reduce((acc, r) => acc + (r.score || 0), 0) / (reviews.length || 1)).toFixed(1)} / 5.0
                </p>
              </div>
              <div className="bg-surface border border-border rounded-xl p-4">
                <h3 className="text-sm text-text-secondary mb-1">Identified Themes</h3>
                <p className="text-2xl font-bold text-ai">{themes.length}</p>
              </div>
            </div>

            {/* Tabs Content */}
            {activeTab === "pulse" && (
              <div className="bg-surface border border-border rounded-xl p-8 prose prose-invert max-w-none">
                {pulse ? (
                  <ReactMarkdown>{pulse.content}</ReactMarkdown>
                ) : (
                  <p className="text-text-secondary">No pulse report available yet.</p>
                )}
              </div>
            )}

            {activeTab === "themes" && (
              <div className="grid grid-cols-1 gap-4">
                {themes.map((theme, i) => (
                  <div key={i} className="bg-surface border border-border hover:border-border-hover rounded-xl p-6 transition-all">
                    <div className="flex items-start justify-between">
                      <div>
                        <h3 className="text-lg font-semibold text-text-primary">{theme.name}</h3>
                        <p className="text-sm text-text-secondary mt-1">{theme.description}</p>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="px-2.5 py-1 rounded-full bg-ai/10 text-ai text-xs font-semibold border border-ai/20">
                          {theme.review_count} reviews
                        </span>
                        <span className={`px-2.5 py-1 rounded-full text-xs font-semibold border ${
                          theme.avg_rating >= 4 ? 'bg-primary/10 text-primary border-primary/20' : 
                          theme.avg_rating <= 2 ? 'bg-danger/10 text-danger border-danger/20' : 
                          'bg-warning/10 text-warning border-warning/20'
                        }`}>
                          ★ {theme.avg_rating}
                        </span>
                      </div>
                    </div>
                    {theme.top_quote && (
                      <div className="mt-4 p-4 bg-surface-floating rounded-lg border border-border/50">
                        <p className="text-sm italic text-text-secondary">"{theme.top_quote}"</p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}

            {activeTab === "reviews" && (
              <div className="bg-surface border border-border rounded-xl overflow-hidden">
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-sm">
                    <thead className="bg-surface-floating border-b border-border">
                      <tr>
                        <th className="px-6 py-3 font-semibold text-text-secondary">Date</th>
                        <th className="px-6 py-3 font-semibold text-text-secondary">Rating</th>
                        <th className="px-6 py-3 font-semibold text-text-secondary">Content</th>
                        <th className="px-6 py-3 font-semibold text-text-secondary">Helpful</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-border">
                      {reviews.slice(0, 50).map((review, i) => (
                        <tr key={i} className="hover:bg-surface-floating/50 transition-colors">
                          <td className="px-6 py-4 whitespace-nowrap text-text-tertiary">
                            {review.at ? format(new Date(review.at), 'MMM d, yyyy') : 'Unknown'}
                          </td>
                          <td className="px-6 py-4">
                            <span className={`px-2 py-1 rounded text-xs font-semibold ${
                              review.score >= 4 ? 'bg-primary/10 text-primary' : 
                              review.score <= 2 ? 'bg-danger/10 text-danger' : 
                              'bg-warning/10 text-warning'
                            }`}>
                              ★ {review.score}
                            </span>
                          </td>
                          <td className="px-6 py-4 max-w-md truncate text-text-secondary" title={review.content}>
                            {review.content}
                          </td>
                          <td className="px-6 py-4 text-text-tertiary">
                            👍 {review.thumbsUpCount || 0}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}
