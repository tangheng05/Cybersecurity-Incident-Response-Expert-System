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
            
            # Check for SQL injection patterns
            sql_injection_patterns = [
                "'", '"', '--', ';', 'union', 'select', 'drop', 'insert', 'update', 
                'delete', 'exec', 'execute', 'script', '<', '>', 'or 1=1', 'or 1 = 1',
                "' or '", '" or "', 'xp_', 'sp_', 'concat', 'char(', 'declare'
            ]
            if any(pattern in service for pattern in sql_injection_patterns):
                facts.add('sql_injection_pattern')
                facts.add('web_attack')
            
            # Check for XSS patterns
            xss_patterns = ['<script', 'javascript:', 'onerror=', 'onload=', 'onclick=', 
                           '<iframe', '<img', 'alert(', 'document.cookie', 'eval(']
            if any(pattern in service for pattern in xss_patterns):
                facts.add('xss_pattern')
                facts.add('web_attack')
            
            # Check for port scan patterns
            if 'port' in service or 'scan' in service or 'nmap' in service:
                facts.add('port_scan_pattern')
            
            # Check for malware patterns
            malware_patterns = ['.exe', '.dll', '.bat', '.ps1', '.vbs', 'payload', 
                               'trojan', 'ransomware', 'virus', 'worm', 'backdoor']
            if any(pattern in service for pattern in malware_patterns):
                facts.add('malware_pattern')
            
            # Check for phishing patterns
            phishing_patterns = ['login', 'verify', 'account', 'suspended', 'confirm',
                                'password', 'urgent', 'click here', 'update payment']
            if any(pattern in service for pattern in phishing_patterns):
                facts.add('phishing_pattern')
            
            # Check for privilege escalation patterns
            priv_esc_patterns = ['sudo', 'su -', 'runas', 'admin', 'root', 'privilege',
                                'escalate', 'suid', 'chmod', 'chown']
            if any(pattern in service for pattern in priv_esc_patterns):
                facts.add('privilege_escalation_pattern')
            
            # Check for data exfiltration patterns
            exfil_patterns = ['download', 'export', 'backup', 'copy', 'transfer',
                            'ftp', 'scp', 'rsync', 'curl', 'wget']
            if any(pattern in service for pattern in exfil_patterns):
                facts.add('data_exfiltration_pattern')
            
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
        
        # Check for suspicious file access
        if raw_data.get('file_access_count', 0) > 50:
            facts.add('suspicious_file_access')
        
        if raw_data.get('sensitive_data_accessed', False):
            facts.add('sensitive_data_access')
        
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
    
    @staticmethod
    def _is_private_ip(ip: str) -> bool:
        try:
            parts = ip.split('.')
            if len(parts) != 4:
                return False
            
            first = int(parts[0])
            second = int(parts[1])
            
            if first == 10:
                return True
            
            if first == 172 and 16 <= second <= 31:
                return True
            
            if first == 192 and second == 168:
                return True
            
            if first == 127:
                return True
            
            return False
        except:
            return False
    
    @staticmethod
    def get_fact_descriptions() -> Dict[str, str]:
        return {
            'high_failed_attempts': 'Failed login attempts ≥ 5',
            'very_high_failed_attempts': 'Failed login attempts ≥ 10',
            'extreme_failed_attempts': 'Failed login attempts ≥ 20',
            'short_timespan': 'Attack window ≤ 5 minutes',
            'very_short_timespan': 'Attack window ≤ 2 minutes',
            'high_traffic_rate': 'Requests/second ≥ 100',
            'very_high_traffic_rate': 'Requests/second ≥ 500',
            'extreme_traffic_rate': 'Requests/second ≥ 1000',
            'high_bandwidth': 'Bandwidth usage ≥ 100 Mbps',
            'very_high_bandwidth': 'Bandwidth usage ≥ 500 Mbps',
            'high_connections': 'Active connections ≥ 100',
            'very_high_connections': 'Active connections ≥ 500',
            'ssh_service': 'Target service: SSH',
            'http_service': 'Target service: HTTP',
            'https_service': 'Target service: HTTPS',
            'rdp_service': 'Target service: RDP',
            'remote_access_service': 'Remote access protocol targeted',
            'web_service': 'Web service targeted',
            'admin_target': 'Administrator account targeted',
            'high_value_target': 'High-value account targeted',
            'elevated_severity': 'Alert severity is high or critical',
            'high_severity': 'High severity alert',
            'critical_severity': 'Critical severity alert',
            'has_source_ip': 'Source IP identified',
            'external_source': 'Attack from external IP',
            'internal_source': 'Attack from internal IP',
            'rapid_brute_force_pattern': 'High login failures in short time',
            'aggressive_brute_force_pattern': 'Very aggressive brute force attempt',
            'ssh_brute_force_pattern': 'SSH-specific brute force',
            'volumetric_attack_pattern': 'High traffic + high connections',
            'severe_ddos_pattern': 'Extreme DDoS indicators',
            'sustained_attack': 'Attack duration > 1 hour',
            'repeat_offender': 'Known repeat attacker',
            'sql_injection_pattern': 'SQL injection syntax detected',
            'web_attack': 'Web application attack detected',
            'xss_pattern': 'Cross-Site Scripting pattern detected',
            'port_scan_pattern': 'Port scanning activity detected',
            'malware_pattern': 'Malware indicators detected',
            'phishing_pattern': 'Phishing attempt detected',
            'privilege_escalation_pattern': 'Privilege escalation attempt detected',
            'data_exfiltration_pattern': 'Data exfiltration indicators detected',
            'suspicious_file_access': 'Excessive file access detected',
            'sensitive_data_access': 'Sensitive data accessed'
        }


def print_facts(alert: Alert) -> None:
    facts = FactExtractor.extract_facts(alert)
    descriptions = FactExtractor.get_fact_descriptions()
    
    print(f"{'='*60}")
    print(f"Source IP: {alert.source_ip}")
    print(f"Severity: {alert.severity}")
    print(f"\nFacts ({len(facts)}):")
    for fact in sorted(facts):
        desc = descriptions.get(fact, 'No description')
        print(f"  ✓ {fact}: {desc}")
    print(f"{'='*60}\n")