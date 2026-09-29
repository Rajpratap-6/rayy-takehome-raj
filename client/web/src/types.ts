/** An order as the client receives it: GET /orders/{id} plus discount info. All money is integer paise. */
export type Order = {
  order_id: string;
  subtotal_paise: number;
  total_paise: number;
  status: "pending" | "paid" | (string & {});
  discount: null | { code: string; amount_paise: number };
};
