import 'package:flutter/material.dart';

/// Shows the subtotal, the discount (code and amount) when there is one, and
/// the total, all through `formatPaise`, plus a Pay button.
///
/// [order] is the JSON from GET /orders/{id} plus discount info:
/// `order_id` (String), `subtotal_paise` (int), `total_paise` (int),
/// `status` (String, e.g. 'pending' or 'paid'), and `discount`
/// (null, or a map with `code` (String) and `amount_paise` (int)).
///
/// - The Pay button is an [ElevatedButton] whose child is `Text('Pay')`.
/// - It is disabled while [onPay] is pending (no double submit); it still
///   shows `Text('Pay')`.
/// - Only when `status` is 'paid' does it show `Text('Paid')`; it is then
///   disabled.
/// - If [onPay] throws, show a [Text] containing 'Payment failed' and
///   re-enable the button.
class OrderSummary extends StatefulWidget {
  const OrderSummary({super.key, required this.order, required this.onPay});

  final Map<String, dynamic> order;
  final Future<void> Function() onPay;

  @override
  State<OrderSummary> createState() => _OrderSummaryState();
}

class _OrderSummaryState extends State<OrderSummary> {
  @override
  Widget build(BuildContext context) {
    // Placeholder: replace with the real summary.
    return Column(
      mainAxisSize: MainAxisSize.min,
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Order ${widget.order['order_id']}'),
      ],
    );
  }
}
