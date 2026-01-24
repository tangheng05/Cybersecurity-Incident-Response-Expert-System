"""
Forward-Chaining Inference Engine with Certainty Factors
"""

from typing import Set, Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, field
import json


@dataclass
class RuleModel:
    id: str
    conditions: Set[str]
    conclusion: str
    cf: float
    explanation_text: str = ""
    
    def __post_init__(self):
        if not 0.0 <= self.cf <= 1.0:
            raise ValueError(f"CF must be in [0.0, 1.0], got {self.cf}")
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'conditions': list(self.conditions),
            'conclusion': self.conclusion,
            'cf': self.cf,
            'explanation_text': self.explanation_text
        }


@dataclass
class ConclusionRecord:
    conclusion: str
    final_cf: float
    supporting_rules: List[Dict[str, Any]] = field(default_factory=list)
    used_facts: Set[str] = field(default_factory=set)
    
    def to_dict(self) -> Dict:
        return {
            'conclusion': self.conclusion,
            'final_cf': self.final_cf,
            'supporting_rules': self.supporting_rules,
            'used_facts': list(self.used_facts)
        }


@dataclass
class Trace:
    fired_rules: List[Dict[str, Any]] = field(default_factory=list)
    skipped_rules: List[Dict[str, Any]] = field(default_factory=list)
    conclusions: Dict[str, ConclusionRecord] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            'fired_rules': self.fired_rules,
            'skipped_rules': self.skipped_rules,
            'conclusions': {k: v.to_dict() for k, v in self.conclusions.items()}
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


class InferenceEngine:
    
    @staticmethod
    def combine_cfs(cf_old: float, cf_new: float) -> float:
        result = cf_old + cf_new * (1.0 - cf_old)
        return max(0.0, min(1.0, result))
    
    @staticmethod
    def infer(facts: Set[str], rules: List[RuleModel]) -> Tuple[Dict[str, float], Trace]:
        trace = Trace()
        conclusions: Dict[str, float] = {}
        support_map: Dict[str, List[Dict]] = {}
        
        for rule in rules:
            missing_conditions = rule.conditions - facts
            
            if not missing_conditions:
                trace.fired_rules.append({
                    'rule_id': rule.id,
                    'matched_conditions': list(rule.conditions),
                    'cf': rule.cf,
                    'conclusion': rule.conclusion,
                    'explanation': rule.explanation_text
                })
                
                if rule.conclusion in conclusions:
                    old_cf = conclusions[rule.conclusion]
                    new_cf = InferenceEngine.combine_cfs(old_cf, rule.cf)
                    conclusions[rule.conclusion] = new_cf
                    
                    support_map[rule.conclusion].append({
                        'rule_id': rule.id,
                        'cf': rule.cf,
                        'matched_conditions': list(rule.conditions),
                        'explanation': rule.explanation_text
                    })
                else:
                    conclusions[rule.conclusion] = rule.cf
                    support_map[rule.conclusion] = [{
                        'rule_id': rule.id,
                        'cf': rule.cf,
                        'matched_conditions': list(rule.conditions),
                        'explanation': rule.explanation_text
                    }]
            else:
                trace.skipped_rules.append({
                    'rule_id': rule.id,
                    'missing_conditions': list(missing_conditions),
                    'conclusion': rule.conclusion,
                    'explanation': rule.explanation_text
                })
        
        for conclusion, final_cf in conclusions.items():
            used_facts: Set[str] = set()
            for support in support_map[conclusion]:
                used_facts.update(support['matched_conditions'])
            
            trace.conclusions[conclusion] = ConclusionRecord(
                conclusion=conclusion,
                final_cf=final_cf,
                supporting_rules=support_map[conclusion],
                used_facts=used_facts
            )
        
        return conclusions, trace
    
    @staticmethod
    def explain(conclusion_id: str, trace: Trace) -> Dict[str, Any]:
        if conclusion_id in trace.conclusions:
            record = trace.conclusions[conclusion_id]
            
            return {
                'type': 'why',
                'conclusion': record.conclusion,
                'final_cf': record.final_cf,
                'supporting_rules': record.supporting_rules,
                'used_facts': list(record.used_facts),
                'stepwise_combination': InferenceEngine._compute_stepwise_cf(record.supporting_rules),
                'summary': InferenceEngine._generate_why_summary(record)
            }
        else:
            candidate_rules = [r for r in trace.skipped_rules if r['conclusion'] == conclusion_id]
            
            return {
                'type': 'why_not',
                'conclusion': conclusion_id,
                'candidate_rules': candidate_rules,
                'summary': InferenceEngine._generate_why_not_summary(conclusion_id, candidate_rules)
            }
    
    @staticmethod
    def _compute_stepwise_cf(supporting_rules: List[Dict]) -> List[Dict]:
        steps = []
        cf_running = 0.0
        
        for idx, rule in enumerate(supporting_rules):
            cf_before = cf_running
            cf_after = InferenceEngine.combine_cfs(cf_running, rule['cf'])
            
            steps.append({
                'step': idx + 1,
                'rule_id': rule['rule_id'],
                'rule_cf': rule['cf'],
                'cf_before': round(cf_before, 4),
                'cf_after': round(cf_after, 4),
                'contribution': round(cf_after - cf_before, 4),
                'explanation': rule.get('explanation', '')
            })
            
            cf_running = cf_after
        
        return steps
    
    @staticmethod
    def _generate_why_summary(record: ConclusionRecord) -> str:
        num_rules = len(record.supporting_rules)
        cf_percent = int(record.final_cf * 100)
        
        summary = f"Conclusion '{record.conclusion}' reached with {cf_percent}% certainty. "
        summary += f"Supported by {num_rules} rule(s) using {len(record.used_facts)} fact(s)."
        
        return summary
    
    @staticmethod
    def _generate_why_not_summary(conclusion_id: str, candidate_rules: List[Dict]) -> str:
        if not candidate_rules:
            return f"Conclusion '{conclusion_id}' was not reached because no rules support it."
        
        num_candidates = len(candidate_rules)
        all_missing = set()
        for rule in candidate_rules:
            all_missing.update(rule['missing_conditions'])
        
        summary = f"Conclusion '{conclusion_id}' was not reached. "
        summary += f"{num_candidates} rule(s) could have supported it, "
        summary += f"but {len(all_missing)} required fact(s) were missing: "
        summary += f"{', '.join(sorted(all_missing))}"
        
        return summary
    
    @staticmethod
    def load_rules_from_db(db_rules) -> List[RuleModel]:
        rules = []
        
        for db_rule in db_rules:
            conditions = set()
            if hasattr(db_rule, 'symbolic_conditions') and db_rule.symbolic_conditions:
                conditions = set(db_rule.symbolic_conditions)
            
            cf = db_rule.cf if hasattr(db_rule, 'cf') and db_rule.cf else 0.5
            conclusion = db_rule.conclusion if hasattr(db_rule, 'conclusion') else "unknown"
            
            rule = RuleModel(
                id=str(db_rule.id),
                conditions=conditions,
                conclusion=conclusion,
                cf=cf,
                explanation_text=db_rule.name if hasattr(db_rule, 'name') else ""
            )
            
            rules.append(rule)
        
        return rules


