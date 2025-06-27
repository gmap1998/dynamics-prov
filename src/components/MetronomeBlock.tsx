// src/components/MetronomeBlock.tsx

import React from "react";
import { HiOutlineArrowPath, HiOutlineClock } from "react-icons/hi2";
import { LuServer } from "react-icons/lu";

interface MetronomeBlockProps {
    lastCycle?: string;
    nextCycleIn?: number;
    onRunCycle?: () => void;
}

const MetronomeBlock: React.FC<MetronomeBlockProps> = ({
    lastCycle = "—",
    nextCycleIn = 0,
    onRunCycle,
}) => {
    return (
        <div className="flex items-center gap-4">
            {/* ⏳ Clock */}
            <div className="flex items-center gap-1 text-sm text-neutral-300">
                <HiOutlineClock size={16} />
                <span>Last:</span>
                <span className="text-neutral-100">{lastCycle}</span>
            </div>

            {/* 🔄 Next cycle countdown */}
            <div className="flex items-center gap-1 text-sm text-blue-400">
                <LuServer size={16} />
                <span>Next in:</span>
                <span>{nextCycleIn}s</span>
            </div>

            {/* 🔁 Run Cycle Button */}
            <button
                onClick={onRunCycle}
                className="bg-neutral-800 hover:bg-neutral-700 border border-neutral-600 px-2 py-1 rounded flex items-center gap-1 text-xs"
            >
                <HiOutlineArrowPath size={14} />
                Refresh
            </button>
        </div>
    );
};

export default MetronomeBlock;
