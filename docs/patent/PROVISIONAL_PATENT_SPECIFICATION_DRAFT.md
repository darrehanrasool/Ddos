FORM 2
THE PATENTS ACT, 1970
(39 of 1970)
&
THE PATENTS RULES, 2003

PROVISIONAL SPECIFICATION
(See Section 10 and Rule 13)

===============================================================================
1. TITLE OF THE INVENTION:
"A SYSTEM AND METHOD FOR HARDWARE-ACCELERATED LINE-RATE INTRUSION PREVENTION 
AND AUTONOMOUS FLOW MITIGATION IN SOFTWARE-DEFINED NETWORKS"
===============================================================================

2. APPLICANT:
(a) NAME: ISLAMIC UNIVERSITY OF SCIENCE AND TECHNOLOGY (IUST)
(b) NATIONALITY: Indian Educational Institution
(c) ADDRESS: 1 University Avenue, Awantipora, Pulwama, Jammu & Kashmir – 192122, India

3. INVENTORS:
(a) NAME: DAR REHAN RASOOL
    NATIONALITY: Indian
    ADDRESS: Centre of Artificial Intelligence, Islamic University of Science and Technology, 
             Awantipora, Pulwama, Jammu & Kashmir – 192122, India

(b) NAME: DR. JAVAD AHMAD
    NATIONALITY: Indian
    ADDRESS: Centre of Artificial Intelligence, Islamic University of Science and Technology, 
             Awantipora, Pulwama, Jammu & Kashmir – 192122, India

(c) NAME: MUNEEB SAYED
    NATIONALITY: Indian
    ADDRESS: Centre of Artificial Intelligence, Islamic University of Science and Technology, 
             Awantipora, Pulwama, Jammu & Kashmir – 192122, India

(d) NAME: SHAFIYA BASHIR PAMPORI
    NATIONALITY: Indian
    ADDRESS: Centre of Artificial Intelligence, Islamic University of Science and Technology, 
             Awantipora, Pulwama, Jammu & Kashmir – 192122, India

===============================================================================
PREAMBLE TO THE DESCRIPTION:
The following specification describes the invention.
===============================================================================

FIELD OF THE INVENTION
[0001] The present invention relates generally to network cybersecurity, high-throughput intrusion prevention systems (IPS), and artificial intelligence. More particularly, the present invention relates to a system and method for hardware-accelerated, line-rate detection and autonomous, closed-loop mitigation of Distributed Denial of Service (DDoS) attacks in high-speed Software-Defined Networks (SDN) and enterprise cloud computing environments.

BACKGROUND OF THE INVENTION AND PRIOR ART
[0002] Distributed Denial of Service (DDoS) attacks represent an existential threat to modern digital infrastructure, capable of overwhelming enterprise gateways, internet service providers (ISPs), and data center switches with traffic exceeding hundreds of gigabits or terabits per second.

[0003] In modern Software-Defined Networking (SDN) architectures, the separation of the data plane (switches) from the control plane (SDN controller) introduces an acute vulnerability. When volumetric or anomalous traffic floods an OpenFlow-enabled network, unmatched packets generate an avalanche of `Packet-In` messages to the central SDN controller. If the intrusion detection mechanism deployed at the controller is unable to process and classify these flows at physical line rate, the control plane suffers CPU and memory starvation, causing the entire network fabric to collapse.

[0004] Prior art attempts to apply deep learning to network intrusion detection have relied heavily on complex sequential and recurrent neural network architectures, such as combinations of Convolutional Neural Networks (CNN), Bidirectional Long Short-Term Memory (BiLSTM) networks, and Multi-Head Attention mechanisms (e.g., Ashfaq Najar et al., 2025). While such recurrent models achieve high theoretical classification metrics on static offline datasets, they suffer from critical technical deficiencies when deployed in real-time production hardware:
    (a) Computational Latency Bottleneck: Recurrent state transitions scale quadratically with sequence length ($\mathcal{O}(T \cdot d^2 + T^2)$) and cannot be natively vectorized across time steps. This imposes per-flow classification latencies exceeding $0.19\text{ ms}$ to $15.0\text{ ms}$, rendering them incapable of handling $10\text{ Gbps}$ or $40\text{ Gbps}$ line rates (where packet arrival intervals are on the order of nanoseconds).
    (b) Resource Exhaustion: Recurrent networks and large Transformers require multi-gigabyte memory footprints and continuous high-power GPU acceleration, rendering them infeasible for edge appliances, smart network interface cards (SmartNICs), and resource-constrained SDN switches.
    (c) Absence of Autonomous Closed-Loop Enforcement: Conventional systems operate as passive intrusion detectors (NIDS) that generate log alerts without directly commanding the underlying network data plane to dynamically enforce rate-limiting, IP-quarantining, or BGP route scrubbing.

