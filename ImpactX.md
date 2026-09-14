# AnnaSetu — The Autonomous Food Rescue Mesh

## MASTER BUILD PROMPT

Build a production-quality hackathon application called **AnnaSetu** for the **AWS Agents for Humans Hackathon**.

AnnaSetu is an autonomous, multi-agent food-rescue coordination network that connects restaurants, caterers, canteens, grocery stores, NGOs, shelters, food banks, and riders.

The core innovation is NOT simply matching surplus food to NGOs.

AnnaSetu must function as a **continuously operating autonomous coordination layer** that:

1. Detects and structures surplus-food events.
2. Predicts likely upcoming surplus and demand.
3. Maintains a live representation of available food, NGO capacity, riders, locations, trust, and deadlines.
4. Dynamically allocates food across multiple recipients.
5. Bundles or splits donations when beneficial.
6. Optimizes transportation.
7. Enforces deterministic food-safety constraints.
8. Continuously re-plans when the environment changes.
9. Executes real actions through tools.
10. Learns reliability patterns over time.
11. Escalates to humans ONLY when a genuine decision cannot safely be automated.

The application must clearly demonstrate that the agents **do real work**, rather than merely generate text.

The application should be designed specifically around the hackathon's three core expectations:

- Real-world usefulness.
- Genuine agentic behavior.
- Strong AWS/Strands implementation.

The target track is:

**Good Neighbor Agents**

because AnnaSetu coordinates multiple groups in a community rather than serving a single individual.

---

# 1. CORE PRODUCT VISION

## Product statement

AnnaSetu transforms unpredictable local food surplus into a continuously coordinated rescue network.

Traditional food donation systems react after surplus appears.

AnnaSetu should proactively prepare the network.

Instead of:

> "Restaurant has food → find NGO."

AnnaSetu should operate as:

> "Restaurant is likely to have surplus → predict it → prepare recipient capacity → anticipate transportation → receive actual surplus → optimize allocation → validate safety → execute pickup → monitor execution → re-plan if something changes."

The central optimization objective is:

> **Maximize the amount of safe food successfully delivered to people before its usable window expires.**

---

# 2. IMPORTANT PRODUCT PRINCIPLES

The implementation MUST follow these principles.

## Principle 1 — Agents must act

Agents should not merely return recommendations.

Agents must have tools that allow them to:

- create events
- update state
- search participants
- calculate ETA
- create allocations
- split allocations
- bundle donations
- reserve riders
- send notifications
- cancel plans
- re-plan
- record outcomes
- escalate decisions

Every major agent should have explicit tool access.

---

## Principle 2 — LLMs do reasoning, deterministic systems enforce hard constraints

Never allow the LLM to override food-safety constraints.

Use a deterministic Safety Policy Engine for hard constraints.

The LLM can:

- interpret messages
- reason about tradeoffs
- explain decisions
- choose among valid options
- request tools

The deterministic policy engine decides:

- whether a food item is outside its allowed window
- whether ETA exceeds the remaining safety window
- whether a recipient can legally/operationally accept the food
- whether capacity is exceeded
- whether required information is missing

The architecture should make this distinction visible.

---

## Principle 3 — The system should be proactive

The system must have a Forecast Agent.

It should use historical and simulated data to predict:

- likely surplus
- expected quantity
- likely time
- expected demand
- rider availability patterns

For the hackathon, this can use a lightweight statistical/ML model or deterministic forecasting algorithm rather than requiring a complex production ML system.

The important feature is the agentic behavior:

**prediction → preparation → execution**

---

## Principle 4 — Dynamic re-planning

The environment is not static.

The system should respond to events such as:

- new donation
- donation quantity changed
- NGO capacity changed
- rider became unavailable
- rider became delayed
- safety window approaching
- NGO rejected shipment
- another donation appeared nearby

Whenever a significant event occurs, the relevant agents should reconsider the current plan.

---

# 3. HIGH-LEVEL ARCHITECTURE

Implement the following architecture.

```text
                         HUMAN NETWORK
                              |
              +---------------+----------------+
              |               |                |
           Vendors           NGOs            Riders
              |               |                |
              +---------------+----------------+
                              |
                         WhatsApp/API
                              |
                              v
                    +---------------------+
                    |   API Gateway /    |
                    |    Web Interface   |
                    +----------+----------+
                               |
                               v
                    +---------------------+
                    |   Signal Agent      |
                    |                    |
                    | Message -> Event   |
                    +----------+----------+
                               |
                               v
                    +---------------------+
                    | Event / State Layer |
                    |                     |
                    | DynamoDB            |
                    | S3                  |
                    +----------+----------+
                               |
              +----------------+----------------+
              |                |                |
              v                v                v
       Forecast Agent    Demand Agent     Trust Agent
              |                |                |
              +----------------+----------------+
                               |
                               v
                    +---------------------+
                    | Allocation Agent    |
                    |                     |
                    | Global planning    |
                    | split / merge       |
                    +----------+----------+
                               |
                +--------------+--------------+
                |              |              |
                v              v              v
          Safety Agent   Logistics Agent   Trust Agent
                |              |
                v              v
        Safety Policy     Amazon Location
           Engine         ETA / routing
                |              |
                +------+-------+
                       |
                       v
                Execution Layer
                       |
            +----------+----------+
            |          |           |
            v          v           v
         Notify     Reserve      Track
         Vendor     Rider        Delivery
                       |
                       v
                Supervisor Agent
                       |
                +------+------+
                |             |
             Automatic      Human
             completion    escalation
```

