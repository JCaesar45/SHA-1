# app.py
import os
import json
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import stripe

app = Flask(__name__)
CORS(app, origins=["http://localhost:8080", "https://atelier-noir.example.com"])

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

with open("data/product.json", encoding="utf-8") as f:
    PRODUCT = json.load(f)

@app.get("/api/product")
def get_product():
    return jsonify(PRODUCT)

@app.post("/api/checkout")
def create_checkout():
    payload = request.get_json(silent=True) or {}
    if payload.get("productId") != PRODUCT["productId"]:
        abort(400, description="Unknown product")

    try:
        session = stripe.checkout.Session.create(
            mode="payment",
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": PRODUCT["price"]["currency"].lower(),
                    "unit_amount": PRODUCT["price"]["amount"] * 100,
                    "product_data": {"name": PRODUCT["name"]},
                },
                "quantity": 1,
            }],
            success_url="https://atelier-noir.example.com/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="https://atelier-noir.example.com/",
        )
        return jsonify({"url": session.url})
    except stripe.error.StripeError as e:
        return jsonify({"error": str(e)}), 502

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
