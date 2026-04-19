from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def generate_synthetic_dataset(n_samples: int = 500, seed: int = 42) -> pd.DataFrame:
    """Generate synthetic network traffic dataset for testing."""
    import random
    random.seed(seed)
    
    attack_types = [
        "DoS_syn_flood source=192.168.1.100 dest=10.0.0.1 port=80 protocol=tcp",
        "Brute_force_ssh source=203.0.113.45 dest=10.0.0.5 port=22 attempts=1000",
        "Malware_detection payload=suspicious_binary size=5MB hash=abc123",
        "SQL_injection input=admin_form query_length=500 encoding=utf8",
        "Port_scan source=198.51.100.10 dest=10.0.0.0/24 ports=1-65535 scan_type=syn",
    ]
    
    normal_types = [
        "HTTP_request source=192.168.0.50 dest=93.184.216.34 port=80 status=200",
        "HTTPS_connection source=192.168.0.51 dest=142.250.185.46 port=443 tls=1.3",
        "DNS_query source=192.168.0.52 dest=8.8.8.8 domain=example.com type=A",
        "FTP_transfer source=192.168.0.53 dest=10.0.0.20 port=21 size=1024",
        "Mail_smtp source=192.168.0.54 dest=10.0.0.30 port=25 status=250",
    ]
    
    texts = []
    labels = []
    
    for i in range(n_samples):
        if i % 5 < 2:  # 40% attacks
            text = random.choice(attack_types)
            label = "attack"
        else:  # 60% normal
            text = random.choice(normal_types)
            label = "normal"
        
        texts.append(text)
        labels.append(label)
    
    return pd.DataFrame({"text": texts, "label": labels})


def save_synthetic_dataset(output_path: Path, n_samples: int = 500) -> None:
    """Generate and save synthetic dataset to CSV."""
    df = generate_synthetic_dataset(n_samples=n_samples)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Dataset synthétique créé: {output_path}")
    print(f"  Total samples: {len(df)}")
    print(f"  Normal: {(df['label']=='normal').sum()}")
    print(f"  Attack: {(df['label']=='attack').sum()}")
