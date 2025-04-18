import React, { useState, useEffect } from "react";
import { initializeApp } from "firebase/app";
import { getDatabase, ref, get } from "firebase/database";
import * as XLSX from "xlsx";
import "./App.css";
// Initialize Firebase
const firebaseConfig = {
  apiKey: "AIzaSyCgcQ5m5xMxA0mnPEAeFU9dXQXSmt6cZtU",
  authDomain: "cloud-integration-c6dde.firebaseapp.com",
  databaseURL: "https://cloud-integration-c6dde-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "cloud-integration-c6dde",
  storageBucket: "cloud-integration-c6dde.firebasestorage.app",
  messagingSenderId: "89955976109",
  appId: "1:89955976109:web:e938bd8f6ff612ffe55724",
  measurementId: "G-E344YC5WYG",
};

const app = initializeApp(firebaseConfig);
const database = getDatabase(app);

const ExportData = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const usersSnapshot = await get(ref(database, "registered_users"));
      const productsSnapshot = await get(ref(database, "scanned_products"));

      const usersData = usersSnapshot.exists() ? usersSnapshot.val() : {};
      const productsData = productsSnapshot.exists() ? productsSnapshot.val() : {};

      const formattedData = Object.entries(usersData).map(([userId, user]) => {
        const userProducts = Object.entries(productsData)
          .filter(([productId, product]) => product.scannedBy === userId) // Use productId as key
          .map(([productId, product]) => ({
            User_ID: userId,
            Name: user.name || "N/A",
            RFID: user.rfid || "N/A",
            Product_ID: productId, // Use productId as key
          }));

        // Fill empty fields with a default value if no products
        if (userProducts.length === 0) {
          userProducts.push({
            User_ID: userId,
            Name: user.name || "N/A",
            RFID: user.rfid || "N/A",
            Product_ID:"N/A",
          });
        }

        return userProducts;
      });

      // Flatten the array
      const flatData = [].concat(...formattedData);
      setData(flatData);
    } catch (error) {
      console.error("Fetch error:", error);
    } finally {
      setLoading(false);
    }
  };

  const exportToExcel = () => {
    if (data.length === 0) {
      alert("No data available to export");
      return;
    }

    const ws = XLSX.utils.json_to_sheet(data);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Exported_Data");

    const filename = `Exported_Data_${new Date().toISOString()}.xlsx`;
    XLSX.writeFile(wb, filename);
  };

  return (
    <div style={{ padding: 20 }}>
      <h2 className="text-center">Exported Data</h2>
      <div className="button1">
        <button onClick={exportToExcel} disabled={loading} className="btn btn-primary">
        {loading ? "Loading..." : "Download Excel file"}
        </button>
      </div>
    </div>
  );
};

export default ExportData;
/*import React, { useState, useEffect } from "react";
import { initializeApp } from "firebase/app";
import { getDatabase, ref, get } from "firebase/database";
import * as XLSX from "xlsx";

// Initialize Firebase
const firebaseConfig = {
  apiKey: "AIzaSyCgcQ5m5xMxA0mnPEAeFU9dXQXSmt6cZtU",
  authDomain: "cloud-integration-c6dde.firebaseapp.com",
  databaseURL: "https://cloud-integration-c6dde-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "cloud-integration-c6dde",
  storageBucket: "cloud-integration-c6dde.firebasestorage.app",
  messagingSenderId: "89955976109",
  appId: "1:89955976109:web:e938bd8f6ff612ffe55724",
  measurementId: "G-E344YC5WYG"
};

const app = initializeApp(firebaseConfig);
const database = getDatabase(app);

const ExportData = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const usersSnapshot = await get(ref(database, "registered_users"));
      const productsSnapshot = await get(ref(database, "scanned_products"));

      const usersData = usersSnapshot.exists() ? usersSnapshot.val() : {};
      const productsData = productsSnapshot.exists() ? productsSnapshot.val() : {};

      const formattedData = Object.entries(usersData).map(([userId, user]) => {
        const userProducts = Object.entries(productsData)
          .filter(([_, product]) => product.scannedBy === userId)
          .map(([productId, product]) => ({
            User_ID: userId,
            Name: user.name || "N/A",
            RFID: user.rfid || "N/A",
            Product_ID: productId || "N/A"
          }));

        // Fill empty fields with a default value if no products
        if (userProducts.length === 0) {
          userProducts.push({
            User_ID: userId,
            Name: user.name || "N/A",
            RFID: user.rfid || "N/A",
            Product_ID: "N/A"
          });
        }

        return userProducts;
      });

      // Flatten the array
      const flatData = [].concat(...formattedData);
      setData(flatData);
    } catch (error) {
      console.error("Fetch error:", error);
    } finally {
      setLoading(false);
    }
  };

  const exportToExcel = () => {
    if (data.length === 0) {
      alert("No data available to export");
      return;
    }

    const ws = XLSX.utils.json_to_sheet(data);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Exported_Data");

    const filename = `Exported_Data_${new Date().toISOString()}.xlsx`;
    XLSX.writeFile(wb, filename);
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Export Data</h2>
      <button onClick={exportToExcel} disabled={loading}>
        {loading ? "Loading..." : "Download Excel"}
      </button>
    </div>
  );
};

export default ExportData;
*/