def print_trace(trace: Trace) -> None:
    print("\n" + "="*60)
    print("INFERENCE TRACE")
    print("="*60)
    
    print(f"\nFired Rules: {len(trace.fired_rules)}")
    for rule in trace.fired_rules:
        print(f"  ✓ {rule['rule_id']}: {rule['conclusion']} (CF={rule['cf']})")
        print(f"    Conditions: {', '.join(rule['matched_conditions'])}")
    
    print(f"\nSkipped Rules: {len(trace.skipped_rules)}")
    for rule in trace.skipped_rules:
        print(f"  ✗ {rule['rule_id']}: {rule['conclusion']}")
        print(f"    Missing: {', '.join(rule['missing_conditions'])}")
    
    print(f"\nConclusions: {len(trace.conclusions)}")
    for concl_id, record in trace.conclusions.items():
        cf_percent = int(record.final_cf * 100)
        print(f"  → {concl_id}: {cf_percent}% certainty")
        print(f"    Rules: {len(record.supporting_rules)}")
        print(f"    Facts: {', '.join(sorted(record.used_facts))}")
    
    print("="*60 + "\n")


def validate_cf_combination() -> bool:
    engine = InferenceEngine()
    
    cf1, cf2, cf3 = 0.7, 0.6, 0.5
    
    result1 = engine.combine_cfs(engine.combine_cfs(cf1, cf2), cf3)
    result2 = engine.combine_cfs(cf1, engine.combine_cfs(cf2, cf3))
    
    tolerance = 1e-10
    is_associative = abs(result1 - result2) < tolerance
    
    result_high = engine.combine_cfs(0.9, 0.9)
    is_bounded = 0.0 <= result_high <= 1.0
    
    cf_base = 0.5
    cf_add = 0.3
    result = engine.combine_cfs(cf_base, cf_add)
    is_monotonic = result >= cf_base
    
    return is_associative and is_bounded and is_monotonic
