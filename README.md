# Ievgen Bondarenko

**Independent Security Researcher**  
AI infrastructure · Industrial and IoT systems · Open source security

I research security boundaries in AI infrastructure, industrial devices, and open-source systems. I document vulnerabilities, work with maintainers on fixes, and publish results through vendor advisories and upstream patches.

[Research](https://ibondarenko.com/research/) · [Open-source contributions](https://ibondarenko.com/open-source/) · [Resume](https://ibondarenko.com/resume/)

<!-- BADGES:START -->
<p>
  <a href="https://github.com/ibondarenko1/ibondarenko1#published-cves"><img alt="8 CVEs published" src="https://img.shields.io/badge/CVEs%20Published-8-c0392b?style=flat-square&logo=cve&logoColor=white&labelColor=222"></a>
  <a href="https://github.com/ibondarenko1/ibondarenko1#cisa-ics-advisories"><img alt="2 CISA ICS advisories with researcher credit" src="https://img.shields.io/badge/CISA%20ICS%20Advisories-2-005ea2?style=flat-square&labelColor=222"></a>
  <a href="https://github.com/search?q=type%3Apr+author%3Aibondarenko1+is%3Amerged+-user%3Aibondarenko1&type=pullrequests"><img alt="25 merged PRs" src="https://img.shields.io/badge/Merged%20PRs-25-2da44e?style=flat-square&logo=github&logoColor=white&labelColor=222"></a>
</p>
<!-- BADGES:END -->

## Selected research and contributions

- **[gVisor](https://github.com/google/gvisor/pull/12927)** - Fixed a time-of-check/time-of-use bug in shared-memory ThreadID handling. Merged upstream.
- **[Swift Package Manager](https://github.com/swiftlang/swift-package-manager/pull/10001)** - Added validation to reject extracted archives with symlinks that escape the destination directory. Merged upstream.
- **[Moxa AIG-302](https://www.cisa.gov/news-events/ics-advisories/icsa-26-293-03)** - Reported missing authorization and a shared root CA private key. Two published CVEs, researcher credit in CISA ICSA-26-293-03, and a firmware fix.
- **[Lantronix G520](https://www.cisa.gov/news-events/ics-advisories/icsa-26-272-01)** - Reported update and package-authenticity flaws. Two published CVEs, researcher credit in CISA ICSA-26-272-01, and vendor remediation.

<!-- CISA_LIST:START -->
## CISA ICS advisories

Researcher credit in the following CISA advisories.

| Product | Advisory | Published |
| --- | --- | --- |
| Lantronix G520 Series Cellular Gateway | [ICSA-26-272-01](https://www.cisa.gov/news-events/ics-advisories/icsa-26-272-01) | 2026-09-29 |
| Moxa AIG-302 ThingsPro Edge | [ICSA-26-293-03](https://www.cisa.gov/news-events/ics-advisories/icsa-26-293-03) | 2026-10-20 |
<!-- CISA_LIST:END -->

## AI and distributed systems research

- **[MLflow](https://github.com/advisories/GHSA-7gwp-5pfp-969j)** - Unauthenticated full-read SSRF in webhook delivery.
- **[Eclipse Ankaios](https://www.cve.org/CVERecord?id=CVE-2026-84173)** - Authorization bypass outside an allowed cluster-state subtree.
- **[vLLM](https://github.com/advisories/GHSA-4hhp-h66f-j5j7)** - Multimodal media retrieval controls bypassed, allowing SSRF and local-file access.
- **[LMDeploy](https://github.com/advisories/GHSA-9xq9-36w5-q796)** - Unsafe remote-code trust during model initialization.

## Other upstream security fixes

- [vLLM](https://github.com/vllm-project/vllm/pull/43117) - Routed multimodal media fetching through existing security controls.
- [Tink](https://github.com/tink-crypto/tink-py/pull/76) - Rejected JWK Sets with duplicate JSON keys.
- [Google Bumble](https://github.com/google/bumble/pull/912) - Validated malformed protocol input to prevent crashes.
- [InterUSS DSS](https://github.com/interuss/dss/pull/1788) - Enforced request-level authorization scopes for subscription notifications.

[More merged upstream pull requests](https://github.com/pulls?q=is%3Apr+author%3Aibondarenko1+is%3Amerged+-user%3Aibondarenko1)

## Research tools and engineering projects

- **[Tink Cross-Port Fuzz](https://github.com/ibondarenko1/tink-cross-port-fuzz)** - Differential testing of JWK Set handling across Tink language ports.
- **[Security Anomaly ML](https://github.com/ibondarenko1/security-anomaly-ml)** - Network-flow anomaly detection with a versioned incident format, CLI, Docker image, and reproducible tests. Research and evaluation release.
- **[Microsoft Sentinel Detection Engineering](https://github.com/ibondarenko1/azure-sentinel-detection-engineering)** - MITRE ATT&CK-mapped KQL detections with controlled validation and PR-gated deployment.
- **[LLM Serving Security](https://github.com/ibondarenko1/llm-serving-security)** - Reference material for vulnerability classes and hardening across model-serving stacks.

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

## Methods and background

Source and firmware analysis, reverse engineering, protocol review, trust-boundary mapping, negative controls, and reproducible vulnerability validation. Operational experience includes Microsoft Sentinel and Defender XDR, KQL, Sigma, Security Onion, Suricata, Zeek, Python, and PowerShell.

**Certifications:** Microsoft Certified: Security Operations Analyst Associate (SC-200) · CompTIA Security+

## Connect

Roseville, California · Open to remote vulnerability research and security engineering roles.

[Website](https://ibondarenko.com) · [LinkedIn](https://www.linkedin.com/in/ievgen-bondarenko-b13098241/) · [Email](mailto:hi@ibondarenko.com)
