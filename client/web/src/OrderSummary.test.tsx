import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { formatPaise } from "./formatPaise";
import { OrderSummary } from "./OrderSummary";
import type { Order } from "./types";

const order: Order = {
  order_id: "ord_test_1",
  subtotal_paise: 19999,
  total_paise: 19999,
  status: "pending",
  discount: null,
};

describe("OrderSummary", () => {
  it("formats paise with Indian digit grouping", () => {
    expect(formatPaise(199999)).toBe("₹1,999.99");
    expect(formatPaise(12345678)).toBe("₹1,23,456.78");
    expect(formatPaise(5)).toBe("₹0.05");
    expect(formatPaise(0)).toBe("₹0.00");
    expect(() => formatPaise(12.5)).toThrow("paise must be an integer");
  });

  it("shows subtotal, discount, and total", () => {
    const discountedOrder: Order = {
      ...order,
      total_paise: 169999,
      subtotal_paise: 199999,
      discount: { code: "PARTNER15", amount_paise: 30000 },
    };

    render(<OrderSummary order={discountedOrder} onPay={async () => {}} />);

    expect(screen.getByRole("region", { name: "Order summary" })).toBeInTheDocument();
    expect(screen.getByText("₹1,999.99")).toBeInTheDocument();
    expect(screen.getByText("Discount (PARTNER15):")).toBeInTheDocument();
    expect(screen.getByText("₹300.00")).toBeInTheDocument();
    expect(screen.getByText("₹1,699.99")).toBeInTheDocument();
  });

  it("disables Pay while payment is in progress", async () => {
    const user = userEvent.setup();
    let finishPayment: () => void = () => {};
    const onPay = vi.fn(
      () => new Promise<void>((resolve) => {
        finishPayment = resolve;
      }),
    );
    render(<OrderSummary order={order} onPay={onPay} />);

    const button = screen.getByRole("button", { name: "Pay" });
    await user.click(button);

    expect(onPay).toHaveBeenCalledOnce();
    expect(button).toBeDisabled();
    expect(button).toHaveTextContent("Pay");

    finishPayment();
    await waitFor(() => expect(button).toBeEnabled());
  });

  it("shows Paid after a successful payment updates the order", async () => {
    const user = userEvent.setup();
    const onPay = vi.fn(async () => {});
    const { rerender } = render(<OrderSummary order={order} onPay={onPay} />);

    await user.click(screen.getByRole("button", { name: "Pay" }));
    expect(onPay).toHaveBeenCalledOnce();

    rerender(<OrderSummary order={{ ...order, status: "paid" }} onPay={onPay} />);

    expect(screen.getByRole("button", { name: "Paid" })).toBeDisabled();
  });

  it("shows an error after failure and allows retry", async () => {
    const user = userEvent.setup();
    const onPay = vi
      .fn<() => Promise<void>>()
      .mockRejectedValueOnce(new Error("gateway unavailable"))
      .mockResolvedValueOnce();
    render(<OrderSummary order={order} onPay={onPay} />);

    const button = screen.getByRole("button", { name: "Pay" });
    await user.click(button);

    expect(await screen.findByRole("alert")).toHaveTextContent("Payment failed");
    expect(button).toBeEnabled();

    await user.click(button);
    await waitFor(() => expect(onPay).toHaveBeenCalledTimes(2));
    await waitFor(() => expect(screen.queryByRole("alert")).not.toBeInTheDocument());
  });
});
