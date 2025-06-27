// src/utils/matrixUtils.ts

/**
 * 🔁 Invert matrix (swap rows and columns)
 */
export function invertMatrix(
    matrix: Record<string, Record<string, number>>
) {
    const result: Record<string, Record<string, number>> = {};

    for (const row in matrix) {
        for (const col in matrix[row]) {
            if (!result[col]) result[col] = {};
            result[col][row] = matrix[row][col];
        }
    }

    return result;
}

/**
 * 🔍 Diff two matrices (A - B)
 */
export function diffMatrices(
    current: Record<string, Record<string, number>>,
    previous: Record<string, Record<string, number>>
) {
    const result: Record<string, Record<string, number>> = {};

    for (const row in current) {
        for (const col in current[row]) {
            const currVal = current[row][col] ?? 0;
            const prevVal = previous?.[row]?.[col] ?? 0;
            const diff = currVal - prevVal;

            if (!result[row]) result[row] = {};
            result[row][col] = diff;
        }
    }

    return result;
}

/**
 * 🎛️ Threshold filter (clamp to min/max)
 */
export function thresholdFilter(
    matrix: Record<string, Record<string, number>>,
    min: number,
    max: number
) {
    const result: Record<string, Record<string, number>> = {};

    for (const row in matrix) {
        for (const col in matrix[row]) {
            const val = matrix[row][col];
            if (val >= min && val <= max) {
                if (!result[row]) result[row] = {};
                result[row][col] = val;
            }
        }
    }

    return result;
}

/**
 * 🪪 Flatten matrix → [{ pair: 'BTCETH', value: X }]
 */
export function flattenMatrix(
    matrix: Record<string, Record<string, number>>
) {
    const flatArray: { pair: string; value: number }[] = [];

    for (const row in matrix) {
        for (const col in matrix[row]) {
            flatArray.push({
                pair: `${row}${col}`,
                value: matrix[row][col],
            });
        }
    }

    return flatArray;
}
