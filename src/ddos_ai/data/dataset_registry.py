"""Dataset catalog and metadata registry for DDoS-AI platform."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class DatasetInfo:
    """Metadata describing a DDoS benchmark dataset."""
    dataset_id: str
    name: str
    institution: str
    year: int
    url: str
    sha256_checksum: str
    attack_classes: List[str] = field(default_factory=list)
    format: str = "csv"
    size_description: str = ""
    domain: str = "Enterprise Network"  # e.g., Enterprise, IoT, SDN, Host/Network
    target_column: str = "Label"
    features_count: int = 70


class DatasetRegistry:
    """Central registry of supported benchmark datasets."""

    _REGISTRY: Dict[str, DatasetInfo] = {
        "CIC-DDoS2019": DatasetInfo(
            dataset_id="CIC-DDoS2019",
            name="Canadian Institute for Cybersecurity DDoS 2019",
            institution="University of New Brunswick (UNB)",
            year=2019,
            url="https://www.unb.ca/cic/datasets/ddos-2019.html",
            sha256_checksum="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            attack_classes=[
                "BENIGN", "Syn", "UDP", "UDPLag", "DNS", "LDAP",
                "MSSQL", "NetBIOS", "NTP", "SNMP", "SSDP", "TFTP", "PortScan"
            ],
            format="csv",
            size_description="~50 Million packets across 2 days (Training & Testing)",
            domain="Enterprise Network Volumetric",
            target_column="Label",
            features_count=70,
        ),
        "CIC-IDS2017": DatasetInfo(
            dataset_id="CIC-IDS2017",
            name="Canadian Institute for Cybersecurity IDS 2017 (DDoS Subset)",
            institution="University of New Brunswick (UNB)",
            year=2017,
            url="https://www.unb.ca/cic/datasets/ids-2017.html",
            sha256_checksum="7bf97dd75ff199ba294901f44d8b9456543ee7d4dfbf6b86cf25471d8be7ddc1",
            attack_classes=["BENIGN", "DDoS", "DoS Hulk", "DoS GoldenEye", "DoS slowloris", "DoS Slowhttptest"],
            format="csv",
            size_description="225,745 flows in Friday DDoS capture (77 MB full, 4.8 MB mixed sample)",
            domain="Enterprise Network Intrusion & DDoS",
            target_column="Label",
            features_count=78,
        ),
        "NSL-KDD": DatasetInfo(
            dataset_id="NSL-KDD",
            name="NSL-KDD Network Intrusion & Denial of Service Dataset",
            institution="University of New Brunswick (UNB) / defcom17",
            year=2009,
            url="https://github.com/defcom17/NSL_KDD",
            sha256_checksum="a848981df9709fd0298a44c9b19e2bf4e8db6c6cfdfcfb6eb09cbe7cf8e7924d",
            attack_classes=[
                "normal", "neptune", "smurf", "pod", "teardrop", "land", "back",
                "satan", "ipsweep", "portsweep", "nmap", "warezclient"
            ],
            format="csv",
            size_description="125,973 train records, 22,544 test records (41 networking features)",
            domain="Connection-Level Protocol & DoS",
            target_column="attack_type",
            features_count=41,
        ),
        "SDN-DDoS": DatasetInfo(
            dataset_id="SDN-DDoS",
            name="Software-Defined Networking Volumetric DDoS Dataset",
            institution="University of Blida / IEEE SDN Telemetry",
            year=2020,
            url="https://github.com/aliasar1/DDoS-Detection-SDN",
            sha256_checksum="b9283f5c7ea1b370a256df693d254b73e5cc9697940e4fbc6810a9f73be272fb",
            attack_classes=["BENIGN", "DDoS_TCP", "DDoS_UDP", "DDoS_ICMP"],
            format="csv",
            size_description="104,345 flow entries from OpenFlow SDN switches (12.5 MB)",
            domain="SDN OpenFlow Controller Telemetry",
            target_column="label",
            features_count=22,
        ),
        "BoT-IoT": DatasetInfo(
            dataset_id="BoT-IoT",
            name="The BoT-IoT Dataset",
            institution="UNSW Canberra Cyber",
            year=2018,
            url="https://research.unsw.edu.au/projects/bot-iot-dataset",
            sha256_checksum="4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a",
            attack_classes=["BENIGN", "DDoS_TCP", "DDoS_UDP", "DDoS_HTTP", "DoS_TCP", "DoS_UDP", "Reconnaissance"],
            format="csv",
            size_description="72 Million records (5% sub-dataset and influential features CSV available)",
            domain="Internet of Things (IoT) Volumetric",
            target_column="category",
            features_count=19,
        ),
        "TON_IoT": DatasetInfo(
            dataset_id="TON_IoT",
            name="TON_IoT Heterogeneous Telemetry Network Dataset",
            institution="UNSW Canberra Cyber",
            year=2020,
            url="https://research.unsw.edu.au/projects/toniot-datasets",
            sha256_checksum="ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d",
            attack_classes=["normal", "ddos", "dos", "scanning", "backdoor", "injection", "password", "xss"],
            format="csv",
            size_description="Heterogeneous IoT/IIoT telemetry network flow records",
            domain="IoT & Industrial IoT Telemetry",
            target_column="type",
            features_count=44,
        ),
        "CSE-CIC-IDS2018": DatasetInfo(
            dataset_id="CSE-CIC-IDS2018",
            name="Communications Security Establishment & CIC IDS 2018",
            institution="CSE & UNB (AWS)",
            year=2018,
            url="https://www.unb.ca/cic/datasets/ids-2018.html",
            sha256_checksum="c1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
            attack_classes=["Benign", "DDoS-LOIC-HTTP", "DDoS-HOIC", "DoS-Slowloris"],
            format="csv",
            size_description="16 Million flows captured on AWS",
            domain="Cloud Infrastructure AWS",
            target_column="Label",
            features_count=80,
        ),
    }

    @classmethod
    def get(cls, dataset_id: str) -> Optional[DatasetInfo]:
        """Looks up dataset metadata by exact or case-insensitive ID."""
        if dataset_id in cls._REGISTRY:
            return cls._REGISTRY[dataset_id]
        clean_id = dataset_id.upper().replace("_", "-")
        for k, v in cls._REGISTRY.items():
            if k.upper().replace("_", "-") == clean_id:
                return v
        return None

    @classmethod
    def list_datasets(cls) -> List[str]:
        return list(cls._REGISTRY.keys())
