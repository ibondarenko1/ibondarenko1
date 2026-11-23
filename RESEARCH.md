# Research record

Public advisories, researcher credits, and merged contributions. Roles follow the linked source.

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
## CISA ICS advisories

Researcher credit in 2 published CISA ICS advisories.

| Product | Advisory | Published |
| --- | --- | --- |
| Lantronix G520 Series Cellular Gateway | [ICSA-26-272-01](https://www.cisa.gov/news-events/ics-advisories/icsa-26-272-01) | 2026-09-29 |
| Moxa AIG-302 ThingsPro Edge | [ICSA-26-293-03](https://www.cisa.gov/news-events/ics-advisories/icsa-26-293-03) | 2026-10-20 |
<!-- CISA_LIST:END -->

<!-- PR_LIST:START -->
## Merged pull requests

25 merged pull requests authored by ibondarenko1 outside personal repositories. Includes code, tests, documentation, detection queries, resource entries, and workflow experiments. Company workflow experiments are labelled below.

[Source query](https://github.com/search?q=is%3Apr+author%3Aibondarenko1+is%3Amerged+-user%3Aibondarenko1&type=pullrequests). Verified 2026-11-23.

| Pull request | Contribution | Merged |
| --- | --- | --- |
| [interuss/dss#1788](https://github.com/interuss/dss/pull/1788) | Enforce request-level scopes for SCD subscription notifications | 2026-10-20 |
| [gvisor/gvisor#13161](https://github.com/gvisor/gvisor/pull/13161) | nftables: validate csumOffset bounds in payloadSet evaluate | 2026-09-26 |
| [gvisor/gvisor#13215](https://github.com/gvisor/gvisor/pull/13215) | cgroupfs: drop registry entries on filesystem release | 2026-09-25 |
| [ElNiak/awesome-ai-cybersecurity#18](https://github.com/ElNiak/awesome-ai-cybersecurity/pull/18) | Add Security Anomaly ML | 2026-08-21 |
| [firecrawl/firecrawl#4274](https://github.com/firecrawl/firecrawl/pull/4274) | fix(self-host): make FoundationDB init idempotent | 2026-08-08 |
| [summitrange-security-lab/actions-workflow-fork-boundary-lab#1](https://github.com/summitrange-security-lab/actions-workflow-fork-boundary-lab/pull/1) | Add harmless fork workflow boundary canary (company workflow experiment) | 2026-07-23 |
| [summitrange-security-lab/actions-workflow-fork-boundary-lab#2](https://github.com/summitrange-security-lab/actions-workflow-fork-boundary-lab/pull/2) | Same-repository workflow boundary control (company workflow experiment) | 2026-07-23 |
| [vllm-project/vllm#43117](https://github.com/vllm-project/vllm/pull/43117) | fix(processor): route MiMo-V2-Omni media fetch through MediaConnector | 2026-07-11 |
| [gvisor/gvisor#13214](https://github.com/gvisor/gvisor/pull/13214) | tcpip/ipv6: use isEnabled() in disableLocked() to match ipv4 sibling | 2026-06-30 |
| [gvisor/gvisor#13243](https://github.com/gvisor/gvisor/pull/13243) | lisafs: bound Walk and WalkStat response payloads to maxMessageSize | 2026-06-23 |
| [gvisor/gvisor#13164](https://github.com/gvisor/gvisor/pull/13164) | tcp: mark ISN and timestamp-offset secrets nosave for checkpoint | 2026-06-05 |
| [microsoft/TypeScript#63516](https://github.com/microsoft/TypeScript/pull/63516) | Update toFixed/toExponential/toPrecision digit range in docs to match the spec | 2026-06-04 |
| [Azure/Azure-Sentinel#14340](https://github.com/Azure/Azure-Sentinel/pull/14340) | Add Raw IP Address Used as URL Domain hunting query | 2026-05-26 |
| [gvisor/gvisor#13165](https://github.com/gvisor/gvisor/pull/13165) | tcp: strict RFC 5961 RST sequence validation (contributes to #1132) | 2026-05-20 |
| [gvisor/gvisor#13181](https://github.com/gvisor/gvisor/pull/13181) | stack: document conntrack seed regen requirement on iptables S/R | 2026-05-19 |
| [gvisor/gvisor#13153](https://github.com/gvisor/gvisor/pull/13153) | lisafs: reject FRemoveXattr on deleted files | 2026-05-13 |
| [swiftlang/swift-package-manager#10001](https://github.com/swiftlang/swift-package-manager/pull/10001) | registry: reject extracted archives with escaping symlinks | 2026-05-11 |
| [tink-crypto/tink-py#76](https://github.com/tink-crypto/tink-py/pull/76) | fix(jwt): reject JWK Sets with duplicate JSON keys | 2026-05-11 |
| [gvisor/gvisor#13015](https://github.com/gvisor/gvisor/pull/13015) | systrap: hold sysmsgThreadsMu around map read in switchToApp | 2026-05-05 |
| [google/osv-scanner#2748](https://github.com/google/osv-scanner/pull/2748) | fix: correct misleading docstrings in scalibrextract extractors | 2026-04-28 |
| [google/bumble#918](https://github.com/google/bumble/pull/918) | avdtp: bound message assembler to drop truncated PDUs (DoS prevention) | 2026-04-27 |
| [google/bumble#914](https://github.com/google/bumble/pull/914) | sdp: bound DataElement parse recursion to prevent RecursionError DoS | 2026-04-26 |
| [google/bumble#912](https://github.com/google/bumble/pull/912) | fix: add input validation to prevent remote crash from empty/malforme… | 2026-04-20 |
| [gvisor/gvisor#12925](https://github.com/gvisor/gvisor/pull/12925) | tun: add empty data check before AsSlice()\[0\] in TUN Write() | 2026-04-15 |
| [gvisor/gvisor#12927](https://github.com/gvisor/gvisor/pull/12927) | systrap: fix TOCTOU on ThreadID in NotifyInterrupt | 2026-04-13 |
<!-- PR_LIST:END -->