---

# 4. AWS ARCHITECTURE

Use AWS services meaningfully.

Preferred architecture:

```text
Frontend
   |
   v
Amazon CloudFront / S3
   |
   v
API Gateway
   |
   v
AWS Lambda / backend service
   |
   v
Strands Agents
   |
   +------------------------------+
   |                              |
   v                              v
Amazon Bedrock               AgentCore
                              |
                +-------------+-------------+
                |             |             |
              Runtime       Memory      Observability
                |
                v
          Agent orchestration
                |
       +--------+---------+
       |        |         |
       v        v         v
   DynamoDB    S3    Amazon Location
       |
       v
 Event/state/history
```

Use:

### Amazon Bedrock

For the foundation model powering reasoning agents.

Use a Bedrock model supported by the current AWS/Strands environment.

Do not hard-code a model unnecessarily.

Configure the model through environment variables.

Example:

```env
AWS_REGION=...
BEDROCK_MODEL_ID=...
```

---

### Strands Agents SDK

This is mandatory.

Use the official **Strands Agents SDK** as the primary agent framework.

Do NOT implement a fake multi-agent system where multiple functions are simply called sequentially.

Each agent should be a genuine Strands agent with:

- system prompt
- model
- tools
- state/context where appropriate
- explicit responsibilities

Recommended modules:

```text
agents/
    supervisor_agent.py
    signal_agent.py
    forecast_agent.py
    demand_agent.py
    allocation_agent.py
    logistics_agent.py
    safety_agent.py
    trust_agent.py
```

---

### Amazon Bedrock AgentCore

Use AgentCore where practical and available.

The architecture should be designed to support:

- AgentCore Runtime
- AgentCore Memory
- AgentCore Gateway where useful
- AgentCore Observability

If deployment constraints make every component impossible during development, ensure the application still runs locally while preserving a clear AgentCore deployment path.

The README must explicitly explain which AgentCore capabilities are being used and why.

---

# 5. AGENT RESPONSIBILITIES

## 5.1 SIGNAL AGENT

### Purpose

Convert unstructured human messages into structured events.

Example input:

> "Bhai 45 plates rice dal available around 8:30, pickup before 9:15."

Output:

```json
{
  "event_type": "SURPLUS_CREATED",
  "vendor_id": "vendor_001",
  "food_items": [
    {
      "type": "rice_dal",
      "quantity": 45,
      "unit": "meals"
    }
  ],
  "available_at": "20:30",
  "latest_safe_pickup": "21:15",
  "location": {
    "lat": 28.61,
    "lng": 77.23
  }
}
```

Tools:

```text
create_surplus_event()
update_surplus_event()
lookup_vendor()
get_vendor_history()
validate_event_schema()
```

The Signal Agent must not make allocation decisions.

---

# 6. FORECAST AGENT

Purpose:

Predict future surplus and demand.

Inputs:

- historical vendor events
- day of week
- time
- vendor type
- recent surplus patterns
- historical NGO demand

Output:

```json
{
  "vendor_id": "vendor_001",
  "prediction": {
    "probability": 0.87,
    "expected_quantity": 48,
    "time_window": "20:30-21:15"
  }
}
```

Use a lightweight forecasting approach.

Possible implementation:

- rolling averages
- exponentially weighted moving average
- simple regression
- probabilistic heuristic

Do not build an unnecessarily complicated ML system.

The important point is that the Forecast Agent should use tools to retrieve historical state and write predictions back into the system.

---

# 7. DEMAND AGENT

Track recipient requirements.

Each NGO should have:

```json
{
  "ngo_id": "ngo_001",
  "capacity": 50,
  "current_capacity": 25,
  "preferred_food_types": [
    "rice",
    "dal",
    "vegetarian_meals"
  ],
  "location": {},
  "operating_hours": {},
  "reliability_score": 0.91
}
```

The Demand Agent should answer:

- Who needs food?
- How much?
- What type?
- How urgently?
- What is their remaining capacity?

Tools:

```text
get_ngo_capacity()
get_ngo_preferences()
update_ngo_capacity()
record_demand()
```

---

# 8. TRUST AGENT

Create a dynamic reliability model.

Track:

```text
pickup punctuality
quantity accuracy
cancellation rate
response time
successful deliveries
rejection rate
delivery completion
```

Maintain a trust/reliability score.

Example:

```json
{
  "participant_id": "ngo_001",
  "trust_score": 0.91,
  "factors": {
    "punctuality": 0.95,
    "response": 0.88,
    "completion": 0.94
  }
}
```

Do not use trust as an exclusionary black box.

Use it as one factor in allocation and routing.

The system should explain why reliability affected a decision.

---

# 9. ALLOCATION AGENT

This is the core intelligence of AnnaSetu.

Its job is to determine:

> What allocation plan maximizes successful safe rescue?

The agent should consider:

```text
quantity
distance
ETA
remaining safety window
NGO capacity
food compatibility
rider capacity
participant reliability
urgency
bundling opportunities
splitting opportunities
```

---

