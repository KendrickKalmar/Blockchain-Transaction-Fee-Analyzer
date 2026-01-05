# Testing Guide

## Quick Test

Run the import test script to verify everything is set up correctly:

```bash
python test_imports.py
```

This will check:
- ✓ All Python dependencies are installed
- ✓ Configuration file can be imported
- ✓ Network modules can be imported
- ⚠ Configuration status (API keys, addresses)

## Manual Testing

### 1. Test Configuration Import

```python
python3 -c "from config.config import *; print('Config OK')"
```

### 2. Test Network Module Import

```python
cd networks
python3 -c "import arbitrum; print('Arbitrum module OK')"
```

### 3. Test with Dry Run

The scripts will fail gracefully if:
- API key is not configured (shows error message)
- Address is not configured (shows error message)
- No transactions found (shows warning)

This allows you to test the code structure without valid credentials.

## Expected Behavior

### When Configuration is Missing

```
ERROR - Arbitrum address not configured. Please set ADDRESSES['arbitrum'] in config/config.py
```

or

```
ERROR - Etherscan API key not configured. Please set ETHERSCAN_API_KEY in config/config.py
```

### When Everything is Configured

The script will:
1. Connect to API
2. Retrieve your transactions
3. Analyze network transactions
4. Generate report
5. Save results to `results/` directory

## Troubleshooting Test Failures

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'requests'`
**Solution:** Install dependencies: `pip install -r requirements.txt`

**Problem:** `ModuleNotFoundError: No module named 'config'`
**Solution:** Make sure you're running from project root directory

### Configuration Errors

**Problem:** `KeyError: 'arbitrum'`
**Solution:** Check that all network keys exist in `ADDRESSES` and `CHAIN_IDS` dictionaries

**Problem:** `Invalid API key`
**Solution:** Verify API key is correct and active on etherscan.io

### Runtime Errors

**Problem:** `Connection timeout`
**Solution:** Check internet connection, API endpoint availability

**Problem:** `No transactions found`
**Solution:** 
- Verify address has recent transactions
- Check address format is correct
- Some networks require confirmed transactions only

## Testing Checklist

Before using in production:

- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] `test_imports.py` passes
- [ ] Configuration file exists and is valid
- [ ] API key is set and valid
- [ ] At least one address is configured
- [ ] Test run completes without errors
- [ ] Results are saved to `results/` directory

