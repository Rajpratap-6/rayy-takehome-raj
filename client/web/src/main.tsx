import React from "react";
import { createRoot } from "react-dom/client";
import { OrderSummary } from "./OrderSummary";
import type { Order } from "./types";

const sample: Order = {
  order_id: "ord_demo_1",
  subtotal_paise: 199999,
  total_paise: 169999,
  status: "pending",
  discount: { code: "DEMO15", amount_paise: 30000 },
};

createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <OrderSummary order={sample} onPay={() => new Promise((resolve) => setTimeout(resolve, 1000))} />
  </React.StrictMode>,
);
