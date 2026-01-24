# V2 Inference Engine Migration Plan

**Project:** Cybersecurity Incident Response Expert System  
**Migration Start:** January 24, 2026  
**Status:** 🟡 In Progress

---

## Overview

Complete migration from heuristic-based inference engine to formal forward-chaining engine with Certainty Factor (CF) logic as specified in v2.md.

---

## Migration Phases

### ✅ Phase 1: Planning & Design

**Status:** ✅ COMPLETED  
**Completed:** January 24, 2026

- [x] Analyze current system architecture
- [x] Compare with v2.md specification
- [x] Create migration plan
- [x] Define data models for v2

---

### ✅ Phase 2: Core Engine Implementation

**Status:** ✅ COMPLETED  
**Completed:** January 24, 2026

#### Tasks:

- [x] Create `inference_engine.py` with pure CF logic
  - [x] Implement `combine_cfs()` function
  - [x] Implement `infer()` function
  - [x] Implement `explain()` function (why & why not)
  - [x] Create Trace, ConclusionRecord data classes
- [x] Create `fact_extractor.py` for Alert → Facts conversion
  - [x] Implement symbolic fact extraction
  - [x] Add fact derivation rules (e.g., failed_attempts >= 5 → high_failed_attempts)
- [ ] Unit tests for engine
  - [ ] Test single rule CF assignment
  - [ ] Test CF combination formula
  - [ ] Test trace recording (fired + skipped)
  - [ ] Test explain() for "why" and "why not"

**Files Created:**

- `app/services/inference_engine.py` (replaced old version)
- `app/services/fact_extractor.py`
- `app/tests/test_inference.py` (pending)

---

### ✅ Phase 3: Database Schema Migration

**Status:** ✅ COMPLETED  
**Completed:** January 24, 2026

#### Tasks:

- [x] Add new fields to Rule model
  - [x] Add `cf` (Float, 0.0-1.0) column
  - [x] Add `conclusion` (String) column
  - [x] Add `symbolic_conditions` (JSON) column for set storage
  - [x] Keep existing fields for backward compatibility
- [x] Update Incident model
  - [x] Add `final_cf` (Float) for certainty factor
  - [x] Add `trace` (JSON) for structured trace
  - [x] Add `conclusions` (JSON) for multiple conclusions
  - [x] Keep old fields for backward compatibility
- [x] Database recreation
  - [x] Schema updated successfully

**Files Modified:**

- `app/models/rule.py`
- `app/models/incident.py`
- `scripts/migrate_database.py` (created)

---

### ✅ Phase 4: Rule Conversion

**Status:** ✅ COMPLETED  
**Completed:** January 24, 2026

#### Tasks:

- [x] Analyze existing 11 rules
- [x] Define symbolic facts for Brute Force attacks
  - [x] Map numeric conditions to symbolic facts
  - [x] Define fact derivation rules
- [x] Define symbolic facts for DDoS attacks
- [x] Create v2 rule definitions with CF values
- [x] Seed v2 rules into database

**Deliverables:**

- `scripts/seed_rules_engine.py` (11 symbolic rules)
- 5 Brute Force rules (CF: 0.85-0.92)
- 5 DDoS rules (CF: 0.83-0.95)
- 1 APT detection rule (CF: 0.78)

- `scripts/convert_rules_v2.py` - Rule conversion script
- `scripts/seed_v2_rules.py` - Seed v2 rules

**Rule Conversion Example:**

```
OLD:
  conditions: {"failed_attempts": ">= 5", "time_window": "<= 300"}

NEW:
  conditions: {"high_failed_attempts", "short_timespan"}
  conclusion: "brute_force_attack"
  cf: 0.85
```

---

### ✅ Phase 5: Service Layer Updates

**Status:** ✅ COMPLETED  
**Completed:** January 24, 2026

#### Tasks:

- [x] Replace `InferenceEngine.analyze_alert()` calls
- [x] Update `AlertService` to use v2 engine
- [x] Update alert routes to use new service
- [x] Update dashboard routes

**Files Modified:**

- `app/services/alert_service.py` - Added `analyze_and_create_incident()`
- `app/routes/alert_routes.py` - Removed old engine calls
- `app/routes/dashboard_routes.py` - Updated to use new service

---

### ✅ Phase 6: Route & Form Updates

**Status:** ✅ COMPLETED  
**Completed:** January 24, 2026

#### Tasks:

- [x] Update `RuleForm` for v2 fields
  - [x] Add CF input (0.0-1.0 range)
  - [x] Add conclusion input
  - [x] Add symbolic conditions editor
- [x] Update rule CRUD routes
  - [x] Create route - handle v2 format
  - [x] Edit route - handle v2 format

**Files Modified:**

- `app/forms/rule_forms.py` - Updated for symbolic conditions & CF
- `app/routes/rule_routes.py` - Updated create/edit routes

---

### 🔄 Phase 7: Template Updates

**Status:** ⏳ PENDING  
**Target:** January 27, 2026

#### Tasks:

- [ ] Update rule templates
  - [ ] `rules/create.html` - Add CF and conclusion fields
  - [ ] `rules/edit.html` - Add CF and conclusion fields
  - [ ] `rules/detail.html` - Display CF and symbolic conditions
- [ ] Update alert/incident templates
  - [ ] `alerts/detail.html` - Show trace data
  - [ ] `incidents/detail.html` - Show conclusions with CFs
  - [ ] Add explanation UI (why/why not buttons)

**Files to Modify:**

- `app/templates/rules/create.html`
- `app/templates/rules/edit.html`
- `app/templates/rules/detail.html`
- `app/templates/alerts/detail.html`
- `app/templates/incidents/detail.html`

---

### 🔄 Phase 8: Testing & Validation

