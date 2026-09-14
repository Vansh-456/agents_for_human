# AnnaSetu — Submission-Ready End-to-End Builder Plan

> **Track:** Good Neighbor Agents  
> **Product:** AnnaSetu, an autonomous food-rescue coordination agent for food donors, community organisations, and delivery partners.  
> **North-star outcome:** maximise safely delivered meals before their usable window expires, while interrupting humans only for decisions that cannot be safely automated.

## 1. Definition of Done

AnnaSetu is ready to submit only when a judge can open a public URL, trigger a realistic surplus event, see a genuine Strands agent tool loop create and safety-check a plan, observe a rider failure cause an automatic re-plan, and inspect the resulting audit trail and measurable impact.

This plan implements the actual requirements for the AWS Agents for Humans Hackathon:

- A **new** project built during the submission period, using the **Strands Agents SDK** to do real, end-to-end work for people.
- A Good Neighbor product serving a group—not an isolated chatbot.
- A public source repository with all setup instructions, an MIT or Apache-2.0 license, and visible license metadata.
- An architecture diagram; an AWS Builder ID; and a video of at most five minutes containing a working demo plus the problem, audience, and impact pitch.
- Optional but scoring-positive live deployment and Amazon Bedrock AgentCore use.

Sources: [official overview and judging criteria](https://agentsforhumans.devpost.com/), [official FAQs and submission guidance](https://agentsforhumans.devpost.com/details/faqs), [AWS Builder Center announcement](https://builder.aws.com/content/3INJ4miNJzex0c3YRxNY4CDehgQ/agents-for-humans-hackathon-build-ai-agents-that-improve-everyday-life).

### Non-negotiable acceptance tests

- [ ] A natural-language donation, web form, or signed webhook creates a structured surplus event; it is not converted into fixed quantities or fixed deadlines.
- [ ] The system uses a Strands agent with a Bedrock model and scoped tools. Its tool calls and resulting decisions are persisted and visible in the UI.
- [ ] No plan is executable unless the deterministic AnnaGuard policy returns `PASS` for each allocation leg.
- [ ] A real disruption event (rider cancellation, changed capacity, delay, or expiry risk) invalidates the affected plan and runs re-planning without a human clicking “fix.”
- [ ] Every displayed metric is calculated from stored workflow data, never hard-coded.
- [ ] The deployed app has a successful smoke test and the local demo works without paid third-party credentials.
- [ ] The primary demo, safety-block demo, and prediction demo are deterministic and reproducible from one command or the `/demo` route.

## 2. What Judges Must Be Able to See

| Judging dimension | Concrete proof in AnnaSetu |
| --- | --- |
| Technological implementation | Strands agent traces, Bedrock structured extraction/reasoning, least-privilege tools, durable workflows, tests, live URL, and preferably AgentCore Runtime/Observability. |
| Design | One coherent operational dashboard for donor, NGO, rider, and operator—not disconnected simulation widgets. |
| Potential impact | A defined pilot geography and operational model, verified safety boundaries, partners/data provenance, and measurable saved-meals, response-time, and recovery metrics. |
| Creativity and originality | Proactive food-rescue network: forecast → pre-position capacity/rider → verify actual surplus → execute → self-heal. |
| Presentation | A five-minute story with visible tool actions, safety gates, automatic recovery, outcome metrics, architecture, and an honest statement of demo vs. live integrations. |

## 3. Product Scope: Real Operations, Not a Toy Dataset

### Pilot operating model

Build for one named pilot area (for example, a 5–10 km zone in Delhi NCR). Target:

- **Donors:** restaurants, caterers, corporate canteens, grocers; they report prepared food, packaging, dietary attributes, quantity, temperature/evidence, pickup deadline, and location.
- **Recipients:** verified food banks, shelters, community kitchens; they publish current acceptance capacity, operating hours, dietary restrictions, storage capability, and receiving contact.
- **Riders:** verified volunteers or logistics partners who publish availability, capacity, vehicle type, live/last-known location, and consented contact route.
- **Operators:** only handle missing safety evidence, recipient-policy conflicts, tied high-impact allocations, or failed automated recovery.

### Data policy

- [ ] Use partner-approved, public, anonymised, or carefully modelled operational data; do not include real personal data, private addresses, phone numbers, or food-recipient records in the public repository.
- [ ] Give every seed record a `source_type` (`partner_approved`, `public_aggregate`, `synthetic_operational`) and `source_reference`.
- [ ] Do not use random or fixed “45 meals” records. Seed data must encode plausible locations, operating hours, food types, preparation times, packaging, capacities, rider shifts, historic events, and disruptions.
- [ ] Include a generator that creates reproducible, constrained operational data for the pilot zone, with a documented seed. It must preserve geospatial and capacity constraints rather than produce arbitrary fixtures.
- [ ] Keep demo data separate from production data and label simulated, observed, predicted, and user-supplied values everywhere.

### Measured success metrics

- [ ] Meals offered, assigned, picked up, delivered, expired, rejected, and safely blocked.
- [ ] Delivery completion rate; median time from report to assignment; median pickup ETA; re-plan recovery rate; safety-policy violation count (target: zero).
- [ ] Donor response time, recipient acceptance rate, rider punctuality, and quantity accuracy; explain the contribution of these factors to trust without making opaque automated exclusions.
- [ ] Forecast precision/recall or MAE against held-out simulated/partner-approved historical events; show confidence and data coverage.

## 4. Target Architecture

```text
Donor / NGO / Rider web app or signed WhatsApp webhook
                        |
            CloudFront + S3 / API Gateway + WAF
                        |
             FastAPI service or Lambda API handlers
                        |
           EventBridge (domain events) + SQS (work queue/DLQ)
                        |
          Workflow worker: Strands Supervisor on Bedrock
       /            |             |              \
Signal          Forecast/Demand   Allocation    Logistics/Trust
  |                    |              |              |
  +--------------------+--------------+--------------+
                       |
       Deterministic AnnaGuard policy engine (cannot be bypassed)
                       |
       DynamoDB workflow state + S3 evidence/archive + CloudWatch traces
                       |
       Notifications / rider reservation / human decision queue
```

### AWS service responsibilities

| Service | Required use in the implementation |
| --- | --- |
| **Amazon Bedrock** | Model inference for structured message extraction, candidate-plan reasoning, explanations, and clarification requests. All outputs must conform to Pydantic schemas and be validated before action. |
| **Strands Agents SDK** | Genuine agentic loop: specialised agents call narrowly scoped tools and the supervisor coordinates durable workflow steps. Do not use it only to decorate a hard-coded script. |
| **Amazon Bedrock AgentCore** | Deploy the worker/agent to AgentCore Runtime and enable Observability if account access permits. This is strongly recommended, not a blocker; document the fallback ECS/Lambda path. |
| **Amazon DynamoDB** | Durable workflow state, entities, idempotency keys, reservations, decisions, and event timeline. Use conditional writes/transactions; no full-table scans on hot paths. |
| **Amazon EventBridge + SQS + DLQ** | Event-driven background work and retry-safe delivery of `SURPLUS_REPORTED`, `RIDER_UNAVAILABLE`, `CAPACITY_CHANGED`, and `DEADLINE_RISK` events. |
| **AWS Lambda or ECS Fargate/App Runner** | Public API and asynchronous worker runtime. Choose one deployment model and fully wire it; do not leave multiple incomplete options. |
| **Amazon S3 + KMS** | Evidence uploads (temperature/photo/packing checklist only where consented), immutable demo artefacts, and lifecycle archive. Use pre-signed uploads and retention rules. |
| **Amazon Location Service** | Production route and ETA calculation. A deterministic geospatial fallback is permitted only in explicit local/demo mode and must be labelled. |
| **Amazon Cognito** | Authentication and organisation/role claims for donor, NGO, rider, operator, and administrator. |
| **Secrets Manager / Parameter Store** | Webhook secrets, notification credentials, and environment configuration; never source-control secrets. |
| **CloudWatch + X-Ray/AgentCore Observability** | Logs, workflow correlation IDs, dashboards, alarms, and trace links from UI decisions to tool calls. |
| **SNS / WhatsApp Cloud API** | Confirmations, assignment requests, reminders, escalation notifications. In demo mode, use a visible in-app notification adapter implementing the same interface. |

## 5. Domain Model and State Contracts

### Required entities

- [ ] `Organisation` (donor, recipient, logistics provider), `User`, `Location`, `FoodBatch`, `SurplusEvent`, `RecipientCapacity`, `Rider`, `RiderReservation`, `AllocationPlan`, `AllocationLeg`, `Workflow`, `Decision`, `Evidence`, `Notification`, `TrustSnapshot`, `Forecast`, and immutable `DomainEvent`.
- [ ] Store `workflow_id`, `correlation_id`, actor, version, timestamps, source, and idempotency key on every changing record.
- [ ] Represent food batches separately from events so one event can contain vegetarian/non-vegetarian, allergen, packaging, temperature, and different safe-window items.
- [ ] Support allocation splitting, bundling compatible batches, cancellation, expiry, partial delivery, rejection, and re-plan lineage.

### Valid lifecycle

```text
REPORTED → NEEDS_CLARIFICATION | VERIFIED → CANDIDATES_READY
→ PROPOSED → SAFETY_PASS | SAFETY_REVIEW | SAFETY_BLOCK
→ RESERVED → ASSIGNED → ACCEPTED → PICKED_UP → IN_TRANSIT
→ DELIVERED | FAILED | CANCELLED | EXPIRED
```

- [ ] Validate every transition centrally; reject invalid transitions with structured error codes.
- [ ] Enforce idempotent ingestion and atomic rider/capacity reservation using DynamoDB conditional writes or transactions.
- [ ] Ensure the API returns a workflow ID immediately; agent work continues asynchronously and UI receives state updates through SSE/WebSocket or bounded polling fallback.

## 6. Agent and Safety Design

### Agent boundaries and tools

| Agent | May decide | May call | Must not do |
| --- | --- | --- | --- |
| Signal | extract event fields, detect ambiguity | create draft, request clarification, attach evidence | allocate or execute deliveries |
| Forecast | likelihood and expected demand/surplus | query historical aggregates, create forecast/preparation | claim observed facts or reserve a rider |
| Demand | recipient suitability | query live capacity/preferences/hours | override a recipient’s policy |
| Allocation | choose among safe candidate combinations | generate candidate plans, rank transparent score | commit without AnnaGuard and reservations |
| Logistics | routing and feasible riders | search/reserve/release rider, calculate ETA | override food safety |
| Trust | explain reliability signal | query outcome history, write snapshot | generate a punitive opaque eligibility decision |
| Supervisor | orchestrate durable steps and exceptions | enqueue tasks, invoke specialised agents, request human decision | bypass deterministic policies or directly mutate state outside approved tools |

### AnnaGuard: deterministic control plane

- [ ] Implement pure, unit-tested policy functions returning `PASS`, `REVIEW`, or `BLOCK` plus machine-readable reasons.
- [ ] Block for expired/unknown food timing, exceeded safe travel window, insufficient capacity, incompatible food/recipient constraints, closed recipient hours, unavailable/unreserved rider, invalid evidence, or missing mandatory data.
- [ ] Use `REVIEW` for policy-configured uncertainty that requires operator confirmation; never silently convert uncertainty into a pass.
- [ ] Calculate safe delivery margin from preparation time, food-specific limit, pickup time, route ETA, handling buffer, and evidence confidence.
- [ ] Record policy version, inputs, decision, and reasons with every plan; execute only after a backend-enforced `PASS`.
- [ ] Treat LLM output strictly as untrusted input. It cannot supply authoritative safety scores, ETA, capacity, or status transitions.

### Structured agent execution

- [ ] Use Pydantic request/response schemas for all tools and JSON/schema-constrained model outputs.
- [ ] Log tool name, redacted arguments, result, latency, model ID, prompt version, token/cost telemetry, and workflow/correlation ID.
- [ ] Add timeout, retry/backoff, circuit breaker, and explicit human escalation for model, routing, notification, and persistence failures.
- [ ] Defend against prompt injection: separate user content from tool instructions; allowlist tools; validate all generated values; do not expose credentials or raw operational records to the model.

## 7. Functional Build Checklist

### P0 — working vertical slice

- [ ] Replace the current hard-coded supervisor path with a durable event-driven workflow service.
- [ ] Parse free text into `SurplusDraft`; if quantity, food category, preparation/expiry time, pickup deadline, location, or evidence is insufficient, create `NEEDS_CLARIFICATION` and ask the donor only for the missing fields.
- [ ] Provide structured reporting as an accessible fallback and ensure it invokes exactly the same API/workflow as WhatsApp/webhook intake.
- [ ] Generate candidates across multiple eligible recipients and riders; optimise safety margin first, then delivered quantity, recipient fit, ETA, and transparent trust signals.
- [ ] Add atomic rider and recipient-capacity reservations, expiry of reservations, release on failure, and re-plan triggers.
- [ ] Persist all plan fields required by the API schema: quantity, legs, ETA, rescue score components, safety result, evidence, status, and rationale.
- [ ] Implement an actual status endpoint for rider acceptance, pickup, in-transit, delivery proof, failure, cancellation, and NGO rejection.

### P0 — realistic deterministic scenarios

- [ ] **45 meals, 42 minutes, one failed rider:** initial safe plan; cancellation event; old reservation released; alternative ETA computed; AnnaGuard re-check; replacement executes; final scorecard shows 45 delivered, one failure recovered, zero violations.
- [ ] **Safety agent says no:** 30 meals, 25-minute remaining window, 38-minute best ETA; deterministic `BLOCK`; no reservation/notification marked as an execution; show reason and either alternatives or an operator action.
- [ ] **Predict before food exists:** historical pattern produces a forecast and pre-checks capacity/rider availability; real reported surplus consumes a prepared plan and compares response time against unprepared baseline.
- [ ] **Split allocation:** one batch is safely split only between compatible recipients with available capacity and separate safe delivery legs.
- [ ] **Capacity/rejection disruption:** a recipient rejects or reduces capacity; impacted allocation re-plans without duplicating food or riders.

### P1 — human-centred product experience

- [ ] Replace the card-list “map” with a geographic view showing coarse/consented locations, route legs, pickup deadlines, status, and safety margin.
- [ ] Add operational views: live queue, surplus detail, plan detail, re-plan comparison, delivery tracking, decision inbox, partner/rider management, and outcome analytics.
- [ ] Give a human operator one-click, auditable choices for `REVIEW`: approve, reject, choose tied recipient, request clarification, or mark evidence invalid.
- [ ] Present explanations in plain language: what happened, why a plan is safe, what changed, what the system did automatically, and what decision remains.
- [ ] Add form validation, loading/error/offline/retry states, mobile layout, keyboard navigation, semantic labels, color-independent statuses, and WCAG-aware contrast.
- [ ] Use environment-driven API URLs, typed clients, and no `any`, hard-coded localhost URLs, fixed metrics, or mojibake icons.

## 8. API, Security, and Privacy

- [ ] Version REST endpoints; generate OpenAPI documentation and typed frontend clients.
- [ ] Provide APIs for intake, surplus list/detail, recipients, riders, workflow/plan detail, re-plan, status update, decision queue/action, metrics, forecasts, and health/readiness.
- [ ] Verify WhatsApp/webhook challenge and HMAC signature; rate-limit endpoints; apply request-size limits, field validation, and idempotency keys.
- [ ] Configure CORS for the deployed frontend only—never `*` together with credentials.
- [ ] Protect endpoints with Cognito JWTs and organisation/role checks. Enforce permissions again in tools, not only in UI.
- [ ] Encrypt data at rest/in transit, use KMS where applicable, redaction in logs, pre-signed evidence uploads, audit records, retention rules, and account deletion/export procedures.
- [ ] Document food-safety limitation clearly: AnnaSetu coordinates based on policy and entered/verified evidence; it is not a replacement for local food-safety regulations or professional inspection.

## 9. Deployment, Reliability, and Cost

### Infrastructure as code

- [ ] Fix and extend the CDK app to provision the selected API/worker deployment, DynamoDB tables/indexes, EventBridge rules, SQS queues/DLQs, S3/KMS, CloudFront, Cognito, IAM roles, CloudWatch resources, Secrets Manager references, and explicit stack outputs.
- [ ] Use environment-specific configuration for `dev`, `staging`, and `prod`; unique resource names; tags; production retention; backups/PITR; no `DESTROY`/auto-delete behaviour in production.
- [ ] Grant each compute role only required actions and resource ARNs; separate web, workflow, notification, and admin permissions.
- [ ] Deploy from CI using a scoped OIDC role, not long-lived access keys.

### Operational requirements

- [ ] Readiness endpoint checks database/event queue/model configuration without leaking secrets.
- [ ] Set DLQ alarms, workflow age alarms, error-rate alarms, failed-notification alarms, and safety-block/replan dashboards.
- [ ] Add replay-safe event handling, exponential retries, poison-message inspection, and a documented recovery runbook.
- [ ] Provide budget guardrails, expected monthly demo cost, Bedrock token caps, log retention, TTL/archive lifecycle, and a teardown command for development stacks.

## 10. Test and Release Gates

- [ ] Python: pinned dependencies (`pyproject.toml` or locked requirements), formatter/linter/type checker, pytest, test database/mock adapters, and no missing test dependencies.
- [ ] Frontend: production build, lint, unit/component tests, accessibility checks, typed API contracts, and visual smoke test.
- [ ] Infrastructure: CDK synth plus meaningful assertions for all resources, encryption, IAM boundaries, queues, and production retention.
- [ ] Unit-test policy boundaries: expired food, unknown evidence, ETA threshold, capacity, hours, compatibility, reservation conflict, and every state transition.
- [ ] Integration-test Strands tools with recorded/mock Bedrock responses and verify that unsafe output cannot execute a plan.
- [ ] End-to-end test all five demo scenarios and assert final stored facts, not just timeline text.
- [ ] Add load/concurrency tests for duplicate webhooks, two workflows contending for the same rider/capacity, and retries.
- [ ] CI gate: install → lint → typecheck → unit → integration → frontend build → CDK synth/assertions → security/dependency scan → deployment smoke test.

## 11. Submission Package

- [ ] Public GitHub repository; MIT or Apache-2.0 `LICENSE`; license shown in repository About; no secrets or private/PII data.
- [ ] Root README with: problem, target users, real workflow, local run, deployment, environment variables, AWS services, AgentCore status, safety model, data provenance, test commands, cost/cleanup, limitations, and demo scenarios.
- [ ] Architecture diagram showing user interface, Strands model → tool → reasoning loop, tools/integrations, each AWS service, storage, security boundary, and outputs.
- [ ] Public live demo URL with a labelled, resettable demo tenant and no privileged credentials required by a judge.
- [ ] Five-minute video: 0:00 problem/audience; 0:30 architecture; 1:00 live normal rescue; 2:00 rider failure and automatic recovery; 3:00 deterministic safety block; 3:40 prediction/pre-positioning; 4:20 metrics, impact, and responsible limits; 4:45 repository/live URL call to action.
- [ ] Devpost description explaining what AnnaSetu does, who it is for, why it matters, AWS/Strands implementation, architecture link, repository, live URL, video, and AWS Builder ID.
- [ ] Publish an AWS Builder Center build-story post titled with “Agents for Humans” before the deadline for bonus points.
- [ ] Disclose starter templates, open-source libraries, generated assets, and any pre-existing work as required by the hackathon rules.

## 12. Execution Order and Exit Criteria

### Phase 1 — correctness before visuals

1. Repair build/test baseline and introduce typed domain contracts.
2. Implement persistent workflow/state machine, idempotency, reservations, and AnnaGuard.
3. Implement the Strands tool loop with Bedrock and tool/audit telemetry.

**Exit:** all P0 policy, lifecycle, and workflow tests pass; no execution bypass exists.

### Phase 2 — autonomous operational proof

4. Implement routing adapter, notification adapter, disruption events, re-planning, and realistic seeded pilot data.
5. Implement all deterministic scenarios through the same production workflow.
6. Build the decision ledger and metrics pipeline.

**Exit:** the five scenarios pass end-to-end and report stored, verifiable outcomes.

### Phase 3 — judge-ready product and AWS deployment

7. Build `/demo`, operational map, plan/re-plan detail, human decision inbox, and accessible responsive UI.
8. Provision and deploy AWS infrastructure; connect Bedrock, AgentCore where available, observability, auth, and CI/CD.
9. Conduct reliability, security, and browser smoke tests from a clean account.

**Exit:** public URL works, traces link a UI action to real Strands tools, and a judge can complete the guided demo unaided.

### Phase 4 — submission hardening

10. Write README, runbook, architecture diagram, cost/cleanup guide, and evidence/data documentation.
11. Record the working five-minute video only after a clean deployed rehearsal.
12. Complete Devpost fields, Builder ID, public-repo/license checks, disclosure, and optional Builder Center post.

**Exit:** every item in Section 1 and Section 11 is checked, all CI checks are green, and the demo has been run twice from reset state.

## 13. Explicit Anti-Patterns to Remove

- [ ] Do not present scripted timeline text as autonomous execution.
- [ ] Do not hard-code quantity, safety window, rider, NGO, ETA, forecast, trust score, or impact metric.
- [ ] Do not rely on an LLM string such as “REJECT” for safety or workflow control.
- [ ] Do not ship a non-functional map, placeholder tests, open CORS, no-auth operations, unverified webhooks, or local-only API URLs.
- [ ] Do not call arbitrary in-memory fixtures “DynamoDB persistence” or arbitrary records “real data.”
- [ ] Do not promise integrations that are not implemented; clearly label local/demo adapters and production adapters.

## Current Baseline Gaps (13 September 2026)

- [ ] Frontend production build is failing because `NetworkState` omits `plans` and `surplus` used by `App.tsx`.
- [ ] Backend repository tests do not run in the current environment because test dependencies are incomplete; existing infrastructure Jest test is only a placeholder.
- [ ] Current mock pipeline ignores donor text and hard-codes donation facts; simulation endpoints write timeline messages rather than mutate/re-plan real workflow state.
- [ ] Current live-agent path does not make the supervisor an effective orchestrator; planned allocations are not durably committed before ad-hoc execution logic.
- [ ] Current `Plan` persistence does not satisfy the declared plan model, and safety covers ETA only.
- [ ] Current infrastructure provisions only DynamoDB and S3; no deployable API, compute, queueing, auth, Bedrock/AgentCore policy, or observability exists.
- [ ] There is no root README, public submission package, meaningful test suite, CI/CD workflow, or full deployment/runbook path yet.
