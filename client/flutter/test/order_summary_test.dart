import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:rayy_client/order_summary.dart';

void main() {
  testWidgets('OrderSummary renders', (tester) async {
    final order = <String, dynamic>{
      'order_id': 'ord_test_1',
      'subtotal_paise': 19999,
      'total_paise': 19999,
      'status': 'pending',
      'discount': null,
    };
    await tester.pumpWidget(MaterialApp(
      home: Scaffold(body: OrderSummary(order: order, onPay: () async {})),
    ));
    expect(find.byType(OrderSummary), findsOneWidget);
  });
}
