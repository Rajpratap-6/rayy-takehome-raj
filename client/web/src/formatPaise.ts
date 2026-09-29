/**
 * Format integer paise as rupees: en-IN digit grouping, exactly two decimals,
 * integer maths only (no floating-point division of the amount).
 *
 *   formatPaise(199999)   === "₹1,999.99"
 *   formatPaise(12345678) === "₹1,23,456.78"
 *   formatPaise(5)        === "₹0.05"
 *   formatPaise(0)        === "₹0.00"
 *
 * Throws an Error if `paise` is not an integer.
 */
export function formatPaise(paise: number): string {
  if (!Number.isSafeInteger(paise)) {
    throw new Error("paise must be an integer");
  }

  const absolutePaise = Math.abs(paise);
  const rupees = Math.floor(absolutePaise / 100);
  const paisePart = String(absolutePaise % 100).padStart(2, "0");
  const digits = String(rupees);
  const lastThree = digits.slice(-3);
  const leadingDigits = digits.slice(0, -3);
  const groupedLeadingDigits = leadingDigits.replace(/\B(?=(\d{2})+(?!\d))/g, ",");
  const groupedRupees = leadingDigits
    ? `${groupedLeadingDigits},${lastThree}`
    : lastThree;
  const sign = paise < 0 ? "-" : "";

  return `${sign}₹${groupedRupees}.${paisePart}`;
}
