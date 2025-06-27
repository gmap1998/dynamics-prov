// src/api/apiCycle.ts

import axios from "axios";

// 🔗 Axios instance with base URL config
const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || "",
});

// 🔥 Fetch any matrix type (id_percent, delta, benchmark, quantid, etc.)
export async function fetchMatrix(type: string) {
    try {
        const response = await api.get(`/api/matrix/${type}`);
        const raw = response.data.matrix;

        if (!raw || typeof raw !== "object")
            return { matrix: [], rows: [], cols: [] };

        // Detect if nested or flat format
        const isNested =
            Object.values(raw)[0] &&
            typeof Object.values(raw)[0] === "object";

        let rows: string[] = [];
        let cols: string[] = [];
        let matrix: number[][] = [];

        if (isNested) {
            rows = Object.keys(raw);
            cols = Object.keys(raw[rows[0]] ?? {});

            matrix = rows.map((row) =>
                cols.map((col) => {
                    const val = raw[row]?.[col];
                    return typeof val === "number" ? val : 0;
                })
            );
        } else {
            // Flattened pairs like BTCETH
            const pairs = Object.keys(raw);
            const coins = Array.from(
                new Set(
                    pairs.flatMap((p) => [
                        p.slice(0, p.length / 2),
                        p.slice(p.length / 2),
                    ])
                )
            );

            rows = coins;
            cols = coins;

            matrix = rows.map((row) =>
                cols.map((col) => {
                    const pair = row + col;
                    const val = raw[pair];
                    return typeof val === "number" ? val : 0;
                })
            );
        }

        return { matrix, rows, cols };
    } catch (error) {
        console.error(`❌ Error fetching matrix ${type}`, error);
        return { matrix: [], rows: [], cols: [] };
    }
}

// 🔥 Trigger a backend cycle execution
export async function runCycle() {
    try {
        const response = await api.post("/api/cycle/run");
        console.log("✅ Cycle triggered:", response.data);
        return response.data;
    } catch (error) {
        console.error("❌ Error running cycle:", error);
        throw error;
    }
}

// 🔥 Fetch dashboard snapshot (entire cycle data)
export async function fetchDashboard() {
    try {
        const response = await api.get("/api/dashboard");
        return response.data;
    } catch (error) {
        console.error("❌ Error fetching dashboard", error);
        throw error;
    }
}

// 🔥 Fetch backend + cache status
export async function fetchStatus() {
    try {
        const response = await api.get("/api/status");
        return response.data;
    } catch (error) {
        console.error("❌ Error fetching status", error);
        throw error;
    }
}

export default api;
