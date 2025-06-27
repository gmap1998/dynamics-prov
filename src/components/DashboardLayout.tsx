// src/components/DashboardLayout.tsx

import React from "react";

interface DashboardLayoutProps {
    ticker: React.ReactNode;
    matrices: React.ReactNode;
    toolsPanel: React.ReactNode;
    statusBar: React.ReactNode;
}

export default function DashboardLayout({
    ticker,
    matrices,
    toolsPanel,
    statusBar,
}: DashboardLayoutProps) {
    return (
        <div className="min-h-screen flex flex-col">
            {/* 🔷 Navbar */}
            <header className="w-full bg-neutral-900 border-b border-neutral-800 px-4 py-3 flex items-center justify-between">
                <h1 className="text-lg font-semibold">Dynamics Dashboard</h1>
                <div>{ticker}</div>
            </header>

            {/* 🔲 Main Grid */}
            <main className="flex-1 grid grid-cols-12 gap-4 p-4">
                {/* 🧠 Left — Matrices */}
                <section className="col-span-7 space-y-4">
                    {matrices}
                </section>

                {/* 📊 Center — Quant + Tools */}
                <aside className="col-span-3 space-y-4">
                    {toolsPanel}
                </aside>

                {/* 🔥 Right — Cinetics/Status */}
                <aside className="col-span-2 space-y-4">
                    {statusBar}
                </aside>
            </main>

            {/* 🔻 Footer */}
            <footer className="w-full bg-neutral-900 border-t border-neutral-800 px-4 py-2 text-xs text-neutral-500">
                Dynamics System · Guest.Labs · 2025
            </footer>
        </div>
    );
}


