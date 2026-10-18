"""Custom typed exception hierarchy for DDoS-AI."""


class DDoSException(Exception):
    """Base exception for all DDoS-AI platform errors."""
    pass


class ConfigurationError(DDoSException):
    """Raised when configuration YAML or parameters are invalid."""
    pass


class DataValidationError(DDoSException):
    """Raised when network packet/flow data fails validation checks."""
    pass


class DatasetDownloadError(DDoSException):
    """Raised when remote dataset downloading or checksum verification fails."""
    pass


class PreprocessingError(DDoSException):
    """Raised when data transformation, imputation, or scaling fails."""
    pass


class ModelTrainingError(DDoSException):
    """Raised when model initialization or training loop fails."""
    pass


class CheckpointError(DDoSException):
    """Raised when saving or loading model weights fails."""
    pass


class HardwareResourceError(DDoSException):
    """Raised when GPU/MPS or RAM resources are exhausted."""
    pass


class AnomalyDetectionError(DDoSException):
    """Raised during unsupervised autoencoder reconstruction error calculation."""
    pass
