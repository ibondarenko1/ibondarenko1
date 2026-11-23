# Research record

Public advisories, researcher credits, and selected upstream contributions. Roles follow the linked source.

[Back to profile](README.md)

<!-- CVE_LIST:START -->
## Published CVEs

Published CVEs with public researcher credit. Listed roles follow the source advisory.

- [CVE-2026-109812](https://www.moxa.com/en/support/product-support/security-advisory/mpsa-262560-cve-2026-109812,-cve-2026-109813-vulnerabilities-in-industrial-computing-products) · **Moxa AIG-302**: Missing authorization on the secrets API.
- [CVE-2026-109813](https://www.moxa.com/en/support/product-support/security-advisory/mpsa-262560-cve-2026-109812,-cve-2026-109813-vulnerabilities-in-industrial-computing-products) · **Moxa AIG-302**: Shared hard-coded root CA private key.
- [CVE-2026-110021](https://www.certvde.com/en/advisories/VDE-2026-121/) · **Phoenix Contact PLCnext Engineer**: Missing cryptographic verification of XML SignatureValue in signed GSDX device-description packages.
- [CVE-2026-110022](https://www.certvde.com/en/advisories/VDE-2026-121/) · **Phoenix Contact PLCnext Engineer**: Plugin signature-validation bypass allowing an unsigned replacement DLL to be loaded.
- [CVE-2026-110935](https://www.certvde.com/en/advisories/VDE-2026-121/) · **Phoenix Contact PLCnext Engineer**: Path traversal during plugin extraction allowing writes outside the plugin repository.
- [CVE-2026-118628](https://github.com/mlflow/mlflow/security/advisories/GHSA-mr9f-g8qf-4w4j) · **MLflow**: SSRF through client-supplied artifact locations and model version sources. Credit: reporter.
- [CVE-2026-46517](https://github.com/advisories/GHSA-9xq9-36w5-q796) · **LMDeploy**: Unsafe remote-code trust during model initialization.
- [CVE-2026-64849](https://github.com/advisories/GHSA-7gwp-5pfp-969j) · **MLflow**: Unauthenticated webhook SSRF via redirects and DNS rebinding.
- [CVE-2026-73560](https://github.com/advisories/GHSA-4hhp-h66f-j5j7) · **vLLM**: Multimodal media retrieval bypass enabling SSRF and local-file access.
- [CVE-2026-80466](https://certvde.com/en/advisories/VDE-2026-096/) · **WAGO Controllers and Touch Panels**: Stored command injection in WBM routing configuration, executed by a privileged helper.
- [CVE-2026-84173](https://www.cve.org/CVERecord?id=CVE-2026-84173) · **Eclipse Ankaios**: Authorization bypass in Control Interface workload rules.
- [CVE-2026-84409](https://www.cisa.gov/news-events/ics-advisories/icsa-26-272-01) · **Lantronix G520**: Cross-site scripting through update metadata.
- [CVE-2026-88850](https://certvde.com/en/advisories/VDE-2026-096/) · **WAGO Controllers and Touch Panels**: Missing authorization allows authenticated users to modify root-owned PROFIBUS configuration.
- [CVE-2026-91191](https://www.cisa.gov/news-events/ics-advisories/icsa-26-272-01) · **Lantronix G520**: Improper cryptographic signature verification of update packages.
<!-- CVE_LIST:END -->

<!-- ADVISORY_LIST:START -->
## Published vendor advisories

Public advisories acknowledging my research.

- [GCVE-105-2026-011](https://github.com/OPCFoundation/OPC-SecurityAdvisories/blob/latest/csaf/2026/011/README.md) · **OPC UA .NET Standard Stack**: A sessionless Call can read a Machinery result file handle that belongs to another session. Published 2026-11-13.
- [GHSA-28j3-9x3h-556f](https://github.com/BerriAI/litellm/security/advisories/GHSA-28j3-9x3h-556f) · **LiteLLM**: Unauthenticated public MCP hub exposed registered server metadata and internal target URLs. Fixed in 1.89.0. Published 2026-11-23.
<!-- ADVISORY_LIST:END -->

<!-- CISA_LIST:START -->
## CISA coordination

7 active vulnerability coordination cases through CISA VINCE-NT. Last verified 2026-11-23.

### CISA ICS advisories

Researcher credit in 2 published CISA ICS advisories.

| Product | Advisory | Published |
| --- | --- | --- |
| Lantronix G520 Series Cellular Gateway | [ICSA-26-272-01](https://www.cisa.gov/news-events/ics-advisories/icsa-26-272-01) | 2026-09-29 |
| Moxa AIG-302 ThingsPro Edge | [ICSA-26-293-03](https://www.cisa.gov/news-events/ics-advisories/icsa-26-293-03) | 2026-10-20 |
<!-- CISA_LIST:END -->

## Selected upstream contributions

- [gVisor](https://github.com/google/gvisor/pull/12927): Fixed a time-of-check/time-of-use bug in shared-memory ThreadID handling.
- [Swift Package Manager](https://github.com/swiftlang/swift-package-manager/pull/10001): Added validation to reject extracted archives with symlinks that escape the destination directory.
- [vLLM](https://github.com/vllm-project/vllm/pull/43117): Routed multimodal media fetching through existing security controls.
- [Tink](https://github.com/tink-crypto/tink-py/pull/76): Rejected JWK Sets with duplicate JSON keys.
- [Google Bumble](https://github.com/google/bumble/pull/912): Validated malformed protocol input to prevent crashes.
- [InterUSS DSS](https://github.com/interuss/dss/pull/1788): Enforced request-level authorization scopes for subscription notifications.

[More merged upstream pull requests](https://github.com/search?q=type%3Apr+author%3Aibondarenko1+is%3Amerged+-user%3Aibondarenko1&type=pullrequests)
