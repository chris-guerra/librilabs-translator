# Security Guidelines

This document outlines security best practices for the Librilabs Translator backend.

## API Key Security

### OpenAI API Key Protection

**Critical Rules:**
1. **Never commit API keys to version control**
   - `.env` file is in `.gitignore` - verify it's never committed
   - Use `.env.example` as a template only (no actual keys)

2. **Environment Variables Only**
   - Always load API keys from environment variables
   - Never hardcode keys in source code
   - Never log API key values (mask if referenced)

3. **Pre-commit Protection**
   - Pre-commit hooks configured to detect secrets
   - Run `detect-secrets scan > .secrets.baseline` to create baseline
   - Hooks will prevent commits containing secrets

4. **Production Deployment**
   - Use secure secret management (Railway environment variables, AWS Secrets Manager, etc.)
   - Rotate keys regularly
   - Use different keys for development and production
   - Never expose keys in deployment logs

### Setup Instructions

1. **Install pre-commit hooks:**
   ```bash
   pip install pre-commit
   pre-commit install
   ```

2. **Create secrets baseline (first time only):**
   ```bash
   pip install detect-secrets
   detect-secrets scan > .secrets.baseline
   ```

3. **Verify hooks work:**
   ```bash
   pre-commit run --all-files
   ```

## CORS Security

### Development
- Allowed origin: `http://localhost:3000` (explicit, not wildcard)
- Credentials: Enabled for session management
- Methods: All allowed (development only)

### Production
- **CRITICAL:** Never use `allow_origins=["*"]`
- Configure allowed origins via environment variable:
  ```python
  ALLOWED_ORIGINS=https://app.librilabs.com,https://www.librilabs.com
  ```
- Use explicit origin list, never wildcards
- Review and update origins regularly

### Configuration
CORS is configured in `backend/app/main.py`. For production, update to:
```python
import os
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Error Handling Security

### Structured Error Responses
- All errors return structured format: `{error: {code, message, timestamp, request_id}}`
- No sensitive information exposed:
  - No API keys in error messages
  - No stack traces in production
  - No internal file paths
  - No database connection strings

### Error Logging
- Log errors server-side with full context (including request_id)
- Never log sensitive data (API keys, passwords, tokens)
- Use structured logging (future enhancement)

## Security Testing

### Automated Security Tests
All security tests are in `backend/tests/`:
- **CORS Tests:** `tests/integration/test_routers/test_cors.py`
- **Error Handling Tests:** `tests/integration/test_routers/test_error_handling.py`
- **API Key Security Tests:** `tests/unit/test_config.py`

### Running Security Tests
```bash
# Run all security tests
pytest tests/integration/test_routers/test_cors.py \
       tests/integration/test_routers/test_error_handling.py \
       tests/unit/test_config.py -v

# Run with coverage
pytest --cov=app --cov-report=html
```

## Security Checklist

Before deploying to production:

- [ ] `.env` file is in `.gitignore` and never committed
- [ ] `.env.example` exists with placeholder values only
- [ ] Pre-commit hooks installed and working
- [ ] No API keys hardcoded in source code
- [ ] CORS configured with explicit origins (not wildcard)
- [ ] Production CORS origins set via environment variables
- [ ] Error handling sanitizes sensitive data
- [ ] All security tests passing
- [ ] API keys stored in secure secret management system
- [ ] Different API keys for dev/staging/production
- [ ] API key rotation plan in place

## Reporting Security Issues

If you discover a security vulnerability:
1. **DO NOT** create a public issue
2. Contact the development team directly
3. Provide details of the vulnerability
4. Allow time for fix before public disclosure

## Security Validation

### Automated Security Checks

**Local Validation:**
```bash
./scripts/validate-security.sh
```

**CI/CD Integration:**
Security checks are automatically run in CI/CD pipeline (`.github/workflows/backend-security.yml`):
- Pre-commit hooks validation
- Secrets detection
- Security test execution
- Code scanning for hardcoded keys

**Manual Security Review:**
Before each deployment, verify:
1. Run security validation script
2. Review pre-commit hook output
3. Verify all security tests pass
4. Check for any new dependencies with known vulnerabilities

## Monitoring

### Ongoing Security Monitoring

**Automated:**
- Pre-commit hooks prevent secret commits
- CI/CD pipeline validates security on every push
- Security tests run in every build

**Manual:**
- Regular security audits (quarterly recommended)
- Review security logs for anomalies
- Monitor API key usage for unauthorized access
- Update dependencies for security patches

**Incident Response:**
- If API key is exposed: Rotate immediately
- If security vulnerability found: Follow reporting process in this document
- If unauthorized access detected: Revoke keys and investigate

## References

- [OpenAI API Security Best Practices](https://platform.openai.com/docs/guides/safety-best-practices)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [FastAPI Security Documentation](https://fastapi.tiangolo.com/tutorial/security/)

