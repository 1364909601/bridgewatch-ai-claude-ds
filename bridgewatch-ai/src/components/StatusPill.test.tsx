import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { StatusPill } from "./StatusPill";

describe("StatusPill", () => {
  it("renders text content", () => {
    render(<StatusPill tone="ok">在线</StatusPill>);
    expect(screen.getByText("在线")).toBeInTheDocument();
  });

  it("applies correct tone class for danger", () => {
    const { container } = render(<StatusPill tone="danger">高风险</StatusPill>);
    expect(container.firstChild).toHaveClass("status-danger");
  });

  it("applies correct tone class for warning", () => {
    const { container } = render(<StatusPill tone="warning">中风险</StatusPill>);
    expect(container.firstChild).toHaveClass("status-warning");
  });

  it("applies correct tone class for ok", () => {
    const { container } = render(<StatusPill tone="ok">已确认</StatusPill>);
    expect(container.firstChild).toHaveClass("status-ok");
  });

  it("applies correct tone class for neutral", () => {
    const { container } = render(<StatusPill tone="neutral">待复核</StatusPill>);
    expect(container.firstChild).toHaveClass("status-neutral");
  });
});
