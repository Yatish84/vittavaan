# Vittavaan — v2 Documentation Index

> This folder contains the definitive, engineering-ready specification documents for Vittavaan.
> Documents in `docs/` (root) are retained as historical reference from an earlier planning pass.
> **All new planning, design, and specification work goes here.**

---

## Document Map

### Foundation
| File | Purpose | Status |
|---|---|---|
| [`Tech_Stack.md`](./Tech_Stack.md) | Technology choices, rationale, and local dev setup guide | ✅ Draft |
| [`Glossary.md`](./Glossary.md) | Canonical definitions for all domain terms | 🔲 Planned |

### Phase 1 — Requirements
| File | Purpose | Status |
|---|---|---|
| [`Phase1/01_Actors_and_System_Boundary.md`](./Phase1/01_Actors_and_System_Boundary.md) | All actors, system boundary, context diagram | ✅ Draft |
| [`Phase1/02_Functional_Requirements.md`](./Phase1/02_Functional_Requirements.md) | Full functional requirements by domain | ✅ Draft |
| [`Phase1/03_Non_Functional_Requirements.md`](./Phase1/03_Non_Functional_Requirements.md) | Performance, security, data residency, regulatory | ✅ Draft |
| [`Phase1/04_India_Legal_Rules_Catalogue.md`](./Phase1/04_India_Legal_Rules_Catalogue.md) | Indian law rules the system must encode | ✅ Draft |
| [`Phase1/05_Use_Cases.md`](./Phase1/05_Use_Cases.md) | Detailed use cases for all major workflows | ✅ Draft |

### Phase 2 — Analysis
| File | Purpose | Status |
|---|---|---|
| `Phase2/01_ECB_Object_Model.md` | Entity-Control-Boundary object model | 🔲 Planned |
| `Phase2/02_Domain_Glossary.md` | Ubiquitous language definitions | 🔲 Planned |
| `Phase2/03_Sequence_Diagrams.md` | Object interaction for key use cases | 🔲 Planned |

### Phase 3 — System Design
| File | Purpose | Status |
|---|---|---|
| `Phase3/01_Architecture_Overview.md` | Subsystem decomposition, tier diagram | 🔲 Planned |
| `Phase3/02_API_Design.md` | REST API contracts, endpoint spec | 🔲 Planned |
| `Phase3/03_Database_Schema.md` | PostgreSQL schema with rationale | 🔲 Planned |
| `Phase3/04_Auth_and_Authorization.md` | Auth flow, RBAC, ABAC consent proxy | 🔲 Planned |
| `Phase3/05_Event_and_Background_Jobs.md` | Event bus, background worker design | 🔲 Planned |
| `Phase3/06_Data_Room_Architecture.md` | Secure document storage design | 🔲 Planned |

### Phase 4 — Object Design
| File | Purpose | Status |
|---|---|---|
| `Phase4/01_Calculation_Engine_Contracts.md` | Mathematical contracts for all 8 engines | 🔲 Planned |
| `Phase4/02_Design_Patterns.md` | Pattern choices with implementation detail | 🔲 Planned |
| `Phase4/03_Class_Interfaces.md` | Full class interface specifications | 🔲 Planned |
| `Phase4/04_Legal_Rules_Engine_Design.md` | Versioned rules engine data model | 🔲 Planned |

### Phase 5 — Implementation
| File | Purpose | Status |
|---|---|---|
| `Phase5/01_Sprint_Roadmap.md` | Feature phasing and milestone plan | 🔲 Planned |
| `Phase5/02_Project_Structure.md` | Monorepo layout and module conventions | 🔲 Planned |
| `Phase5/03_Code_Standards.md` | Style, linting, commit, review rules | 🔲 Planned |

### Phase 6 — Testing
| File | Purpose | Status |
|---|---|---|
| `Phase6/01_Test_Strategy.md` | Testing pyramid and tooling | 🔲 Planned |
| `Phase6/02_Test_Personas.md` | Realistic test data personas | 🔲 Planned |
| `Phase6/03_Security_Test_Plan.md` | Security-specific test cases | 🔲 Planned |

### Phase 7 — Deployment
| File | Purpose | Status |
|---|---|---|
| `Phase7/01_Infrastructure_as_Code.md` | Docker, cloud provisioning | 🔲 Planned |
| `Phase7/02_CI_CD_Pipeline.md` | GitHub Actions workflow | 🔲 Planned |
| `Phase7/03_Monitoring_and_Observability.md` | Logging, metrics, alerting | 🔲 Planned |

---

*Status key: ✅ Draft · 🔄 In Review · ✔️ Approved · 🔲 Planned*
