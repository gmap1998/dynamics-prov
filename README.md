# ⚙️ Dynamics Prototype

A real-time financial matrix engine — designed for cycle-based computation, strategy modeling, and dynamic asset tracking.  
Powered by Python (FastAPI + MongoDB) with React (Vite) frontend support.

---

## 🚀 Project Architecture

### 🔗 Backend Modules

| Module | Description |
|--------|-------------|
| `execution_controller.py` | Main pipeline. Fetch → Compute → Save cycle. |
| `cycle.py` | Provides wallet snapshot, assets, and cycle timestamp helpers. |
| `matrix_utils.py` | Matrix computations: benchmark, delta, delta_pct, quantid. |
| `db_mongo.py` | Database interface for MongoDB. |
| `cache.py` | Local JSON cache manager (delta, quantid). |
| `save.py` | DB snapshot saving (cycle matrix, wallet, market). |
| `strategy.py` | Strategy Aux and Config manager — tracks state, tier, mode. |
| `routers.py` | API routing for dashboard, wallet, market, strategy, etc. |
| `cli.py` | Command-line interface for admin tasks, strategy, and DB management. |
| `config.py` | Environment variables and operational defaults loader. |

---

## 🧠 Functional Model

### 🔥 Matrix Flow

| Matrix | Description |
|--------|-------------|
| `id_benchmark` | Binance spot prices (benchmark matrix). |
| `id_delta` | Absolute price change (Δ). |
| `id_percent` | Instant delta percentage (Δ%). |
| `id_pct` | Frame-to-frame ΔΔ%. |
| `quantid_matrix` | Normalized quant kinetic matrix. |

---

## 📦 Database Collections

| Collection | Purpose |
|-------------|---------|
| `cycle_matrices` | Full snapshot of each cycle run. |
| `strategy_aux` | Per-cycle auxiliary data: turn, grt, shift, lead quant. |
| `config` | Persistent settings: tier, mode, imprint, luggage, quant base. |

---

## 🌐 API Endpoints

### 🏠 General
- `GET /` → Health check.
- `GET /dashboard` → Run a full cycle and return matrix.

### 💼 Wallet
- `GET /wallet` → Current wallet equivalent from last cycle.

### 🔗 Assets
- `GET /assets` → List assets from last cycle.

### 🗺️ Market
- `GET /market` → Return full matrices (benchmark, delta, delta_pct, id_pct, quantid).

### 🔢 Matrix Access
- `GET /matrix/{matrix_type}` → Fetch single matrix.

### 🔍 Status
- `GET /status` → DB status + last cycle timestamp.

### 🎯 Strategy
- `GET /strategy/config` → Fetch tier/mode/imprint settings.
- `POST /strategy/config` → Update tier/mode/imprint settings.
- `GET /strategy/aux` → Current aux table (turn, grt, shift, lead quant).

---

## 🛠️ CLI Commands

| Command | Description |
|---------|-------------|
| `python cli.py purge --confirm` | Delete all cycles. |
| `python cli.py init` | Setup DB indexes. |
| `python cli.py inspect` | Show latest cycle. |
| `python cli.py reset-cache` | Clear local JSON cache. |
| `python cli.py show-strategy` | Display strategy config (tier/mode/imprint). |
| `python cli.py set-strategy --tier T --mode M` | Update strategy config. |
| `python cli.py show-aux` | Show current strategy aux table. |

---

## ⚙️ Setup

### Install Dependencies
```bash
pip install -r requirements.txt
npm install
```

### Environment Variables
Create a `.env` file with values similar to:
```bash
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=dynamics_prototype
BINANCE_API_KEY=your_key
BINANCE_SECRET_KEY=your_secret
FASTAPI_SECRET_KEY=your_secret_key
VITE_API_URL=http://localhost:8000
```

### Running the FastAPI Server
```bash
uvicorn main:app --reload
```

### Building the Frontend
```bash
npm run build
```

## ⚡ License

MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal 
in the Software without restriction, including without limitation the rights 
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
copies of the Software, and to permit persons to whom the Software is 
furnished to do so, subject to the following conditions:

[...full MIT license text can be here or linked...]

---
Licensed under the MIT License — see LICENSE for details.
