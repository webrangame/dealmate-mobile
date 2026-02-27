import { initializeApp } from "firebase/app";
// import { getAnalytics } from "firebase/analytics";

// Placeholder Firebase configuration
// Replace with your actual project config
const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_AUTH_DOMAIN",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_STORAGE_BUCKET",
    messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
    appId: "YOUR_APP_ID",
    measurementId: "YOUR_MEASUREMENT_ID"
};

// Initialize Firebase
// Only initialize if config is provided
const app = typeof window !== "undefined" ? initializeApp(firebaseConfig) : null;
// const analytics = typeof window !== "undefined" ? getAnalytics(app) : null;

export { app };
