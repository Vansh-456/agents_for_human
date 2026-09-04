# BUILD PROMPT — ANNASETU
## Autonomous, Evidence-Aware Food Rescue Network
### AWS Agents for Humans Hackathon — Good Neighbor Agents

Build a production-quality full-stack prototype called **AnnaSetu**, an autonomous food-rescue coordination network.

The system connects:

**Food Vendors → AnnaSetu Agent Network → NGOs / Shelters / Community Kitchens**

and coordinates:

**Detection → Verification → Demand Matching → Allocation → Logistics → Safety Validation → Execution → Monitoring → Feedback**

The application must demonstrate genuine **agentic behavior using the Strands Agents SDK**, AWS-native architecture, human escalation, deterministic safety controls, evidence-based freshness verification, and a closed-loop operational workflow.

Do NOT build this as a simple CRUD food-donation marketplace.

The central architectural principle is:

> **Agents reason and plan. Deterministic systems enforce safety and constraints. Tools execute real actions. Humans intervene only when the system encounters genuine uncertainty or an irreversible decision.**

---

# 1. PRIMARY PRODUCT OBJECTIVE

AnnaSetu solves the coordination problem surrounding perishable surplus food.

A vendor should be able to send a simple natural-language message such as:

> "50 veg meals ready, prepared 20 minutes ago, pickup within 40 minutes."

AnnaSetu should autonomously:

1. Parse the message.
2. Create a structured surplus event.
3. Verify the credibility of the freshness claim.
4. Identify suitable recipients.
5. Determine their current capacity and urgency.
6. Generate multiple allocation plans.
7. Find feasible logistics.
8. Calculate whether the food can safely reach recipients.
9. Apply deterministic food-safety constraints.
10. Select the best valid plan.
11. Execute the workflow.
12. Notify vendor, rider and recipient.
13. Monitor execution.
14. Re-plan if something fails.
15. Record the outcome.
16. Update trust, memory and future predictions.

The system must visibly demonstrate this workflow in the UI.

---

# 2. HIGH-LEVEL ARCHITECTURE

Implement the following logical architecture:

```text
                         HUMAN / REAL WORLD
                               |
              +----------------+----------------+
              |                |                |
           Vendors            NGOs            Riders
              |                |                |
              +-------- WhatsApp / Web --------+
                               |
                               v
                    +----------------------+
                    | API / EVENT LAYER    |
                    | API Gateway / Lambda |
                    +----------+-----------+
                               |
                               v
                 +--------------------------+
                 | STRANDS AGENT NETWORK    |
                 |                          |
                 |       SUPERVISOR         |
                 |           |              |
                 |   +-------+-------+      |
                 |   |       |       |      |
                 | Signal Demand Forecast   |
                 |           |              |
                 |        Allocation        |
                 |       /    |    \        |
                 |   Safety Logistics Trust |
                 +-----------+--------------+
                             |
                             v
                  +-------------------------+
                  | ANNAPROOF               |
                  | Evidence Verification   |
                  +-----------+-------------+
                              |
                              v
                  +-------------------------+
                  | ANNAGUARD               |
                  | Deterministic Safety    |
                  | & Policy Control Plane   |
                  +-----------+-------------+
                              |
                     +--------+--------+
                     |        |        |
                    PASS    REVIEW    BLOCK
                     |        |        |
                     v        v        v
                  EXECUTE   HUMAN    REJECT
                     |
                     v
               REAL-WORLD ACTION
                     |
                     v
                  OUTCOME
                     |
                     v
            FEEDBACK / MEMORY / TRUST
                     |
                     +---------> NEXT DECISION
```

Preserve this conceptual separation in the implementation.

---

# 3. FRONTEND

Build a polished React + TypeScript dashboard.

Use a professional civic-tech / logistics aesthetic.

The interface should feel like a **live autonomous operations center**, not a generic admin dashboard.

Include the following major pages:

## A. Operations Dashboard

Display:

- Active surplus
- Meals currently available
- Meals successfully rescued today
- Donations at risk
- Active pickups
- Active deliveries
- Pending human decisions
- Safety blocks
- Average rescue time
- Rescue success rate

