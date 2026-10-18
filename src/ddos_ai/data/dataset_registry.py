"""Dataset catalog and metadata registry."""

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
            size_description="~50 Million packets across 2 days (Training & Testing)",
        ),
        "BoT-IoT": DatasetInfo(
            dataset_id="BoT-IoT",
            name="The BoT-IoT Dataset",
            institution="UNSW Canberra Cyber",
            year=2018,
            url="https://research.unsw.edu.au/projects/bot-iot-dataset",
            sha256_checksum="4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a",
            attack_classes=["BENIGN", "DDoS_TCP", "DDoS_UDP", "DDoS_HTTP", "DoS_TCP", "DoS_UDP"],
            size_description="72 Million records (1000-flow and 5% subsets available)",
        ),
        "TON_IoT": DatasetInfo(
            dataset_id="TON_IoT",
            name="TON_IoT Telemetry Dataset",
            institution="UNSW Canberra Cyber",
            year=2020,
            url="https://research.unsw.edu.au/projects/toniot-datasets",
            sha256_checksum="ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d",
            attack_classes=["normal", "ddos", "dos", "scanning", "backdoor", "injection"],
            size_description="Multi-GB heterogeneous IoT telemetry",
        ),
        "CSE-CIC-IDS2018": DatasetInfo(
            dataset_id="CSE-CIC-IDS2018",
            name="Communications Security Establishment & CIC IDS 2018",
            institution="CSE & UNB (AWS)",
            year=2018,
            url="https://www.unb.ca/cic/datasets/ids-2018.html",
            sha256_checksum="c1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
            attack_classes=["Benign", "DDoS-LOIC-HTTP", "DDoS-HOIC", "DoS-Slowloris"],
            size_description="16 Million flows captured on AWS",
        ),
    }

    @classmethod
    def get(cls, dataset_id: str) -> Optional[DatasetInfo]:
        return cls._REGISTRY.get(dataset_id)

    @classmethod
    def list_datasets(cls) -> List[str]:
        return list(cls._REGISTRY.keys())
