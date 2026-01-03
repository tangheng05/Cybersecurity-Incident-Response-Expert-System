"""
Inference Engine for Cybersecurity Incident Response Expert System
Analyzes alerts against security rules and generates recommendations
"""
import json
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Any
from app.models.rule import Rule
from app.models.alert import Alert
from app.models.attack_type import AttackType


class InferenceEngine:
    """Core reasoning engine for analyzing security alerts"""
    
    @staticmethod
    def analyze_alert(alert: Alert, rules: List[Rule] = None) -> Dict[str, Any]:
        """
        Main analysis function - analyzes an alert against all active rules
        
        Args:
            alert: Alert object to analyze
            rules: Optional list of rules (if None, fetches all active rules)
            
        Returns:
            dict with keys: matched_rules, recommended_actions, confidence_score, 
                           explanation, attack_type_id
        """
        from app.services.rule_service import RuleService
        
        if rules is None:
            rules = RuleService.get_all(active_only=True)
        
        # Match rules against alert
        matched_rules = InferenceEngine.match_rules(alert, rules)
        
        if not matched_rules:
            return {
                'matched_rules': [],
                'recommended_actions': ['monitor', 'log_for_analysis'],
                'confidence_score': 0,
                'explanation': 'No matching rules found. Alert logged for manual review.',
                'attack_type_id': None
            }
        
        # Prioritize and select actions
        actions = InferenceEngine.prioritize_actions(matched_rules)
        
        # Calculate confidence score
        confidence = InferenceEngine.calculate_confidence(matched_rules, alert)
        
        # Generate explanation
        explanation = InferenceEngine.generate_explanation(matched_rules, alert)
        
        # Determine primary attack type
        attack_type_id = matched_rules[0]['rule'].attack_type_id if matched_rules else None
        
        return {
            'matched_rules': [r['rule'].id for r in matched_rules],
            'recommended_actions': actions,
            'confidence_score': confidence,
            'explanation': explanation,
            'attack_type_id': attack_type_id
        }
    
    @staticmethod
    def match_rules(alert: Alert, rules: List[Rule]) -> List[Dict[str, Any]]:
        """
        Pattern matching - finds all rules that match the alert
        
        Returns:
            List of dicts with 'rule' and 'match_score' keys, sorted by priority
        """
        matched = []
        
        for rule in rules:
            if not rule.is_active:
                continue
            
            # Evaluate rule conditions against alert
            is_match, match_score = InferenceEngine.evaluate_conditions(alert, rule)
            
            if is_match:
                matched.append({
                    'rule': rule,
                    'match_score': match_score
                })
        
        # Sort by priority (high=3, medium=2, low=1) then severity_score
        priority_map = {'high': 3, 'medium': 2, 'low': 1}
        matched.sort(
            key=lambda x: (
                priority_map.get(x['rule'].priority, 0),
                x['rule'].severity_score,
                x['match_score']
            ),
            reverse=True
        )
        
        return matched
    
    @staticmethod
    def evaluate_conditions(alert: Alert, rule: Rule) -> Tuple[bool, float]:
        """
        Evaluates if alert data matches rule conditions
        
        Returns:
            (is_match: bool, match_score: float 0-1)
        """
        conditions = rule.conditions
        raw_data = alert.raw_data or {}
        
        matched_conditions = 0
        total_conditions = len(conditions)
        
        if total_conditions == 0:
            return False, 0.0
        
        for key, condition_value in conditions.items():
            alert_value = raw_data.get(key)
            
            # Handle different condition types
            if isinstance(condition_value, str) and any(op in condition_value for op in ['>=', '<=', '>', '<', '==']):
                # Numeric comparison
                if InferenceEngine._evaluate_numeric_condition(alert_value, condition_value):
                    matched_conditions += 1
            elif isinstance(condition_value, bool):
                # Boolean check
                if alert_value == condition_value:
                    matched_conditions += 1
            elif isinstance(condition_value, str):
                # String match or IP address
                if str(alert_value) == condition_value or alert_value == condition_value:
                    matched_conditions += 1
            elif isinstance(condition_value, list):
                # Value in list
                if alert_value in condition_value:
                    matched_conditions += 1
            else:
                # Direct equality
                if alert_value == condition_value:
                    matched_conditions += 1
        
        match_score = matched_conditions / total_conditions
        is_match = match_score >= 0.7  # 70% threshold for rule match
        
        return is_match, match_score
    
    @staticmethod
    def _evaluate_numeric_condition(value: Any, condition: str) -> bool:
        """Evaluates numeric conditions like '>= 5', '< 100'"""
        try:
            # Parse condition string
            if '>=' in condition:
                threshold = float(condition.split('>=')[1].strip())
                return float(value) >= threshold
            elif '<=' in condition:
                threshold = float(condition.split('<=')[1].strip())
                return float(value) <= threshold
            elif '>' in condition:
                threshold = float(condition.split('>')[1].strip())
                return float(value) > threshold
            elif '<' in condition:
                threshold = float(condition.split('<')[1].strip())
                return float(value) < threshold
            elif '==' in condition:
                threshold = float(condition.split('==')[1].strip())
                return float(value) == threshold
        except (ValueError, TypeError, AttributeError):
            return False
        
        return False
    
    @staticmethod
    def prioritize_actions(matched_rules: List[Dict[str, Any]]) -> List[str]:
        """
        Combines and prioritizes actions from multiple matched rules
        
        Returns:
            List of unique action strings, ordered by priority
        """
        action_priority = {
            'block_ip': 10,
            'block_country': 9,
            'rate_limit': 8,
            'alert_admin': 7,
            'quarantine_traffic': 6,
            'enable_captcha': 5,
            'log_incident': 4,
            'monitor': 3,
            'investigate': 2,
            'notify_team': 1
        }
        
        actions_set = set()
        
        for match in matched_rules:
            rule_actions = match['rule'].actions
            if isinstance(rule_actions, list):
                actions_set.update(rule_actions)
        
        # Sort actions by priority
        sorted_actions = sorted(
            actions_set,
            key=lambda a: action_priority.get(a, 0),
            reverse=True
        )
        
        return sorted_actions
    
    @staticmethod
    def calculate_confidence(matched_rules: List[Dict[str, Any]], alert: Alert) -> int:
        """
        Calculates confidence score (0-100) based on:
        - Number of matching rules
        - Match scores
        - Rule priority levels
        - Alert severity
        """
        if not matched_rules:
            return 0
        
        # Base score from number of matches
        num_matches = len(matched_rules)
        base_score = min(40, num_matches * 10)
        
        # Average match score contribution (0-30 points)
        avg_match_score = sum(m['match_score'] for m in matched_rules) / num_matches
        match_contribution = int(avg_match_score * 30)
        
        # Priority contribution (0-20 points)
        priority_map = {'high': 20, 'medium': 15, 'low': 10}
        top_priority = matched_rules[0]['rule'].priority if matched_rules else 'low'
        priority_contribution = priority_map.get(top_priority, 10)
        
        # Severity contribution (0-10 points)
        severity_map = {'critical': 10, 'high': 8, 'medium': 5, 'low': 2}
        severity_contribution = severity_map.get(alert.severity, 5)
        
        total_score = base_score + match_contribution + priority_contribution + severity_contribution
        
        return min(100, total_score)
    
    @staticmethod
    def generate_explanation(matched_rules: List[Dict[str, Any]], alert: Alert) -> str:
        """
        Generates human-readable explanation of the decision
        """
        if not matched_rules:
            return "No matching security rules found for this alert."
        
        explanation_parts = []
        
        # Summary
        num_rules = len(matched_rules)
        top_rule = matched_rules[0]['rule']
        
        explanation_parts.append(
            f"Alert analyzed and matched {num_rules} security rule(s). "
            f"Primary match: '{top_rule.name}' (Priority: {top_rule.priority.upper()}, "
            f"Severity: {top_rule.severity_score}/10)."
        )
        
        # Attack type
        if top_rule.attack_type:
            explanation_parts.append(
                f"\n\nDetected Attack Type: {top_rule.attack_type.name.replace('_', ' ').title()} - "
                f"{top_rule.attack_type.description}"
            )
        
        # Matched rules details
        if num_rules > 1:
            explanation_parts.append("\n\nMatched Rules:")
            for idx, match in enumerate(matched_rules[:3], 1):  # Show top 3
                rule = match['rule']
                score = match['match_score']
                explanation_parts.append(
                    f"\n{idx}. {rule.name} (Match: {score*100:.0f}%, Severity: {rule.severity_score}/10)"
                )
            
            if num_rules > 3:
                explanation_parts.append(f"\n... and {num_rules - 3} more rule(s)")
        
        # Alert details
        explanation_parts.append(f"\n\nAlert Details:")
        explanation_parts.append(f"- Source IP: {alert.source_ip or 'Unknown'}")
        explanation_parts.append(f"- Timestamp: {alert.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        explanation_parts.append(f"- Severity: {alert.severity.upper()}")
        
        return ''.join(explanation_parts)