[0005] Consequently, there exists an urgent, unfulfilled need in the art for a hardware-aware, line-rate intrusion prevention system that provides sub-millisecond screening latency, minimal memory footprint, and direct closed-loop autonomous mitigation at the network switch layer.

OBJECTS OF THE INVENTION
[0006] The primary object of the present invention is to provide a hardware-accelerated system and method capable of detecting and mitigating DDoS attacks at line rates exceeding 10 Gbps with sub-millisecond per-flow processing latency.

[0007] Another object of the present invention is to provide a cascading dual-tier detection engine wherein a lightweight, histogram-binned integer screening tier dispatches benign and obvious volumetric attacks in microseconds, dynamically invoking a deep residual tabular neural network only for ambiguous, high-entropy flow anomalies.

[0008] Yet another object of the present invention is to provide an autonomous closed-loop mitigation controller that translates multi-tier neural confidence scores directly into active network enforcement primitives (such as OpenFlow flow-mod drop rules, dynamic rate-limiting, and BGP-Flowspec scrubbing).

[0009] Still another object of the present invention is to provide a canonical cross-domain 16-dimensional feature harmonizer that maps heterogeneous enterprise, SDN, and IoT traffic into an invariant topological space incorporating statistical Shannon entropy, packet symmetry ratios, and inter-arrival timing jitter.

[0010] A further object of the present invention is to provide a bounded-memory execution framework optimized for Apple Silicon Metal Performance Shaders (MPS) and CUDA vector units that maintains an operational memory footprint under 150 MB.

SUMMARY OF THE INVENTION
[0011] In accordance with the present invention, there is provided a hardware-accelerated system and method for line-rate intrusion prevention and autonomous flow mitigation in software-defined networks. The system comprises:
    (a) a Canonical Feature Harmonization Module configured to ingest raw telemetry packets at line rate and compute a standardized 16-dimensional flow vector incorporating statistical entropy, bidirectional packet volume symmetry, and timing jitter;
    (b) a Cascading Dual-Tier Inference Engine comprising:
        (i) a Tier-1 Histogram-Binned Decision Engine operating on pre-computed integer quantile bins with $\mathcal{O}(1)$ computational complexity, configured to evaluate flow vectors in under $0.002\text{ ms}$ ($1.9\text{ microseconds}$), discharging definitive benign traffic and obvious volumetric floods; and
        (ii) a Tier-2 Deep Tabular Residual Neural Network comprising multiple linear layers with LayerNorm and residual skip connections, selectively triggered solely when the Tier-1 decision confidence falls within an ambiguous boundary threshold ($0.20 \le P \le 0.85$);
    (c) an Autonomous Closed-Loop Mitigation Controller operatively connected to the dual-tier engine, configured to automatically generate and push OpenFlow, ACL, and BGP-Flowspec rules to physical and virtual network switches in real time; and
    (d) a Hardware-Aware Unified Memory Acceleration Layer executing tensor operations natively on unified memory graphics/neural accelerators with bounded memory consumption under $150\text{ MB}$.

BRIEF DESCRIPTION OF THE DRAWINGS
[0012] The invention will be described with reference to the accompanying drawings, in which:
    - FIG. 1 illustrates the overall topological architecture of the software-defined network incorporating the hardware-accelerated intrusion prevention system.
    - FIG. 2 illustrates the detailed structural architecture of the Cascading Dual-Tier Inference Engine and its routing pathways.
    - FIG. 3 is a logic flowchart depicting the real-time flow evaluation, ambiguity threshold gating, and autonomous mitigation actuation process.
    - FIG. 4 is a graph comparing the per-flow latency and throughput of the present invention against prior art recurrent BiLSTM-Attention baselines.

DETAILED DESCRIPTION OF THE PREFERRED EMBODIMENTS
[0013] Referring to FIG. 1 and FIG. 2, the system comprises a high-throughput network ingestion interface coupled to a canonical feature extraction pipeline. As raw ingress packets arrive from physical interfaces (e.g., `en0`) or virtual tunnels (e.g., `utun`, OpenFlow switches), flows are tracked using a bidirectional 5-tuple key:
    $$\text{FlowKey} = \langle \text{SrcIP}, \text{DstIP}, \text{SrcPort}, \text{DstPort}, \text{Protocol} \rangle$$

[0014] The Feature Harmonization Module extracts 16 standardized features representing:
    1. Bidirectional packet counts and volume ratios:
       $$R_{\text{pkt}} = \frac{N_{\text{fwd}}}{N_{\text{fwd}} + N_{\text{bwd}} + \epsilon}$$
    2. Statistical Shannon entropy of packet lengths across rolling sliding windows:
       $$H(X) = - \sum_{i=1}^{k} P(x_i) \log_2 P(x_i)$$
    3. Inter-Arrival Time (IAT) variance and forward/backward byte velocity:
       $$V_{\text{bytes}} = \frac{\sum \text{Bytes}}{\Delta T}$$
    4. TCP control flag density (SYN-ACK ratio, RST frequency, FIN anomalies).