# 10. RESCUE SCORE

Implement a deterministic scoring engine.

Example conceptual score:

```text
Rescue Score =
Expected Successfully Rescued Food
-----------------------------------
Transport Cost + Time Penalty
```

Where expected rescued food incorporates:

```text
quantity
× probability of successful delivery
× safety validity
```

Do NOT let the LLM invent numerical scores.

Use deterministic calculations.

The LLM should choose between valid plans and explain its choice.

---

# 11. DYNAMIC BUNDLING

Implement donation bundling.

Example:

```text
Restaurant A → 25 meals
Restaurant B → 15 meals

NGO X capacity → 45

Distance A-B → 1.2 km
```

The system may create:

```text
A + B → NGO X
```

rather than two independent deliveries.

Tool:

```text
find_bundle_candidates()
evaluate_bundle()
create_bundle()
```

---

# 12. DYNAMIC SPLITTING

If:

```text
Donation = 60 meals

NGO X capacity = 30
NGO Y capacity = 40
```

create:

```text
30 → NGO X
30 → NGO Y
```

Tool:

```text
split_allocation()
```

The split must respect:

- capacity
- food compatibility
- logistics
- safety

---

# 13. LOGISTICS AGENT

Use Amazon Location Service where practical.

Responsibilities:

- calculate distance
- estimate travel time
- find available riders
- reserve riders
- calculate pickup route
- calculate delivery route
- re-route when required

Tools:

```text
calculate_distance()
calculate_eta()
find_available_riders()
reserve_rider()
release_rider()
update_rider_location()
```

The Logistics Agent should NEVER override Safety Agent constraints.

---

# 14. SAFETY AGENT

This is one of the most important parts of the architecture.

The Safety Agent must operate with a deterministic policy engine.

Example:

```python
def validate_delivery(food, eta):
    if food.remaining_safe_minutes <= 0:
        return REJECT

    if eta > food.remaining_safe_minutes:
        return REJECT

    if food.temperature_requirement_missing:
        return ESCALATE

    return PASS
```

The LLM can explain:

> "This delivery was blocked because the estimated travel time exceeds the remaining safe handling window."

But it cannot change:

```text
REJECT → PASS
```

---

# 15. SUPERVISOR AGENT

The Supervisor coordinates the entire system.

It should NOT perform every task itself.

It should:

1. understand the global state
2. delegate work
3. monitor agent outputs
4. detect conflicts
5. initiate re-planning
6. escalate genuine human decisions

Example:

```text
SURPLUS_EVENT
      |
      v
Signal Agent
      |
      v
Forecast / Demand
      |
      v
Allocation
      |
      v
Safety
      |
      v
Logistics
      |
      v
Execution
      |
      v
Completed
```

If something fails:

```text
Logistics failure
      |
      v
Supervisor
      |
      v
Re-plan
      |
      v
Alternative rider
```

---

# 16. HUMAN ESCALATION POLICY

The system should minimize human interruptions.

Human escalation is allowed only when:

- multiple valid allocations are materially equivalent
- required safety information is missing
- an operational policy requires human approval
- a donation cannot be safely routed automatically
- unusual edge case is detected

Example:

```json
{
  "requires_human": true,
  "reason": "Two NGOs have equivalent rescue scores.",
  "options": [
    {
      "ngo": "ngo_001",
      "score": 91
    },
    {
      "ngo": "ngo_002",
      "score": 90.8
    }
  ]
}
```

The UI should show:

> **Decision required**

rather than making a hidden arbitrary choice.

---

# 17. EVENT-DRIVEN PIPELINE

Design the application around events.

Supported events:

```text
SURPLUS_CREATED
SURPLUS_UPDATED
SURPLUS_EXPIRING
DEMAND_CREATED
DEMAND_UPDATED
RIDER_AVAILABLE
RIDER_UNAVAILABLE
RIDER_DELAYED
PICKUP_COMPLETED
DELIVERY_COMPLETED
DELIVERY_FAILED
NGO_REJECTED
SAFETY_BLOCKED
REPLAN_REQUIRED
```

Each event should be persisted.

Use DynamoDB for current state and event records.

---

# 18. COMPLETE PIPELINE — NORMAL FLOW

Implement this exact logical flow.

```text
1. Vendor sends message
        ↓
2. Signal Agent parses message
        ↓
3. Event created
        ↓
4. State persisted
        ↓
5. Demand Agent checks recipient capacity
        ↓
6. Trust Agent retrieves reliability
        ↓
7. Forecast Agent updates future state
        ↓
8. Allocation Agent generates candidate plans
        ↓
9. Deterministic Rescue Score evaluates candidates
        ↓
10. Safety Agent validates candidates
        ↓
11. Logistics Agent calculates ETA
        ↓
12. Allocation Agent selects valid plan
        ↓
13. Supervisor approves execution
        ↓
14. Rider reserved
        ↓
15. NGO notified
        ↓
16. Vendor notified
        ↓
17. Pickup tracked
        ↓
18. Delivery completed
        ↓
19. State updated
        ↓
20. Trust scores updated
        ↓
21. Outcome recorded
```

---

# 19. COMPLETE PIPELINE — FAILURE FLOW

Implement a real failure scenario.

Example:

```text
Donation:
50 meals

Remaining safety window:
42 minutes

Rider ETA:
65 minutes
```