Include a live map showing:

- vendors
- NGOs
- riders
- active routes
- surplus locations
- recipient locations
- critical donations

---

# 4. LIVE AGENT TIMELINE

Every active rescue workflow must expose an agent timeline.

Example:

```text
21:04:12  SURPLUS_RECEIVED
21:04:13  SIGNAL_AGENT parsed vendor message
21:04:14  ANNAPROOF evaluating freshness evidence
21:04:15  DEMAND_AGENT found 7 recipient candidates
21:04:16  ALLOCATION_AGENT generated 3 plans
21:04:17  LOGISTICS_AGENT calculated ETAs
21:04:18  ANNAGUARD rejected Plan A
21:04:19  ALLOCATION_AGENT generated Plan B
21:04:20  SAFETY_GATE approved Plan B
21:04:21  RIDER_ASSIGNED
21:04:23  NGO_NOTIFIED
```

Each event should show:

- timestamp
- agent
- action
- tool used
- result
- confidence / risk where relevant

This is critical for the hackathon demo.

---

# 5. SURPLUS CREATION

Create a vendor interface with two modes.

## Mode 1 — Natural Language

Text input:

```text
"45 vegetarian meals ready.
Prepared 25 minutes ago.
Need pickup within 45 minutes."
```

Send this to the Signal Agent.

## Mode 2 — Structured Simulation

Fields:

- Vendor
- Food category
- Quantity
- Claimed preparation time
- Storage condition
- Temperature status
- Pickup deadline
- Location

This allows judges to easily create demo scenarios.

---

# 6. STRANDS AGENT ARCHITECTURE

Implement agents as separate modules/classes.

Do not implement everything inside one agent.

Use the **Strands Agents SDK** for agent creation, tool calling and orchestration.

Recommended modules:

```text
agents/
    supervisor_agent
    signal_agent
    forecast_agent
    demand_agent
    allocation_agent
    logistics_agent
    safety_agent
    trust_agent
```

Each agent must have:

- explicit system instructions
- narrowly scoped tools
- structured outputs
- clear responsibilities
- no unnecessary access to unrelated tools

---

# 7. SUPERVISOR AGENT

The Supervisor is responsible for orchestration.

Responsibilities:

- understand current workflow state
- delegate tasks
- collect agent outputs
- identify conflicts
- trigger replanning
- decide when human escalation is required
- initiate execution after safety validation

The Supervisor must NOT directly override AnnaGuard.

Never allow:

```text
Supervisor -> Execute
```

without passing through the safety control plane.

The correct flow is:

```text
Supervisor
    ↓
Proposed Plan
    ↓
AnnaProof
    ↓
AnnaGuard
    ↓
PASS / REVIEW / BLOCK
    ↓
Execution
```

---

# 8. SIGNAL AGENT

Purpose:

Convert unstructured human messages into structured events.

Example:

Input:

```text
"50 veg meals ready, made 20 mins ago.
Can someone pick them up?"
```

Output:

```json
{
  "quantity": 50,
  "food_category": "vegetarian_meals",
  "claimed_preparation_time": "...",
  "pickup_deadline": "...",
  "source": "...",
  "confidence": 0.94
}
```

The Signal Agent must identify missing information.

If critical information is missing, it should request clarification rather than hallucinate.

---

# 9. FORECAST AGENT

Predict:

- expected vendor surplus
- likely surplus time
- expected quantity
- recipient demand
- recurring patterns

Example:

```text
Restaurant A historically produces:
15–25 surplus meals
between 9:00–10:00 PM.

Predicted surplus tonight:
~20 meals.
```

For MVP, use historical mock data and lightweight statistical logic.

Do not pretend that the prediction model is production-grade.

Clearly distinguish:

```text
Observed data
Predicted data
Simulated data
```

---

# 10. DEMAND AGENT

Determine suitable recipient organizations.

Evaluate:

- current capacity
- food requirements
- dietary compatibility
- urgency
- operating hours
- distance
- historical acceptance
- reliability

Example:

