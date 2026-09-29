/// Format integer paise as rupees: en-IN digit grouping, exactly two
/// decimals, integer maths only.
///
///     formatPaise(199999)   == '₹1,999.99'
///     formatPaise(12345678) == '₹1,23,456.78'
///     formatPaise(5)        == '₹0.05'
///     formatPaise(0)        == '₹0.00'
///
/// Throws an [ArgumentError] if [paise] is negative.
String formatPaise(int paise) {
  throw UnimplementedError('not implemented');
}
