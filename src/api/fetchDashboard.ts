// src/api/fetchDashboard.ts

import { useEffect, useState } from "react";
import api from "@/api/matrixApi"; // Axios instance

// 🔗 Main dashboard fetcher
export async function fetchDashboard() {
    try {
        const res = await api.get("/api/dashboard");
        console.log("✅ Dashboard fetched:", res.data);
        return res.data;
    } catch (err) {
        console.error("❌ Error fetching dashboard:", err);
        return {};
    }
}

// 🔥 Hook: Auto-fetch dashboard with interval
export function useDashboard(intervalMs = 30000) {
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    const fetchData = async () => {
        setLoading(true);
        try {
            const result = await fetchDashboard();
            setData(result);
            setError(null);
        } catch (err: any) {
            setError(err.message || "Unknown error");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
        const interval = setInterval(fetchData, intervalMs);
        return () => clearInterval(interval);
    }, [intervalMs]);

    return { data, loading, error, refetch: fetchData };
}

// 🔗 Hook: Extract matrices only
export function useMatrices() {
    const [matrices, setMatrices] = useState({
        benchmark: {},
        delta: {},
        delta_percent: {},
        id_percent: {},
        quantid: {},
    });

    const fetchMatrices = async () => {
        try {
            const response = await api.get("/api/dashboard");
            const { matrix } = response.data;

            const parsed = {
                benchmark: matrix?.benchmark ?? {},
                delta: matrix?.delta ?? {},
                delta_percent: matrix?.delta_percent ?? {},
                id_percent: matrix?.id_percent ?? {},
                quantid: matrix?.quantid ?? {},
            };

            setMatrices(parsed);
            return parsed;
        } catch (error) {
            console.error("❌ Error fetching matrices", error);
            const empty = {
                benchmark: {},
                delta: {},
                delta_percent: {},
                id_percent: {},
                quantid: {},
            };
            setMatrices(empty);
            return empty;
        }
    };

    useEffect(() => {
        fetchMatrices();
    }, []);

    return { matrices, fetchMatrices };
}

// 🔥 Hook: Wallet + Strategy fetcher
export function useAux() {
    const [wallet, setWallet] = useState<Record<string, number>>({});
    const [strategy, setStrategy] = useState<Record<string, any>>({});

    useEffect(() => {
        const fetchAux = async () => {
            try {
                const [walletRes, strategyRes] = await Promise.all([
                    api.get("/api/wallet"),
                    api.get("/api/strategy/aux"),
                ]);
                setWallet(walletRes.data?.wallet_equivalent ?? {});
                setStrategy(strategyRes.data?.strategy_aux ?? {});
            } catch (error) {
                console.error("❌ Error fetching aux data:", error);
                setWallet({});
                setStrategy({});
            }
        };

        fetchAux();
    }, []);

    return { wallet, strategy };
}
