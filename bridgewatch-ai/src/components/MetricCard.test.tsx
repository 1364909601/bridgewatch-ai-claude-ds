import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { MetricCard } from "./MetricCard";
import type { DashboardMetric } from "../types";

describe("MetricCard", () => {
  const baseMetric: DashboardMetric = {
    id: "test",
    label: "高风险事件",
    value: "3",
    hint: "需要立即复核",
    tone: "danger",
  };

  it("renders label", () => {
    render(<MetricCard metric={baseMetric} />);
    expect(screen.getByText("高风险事件")).toBeInTheDocument();
  });

  it("renders value", () => {
    render(<MetricCard metric={baseMetric} />);
    expect(screen.getByText("3")).toBeInTheDocument();
  });

  it("renders hint text", () => {
    render(<MetricCard metric={baseMetric} />);
    expect(screen.getByText("需要立即复核")).toBeInTheDocument();
  });

  it("applies correct tone class for danger", () => {
    const { container } = render(<MetricCard metric={baseMetric} />);
    expect(container.querySelector(".risk-danger")).toBeInTheDocument();
  });

  it("displays warning icon for warning tone", () => {
    const warningMetric = { ...baseMetric, tone: "warning" as const };
    const { container } = render(<MetricCard metric={warningMetric} />);
    expect(container.querySelector(".risk-warning")).toBeInTheDocument();
  });
});
