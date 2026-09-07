# Ievgen (Jack) Bondarenko

**Security Engineering · Vulnerability Research · Detection Engineering · AI Infrastructure**

I work across the boundary between how systems fail and how defenders detect that failure.

On the research side, I audit source code in AI infrastructure, container runtimes, cloud integrations, and security-sensitive backend systems. That work has led to published vulnerabilities, Google VRP findings, coordinated disclosures, and upstream security fixes.

On the defensive side, I build controls that are tested end to end rather than treated as configuration: detection logic, controlled triggering, incident generation, investigation evidence, false-positive measurement, and deployment as code.

More recently, those two sides have started to converge in my work: security tooling and detection systems that combine source-level analysis, operational telemetry, reproducible engineering, and ML where it improves the security workflow.

<!-- BADGES:START -->
<p>
  <a href="https://github.com/advisories?query=credit%3Aibondarenko1"><img alt="2 CVE published" src="https://img.shields.io/badge/CVEs%20Published-2-c0392b?style=flat-square&logo=cve&logoColor=white&labelColor=222"></a>
  <a href="https://github.com/pulls?q=is%3Apr+author%3Aibondarenko1+is%3Amerged+-user%3Aibondarenko1"><img alt="22 merged PRs" src="https://img.shields.io/badge/Merged%20PRs-22-2da44e?style=flat-square&logo=github&logoColor=white&labelColor=222"></a>
</p>
<!-- BADGES:END -->

## 🔬 Selected Work

### [Security Anomaly ML](https://github.com/ibondarenko1/security-anomaly-ml)

Open-source ML network-flow detector that turns unlabeled CICFlowMeter-compatible traffic into deterministic analyst-facing security incidents.

The v0.1 release includes a frozen temporally validated model, causal feature pipeline, deterministic incident aggregation, versioned `incident-v1` output, Python CLI, Docker distribution, real-model end-to-end regression, and public CI.

The project is intentionally explicit about its limits: usable as a research/evaluation product, but not presented as production-ready.

### AI & Infrastructure Security Research

