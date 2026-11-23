# Ievgen Bondarenko

**Independent Security Researcher**  
AI infrastructure · Industrial systems · Open-source security

I investigate authorization, isolation, and input-handling flaws in software. My work combines source and protocol analysis with reproducible tests, upstream patches, and verification of vendor fixes.

<!-- PROFILE_EVIDENCE:START -->
**[14 published CVEs](RESEARCH.md#published-cves)** · **[25 merged pull requests](RESEARCH.md#merged-pull-requests)** · **[2 published CISA ICS advisories](RESEARCH.md#cisa-ics-advisories)**
<!-- PROFILE_EVIDENCE:END -->

[Website](https://ibondarenko.com) · [Resume](https://ibondarenko.com/resume/) · [LinkedIn](https://www.linkedin.com/in/ievgen-bondarenko-b13098241/) · [Contact](mailto:hi@ibondarenko.com)

## Published research

### Industrial software and devices

| Product | Work and outcome |
| --- | --- |
| [WAGO controllers](https://certvde.com/en/advisories/VDE-2026-096/) | Root-level command injection in routing configuration and missing authorization for PROFIBUS settings. Vendor fixes published. |
| [Phoenix Contact PLCnext Engineer](https://www.certvde.com/en/advisories/VDE-2026-121/) | GSDX signature-verification failure, plugin signature bypass, and extraction path traversal. Fixed in 2026.6. |
| [Moxa AIG-302](https://www.cisa.gov/news-events/ics-advisories/icsa-26-293-03) | Missing authorization on the secrets API and shared root CA private-key material. Remediation documented in a CISA ICS advisory. |
| [Lantronix G520](https://www.cisa.gov/news-events/ics-advisories/icsa-26-272-01) | Update-metadata XSS and update-package signature-verification flaws. Vendor remediation documented by CISA. |
| [OPC UA .NET Standard Stack](https://github.com/OPCFoundation/OPC-SecurityAdvisories/blob/latest/csaf/2026/011/README.md) | Cross-session file access in the optional Machinery ResultTransfer component. Fixed in 2.0.2. |

### AI infrastructure and distributed systems

| Product | Work and outcome |
| --- | --- |
| MLflow | SSRF through [webhook delivery](https://github.com/advisories/GHSA-7gwp-5pfp-969j) and [artifact locations / model version sources](https://github.com/mlflow/mlflow/security/advisories/GHSA-mr9f-g8qf-4w4j). Both findings publicly disclosed. |
| [LiteLLM](https://github.com/BerriAI/litellm/security/advisories/GHSA-28j3-9x3h-556f) | Unauthenticated exposure of MCP server metadata and internal target URLs. Fixed in 1.89.0. |
| [Eclipse Ankaios](https://www.cve.org/CVERecord?id=CVE-2026-84173) | Workloads could access or modify cluster state outside their authorized subtree. Validated the maintainer's fix. |
| [vLLM](https://github.com/advisories/GHSA-4hhp-h66f-j5j7) | Multimodal media retrieval bypass allowed SSRF and local-file access. Contributed the [MediaConnector fix](https://github.com/vllm-project/vllm/pull/43117). |
| [LMDeploy](https://github.com/advisories/GHSA-9xq9-36w5-q796) | Unsafe remote-code trust during model initialization. Published advisory credits the research. |

## Open-source engineering

- **gVisor:** Fixed a [shared-memory ThreadID race](https://github.com/gvisor/gvisor/pull/12927), tightened [TCP reset validation](https://github.com/gvisor/gvisor/pull/13165), and bounded [filesystem protocol responses](https://github.com/gvisor/gvisor/pull/13243).
- **Swift Package Manager:** [Rejected extracted archives](https://github.com/swiftlang/swift-package-manager/pull/10001) with symlinks that escape the destination directory.
- **Tink:** [Rejected duplicate JSON keys in JWK Sets](https://github.com/tink-crypto/tink-py/pull/76). Built [Tink Cross-Port Fuzz](https://github.com/ibondarenko1/tink-cross-port-fuzz) to compare behavior across language implementations.
- **Google Bumble:** Added [protocol-input validation](https://github.com/google/bumble/pull/912), [SDP recursion bounds](https://github.com/google/bumble/pull/914), and [truncated-PDU handling](https://github.com/google/bumble/pull/918) to prevent crashes.
- **InterUSS DSS:** [Enforced request-level authorization scopes](https://github.com/interuss/dss/pull/1788) for subscription notifications.
- **Microsoft Sentinel:** Contributed a [KQL hunting query](https://github.com/Azure/Azure-Sentinel/pull/14340) for raw IP addresses used as URL domains.
- **Firecrawl:** Made [FoundationDB initialization idempotent](https://github.com/firecrawl/firecrawl/pull/4274) for self-hosted deployments.

## Projects

- **[Security Anomaly ML](https://github.com/ibondarenko1/security-anomaly-ml):** Network-flow anomaly detection with a versioned incident format, CLI, Docker image, and reproducible tests. Research and evaluation release.
- **[Microsoft Sentinel Detection Engineering](https://github.com/ibondarenko1/azure-sentinel-detection-engineering):** MITRE ATT&CK-mapped KQL detections with controlled validation and PR-gated deployment.
- **[LLM Serving Security](https://github.com/ibondarenko1/llm-serving-security):** Reference material for vulnerability classes and hardening across model-serving stacks.

## Background

Windows and Linux security, cloud and identity assessments, and remediation planning against ISO 27001, NIST, and SOC 2 controls.

**Tools:** Python, Go, PowerShell, Linux, Docker, GitHub Actions, Semgrep, CodeQL, Joern.  
**Certifications:** Microsoft Certified: Security Operations Analyst Associate (SC-200) · CompTIA Security+

Roseville, California · Open to remote vulnerability research and security engineering roles.
