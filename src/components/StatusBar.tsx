// src/components/StatusBar.tsx

import React from "react";
import { HiOutlineClock } from "react-icons/hi2";
import { LuServer, LuBox, LuWallet, LuDatabase } from "react-icons/lu";

export interface StatusBarProps {
    wallet: Record<string, any>;
    dashboard: Record<string, any>;
    strategy?: Record<string, any>;
}


const StatusBar: React.FC<StatusBarProps> = ({
    wallet,
    strategy,
    dashboard
}) => {
    const dbStatus = dashboard?.db?.status ?? false;
    const cacheStatus = dashboard?.cache?.matrix ? true : false;
    const timestamp = dashboard?.timestamp ?? "—";

    const walletKeys = wallet ? Object.keys(wallet) : [];
    const walletCount = walletKeys.length;

    return (
        <div className="border border-neutral-700 rounded-xl bg-neutral-900 shadow-md p-4 space-y-3">
            <h2 className="text-lg font-semibold mb-1 border-b border-neutral-800 pb-1">
                Status
            </h2>

            <div className="flex items-center gap-2 text-sm">
                <LuDatabase size={16} />
                DB:{" "}
                <span
                    className={
                        dbStatus
                            ? "text-green-400"
                            : "text-red-500"
                    }
                >
                    {dbStatus ? "Connected" : "Offline"}
                </span>
            </div>

            <div className="flex items-center gap-2 text-sm">
                <LuBox size={16} />
                Cache:{" "}
                <span
                    className={
                        cacheStatus
                            ? "text-green-400"
                            : "text-red-500"
                    }
                >
                    {cacheStatus ? "Available" : "Empty"}
                </span>
            </div>

            <div className="flex items-center gap-2 text-sm">
                <LuWallet size={16} />
                Wallet Entries:{" "}
                <span className="text-blue-400">
                    {walletCount}
                </span>
            </div>

            <div className="flex items-center gap-2 text-sm">
                <HiOutlineClock size={16} />
                Last Timestamp:{" "}
                <span className="text-neutral-300">
                    {timestamp}
                </span>
            </div>

            <div className="border-t border-neutral-800 pt-2 text-xs text-neutral-500">
                Strategy Placeholder: {Object.keys(strategy || {}).length} entries
            </div>
        </div>
    );
};

export default StatusBar;


