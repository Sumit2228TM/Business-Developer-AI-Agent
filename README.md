🧬 Biotech Lead Scoring Agent
AI-powered lead generation system for 3D In-Vitro Models in pharma/biotech
Built for: Task at Euprime AI Engineering Intern | Built by: Sumit Gatade

# 1. 🎯 What It Does
This tool identifies and ranks biotech/pharma researchers who are most likely to be interested in 3D in-vitro models for therapy development.
Input: PubMed publications on relevant topics
Output: Ranked list of leads with propensity scores (0-100)

🚀 Quick Start (3 commands)
bash# 1. Install dependencies
pip install biopython pandas streamlit

# 2. Collect leads from PubMed (takes ~5 min)
python collect_leads.py

# 3. Score the leads
python score_leads.py

# 4. Launch dashboard
streamlit run app.py
✅ You'll have 50-100 scored leads in minutes!

📊 Scoring Methodology
Each lead receives a score from 0-100 based on:
FactorWeightExampleRole Fit30 ptsTitle contains "Director of Toxicology"Company Intent20 ptsWorks at funded pharma companyTechnographic15 ptsPublications mention "3D models"Location10 ptsBased in Cambridge, MA or BaselScientific Intent40 ptsPublished on DILI in last 2 years
Tiers:

🔴 Tier A (80-100): Hot leads - contact immediately
🟠 Tier B (60-79): Warm leads - qualify further
🟢 Tier C (0-59): Cold leads - long-term nurture


📁 Project Structure
biotech-lead-scorer/
├── collect_leads.py      # PubMed scraper
├── score_leads.py        # Scoring engine
├── app.py                # Streamlit dashboard
├── leads_raw.csv         # Raw collected leads
├── leads_scored.csv      # Scored & ranked leads
└── README.md

🔍 Data Sources

PubMed (active): Recent publications on DILI, hepatotoxicity, 3D models
LinkedIn (future): Sales Navigator exports
NIH RePORTER (future): Grant recipients
Conferences (future): SOT, AACR attendees


📈 Sample Output
The dashboard shows:

✅ 50+ leads collected from PubMed
✅ Ranked by propensity score
✅ Filterable by tier, location, company
✅ Exportable to CSV

Top Lead Example:
🔴 Dr. Sarah Johnson (Score: 95/100)
Director of Toxicology at Pfizer
📍 Cambridge, MA
✉️ sarah.johnson@pfizer.com
📄 "Assessment of DILI risk using 3D hepatic spheroids" (2024)

🛠️ Technical Skills Demonstrated

API Integration: Biopython/PubMed NCBI API
Data Processing: Pandas for ETL pipeline
Feature Engineering: Weighted scoring algorithm
Web Development: Streamlit dashboard
NLP: Text parsing for company/location extraction


🚀 Future Enhancements

 Add LinkedIn Sales Navigator integration
 Email enrichment via Hunter.io
 Conference attendee scraping
 Funding data from Crunchbase
 ML-based scoring (XGBoost)


📧 Contact
Sumit Gatade
📧 sumitgatade05@gmail.com
🔗 LinkedIn - https://www.linkedin.com/in/sumit-gatade-b30142295/
💻 GitHub - https://github.com/Sumit2228TM
