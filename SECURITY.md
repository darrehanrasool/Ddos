# Security Policy

## Overview

The **DDoS-AI** project is an artificial intelligence-driven network security and intrusion prevention platform designed for high-throughput network environments, Software-Defined Networks (SDN), and cloud infrastructure.

Because this platform processes network telemetry, packet flows, and critical mitigation rules, we place the utmost importance on software reliability, model integrity, and defensiveness. We welcome responsible security research and vulnerability disclosures from the community.

---

## Supported Versions

Security updates, patches, and vulnerability fixes are prioritized for the active codebase:

| Version / Branch | Supported | Notes |
| :--- | :--- | :--- |
| `main` (Latest) | :white_check_mark: Active | Actively maintained with current bug and security fixes |
| `v1.0.x` | :white_check_mark: Active | Stable release series |
| `< v1.0.0` | :x: Unsupported | Legacy / initial development snapshots |

We strongly recommend running the latest release or staying synchronized with the `main` branch to ensure you have the latest security and stability enhancements.

---

## Reporting a Vulnerability

If you discover a security vulnerability or security-sensitive defect in DDoS-AI, **please do NOT open a public GitHub issue or disclose the vulnerability publicly.** Public disclosure puts users and network testbeds at risk.

Instead, please submit your findings through one of the following responsible disclosure channels:

### 1. GitHub Security Advisory (Recommended)
You can report a private vulnerability directly through GitHub:
- Navigate to the repository's **Security** tab.
- Click **Advisories** -> **Report a vulnerability** (or visit [Security Advisories](https://github.com/darrehanrasool/Ddos/security/advisories/new)).
- Provide complete details of your finding. This maintains private communication between you and the maintainers until a patch is issued.

### 2. Direct Confidential Email
If you prefer email, please reach out to the project leadership:
- **Lead Author & Maintainer**: Dar Rehan Rasool ([rehanrasool@iust.ac.in](mailto:rehanrasool@iust.ac.in))
- **Faculty Supervisor**: Dr. Javad Ahmad, Centre of Artificial Intelligence (CAI), Islamic University of Science and Technology (IUST)

### Information to Include in Your Report

To help us investigate, triage, and resolve the issue quickly, please provide:
1. **Component Affected**: The specific module, script, or model component (e.g., `ddos_ai.pipeline`, `packet_capture`, `dashboard`, `feature_extraction`).
2. **Vulnerability Description**: A concise explanation of the vulnerability, attack vector, and potential impact (e.g., privilege escalation, denial-of-service against the monitoring pipeline, remote code execution via unsafe deserialization, or mitigation bypass).
3. **Step-by-Step Reproduction Steps**: A minimal, reproducible proof-of-concept (PoC) script, PCAP sample, or step-by-step instructions.
4. **Environment Details**: Operating system (macOS / Linux), Python version, PyTorch version, and relevant dependencies.
5. **Suggested Mitigation (Optional)**: Any suggested code fixes or configuration changes.

---

## Scope of Security Research

### In-Scope Areas
The following areas are of primary importance to the security of the DDoS-AI platform:

- **Model Checkpoint Deserialization**: Integrity verification, safe loading of weights, and protection against malicious serialization payloads (e.g., untrusted pickle code execution).
- **Packet Parsers & Telemetry Ingestion**: Memory safety, bounds checking, and robustness of packet decoders against malformed, fragmented, or corrupted PCAPs and network flows.
- **Algorithmic Complexity & Resource Exhaustion**: Defending the dual-tier cascading pipeline and feature calculators against deliberate algorithmic worst-case exhaustion attacks.
- **Mitigation & ACL Synthesis**: Ensuring that OpenFlow / iptables / eBPF rule generation cannot be manipulated into blackholing legitimate critical infrastructure traffic.
- **API & Web Dashboard**: Input validation, cross-site scripting (XSS), cross-origin request forgery (CSRF), and unauthorized control actions on the management interface.

### Out-of-Scope
The following are considered out of scope and do not qualify as valid security vulnerabilities:

- Reports generated solely by automated scanning tools without a verified, actionable proof-of-concept.
- Denial-of-service attacks directed at public documentation hosts, institutional web servers, or third-party git infrastructure.
- Social engineering, phishing, or physical attacks against project researchers or university personnel.
- Weaknesses requiring root / administrative access already compromised on the host running the software.
- Attacks relying on heavily customized, unsupported modifications to the core codebase.

---

## Response & Disclosure Process

We follow a coordinated and transparent vulnerability resolution process:

1. **Initial Acknowledgment**: We will acknowledge receipt of your vulnerability report within **48 hours**.
2. **Triage & Validation**: The maintainers will analyze and reproduce the reported issue within **5 business days**, confirming its severity and impact.
3. **Remediation & Patch Development**: A fix will be developed in a private branch, verified against our continuous integration test suite, and backported if necessary.
4. **Coordinated Disclosure**: We aim to release a patch and security advisory within **30 to 60 days** of initial triage. If you wish, we will publicly credit your contribution and research in the release notes and advisory.

---

## Safe Harbor & Ethical Research

We consider security research conducted under this policy to be authorized and protected under our safe harbor principles:
- You make a good-faith effort to avoid privacy violations, data destruction, and service degradation.
- You do not access, alter, or retain data belonging to other users or institutions.
- You communicate privately with maintainers and give us reasonable time to resolve the issue before public disclosure.

Thank you for helping keep the DDoS-AI research platform secure!
