// src/firebaseConfig.js
import { initializeApp } from "firebase/app";
import { getDatabase } from "firebase/database";

// 🔹 Replace these values with your Firebase project config
const firebaseConfig = {
  apiKey: "AIzaSyCgcQ5m5xMxA0mnPEAeFU9dXQXSmt6cZtU",
  authDomain: "cloud-integration-c6dde.firebaseapp.com",
  databaseURL: "https://cloud-integration-c6dde-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "cloud-integration-c6dde",
  storageBucket: "cloud-integration-c6dde.firebasestorage.app",
  messagingSenderId: "89955976109",
  appId: "1:89955976109:web:e938bd8f6ff612ffe55724",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const database = getDatabase(app);

export { database };
