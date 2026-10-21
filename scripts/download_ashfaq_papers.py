#!/usr/bin/env python3
"""Automated Paper Downloader & Direct Access Helper for Dr. Ashfaq Ahmad Najar's Publications.

Assists in downloading and opening official PDFs from Elsevier ScienceDirect, Wiley,
and ResearchGate directly into the papers/pdf/ directory.
"""

import argparse
import os
import sys
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PDF_DIR = ROOT / "papers" / "pdf"
PDF_DIR.mkdir(parents=True, exist_ok=True)

PAPERS = [
    {
        "id": "paper_1_cnn_bilstm_attention",
        "title": "DDoS attack detection using CNN-BiLSTM with attention mechanism",
        "journal": "Telematics and Informatics Reports (Elsevier, June 2025)",
        "doi": "10.1016/j.teler.2025.100211",
        "url": "https://doi.org/10.1016/j.teler.2025.100211",
        "direct_link": "https://www.sciencedirect.com/science/article/pii/S277258552400085X",
        "researchgate": "https://www.researchgate.net/profile/Ashfaq-Najar",
        "filename": "najar_2025_cnn_bilstm_attention.pdf",
    },
    {
        "id": "paper_2_cybersecure_sdn_cnn",
        "title": "Cyber-secure SDN: A CNN-based approach for efficient detection and mitigation of DDoS attacks",
        "journal": "Computers & Security (Elsevier, April 2024)",
        "doi": "10.1016/j.cose.2024.103716",
        "url": "https://doi.org/10.1016/j.cose.2024.103716",
        "direct_link": "https://www.sciencedirect.com/science/article/pii/S016740482400045X",
        "researchgate": "https://www.researchgate.net/profile/Ashfaq-Najar",
        "filename": "najar_2024_cybersecure_sdn_cnn.pdf",
    },
    {
        "id": "paper_3_robust_ddos_cnn",
        "title": "A Robust DDoS Intrusion Detection System Using Convolutional Neural Network",
        "journal": "Computers and Electrical Engineering (Elsevier, 2024)",
        "doi": "10.1016/j.compeleceng.2024.109277",
        "url": "https://doi.org/10.1016/j.compeleceng.2024.109277",
        "direct_link": "https://www.sciencedirect.com/science/article/pii/S004579062400260X",
        "researchgate": "https://www.researchgate.net/publication/380295240",
        "filename": "najar_2024_robust_ddos_cnn.pdf",
    },
    {
        "id": "paper_4_lids_lightweight_ids",
        "title": "LIDS: A Novel Lightweight Intrusion Detection System for DDoS Attacks",
        "journal": "Security and Privacy (Wiley, 2025)",
        "doi": "10.1002/spy2.412",
        "url": "https://doi.org/10.1002/spy2.412",
        "direct_link": "https://onlinelibrary.wiley.com/doi/10.1002/spy2.412",
        "researchgate": "https://www.researchgate.net/profile/Ashfaq-Najar",
        "filename": "najar_2025_lids_lightweight_ids.pdf",
    },
]


def main():
    parser = argparse.ArgumentParser(description="Download Dr. Ashfaq Ahmad Najar's Research Papers")
    parser.add_argument("--open-browser", action="store_true", help="Open all direct ScienceDirect/DOI download links in browser")
    args = parser.parse_args()

    print("=" * 80)
    print("      DR. ASHFAQ AHMAD NAJAR: RESEARCH PAPERS DIRECT ACCESS DIRECTORY       ")
    print("=" * 80)
    print(" Target Folder for PDFs: papers/pdf/\n")

    for i, p in enumerate(PAPERS, start=1):
        target_path = PDF_DIR / p["filename"]
        status = "[EXISTS LOCALLY]" if target_path.exists() else "[NEEDS DOWNLOAD]"
        print(f"[{i}] {p['title']}")
        print(f"    Journal:     {p['journal']}")
        print(f"    DOI URL:     {p['url']}")
        print(f"    ScienceDir:  {p['direct_link']}")
        print(f"    Target PDF:  papers/pdf/{p['filename']} ({status})")
        print("-" * 80)

    print("\n[+] Instructions to save PDFs into your repository:")
    print("    1. Click the links above to open the papers via your IUST university network.")
    print("    2. Click 'Download PDF' on ScienceDirect / ResearchGate.")
    print("    3. Save the PDF files directly into the 'papers/pdf/' folder.")
    print("=" * 80)

    if args.open_browser:
        print("\n[+] Opening direct paper download portals in your default browser...")
        for p in PAPERS:
            webbrowser.open(p["direct_link"])


if __name__ == "__main__":
    main()
