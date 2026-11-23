# Ievgen Bondarenko

Independent Security Researcher

I work on product security in AI infrastructure, industrial software, and connected systems. I focus on authorization, isolation, and how untrusted data moves between components.

## How I work

I combine source and firmware review with protocol analysis and testing in isolated environments. Reproducible cases and negative controls help establish what fails and what the impact is. I document root causes and remediation, contribute fixes and regression tests, and coordinate disclosure with vendors and open-source maintainers. I use Python and PowerShell for testing and automation.

## Selected work

- **[WAGO](https://certvde.com/en/advisories/VDE-2026-096/)**: Reported command injection in routing configuration and missing authorization for PROFIBUS settings, leading to firmware remediation.
- **MLflow**: Reported SSRF in [webhook delivery](https://github.com/advisories/GHSA-7gwp-5pfp-969j) and [artifact/model source handling](https://github.com/mlflow/mlflow/security/advisories/GHSA-mr9f-g8qf-4w4j), documenting how attacker-controlled locations crossed the tracking server's network boundary.
- **[gVisor](https://github.com/google/gvisor/pull/12927)**: Fixed a time-of-check/time-of-use bug in shared-memory ThreadID handling. Merged upstream.

Other merged contributions include archive containment checks in [Swift Package Manager](https://github.com/swiftlang/swift-package-manager/pull/10001) and rejection of duplicate JSON keys in [Tink's JWK parsing](https://github.com/tink-crypto/tink-py/pull/76).

## Projects

- **[Tink Cross-Port Fuzz](https://github.com/ibondarenko1/tink-cross-port-fuzz)**: Differential testing of JWK Set handling across Tink language ports.
- **[Security Anomaly ML](https://github.com/ibondarenko1/security-anomaly-ml)**: A network-flow anomaly detection project with a CLI, Docker image, and reproducible tests. Research and evaluation release.

<a name="published-cves"></a>
<a name="published-vendor-advisories"></a>
<a name="cisa-coordination"></a>
<a name="cisa-ics-advisories"></a>

<!-- PROFILE_EVIDENCE:START -->
Public records credit my work in 14 published CVEs. [Research record and sources](RESEARCH.md).
<!-- PROFILE_EVIDENCE:END -->

## Background and contact

Microsoft Certified: Security Operations Analyst Associate (SC-200) · CompTIA Security+

Based in Roseville, California. Open to remote vulnerability research and security engineering roles.

[Website](https://ibondarenko.com) · [Resume](https://ibondarenko.com/resume/) · [LinkedIn](https://www.linkedin.com/in/ievgen-bondarenko-b13098241/) · [Email](mailto:hi@ibondarenko.com)
