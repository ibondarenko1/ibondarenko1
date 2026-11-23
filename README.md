# Ievgen Bondarenko

**Independent Security Researcher**  
AI infrastructure · Industrial and connected systems · Open-source security

I investigate how software enforces authorization, isolation, and trust in external inputs. My work combines vulnerability research with practical engineering: reproducible tests, upstream fixes, and remediation verification with vendors and maintainers.

[Research](https://ibondarenko.com/research/) · [Open-source contributions](https://ibondarenko.com/open-source/) · [Resume](https://ibondarenko.com/resume/)

## How I work

I review source code, firmware, and protocols, then test suspected failures in isolated environments. Negative controls help separate demonstrated impact from assumptions. I document root causes and remediation, contribute patches and regression tests, and coordinate disclosure.

**Tools:** Python, Go, PowerShell, Linux, Docker, GitHub Actions, Semgrep, CodeQL, and Joern.

## Security engineering contributions

Selected fixes merged into upstream projects:

- **[Google gVisor](https://github.com/google/gvisor/pull/12927)**: Fixed a time-of-check/time-of-use bug in shared-memory ThreadID handling.
- **[Swift Package Manager](https://github.com/swiftlang/swift-package-manager/pull/10001)**: Rejected extracted archives containing symlinks that escape the destination directory.
- **[vLLM](https://github.com/vllm-project/vllm/pull/43117)**: Routed multimodal media fetching through the existing security controls.
- **[Tink](https://github.com/tink-crypto/tink-py/pull/76)**: Rejected JWK Sets containing duplicate JSON keys.
- **[Google Bumble](https://github.com/google/bumble/pull/912)**: Validated malformed protocol input to prevent crashes.
- **[InterUSS DSS](https://github.com/interuss/dss/pull/1788)**: Enforced request-level authorization scopes for subscription notifications.

[More merged contributions](https://github.com/search?q=type%3Apr+author%3Aibondarenko1+is%3Amerged+-user%3Aibondarenko1&type=pullrequests)

## Vulnerability research

### Industrial software and devices

| Product | Research and outcome |
| --- | --- |
| [WAGO controllers](https://certvde.com/en/advisories/VDE-2026-096/) | Routing command injection with root-level impact and missing authorization for PROFIBUS configuration. Vendor fixes and CERT@VDE researcher credit. |
| [Phoenix Contact PLCnext Engineer](https://www.certvde.com/en/advisories/VDE-2026-121/) | GSDX signature verification, plugin signature bypass, and extraction path traversal. Fixed in 2026.6. |
| [Moxa AIG-302](https://www.cisa.gov/news-events/ics-advisories/icsa-26-293-03) | Missing authorization and shared root CA private-key material. Vendor remediation and CISA researcher credit. |
| [Lantronix G520](https://www.cisa.gov/news-events/ics-advisories/icsa-26-272-01) | Update-metadata XSS and update-package signature verification flaws. Vendor remediation and CISA researcher credit. |
| [OPC UA .NET Standard Stack](https://github.com/OPCFoundation/OPC-SecurityAdvisories/blob/latest/csaf/2026/011/README.md) | Cross-session file access through sessionless calls in the optional Machinery ResultTransfer component. Fixed in 2.0.2. |

### AI infrastructure and distributed systems

| Product | Research and outcome |
| --- | --- |
| MLflow | SSRF in [webhook delivery](https://github.com/advisories/GHSA-7gwp-5pfp-969j) and [artifact locations / model version sources](https://github.com/mlflow/mlflow/security/advisories/GHSA-mr9f-g8qf-4w4j). Public finder and reporter credits. |
| [LiteLLM](https://github.com/BerriAI/litellm/security/advisories/GHSA-28j3-9x3h-556f) | Unauthenticated exposure of MCP server metadata and internal target URLs. Fixed in 1.89.0. |
| [Eclipse Ankaios](https://www.cve.org/CVERecord?id=CVE-2026-84173) | Scoped workloads could access or modify cluster state outside their permitted subtree. Validated the maintainer fix. |
| [vLLM](https://github.com/advisories/GHSA-4hhp-h66f-j5j7) | Multimodal media retrieval bypass allowing SSRF and local-file access. Contributed the upstream retrieval fix. |
| [LMDeploy](https://github.com/advisories/GHSA-9xq9-36w5-q796) | Unsafe remote-code trust during model initialization. Public researcher credit. |

<a name="published-cves"></a>
<a name="published-vendor-advisories"></a>

<!-- PROFILE_EVIDENCE:START -->
Public records credit my work in 14 published CVEs. [Research record and sources](RESEARCH.md).
<!-- PROFILE_EVIDENCE:END -->

<a name="cisa-coordination"></a>
<a name="cisa-ics-advisories"></a>

## CISA coordination

As of 2026-11-23, I am coordinating **7 active cases through CISA VINCE-NT**. Researcher credit also appears in **2 published CISA ICS advisories**, for [Moxa AIG-302](https://www.cisa.gov/news-events/ics-advisories/icsa-26-293-03) and [Lantronix G520](https://www.cisa.gov/news-events/ics-advisories/icsa-26-272-01).

[Coordination record and advisory dates](RESEARCH.md#cisa-coordination)

## Research tools and engineering projects

- **[Tink Cross-Port Fuzz](https://github.com/ibondarenko1/tink-cross-port-fuzz)**: Differential testing of JWK Set handling across Tink language ports.
- **[Security Anomaly ML](https://github.com/ibondarenko1/security-anomaly-ml)**: Network-flow anomaly detection with a versioned incident format, CLI, Docker image, and reproducible tests. Research and evaluation release.
- **[Microsoft Sentinel Detection Engineering](https://github.com/ibondarenko1/azure-sentinel-detection-engineering)**: MITRE ATT&CK-mapped KQL detections with controlled validation and PR-gated deployment.
- **[LLM Serving Security](https://github.com/ibondarenko1/llm-serving-security)**: Reference material for vulnerability classes and hardening across model-serving stacks.

## Background and contact

My background includes Windows and Linux security, cloud and identity assessments, and remediation planning against ISO 27001, NIST, and SOC 2 controls.

**Certifications:** Microsoft Certified: Security Operations Analyst Associate (SC-200) · CompTIA Security+

Roseville, California · Open to remote vulnerability research and security engineering roles.

[Website](https://ibondarenko.com) · [LinkedIn](https://www.linkedin.com/in/ievgen-bondarenko-b13098241/) · [Email](mailto:hi@ibondarenko.com)
