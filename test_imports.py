#!/usr/bin/env python3
"""
Test script to verify all imports and basic functionality work.
Run this before using the analyzer to ensure everything is set up correctly.
"""

import sys
import os

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import requests
        print("✓ requests imported")
    except ImportError as e:
        print(f"✗ requests import failed: {e}")
        return False
    
    try:
        import tabulate
        print("✓ tabulate imported")
    except ImportError as e:
        print(f"✗ tabulate import failed: {e}")
        return False
    
    try:
        from collections import defaultdict
        print("✓ collections imported")
    except ImportError as e:
        print(f"✗ collections import failed: {e}")
        return False
    
    return True

def test_config_import():
    """Test that config can be imported."""
    print("\nTesting config import...")
    
    # Add config to path
    config_path = os.path.join(os.path.dirname(__file__), 'config')
    if config_path not in sys.path:
        sys.path.insert(0, config_path)
    
    try:
        from config import ETHERSCAN_API_KEY, ADDRESSES, TOKENS, SETTINGS, CHAIN_IDS, API_ENDPOINTS
        print("✓ Config imported successfully")
        
        # Check if config is set up
        if ETHERSCAN_API_KEY == "YOUR_ETHERSCAN_API_KEY_HERE":
            print("⚠ Warning: API key not configured")
        else:
            print("✓ API key is set")
        
        # Check addresses
        missing_addresses = []
        for network in ["ethereum", "arbitrum", "polygon", "litecoin"]:
            if ADDRESSES.get(network, "").startswith("YOUR_") or not ADDRESSES.get(network):
                missing_addresses.append(network)
        
        if missing_addresses:
            print(f"⚠ Warning: Addresses not configured for: {', '.join(missing_addresses)}")
        else:
            print("✓ All addresses are configured")
        
        # Check chain IDs
        print(f"✓ Chain IDs configured: {list(CHAIN_IDS.keys())}")
        
        return True
    except ImportError as e:
        print(f"✗ Config import failed: {e}")
        print("  Make sure config/config.py exists")
        return False
    except Exception as e:
        print(f"✗ Config error: {e}")
        return False

def test_network_modules():
    """Test that network modules can be imported."""
    print("\nTesting network modules...")
    
    networks_dir = os.path.join(os.path.dirname(__file__), 'networks')
    if networks_dir not in sys.path:
        sys.path.insert(0, networks_dir)
    
    networks = ["ethereum", "arbitrum", "polygon", "litecoin"]
    success = True
    
    for network in networks:
        try:
            # Try to import the module (this will fail if config is wrong, but that's OK)
            module = __import__(network)
            print(f"✓ {network}.py can be imported")
        except ImportError as e:
            if "config" in str(e).lower():
                print(f"⚠ {network}.py import depends on config (this is OK)")
            else:
                print(f"✗ {network}.py import failed: {e}")
                success = False
        except Exception as e:
            print(f"⚠ {network}.py import error: {e}")
    
    return success

def main():
    """Run all tests."""
    print("=" * 60)
    print("Blockchain Fee Analyzer - Import Test")
    print("=" * 60)
    
    all_ok = True
    
    if not test_imports():
        all_ok = False
    
    if not test_config_import():
        all_ok = False
    
    if not test_network_modules():
        all_ok = False
    
    print("\n" + "=" * 60)
    if all_ok:
        print("✓ All basic tests passed!")
        print("\nNext steps:")
        print("1. Configure config/config.py with your API keys and addresses")
        print("2. Run: python networks/<network>.py")
    else:
        print("✗ Some tests failed. Please fix the issues above.")
    print("=" * 60)

if __name__ == "__main__":
    main()

