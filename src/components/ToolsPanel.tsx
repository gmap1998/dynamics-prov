// src/components/ToolsPanel.tsx

import React, { useState } from "react";
import { LuDownload, LuEye, LuFilter, LuRepeat, LuShuffle } from "react-icons/lu";
import { HiOutlineArrowPath, HiOutlineClock } from "react-icons/hi2";



export type MatrixType = Record<string, Record<string, number>>;

export interface ToolsPanelProps {
    currentMatrix: MatrixType;
    previousMatrix: MatrixType;
    onApply: (newMatrix: MatrixType) => void;
    onInvert: () => void;
    onDiff: () => void;
    onFlatten: () => void;
    onDownload: () => void;
    onThreshold: (min: number, max: number) => void;
    highlightInverses: boolean;
    setHighlightInverses: (v: boolean) => void;
}

const ToolsPanel: React.FC<ToolsPanelProps> = ({
    currentMatrix,
    previousMatrix,
    onApply,
    onInvert,
    onDiff,
    onFlatten,
    onDownload,
    onThreshold,
    highlightInverses,
    setHighlightInverses,
}) => {

    const [min, setMin] = useState<number | string>("");
    const [max, setMax] = useState<number | string>("");

    const parseOrEmpty = (value: string | number) =>
        value === "" || isNaN(Number(value)) ? "" : Number(value);

    const handleApplyThreshold = () => {
        const minValue = Number(min) || 0;
        const maxValue = Number(max) || 0;
        onThreshold(minValue, maxValue);
    };

    return (
        <div className="border border-neutral-700 rounded-xl bg-neutral-900 shadow-md p-4 space-y-2 w-64">
            <h2 className="text-base font-semibold border-b border-neutral-800 pb-1">
                Tools Panel
            </h2>

            <div className="flex flex-col space-y-1">
                <button onClick={onInvert} className="button">
                    <LuShuffle size={14} /> Invert
                </button>
                <button onClick={onDiff} className="button">
                    <LuRepeat size={14} /> Compare Δ
                </button>
                <button onClick={onFlatten} className="button">
                    <LuEye size={14} /> Flatten → Console
                </button>
                <button onClick={onDownload} className="button">
                    <LuDownload size={14} /> Download JSON
                </button>
            </div>

            <div className="border-t border-neutral-800 pt-2 space-y-2">
                <h3 className="text-xs text-neutral-400">Threshold Filter</h3>
                <div className="flex space-x-1">
                    <input
                        type="number"
                        className="input w-1/2"
                        placeholder="Min"
                        value={parseOrEmpty(min)}
                        onChange={(e) => setMin(e.target.value)}
                    />
                    <input
                        type="number"
                        className="input w-1/2"
                        placeholder="Max"
                        value={parseOrEmpty(max)}
                        onChange={(e) => setMax(e.target.value)}
                    />
                </div>
                <button onClick={handleApplyThreshold} className="button w-full">
                    Apply
                </button>
            </div>

            <label className="flex items-center space-x-2 text-xs pt-1">
                <input
                    type="checkbox"
                    checked={highlightInverses}
                    onChange={(e) => setHighlightInverses(e.target.checked)}
                />
                <span>Highlight Inverse Pairs</span>
            </label>
        </div>
    );
};

export default ToolsPanel;
