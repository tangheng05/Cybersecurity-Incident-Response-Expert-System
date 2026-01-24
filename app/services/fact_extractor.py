"""
Fact Extractor - Converts Alert data into symbolic facts
"""

from typing import Set, Dict, Any
from app.models.alert import Alert


class FactExtractor:
    

    THRESHOLDS = {
        # Brute Force Attack thresholds
        'failed_attempts_high': 5,
        'failed_attempts_very_high': 10,
        'failed_attempts_extreme': 20,
        'time_window_short': 300,  # 5 minutes
        'time_window_very_short': 120,
        'requests_per_second_high': 100,
        'requests_per_second_very_high': 500,
        'requests_per_second_extreme': 1000,
        'bandwidth_high_mbps': 100,
        'bandwidth_very_high_mbps': 500,
        'connection_count_high': 100,
        'connection_count_very_high': 500,
    }
    
    @staticmethod
    def extract_facts(alert: Alert) -> Set[str]:
        facts = set()
        raw_data = alert.raw_data or {}
        facts.update(FactExtractor._extract_numeric_facts(raw_data))
        facts.update(FactExtractor._extract_categorical_facts(raw_data))
        facts.update(FactExtractor._extract_ip_facts(alert))
        facts.update(FactExtractor._extract_severity_facts(alert))
        facts.update(FactExtractor._extract_temporal_facts(raw_data))
        facts.update(FactExtractor._derive_compound_facts(facts, raw_data))
        
        return facts
    
    @staticmethod
    def _extract_numeric_facts(raw_data: Dict[str, Any]) -> Set[str]:
        facts = set()
        thresholds = FactExtractor.THRESHOLDS
        
        failed_attempts = raw_data.get('failed_attempts', 0)
        if failed_attempts >= thresholds['failed_attempts_extreme']:
            facts.add('extreme_failed_attempts')
            facts.add('very_high_failed_attempts')
            facts.add('high_failed_attempts')
        elif failed_attempts >= thresholds['failed_attempts_very_high']:
            facts.add('very_high_failed_attempts')
            facts.add('high_failed_attempts')
        elif failed_attempts >= thresholds['failed_attempts_high']:
            facts.add('high_failed_attempts')
        
        time_window = raw_data.get('time_window', 999999)
        if time_window <= thresholds['time_window_very_short']:
            facts.add('very_short_timespan')
            facts.add('short_timespan')
        elif time_window <= thresholds['time_window_short']:
            facts.add('short_timespan')
        
        rps = raw_data.get('requests_per_second', 0)
        if rps >= thresholds['requests_per_second_extreme']:
            facts.add('extreme_traffic_rate')
            facts.add('very_high_traffic_rate')
            facts.add('high_traffic_rate')
        elif rps >= thresholds['requests_per_second_very_high']:
            facts.add('very_high_traffic_rate')
            facts.add('high_traffic_rate')
        elif rps >= thresholds['requests_per_second_high']:
            facts.add('high_traffic_rate')
        
        bandwidth = raw_data.get('bandwidth_mbps', 0)
        if bandwidth >= thresholds['bandwidth_very_high_mbps']:
            facts.add('very_high_bandwidth')
            facts.add('high_bandwidth')
        elif bandwidth >= thresholds['bandwidth_high_mbps']:
            facts.add('high_bandwidth')
        
        connections = raw_data.get('connection_count', 0)
        if connections >= thresholds['connection_count_very_high']:
            facts.add('very_high_connections')
            facts.add('high_connections')
        elif connections >= thresholds['connection_count_high']:
            facts.add('high_connections')
        
        return facts
    
    @staticmethod
    def _extract_categorical_facts(raw_data: Dict[str, Any]) -> Set[str]:
        facts = set()
        
        service = raw_data.get('target_service', '').lower()
        if service:
            facts.add(f'{service}_service')
            
            if service in ['ssh', 'rdp', 'telnet']:
                facts.add('remote_access_service')
            elif service in ['http', 'https']:
                facts.add('web_service')
            elif service in ['ftp', 'sftp']:
                facts.add('file_transfer_service')
            elif service in ['smtp', 'pop3', 'imap']:
                facts.add('email_service')
        
        username = raw_data.get('target_username', '').lower()
        if username:
            if username in ['admin', 'root', 'administrator']:
                facts.add('admin_target')
                facts.add('high_value_target')
            elif username in ['guest', 'test', 'demo']:
                facts.add('low_privilege_target')
        
        protocol = raw_data.get('protocol', '').lower()
        if protocol:
            facts.add(f'{protocol}_protocol')
        
        attack_type = raw_data.get('attack_type', '').lower()
        if attack_type:
            facts.add(f'suspected_{attack_type}')
        
        source_country = raw_data.get('source_country', '').lower()
        if source_country:
            facts.add(f'source_country_{source_country}')
            
            high_risk_countries = ['cn', 'ru', 'kp']
            if source_country in high_risk_countries:
                facts.add('high_risk_country')
        
        return facts
    
    @staticmethod
    def _extract_ip_facts(alert: Alert) -> Set[str]:
        facts = set()
        
        if alert.source_ip:
            facts.add('has_source_ip')
            
            if FactExtractor._is_private_ip(alert.source_ip):
                facts.add('internal_source')
            else:
                facts.add('external_source')
        
        if alert.destination_ip:
            facts.add('has_destination_ip')
            
            if FactExtractor._is_private_ip(alert.destination_ip):
                facts.add('internal_target')
            else:
                facts.add('external_target')
        return facts
    
    @staticmethod
    def _extract_severity_facts(alert: Alert) -> Set[str]:
        """Extract facts from alert severity"""
        facts = set()
        
        severity = alert.severity.lower() if alert.severity else 'medium'
        facts.add(f'{severity}_severity')
        
        if severity in ['high', 'critical']:
            facts.add('elevated_severity')
        
        return facts
    
    @staticmethod
    def _extract_temporal_facts(raw_data: Dict[str, Any]) -> Set[str]:
        facts = set()
        
        duration = raw_data.get('attack_duration_seconds', 0)
        if duration > 3600:
            facts.add('sustained_attack')
        elif duration > 600:
            facts.add('prolonged_attack')
        elif duration > 0:
            facts.add('brief_attack')
        
        if raw_data.get('is_repeat_offender', False):
            facts.add('repeat_offender')
            facts.add('known_attacker')
        
        return facts
    
    @staticmethod
    def _derive_compound_facts(facts: Set[str], raw_data: Dict[str, Any]) -> Set[str]:
        derived = set()
        
        if 'high_failed_attempts' in facts and 'short_timespan' in facts:
            derived.add('rapid_brute_force_pattern')
        
        if 'very_high_failed_attempts' in facts and 'very_short_timespan' in facts:
            derived.add('aggressive_brute_force_pattern')
        
        if 'admin_target' in facts and 'high_failed_attempts' in facts:
            derived.add('targeted_admin_attack')
        
        if 'ssh_service' in facts and 'high_failed_attempts' in facts:
            derived.add('ssh_brute_force_pattern')
        
        # DDoS patterns
        if 'high_traffic_rate' in facts and 'high_connections' in facts:
            derived.add('volumetric_attack_pattern')
        
        if 'very_high_traffic_rate' in facts and 'very_high_connections' in facts:
            derived.add('severe_ddos_pattern')
        
        if 'high_bandwidth' in facts and 'high_traffic_rate' in facts:
            derived.add('bandwidth_exhaustion_pattern')
        
        if 'external_source' in facts and 'high_traffic_rate' in facts:
            derived.add('external_flood_attack')
        
        if 'high_failed_attempts' in facts and 'repeat_offender' in facts:
            derived.add('credential_stuffing_pattern')
        
        if 'sustained_attack' in facts and 'high_value_target' in facts:
            derived.add('apt_pattern')
        
        return derived
    def _is_private_ip(ip: str) -> bool:
    
    @staticmethod
    def _is_private_ip(ip: str) -> bool:
        try:
            parts = ip.split('.')
            if len(parts) != 4:
                return False
            
            first = int(parts[0])
            second = int(parts[1])10:
                return True
            
            # 172.16.0.0/12
            if first == 172 and 16 <= second <= 31:
                return True
            
            if first == 192 and second == 168:
                return True
            
            # Loopback
            if first == 127:
                return True
            
            return False
    return {
            'high_fai
    def get_fact_descriptions() -> Dict[str, str]:
        """
        Useful for UI displed_attempts': 'Failed login attempts ≥ 5',
            'very_high_failed_attempts': 'Failed login attempts ≥ 10',
            'extreme_failed_attempts': 'Failed login attempts ≥ 20',
            
            # Timespan
            'short_timespan': 'Attack window ≤ 5 minutes',
            'very_short_timespan': 'Attack window ≤ 2 minutes',
            
            # Traffic rate
            'high_traffic_rate': 'Requests/second ≥ 100',
            'very_high_traffic_rate': 'Requests/second ≥ 500',
            'extreme_traffic_rate': 'Requests/second ≥ 1000',
            'very_high_bandwidth': 'Bandwidth usage ≥ 500 Mbps',
            
            # Connections
            'higtions': 'Active connections ≥ 500',
            
            'ssh_service': 'Target service: SSH',
            'http_service': 'Target service: HTTP',
            'https_service': 'Target service: HTTPS',
            'rdp_service': 'Target service: RDP',
            'remote_access_service': 'Remote access protocol targeted',
            'web_service': 'Web service targeted',
            
            'admin_target': 'Administrator account targeted',
            'high_value_target': 'High-value account targeted',
            
            'elevated_severity': 'Alert severity is high or
            ritical',
            'high_severity': 'High severity alert',
            'critical_severity': 'Critical severity alert',et
            'external_source': 'Attack from external IP',
            'internal_source': 'Attack from internal IP',
            
            'rapid_bru'has_source_ip': 'Source IP identified',
            te_force_pattern': 'High login failures in short time',
            'aggressive_brute_force_pattern': 'Very aggressive brute force attempt',
            'ssh_brute_force_pattern': 'SSH-specific brute force',
            'volumetric_attack_pattern': 'High traffic + high connections',
            'severe_ddos_pattern': 'Extreme DDoS indicators',


def print_facts(alert: Alert) -> None:
    facts = FactExtractor.extract_facts(alert)
    descriptions = Fac
def print_facts(alert: Alert) -> None:
    """Pretty-print extracted facts for debugging
    print(f"{'='*60}")
    print(f"Source IP: {alert.source_ip}")
    print(f"Severity: {alert.severity}")
    for fact in sorted(facts):
        desc = descriptions.get(fact, 'No description')
        print(f"  ✓ {fact}: {desc}")
    
    print(f"{'='*60}\n")")
    print(f"\nFacts ({len(facts)}):")
        desc = descriptions.get(fact, 'No description')
        print(f"  ✓ {fact}: {desc}")
    
    print(f"{'='*60}\n")
def print_facts(alert: Alert) -> None: