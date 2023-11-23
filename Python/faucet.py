from flask import Flask, request, jsonify
from web3 import Web3
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import time
import os
from dotenv import load_dotenv
import re

load_dotenv()  # Load environment variables from a .env file

app = Flask(__name__)
# CORS(
#     app
# )  # This will allow all origins. For production, you'd want to specify allowed origins.
CORS(
    app,
    origins=[
        "https://faucet-testnet.maalscan.io",
        "https://faucet-testnet.maalscan.io/",
    ],
)

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///maal_faucet.db"
db = SQLAlchemy(app)

# Connect to the EVM
w3 = Web3(Web3.HTTPProvider("https://node1.maalscan.io"))

# Fetch private key from environment variable
private_key = os.environ.get("PRIVATE_KEY")
if not private_key or not re.match("^0x[a-fA-F0-9]{64}$", private_key):
    raise ValueError("Invalid or missing private key in environment variable.")
account = w3.eth.account.from_key(private_key)

class WalletClaim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wallet = db.Column(db.String(42), unique=True, nullable=False)
    timestamp = db.Column(db.Float, nullable=False)


class IPClaim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(15), nullable=False)
    timestamp = db.Column(db.Float, nullable=False)


@app.route("/claim", methods=["POST"])
def claim_maal():
    address = request.json["address"]
    ip_address = request.access_route[0]

    wallet_claim = WalletClaim.query.filter_by(wallet=address).first()
    ip_claim = IPClaim.query.filter_by(ip_address=ip_address).first()

    # Check wallet's last claim
    if wallet_claim and time.time() - wallet_claim.timestamp < 86400:
        return jsonify({"error": "This wallet can claim only every 24 hours."}), 403

    # Check IP's last claim
    if ip_claim and time.time() - ip_claim.timestamp < 86400:
        return jsonify({"error": "This IP address can claim only every 24 hours."}), 403

    tx = {
        "to": address,
        "value": w3.to_wei(1, "ether"),  # Assuming 1 MAAL = 1 Ether for simplicity
        "gas": 21000,
        "gasPrice": w3.to_wei("12", "gwei"),
        "nonce": w3.eth.get_transaction_count(account.address),
    }
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Add new claim data to the database
    new_wallet_claim = WalletClaim(wallet=address, timestamp=time.time())
    new_ip_claim = IPClaim(ip_address=ip_address, timestamp=time.time())
    db.session.add(new_wallet_claim)
    db.session.add(new_ip_claim)
    db.session.commit()

    return jsonify({"txHash": tx_hash.hex()})


if __name__ == "__main__":
    with app.app_context():  # Wrapping the database creation within the app context
        db.create_all()
    app.run(debug=True)
