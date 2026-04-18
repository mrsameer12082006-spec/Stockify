"""Shared helper utilities for the application."""


def format_currency(value: float) -> str:
	"""Format numeric values as Indian rupees."""
	try:
		return f"₹{float(value):,.2f}"
	except (TypeError, ValueError):
		return "₹0.00"
