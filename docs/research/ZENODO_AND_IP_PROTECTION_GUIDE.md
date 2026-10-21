# Zenodo Integration & Intellectual Property Protection Guide
**Centre of Artificial Intelligence (CAI)**  
**Islamic University of Science and Technology (IUST), Awantipora, Kashmir**  
*Project: DDoS-AI*  
*Authors: Dar Rehan Rasool, Muneeb Sayed, Shafiya Bashir Pampori, Dr. Javad Ahmad*

---

## 🛡️ Why Zenodo Protects Your Work

[Zenodo](https://zenodo.org/) is an open scientific archive operated by **CERN** (the European Organization for Nuclear Research). 

When you connect your GitHub repository to Zenodo:
1. **Permanent Digital Object Identifier (DOI)**: Your code, model architecture, and benchmarks receive an immutable, internationally recognized DOI (e.g., `10.5281/zenodo.XXXXXXX`).
2. **Legal Priority Timestamp**: It creates unalterable timestamped proof that **your team at IUST created this system on this exact date**. If another researcher or competitor ever tries to steal or copy your code, your Zenodo record legally predates them.
3. **Academic Indexing**: Zenodo automatically indexes your repository in **OpenAIRE, DataCite, Google Scholar**, and university library catalogs.
4. **Permanent Archive**: Even if GitHub went down or someone deleted the repo, the code snapshot is preserved forever in CERN's high-security data centers in Geneva, Switzerland.

---

## 🚀 Step-by-Step Instructions: Connect GitHub to Zenodo

Follow these simple steps in your web browser:

### Step 1: Log in to Zenodo with GitHub
1. Open your browser and navigate to: [https://zenodo.org/](https://zenodo.org/)
2. In the top right corner, click **Log in**.
3. Choose **"Log in with GitHub"** (this securely authenticates your GitHub account with Zenodo).
4. Authorize Zenodo to access your public/private repositories.

---

### Step 2: Enable the DDoS-AI Repository
1. Once logged in, click your profile icon in the top right corner and select **"GitHub"** (or visit [https://zenodo.org/account/settings/github/](https://zenodo.org/account/settings/github/)).
2. You will see a list of your GitHub repositories.
3. Find **`DDoS-AI`** (or `Ddos`).
4. Flip the toggle switch next to `DDoS-AI` from **OFF to ON** (it turns green).
   > *Zenodo is now listening for any release tags you create on GitHub!*

---

### Step 3: Publish Your First Release on GitHub
Zenodo only mints a DOI when you create a formal **Release** in GitHub:

1. Push your latest commits to GitHub:
   ```bash
   git add .
   git commit -m "feat: strict academic license, zenodo metadata, and citation"
   git push origin main
   ```
2. Go to your repository on GitHub: `https://github.com/darrehanrasool/DDoS-AI`
3. On the right sidebar, click **"Releases"** (or click **"Create a new release"**).
4. Click **"Draft a new release"**:
   - **Tag version**: Type `v1.0.0` and select *Create new tag*.
   - **Target**: `main`
   - **Release title**: `DDoS-AI v1.0.0: High-Throughput Dual-Tier DDoS Defense Platform`
   - **Description**: Click *Generate release notes* or paste the summary from `README.md`.
5. Click the green button: **"Publish release"**.

---

### Step 4: Retrieve Your Official DOI Badge
1. Within 60 seconds of publishing the release, switch back to [Zenodo GitHub Settings](https://zenodo.org/account/settings/github/).
2. Click on `DDoS-AI`.
3. You will see your newly generated **DOI badge** (e.g., `10.5281/zenodo.14892345`).
4. Click the badge, copy the Markdown snippet, and update the badge link in `README.md`.

---

## 📋 Automatic Metadata Pre-Configuration

To save you time, the following configuration files have already been created in this repository:

1. [`.zenodo.json`](file:///Users/darrehanrasool/Desktop/Ddos/.zenodo.json):
   - Automatically populates the official title, abstract, keywords, and creators (**Dar Rehan Rasool**, **Muneeb Sayed**, **Shafiya Bashir Pampori**, and **Dr. Javad Ahmad**) with **IUST** affiliation.
   - Automatically sets the license to `cc-by-nc-nd-4.0` (Attribution-NonCommercial-NoDerivatives) on Zenodo.

2. [`CITATION.cff`](file:///Users/darrehanrasool/Desktop/Ddos/CITATION.cff):
   - Enables GitHub's native **"Cite this repository"** button in the right sidebar. Any scholar visiting your GitHub repo can click one button to copy the exact BibTeX citation with all authors and IUST affiliation.

3. [`LICENSE`](file:///Users/darrehanrasool/Desktop/Ddos/LICENSE):
   - Replaced permissive Apache 2.0 with the **Strict Academic & Non-Commercial Research Evaluation License** (All Rights Reserved).

---

## 🔒 3 Critical Security Rules for GitHub

1. **Keep Private until Paper Submission**: If you are writing a research paper with Dr. Javad Ahmad for an IEEE/Elsevier journal, keep the repository **Private** on GitHub. Only invite your team members as collaborators. Once submitted or accepted, switch it to **Public**.
2. **Never Commit Secrets**: Ensure `.env` or any sensitive API keys remain in `.gitignore`. (Already configured).
3. **Branch Protection**: On GitHub, go to *Settings → Branches → Add branch protection rule* for `main`, requiring pull request reviews before merging.
