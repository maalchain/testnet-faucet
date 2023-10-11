import React, { useState } from "react";
import "./Faucet.css";
import { Flowbite } from "flowbite-react";
import maal from "./maal.png";

function Faucet() {
  const [walletAddress, setWalletAddress] = useState("");
  const [responseMessage, setResponseMessage] = useState("");

  const handleClaim = async () => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      // Update the body to send the data in the desired format
      body: JSON.stringify({ address: walletAddress }),
    };

    try {
      const response = await fetch(
        "https://faucet-api-pqr8.onrender.com/claim",
        requestOptions
      );
      const data = await response.json();

      if (data.txHash) {
        setResponseMessage(`Transaction successful: ${data.txHash}`);
      } else {
        setResponseMessage(data.error);
      }
    } catch (error) {
      setResponseMessage("Error occurred while claiming tokens.");
    }
  };

  return (
    <div className="faucet-container">
       <img
              src={maal}
              className="w-5 m-b-1"
            />
      <h1>MaalChain Testnet Faucet</h1>
      <input
        type="text"
        placeholder="Enter your wallet address"
        value={walletAddress}
        onChange={(e) => setWalletAddress(e.target.value)}
      />
      <button onClick={handleClaim}>Claim 1 test MAAL Token</button>
      {responseMessage && <p className="response-message">{responseMessage}</p>}
    </div>
  );
}

export default Faucet;