```text
NGO A
Capacity: 30
Distance: 2.4 km
Urgency: HIGH
Reliability: 96

NGO B
Capacity: 50
Distance: 6.8 km
Urgency: MEDIUM
Reliability: 91
```

Return ranked candidates with explanations.

---

# 11. ALLOCATION AGENT

This is the core optimization agent.

It must generate multiple possible plans.

Example:

```text
Plan A
NGO A → 30
NGO B → 20

Plan B
NGO B → 50

Plan C
NGO A → 20
NGO C → 30
```

Score plans using configurable weighted factors:

```text
recipient need
quantity rescued
distance
ETA
participant reliability
transport availability
spoilage risk
operational constraints
```

Do not simply select the nearest recipient.

The goal is:

> **maximize safely rescued food under real-world constraints.**

---

# 12. LOGISTICS AGENT

Responsibilities:

- find available riders
- calculate route distance
- calculate ETA
- evaluate transport feasibility
- reserve a rider
- release a rider
- detect logistics failure
- trigger re-planning

Expose tools such as:

```text
find_available_riders()
calculate_eta()
calculate_distance()
reserve_rider()
release_rider()
track_delivery()
```

Use Amazon Location Service where feasible.

For local/demo mode, provide deterministic simulated routing fallback.

---

# 13. TRUST AGENT

Maintain operational reliability scores.

Track:

### Vendor

- accurate quantity reports
- successful donations
- cancellations
- preparation consistency

### NGO

- accepted donations
- rejected donations
- pickup readiness
- confirmation reliability

### Rider

- successful pickups
- cancellations
- lateness
- delivery completion

Example:

```text
Vendor A
Trust: 93

NGO B
Trust: 96

Rider C
Trust: 88
```

IMPORTANT:

Trust must never be treated as proof of food safety.

It should influence:

- candidate ranking
- verification intensity
- operational confidence

but never override AnnaGuard.

---

# 14. ANNAPROOF — EVIDENCE VERIFICATION LAYER

This is a core novelty.

AnnaProof exists because vendors can provide false freshness information.

Example malicious input:

```text
"Food prepared 5 minutes ago."
```

AnnaProof must NOT blindly trust it.

Evaluate evidence from multiple sources.

Possible evidence:

```text
vendor claim
system message timestamp
event creation time
historical behavior
quantity anomaly
POS/kitchen record if available
storage information
temperature evidence if available
```

Represent evidence explicitly:

```json
{
  "claim": "prepared 5 minutes ago",
  "evidence": [
    {
      "type": "system_timestamp",
      "value": "...",
      "reliability": "high"
    },
    {
      "type": "vendor_claim",
      "value": "...",
      "reliability": "low"
    }
  ],
  "consistency": "LOW"
}
```

The system should identify contradictions.

Example:

```text
Vendor claims:
Prepared 5 minutes ago

System:
Donation first reported 47 minutes ago

Result:
ANOMALY DETECTED
```

Do not claim that AI or a photograph can scientifically prove food safety.

Treat them as supporting evidence only.

---

# 15. ANNA GUARD — DETERMINISTIC SAFETY CONTROL PLANE

AnnaGuard must be implemented primarily as deterministic business logic, NOT as an LLM decision.

Its responsibility is:

> Prevent unsafe or insufficiently verified food from entering execution.

Inputs:

```text
food state
preparation evidence
storage evidence
remaining safe window
transport ETA
safety buffer
food category
operational constraints
verification status
```

The exact safety rules must be configurable and based on authoritative food-safety guidance for the intended deployment jurisdiction.

Never invent universal safety limits.

---

# 16. SAFETY DECISION

AnnaGuard must return exactly one of:

```text
PASS
REVIEW
BLOCK
```

### PASS

All mandatory constraints satisfied.

### REVIEW

Evidence or circumstances are ambiguous.

Human intervention required.

### BLOCK

Safety conditions cannot be satisfied.

No agent can override BLOCK.

---

# 17. FRESHNESS MODEL

Do not represent freshness as only:

```text
expiry_time
```

Represent a food batch as:

