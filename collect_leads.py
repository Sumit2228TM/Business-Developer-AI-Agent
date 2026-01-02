# collect_leads.py - MINIMAL VERSION FOR 10-HOUR DEMO
# Run this first: pip install biopython pandas

from Bio import Entrez
from datetime import datetime, timedelta
import pandas as pd
import json

Entrez.email = "sumitgatade05@gmail.com"  # Required by NCBI

def collect_biotech_leads():
    """
    Collect leads from PubMed in ONE function
    Target: 50-100 leads in under 2 hours
    """
    print("🧬 Starting lead collection...")
    
    # Keywords from the assignment
    keywords = [
        "DILI", "drug-induced liver injury", "hepatotoxicity",
        "3D cell culture", "organoid", "spheroid", "in vitro toxicity"
    ]
    
    all_leads = []
    
    for keyword in keywords:
        print(f"\n📡 Searching: {keyword}")
        
        # Search PubMed
        query = f'"{keyword}"[Title/Abstract] AND (2023[PDAT] : 3000[PDAT])'
        
        try:
            # Get paper IDs
            handle = Entrez.esearch(db="pubmed", term=query, retmax=20)
            record = Entrez.read(handle)
            pmids = record["IdList"]
            handle.close()
            
            if not pmids:
                continue
            
            print(f"   Found {len(pmids)} papers")
            
            # Get paper details
            handle = Entrez.efetch(db="pubmed", id=pmids, retmode="xml")
            papers = Entrez.read(handle)
            handle.close()
            
            # Extract authors
            for paper in papers['PubmedArticle']:
                try:
                    article = paper['MedlineCitation']['Article']
                    
                    # Get publication date
                    pub_date = article.get('ArticleDate', [{}])
                    if pub_date:
                        year = pub_date[0].get('Year', '')
                        month = pub_date[0].get('Month', '01').zfill(2)
                        date_str = f"{year}-{month}"
                    else:
                        date_str = "2024-01"
                    
                    # Extract ALL authors (not just corresponding)
                    for author in article.get('AuthorList', []):
                        first = author.get('ForeName', '')
                        last = author.get('LastName', '')
                        name = f"{first} {last}".strip()
                        
                        if not name or len(name) < 5:
                            continue
                        
                        # Get affiliation
                        aff_list = author.get('AffiliationInfo', [])
                        affiliation = aff_list[0].get('Affiliation', '') if aff_list else ''
                        
                        # Extract company
                        company = extract_company(affiliation)
                        location = extract_location(affiliation)
                        
                        # Create lead
                        lead = {
                            "name": name,
                            "title": "Researcher",  # Default
                            "company": company,
                            "location": location,
                            "email": guess_email(name, company),
                            "linkedin": f"linkedin.com/in/{name.lower().replace(' ', '')}",
                            "recent_publication": article.get('ArticleTitle', '')[:100],
                            "pub_date": date_str,
                            "journal": article.get('Journal', {}).get('Title', ''),
                            "pmid": str(paper['MedlineCitation']['PMID']),
                            "keywords": keyword,
                            "source": "PubMed"
                        }
                        
                        all_leads.append(lead)
                        
                except Exception as e:
                    continue
        
        except Exception as e:
            print(f"   ⚠️  Error: {e}")
            continue
    
    # Remove duplicates by name
    seen = set()
    unique_leads = []
    for lead in all_leads:
        if lead["name"] not in seen:
            seen.add(lead["name"])
            unique_leads.append(lead)
    
    print(f"\n✅ Collected {len(unique_leads)} unique leads")
    
    # Save to CSV
    df = pd.DataFrame(unique_leads)
    df.to_csv("leads_raw.csv", index=False)
    print(f"💾 Saved to leads_raw.csv")
    
    return unique_leads


def extract_company(affiliation):
    """Extract company name from affiliation"""
    if not affiliation:
        return "Unknown"
    
    # Split by comma
    parts = [p.strip() for p in affiliation.split(',')]
    
    # Remove USA, UK, etc
    parts = [p for p in parts if p not in ['USA', 'US', 'UK', 'EU'] and len(p) > 2]
    
    # Usually company is 2nd element
    if len(parts) >= 2:
        return parts[1]
    elif len(parts) == 1:
        return parts[0]
    
    return "Unknown"


def extract_location(affiliation):
    """Extract location from affiliation"""
    if not affiliation:
        return "Unknown"
    
    # Common biotech hubs
    hubs = {
        "Cambridge": "Cambridge, MA",
        "Boston": "Boston, MA",
        "San Francisco": "San Francisco, CA",
        "San Diego": "San Diego, CA",
        "Basel": "Basel, Switzerland",
        "Oxford": "Oxford, UK"
    }
    
    for hub, full_name in hubs.items():
        if hub in affiliation:
            return full_name
    
    # Just return last part (usually city, state)
    parts = affiliation.split(',')
    if len(parts) >= 2:
        return f"{parts[-2].strip()}, {parts[-1].strip()}"
    
    return "Unknown"


def guess_email(name, company):
    """Guess email format"""
    if not name or not company or company == "Unknown":
        return ""
    
    parts = name.lower().split()
    if len(parts) < 2:
        return ""
    
    first, last = parts[0], parts[-1]
    domain = company.lower().replace(" ", "").replace("university", "edu").replace("institute", "org")
    
    # Add .com if no extension
    if '.' not in domain:
        domain += ".com"
    
    return f"{first}.{last}@{domain}"


if __name__ == "__main__":
    leads = collect_biotech_leads()
    print(f"\n🎉 Collection complete! Run 'python score_leads.py' next")