import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
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
  it("renders", () => {
    render(<OrderSummary order={order} onPay={async () => {}} />);
    expect(screen.getByRole("region", { name: "Order summary" })).toBeInTheDocument();
  });
});
