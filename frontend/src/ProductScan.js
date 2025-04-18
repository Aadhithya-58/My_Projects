import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function ProductScan() {
  const navigate = useNavigate();
  const [product, setProduct] = useState("");
  const [products, setProducts] = useState([]);
  const [activeUserId, setActiveUserId] = useState(""); // Example: Set initial user ID

  const fetchScannedProducts = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5001/get-scanned-products");
      const data = await response.json();

      if (Array.isArray(data.products)) {
        setProducts(data.products);
      } else {
        console.error("Invalid products format:", data.products);
        setProducts([]);
      }
    } catch (error) {
      console.error("Error fetching scanned products:", error);
    }
  };

  const scanProduct = async () => {
    console.log("📡 Requesting scan from Flask...");
    try {
      const response = await fetch(
        `http://127.0.0.1:5001/scan-product?user_id=${activeUserId}`
      ); // Include user_id as query parameter
      const data = await response.json();
      console.log("📥 QR Response from Flask:", data);

      if (data.success) {
        setProduct(data.product);
        fetchScannedProducts(); // Refresh the list
      } else {
        setProduct("Scan failed: " + data.message);
      }
    } catch (error) {
      console.error("Error during scan:", error);
      setProduct("Failed to connect to backend");
    }
  };

  useEffect(() => {
    fetchScannedProducts();
  }, []);

  return (
    <div className="container mt-5">
      <h1 className="mb-4">🔍 GM65 QR Product Scanner</h1>

      {/* Example: Input field for user ID */}
      <input
        type="text"
        placeholder="User ID"
        value={activeUserId}
        onChange={(e) => setActiveUserId(e.target.value)}
        className="mb-3"
      />

      <button className="btn btn-primary mb-3" onClick={scanProduct}>
        Scan Product
      </button>

      {product && (
        <div className="alert alert-success">
          <strong>Scanned:</strong> {product}
        </div>
      )}

      <h3>📦 Scanned Products</h3>
      <ul className="list-group">
        {products.map((item, index) => (
          <li className="list-group-item" key={index}>
            <strong>{item.product}</strong> (ID: {item.id})
          </li>
        ))}
      </ul>
      <button className="btn btn-primary" onClick={() => navigate("/")}>
        Home
      </button>
    </div>
  );
}

export default ProductScan;

/*import React, { useState, useEffect } from "react";

function ProductScan() {
  const [product, setProduct] = useState("");
  const [products, setProducts] = useState([]);

  const fetchScannedProducts = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5001/get-scanned-products");
      const data = await response.json();
      setProducts(data.products || []);
    } catch (error) {
      console.error("Error fetching scanned products:", error);
    }
  };

  const scanProduct = async () => {
    console.log("📡 Requesting scan from Flask...");
    try {
      const response = await fetch("http://127.0.0.1:5001/scan-product");
      const data = await response.json();
      console.log("📥 QR Response from Flask:", data);

      if (data.success) {
        setProduct(data.product);
        fetchScannedProducts(); // refresh the product list
      } else {
        setProduct("Scan failed: " + data.message);
      }
    } catch (error) {
      console.error("Error during scan:", error);
      setProduct("Failed to connect to backend");
    }
  };

  useEffect(() => {
    fetchScannedProducts();
  }, []);

  return (
    <div className="container mt-5">
      <h1 className="mb-4">🔍 GM65 QR Product Scanner</h1>
      <button className="btn btn-primary mb-3" onClick={scanProduct}>
        Scan Product
      </button>

      {product && (
        <div className="alert alert-success">
          <strong>Scanned:</strong> {product}
        </div>
      )}

      <h3>📦 Scanned Products</h3>
      <ul className="list-group">
        {products.map((item) => (
          <li className="list-group-item" key={item.id}>
            {item.product}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ProductScan;
*/