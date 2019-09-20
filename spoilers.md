# Spoilers

The challenges have the following vulnerabilities:

- [Injection](https://www.owasp.org/index.php/Injection_Flaws)
- [Broken Authentication and Session Management](https://www.owasp.org/index.php/Broken_Authentication_and_Session_Management)
- [Broken Access Control](https://www.owasp.org/index.php/Broken_Access_Control)
- [Security Misconfiguration](https://www.owasp.org/index.php/Top_10-2017_A6-Security_Misconfiguration)
- [Using Components with Known Vulnerabilities](https://www.owasp.org/index.php/Top_10-2017_A9-Using_Components_with_Known_Vulnerabilities)
- [Insecure Deserialization](https://www.owasp.org/index.php/Top_10-2017_A8-Insecure_Deserialization)
- [Path Traversal](https://www.owasp.org/index.php/Path_Traversal)
- [Timing attack](https://en.wikipedia.org/wiki/Timing_attack)

<details>
 <summary>Show spoilers</summary>

 Injection
 - `forum2` is vulnerable to SQL injection

 Broken Authentication and Session Management
 - `pin` has a weak password, easy to brute-force
 - `forum` uses a broken authentication scheme (username in a cookie)
 - `name` stores password in plaintext (you need another vulnerability to retrieve it, though)

 Broken Access Control
 - `notes` doesn't authenticate the AJAX endpoints
 - `name` has some validation that is enforced only client-side

 Security Misconfiguration
 - `name` has Flask debug mode enabled, allowing you to see stack trace

 Using Components with Known Vulnerabilities
 - `mines2` uses PyYAML version in which `yaml.load` allows arbitrary Python execution

 Insecure Deserialization
 - `mines` uses Python's `exec()` (a variant of eval) to load save game
 - `mines2` does slightly better (YAML) but has a vulnerability

 Path Traversal
 - `gallery` accepts paths using `..`

 Timing attack
 - `pin2` can be solved by analyzing response times

</details>
