# Security Policy

## Supported Versions

Use this section to tell people about which versions of your project are
currently being supported with security updates.

| Version      | Supported                                                                                                                          |
| -------------| -----------------------------------------------------------------------------------------------------------------------------------|
| Latest       | Yes, will have acesss shut down and will update a new release                                                                      |
| All versions | Can shut down acesss, no fix possible due to how many releases would have to be changed, UNLESS it is only 1-3 versions that fixed |

## Reporting a Vulnerability

Probally will take 1-3 days to get a responce to the vulnerability then I will try to reproduce and shut down access to server versions/client versions automaticly depending on the severity. Clients/Servers cannot be forced shut down if they have been motified but servers will refuse connections to clients that advertise (can be spoofed) a vulnerable version. Server COULD spoof this because this is incase the client couldn't connect to github to verify if it was true. Same with clients, they will refuse a server that has a vulnerable version.