Flow:

```text
Logistics Agent
       ↓
ETA = 65 min
       ↓
Safety Agent
       ↓
REJECT
       ↓
Supervisor
       ↓
REPLAN
       ↓
Find alternative rider
       ↓
ETA = 18 min
       ↓
Safety PASS
       ↓
Execute
```

The UI must visibly show this.

This should be one of the main hackathon demo scenarios.

---

# 20. COMPLETE PIPELINE — PREDICTIVE FLOW

Demonstrate:

```text
Historical events
       ↓
Forecast Agent
       ↓
High probability surplus
       ↓
Network preparation
       ↓
Reserve likely recipient capacity
       ↓
Identify nearby riders
       ↓
Actual surplus arrives
       ↓
Fast allocation
       ↓
Execution
```

This is AnnaSetu's primary differentiating capability.

---

# 21. COMPLETE PIPELINE — DYNAMIC RE-PLANNING

Example:

```text
Plan created

A → NGO X
B → NGO Y

        ↓

Rider assigned to A becomes unavailable

        ↓

Event:
RIDER_UNAVAILABLE

        ↓

Supervisor detects plan invalidation

        ↓

Logistics Agent searches alternatives

        ↓

Alternative rider found

        ↓

Safety validation

        ↓

New plan

        ↓

Execution continues
```

The user should see the plan changing live.

---

# 22. DATA MODEL

Use DynamoDB.

Recommended entities:

## Vendor

```text
PK = VENDOR#<id>
SK = PROFILE
```

Fields:

```text
name
type
location
operating_hours
historical_surplus
trust_score
```

## NGO

```text
PK = NGO#<id>
SK = PROFILE
```

Fields:

```text
name
location
capacity
food_preferences
operating_hours
trust_score
```

## Rider

```text
PK = RIDER#<id>
SK = PROFILE
```

Fields:

```text
name
location
capacity
availability
vehicle_type
trust_score
```

## Surplus

```text
PK = SURPLUS#<id>
SK = EVENT
```

Fields:

```text
vendor_id
food_type
quantity
created_at
available_at
safe_until
status
location
```

## Allocation

```text
PK = ALLOCATION#<id>
SK = PLAN
```

Fields:

```text
surplus_ids
ngo_id
rider_id
quantity
eta
rescue_score
safety_status
status
```

## Event

```text
PK = EVENT#<id>
SK = TIMESTAMP#<timestamp>
```

Fields:

```text
event_type
actor
payload
created_at
```

---

# 23. MEMORY

Use AgentCore Memory or an equivalent AWS-backed persistence mechanism where appropriate.

Memory should allow agents to retain useful operational context such as:

```text
vendor patterns
participant reliability
successful routing patterns
historical demand
previous interactions
```

Do NOT store unnecessary personal information.

Use synthetic/demo data for the hackathon.

---

# 24. TOOL ARCHITECTURE

Every tool must have:

- clear input schema
- clear output schema
- validation
- error handling
- logging

Recommended tool structure:

```text
tools/
    participant_tools.py
    surplus_tools.py
    demand_tools.py
    logistics_tools.py
    safety_tools.py
    allocation_tools.py
    notification_tools.py
    trust_tools.py
    analytics_tools.py
```

Example:

```python
@tool
def find_available_riders(
    latitude: float,
    longitude: float,
    required_capacity: int
):
    ...
```

Agents should invoke tools rather than directly manipulating databases wherever practical.

---

# 25. NOTIFICATION SYSTEM

For hackathon demonstration, provide two modes.

## Mode A — WhatsApp integration

Design the backend around WhatsApp Cloud API.

Incoming:

```text
POST /webhooks/whatsapp
```

Outgoing:

```text
send_whatsapp_message()
```

The implementation must support webhook verification.

Use environment variables:

```env
WHATSAPP_VERIFY_TOKEN=
WHATSAPP_ACCESS_TOKEN=
WHATSAPP_PHONE_NUMBER_ID=
```

---

## Mode B — Demo simulator

Because external WhatsApp credentials may not be available during judging, build a simulator in the frontend.

It should visually resemble conversations.

Example:

```text
Vendor — 8:41 PM

"45 meals ready."

AnnaSetu — 8:41 PM

"Received. Finding the safest rescue plan..."
```

The same backend event pipeline should process simulator messages.

DO NOT create a completely separate fake backend.

The simulator must call the same APIs as the WhatsApp integration.

---

# 26. FRONTEND

Build a polished dashboard.

The UI should have:

## Dashboard

Show:

```text
Meals rescued today
Active donations
Active deliveries
Food at risk
Current riders
Pending human decisions
```

---

## Live Network

Display:

```text
Vendors
NGOs
Riders
Active food
Routes
```

Use a map if practical.

---

## Agent Activity

This is essential.

Show a live agent timeline:

```text
20:41:02 Signal Agent
Parsed 45 meals

20:41:03 Demand Agent
Found 3 eligible NGOs

20:41:04 Trust Agent
Ranked participants

20:41:05 Allocation Agent
Generated 4 plans

20:41:06 Safety Agent
Plan #2 rejected

20:41:07 Logistics Agent
Rider #14 ETA 17 min

20:41:08 Supervisor
Plan #3 approved
```

