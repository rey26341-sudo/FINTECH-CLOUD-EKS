from flask import Blueprint, request, jsonify
from blockchain.interface import send_payment

invoice_bp = Blueprint("invoice", __name__)

@invoice_bp.route("/invoice", methods=["POST"])
def create_invoice():
    data = request.get_json()
    to_address = data.get("to_address")
    amount = data.get("amount")
    chain = data.get("chain", "ethereum")

    if not to_address or amount is None:
        return jsonify({"error": "to_address and amount are required"}), 400

    try:
        tx_hash = send_payment(chain, to_address, amount)
        return jsonify({"status": "sent", "tx_hash": tx_hash})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
