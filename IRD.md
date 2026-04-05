# Integration Requirements Document (IRD) - DNAV

## 1. System Landscape
The DNAV Engine acts as an "Abstraction Layer" over three primary enterprise data streams.

| Source System | Integration Protocol | Data Ingested | Frequency |
| :--- | :--- | :--- | :--- |
| **SAP BTP Footprint Hub** | OData v4 / API | GHG Sub-ledger (S1, S2, S3) | Daily (08:30) |
| **Microsoft Graph API** | MS Graph / SharePoint | Digital Certificates (Verified Offsets) | Ad-hoc / On-push |
| **SMTP / Shared Mailbox** | IMAP over TLS | Custodian Carbon Portfolios | Weekly |

## 2. API Specifications (OData)
Fetching data from SAP BTP Footprint Hub:
- **Endpoint:** `https://btp-gateway.sap/footprint/Emissions?$filter=AssetID eq 'AAPL'`
- **Auth:** OAuth 2.0 (Client Credentials Grant)

## 3. Microsoft Graph Schema (Certs)
Polling SharePoint for carbon certificate validity:
- **Folder Path:** `/Finance/ESG_Compliance/Verified_Certs`
- **Metadata Check:** Verify `Issuer_ID` and `Retirement_Date` from custom column metadata to prevent double-counting.

## 4. Security & Compliance
- **Data at Rest:** All ingested carbon footprints must be encrypted using AES-256.
- **Audit Logging:** Every successful and failed API call must be logged in the "Live Audit Ledger" within the UI.
