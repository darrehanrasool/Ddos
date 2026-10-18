"""Constants and enumerations for DDoS-AI."""

from enum import Enum, IntEnum
from typing import List


class Protocol(IntEnum):
    """Network transport layer protocol numbers."""
    HOPOPT = 0
    ICMP = 1
    IGMP = 2
    TCP = 6
    UDP = 17
    GRE = 47
    ESP = 50
    AH = 51


class AttackType(str, Enum):
    """Standard DDoS attack classifications in CIC-DDoS2019 and modern telemetry."""
    BENIGN = "BENIGN"
    SYN_FLOOD = "Syn"
    UDP_FLOOD = "UDP"
    UDP_LAG = "UDPLag"
    DNS_AMPLIFICATION = "DNS"
    LDAP_AMPLIFICATION = "LDAP"
    MSSQL_AMPLIFICATION = "MSSQL"
    NETBIOS_FLOOD = "NetBIOS"
    NTP_AMPLIFICATION = "NTP"
    SNMP_AMPLIFICATION = "SNMP"
    SSDP_AMPLIFICATION = "SSDP"
    TFTP_AMPLIFICATION = "TFTP"
    PORT_SCAN = "PortScan"
    SLOWLORIS = "Slowloris"
    HTTP_FLOOD = "HTTP_Flood"


class AttackSeverity(str, Enum):
    """Alert severity levels for Security Operations Center (SOC)."""
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


# Default 70 Numerical Features extracted by CICFlowMeter
DEFAULT_FEATURE_COLUMNS: List[str] = [
    "Flow Duration",
    "Total Fwd Packets",
    "Total Backward Packets",
    "Total Length of Fwd Packets",
    "Total Length of Bwd Packets",
    "Fwd Packet Length Max",
    "Fwd Packet Length Min",
    "Fwd Packet Length Mean",
    "Fwd Packet Length Std",
    "Bwd Packet Length Max",
    "Bwd Packet Length Min",
    "Bwd Packet Length Mean",
    "Bwd Packet Length Std",
    "Flow Bytes/s",
    "Flow Packets/s",
    "Flow IAT Mean",
    "Flow IAT Std",
    "Flow IAT Max",
    "Flow IAT Min",
    "Fwd IAT Total",
    "Fwd IAT Mean",
    "Fwd IAT Std",
    "Fwd IAT Max",
    "Fwd IAT Min",
    "Bwd IAT Total",
    "Bwd IAT Mean",
    "Bwd IAT Std",
    "Bwd IAT Max",
    "Bwd IAT Min",
    "Fwd PSH Flags",
    "Bwd PSH Flags",
    "Fwd URG Flags",
    "Bwd URG Flags",
    "Fwd Header Length",
    "Bwd Header Length",
    "Fwd Packets/s",
    "Bwd Packets/s",
    "Min Packet Length",
    "Max Packet Length",
    "Packet Length Mean",
    "Packet Length Std",
    "Packet Length Variance",
    "FIN Flag Count",
    "SYN Flag Count",
    "RST Flag Count",
    "PSH Flag Count",
    "ACK Flag Count",
    "URG Flag Count",
    "CWE Flag Count",
    "ECE Flag Count",
    "Down/Up Ratio",
    "Average Packet Size",
    "Avg Fwd Segment Size",
    "Avg Bwd Segment Size",
    "Subflow Fwd Packets",
    "Subflow Fwd Bytes",
    "Subflow Bwd Packets",
    "Subflow Bwd Bytes",
    "Init_Win_bytes_forward",
    "Init_Win_bytes_backward",
    "act_data_pkt_fwd",
    "min_seg_size_forward",
    "Active Mean",
    "Active Std",
    "Active Max",
    "Active Min",
    "Idle Mean",
    "Idle Std",
    "Idle Max",
    "Idle Min",
]

TARGET_COLUMN = "Label"
RANDOM_SEED_DEFAULT = 42
