import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { LoginPage } from "./LoginPage";

// Mock the auth context
vi.mock("../contexts/AuthContext", () => ({
  useAuth: () => ({
    login: vi.fn(),
    error: null,
  }),
}));

describe("LoginPage", () => {
  it("renders login form with title", () => {
    render(<LoginPage />);
    expect(screen.getByText("BridgeWatch AI")).toBeInTheDocument();
    expect(screen.getByText("基础设施智能监测面板")).toBeInTheDocument();
  });

  it("shows test account hints", () => {
    render(<LoginPage />);
    expect(screen.getByText(/admin\/admin123/)).toBeInTheDocument();
  });

  it("has username and password inputs", () => {
    render(<LoginPage />);
    expect(screen.getByLabelText("用户名")).toBeInTheDocument();
    expect(screen.getByLabelText("密码")).toBeInTheDocument();
  });

  it("has disabled submit button when inputs empty", () => {
    render(<LoginPage />);
    expect(screen.getByRole("button", { name: "登 录" })).toBeDisabled();
  });

  it("enables submit when inputs filled", async () => {
    const user = userEvent.setup();
    render(<LoginPage />);
    const username = screen.getByLabelText("用户名");
    const password = screen.getByLabelText("密码");
    await user.type(username, "admin");
    await user.type(password, "admin123");
    expect(screen.getByRole("button", { name: "登 录" })).not.toBeDisabled();
  });
});
