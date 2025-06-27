// src/components/MatricesTable.tsx

import React from "react";

interface MatricesTableProps {
    matrix: Record<string, Record<string, number>>;
    highlightInverses: boolean;
}

const MatricesTable: React.FC<MatricesTableProps> = ({
    matrix,
    highlightInverses,
}) => {
    const rows = Object.keys(matrix);
    const cols = rows.length > 0 ? Object.keys(matrix[rows[0]]) : [];

    const isInverse = (row: string, col: string) => {
        return highlightInverses && matrix[col] && matrix[col][row] != null;
    };

    const formatCell = (value: number | null | undefined) => {
        if (value === null || value === undefined || isNaN(value)) {
            return "-";
        }
        return value.toFixed(4);
    };

    const MatrixPanel = ({
        title,
        matrixData,
    }: {
        title: string;
        matrixData: Record<string, Record<string, number>>;
    }) => (
        <div className="border border-neutral-700 rounded-xl bg-neutral-900 shadow-md p-4 space-y-2">
            <h2 className="text-base font-semibold border-b border-neutral-800 pb-1">
                {title}
            </h2>
            <div className="overflow-auto">
                <table className="min-w-full text-xs">
                    <thead>
                        <tr>
                            <th className="p-1"></th>
                            {cols.map((col) => (
                                <th
                                    key={col}
                                    className="p-1 text-center text-neutral-400"
                                >
                                    {col}
                                </th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {rows.map((row) => (
                            <tr key={row}>
                                <td className="p-1 font-medium text-neutral-300">
                                    {row}
                                </td>
                                {cols.map((col) => {
                                    const value =
                                        matrixData[row]?.[col] ?? null;
                                    const inverse =
                                        highlightInverses &&
                                        matrixData[col]?.[row] != null;

                                    return (
                                        <td
                                            key={`${row}-${col}`}
                                            className={`p-1 text-right ${inverse
                                                    ? "bg-neutral-800"
                                                    : ""
                                                }`}
                                        >
                                            {formatCell(value)}
                                        </td>
                                    );
                                })}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );

    return (
        <div className="space-y-4">
            <MatrixPanel title="Matrix" matrixData={matrix} />
        </div>
    );
};

export default MatricesTable;

