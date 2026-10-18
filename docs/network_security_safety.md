# Operational Safety & Security Policy: DDoS Defense

## 1. Safety Principles for Automated Mitigation
Automated mitigation actions (e.g., dynamic BGP blackholing, OpenFlow rule insertion, or iptables rate-limiting) must follow strict fail-safe guardrails:

1. **Never Drop Infrastructure Traffic**:
   - Hardcoded whitelists for core DNS root servers, internal Active Directory domain controllers, BGP peer routers, and NTP stratum servers must never be blocked regardless of classifier output.
2. **Two-Tier Mitigation Actions**:
   - **Low Confidence ($0.50 \le P < 0.85$)**: Trigger TCP SYN cookies, CAPTCHA challenges, or rate-limiting into a priority queue without dropping traffic.
   - **High Confidence ($P \ge 0.85$)**: Enact temporary flow throttling or route to scrubbing centers with a strict 300-second maximum lease time before re-evaluation.
3. **Fail-Open Policy**:
   - In the event of hardware accelerator failure, OOM exception, or daemon crash, network switches MUST default to fail-open (pass-through) mode to prevent an AI outage from causing an unintended denial of service.
4. **Audit Logging & SOC Accountability**:
   - Every block or rate-limit decision generates an immutable cryptographic log entry containing flow features, SHAP top-3 contributing factors, model timestamp, and confidence score.
