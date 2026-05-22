![header](https://www.digitalsolutionservices.com/img/services/website1.gif)

# Ievgen (Jack) Bondarenko

**Security Researcher & Compliance Advisor**

I came to security through compliance  frameworks, audits, the long documents that describe what should be true. I stayed because the code describes what is, and the gap between the two is where the interesting work lives.

These days I spend most of my time reading implementations against their specifications. I look for the edge case that nobody wrote a test for, the assumption that holds everywhere except in one narrow window. When something survives review, I send it upstream.

I'm a researcher by temperament more than by title. I read more than I write, write more than I publish, and try to keep the ratio honest. The good bugs tend to be quiet  they sit between two lines that both look correct, and they reward patience over cleverness.



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

## 🛡 Published CVEs & Advisories

Four High-severity CVEs in [InternLM/lmdeploy](https://github.com/InternLM/lmdeploy), an LLM serving framework.

<!-- CVES:START -->
| CVE | Severity | Vulnerability |
|-----|----------|---------------|
| [CVE-2025-67729](https://github.com/advisories/GHSA-9pf3-7rrr-x5jh) | High | Arbitrary code execution via insecure deserialization in `torch.load()` |
| [CVE-2026-33626](https://github.com/advisories/GHSA-6w67-hwm5-92mq) | High | Server-side request forgery via vision-language image loading |
| [CVE-2026-46432](https://github.com/advisories/GHSA-m549-qq94-fvhg) | High | Arbitrary code execution via hardcoded `trust_remote_code=True` |
| [CVE-2026-46517](https://github.com/advisories/GHSA-9xq9-36w5-q796) | High | Unsafe remote-code load path with no user opt-out |
<!-- CVES:END -->

## 🛡 Hands-On Defense

Security blue team through a 48-hour live red team engagement. Hardened a multi-zone 
WAN/DMZ/LAN environment: deployed Security Onion IDS/IPS, Suricata, Zeek, 
Wazuh HIDS, PFSense firewall rules, honeypots, and automated incident 
response. Maintained service uptime under sustained attack against a 
NIST + HIPAA baseline.
## 🔼 Upstream Contributions

Upstream pull requests into production open-source projects, focused on memory-safety, DoS hardening, and protocol validation.

<!-- PRS:START -->
**12** merged pull requests across **5** open-source projects.

**[google/gvisor](https://github.com/google/gvisor)** - container runtime / application kernel
- [#13181](https://github.com/google/gvisor/pull/13181) - stack: document conntrack seed regen requirement on iptables S/R
- [#13165](https://github.com/google/gvisor/pull/13165) - tcp: strict RFC 5961 RST sequence validation (contributes to #1132)
- [#13153](https://github.com/google/gvisor/pull/13153) - lisafs: reject FRemoveXattr on deleted files
- [#13015](https://github.com/google/gvisor/pull/13015) - systrap: hold sysmsgThreadsMu around map read in switchToApp
- [#12927](https://github.com/google/gvisor/pull/12927) - systrap: fix TOCTOU on ThreadID in NotifyInterrupt
- [#12925](https://github.com/google/gvisor/pull/12925) - tun: add empty data check before AsSlice()[0] in TUN Write()

**[google/bumble](https://github.com/google/bumble)** - Bluetooth protocol stack
- [#918](https://github.com/google/bumble/pull/918) - avdtp: bound message assembler to drop truncated PDUs (DoS prevention)
- [#914](https://github.com/google/bumble/pull/914) - sdp: bound DataElement parse recursion to prevent RecursionError DoS
- [#912](https://github.com/google/bumble/pull/912) - fix: add input validation to prevent remote crash from empty/malformed input

**[google/osv-scanner](https://github.com/google/osv-scanner)** - vulnerability scanner
- [#2748](https://github.com/google/osv-scanner/pull/2748) - fix: correct misleading docstrings in scalibrextract extractors

**[swiftlang/swift-package-manager](https://github.com/swiftlang/swift-package-manager)** - Apple, Swift toolchain
- [#10001](https://github.com/swiftlang/swift-package-manager/pull/10001) - registry: reject extracted archives with escaping symlinks

**[tink-crypto/tink-py](https://github.com/tink-crypto/tink-py)** - Google cryptography library
- [#76](https://github.com/tink-crypto/tink-py/pull/76) - fix(jwt): reject JWK Sets with duplicate JSON keys
<!-- PRS:END -->

## 📜 Certifications

<p>
 
  <img src="https://img.shields.io/badge/CompTIA-Security%2B-FF0000?style=flat-square&logo=comptia&logoColor=white" />
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
