import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { PageNav } from "./PageNav";

const items = [
  { id: "overview" as const, label: "总览指挥台", eyebrow: "Overview" },
  { id: "events" as const, label: "事件中心", eyebrow: "Events" },
  { id: "reports" as const, label: "报告中心", eyebrow: "Reports" },
  { id: "settings" as const, label: "系统设置", eyebrow: "Settings" },
];

describe("PageNav", () => {
  it("renders all nav items", () => {
    render(<PageNav items={items} activeId="overview" onNavigate={() => {}} />);
    expect(screen.getByText("总览指挥台")).toBeInTheDocument();
    expect(screen.getByText("事件中心")).toBeInTheDocument();
    expect(screen.getByText("报告中心")).toBeInTheDocument();
    expect(screen.getByText("系统设置")).toBeInTheDocument();
  });

  it("highlights the active item", () => {
    render(<PageNav items={items} activeId="events" onNavigate={() => {}} />);
    const buttons = screen.getAllByRole("button");
    const activeBtn = buttons.find((b) => b.className.includes("is-active"));
    expect(activeBtn).toBeTruthy();
    expect(activeBtn?.textContent).toContain("事件中心");
  });

  it("calls onNavigate when item clicked", async () => {
    const onNavigate = vi.fn();
    const user = userEvent.setup();
    render(<PageNav items={items} activeId="overview" onNavigate={onNavigate} />);
    await user.click(screen.getByText("报告中心"));
    expect(onNavigate).toHaveBeenCalledWith("reports");
  });

  it("renders icons for each item", () => {
    const { container } = render(<PageNav items={items} activeId="overview" onNavigate={() => {}} />);
    const svgs = container.querySelectorAll("svg");
    expect(svgs.length).toBe(items.length);
  });
});