This makes the multi-agent system visible to judges.

---

# 27. DECISION EXPLAINABILITY

Every major autonomous decision should have an explanation.

Example:

```text
WHY NGO X?

Capacity:
30 meals

Distance:
2.1 km

ETA:
14 min

Reliability:
94%

Safety:
PASS

Rescue Score:
91.4
```

The system should clearly distinguish:

```text
FACT
CALCULATION
AGENT REASONING
```

This avoids pretending that an LLM generated objective facts.

---

# 28. AGENT OBSERVABILITY

Use AgentCore Observability and/or CloudWatch where available.

Track:

```text
agent execution
tool calls
latency
errors
decision paths
re-planning events
human escalations
```

Create an observability view in the dashboard if practical.

Example:

```text
Agent
Calls
Latency
Success
Escalations

Signal
124
0.8s
99%
0

Allocation
73
2.1s
96%
3

Safety
73
0.2s
100%
4

Logistics
68
1.3s
97%
1
```

---

# 29. SECURITY

Never hard-code credentials.

Use:

```text
AWS IAM
environment variables
AWS Secrets Manager where appropriate
```

Never commit:

```text
AWS_SECRET_ACCESS_KEY
AWS_ACCESS_KEY_ID
BEDROCK credentials
WhatsApp tokens
API keys
```

Include:

```text
.env.example
```

with placeholders only.

---

# 30. ERROR HANDLING

Every agent must gracefully handle:

- malformed input
- unavailable tools
- timeout
- missing state
- invalid location
- no recipient
- no rider
- safety failure
- Bedrock failure

Never let one agent crash the entire workflow.

The Supervisor should be able to mark:

```text
REPLAN_REQUIRED
```

or:

```text
HUMAN_REQUIRED
```

---

# 31. IDEMPOTENCY

Important for production-quality architecture.

Events may arrive multiple times.

Implement idempotency keys.

For example:

```text
event_id
request_id
allocation_id
```

Repeated webhook events must not create duplicate deliveries.

---

# 32. SIMULATION ENGINE

Because the hackathon needs a reliable demo, create a deterministic simulation environment.

Seed:

```text
8 vendors
5 NGOs
10 riders
historical events
current events
historical demand
```

Allow the judge to trigger scenarios:

```text
NORMAL RESCUE

SURPLUS SPIKE

RIDER FAILURE

SAFETY FAILURE

DONATION SPLIT

DONATION BUNDLING

PREDICTIVE SURPLUS
```

Every scenario should run through the real agent pipeline.

---

# 33. DEMO MODE

Add a clearly visible:

**DEMO MODE**

This should allow judges to start predefined scenarios.

Example:

```text
Scenario 1:
"Friday Night Surplus"

Scenario 2:
"Rider Cancellation"

Scenario 3:
"Food Safety Conflict"

Scenario 4:
"Multi-NGO Split"

Scenario 5:
"Predictive Pre-positioning"
```

The demo mode should NOT bypass the agents.

It only supplies controlled input events.

---

# 34. KEY DEMO SCENARIO

The primary demo must be:

## "45 Meals, 42 Minutes, One Failed Rider"

Initial state:

```text
Restaurant A:
45 meals

Safety window:
42 minutes

NGO X:
capacity 30

NGO Y:
capacity 40

Rider A:
available

Rider B:
available
```

System creates plan.

Then introduce:

```text
Rider A:
UNAVAILABLE
```

System should automatically:

```text
detect failure
→ re-plan
→ select Rider B
→ calculate ETA
→ safety validate
→ execute
```

Then show final:

```text
45 meals rescued
0 safety violations
1 failed plan automatically recovered
```

---

# 35. SECOND DEMO SCENARIO

## "Predict Before the Food Exists"

Show historical data:

```text
Vendor A

Mon:
42 meals

Tue:
48 meals

Wed:
44 meals

Thu:
51 meals

Fri:
?
```

Forecast Agent:

```text
Predicted Friday surplus:
45–60 meals

Confidence:
87%
```

AnnaSetu proactively identifies:

```text
NGO capacity
rider availability
likely routes
```

When actual surplus appears, the network is already prepared.

---

# 36. THIRD DEMO SCENARIO

## "The Safety Agent Says No"

Input:

```text
Food:
30 meals

Remaining safe window:
25 minutes

Closest rider ETA:
38 minutes
```

System must show:

```text
SAFETY BLOCK

Reason:
ETA exceeds remaining safe window.

Action:
Search alternative.
```

This must be a hard deterministic block.

---

# 37. API DESIGN

Create REST APIs such as:

```text
POST /api/events
POST /api/surplus
GET  /api/surplus
GET  /api/ngos
GET  /api/riders
POST /api/allocate
POST /api/replan
POST /api/simulate
GET  /api/network
GET  /api/agents
GET  /api/decisions
GET  /api/metrics
POST /api/webhooks/whatsapp
```

Do not expose internal AWS credentials.

---

# 38. BACKEND STRUCTURE

Preferred structure:

