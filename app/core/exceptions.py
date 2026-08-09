class ScannerBaseException(Exception):
    """Base exception for NetSec Scanner platform."""
    def __init__(self, message: str = "An error occurred within the scanner system."):
        self.message = message
        super().__init__(self.message)

class ScannerError(ScannerBaseException):
    """Raised when scanner operations fail."""
    pass

class NmapNotInstalledError(ScannerError):
    """Raised when Nmap executable is missing or not found in PATH."""
    def __init__(self, message: str = "Nmap executable was not found on system. Please install Nmap."):
        super().__init__(message)

class InvalidTargetError(ScannerError):
    """Raised when a target IP/CIDR/Hostname format is invalid or unreachable."""
    def __init__(self, target: str, message: str = "Invalid target format specified."):
        self.target = target
        super().__init__(f"{message} Target: {target}")

class ScanTimeoutError(ScannerError):
    """Raised when a scan operation times out."""
    def __init__(self, timeout: int, message: str = "Scan operation exceeded timeout limits."):
        self.timeout = timeout
        super().__init__(f"{message} (Timeout: {timeout}s)")

class PluginError(ScannerBaseException):
    """Raised when plugin registration or execution fails."""
    pass

class ReportGenerationError(ScannerBaseException):
    """Raised when report generation fails."""
    pass

class AuthorizationError(ScannerBaseException):
    """Raised when an intrusive scan mode is requested without user explicit authorization."""
    def __init__(self, message: str = "Intrusive scan requires explicit authorization flag (--authorized)."):
        super().__init__(message)
