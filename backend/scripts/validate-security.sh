#!/bin/bash
# Security validation script
# Run this script to validate security configuration before deployment

set -e

echo "🔒 Running Security Validation Checks..."
echo ""

ERRORS=0

# Check 1: Verify .env is in .gitignore
echo "✓ Checking .env is in .gitignore..."
if git check-ignore .env > /dev/null 2>&1; then
    echo "  ✅ .env is properly ignored"
else
    echo "  ❌ ERROR: .env is NOT in .gitignore"
    ERRORS=$((ERRORS + 1))
fi

# Check 2: Verify .env.example exists
echo "✓ Checking .env.example exists..."
if [ -f .env.example ]; then
    echo "  ✅ .env.example exists"
    
    # Check that .env.example doesn't contain actual keys
    if grep -q "sk-[a-zA-Z0-9]" .env.example 2>/dev/null; then
        echo "  ❌ ERROR: .env.example contains what looks like an API key"
        ERRORS=$((ERRORS + 1))
    else
        echo "  ✅ .env.example doesn't contain actual keys"
    fi
else
    echo "  ❌ ERROR: .env.example is missing"
    ERRORS=$((ERRORS + 1))
fi

# Check 3: Verify no hardcoded API keys in source code
echo "✓ Checking for hardcoded API keys in source code..."
if grep -r "sk-[a-zA-Z0-9]\{20,\}" app/ 2>/dev/null | grep -v ".pyc" | grep -v "__pycache__"; then
    echo "  ❌ ERROR: Potential API keys found in source code"
    ERRORS=$((ERRORS + 1))
else
    echo "  ✅ No hardcoded API keys found"
fi

# Check 4: Verify pre-commit hooks are configured
echo "✓ Checking pre-commit hooks configuration..."
if [ -f .pre-commit-config.yaml ]; then
    echo "  ✅ .pre-commit-config.yaml exists"
    
    if grep -q "detect-secrets" .pre-commit-config.yaml; then
        echo "  ✅ detect-secrets is configured"
    else
        echo "  ⚠️  WARNING: detect-secrets not found in pre-commit config"
    fi
else
    echo "  ⚠️  WARNING: .pre-commit-config.yaml not found"
fi

# Check 5: Verify secrets baseline exists
echo "✓ Checking secrets baseline..."
if [ -f .secrets.baseline ]; then
    echo "  ✅ .secrets.baseline exists"
else
    echo "  ⚠️  WARNING: .secrets.baseline not found (run: detect-secrets scan > .secrets.baseline)"
fi

# Check 6: Verify CORS doesn't use wildcard for origins
echo "✓ Checking CORS configuration..."
# Check for wildcard in allow_origins (excluding comments)
if grep -v "^\s*#" app/main.py | grep -E 'allow_origins\s*=\s*\[["\047]\*["\047]\]' 2>/dev/null; then
    echo "  ❌ ERROR: CORS uses wildcard allow_origins"
    ERRORS=$((ERRORS + 1))
elif grep -v "^\s*#" app/main.py | grep -q "ALLOWED_ORIGINS\|os.getenv.*ALLOWED_ORIGINS" 2>/dev/null; then
    echo "  ✅ CORS uses environment variable for origins (production-safe)"
elif grep -v "^\s*#" app/main.py | grep -q "allow_origins=" 2>/dev/null; then
    # Check if it's a hardcoded list without wildcard
    if grep -v "^\s*#" app/main.py | grep -A 1 "allow_origins=" | grep -q "\*"; then
        echo "  ❌ ERROR: CORS may use wildcard"
        ERRORS=$((ERRORS + 1))
    else
        echo "  ✅ CORS uses explicit origin configuration (production-safe)"
    fi
else
    echo "  ✅ CORS configuration verified"
fi

# Check 7: Verify SECURITY.md exists
echo "✓ Checking security documentation..."
if [ -f SECURITY.md ]; then
    echo "  ✅ SECURITY.md exists"
else
    echo "  ⚠️  WARNING: SECURITY.md not found"
fi

# Check 8: Run security tests
echo "✓ Running security tests..."
if python -m pytest tests/integration/test_routers/test_cors.py \
           tests/integration/test_routers/test_error_handling.py \
           tests/unit/test_config.py \
           -v --tb=short > /dev/null 2>&1; then
    echo "  ✅ All security tests pass"
else
    echo "  ❌ ERROR: Security tests failed"
    ERRORS=$((ERRORS + 1))
fi

echo ""
if [ $ERRORS -eq 0 ]; then
    echo "✅ Security validation PASSED - All checks successful"
    exit 0
else
    echo "❌ Security validation FAILED - $ERRORS error(s) found"
    exit 1
fi

