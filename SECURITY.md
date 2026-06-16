# Security Policy

## Supported Versions

The current `main` branch is the supported development line.

## Reporting a Vulnerability

Please report security issues by opening a private advisory on GitHub when available, or by contacting the maintainer through the GitHub profile associated with this repository.

Do not include private study documents, copyrighted source material, or personal data in a public issue. If a bug requires a sample file, reduce it to a minimal synthetic example first.

## Security Notes

`study-pack-builder` is a local CLI. It should not require network access for core CSV, quiz, or PDF processing. Future AI-assisted features should be optional and must clearly document when data is sent to an external API.
