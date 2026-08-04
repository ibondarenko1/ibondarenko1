# Ievgen (Jack) Bondarenko

**Detection Engineering & Vulnerability Research** · Microsoft Sentinel · AI and container infrastructure

I work the defensive side of cloud security: detections that fire on a live Microsoft Sentinel and Defender tenant, each one proven end to end. A control isn't real until you can show it catching the thing it claims to catch, so I build the whole loop (rule logic, controlled trigger, the incident it raises, the investigation, the MITRE mapping) versioned and deployed like code, not clicked into a portal. The good signal is quiet; it sits between two events that both look normal, and it rewards patience over cleverness.

The other half of the work is source-level: I read code in container runtimes, protocol stacks, and the LLM serving stack, and report what I find. Knowing how a thing actually breaks, not just how its alert looks, is what tells you where to point the telemetry.

<!-- BADGES:START -->
<p>
  <a href="https://github.com/advisories?query=credit%3Aibondarenko1"><img alt="Published advisories" src="https://img.shields.io/badge/Published%20Advisories-2-c0392b?style=flat-square&logo=cve&logoColor=white&labelColor=222"></a>
  <a href="https://github.com/advisories/GHSA-7gwp-5pfp-969j"><img alt="Critical advisory" src="https://img.shields.io/badge/MLflow%20SSRF-Critical-8e1616?style=flat-square&labelColor=222"></a>
  <a href="https://bughunters.google.com/"><img alt="Google Cloud VRP" src="https://img.shields.io/badge/Google%20Cloud%20VRP-Rewarded-4285F4?style=flat-square&logo=google&logoColor=white&labelColor=222"></a>
  <a href="https://github.com/pulls?q=is%3Apr+author%3Aibondarenko1+is%3Amerged+-user%3Aibondarenko1"><img alt="20 merged PRs" src="https://img.shields.io/badge/Merged%20PRs-20-2da44e?style=flat-square&logo=github&logoColor=white&labelColor=222"></a>
</p>
<!-- BADGES:END -->

## 🎯 Focus

- **Detection engineering on the Microsoft stack:** Sentinel (KQL), Defender XDR, Defender for Endpoint, Entra ID.
- **Detection-as-Code:** versioned rules, PR-gated CI/CD, OIDC deploy, unit-tested and false-positive measured.
- **Vulnerability research:** static and symbolic analysis (Semgrep, Joern) with a separate verification stage, so what gets reported is what survived verification.
- **Three telemetry planes:** cloud control plane (Activity Log), endpoint, and identity (sign-ins).
- **MITRE ATT&CK mapping**, with Sigma for vendor-neutral portability.

## 🔬 Research and Upstream Contributions

