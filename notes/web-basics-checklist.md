# Web basics checklist

🇹🇷 [Türkçe](web-basics-checklist.tr.md)

Study notes for intentionally vulnerable or authorised targets only.

## 1. First look

- [ ] Open the site in a browser with the developer tools (F12) open. Read the page source and comments.
- [ ] `/robots.txt`, `/sitemap.xml`, `/.git/`, `/admin`, `/backup`, `/login`.
- [ ] Identify the stack: response headers (`curl -I URL`), error pages, cookie names, file extensions.
- [ ] Look at JavaScript files and API calls in the Network tab; they list endpoints and parameters.

## 2. Content discovery

- [ ] Directory and file brute force (gobuster / ffuf), with extensions that fit the stack.
- [ ] Virtual hosts and subdomains if a domain name is involved.
- [ ] Parameter discovery on pages that look dynamic.

## 3. Authentication and sessions

- [ ] Default credentials for the product you identified (only where rules allow).
- [ ] User enumeration: different messages for "unknown user" vs "wrong password".
- [ ] Cookies: flags (`HttpOnly`, `Secure`), predictable values, JWTs (decode, check `alg` and signature handling).
- [ ] Password reset logic, registration, "remember me".

## 4. Access control

- [ ] IDOR: change IDs in URLs/bodies (`/user?id=1` to `2`). Can you read other users' data?
- [ ] Can a normal user reach admin pages or call admin APIs directly?
- [ ] HTTP method tampering (GET vs POST vs PUT).

## 5. Input handling (test every parameter, header and cookie)

| Test | Quick probe | What a hit looks like |
|------|-------------|-----------------------|
| SQL injection | `'` or `' OR '1'='1` | SQL error, changed results |
| XSS | `<script>alert(1)</script>` | script runs / is reflected unescaped |
| Path traversal / LFI | `../../../../etc/passwd` | file contents returned |
| Command injection | `; id` or `\| id` | command output appears |
| SSRF | URL parameter pointing at your own server | request arrives at your listener |
| SSTI | `{{7*7}}` | `49` is rendered |
| File upload | upload a harmless test file with a changed extension/type | file is stored and reachable |

Test one thing at a time and watch the full response (status, length, time), not just the page.

## 6. Tools

- Burp Suite Community or OWASP ZAP: intercept and replay requests.
- `curl -i`, `curl -X POST -d 'a=b'`, `curl -H 'Header: value'`, `curl -b 'name=value'`.
- `sqlmap` only where the rules allow automated tools; understand the manual injection first.

## 7. Reference

The OWASP Top 10 is a good map of what to look for: broken access control, cryptographic
failures, injection, insecure design, security misconfiguration, vulnerable components,
authentication failures, integrity failures, logging failures, SSRF.