```text
Food Batch
    |
    +-- preparation evidence
    +-- storage evidence
    +-- handling history
    +-- temperature evidence
    +-- current timestamp
    +-- transport ETA
    +-- confidence
    +-- safety status
```

Maintain a dynamic freshness state:

```text
SAFE
URGENT
CRITICAL
REVIEW
BLOCKED
```

The exact state transitions must be configurable.

---

# 18. SAFETY BUFFER

Never use:

```text
ETA < remaining_safe_time
```

as the only criterion.

Use a safety margin:

```text
remaining_safe_window
>
pickup_time
+
transport_time
+
uncertainty_buffer
```

If this condition fails:

```text
BLOCK / REPLAN
```

The uncertainty buffer should increase when evidence quality is poor.

---

# 19. STALE FOOD MANAGEMENT

When a batch becomes unsafe:

```text
FOOD_UNSAFE
      ↓
Cancel allocation
      ↓
Stop transport
      ↓
Notify stakeholders
      ↓
Record disposition
```

Possible disposition states:

```text
DELIVERED
CONSUMED
BLOCKED
DISPOSED
OTHER_APPROVED_DISPOSITION
```

Do not simply delete stale food from the database.

Maintain an audit trail.

---

# 20. EVENT-DRIVEN ARCHITECTURE

Represent major lifecycle transitions as events.

Example:

```text
SURPLUS_CREATED
MATCH_REQUESTED
CANDIDATES_FOUND
PLAN_GENERATED
PLAN_REJECTED
PLAN_APPROVED
RIDER_ASSIGNED
PICKUP_STARTED
PICKUP_COMPLETED
DELIVERY_STARTED
DELIVERY_COMPLETED
DELIVERY_FAILED
FOOD_AT_RISK
FOOD_UNSAFE
HUMAN_ESCALATION
```

Use EventBridge where feasible.

Events should trigger:

- agent workflows
- monitoring
- replanning
- freshness checks
- notifications
- trust updates

---

# 21. FAILURE AND REPLANNING

AnnaSetu must not stop when the first plan fails.

Example:

```text
Plan A
    ↓
Rider cancels
    ↓
DELIVERY_FAILED
    ↓
Supervisor
    ↓
Logistics Agent
    ↓
Find alternative riders
    ↓
Allocation Agent re-evaluates
    ↓
AnnaGuard
    ↓
New Plan
    ↓
Execute
```

This should be visibly demonstrated.

---

# 22. HUMAN ESCALATION

Humans should NOT approve every donation.

Escalate only for genuine ambiguity.

Examples:

```text
conflicting freshness evidence
unknown storage conditions
no safe transport option
two equally viable allocation plans
unusual high-volume donation
policy exception
```

Show a Human Decision Queue:

```text
PENDING DECISION

Donation F1023

Reason:
Preparation timestamp conflicts with
system event history.

Risk:
HIGH

Recommended action:
Request verification

[REQUEST EVIDENCE]
[BLOCK]
[APPROVE WITH JUSTIFICATION]
```

Human decisions must be logged.

---

# 23. AWS ARCHITECTURE

Use AWS-native components where practical.

Recommended architecture:

```text
Frontend
   ↓
API Gateway
   ↓
Lambda / backend
   ↓
Strands Agents
   ↓
Amazon Bedrock
   ↓
AgentCore
   ↓
Tools
   ↓
AWS services
```

Use:

### Amazon Bedrock
For foundation-model reasoning.

### Strands Agents SDK
For agent implementation/orchestration.

### Amazon Bedrock AgentCore
Use where supported for agent runtime, memory, gateway/tool integration, identity and observability capabilities.

### DynamoDB
Operational state:

```text
vendors
ngos
riders
surplus
food_batches
allocations
deliveries
trust_scores
events
human_decisions
```

### S3
Store:

- historical datasets
- simulation artifacts
- reports
- optional evidence files

### Amazon Location Service
Distance, routes and ETA.

### EventBridge
Event-driven orchestration.

### Lambda
Serverless backend functions and lightweight tool execution.

### API Gateway
External API and WhatsApp webhook entry point.

### CloudWatch
Logs, metrics and observability.

### IAM
Least-privilege permissions.