```text
backend/
├── agents/
│   ├── supervisor.py
│   ├── signal.py
│   ├── forecast.py
│   ├── demand.py
│   ├── allocation.py
│   ├── logistics.py
│   ├── safety.py
│   └── trust.py
│
├── tools/
│   ├── surplus.py
│   ├── demand.py
│   ├── logistics.py
│   ├── allocation.py
│   ├── safety.py
│   ├── trust.py
│   └── notifications.py
│
├── services/
│   ├── event_service.py
│   ├── safety_service.py
│   ├── scoring_service.py
│   ├── simulation_service.py
│   └── notification_service.py
│
├── models/
│   ├── events.py
│   ├── surplus.py
│   ├── ngo.py
│   ├── rider.py
│   └── allocation.py
│
├── api/
│   ├── events.py
│   ├── simulation.py
│   ├── network.py
│   └── whatsapp.py
│
├── config/
│   └── settings.py
│
└── main.py
```

---

# 39. FRONTEND STRUCTURE

Use React + TypeScript.

Recommended:

```text
frontend/
├── src/
│   ├── pages/
│   │   ├── Dashboard.tsx
│   │   ├── Network.tsx
│   │   ├── AgentActivity.tsx
│   │   ├── Donations.tsx
│   │   └── Simulation.tsx
│   │
│   ├── components/
│   │   ├── NetworkMap.tsx
│   │   ├── AgentTimeline.tsx
│   │   ├── DecisionCard.tsx
│   │   ├── DonationCard.tsx
│   │   ├── SafetyAlert.tsx
│   │   └── MetricsPanel.tsx
│   │
│   ├── services/
│   │   └── api.ts
│   │
│   └── types/
│       └── index.ts
```

---

# 40. VISUAL DESIGN

The interface should feel like a serious operational system rather than a generic AI chatbot.

Design characteristics:

- clean
- modern
- high information density
- accessible
- mobile responsive
- strong hierarchy
- minimal unnecessary decoration

The main screen should immediately communicate:

```text
WHAT IS HAPPENING?
WHY DID THE SYSTEM DECIDE THIS?
WHAT WILL HAPPEN NEXT?
```

---

# 41. LANDING PAGE

Hero:

> **AnnaSetu**

Subtitle:

> **The autonomous food rescue mesh.**

Supporting statement:

> Predict surplus. Coordinate capacity. Optimize rescue. Adapt in real time.

CTA:

```text
Launch Network
Run Demo
```

Show a simple animation:

```text
SURPLUS → AGENTS → RESCUE
```

---

# 42. IMPACT METRICS

Track real metrics inside the application:

```text
meals rescued
kg food rescued
successful deliveries
failed deliveries
average coordination time
average pickup ETA
food safety blocks
automatic recoveries
human escalations
distance traveled
```

Do not fabricate metrics in the final submission.

All displayed metrics must come from the simulation/database.

---

# 43. BEFORE VS AFTER

Create an impact comparison.

Traditional process:

```text
Receive message
→ phone calls
→ find NGO
→ find rider
→ negotiate
→ coordinate
```

AnnaSetu:

```text
Message
→ agents
→ plan
→ safety
→ execution
```

Track actual simulated coordination latency.

---

# 44. AGENT COMMUNICATION

Make inter-agent communication structured.

Use typed objects rather than passing arbitrary strings wherever possible.

Example:

```json
{
  "task_id": "task_123",
  "agent": "allocation",
  "input": {
    "surplus_id": "surplus_001"
  },
  "output": {
    "candidate_plans": []
  }
}
```

Log:

```text
agent
task
timestamp
input_summary
tool_calls
result
decision
```

Avoid storing unnecessary sensitive data.

---

# 45. SUPERVISOR STATE MACHINE

Implement a clear workflow state machine.

States:

```text
RECEIVED
STRUCTURED
FORECASTED
MATCHING
ALLOCATED
SAFETY_CHECK
LOGISTICS_CHECK
READY
EXECUTING
PICKED_UP
DELIVERED
COMPLETED
FAILED
REPLANNING
HUMAN_REQUIRED
EXPIRED
```

Transitions must be validated.

---

# 46. SAFETY STATE MACHINE

Safety states:

```text
UNKNOWN
PENDING
PASS
BLOCKED
EXPIRED
HUMAN_REVIEW
```

Never transition:

```text
BLOCKED → PASS
```

without a new validated state.

---

# 47. TESTING

Create tests for:

## Unit tests

- safety rules
- rescue score
- splitting
- bundling
- ETA
- capacity
- trust calculation

## Agent tests

- Signal extraction
- Allocation reasoning
- Logistics tool use
- Safety behavior
- Supervisor recovery

## Integration tests

```text
surplus → allocation → safety → logistics → completion
```

## Failure tests

```text
rider unavailable
NGO unavailable
expired food
duplicate event
invalid message
no valid allocation
```

---

# 48. LOCAL DEVELOPMENT

The application must run locally without requiring every AWS integration.

Provide:

```text
MOCK_AWS=true
MOCK_WHATSAPP=true
MOCK_LOCATION=true
```

When enabled:

- DynamoDB Local or in-memory persistence can be used.
- Location calculations can use deterministic mock coordinates.
- WhatsApp becomes the simulator.
- Bedrock can optionally use a development fallback only if necessary.

However, the architecture and production configuration must remain AWS-native.

---

# 49. PRODUCTION CONFIGURATION

Use:

