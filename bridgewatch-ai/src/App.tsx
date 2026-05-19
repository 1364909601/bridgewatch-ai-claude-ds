import { AnimatePresence, motion } from "framer-motion";
import {
  Bell,
  Bot,
  CheckCircle2,
  Clock3,
  Gauge,
  LogOut,
  RefreshCw,
  Settings,
  ShieldCheck,
  Sun,
  User,
} from "lucide-react";
import { startTransition, useEffect, useMemo, useRef, useState } from "react";

function useCurrentTime() {
  const [time, setTime] = useState(() => new Date().toLocaleString("zh-CN", { hour12: false }));
  useEffect(() => {
    const id = setInterval(() => {
      setTime(new Date().toLocaleString("zh-CN", { hour12: false }));
    }, 1000);
    return () => clearInterval(id);
  }, []);
  return time;
}
import { QueryProvider } from "./lib/query-provider";
import { generateOperationsDigest } from "./lib/gemini";
import {
  events as mockEvents,
  navItems,
  pageHighlights,
  pageObjectives,
  systemStats
} from "./data/mockData";
import { useEventList, useEventDetail, useReviewEvent } from "./hooks/use-events";
import { mapEventsApiToRecords } from "./lib/type-mappers";
import type { EventRecord, OperationsDigest, PageId } from "./types";
import { EventCenterPage } from "./pages/EventCenterPage";
import { MegaBridgePage } from "./pages/MegaBridgePage";
import { ModelOpsPage } from "./pages/ModelOpsPage";
import { OrdinaryBridgePage } from "./pages/OrdinaryBridgePage";
import { OverviewPage } from "./pages/OverviewPage";
import { PlaybackPage } from "./pages/PlaybackPage";
import { ReportsPage } from "./pages/ReportsPage";
import { SettingsPage } from "./pages/SettingsPage";
import { AuditLogPage } from "./pages/AuditLogPage";
import { TunnelPage } from "./pages/TunnelPage";
import { PageNav } from "./components/PageNav";
import { StatusPill } from "./components/StatusPill";
import { AlertBell } from "./components/AlertBell";
import { AuthProvider, useAuth } from "./contexts/AuthContext";
import { LoginPage } from "./pages/LoginPage";

