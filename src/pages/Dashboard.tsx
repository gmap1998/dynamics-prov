import { useState } from "react";
import DashboardLayout from "@/components/DashboardLayout";
import MatricesTable from "@/components/MatricesTable";
import ToolsPanel from "@/components/ToolsPanel";
import MetronomeBlock from "@/components/MetronomeBlock";
import StatusBar from "@/components/StatusBar";

import { useDashboard, useMatrices, useAux } from "@/api/fetchDashboard";
import { runCycle } from "@/api/matrixApi";

export default function Dashboard() {
    const { data: dashboard, refetch: refetchDashboard } = useDashboard();
    const { matrices } = useMatrices();
    const { wallet } = useAux();

    const [currentMatrix, setCurrentMatrix] = useState(matrices.benchmark);
    const [previousMatrix, setPreviousMatrix] = useState(matrices.benchmark);
    const [highlightInverses, setHighlightInverses] = useState(false);

    const handleRunCycle = async () => {
        await runCycle();
        refetchDashboard();
    };

    return (
        <DashboardLayout
            ticker={<MetronomeBlock />}
            matrices={
                <MatricesTable
                    matrix={currentMatrix}
                    highlightInverses={highlightInverses}
                />
            }
            toolsPanel={
                <ToolsPanel
                    currentMatrix={currentMatrix}
                    previousMatrix={previousMatrix}
                    onApply={(newMatrix) => setCurrentMatrix(newMatrix)}
                    onInvert={() => console.log("Invert Matrix")}
                    onDiff={() => console.log("Compute Difference")}
                    onFlatten={() => console.log("Flatten Matrix")}
                    onDownload={() => console.log("Download CSV")}
                    onThreshold={(min, max) => console.log("Threshold", min, max)}
                    highlightInverses={highlightInverses}
                    setHighlightInverses={setHighlightInverses}
                />

            }
            statusBar={
                <StatusBar
                    wallet={wallet}
                    dashboard={dashboard}
                />
            }
        />
    );
}