**Status:** ⏳ PENDING  
**Target:** January 28, 2026

#### Tasks:

- [ ] Update existing tests for v2 engine
- [ ] Test CF combination accuracy
- [ ] Test trace recording
- [ ] Test explain() functionality
- [ ] Integration tests with real alert data
- [ ] Performance testing
- [ ] Edge case testing
  - [ ] No matching rules
  - [ ] All rules skipped
  - [ ] Multiple conclusions
  - [ ] CF clamping (ensure 0.0-1.0)

**Files to Update:**

- `app/tests/test_models.py`
- `app/tests/test_services.py`
- `app/tests/test_attack_simulations.py`
- `app/tests/test_inference_v2.py` (new)

---

### 🔄 Phase 9: Documentation Updates

**Status:** ⏳ PENDING  
**Target:** January 29, 2026

#### Tasks:

- [ ] Update README.md
  - [ ] Document v2 inference engine
  - [ ] Update confidence scoring explanation
  - [ ] Document CF combination formula
- [ ] Update code comments
- [ ] Create API documentation for explain()
- [ ] Update user guide
- [ ] Add migration notes for existing users

**Files to Update:**

- `README.md`
- `DEPLOYMENT.md`
- Create `V2_FEATURES.md`

---

### 🔄 Phase 10: Cleanup & Optimization

**Status:** ⏳ PENDING  
**Target:** January 30, 2026

#### Tasks:

- [ ] Remove old inference_engine.py
- [ ] Remove unused fields from models
- [ ] Database cleanup
- [ ] Code optimization
- [ ] Performance profiling
- [ ] Final security audit

---

## Key Changes Summary

### Data Model Changes

| Model    | Old Field                 | New Field                       | Change                     |
| -------- | ------------------------- | ------------------------------- | -------------------------- |
| Rule     | `conditions: JSON`        | `symbolic_conditions: Set[str]` | Simplified to symbols      |
| Rule     | `actions: JSON`           | `conclusion: String`            | Single conclusion          |
| Rule     | `severity_score: 1-10`    | `cf: 0.0-1.0`                   | Certainty factor           |
| Rule     | `match_threshold: 0.7`    | Removed                         | Always 100% match required |
| Incident | `confidence_score: 0-100` | `final_cf: 0.0-1.0`             | Changed to CF              |
| Incident | `explanation: Text`       | `trace: JSON`                   | Structured trace           |
| Incident | `matched_rules: [ids]`    | `conclusions: {concl→CF}`       | Multiple conclusions       |

### Logic Changes

| Aspect         | Old                     | New                      |
| -------------- | ----------------------- | ------------------------ |
| Matching       | Partial (70% threshold) | All-or-nothing (100%)    |
| Confidence     | Multi-factor heuristic  | CF combination formula   |
| Multiple Rules | First match wins        | All contribute via CF    |
| Trace          | Text explanation        | Structured fired/skipped |
| Explanation    | Generated text          | Why/Why not from trace   |

---

## Rollback Plan

If issues occur during migration:

1. **Database**: Keep old schema columns until v2 is stable
2. **Code**: Use git branches for easy revert
3. **Rules**: Maintain old rule format in parallel
4. **Testing**: Extensive testing before each phase

---

## Risk Assessment

| Risk                       | Probability | Impact | Mitigation                        |
| -------------------------- | ----------- | ------ | --------------------------------- |
| Data loss during migration | Low         | High   | Backup database before each phase |
| CF formula bugs            | Medium      | Medium | Extensive unit tests              |
| Performance degradation    | Low         | Medium | Profiling and optimization        |
| User confusion             | Medium      | Low    | Clear documentation               |

---

## Success Metrics

- [ ] All 11 rules converted to v2 format
- [ ] CF combination accurate to 0.001
- [ ] Trace captures all fired/skipped rules
- [ ] Explain() works for all conclusions
- [ ] Alert analysis time < 1 second
- [ ] All tests passing (100% coverage)
- [ ] Zero data loss

---

## Progress Tracking

**Current Phase:** Phase 7 - Template Updates  
**Overall Progress:** ██████░░░░ 60%

### Completed Phases: 6 / 10

### Estimated Completion: January 30, 2026

---

## Notes & Decisions

### January 24, 2026

- ✅ Decision: Complete migration (not parallel implementation)
- ✅ Created migration milestone file
- ✅ Phase 2 Complete: Core engine implementation
  - Replaced `inference_engine.py` with forward-chaining CF logic
  - Created `fact_extractor.py` with symbolic fact derivation
  - Removed unnecessary comments from code
  - No "v2" in file names (clean naming convention)
- ✅ Phase 3 Complete: Database schema migration
  - Updated Rule model with symbolic_conditions, conclusion, cf
  - Updated Incident model with conclusions, trace, final_cf
  - Maintained backward compatibility
  - Database recreated with new schema
- ✅ Phase 4 Complete: Rule conversion
  - Created `seed_rules_engine.py` with 11 symbolic rules
  - All rules seeded with appropriate CF values
  - Symbolic conditions mapped to fact_extractor thresholds
- ✅ Phase 5 Complete: Service layer updates
  - Updated AlertService with `analyze_and_create_incident()` method
  - Removed all old InferenceEngine.analyze_alert() calls
  - Updated alert and dashboard routes to use new engine

---

## Next Steps

1. ✅ Create milestone file
2. ✅ Implement inference_engine.py
3. ✅ Implement fact_extractor.py
4. ✅ Update database schema
5. ✅ Convert rules to symbolic format
6. ✅ Update service layer (alert_service.py)
7. 🔄 Update routes and forms
8. ⏳ Update templates
9. ⏳ Create tests

---

**Last Updated:** January 24, 2026  
**Updated By:** AI Assistant  
**Next Review:** End of Phase 2
