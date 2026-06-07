![header](https://www.digitalsolutionservices.com/img/services/website1.gif)

# Ievgen (Jack) Bondarenko

**Security Researcher & Compliance Advisor**

I came to security through compliance  frameworks, audits, the long documents that describe what should be true. I stayed because the code describes what is, and the gap between the two is where the interesting work lives.

These days I spend most of my time reading implementations against their specifications. I look for the edge case that nobody wrote a test for, the assumption that holds everywhere except in one narrow window. When something survives review, I send it upstream.

I'm a researcher by temperament more than by title. I read more than I write, write more than I publish, and try to keep the ratio honest. The good bugs tend to be quiet  they sit between two lines that both look correct, and they reward patience over cleverness.

<!-- BADGES:START -->
<p>
  <a href="https://github.com/advisories?query=credit%3Aibondarenko1"><img alt="1 CVE published" src="https://img.shields.io/badge/CVEs%20Published-1-c0392b?style=flat-square&logo=cve&logoColor=white&labelColor=222"></a>
  <a href="https://github.com/pulls?q=is%3Apr+author%3Aibondarenko1+is%3Amerged+-user%3Aibondarenko1"><img alt="15 merged PRs" src="https://img.shields.io/badge/Merged%20PRs-15-2da44e?style=flat-square&logo=github&logoColor=white&labelColor=222"></a>
</p>
<!-- BADGES:END -->

## 🌐 About Me

I work at the intersection of cybersecurity, low-level systems, and compliance engineering. Most of my professional work has been in regulated environments  healthcare, financial services, MSPs, legal firms  where the question is not whether controls exist, but whether they hold up when something unusual arrives at the door.

## 🔧 What I'm Currently Working On

Reading code in places that are supposed to be safe. Container runtimes, protocol stacks, syscall layers. Writing notes. Sending small patches upstream when they survive review.

On the compliance side, I keep returning to one question: how does runtime evidence  what the system actually does under load  map back to the controls auditors ask about. Most frameworks describe intent. The interesting work is closing the distance between intent and behavior.

## 🎯 Focus Areas

- Container and sandbox runtime internals
- Protocol parsers and the state machines around them
- Race conditions, TOCTOU, and the windows where they hide
- Fuzzing and differential testing
- Compliance frameworks: HIPAA · NIST CSF · ISO 27001 · PCI DSS · SOC 2

## 📂 Featured Projects

**[azure-soc-detection-lab](https://github.com/ibondarenko1/azure-soc-detection-lab)** — Detection-as-Code on a live Microsoft Sentinel + Defender XDR tenant. Five AzureActivity analytics rules (MITRE-mapped), each proven end-to-end (trigger → incident → investigation), authored as versioned YAML and deployed by a **PR-gated GitHub Actions pipeline via OIDC** (no secrets) — not hand-clicked. Built alongside SC-200.

**[m365-security-operations](https://github.com/ibondarenko1/m365-security-operations)** — detect-and-remediate audit toolkit for solo defenders running Microsoft 365 + Cloudflare in small organizations. Five domains audited in one PowerShell command (Sentinel, Defender for O365, DNS + email auth, Entra ID identity, Defender for Cloud); ~60 framework-tagged checks (NIST CSF, NIST 800-53, ISO 27001, MITRE ATT&CK, MCSB); every finding linked to a ready-to-deploy remediation artifact. 30-second demo via mock mode. MIT licensed.

**[llm-serving-security](https://github.com/ibondarenko1/llm-serving-security)** — practical security reference for the LLM serving stack. CVE matrix, vulnerability classes, and hardening guidance for vLLM, Triton, lmdeploy, BentoML, SGLang, Ollama, TGI.

**[blue-team-engagement](https://github.com/ibondarenko1/blue-team-engagement)** — one-week red-team / blue-team enterprise network defense engagement: case study, custom Sigma detection pack, and methodology against sustained attack across multi-zone WAN/DMZ/LAN.

## 🛡 Hands-On Defense

Security blue team through a 48-hour live red team engagement. Hardened a multi-zone 
WAN/DMZ/LAN environment: deployed Security Onion IDS/IPS, Suricata, Zeek, 
Wazuh HIDS, PFSense firewall rules, honeypots, and automated incident 
response. Maintained service uptime under sustained attack against a 
NIST + HIPAA baseline.
## 📜 Certifications

<p>
  <img src="https://img.shields.io/badge/CompTIA-Security%2B-FF0000?style=flat-square&logo=comptia&logoColor=white" />
  <img src="https://img.shields.io/badge/Microsoft%20Certified-Security%20Operations%20Analyst%20Associate-0078D4?style=flat-square&logo=data:image/svg%2Bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyMyAyMyI+PHBhdGggZmlsbD0iI2YyNTAyMiIgZD0iTTEgMWgxMHYxMEgxeiIvPjxwYXRoIGZpbGw9IiM3ZmJhMDAiIGQ9Ik0xMiAxaDEwdjEwSDEyeiIvPjxwYXRoIGZpbGw9IiMwMGE0ZWYiIGQ9Ik0xIDEyaDEwdjEwSDF6Ii8+PHBhdGggZmlsbD0iI2ZmYjkwMCIgZD0iTTEyIDEyaDEwdjEwSDEyeiIvPjwvc3ZnPg==" />
</p>

## 🛠 Skills & Tools

<p>
  <img src="https://img.shields.io/badge/OS-Windows-blue?style=flat-square&logo=windows&logoColor=white" />
  <img src="https://img.shields.io/badge/OS-Kali%20Linux-blue?style=flat-square&logo=linux&logoColor=white" />
  <img src="https://img.shields.io/badge/Networking-Cisco%20IOS-1BA0E2?style=flat-square&logo=cisco&logoColor=white" />
  <img src="https://img.shields.io/badge/Networking-Wireshark-1679A7?style=flat-square&logo=wireshark&logoColor=white" />
  <img src="https://img.shields.io/badge/Virtualization-Hyper--V-0078D6?style=flat-square&logo=microsoft&logoColor=white" />
  <img src="https://img.shields.io/badge/Sysadmin-Active%20Directory-0078D6?style=flat-square&logo=microsoft&logoColor=white" />
  <img src="https://img.shields.io/badge/Scripting-PowerShell-5391FE?style=flat-square&logo=powershell&logoColor=white" />
  <img src="https://img.shields.io/badge/SIEM-Elastic%20%7C%20Kibana-005571?style=flat-square&logo=elastic&logoColor=white" />
  <img src="https://img.shields.io/badge/SIEM-Security%20Onion%202.4-3D5A80?style=flat-square&logoColor=white" />
  <img src="https://img.shields.io/badge/HIDS-Wazuh-005377?style=flat-square&logoColor=white" />
  <img src="https://img.shields.io/badge/IDS-Suricata-FF6900?style=flat-square&logoColor=white" />
  <img src="https://img.shields.io/badge/NSM-Zeek-2596be?style=flat-square&logoColor=white" />
  <img src="https://img.shields.io/badge/Framework-MITRE%20ATT%26CK-CC0000?style=flat-square&logoColor=white" />
  <img src="https://img.shields.io/badge/Web%20Testing-Burp%20Suite-FF6633?style=flat-square&logoColor=white" />
  <img src="https://img.shields.io/badge/Web%20Testing-OWASP%20ZAP-00549E?style=flat-square&logoColor=white" />
  <img src="https://img.shields.io/badge/Cloud-AWS%20%7C%20Azure-FF9900?style=flat-square&logo=amazonaws&logoColor=white" />
  <img src="https://img.shields.io/badge/Automation-GitHub%20Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white" />
</p>

## 🤝 Let's Connect

Open to technical conversations and collaboration with people working in low-level security, protocol research, or compliance engineering.

🔗 LinkedIn: [ievgen-jack-bondarenko](https://www.linkedin.com/in/ievgen-bondarenko-b13098241/)
🐙 GitHub: [ibondarenko1](https://github.com/ibondarenko1)