- **[GHSA-7gwp-5pfp-969j](https://github.com/advisories/GHSA-7gwp-5pfp-969j)** — MLflow, Critical: unauthenticated full-read SSRF through redirect and DNS-rebinding weaknesses in webhook delivery.
- **CVE-2026-46517 / GHSA-9xq9-36w5-q796** — vulnerability in `lmdeploy`, an AI model inference server, resolved through coordinated disclosure.
- **Google Cloud VRP award** — SSRF, API-key disclosure, and response forgery through a per-request `baseUrl` override affecting Gemini and Vertex AI client paths.
- **[llm-serving-security](https://github.com/ibondarenko1/llm-serving-security)** — security reference for the LLM serving stack, covering vulnerability classes and hardening across vLLM, Triton, lmdeploy, SGLang, BentoML, Ollama, and TGI.

### Detection Engineering

**[azure-sentinel-detection-engineering](https://github.com/ibondarenko1/azure-sentinel-detection-engineering)**

Detection-as-Code on Microsoft Sentinel and Defender: KQL detections mapped to MITRE ATT&CK, controlled triggers, incident generation, investigation evidence, false-positive measurement, and PR-gated deployment through GitHub Actions and OIDC.

## 🧩 Research & Upstream Engineering

Merged security and hardening work across projects including:

- Google gVisor
- Kubernetes
- Firecrawl
- Azure Sentinel
- Swift Package Manager
- OSV-Scanner
- Tink

The work spans container hardening, validation boundaries, race conditions, crash handling, sandbox behavior, shared-memory security, SSRF defenses, and protocol/API behavior.

Coordinated disclosure experience includes GitHub Security Advisories, Google VRP, Microsoft MSRC, and CERT/CC VINCE.

## 🛡 Defensive Engineering

Hands-on work spans cloud, endpoint, identity, and network telemetry:

- Microsoft Sentinel, Defender XDR, Defender for Endpoint, Entra ID
- KQL, Sigma, MITRE ATT&CK
- Security Onion, Suricata, Zeek, Wazuh
- Elastic / Kibana
- pfSense
- Windows Server / Active Directory
- Python and PowerShell

I have also worked through live red-team / blue-team engagements involving segmented WAN/DMZ/LAN environments, IDS/IPS, firewall policy, honeypots, incident response, and maintaining service availability under sustained attack.

## 🎯 Current Focus

- **Vulnerability research:** source-level analysis of AI infrastructure, cloud integrations, container boundaries, and security-sensitive backend systems.
- **Detection engineering:** tested detections, Detection-as-Code, SIEM/XDR engineering, and operational signal quality.
- **AI infrastructure security:** model-serving systems, inference infrastructure, isolation boundaries, and attack surfaces created around AI workloads.
- **Security tooling:** reproducible systems that connect detection, program analysis, automation, and ML without hiding the evidence behind the result.
- **Security & compliance engineering:** SOC 2, ISO 27001, HIPAA, and NIST controls implemented as measurable operational systems rather than policy-only artifacts.

## 📜 Certifications

<p>
  <img src="https://img.shields.io/badge/Microsoft%20Certified-Security%20Operations%20Analyst%20Associate%20(SC--200)-0078D4?style=flat-square&logo=data:image/svg%2Bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyMyAyMyI+PHBhdGggZmlsbD0iI2YyNTAyMiIgZD0iTTEgMWgxMHYxMEgxeiIvPjxwYXRoIGZpbGw9IiM3ZmJhMDAiIGQ9Ik0xMiAxaDEwdjEwSDEyeiIvPjxwYXRoIGZpbGw9IiMwMGE0ZWYiIGQ9Ik0xIDEyaDEwdjEwSDF6Ii8+PHBhdGggZmlsbD0iI2ZmYjkwMCIgZD0iTTEyIDEyaDEwdjEwSDEyeiIvPjwvc3ZnPg==" />
  <img src="https://img.shields.io/badge/CompTIA-Security%2B-FF0000?style=flat-square&logo=comptia&logoColor=white" />
</p>

## 🛠 Tools

**Research**
<p>
  <img src="https://img.shields.io/badge/SAST-Semgrep-1B2B34?style=flat-square&logoColor=white" />
  <img src="https://img.shields.io/badge/Code%20Property%20Graph-Joern-6a1b9a?style=flat-square&logoColor=white" />
  <img src="https://img.shields.io/badge/SAST-CodeQL-2088FF?style=flat-square&logo=github&logoColor=white" />
  <img src="https://img.shields.io/badge/Supply%20Chain-OSV--Scanner-0b7285?style=flat-square&logoColor=white" />
</p>

**Detection & cloud**
<p>
  <img src="https://img.shields.io/badge/KQL-Kusto-3970e4?style=flat-square&logoColor=white" />
  <img src="https://img.shields.io/badge/SIEM-Microsoft%20Sentinel-0078D4?style=flat-square&logo=microsoftazure&logoColor=white" />
  <img src="https://img.shields.io/badge/XDR-Microsoft%20Defender-0078D4?style=flat-square&logo=microsoft&logoColor=white" />
  <img src="https://img.shields.io/badge/Identity-Entra%20ID-0078D4?style=flat-square&logo=microsoftazure&logoColor=white" />
  <img src="https://img.shields.io/badge/Detection--as--Code-GitHub%20Actions%20%2B%20OIDC-2088FF?style=flat-square&logo=githubactions&logoColor=white" />
  <img src="https://img.shields.io/badge/Detection-Sigma-1f6feb?style=flat-square&logoColor=white" />
</p>

**Platforms**
<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/PowerShell-5391FE?style=flat-square&logo=powershell&logoColor=white" />
  <img src="https://img.shields.io/badge/Linux-blue?style=flat-square&logo=linux&logoColor=white" />
  <img src="https://img.shields.io/badge/Windows%20Server-blue?style=flat-square&logo=windows&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white" />
</p>

## 🤝 Connect

Open to remote roles and selected technical work in security engineering, vulnerability research, detection engineering, and AI infrastructure security.

**Website:** [ibondarenko.com](https://ibondarenko.com)  
**LinkedIn:** [ievgen-bondarenko-b13098241](https://www.linkedin.com/in/ievgen-bondarenko-b13098241/)  
**Email:** [hi@ibondarenko.com](mailto:hi@ibondarenko.com)
