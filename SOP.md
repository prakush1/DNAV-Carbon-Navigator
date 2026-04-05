# Standard Operating Procedure (SOP) - DNAV

**Version:** 1.0 (April 2026 Audit-Ready Edition)
**Target:** Fund Accountants & Compliance Analysts

## 1. Daily Ingestion (08:30 - 09:30 AM)
1.  **Set Regulatory Context**: In the sidebar, select the target **Jurisdiction** (e.g., EU, India, or USA). This automatically adjusts the compliance baseline.
2.  **Open DNAV App** and navigate to the **"Connectors"** tab.
3.  **Manual Check**: If any email attachments were received, verify the filename against the `Ref_Carbon_2026` pattern.
4.  **SAP Reconciliation**: Click **"Reconcile SAP Footprint"** to trigger the BTP Hub polling.
5.  **Confirm Data**: Once "Success" is displayed, navigate to the **Dashboard** to see the updated **CANAV**.

## 2. Strategic Forecasting (10:00 AM)
1. Navigate to the **"Strategic Forecast"** tab.
2. Review the **Monte Carlo Probability Distribution**.
3. Identify the **P90 (Worst Case)** scenario for the next 5 years to determine if an asset rebalancing is required.

## 3. AI Sentry & Fraud Review (10:30 AM)
1.  Navigate to the **"AI Oversight"** tab.
2. Review the **Anomaly Alert** dashboard for any Red/Orange flags.
3. **Fraud Action Center**: Select the flagged transaction (e.g., duplicate certificate) and click **"Review"**.
4. **Active Response**: Based on evidence, select **"Verify & White-list"** or **"Block Transaction"**. This action is automatically recorded in the Session Audit Log.
5. **Escalation**: Report the anomaly to the Portfolio Manager if manual verification remains unresolved.

## 4. Final Compliance Review (04:30 PM)
1. Review the **Sidebar Audit Ledger** to ensure all parameter changes (e.g., Price adjustments) have been logged with a justification.
2. Click **"Download Audit PDF"** to reconcile with the daily T+1 NAV ledger.

## 5. Troubleshooting
- **Connection Error**: If SAP/SharePoint connectivity fails, check the **IRD.md** for endpoint configuration.
- **Data Gap**: If an asset is missing carbon data, the system will apply a "Sector Average" penalty as a proxy (Tier 1 logic).
