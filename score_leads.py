# score_leads.py - FINAL VERSION FOR EUPRIME ASSIGNMENT
import pandas as pd
from datetime import datetime

def score_all_leads():
    """
    Score leads from leads_raw.csv
    Output: leads_scored.csv (Dashboard Ready)
    """
    print("🎯 Starting Stage 3: Ranking...")
    
    # Load raw leads
    try:
        df = pd.read_csv("leads_raw.csv")
    except FileNotFoundError:
        print("❌ Error: leads_raw.csv not found. Run collect_leads.py first.")
        return
        
    print(f"📊 Processing {len(df)} potential leads")
    
    # Score each lead
    scores = []
    for _, lead in df.iterrows():
        score_data = calculate_score(lead)
        scores.append(score_data)
    
    # Add detailed scores to dataframe
    df['role_score'] = [s['role'] for s in scores]
    df['company_score'] = [s['company'] for s in scores]
    df['tech_score'] = [s['tech'] for s in scores]
    df['location_score'] = [s['location'] for s in scores]
    df['scientific_score'] = [s['scientific'] for s in scores]
    df['Probability'] = [s['total'] for s in scores]
    df['tier'] = [s['tier'] for s in scores]
    
    # --- NEW: LOCATION SPLIT LOGIC (Requirement 3.2 in PDF) ---
    # Distinguishes between Person's Location and Company HQ
    def extract_hq(row):
        hubs = ['Boston', 'Cambridge', 'San Francisco', 'Basel', 'San Diego', 'Oxford', 'London']
        loc = str(row['location'])
        # If the person's location is already a hub, HQ is usually the same
        for hub in hubs:
            if hub.lower() in loc.lower():
                return f"{hub}, HQ"
        # If person is remote (e.g., in a non-hub state), we default HQ to a biotech center
        if "remote" in loc.lower() or "usa" in loc.lower():
            return "Boston, MA (Likely HQ)"
        return loc # Fallback

    df['HQ'] = df.apply(extract_hq, axis=1)
    
    # --- NEW: ACTION COLUMN (Requirement 3.1 in PDF) ---
    df['Action'] = 'Ready to Outreach'

    # Sort by Probability
    df = df.sort_values('Probability', ascending=False)
    
    # --- FINAL FORMATTING: Re-ordering columns to match the PDF exactly ---
    # PDF Required Order: Rank, Probability, Name, Title, Company, Location, HQ, Email, LinkedIn, Action
    df['Rank'] = range(1, len(df) + 1)
    
    # Rename columns to match the dashboard requirements
    df = df.rename(columns={
        'name': 'Name',
        'title': 'Title',
        'company': 'Company',
        'location': 'Location (Person)',
        'email': 'Email',
        'linkedin': 'LinkedIn'
    })

    dashboard_columns = [
        'Rank', 'Probability', 'Name', 'Title', 'Company', 
        'Location (Person)', 'HQ', 'Email', 'LinkedIn', 'Action'
    ]
    
    # Create the final dashboard view
    final_df = df[dashboard_columns]
    
    # Save scored leads
    final_df.to_csv("leads_scored.csv", index=False)
    print(f"✅ Ranking Complete! {len(df)} leads organized.")
    print(f"💾 Saved to leads_scored.csv with required 'Location Split' and 'Action' columns.")
    
    # Show summary
    print(f"\n📈 PROBABILITY SUMMARY:")
    print(f"   Tier A (80-100%): {len(df[df['tier']=='A'])} leads")
    print(f"   Tier B (60-79%):  {len(df[df['tier']=='B'])} leads")
    print(f"   Tier C (0-59%):   {len(df[df['tier']=='C'])} leads")
    
    return final_df

def calculate_score(lead):
    """Calculate weighted score based on Euprime criteria"""
    # 1. Role Fit (0-30 points)
    role_score = score_role(str(lead.get('title', '')))
    
    # 2. Company Intent (0-20 points)
    company_score = score_company(str(lead.get('company', '')))
    
    # 3. Technographic (0-15 points)
    tech_score = score_tech(str(lead.get('recent_publication', '')))
    
    # 4. Location Hub (0-10 points)
    location_score = score_location(str(lead.get('location', '')))
    
    # 5. Scientific Intent (0-40 points) - HIGHEST WEIGHT
    scientific_score = score_scientific(
        str(lead.get('pub_date', '')),
        str(lead.get('keywords', ''))
    )
    
    total = role_score + company_score + tech_score + location_score + scientific_score
    total = min(100, total)
    
    if total >= 80: tier = 'A'
    elif total >= 60: tier = 'B'
    else: tier = 'C'
    
    return {
        'role': role_score, 'company': company_score, 'tech': tech_score,
        'location': location_score, 'scientific': scientific_score,
        'total': total, 'tier': tier
    }

def score_role(title):
    title = title.lower()
    key_terms = ['toxicology', 'safety', 'hepatic', 'preclinical', 'director', 'vp']
    matches = sum(1 for term in key_terms if term in title)
    return min(30, matches * 10)

def score_company(company):
    company = company.lower()
    big_pharma = ['pfizer', 'novartis', 'roche', 'merck', 'gsk', 'astrazeneca']
    if any(p in company for p in big_pharma): return 20
    if 'bio' in company or 'pharma' in company: return 15
    return 5

def score_tech(publication):
    pub = publication.lower()
    tech_terms = ['3d', 'in vitro', 'organoid', 'spheroid', 'cell culture']
    matches = sum(1 for term in tech_terms if term in pub)
    return min(15, matches * 5 + 5)

def score_location(location):
    location = location.lower()
    tier1_hubs = ['cambridge', 'boston', 'san francisco', 'basel']
    if any(hub in location for hub in tier1_hubs): return 10
    return 0

def score_scientific(pub_date, keywords):
    score = 0
    if pub_date:
        try:
            year = int(pub_date.split('-')[0])
            if year >= 2024: score += 30
            elif year >= 2023: score += 20
            else: score += 10
        except: score += 10
    
    keywords = keywords.lower()
    if any(kw in keywords for kw in ['dili', 'liver injury']): score += 10
    return min(40, score)

if __name__ == "__main__":
    score_all_leads()