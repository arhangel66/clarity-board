# ADR-0003: OpenRouter as Primary LLM Provider

- Status: Accepted
- Date: 2026-03-05
- Deciders: project maintainers

## Context

Application requires chat generation for card operations and can optionally use OpenAI for transcription/other capabilities. Need pragmatic provider strategy with low coupling.

## Decision

Use OpenRouter as primary chat provider via OpenAI-compatible SDK in `AIService`.

- Primary chat model currently configured through OpenRouter.
- OpenAI client remains optional for non-chat features (e.g., transcription).
- DI wiring in `backend/app/construct.py` owns provider instantiation.

## Consequences

### Positive

- Flexibility to switch chat model/provider with minimal API surface changes.
- Keeps integration code concentrated in one service.

### Negative

- Additional dependency on OpenRouter availability and API behavior.
- Requires explicit fallback strategy if provider unavailable.

## Alternatives Considered

- OpenAI-only provider for all AI features.
- Multi-provider runtime routing in initial architecture.