[0015] In accordance with a core aspect of the invention, the flow vector is first processed by the Tier-1 Histogram-Binned Decision Engine. Continuous features are discretized into 256 integer quantile bins, allowing decision tree threshold evaluations to execute via direct array index lookups in cache memory without floating-point division. The Tier-1 engine computes an anomaly probability score $P_{\text{tier1}}$.
    - If $P_{\text{tier1}} < 0.20$, the flow is definitively classified as benign and instantly granted a `PASS` directive without invoking neural network inference.
    - If $P_{\text{tier1}} > 0.85$, the flow is flagged as a catastrophic volumetric flood, triggering an immediate `ACL_BLOCK_IP` rule at the switch ASIC.
    - If $0.20 \le P_{\text{tier1}} \le 0.85$, the flow represents an ambiguous burst or low-rate application attack and is dynamically routed to Tier-2.

[0016] The Tier-2 Deep Tabular Residual Neural Network comprises an input projection layer, followed by a sequence of residual MLP blocks with Layer Normalization, Gaussian Error Linear Unit (GELU) activations, and residual skip connections:
    $$y = \text{GELU}(\text{LayerNorm}(W_2 \cdot \text{GELU}(\text{LayerNorm}(W_1 x + b_1)) + b_2)) + x$$
This skip connection enables gradient propagation without degradation, allowing the model to accurately detect stealthy slow-rate attacks, high-entropy spoofing, and zero-day variants.

[0017] In another preferred embodiment, the mitigation controller enforces proportional closed-loop responses based on the synthesized risk score $S_{\text{risk}}$:
    - Normal Flow ($S_{\text{risk}} < 0.30$): Forward normally (`PASS`).
    - Early Volumetric Burst ($0.30 \le S_{\text{risk}} < 0.60$): Apply token-bucket policing (`RATE_LIMIT_50PCT`).
    - Suspicious Stateful Anomaly ($0.60 \le S_{\text{risk}} < 0.80$): Divert to sandboxed inspection (`QUARANTINE_FLOW`).
    - High-Rate Reflection Flood ($0.80 \le S_{\text{risk}} < 0.95$): Inject upstream scrubbing route (`BGP_FLOWSPEC_SCRUB`).
    - Hostile Botnet Endpoint ($S_{\text{risk}} \ge 0.95$): Drop at ingress switch hardware (`ACL_BLOCK_IP`).

WORKING EXAMPLE & BENCHMARK VALIDATION
[0018] The system was implemented and evaluated on an Apple Silicon unified memory platform (Apple M4, Metal Performance Shaders) using the InSDN and CIC-DDoS2019 standard datasets. Under rigorous testing against the state-of-the-art recurrent baseline (Ashfaq Najar et al., 2025 CNN-BiLSTM-Attention):
    - The present invention achieved an average cascading latency of $0.0128\text{ ms}$ ($12.8\text{ microseconds}$), representing a $14.9\times$ acceleration over the baseline ($0.1907\text{ ms}$).
    - Throughput reached $78,035\text{ flows per second}$ on a single core, compared to $5,243\text{ flows per second}$ for the baseline (a $1,388\%$ improvement).
    - Classification performance was sustained at $96.09\%$ F1-score with zero packet loss at $10\text{ Gbps}$ simulated line rate, while maintaining memory consumption below $142\text{ MB}$.

PRELIMINARY CLAIMS SCOPE (TO BE EXPANDED IN COMPLETE SPECIFICATION)
[0019] Having described the invention, what is primarily contemplated to be claimed includes:
    1. A hardware-accelerated intrusion prevention system for software-defined networks comprising a canonical feature extraction module, a cascading dual-tier inference engine, an autonomous closed-loop mitigation controller, and a unified memory acceleration layer.
    2. The system of claim 1, wherein said dual-tier engine executes an $\mathcal{O}(1)$ histogram-binned integer screening tier with latency under $0.002\text{ ms}$, cascading ambiguous flows within a predefined probability interval to a deep tabular residual neural network.
    3. The system of claim 1, wherein said closed-loop mitigation controller translates continuous neural confidence outputs into discrete proportional switch primitives comprising dynamic rate-limiting, flow quarantine, and upstream BGP scrubbing.
    4. A method for line-rate DDoS prevention comprising the steps of extracting 16 canonical features, screening via histogram quantile bins, selectively executing deep residual inference, and autonomously issuing OpenFlow control commands.

===============================================================================
Dated this 21st day of October, 2026.

SIGNATURE OF APPLICANT / AGENT:

________________________________________
(Registrar / Authorized Signatory)
Islamic University of Science and Technology (IUST)
Awantipora, Pulwama, Jammu & Kashmir, India
===============================================================================
