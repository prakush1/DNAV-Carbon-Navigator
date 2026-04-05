# DNAV Project Glossary & Industry Intelligence (April 2026 Edition)

Welcome to the **DNAV Knowledge Base**. This glossary is designed to bridge the gap between high-finance (Private Equity/Accounting) and Climate-Tech (Carbon Science). It explains the "what", "why", and "who" behind the DNAV engine.

---

## 🏛️ Regulatory Bodies & Standards (Verification Sites)
*Use these links to verify the methodology used in this project.*

1.  **[PCAF (Partnership for Carbon Accounting Financials)](https://carbonaccountingfinancials.com/)**: The global "gold standard" for measuring *financed emissions*. DNAV uses PCAF methodology for Scope 3 portfolio calculation.
2.  **[SBTi (Science Based Targets initiative)](https://sciencebasedtargets.org/)**: Validates if corporate emissions reduction targets are in line with the Paris Agreement (limiting warming to 1.5°C).
3.  **[ISSB (International Sustainability Standards Board)](https://www.ifrs.org/groups/international-sustainability-standards-board/)**: The IFRS-backed board setting the global baseline for sustainability disclosure (IFRS S1 and S2).
4.  **[IPCC Emission Factor Database](https://www.ipcc-nggip.iges.or.jp/EFDB/main.php)**: The library of "multipliers" used to convert activity data (e.g., flight miles) into CO2 equivalents.
5.  **[CDP (Carbon Disclosure Project)](https://www.cdp.net/en)**: The global disclosure system for investors, companies, cities, and states to manage their environmental impacts.

---

## 🏢 Key Industry Vendors (Data Providers)
*These are the "Bloomberg/Reuters" of the carbon world. DNAV is designed to ingest data from these leaders.*

- **MSCI ESG Research**: Provides ESG ratings, climate data, and indices. Widely used for benchmarking portfolio performance.
- **Sustainalytics (Morningstar)**: Specialized in ESG risk ratings and controversy research. DNAV integrates Sustainalytics for "Controversy Risk" flags.
- **S&P Global Sustainable1**: Offers deep climate risk analytics and ESG scores across 100,000+ companies.
- **Refinitiv (London Stock Exchange Group)**: Transparent ESG data coverage used by institutional investors.
- **Watershed / Persefoni**: Modern "Carbon Accounting Software" (SaaS) targets. DNAV acts as the *Asset Management* layer on top of these activity trackers.

---

## 📖 Technical Definitions (Simple Level)

### A - G
- **BRSR Core (Business Responsibility and Sustainability Reporting)**: 
  - *Simple Level*: SEBI's (India) mandatory report for the top 1,000 companies. It checks if they are acting responsibly.
  - *Industry Value*: Requires "Reasonable Assurance" (an intense audit) as of April 2024.
- **Carbon Navigator (DNAV Core)**: The engine that maps traditional financial NAV to carbon-liabilities.
- **Carbon-Adjusted NAV (caNAV)**: 
  - *Formula*: `Standard NAV - Future Carbon Liability`.
  - *Why it matters*: Shows the "hidden risk" if carbon prices suddenly spike.
- **Double Materiality**: The concept that climate change affects the company (financial risk) AND the company affects the environment (impact risk).

### I - P
- **Internal Carbon Price (ICP)**: A "shadow price" a company places on its own emissions to simulate future taxes. Currently ranges from $50 to $200 per tonne globally.
- **ISSA 5000**: The new international standard for sustainability assurance. If your project follows this, auditors (PwC, EY, etc.) can trust it.
- **Limited vs. Reasonable Assurance**:
  - *Limited*: "We didn't see anything wrong." (Low bar).
  - *Reasonable*: "We checked everything and it is correct." (High bar - required for 2026).
- **PCAF Score**: A 1 to 5 rating of how good your data is. Score 1 is "High Quality" (direct measurement), Score 5 is "Low Quality" (guesses based on industry averages).

### S - Z
- **Scope 1, 2, 3 (The Emissions Layers)**:
  - **Scope 1**: Things you burn (your gas, your cars).
  - **Scope 2**: Energy you buy (your electricity bill).
  - **Scope 3 (The Hard One)**: Your supply chain (your vendors) and your investments (financed emissions).
- **SFDR (Sustainable Finance Disclosure Regulation)**: EU law that forces investment funds to categorize themselves as Green (Article 9), Light Green (Article 8), or Gray (Article 6).
- **True Fair Value**: In accounting, "Fair Value" is what something is worth now. "True Fair Value" in 2026 must include the cost of cleaning up its carbon footprint.
- **WACI (Weighted Average Carbon Intensity)**: A measure of a portfolio's exposure to carbon-intensive companies. Formula: `Sum(Weight * Carbon Intensity)`.

---

## 🛡️ GRC & Audit Terms
- **Audit Ledger**: A permanent, unchangeable record of every button click and change in the system. Required for compliance.
- **Kill Switch**: A safety mechanism that disables the "Automated AI Logic" if it starts behaving unexpectedly (e.g., hallucinating data).
- **Phantom Offset**: A fake carbon credit. DNAV's AI scans for these to prevent fraud.
