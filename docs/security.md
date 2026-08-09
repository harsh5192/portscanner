# Security Considerations & Scope Protection

## Authorized Defensive Testing

This application is strictly designed for authorized security assessments on systems/networks owned or explicitly permitted by the user.

## Built-In Security Controls

1. **Target Input Validation**: All input targets (IPs, IPv4/IPv6 CIDR blocks, Hostnames) are parsed and validated using Python's `ipaddress` and strict RFC regex pattern matching.
2. **Subprocess Argument Sanitization**: Commands and parameters are sanitized to prevent shell injection vulnerabilities. Subprocess executions pass argument lists directly without `shell=True`.
3. **Authorization Check (`--authorized`)**: Scan profiles classified as intrusive (e.g. `FULL`) require explicit authorization parameters (`--authorized`).
4. **Secret Protection**: Logging explicitly strips credentials and sensitive fields.