### Secrets Manager
API credentials and secrets.

---

# 24. WHATSAPP INTEGRATION

Design the system so WhatsApp Cloud API can act as the primary human interface.

Webhook:

```text
WhatsApp
   ↓
API Gateway
   ↓
Lambda
   ↓
Signal Agent
```

Outgoing:

```text
Agent
   ↓
Notification Tool
   ↓
WhatsApp Cloud API
   ↓
Vendor / NGO / Rider
```

If actual WhatsApp credentials are unavailable during development, implement a fully functional **WhatsApp Simulator** in the UI.

The simulator should look like a real conversation and trigger exactly the same backend workflow.

Do not create a fake architecture where WhatsApp is merely decorative.

---

# 25. TOOL ARCHITECTURE

Create explicit tools.

Example:

```text
surplus_tools
    create_surplus()
    update_surplus()
    get_surplus()
    get_surplus_history()

demand_tools
    get_ngo_capacity()
    get_ngo_preferences()
    get_current_demand()

allocation_tools
    generate_candidate_plans()
    score_plan()
    split_donation()
    bundle_donations()

logistics_tools
    find_riders()
    calculate_eta()
    calculate_distance()
    reserve_rider()
    release_rider()

safety_tools
    get_freshness_state()
    get_safety_evidence()
    run_safety_gate()

trust_tools
    get_trust_score()
    record_outcome()
    update_trust()

notification_tools
    notify_vendor()
    notify_ngo()
    notify_rider()
    escalate_human()

tracking_tools
    update_delivery()
    get_delivery_status()
```

Agents should call tools instead of directly manipulating database state whenever practical.

---

# 26. DATA MODEL

Create clear entities.

## Vendor

```text
id
name
location
operating_hours
trust_score
historical_surplus
verification_level
```

## NGO

```text
id
name
location
capacity
food_preferences
urgency
operating_hours
trust_score
```

## Rider

```text
id
name
location
availability
vehicle_type
trust_score
```

## Food Batch

```text
id
vendor_id
food_category
quantity
claimed_preparation_time
system_reported_time
storage_condition
temperature_status
evidence_score
freshness_state
safe_window
status
```

## Allocation

```text
id
food_batch_id
recipient_id
quantity
rider_id
eta
safety_status
allocation_score
status
```

## Event

```text
id
type
timestamp
actor
entity_id
metadata
```

---

# 27. AGENT MEMORY

Use AgentCore Memory where available.

Store useful operational context such as:

```text
vendor behavior
recipient preferences
recurring surplus patterns
successful logistics patterns
previous escalation decisions
```

Do not use memory as a replacement for authoritative current state.

The distinction is:

```text
DynamoDB
=
What is happening now?

Memory
=
What has the system learned from previous interactions?
```

---

# 28. SECURITY

Implement least-privilege access.

Example:

```text
Signal Agent
→ message/event access

Demand Agent
→ recipient data

Logistics Agent
→ routing/rider data

Safety Agent
→ food safety state

Supervisor
→ orchestration

Notification Tool
→ outbound communication
```

No agent should automatically receive unrestricted access to the entire database.

Protect secrets with environment variables / Secrets Manager.

Never expose credentials in frontend code.

---

# 29. OBSERVABILITY

The dashboard must expose:

```text
Agent
Task
Tool
Latency
Result
Error
Decision
```

Example:

```text
ALLOCATION_AGENT
├── get_ngo_capacity()
├── get_current_demand()
├── generate_candidate_plans()
└── score_plan()

SAFETY_AGENT
├── get_safety_evidence()
├── calculate_remaining_window()
└── run_safety_gate()
```

Include a workflow trace view.

This is important for demonstrating actual agent behavior.

---

# 30. SIMULATION MODE

Create a deterministic simulation environment so the complete system can be demonstrated without external dependencies.

Include scenarios:

### Scenario A — Successful Rescue

```text
50 meals
freshness verified
recipient available
rider available
→ successful delivery
```

### Scenario B — Fake Freshness Claim

