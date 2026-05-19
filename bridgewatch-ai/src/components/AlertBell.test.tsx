import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { describe, expect, it, vi } from "vitest";
import { AlertBell } from "./AlertBell";

// Mock the hooks
vi.mock("../hooks/use-alerts", () => ({
  useUnreadAlertCount: () => ({ data: { count: 3 } }),
  useAlerts: () => ({
    data: {
      list: [
        {
          alert_id: "ALT-001", severity: "critical", title: "高风险事件",
          message: "桥面火灾", alert_type: "new_event", status: "unread",
          related_event_id: null, created_time: "2026-05-19T10:00:00",
        },
        {
          alert_id: "ALT-002", severity: "warning", title: "中风险事件",
          message: "车辆积压", alert_type: "new_event", status: "unread",
          related_event_id: null, created_time: "2026-05-19T09:00:00",
        },
      ],
    },
  }),
  useAcknowledgeAlert: () => ({ mutate: vi.fn() }),
}));

function renderWithQuery(ui: React.ReactElement) {
  const qc = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return render(<QueryClientProvider client={qc}>{ui}</QueryClientProvider>);
}

describe("AlertBell", () => {
  it("shows unread count badge", () => {
    renderWithQuery(<AlertBell />);
    expect(screen.getByText("3")).toBeInTheDocument();
  });

  it("shows dropdown when clicked", async () => {
    const user = userEvent.setup();
    renderWithQuery(<AlertBell />);
    await user.click(screen.getByTitle("告警通知"));
    expect(screen.getByText("告警通知")).toBeInTheDocument();
    expect(screen.getByText("高风险事件")).toBeInTheDocument();
    expect(screen.getByText("中风险事件")).toBeInTheDocument();
  });

  it("displays severity badges", async () => {
    const user = userEvent.setup();
    renderWithQuery(<AlertBell />);
    await user.click(screen.getByTitle("告警通知"));
    expect(screen.getByText("紧急")).toBeInTheDocument();
    expect(screen.getByText("警告")).toBeInTheDocument();
  });

  it("shows correct unread count in header", () => {
    renderWithQuery(<AlertBell />);
    expect(screen.getByText("3")).toBeInTheDocument();
  });
});