```env
AWS_REGION=
BEDROCK_MODEL_ID=

DYNAMODB_TABLE=
S3_BUCKET=

AGENTCORE_RUNTIME_ID=
AGENTCORE_MEMORY_ID=

WHATSAPP_VERIFY_TOKEN=
WHATSAPP_ACCESS_TOKEN=
WHATSAPP_PHONE_NUMBER_ID=

LOCATION_CALCULATOR_NAME=
```

Never commit real credentials.

---

# 50. AWS DEPLOYMENT

Provide infrastructure configuration.

Prefer:

```text
AWS CDK
```

or another appropriate AWS IaC approach.

The deployment should provision:

```text
DynamoDB
S3
Lambda/API
IAM roles
CloudWatch logging
API Gateway
```

Where AgentCore deployment is supported, include the corresponding configuration.

The README must explain:

```text
Local development
AWS deployment
AgentCore deployment
Environment variables
IAM permissions
```

---

# 51. IAM

Use least privilege.

Create separate permissions where practical for:

```text
DynamoDB
S3
Bedrock
Location
CloudWatch
AgentCore
```

Do not use unrestricted permissions such as:

```text
AdministratorAccess
```

for production execution roles.

---

# 52. README REQUIREMENTS

Create a highly polished README.

It must contain:

## 1. Hero

```text
AnnaSetu
The Autonomous Food Rescue Mesh
```

## 2. Problem

Explain:

- food surplus is unpredictable
- NGO demand is fragmented
- transportation is constrained
- manual coordination is slow
- safety windows make delay costly

## 3. Solution

Explain predictive, autonomous coordination.

## 4. Why agents?

Explain why multiple agents are necessary.

## 5. Architecture

Include the complete architecture diagram.

## 6. Agent responsibilities

Document every agent.

## 7. AWS architecture

Document:

- Bedrock
- Strands
- AgentCore
- DynamoDB
- S3
- Location
- Lambda/API Gateway
- CloudWatch

## 8. Safety architecture

Explain:

> LLM reasoning does not override deterministic safety constraints.

## 9. Demo

Provide demo scenarios.

## 10. Local setup

Give exact commands.

## 11. AWS deployment

Give exact deployment instructions.

## 12. Environment variables

Document `.env.example`.

## 13. Testing

Provide test commands.

## 14. Screenshots

Add polished screenshots.

## 15. Demo video

Provide link placeholder.

## 16. Hackathon track

Explicitly state:

> Good Neighbor Agents

## 17. Open source

Include:

> MIT License

---

# 53. LICENSE

Add an MIT License.

The GitHub repository's About section must clearly indicate the open-source license.

---

# 54. ARCHITECTURE DIAGRAM

Create a polished architecture diagram as:

```text
HUMANS
  |
WhatsApp / Web
  |
API Gateway
  |
Signal Agent
  |
Event State
  |
+---------------------------+
|                           |
Forecast                Demand
Agent                   Agent
|                           |
+-------------+-------------+
              |
         Allocation
           Agent
              |
     +--------+--------+
     |        |        |
 Safety   Logistics   Trust
 Agent      Agent     Agent
     |        |
     |     Location
     |
Safety Policy
     |
     +--------+
              |
          Supervisor
              |
      +-------+-------+
      |               |
   Execute          Escalate
      |
Notifications / Rider / NGO
```

The actual final diagram should also include AWS service logos and clearly indicate:

```text
Amazon Bedrock
Strands Agents SDK
AgentCore Runtime
AgentCore Memory
AgentCore Observability
DynamoDB
S3
Amazon Location Service
Lambda
API Gateway
CloudWatch
```

---

# 55. AGENTIC DESIGN REQUIREMENT

Do NOT create a fake architecture like:

```text
LLM 1
LLM 2
LLM 3
LLM 4
```

Agents must have distinct decision boundaries.

Use:

```text
Signal → understands
Forecast → predicts
Demand → understands capacity
Trust → evaluates reliability
Allocation → plans
Safety → validates
Logistics → executes transportation
Supervisor → coordinates/replans
```

---

# 56. NO SINGLE GIANT AGENT

Do not create one giant agent that calls all tools.

The Supervisor must delegate to specialized agents.

The specialized agents must have minimal tool permissions.

For example:

Signal Agent:

```text
message parsing
event creation
```

Safety Agent:

```text
safety validation
```

Logistics:

```text
routing
riders
```

Allocation:

```text
planning
```

This demonstrates proper agentic architecture.

---

# 57. AVOID UNNECESSARY LLM CALLS

Not every operation requires an LLM.

Use deterministic code for:

```text
distance
ETA
capacity
safety
scores
database CRUD
state transitions
```

Use LLM reasoning for:

```text
messy human input
ambiguous intent
planning
tradeoff analysis
explanation
exception interpretation
```

This makes the system faster, cheaper and more reliable.

---

# 58. OBSERVABLE REASONING

Do NOT expose hidden chain-of-thought.

Instead show structured decision summaries.

Example:

```text
Decision:
Choose NGO X

Factors:
- capacity sufficient
- 2.1 km distance
- 14 min ETA
- 94% reliability
- food compatible
- safety PASS
```

Never expose private chain-of-thought.

---

# 59. PERFORMANCE TARGETS

Design for:

```text
normal allocation:
< 5 seconds

safety validation:
< 500 ms

re-planning:
< 5 seconds

dashboard event update:
near real-time
```