```text
Vendor:
"prepared 5 minutes ago"

System evidence:
first report 47 minutes ago

→ anomaly
→ AnnaProof LOW confidence
→ AnnaGuard REVIEW/BLOCK
```

### Scenario C — Food Approaching Safety Limit

```text
remaining safe window
↓
URGENT
↓
Allocation Agent prioritizes fastest feasible recipient
```

### Scenario D — Rider Cancellation

```text
Rider A cancels
↓
EventBridge
↓
Supervisor
↓
Logistics Agent
↓
Rider B
↓
AnnaGuard
↓
delivery
```

### Scenario E — No Safe Recipient

```text
No recipient can receive food
before the applicable safety limit.

→ BLOCK
→ notify vendor/coordinator
→ record disposition
```

---

# 31. CRITICAL DEMO SCENARIO

The main demo should be approximately:

```text
Vendor sends WhatsApp message
        ↓
Signal Agent extracts data
        ↓
AnnaProof verifies claim
        ↓
Demand Agent finds recipients
        ↓
Allocation Agent creates 3 plans
        ↓
Logistics Agent calculates ETAs
        ↓
AnnaGuard validates plans
        ↓
Best valid plan selected
        ↓
Rider assigned
        ↓
NGO notified
        ↓
Delivery succeeds
        ↓
Trust + memory updated
```

Then immediately demonstrate the adversarial scenario:

```text
Vendor lies about preparation time
        ↓
AnnaProof detects contradiction
        ↓
AnnaGuard blocks automatic distribution
        ↓
Human receives only the necessary escalation
```

This should be the emotional/technical highlight of the demo.

---

# 32. UI PAGES

Create:

```text
/
    Landing / Mission

/dashboard
    Operations center

/donations
    Food batches

/donations/:id
    Food provenance + freshness timeline

/network
    Vendor / NGO / rider network map

/agents
    Agent activity

/workflows/:id
    Full agent trace

/decisions
    Human escalation queue

/simulation
    Hackathon demo scenarios

/analytics
    Rescue statistics

/settings
    Safety policies / thresholds / system configuration
```

---

# 33. FOOD PROVENANCE UI

For every donation display:

```text
FOOD BATCH F1023

40 vegetarian meals

Claimed preparation:
21:05

First system report:
21:08

Evidence:
✓ system timestamp
✓ vendor history
✓ storage information
⚠ temperature evidence unavailable

Freshness confidence:
MEDIUM

AnnaGuard:
REVIEW
```

Make contradictions visually obvious.

---

# 34. SAFETY GATE UI

Display:

```text
ANNA GUARD

Food:
F1023

Remaining safe window:
32 min

Pickup ETA:
7 min

Transport ETA:
14 min

Uncertainty buffer:
6 min

Required:
7 + 14 + 6 = 27 min

Decision:
PASS
```

This makes the deterministic reasoning transparent.

---

# 35. ARCHITECTURAL PRINCIPLES

Do not violate these principles:

### Principle 1

LLMs do not directly determine food safety.

### Principle 2

Vendor claims are evidence, not truth.

### Principle 3

Trust scores never override safety.

### Principle 4

No execution bypasses AnnaGuard.

### Principle 5

Human escalation is the fallback for uncertainty.

### Principle 6

Every important action creates an event.

### Principle 7

Every completed workflow generates feedback.

### Principle 8

Agents use tools to perform actions.

### Principle 9

Current operational state is separate from learned memory.

### Principle 10

The system should fail safely.

---

# 36. REPOSITORY STRUCTURE

Use a clean monorepo structure:

```text
annasetu/
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── services/
│   │   └── types/
│
├── backend/
│   ├── agents/
│   │   ├── supervisor.py
│   │   ├── signal.py
│   │   ├── forecast.py
│   │   ├── demand.py
│   │   ├── allocation.py
│   │   ├── logistics.py
│   │   ├── safety.py
│   │   └── trust.py
│   │
│   ├── tools/
│   │   ├── surplus.py
│   │   ├── demand.py
│   │   ├── allocation.py
│   │   ├── logistics.py
│   │   ├── safety.py
│   │   ├── trust.py
│   │   └── notifications.py
│   │
│   ├── safety/
│   │   ├── anna_guard.py
│   │   ├── anna_proof.py
│   │   └── policies.py
│   │
│   ├── models/
│   ├── services/
│   ├── events/
│   └── api/
│
├── infrastructure/
│   ├── iam/
│   ├── dynamodb/
│   ├── lambda/
│   ├── eventbridge/
│   └── agentcore/
│
├── simulation/
│   ├── scenarios/
│   └── fixtures/
│
├── docs/
│   └── architecture.md
│
├── tests/
│
├── README.md
├── LICENSE
└── .env.example
```

