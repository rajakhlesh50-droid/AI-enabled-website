/**
 * Centurion University of Technology and Management (CUTM)
 * Main Frontend Shared Utilities
 */

const CUTM = {
    API_BASE: "http://127.0.0.1:5000",
    
    // Auth helpers
    getToken() {
        return localStorage.getItem("token");
    },

    getCurrentUser() {
        try {
            return JSON.parse(localStorage.getItem("currentUser") || "null");
        } catch (e) {
            return null;
        }
    },

    logout() {
        localStorage.removeItem("token");
        localStorage.removeItem("currentUser");
        window.location.href = "login.html";
    },

    // Format currency (INR)
    formatCurrency(amount) {
        return new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 }).format(amount);
    },

    // Format date
    formatDate(isoString) {
        if (!isoString) return "-";
        const d = new Date(isoString);
        return isNaN(d.getTime()) ? isoString : new Intl.DateTimeFormat("en-IN", {
            day: "numeric", month: "short", year: "numeric"
        }).format(d);
    }
};

window.CUTM = CUTM;

