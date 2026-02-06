# Tooling Strategy (Dev vs Runtime)

This folder captures MCP-specific configuration and server stubs.

## Separation of concerns
- **Dev tooling MCP servers**: used for repository inspection, lint/test orchestration, spec validation, etc.
- **Runtime MCP servers**: used by the running application to interact with external systems (news, social, commerce, etc.).

## Principles
- Keep runtime servers minimal and explicitly permissioned.
- Keep dev tooling servers isolated from runtime credentials.
- Store templates and examples here; keep secrets out of the repo.

