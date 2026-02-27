# Daily Catalog Update Script - Quick Reference

## Current Week URLs (Feb 11-17, 2026)
- **Coles NSW Metro**: `https://d3vvi2v9oj75wh.cloudfront.net/uploads/pdf/COLNSWMETRO_110226_AQH86RS.pdf`
- **Woolworths NSW**: `https://d3vvi2v9oj75wh.cloudfront.net/uploads/pdf/WW_NSW_110226_5UK7TA7434.pdf`

## How to Update for New Week

Every Wednesday, update the URLs in `auto_update_catalogs.py`:

1. **Find the new date code**: Format is `DDMMYY` (e.g., `110226` for Feb 11, 2026)
2. **Update `current_week_urls` in both functions**:
   - `get_coles_pdf_url()` - lines ~22-25
   - `get_woolworths_pdf_url()` - lines ~58-61

### Finding New URLs

**Option 1: Browser Method**
- Go to https://salefinder.com.au/Coles-catalogue
- Open browser DevTools (F12) → Network tab
- Click on the catalogue → Look for PDF requests
- Copy the Cloudfront URL

**Option 2: Pattern Guessing** (faster but less reliable)
- Coles pattern: `COLNSWMETRO_DDMMYY_XXXXXX.pdf`
- Woolworths pattern: `WW_NSW_DDMMYY_XXXXXX.pdf`
- The suffix (`XXXXXX`) changes weekly - try common patterns or check previous weeks

## Running the Script

```bash
# Test email configuration
python3 auto_update_catalogs.py --test-email

# Run full update (downloads PDFs, ingests, sends email)
python3 auto_update_catalogs.py
```

## Automation (Cron)

Add to crontab to run every Wednesday at 8 AM:
```
0 8 * * 3 cd /path/to/backend && python3 auto_update_catalogs.py >> catalog_update.log 2>&1
```

## Troubleshooting

- **403 Errors**: URLs are outdated, update manually
- **Download Fails**: Check internet connection or Cloudfront availability
- **Ingestion Fails**: Check database connection and `rag_engine.py`
- **Email Fails**: Verify SMTP credentials in `.env`