These are engineering targets, not fabricated results.

Measure actual performance in demo mode.

---

# 60. DEMO SCRIPT SUPPORT

Create a `/demo` route.

The route should provide controls:

```text
START DEMO

Inject Surplus
Inject Rider Failure
Inject Safety Conflict
Inject New NGO
Inject Demand Spike
Trigger Forecast
```

The controls should invoke the actual backend event APIs.

---

# 61. FINAL JUDGE EXPERIENCE

A judge should be able to understand the system within 30 seconds.

When the application opens, immediately show:

```text
ACTIVE NETWORK

12 vendors
5 NGOs
8 riders

Today's rescue:
327 meals

Current risk:
14 meals approaching expiry

Agent status:
All operational
```

Then demonstrate one active rescue.

---

# 62. FINAL DEMO STORY

The demo should communicate:

### Problem

Food surplus and people in need are separated by a coordination problem.

### Insight

The network needs to predict and coordinate continuously.

### Solution

AnnaSetu uses autonomous agents to coordinate it.

### Proof

Show:

```text
surplus
→ prediction
→ allocation
→ safety
→ logistics
→ execution
```

### Failure

Break the system intentionally.

Show automatic recovery.

### Differentiator

Show predictive pre-positioning.

### Impact

Show measurable rescue metrics.

---

# 63. HACKATHON POSITIONING

The project description should emphasize:

> AnnaSetu is not another donation marketplace or chatbot.

It is:

> **an autonomous coordination layer for decentralized food rescue.**

Its key capabilities are:

```text
Predict
Plan
Validate
Execute
Adapt
Learn
```

---

# 64. BUILD PRIORITY

Build in this order.

## PHASE 1 — CORE ENGINE

Implement:

```text
DynamoDB/in-memory state
events
surplus
NGO
rider
allocation
safety
```

## PHASE 2 — STRANDS

Implement:

```text
Signal Agent
Allocation Agent
Safety Agent
Logistics Agent
Supervisor Agent
```

## PHASE 3 — REAL AGENT TOOLS

Implement:

```text
database tools
location tools
allocation tools
safety tools
notification tools
```

## PHASE 4 — PREDICTION

Implement:

```text
Forecast Agent
Demand Agent
Trust Agent
```

## PHASE 5 — RE-PLANNING

Implement:

```text
rider failure
safety conflict
NGO capacity change
new donation
```

## PHASE 6 — AWS

Integrate:

```text
Bedrock
DynamoDB
Location
CloudWatch
AgentCore
```

## PHASE 7 — FRONTEND

Build:

```text
dashboard
network
agent timeline
simulation
decision cards
metrics
```

## PHASE 8 — DEMO HARDENING

Create deterministic scenarios.

## PHASE 9 — DOCUMENTATION

Create:

```text
README
architecture diagram
setup
deployment
screenshots
license
```

---

# 65. CRITICAL IMPLEMENTATION RULE

At every stage ask:

> "Does this demonstrate that an autonomous agent is doing meaningful work?"

If the answer is no, simplify it.

Do not add unnecessary AI.

The goal is not maximum number of agents.

The goal is:

> **maximum useful autonomous behavior with minimum unnecessary complexity.**

---

# 66. FINAL QUALITY BAR

Before considering the application complete, verify:

```text
[ ] Strands Agents SDK is genuinely used
[ ] Amazon Bedrock is used for reasoning
[ ] AgentCore deployment/configuration is present
[ ] Agents have distinct responsibilities
[ ] Agents use real tools
[ ] State is persisted
[ ] Safety constraints are deterministic
[ ] Allocation is deterministic/constraint-aware
[ ] Prediction exists
[ ] Dynamic re-planning exists
[ ] Bundling exists
[ ] Splitting exists
[ ] Trust exists
[ ] Logistics exists
[ ] Human escalation exists
[ ] WhatsApp architecture exists
[ ] Demo simulator exists
[ ] Frontend is polished
[ ] Agent activity is visible
[ ] AWS architecture is documented
[ ] Observability is implemented
[ ] Tests exist
[ ] Failure handling exists
[ ] Idempotency exists
[ ] Credentials are protected
[ ] .env.example exists
[ ] MIT License exists
[ ] README is complete
[ ] Architecture diagram exists
[ ] Demo scenarios are deterministic
[ ] Application runs locally
[ ] AWS deployment path is documented
```

---

# 67. FINAL PRODUCT IDENTITY

Name:

**AnnaSetu**

Tagline:

> **The Autonomous Food Rescue Mesh**

One-liner:

> **AnnaSetu predicts surplus, coordinates community capacity, validates safety, executes rescue logistics, and autonomously re-plans when reality changes.**

Core loop:

```text
PREDICT
   ↓
PREPARE
   ↓
DETECT
   ↓
ALLOCATE
   ↓
VALIDATE
   ↓
EXECUTE
   ↓
MONITOR
   ↓
ADAPT
   ↓
LEARN
   ↺
```

Build the application around this loop.

Do not reduce AnnaSetu to a chatbot.

Do not reduce it to a food marketplace.

Do not reduce it to a static matching algorithm.

It must feel like an **autonomous operating system for a local food-rescue network**.

The final application should be something a hackathon judge can interact with, break, observe recovering automatically, and immediately understand why multiple agents are necessary.