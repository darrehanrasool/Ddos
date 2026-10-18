# Known Limitations & Threat Model

## 1. Adversarial Evasion Vulnerability
Attackers employing gradient-based perturbation techniques (e.g. FGSM, PGD, or Carlini-Wagner adapted to tabular flow features) can inject small amounts of dummy payload data or manipulate inter-arrival delays. While our adversarial training and autoencoder mitigation reduce this threat, advanced attackers may still degrade detection confidence.

## 2. Flash Crowd vs. DDoS Ambiguity
Legitimate flash crowds (e.g., breaking news, major product releases, or streaming events) mimic volumetric DDoS attacks in terms of destination port concentration and aggregate bandwidth. Although packet inter-arrival time distributions and source IP entropy differ, aggressive rate-limiting rules may inadvertently throttle legitimate users.

## 3. Encrypted Traffic (QUIC / TLS 1.3)
DDoS-AI operates on flow metadata rather than payload inspection, making it robust against payload encryption. However, modern transport protocols such as QUIC (over UDP) and TLS 1.3 with Encrypted Client Hello (ECH) obscure server name indications (SNI), limiting application-layer classification to behavioral flow timing and packet size distributions.

## 4. Asymmetric Routing
In large enterprise or ISP networks, traffic may route through asymmetric paths (forward packets traversing Router A, reverse responses traversing Router B). In such topologies, unidirectional flow collectors cannot accurately compute bidirectional features (e.g., `Bwd Packet Length Mean`), degrading model precision unless collector synchronization is enabled.
