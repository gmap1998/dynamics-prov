import React, { useEffect, useState } from "react";

console.log("⏱️ Metronome module loaded");

export interface MetronomeProps {
    tick: number;
}

const Metronome: React.FC<MetronomeProps> = ({ tick }) => {
    const [pulse, setPulse] = useState(false);

    useEffect(() => {
        console.log("🎵 Metronome tick", tick);
        const isTriple = tick % 3 === 0;

        const sound = new Audio(isTriple ? "/sounds/double.mp3" : "/sounds/single.mp3");
        sound.play().catch(console.error);

        setPulse(true);
        const t = setTimeout(() => setPulse(false), 400);
        return () => clearTimeout(t);
    }, [tick]);

    return (
        <div className="flex items-center space-x-2">
            <span className={`text-xl ${pulse ? "animate-ping text-green-600" : "text-gray-400"}`}>
                {tick % 3 === 0 ? "🔔" : "🔅"}
            </span>
            <span className="text-xs text-gray-500">
                Tick: <strong>{tick}</strong>
            </span>
        </div>
    );
};

export default Metronome;
