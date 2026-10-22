# Ievgen Bondarenko

**Independent Security Researcher**  
AI Infrastructure · Robotics & Distributed Systems · IoT & Industrial Systems · Open Source Security

I investigate security boundaries in AI services, industrial and connected systems, firmware, and security-sensitive open source. I use source review, reverse engineering, and controlled reproduction to establish root cause, practical impact, and remediation. Public results include vendor and CISA advisories, Google Cloud VRP recognition, and merged upstream security fixes.

[Research](https://ibondarenko.com/research/) · [Open-source contributions](https://ibondarenko.com/open-source/) · [Resume](https://ibondarenko.com/resume/)

<!-- BADGES:START -->
<p>
  <a href="https://github.com/ibondarenko1/ibondarenko1#published-cves"><img alt="8 CVEs published" src="https://img.shields.io/badge/CVEs%20Published-8-c0392b?style=flat-square&logo=cve&logoColor=white&labelColor=222"></a>
  <a href="https://www.cisa.gov/news-events/ics-advisories/icsa-26-272-01"><img alt="CISA ICS Advisory ICSA-26-272-01" src="https://img.shields.io/badge/CISA%20ICS-ICSA--26--272--01-005ea2?style=flat-square&labelColor=222"></a>
  <a href="https://github.com/search?q=type%3Apr+author%3Aibondarenko1+is%3Amerged+-user%3Aibondarenko1&type=pullrequests"><img alt="25 merged PRs" src="https://img.shields.io/badge/Merged%20PRs-25-2da44e?style=flat-square&logo=github&logoColor=white&labelColor=222"></a>
</p>
<!-- BADGES:END -->

## Selected published research

### Industrial & IoT security

- **[Moxa AIG-302 · MPSA-262560](https://www.moxa.com/en/support/product-support/security-advisory/mpsa-262560-cve-2026-109812,-cve-2026-109813-vulnerabilities-in-industrial-computing-products)**: [CVE-2026-109812](https://www.cve.org/CVERecord?id=CVE-2026-109812) and [CVE-2026-109813](https://www.cve.org/CVERecord?id=CVE-2026-109813). Missing authorization in a secrets API and a shared hard-coded root CA private key. Moxa credits my report and provides a fix in firmware 1.4.1.
- **[Lantronix G520 · CISA ICSA-26-272-01](https://www.cisa.gov/news-events/ics-advisories/icsa-26-272-01)**: [CVE-2026-84409](https://www.cve.org/CVERecord?id=CVE-2026-84409) and [CVE-2026-91191](https://www.cve.org/CVERecord?id=CVE-2026-91191). Update-metadata XSS and improper package-signature verification. CISA credits the research and documents vendor remediation.

### AI infrastructure & distributed systems

- **[MLflow · CVE-2026-64849](https://github.com/advisories/GHSA-7gwp-5pfp-969j)**: Unauthenticated full-read SSRF in webhook delivery through redirects and DNS-rebinding weaknesses.
- **[Eclipse Ankaios · CVE-2026-84173](https://www.cve.org/CVERecord?id=CVE-2026-84173)**: Control Interface authorization bypass permitting access outside an authorized cluster-state subtree.
- **[vLLM · CVE-2026-73560](https://github.com/advisories/GHSA-4hhp-h66f-j5j7)**: Multimodal media retrieval bypass enabling SSRF and local-file access outside hardened retrieval controls.
- **[LMDeploy · CVE-2026-46517](https://github.com/advisories/GHSA-9xq9-36w5-q796)**: Unsafe remote-code trust during model initialization.
- **[Google Cloud VRP recognition](https://ibondarenko.com/research/)**: Research on a caller-influenced provider endpoint in Google Genkit, exposing SSRF, API-key disclosure, and response-forgery paths.

## Selected upstream security fixes

- **[gVisor · systrap ThreadID TOCTOU](https://github.com/google/gvisor/pull/12927)**: Eliminated a guest-writable shared-memory time-of-check/time-of-use window.
- **[vLLM · multimodal media retrieval](https://github.com/vllm-project/vllm/pull/43117)**: Routed image and audio fetching through MediaConnector security controls.
- **[Swift Package Manager · archive extraction](https://github.com/swiftlang/swift-package-manager/pull/10001)**: Rejected extracted archives containing escaping symlinks.
- **[Tink · JWK Set validation](https://github.com/tink-crypto/tink-py/pull/76)**: Rejected ambiguous JWK Sets containing duplicate JSON keys.
- **[Google Bumble · protocol input validation](https://github.com/google/bumble/pull/912)**: Hardened malformed-input handling to prevent remote crashes.

[More merged upstream pull requests](https://github.com/pulls?q=is%3Apr+author%3Aibondarenko1+is%3Amerged+-user%3Aibondarenko1)

## Security engineering projects

- **[Security Anomaly ML](https://github.com/ibondarenko1/security-anomaly-ml)**: Network-flow anomaly detection with deterministic analyst-facing incidents, causal feature processing, a versioned output format, and reproducible tests. Research/evaluation release, not presented as production-ready.
- **[Microsoft Sentinel Detection Engineering](https://github.com/ibondarenko1/azure-sentinel-detection-engineering)**: MITRE ATT&CK-mapped KQL detections, controlled validation, incident evidence, and PR-gated Detection-as-Code deployment.
- **[LLM Serving Security](https://github.com/ibondarenko1/llm-serving-security)**: Research reference for vulnerability classes and hardening across popular model-serving stacks.

<!-- CVE_LIST:START -->
## Published CVEs

Verified public advisory links for each published CVE.

- [CVE-2026-109812](https://www.moxa.com/en/support/product-support/security-advisory/mpsa-262560-cve-2026-109812,-cve-2026-109813-vulnerabilities-in-industrial-computing-products) · **Moxa AIG-302**: Missing authorization on the secrets API.
- [CVE-2026-109813](https://www.moxa.com/en/support/product-support/security-advisory/mpsa-262560-cve-2026-109812,-cve-2026-109813-vulnerabilities-in-industrial-computing-products) · **Moxa AIG-302**: Shared hard-coded root CA private key.
- [CVE-2026-46517](https://github.com/advisories/GHSA-9xq9-36w5-q796) · **LMDeploy**: Unsafe remote-code trust during model initialization.
- [CVE-2026-64849](https://github.com/advisories/GHSA-7gwp-5pfp-969j) · **MLflow**: Unauthenticated webhook SSRF via redirects and DNS rebinding.
- [CVE-2026-73560](https://github.com/advisories/GHSA-4hhp-h66f-j5j7) · **vLLM**: Multimodal media retrieval bypass enabling SSRF and local-file access.
- [CVE-2026-84173](https://www.cve.org/CVERecord?id=CVE-2026-84173) · **Eclipse Ankaios**: Authorization bypass in Control Interface workload rules.
- [CVE-2026-84409](https://www.cisa.gov/news-events/ics-advisories/icsa-26-272-01) · **Lantronix G520**: Cross-site scripting through update metadata.
- [CVE-2026-91191](https://www.cisa.gov/news-events/ics-advisories/icsa-26-272-01) · **Lantronix G520**: Improper cryptographic signature verification of update packages.
<!-- CVE_LIST:END -->

## Methods & background

Source and firmware analysis, reverse engineering, protocol review, trust-boundary mapping, negative controls, and reproducible vulnerability validation. Operational experience includes Microsoft Sentinel and Defender XDR, KQL, Sigma, Security Onion, Suricata, Zeek, Python, and PowerShell.

**Certifications:** Microsoft Certified: Security Operations Analyst Associate (SC-200) · CompTIA Security+

## Connect

Sacramento, California · Open to remote vulnerability research and security engineering roles.

[Website](https://ibondarenko.com) · [LinkedIn](https://www.linkedin.com/in/ievgen-bondarenko-b13098241/) · [Email](mailto:hi@ibondarenko.com)
