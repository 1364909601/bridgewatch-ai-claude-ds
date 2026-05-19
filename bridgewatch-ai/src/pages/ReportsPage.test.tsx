import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { ReportsPage } from "./ReportsPage";

describe("ReportsPage", () => {
  it("renders page title", () => {
    render(<ReportsPage />);
    expect(screen.getByText("报告生成")).toBeInTheDocument();
  });

  it("renders three report cards", () => {
    render(<ReportsPage />);
    expect(screen.getByText("事件统计报告")).toBeInTheDocument();
    expect(screen.getByText("系统运行报告")).toBeInTheDocument();
    expect(screen.getByText("数据导出")).toBeInTheDocument();
  });

  it("renders recent reports section", () => {
    render(<ReportsPage />);
    expect(screen.getByText("最近报告")).toBeInTheDocument();
    expect(screen.getByText("2026年5月事件统计报告")).toBeInTheDocument();
    expect(screen.getByText("2026年4月事件统计报告")).toBeInTheDocument();
  });

  it("renders download buttons", () => {
    render(<ReportsPage />);
    const downloadButtons = document.querySelectorAll('[title="下载"]');
    expect(downloadButtons.length).toBeGreaterThan(0);
  });
});
