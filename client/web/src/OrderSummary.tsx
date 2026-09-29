import { useState } from "react";
import { formatPaise } from "./formatPaise";
import type { Order } from "./types";

/**
 * Shows the subtotal, the discount (code and amount) when there is one, and
 * the total, all through formatPaise, plus a "Pay" button that calls onPay.
 *
 * - The button is disabled while onPay is pending (no double submit); it
 *   still reads "Pay".
 * - Only when order.status is "paid" does the button read "Paid"; it is then
 *   disabled.
 * - If onPay rejects, show an error in an element with role="alert" and
 *   re-enable the button.
 */
export function OrderSummary(props: { order: Order; onPay: () => Promise<void> }): JSX.Element {
  const { order, onPay } = props;
  const [isPaying, setIsPaying] = useState(false);
  const [paymentError, setPaymentError] = useState<string | null>(null);
  const isPaid = order.status === "paid";

  async function handlePay(): Promise<void> {
    setIsPaying(true);
    setPaymentError(null);
    try {
      await onPay();
    } catch {
      setPaymentError("Payment failed. Please try again.");
    } finally {
      setIsPaying(false);
    }
  }

  return (
    <section aria-label="Order summary">
      <h2>Order {order.order_id}</h2>
      <p>
        Subtotal: <span>{formatPaise(order.subtotal_paise)}</span>
      </p>
      {order.discount && (
        <p>
          Discount ({order.discount.code}): <span>{formatPaise(order.discount.amount_paise)}</span>
        </p>
      )}
      <p>
        Total: <span>{formatPaise(order.total_paise)}</span>
      </p>
      <button type="button" disabled={isPaying || isPaid} onClick={handlePay}>
        {isPaid ? "Paid" : "Pay"}
      </button>
      {paymentError && <p role="alert">{paymentError}</p>}
    </section>
  );
}
