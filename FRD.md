# Functional Requirements Document (FRD) - DNAV

## 1. Core Logic & Features

### 1.1 CANAV Calculation Engine
- **Formula**: `CANAV = Gross NAV - (Portfolio CO2e * Internal Carbon Price)`
- **Portfolio CO2e**: Weighted average carbon intensity (WACI) based on asset value.
- **Temp Alignment**: Mapping WACI to 1.5°C, 2.0°C, and 3.0°C scenarios using PACTA-inspired thresholds.

### 1.4 Strategic Forecasting (Monte Carlo)
- **Engine**: Perform 1,000 iterations of portfolio NAV impact based on stochastic carbon price volatility.
- **Output**: 5-Year Probability Distribution (P10, P50, P90) of expected Carbon Liability.
- **Goal**: Identify "NAV at Risk" for long-term strategic resilience.

### 1.5 Sensitivity Analysis (Break-Even)
- **Engine**: Dynamic calculation of the "Insolvency Carbon Price"—the value at which `Gross NAV == Carbon Liability`.
- **UI**: Slider-based stress-testing to visualize the NAV impact of sudden price shocks.

### 1.6 Session Auditability (Immutable Ledger)
- **Logic**: Every user action (Jurisdiction Change, Parameter Adjustment, Data Load) must be timestamped and logged in a persistent session-state list.
- **Reporting**: Ability to export the session audit trail as part of the Daily Compliance Report.

## 2. Integration Requirements
- **SAP BTP**: Fetch emission sub-ledgers using BTP Footprint Management OData APIs.
- **MS SharePoint/Graph**: Automated polling of email attachments and shared drive folders for "Carbon Certificate" PDFs.
- **SMTP Gateway**: IMAP polling of shared mailboxes for custodian emissions reports.

## 3. UI/UX Requirements
- **Sidebar Safety**: Global "AI Kill Switch" to pause automated calculations if data variance exceeds ±15% benchmarks.
- **Mobile-Responsive**: Compatible with tablet/mobile views for senior fund accountants on the go.