- **[GHSA-7gwp-5pfp-969j](https://github.com/advisories/GHSA-7gwp-5pfp-969j)** (MLflow, Critical): unauthenticated full-read SSRF in webhook delivery. The existing URL guard was bypassable through unvalidated HTTP redirects and DNS rebinding, letting an unauthenticated caller read cloud instance metadata and internal services through the server. Credited independent finder.
- **CVE-2026-46517 / GHSA-9xq9-36w5-q796** (lmdeploy): vulnerability in an AI model inference server, resolved through coordinated disclosure.
- **Google Cloud VRP award:** SSRF, API key disclosure, and response forgery via a per-request `baseUrl` override in `@genkit-ai/google-genai`, affecting Gemini and Vertex AI client paths.
- **Merged upstream security fixes** in Google gVisor, Kubernetes, Azure Sentinel, Swift Package Manager, OSV-Scanner, and Tink-Crypto: container hardening, race conditions, crash handling, sandbox behavior, shared-memory security.
- Coordinated disclosure through Microsoft MSRC, Google VRP, and CERT/CC VINCE.

## 📂 Featured Projects

**[azure-sentinel-detection-engineering](https://github.com/ibondarenko1/azure-sentinel-detection-engineering)** (flagship): Detection-as-Code on a live Microsoft Sentinel + Defender XDR tenant. Nine MITRE-mapped analytics rules across control-plane, endpoint, and identity (including a multi-stage correlation rule, privilege grant → deployment, and a Resource Graph-backed NSG content rule), each proven end-to-end (trigger → incident → investigation) and checked by a live benign + attack harness that measures false positives instead of assuming them. Versioned YAML, deployed by a PR-gated GitHub Actions pipeline via OIDC (no secrets). Built alongside SC-200.

**[llm-serving-security](https://github.com/ibondarenko1/llm-serving-security)**: security reference for the LLM serving stack. CVE matrix, vulnerability classes, and hardening for vLLM, Triton, lmdeploy, BentoML, SGLang, Ollama, TGI. The point where the research above and the detection work meet.

**[m365-security-operations](https://github.com/ibondarenko1/m365-security-operations)**: detect-and-remediate audit toolkit for Microsoft 365 + Cloudflare in small organizations. Five domains in one PowerShell command; ~60 framework-tagged checks (NIST CSF, NIST 800-53, ISO 27001, MITRE ATT&CK, MCSB), each finding linked to a ready-to-deploy remediation. 30-second demo via mock mode. MIT licensed.

**[blue-team-engagement](https://github.com/ibondarenko1/blue-team-engagement)**: one-week red-team / blue-team enterprise defense engagement. Case study, custom Sigma detection pack, and methodology against sustained attack across a multi-zone WAN/DMZ/LAN.

## 🛡 Hands-On Defense

Blue team through live red-team engagement. Hardened a multi-zone WAN/DMZ/LAN: deployed Security Onion IDS/IPS, Suricata, Zeek, Wazuh HIDS, pfSense firewall rules, honeypots, and automated incident response. Maintained service uptime under sustained attack against a NIST + HIPAA baseline.

## 📜 Certifications

<p>
  <img src="https://img.shields.io/badge/Microsoft%20Certified-Security%20Operations%20Analyst%20Associate%20(SC--200)-0078D4?style=flat-square&logo=data:image/svg%2Bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyMyAyMyI+PHBhdGggZmlsbD0iI2YyNTAyMiIgZD0iTTEgMWgxMHYxMEgxeiIvPjxwYXRoIGZpbGw9IiM3ZmJhMDAiIGQ9Ik0xMiAxaDEwdjEwSDEyeiIvPjxwYXRoIGZpbGw9IiMwMGE0ZWYiIGQ9Ik0xIDEyaDEwdjEwSDF6Ii8+PHBhdGggZmlsbD0iI2ZmYjkwMCIgZD0iTTEyIDEyaDEwdjEwSDEyeiIvPjwvc3ZnPg==" />
  <img src="https://img.shields.io/badge/CompTIA-Security%2B-FF0000?style=flat-square&logo=comptia&logoColor=white" />
</p>

## 🛠 Skills & Tools

**Vulnerability research**
<p>
  <img src="https://img.shields.io/badge/SAST-Semgrep-1B2B34?style=flat-square&logoColor=white" />
  <img src="https://img.shields.io/badge/Code%20Property%20Graph-Joern-6a1b9a?style=flat-square&logoColor=white" />
  <img src="https://img.shields.io/badge/SAST-CodeQL-2088FF?style=flat-square&logo=github&logoColor=white" />
  <img src="https://img.shields.io/badge/Supply%20Chain-SCA%20%2F%20OSV--Scanner-0b7285?style=flat-square&logoColor=white" />
  <img src="https://img.shields.io/badge/Classification-OWASP%20%2F%20CWE%20%2F%20CVSS-b8860b?style=flat-square&logoColor=white" />
  <img src="https://img.shields.io/badge/Process-Coordinated%20Disclosure-495057?style=flat-square&logoColor=white" />
</p>

**Detection & cloud (primary)**
<p>
  <img src="https://img.shields.io/badge/KQL-Kusto%20Query%20Language-3970e4?style=flat-square&logoColor=white" />
  <img src="https://img.shields.io/badge/SIEM-Microsoft%20Sentinel-0078D4?style=flat-square&logo=microsoftazure&logoColor=white" />
  <img src="https://img.shields.io/badge/XDR-Microsoft%20Defender-0078D4?style=flat-square&logo=microsoft&logoColor=white" />
  <img src="https://img.shields.io/badge/EDR-Defender%20for%20Endpoint-0078D4?style=flat-square&logo=microsoft&logoColor=white" />
  <img src="https://img.shields.io/badge/Identity-Entra%20ID-0078D4?style=flat-square&logo=microsoftazure&logoColor=white" />
  <img src="https://img.shields.io/badge/Cloud-Azure-0089D6?style=flat-square&logo=microsoftazure&logoColor=white" />
  <img src="https://img.shields.io/badge/Detection--as--Code-GitHub%20Actions%20%2B%20OIDC-2088FF?style=flat-square&logo=githubactions&logoColor=white" />
  <img src="https://img.shields.io/badge/Detection-Sigma-1f6feb?style=flat-square&logoColor=white" />
  <img src="https://img.shields.io/badge/Framework-MITRE%20ATT%26CK-CC0000?style=flat-square&logoColor=white" />
</p>

**Defensive operations**
<p>
  <img src="https://img.shields.io/badge/SIEM-Security%20Onion%202.4-3D5A80?style=flat-square&logoColor=white" />
  <img src="https://img.shields.io/badge/SIEM-Elastic%20%7C%20Kibana-005571?style=flat-square&logo=elastic&logoColor=white" />
  <img src="https://img.shields.io/badge/HIDS-Wazuh-005377?style=flat-square&logoColor=white" />
  <img src="https://img.shields.io/badge/IDS-Suricata-FF6900?style=flat-square&logoColor=white" />
  <img src="https://img.shields.io/badge/NSM-Zeek-2596be?style=flat-square&logoColor=white" />
  <img src="https://img.shields.io/badge/Firewall-pfSense-212121?style=flat-square&logoColor=white" />
</p>

**Platforms & scripting**
<p>
  <img src="https://img.shields.io/badge/Scripting-PowerShell-5391FE?style=flat-square&logo=powershell&logoColor=white" />
  <img src="https://img.shields.io/badge/Scripting-Python-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Audit-Go-00ADD8?style=flat-square&logo=go&logoColor=white" />
  <img src="https://img.shields.io/badge/Audit-C%2B%2B-00599C?style=flat-square&logo=cplusplus&logoColor=white" />
  <img src="https://img.shields.io/badge/OS-Windows%20Server-blue?style=flat-square&logo=windows&logoColor=white" />
  <img src="https://img.shields.io/badge/OS-Linux-blue?style=flat-square&logo=linux&logoColor=white" />
  <img src="https://img.shields.io/badge/Sysadmin-Active%20Directory-0078D6?style=flat-square&logo=microsoft&logoColor=white" />
  <img src="https://img.shields.io/badge/Analysis-Wireshark-1679A7?style=flat-square&logo=wireshark&logoColor=white" />
</p>

## 🤝 Let's Connect

Open to remote roles in detection engineering, cloud security, and vulnerability research, and to technical conversation with people working in cloud detection, SIEM engineering, AI infrastructure security, or low-level security.

🔗 **LinkedIn:** [ievgen-jack-bondarenko](https://www.linkedin.com/in/ievgen-bondarenko-b13098241/)

🐙 **GitHub:** [ibondarenko1](https://github.com/ibondarenko1)
