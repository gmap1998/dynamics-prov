// src/api/runCycle.ts

import axios from "axios";

export async function runCycle() {
    try {
        const response = await axios.post("/api/cycle/run");
        console.log("✅ Cycle triggered:", response.data);
        return response.data;
    } catch (error) {
        console.error("❌ Error running cycle:", error);
        throw error;
    }
}


