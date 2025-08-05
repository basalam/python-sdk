#!/usr/bin/env python3
"""
Generate type stubs for BasalamClient.
Simple script that extracts method names from service files.
"""
import re
from pathlib import Path


def extract_methods_from_file(file_path):
    """Extract method signatures from a Python service file."""
    methods = []
    try:
        content = file_path.read_text()

        # Find method definitions with multiline support
        lines = content.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Look for method definition start
            if re.match(r'\s*(?:async\s+)?def\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\(', lines[i]):
                method_lines = [lines[i]]
                i += 1

                # Collect method signature lines until we find the closing ):
                paren_count = lines[i - 1].count('(') - lines[i - 1].count(')')
                while i < len(lines) and (paren_count > 0 or not lines[i - 1].rstrip().endswith(':')):
                    if i < len(lines):
                        method_lines.append(lines[i])
                        paren_count += lines[i].count('(') - lines[i].count(')')
                        if lines[i].rstrip().endswith(':'):
                            break
                    i += 1

                # Join and clean the complete signature
                full_signature = ' '.join(line.strip() for line in method_lines)
                full_signature = re.sub(r'\s+', ' ', full_signature)  # Normalize whitespace
                full_signature = full_signature.rstrip(':').strip()

                # Remove inline comments that can break the signature
                full_signature = re.sub(r'#[^,)]*', '', full_signature)
                # Clean up extra commas and whitespace left by comment removal
                full_signature = re.sub(r',\s*,+', ',', full_signature)  # Remove double commas
                full_signature = re.sub(r',(\s*\))', r'\1', full_signature)  # Remove trailing commas before )
                full_signature = re.sub(r'\s+', ' ', full_signature)  # Clean up whitespace

                # Extract method name
                method_match = re.search(r'(?:async\s+)?def\s+([a-zA-Z_][a-zA-Z0-9_]*)', full_signature)
                if method_match:
                    method_name = method_match.group(1)

                    # Filter public methods
                    if not method_name.startswith('_') and method_name != '__init__':
                        # Clean up signature: remove self parameter
                        clean_signature = re.sub(r'\(\s*self\s*,?\s*', '(', full_signature)
                        clean_signature = re.sub(r'\(\s*\)', '()', clean_signature)
                        methods.append((method_name, clean_signature))
            else:
                i += 1

    except Exception as e:
        print(f"Error reading {file_path}: {e}")

    return sorted(set(methods), key=lambda x: x[0])


def generate_stub():
    """Generate the complete stub file."""
    base_path = Path(__file__).parent.parent / "src" / "basalam_sdk"

    services = [
        ("core", base_path / "core" / "client.py"),
        ("chat", base_path / "chat" / "client.py"),
        ("order", base_path / "order" / "client.py"),
        ("order_processing", base_path / "order_processing" / "client.py"),
        ("search", base_path / "search" / "client.py"),
        ("upload", base_path / "upload" / "client.py"),
        ("wallet", base_path / "wallet" / "client.py"),
        ("webhook", base_path / "webhook" / "client.py"),
    ]

    stub_lines = [
        '"""Type stubs for BasalamClient - provides IDE autocomplete support."""',
        "from typing import Any, Dict, List, Optional, Union, BinaryIO",
        "from .auth import BaseAuth, Scope",
        "from .config import BasalamConfig",
        "",
        "class BasalamClient:",
        '    """Main client for interacting with the Basalam API."""',
        "",
        "    def __init__(self, auth: BaseAuth, config: Optional[BasalamConfig] = None) -> None: ...",
        "",
        "    # Service attributes",
    ]

    # Add service attributes
    for service_name, _ in services:
        stub_lines.append(f"    {service_name}: Any")

    stub_lines.extend([
        "",
        "    # Context manager and auth methods",
        "    async def __aenter__(self) -> BasalamClient: ...",
        "    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None: ...",
        "    def has_scope(self, scope: Union[str, Scope]) -> bool: ...",
        "    def get_granted_scopes(self) -> List[str]: ...",
        "    async def refresh_auth_token(self) -> None: ...",
        "    def refresh_auth_token_sync(self) -> None: ...",
        "",
        "    # Service methods (dynamically delegated)",
    ])

    # Extract and add all service methods
    all_methods = set()
    for service_name, service_file in services:
        if service_file.exists():
            method_signatures = extract_methods_from_file(service_file)
            for method_name, signature in method_signatures:
                if method_name not in all_methods:
                    # Add the method with its actual signature
                    stub_lines.append(f"    {signature}: ...")
                    all_methods.add(method_name)

    return "\n".join(stub_lines)


def main():
    """Generate and write the stub file."""
    stub_content = generate_stub()

    # Write to basalam_client.pyi
    output_path = Path(__file__).parent.parent / "src" / "basalam_sdk" / "basalam_client.pyi"
    output_path.write_text(stub_content)

    # Ensure py.typed marker file exists
    py_typed_path = Path(__file__).parent.parent / "src" / "basalam_sdk" / "py.typed"
    if not py_typed_path.exists():
        py_typed_path.write_text("")

    print(f"✅ Generated stub file: {output_path}")
    print(f"✅ Ensured py.typed marker: {py_typed_path}")
    print(f"📊 Methods included: {stub_content.count('def ')}")


if __name__ == "__main__":
    main()