function AppInner() {
  const { isLoggedIn, user, logout } = useAuth();
  const currentTime = useCurrentTime();
  const [activePage, setActivePage] = useState<PageId>("overview");
  const [selectedEventId, setSelectedEventId] = useState(mockEvents[0].id);
  const [digest, setDigest] = useState<OperationsDigest>({
    headline: "当前系统运行正常",
    bullets: ["AI 风险摘要已接入演示数据。", "高风险事件按优先级进入复核队列。", "可从事件中心直接跳转视频回放。"],
    source: "mock",
    generatedAt: "--:--:--"
  });
  const [digestLoading, setDigestLoading] = useState(false);
  const [useBackend, setUseBackend] = useState(false);

  // Try to fetch events from API; fall back to mock data
  const { data: eventListData, isLoading: eventsLoading, isError: eventsError } = useEventList();

  // Determine whether to use backend or mock data
  const events: EventRecord[] = useMemo(() => {
    if (useBackend && eventListData?.list) {
      return mapEventsApiToRecords(eventListData.list);
    }
    return mockEvents;
  }, [useBackend, eventListData]);

  // If backend is available, switch to it
  useEffect(() => {
    if (eventListData?.list && !eventsLoading && !eventsError) {
      setUseBackend(true);
    }
  }, [eventListData, eventsLoading, eventsError]);

  // Fetch selected event detail from API if using backend
  const { data: eventDetailData } = useEventDetail(useBackend ? selectedEventId : null);

  const selectedEvent: EventRecord = useMemo(() => {
    if (useBackend && eventDetailData) {
      return mapEventsApiToRecords([eventDetailData])[0];
    }
    return events.find((event) => event.id === selectedEventId) ?? events[0];
  }, [useBackend, eventDetailData, events, selectedEventId]);

  const reviewMutation = useReviewEvent();

  const handleReviewEvent = (eventId: string, review_status: string, review_remark?: string) => {
    reviewMutation.mutate({ eventId, review_status, review_remark });
  };

  const activeNav = useMemo(
    () => navItems.find((item) => item.id === activePage) ?? navItems[0],
    [activePage],
  );

  useEffect(() => {
    let active = true;
    setDigestLoading(true);

    generateOperationsDigest({
      pageId: activePage,
      pageTitle: activeNav.label,
      pageObjective: pageObjectives[activePage],
      highlights: pageHighlights[activePage],
      selectedEvent: activePage === "events" || activePage === "playback" ? selectedEvent : undefined
    })
      .then((nextDigest) => {
        if (active) setDigest(nextDigest);
      })
      .finally(() => {
        if (active) setDigestLoading(false);
      });

    return () => {
      active = false;
    };
  }, [activeNav.label, activePage, selectedEvent]);

  const navigate = (pageId: PageId) => {
    startTransition(() => setActivePage(pageId));
  };

  const focusEvent = (eventId: string, targetPage: PageId = "events") => {
    setSelectedEventId(eventId);
    startTransition(() => setActivePage(targetPage));
  };

  const renderPage = () => {
    switch (activePage) {
      case "overview":
        return <OverviewPage onFocusEvent={focusEvent} />;
      case "events":
        return (
          <EventCenterPage
            events={events}
            selectedEvent={selectedEvent}
            onSelectEvent={setSelectedEventId}
            onOpenPlayback={(eventId) => focusEvent(eventId, "playback")}
            onReviewEvent={handleReviewEvent}
            reviewPending={reviewMutation.isPending}
          />
        );
      case "playback":
        return <PlaybackPage event={selectedEvent} relatedEvents={events} onSelectEvent={setSelectedEventId} />;
      case "ordinary":
        return <OrdinaryBridgePage onFocusEvent={focusEvent} />;
      case "ship":
        return <MegaBridgePage />;
      case "tunnel":
        return <TunnelPage />;
      case "ops":
        return <ModelOpsPage />;
      case "reports":
        return <ReportsPage />;
      case "settings":
        return <SettingsPage />;
      case "audit":
        return <AuditLogPage />;
      default:
        return null;
    }
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-row">
          <div className="brand-mark">
            <ShieldCheck size={27} />
          </div>
          <div>
            <div className="brand-title">BridgeWatch AI</div>
            <div className="brand-subtitle">基础设施智能监测面板</div>
          </div>
        </div>
        <PageNav items={navItems} activeId={activePage} onNavigate={navigate} />
      </aside>

      <div className="workspace">
        <header className="topbar">
          <div className="mobile-nav-wrap">
            <PageNav items={navItems} activeId={activePage} onNavigate={navigate} compact />
          </div>
          <div className="top-metrics">
            <div className="top-metric">
              <span>监测对象</span>
              <strong>28</strong>
              <StatusPill tone="ok">在线</StatusPill>
            </div>
            <div className="top-metric">
              <span>系统状态</span>
              <strong className="top-status">
                <CheckCircle2 size={20} />
                {useBackend ? "后端已连接" : "演示模式"}
              </strong>
              <small>{useBackend ? "API 数据实时" : "所有服务运行稳定"}</small>
            </div>
            <div className="top-metric">
              <span>AI 分析引擎</span>
              <strong className="top-status">
                <Bot size={20} />
                Gemini 摘要助手
              </strong>
              <small>实时生成值守摘要</small>
            </div>
            <div className="top-metric">
              <span>数据刷新</span>
              <strong>2.4s</strong>
              <small>最近一次同步</small>
            </div>
          </div>
          <div className="top-actions">
            <span className="timestamp">{currentTime}</span>
            <AlertBell />
            <button className="icon-button" type="button" title="刷新">
              <RefreshCw size={16} />
            </button>
            <button className="icon-button" type="button" title="主题">
              <Sun size={16} />
            </button>
            <button className="icon-button" type="button" title="设置">
              <Settings size={16} />
            </button>
            {user && (
              <div className="flex items-center gap-2 border-l border-slate-700/50 pl-3 ml-1">
                <div className="flex h-7 w-7 items-center justify-center rounded-full bg-brass/20">
                  <User size={14} className="text-brass" />
                </div>
                <span className="hidden text-sm text-slate-200 md:inline">
                  {user.display_name || user.username}
                </span>
                <button
                  type="button"
                  onClick={logout}
                  className="icon-button text-slate-500 hover:text-danger"
                  title="退出登录"
                >
                  <LogOut size={15} />
                </button>
              </div>
            )}
          </div>
        </header>

        <main className="content-grid">
          <section className="page-area">
            <div className="page-title-row">
              <div>
                <div className="page-kicker">{activeNav.eyebrow}</div>
                <h1>{activeNav.label}</h1>
              </div>
              <div className="page-tools">
                <StatusPill tone="ok">
                  <Gauge size={13} />
                  实时分析中
                </StatusPill>
                <StatusPill tone="neutral">
                  <Clock3 size={13} />
                  {digest.generatedAt}
                </StatusPill>
              </div>
            </div>

            <AnimatePresence mode="wait">
              <motion.div
                key={activePage}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -6 }}
                transition={{ duration: 0.18 }}
              >
                {renderPage()}
              </motion.div>
            </AnimatePresence>
          </section>

          <aside className="ai-panel" style={user && user.role === "viewer" ? { maxHeight: "calc(100vh - 180px)", overflowY: "auto" } : {}}>
            <div className="panel-header tight">
              <div>
                <h3 className="panel-title">AI 风险摘要</h3>
                <p className="panel-eyebrow">Gemini Summary</p>
              </div>
              <StatusPill tone="neutral">{digestLoading ? "分析中" : digest.source}</StatusPill>
            </div>
            <div className="ai-headline">{digest.headline}</div>
            <div className="risk-list">
              {events.slice(0, 5).map((event) => (
                <button key={event.id} type="button" className="risk-row" onClick={() => focusEvent(event.id, "events")}>
                  <Bell size={15} className={`risk-dot-${event.riskLevel}`} />
                  <div>
                    <strong>{event.title}</strong>
                    <span>{event.objectName}</span>
                  </div>
                  <StatusPill tone={event.riskLevel === "高" ? "danger" : event.riskLevel === "中" ? "warning" : "low"}>
                    {event.riskLevel}风险
                  </StatusPill>
                </button>
              ))}
            </div>
            <div className="ai-bullets">
              {digest.bullets.map((bullet) => (
                <p key={bullet}>{bullet}</p>
              ))}
            </div>
            <button className="full-button" type="button" onClick={() => navigate("events")}>
              查看全部事件
            </button>
          </aside>
        </main>

        <footer className="status-strip">
          {systemStats.map((item) => (
            <div key={item.label}>
              <span>{item.label}</span>
              <strong>{item.value}</strong>
              <small>{item.status}</small>
            </div>
          ))}
        </footer>
      </div>
    </div>
  );
}

function AppShell() {
  const { isLoggedIn, loading } = useAuth();

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[radial-gradient(ellipse_at_50%_30%,rgba(26,38,35,0.9),rgb(10,12,14))]">
        <div className="text-slate-400 text-sm">加载中...</div>
      </div>
    );
  }

  if (!isLoggedIn) {
    return <LoginPage />;
  }

  return <AppInner />;
}

export default function App() {
  return (
    <QueryProvider>
      <AuthProvider>
        <AppShell />
      </AuthProvider>
    </QueryProvider>
  );
}
