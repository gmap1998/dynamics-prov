// src/types/types.ts

export interface WalletItem {
  currency: string;
  balance: number;
  fiat_equivalent: number;
}

export interface MatrixData {
  [base: string]: {
    [quote: string]: number;
  };
}

export interface MarketMatrix {
  benchmark: MatrixData;
  delta: MatrixData;
  delta_pct: MatrixData;
  quantid: Record<string, Record<string, number>>;
}

export interface DashboardData {
  wallet: WalletItem[];
  market: MarketMatrix;
}

export type MatrixType = Record<string, Record<string, number>>;
