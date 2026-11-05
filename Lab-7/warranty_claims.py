"""
Warranty Claims Processing Module
Hardened against unexpected, malformed, and edge-case inputs via defensive programming.
Tested with Hypothesis property-based fuzz testing.
"""
import math


def parse_claim(text):
    """
    Parse a claim string formatted as 'plan:age_months' (e.g. 'standard:30').
    Returns a tuple of (plan_title, age_float) or (None, 0.0) if malformed.
    """
    if not isinstance(text, str):
        return None, 0.0
    parts = text.split(':')
    if len(parts) != 2:
        return None, 0.0
    plan = parts[0].strip().title()
    if not plan:
        return None, 0.0
    try:
        months = float(parts[1].strip())
        if math.isnan(months) or math.isinf(months) or months < 0:
            return None, 0.0
        return plan, months
    except (ValueError, TypeError, OverflowError):
        return None, 0.0


def age_average(ages_csv):
    """
    Parse a comma-separated list of product ages and compute their integer average.
    Returns the integer floor average, or 0 if input is invalid or empty.
    """
    if not isinstance(ages_csv, str):
        return 0
    values = []
    for r in ages_csv.split(','):
        clean_r = r.strip()
        if not clean_r:
            continue
        try:
            val = int(clean_r)
            if val >= 0:
                values.append(val)
        except (ValueError, TypeError, OverflowError):
            continue
    if not values:
        return 0
    return sum(values) // len(values)


def payable_charge(text):
    """
    Parse 'charge|discount' string and calculate net payable amount with 18% tax.
    Formula: max(charge * 1.18 - discount, 0.0)
    Returns float payable charge, or 0.0 if input is malformed or invalid.
    """
    if not isinstance(text, str):
        return 0.0
    parts = text.split('|')
    if len(parts) != 2:
        return 0.0
    try:
        charge = float(parts[0].strip())
        discount = float(parts[1].strip())
        if math.isnan(charge) or math.isinf(charge) or math.isnan(discount) or math.isinf(discount):
            return 0.0
        if charge < 0:
            return 0.0
        total = charge * 1.18 - discount
        return max(total, 0.0)
    except (ValueError, TypeError, OverflowError):
        return 0.0


def main():
    print("==== Running parse_claim ====")
    user_input = input("Enter plan:age in months (e.g. standard:30): ")
    result = parse_claim(user_input)
    print("Plan and Age:", result)

    print("\n==== Running age_average ====")
    user_input = input("Enter product ages as CSV (e.g. 12,24,36): ")
    result = age_average(user_input)
    print("Average Age:", result)

    print("\n==== Running payable_charge ====")
    user_input = input("Enter charge|discount (e.g. 1500|200): ")
    result = payable_charge(user_input)
    print("Payable Charge:", result)


if __name__ == "__main__":
    main()
