"use client";

import React, { useEffect, useState } from "react";
import { format } from "date-fns";
import ReactMarkdown from "react-markdown";
import { motion, AnimatePresence } from "framer-motion";
import { Sparkles, MessageSquare, BarChart2, Zap, LayoutList, MessageCircle, Quote } from "lucide-react";

import { SentimentTrajectoryChart } from "@/components/SentimentTrajectoryChart";
import { FeaturePodChart } from "@/components/FeaturePodChart";
import { StoreEcologyChart } from "@/components/StoreEcologyChart";
import { Activity, Target } from "lucide-react";

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

interface KPIs {
  net_sentiment: number;
  velocity: number;
  detractor_rate: number;
}

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState("analytics");
  const [reviews, setReviews] = useState<Review[]>([]);
  const [themes, setThemes] = useState<Theme[]>([]);
  const [pulse, setPulse] = useState<Pulse | null>(null);
  const [trajectory, setTrajectory] = useState<any[]>([]);
  const [kpis, setKpis] = useState<KPIs>({ net_sentiment: 0, velocity: 0, detractor_rate: 0 });
  const [featurePods, setFeaturePods] = useState<any[]>([]);
  const [storeEcology, setStoreEcology] = useState<any>({});
  const [loading, setLoading] = useState(true);
  const [triggering, setTriggering] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

  const fetchData = async (showLoading = true) => {
    if (showLoading) setLoading(true);
    try {
      const [reviewsRes, themesRes, pulseRes, trajRes, kpiRes, podsRes, ecoRes] = await Promise.all([
        fetch(`${API_URL}/reviews`),
        fetch(`${API_URL}/themes`),
        fetch(`${API_URL}/pulse/latest`),
        fetch(`${API_URL}/analytics/trajectory`),
        fetch(`${API_URL}/analytics/kpis`),
        fetch(`${API_URL}/analytics/feature-pods`),
        fetch(`${API_URL}/analytics/store-ecology`)
      ]);

      if (reviewsRes.ok) setReviews(await reviewsRes.json());
      if (themesRes.ok) {
        const themesData = await themesRes.json();
        setThemes(themesData.themes || []);
      }
      if (pulseRes.ok) setPulse(await pulseRes.json());
      if (trajRes.ok) setTrajectory(await trajRes.json());
      if (kpiRes.ok) setKpis(await kpiRes.json());
      if (podsRes.ok) setFeaturePods(await podsRes.json());
      if (ecoRes.ok) setStoreEcology(await ecoRes.json());
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
        let attempts = 0;
        const maxAttempts = 90;
        
        const pollInterval = setInterval(async () => {
          attempts++;
          await fetchData(false); 
          
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

  const avgSentiment = reviews.length 
    ? (reviews.reduce((acc, r) => acc + (r.score || 0), 0) / reviews.length).toFixed(1)
    : "0.0";

  return (
    <div className="min-h-screen bg-background text-text-primary overflow-hidden relative">
      {/* Animated Background Blobs */}
      <div className="fixed inset-0 w-full h-full pointer-events-none z-0 overflow-hidden">
        <div className="absolute top-[-10%] left-[-10%] w-96 h-96 bg-primary/20 rounded-full mix-blend-screen filter blur-[100px] animate-blob" />
        <div className="absolute top-[20%] right-[-10%] w-96 h-96 bg-ai/20 rounded-full mix-blend-screen filter blur-[100px] animate-blob animation-delay-2000" />
        <div className="absolute bottom-[-20%] left-[20%] w-96 h-96 bg-primary/10 rounded-full mix-blend-screen filter blur-[100px] animate-blob animation-delay-4000" />
      </div>

      {/* Header */}
      <header className="fixed top-0 w-full z-50 bg-surface/80 backdrop-blur-xl border-b border-border/50">
        <div className="max-w-[1440px] mx-auto px-6 h-16 flex items-center justify-between">
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center gap-4"
          >
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-ai flex items-center justify-center shadow-lg shadow-primary/20">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-lg font-bold tracking-tight text-white">Groww Pulse</h1>
              <p className="text-xs text-text-secondary font-medium tracking-wide uppercase">AI Review Intelligence</p>
            </div>
          </motion.div>
          
          <nav className="flex items-center space-x-6">
            <div className="flex p-1 bg-surface-floating rounded-xl border border-border/50">
              {[
                { id: "analytics", icon: Activity, label: "Analytics" },
                { id: "pulse", icon: Zap, label: "Pulse" },
                { id: "themes", icon: LayoutList, label: "Themes" },
                { id: "reviews", icon: MessageCircle, label: "Reviews" }
              ].map((tab) => {
                const Icon = tab.icon;
                const isActive = activeTab === tab.id;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`relative px-4 py-1.5 rounded-lg text-sm font-medium transition-all duration-300 flex items-center gap-2 ${
                      isActive ? "text-white" : "text-text-secondary hover:text-white"
                    }`}
                  >
                    {isActive && (
                      <motion.div
                        layoutId="active-tab"
                        className="absolute inset-0 bg-border/50 rounded-lg shadow-sm"
                        transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                      />
                    )}
                    <Icon className="w-4 h-4 relative z-10" />
                    <span className="relative z-10">{tab.label}</span>
                  </button>
                );
              })}
            </div>
            
            <button 
              onClick={triggerPipeline} 
              disabled={triggering}
              className="relative group px-5 py-2 rounded-xl text-sm font-bold transition-all overflow-hidden"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-ai to-primary opacity-20 group-hover:opacity-30 transition-opacity" />
              <div className="absolute inset-0 border border-white/10 group-hover:border-white/20 rounded-xl transition-colors" />
              <div className="relative flex items-center gap-2 text-white">
                {triggering ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white/50 border-t-white rounded-full animate-spin" />
                    Generating Magic...
                  </>
                ) : (
                  <>
                    <Zap className="w-4 h-4 text-primary" />
                    Trigger Now
                  </>
                )}
              </div>
            </button>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="pt-28 pb-12 max-w-[1440px] mx-auto px-6 relative z-10">
        {loading ? (
          <div className="flex flex-col items-center justify-center h-[60vh] gap-4">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-primary to-ai p-[2px] animate-pulse">
              <div className="w-full h-full bg-background rounded-[14px] flex items-center justify-center">
                <Sparkles className="w-5 h-5 text-primary" />
              </div>
            </div>
            <p className="text-text-secondary font-medium tracking-wide">Loading Intelligence...</p>
          </div>
        ) : error ? (
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="p-6 bg-danger/10 border border-danger/20 rounded-2xl text-danger backdrop-blur-md">
            {error}
          </motion.div>
        ) : (
          <div className="space-y-8">
            {/* Tab Content */}
            <AnimatePresence mode="wait">
              <motion.div
                key={activeTab}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.2 }}
              >
                {activeTab === "analytics" && (
                  <div className="space-y-6">
                    {/* KPI Cards */}
                    <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-4">
                      {[
                        { label: "Reviews Analysed", value: reviews.length, icon: MessageSquare, color: "text-blue-400" },
                        { label: "Identified Themes", value: themes.length, icon: Sparkles, color: "text-purple-400" },
                        { label: "Net Sentiment", value: `${kpis.net_sentiment.toFixed(1)}`, icon: Target, color: "text-primary" },
                        { label: "Detractor Rate", value: `${kpis.detractor_rate.toFixed(1)}%`, icon: BarChart2, color: "text-danger" },
                        { label: "Avg Sentiment", value: `${avgSentiment}`, icon: Zap, color: "text-blue-400" },
                        { label: "Velocity (/Day)", value: kpis.velocity, icon: Activity, color: "text-ai" }
                      ].map((kpi, i) => (
                        <motion.div
                          key={kpi.label}
                          initial={{ opacity: 0, y: 20 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: i * 0.1 }}
                          className="bg-surface/50 backdrop-blur-xl border border-border/50 rounded-2xl p-6 relative overflow-hidden group hover:border-border transition-colors"
                        >
                          <div className={`absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-white/5 to-transparent rounded-bl-full opacity-0 group-hover:opacity-100 transition-opacity`} />
                          <div className="flex items-start justify-between relative z-10">
                            <div>
                              <h3 className="text-sm text-text-secondary font-medium tracking-wide mb-2">{kpi.label}</h3>
                              <p className="text-3xl font-bold text-white tracking-tight">{kpi.value}</p>
                            </div>
                            <div className={`p-3 rounded-xl bg-surface-floating border border-border/50 ${kpi.color}`}>
                              <kpi.icon className="w-5 h-5" />
                            </div>
                          </div>
                        </motion.div>
                      ))}
                    </div>

                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* Sentiment Trajectory */}
                    <div className="lg:col-span-2 bg-surface/60 backdrop-blur-xl border border-border/50 rounded-3xl p-6 shadow-2xl flex flex-col">
                      <h2 className="text-lg font-bold text-white mb-6">Sentiment Trajectory</h2>
                      <SentimentTrajectoryChart data={trajectory} />
                    </div>

                    {/* Store Ecology */}
                    <div className="bg-surface/60 backdrop-blur-xl border border-border/50 rounded-3xl p-6 shadow-2xl flex flex-col">
                      <h2 className="text-lg font-bold text-white mb-6">Store Ecology</h2>
                      <StoreEcologyChart data={storeEcology} />
                      {storeEcology.android && (
                        <div className="mt-4 flex flex-col space-y-2">
                          <div className="flex justify-between items-center text-sm">
                            <span className="text-text-secondary">Android Avg:</span>
                            <span className="text-white font-bold">{storeEcology.android.avg_rating} ★</span>
                          </div>
                          <div className="flex justify-between items-center text-sm">
                            <span className="text-text-secondary">iOS Avg:</span>
                            <span className="text-white font-bold">{storeEcology.ios?.avg_rating || 0} ★</span>
                          </div>
                        </div>
                      )}
                    </div>

                    {/* Feature Pods */}
                    <div className="lg:col-span-3 bg-surface/60 backdrop-blur-xl border border-border/50 rounded-3xl p-6 shadow-2xl flex flex-col">
                      <h2 className="text-lg font-bold text-white mb-6">Feature Pod Metrics (30 Days)</h2>
                      <FeaturePodChart data={featurePods} />
                    </div>
                  </div>
                  </div>
                )}

                {activeTab === "pulse" && (
                  <div className="bg-surface/60 backdrop-blur-xl border border-border/50 rounded-3xl p-10 shadow-2xl">
                    {pulse ? (
                      <div className="prose prose-invert prose-lg max-w-none prose-headings:text-white prose-a:text-primary prose-strong:text-white prose-strong:font-semibold">
                        <ReactMarkdown>{pulse.content}</ReactMarkdown>
                      </div>
                    ) : (
                      <div className="flex flex-col items-center justify-center py-20 text-center">
                        <div className="w-16 h-16 rounded-2xl bg-surface-floating border border-border flex items-center justify-center mb-6">
                          <Zap className="w-8 h-8 text-text-tertiary" />
                        </div>
                        <h2 className="text-xl font-bold text-white mb-2">No Pulse Generated</h2>
                        <p className="text-text-secondary max-w-md">The AI hasn't generated a pulse report for this week yet. Click the Trigger button above to analyze recent reviews.</p>
                      </div>
                    )}
                  </div>
                )}

                {activeTab === "themes" && (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {themes.map((theme, i) => (
                      <motion.div 
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: i * 0.05 }}
                        key={i} 
                        className="bg-surface/50 backdrop-blur-xl border border-border/50 hover:border-white/20 rounded-3xl p-8 transition-all duration-300 relative overflow-hidden group"
                      >
                        {/* Subtle glowing top border for top 3 themes */}
                        {i < 3 && (
                          <div className={`absolute top-0 left-0 w-full h-1 bg-gradient-to-r ${
                            i === 0 ? 'from-primary to-ai' : i === 1 ? 'from-ai to-blue-500' : 'from-blue-500 to-primary'
                          } opacity-70`} />
                        )}
                        
                        <div className="flex items-start justify-between mb-4">
                          <h3 className="text-xl font-bold text-white group-hover:text-primary transition-colors">{theme.name}</h3>
                          <div className="flex gap-2">
                            <span className="px-3 py-1 rounded-full bg-surface-floating border border-border/50 text-text-secondary text-xs font-bold tracking-wide">
                              {theme.review_count} REVIEWS
                            </span>
                            <span className={`px-3 py-1 rounded-full text-xs font-bold border ${
                              theme.avg_rating >= 4 ? 'bg-primary/10 text-primary border-primary/20' : 
                              theme.avg_rating <= 2 ? 'bg-danger/10 text-danger border-danger/20' : 
                              'bg-warning/10 text-warning border-warning/20'
                            }`}>
                              ★ {theme.avg_rating}
                            </span>
                          </div>
                        </div>
                        <p className="text-sm text-text-secondary leading-relaxed mb-6">{theme.description}</p>
                        
                        {theme.top_quote && (
                          <div className="p-5 bg-surface-floating/80 rounded-2xl border border-border/30 relative mt-auto">
                            <Quote className="w-5 h-5 text-primary/40 absolute top-4 right-4" />
                            <p className="text-sm italic text-text-primary/90 pr-6">"{theme.top_quote}"</p>
                          </div>
                        )}
                      </motion.div>
                    ))}
                  </div>
                )}

                {activeTab === "reviews" && (
                  <div className="bg-surface/50 backdrop-blur-xl border border-border/50 rounded-3xl overflow-hidden shadow-2xl">
                    <div className="overflow-x-auto">
                      <table className="w-full text-left text-sm">
                        <thead className="bg-surface-floating/50 border-b border-border/50 backdrop-blur-md">
                          <tr>
                            <th className="px-8 py-5 font-semibold text-text-secondary tracking-wide uppercase text-xs">Date</th>
                            <th className="px-8 py-5 font-semibold text-text-secondary tracking-wide uppercase text-xs">Rating</th>
                            <th className="px-8 py-5 font-semibold text-text-secondary tracking-wide uppercase text-xs">Content</th>
                            <th className="px-8 py-5 font-semibold text-text-secondary tracking-wide uppercase text-xs">Helpful</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-border/30">
                          {reviews.slice(0, 50).map((review, i) => (
                            <tr key={i} className="hover:bg-surface-floating/30 transition-colors">
                              <td className="px-8 py-5 whitespace-nowrap text-text-tertiary font-medium">
                                {review.at ? format(new Date(review.at), 'MMM d, yyyy') : 'Unknown'}
                              </td>
                              <td className="px-8 py-5">
                                <span className={`inline-flex items-center justify-center px-2.5 py-1 rounded-md text-xs font-bold ${
                                  review.score >= 4 ? 'bg-primary/10 text-primary' : 
                                  review.score <= 2 ? 'bg-danger/10 text-danger' : 
                                  'bg-warning/10 text-warning'
                                }`}>
                                  ★ {review.score}
                                </span>
                              </td>
                              <td className="px-8 py-5 text-text-secondary max-w-xl truncate hover:whitespace-normal hover:bg-surface-floating/50 hover:rounded-lg p-2 transition-all cursor-default">
                                {review.content}
                              </td>
                              <td className="px-8 py-5 text-text-tertiary font-medium">
                                {review.thumbsUpCount || 0}
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}
              </motion.div>
            </AnimatePresence>
          </div>
        )}
      </main>
    </div>
  );
}
