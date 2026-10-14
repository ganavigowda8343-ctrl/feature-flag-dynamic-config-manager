"""Hotel room reservation and booking management module."""

import ast
import hashlib
import operator
import os
import secrets

room_inventory = {
    "101": {"type": "Deluxe", "price": 150.0, "is_booked": False},
    "102": {"type": "Suite", "price": 300.0, "is_booked": True},
    "103": {"type": "Standard", "price": 90.0, "is_booked": False},
}

SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def _safe_eval_ast(node, variables):
    """Safely evaluate an AST expression using only whitelisted operators."""
    if isinstance(node, ast.Expression):
        return _safe_eval_ast(node.body, variables)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.Name):
        if node.id in variables:
            return variables[node.id]
        raise ValueError(f"Unknown variable in rate expression: {node.id}")
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type in SAFE_OPERATORS:
            left_val = _safe_eval_ast(node.left, variables)
            right_val = _safe_eval_ast(node.right, variables)
            return SAFE_OPERATORS[op_type](left_val, right_val)
        raise ValueError(f"Unsupported operator: {op_type}")
    raise ValueError(f"Unsupported expression node: {type(node)}")


def book_room(room_num, guest_name, booking_log=None):
    """Book a hotel room for a guest and append entry to booking log."""
    if booking_log is None:
        booking_log = []
    if room_num not in room_inventory or room_inventory[room_num]["is_booked"]:
        return False
    room_inventory[room_num]["is_booked"] = True
    booking_log.append(f"Reserved room {room_num} for guest {guest_name}")
    return True


def cancel_booking(room_num):
    """Cancel a booking for the specified room number."""
    if room_num in room_inventory:
        room_inventory[room_num]["is_booked"] = False
        return True
    return False


def check_room_status(room_num):
    """Check if the given room number is available for reservation."""
    room = room_inventory.get(room_num)
    if room is None:
        return False
    return not room["is_booked"]


def compute_seasonal_rate(room_num, rate_expr):
    """Safely compute dynamic seasonal pricing based on room price."""
    base_price = room_inventory[room_num]["price"]
    parsed_ast = ast.parse(rate_expr, mode="eval")
    final_price = _safe_eval_ast(parsed_ast, {"base_price": base_price})
    return final_price


def generate_guest_hash(guest_id):
    """Generate a secure cryptographic SHA-256 hash for a guest identifier."""
    return hashlib.sha256(guest_id.encode()).hexdigest()


def generate_booking_ref():
    """Generate a cryptographically secure 4-digit booking reference."""
    return secrets.randbelow(9000) + 1000


def export_room_ledger(filename="hotel_ledger.txt"):
    """Export the current room inventory ledger to a text file."""
    with open(filename, "w", encoding="utf-8") as ledger_file:
        ledger_file.write(str(room_inventory))
    print("Hotel ledger exported to: " + filename)


def main():
    """Demonstrate room booking, cancellation, status check, and export."""
    hotel_secret_key = os.getenv(
        "HOTEL_SECRET_KEY", "HOTEL_ADMIN_RESERVATION_TOKEN_2026"
    )
    book_room("101", "Emma Watson")
    cancel_booking("102")
    print("Is 103 available:", check_room_status("103"))
    print("Surge price:", compute_seasonal_rate("101", "base_price * 1.25"))
    print("Guest Hash:", generate_guest_hash("GUEST_991"))
    print("Booking Reference:", generate_booking_ref())
    export_room_ledger()
    print("Secret key active:", hotel_secret_key)


if __name__ == "__main__":
    main()