---

# 37. IMPLEMENTATION PRIORITY

Build in this order.

## Phase 1 — Core workflow

```text
Signal
→ Demand
→ Allocation
→ Safety
→ Execution
```

## Phase 2 — Logistics

```text
riders
ETA
routing
replanning
```

## Phase 3 — AnnaProof

```text
evidence
timestamp contradictions
anomaly detection
```

## Phase 4 — Trust + Memory

```text
outcomes
trust updates
historical context
```

## Phase 5 — Forecasting

```text
predict surplus
predict demand
```

## Phase 6 — AWS production integration

```text
Bedrock
AgentCore
DynamoDB
EventBridge
Location
CloudWatch
IAM
```

## Phase 7 — Demo polish

```text
agent trace
map
freshness clock
safety gate
human escalation
simulation
```

---

# 38. FALLBACK REQUIREMENT

The application must remain demoable even if external AWS services are unavailable.

Create:

```text
DEMO_MODE=true
```

In demo mode:

- use deterministic mock data
- simulate WhatsApp
- simulate riders
- simulate location
- simulate delivery
- retain the same agent/tool interfaces
- clearly label simulated components

Do NOT fake successful external integrations.

The architecture should remain identical; only the tool implementation changes.

---

# 39. DESIGN REQUIREMENT

The UI should visually communicate:

**TIME**

because food is perishable.

**TRUST**

because vendor claims can be unreliable.

**SAFETY**

because unsafe food must never be distributed.

**AUTONOMY**

because agents should execute the workflow.

**HUMAN CONTROL**

because uncertain decisions require escalation.

Use live status indicators, timelines, maps, countdowns, agent traces and safety decisions.

Avoid excessive generic cards and meaningless charts.

---

# 40. SUCCESS CRITERIA

The final application is successful only if a judge can see:

1. A vendor creates surplus using natural language.
2. Signal Agent understands it.
3. AnnaProof evaluates the freshness claim.
4. Demand Agent identifies recipients.
5. Allocation Agent creates multiple plans.
6. Logistics Agent calculates feasible delivery.
7. AnnaGuard independently validates safety.
8. The system executes the valid plan.
9. Notifications are generated.
10. A failure triggers autonomous replanning.
11. A suspicious freshness claim triggers review/block.
12. Delivery outcome updates trust/memory.
13. The dashboard shows the complete agent trace.

The project must clearly demonstrate that this is an **agentic system performing real work**, rather than a chatbot generating recommendations.

---

# 41. FINAL PRODUCT PHILOSOPHY

Build AnnaSetu around this statement:

> **"AnnaSetu doesn't just find someone who wants surplus food. It autonomously determines whether the food can still be safely rescued, who should receive it, how it should get there, executes the rescue, and learns from what happened."**

The system should feel like:

**a real-time autonomous operating system for community food rescue.**

The most important architectural distinction is:

```text
LLM / AGENTS
    ↓
Reason
Plan
Delegate
Explain
Re-plan

ANNA PROOF
    ↓
Corroborate evidence
Detect contradictions
Assess confidence

ANNA GUARD
    ↓
Enforce deterministic safety
PASS / REVIEW / BLOCK

TOOLS / AWS
    ↓
Execute

REAL WORLD
    ↓
Observe outcome

MEMORY / TRUST / FORECAST
    ↓
Improve next decision
```

Do not collapse these layers into one generic AI service.

Implement the architecture so that the **agentic reasoning layer, evidence layer, deterministic safety layer, execution layer and feedback layer are visibly and technically separate**.