#!/bin/bash

# Script to run job scraper and deploy to Cloudflare Pages
# Runs every hour via cron

# Navigate to the project directory
cd $HOME/services/olj || exit 1

# Log start time
echo "[$(date)] Starting job scraper run" >> $HOME/services/olj/cron.log

# Run the job scraper using uv
if $HOME/.local/bin/uv run job_scraper_enhanced.py >> $HOME/services/olj/cron.log 2>&1; then
    echo "[$(date)] Job scraper completed successfully" >> $HOME/services/olj/cron.log
    
    # Run job posting scraper
    echo "[$(date)] Starting job posting scraper" >> $HOME/services/olj/cron.log
    if $HOME/.local/bin/uv run job_posting_scraper.py >> $HOME/services/olj/cron.log 2>&1; then
        echo "[$(date)] Job posting scraper completed successfully" >> $HOME/services/olj/cron.log
    else
        echo "[$(date)] WARNING: Job posting scraper failed" >> $HOME/services/olj/cron.log
    fi
    
    # Run insights engine
    echo "[$(date)] Starting insights engine" >> $HOME/services/olj/cron.log
    if $HOME/.local/bin/uv run insights_engine.py >> $HOME/services/olj/cron.log 2>&1; then
        echo "[$(date)] Insights engine completed successfully" >> $HOME/services/olj/cron.log
    else
        echo "[$(date)] WARNING: Insights engine failed" >> $HOME/services/olj/cron.log
    fi
    
    # Deploy to Cloudflare Pages using wrangler
    if $HOME/.local/bin/mise exec -- npx wrangler pages deploy ./ --project-name=olj >> $HOME/services/olj/cron.log 2>&1; then
        echo "[$(date)] Deployment to Cloudflare Pages successful" >> $HOME/services/olj/cron.log
    else
        echo "[$(date)] ERROR: Deployment to Cloudflare Pages failed" >> $HOME/services/olj/cron.log
        exit 1
    fi
else
    echo "[$(date)] ERROR: Job scraper failed" >> $HOME/services/olj/cron.log
    exit 1
fi

echo "[$(date)] Run and deploy completed" >> $HOME/services/olj/cron.log
echo "----------------------------------------" >> $HOME/services/olj/cron.log