# OnlineJobs.ph Skills Visualizer - Upskilling Opportunities

This enhanced visualization shows real job market data to help identify upskilling opportunities. The tree visualization now displays actual job counts for each skill, making it easy to see which skills are in high demand.

## Features

### Visual Indicators for Job Opportunities

1. **Node Size** - Larger nodes indicate more job opportunities:
   - 🟢 Large nodes (100+ jobs) - High demand skills
   - 🟡 Medium nodes (20-99 jobs) - Moderate demand
   - 🔵 Small nodes (1-19 jobs) - Lower demand
   - ⚪ Default size - No job data or branch nodes

2. **Color Intensity** - Darker green = more opportunities
   - Uses a gradient from light to dark green based on job count

3. **Red Border** - Skills with 50+ jobs are highlighted as "high opportunity"

4. **Interactive Tooltips** - Hover over any node to see:
   - Skill name and level
   - Number of available jobs
   - Total jobs in category (for branch nodes)

5. **Job Count Labels** - Leaf nodes show "(X jobs)" below the skill name

### Interactive Features

- **Filter by Job Count** - Use the slider to show only skills with minimum job opportunities
- **Toggle High Opportunity Highlighting** - Show/hide red borders on high-demand skills
- **Search** - Find specific skills quickly
- **Click Leaf Nodes** - Opens OnlineJobs.ph job search for that skill

## Setup Instructions

### 1. Install uv (if not already installed)

```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using pip
pip install uv
```

### 2. Install Dependencies with uv

```bash
# Create virtual environment and install dependencies
uv venv
uv pip sync requirements.txt
```

### 3. Scrape Job Data

The scraper now supports **parallel processing** for much faster execution! It uses multiple workers to scrape skills simultaneously.

Run the enhanced scraper to fetch real job counts using uv:

```bash
# Test mode - scrapes only 10 skills
uv run python job_scraper_enhanced.py --test

# Full mode with default workers (uses all CPU cores)
uv run python job_scraper_enhanced.py

# Specify number of workers
uv run python job_scraper_enhanced.py --workers 8

# Custom options
uv run python job_scraper_enhanced.py --workers 4 --delay 2.0 --limit 50
```

**Command-line options:**
- `--test` - Test mode, scrapes only 10 skills
- `--workers N` - Number of parallel workers (default: CPU count)
- `--delay N` - Delay between requests per worker in seconds (default: 1.5)
- `--limit N` - Limit number of skills to scrape

Alternative: If you've activated the virtual environment:
```bash
# Activate the virtual environment
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows

# Then run directly
python job_scraper_enhanced.py --test --workers 4
```

**Performance improvements:**
- With 4 workers: ~4x faster
- With 8 workers: ~6-8x faster (diminishing returns due to rate limiting)
- Test scrape (10 skills): ~7-10 seconds instead of 15+
- Full scrape: ~10-15 minutes instead of 30-60

The scraper will:
- Find all leaf skills in the tree
- Visit each skill's job search page
- Extract the number of available jobs
- Save enhanced data to `skills_with_jobs_current.json`

### 4. View the Enhanced Visualization

Start the local server:
```bash
./start_server.sh
```

Then open http://localhost:8000/index.html in your browser. The visualization will:
- Automatically load job data if available
- Fall back to demo data if the scraper hasn't been run
- Show a status indicator for data mode

## Understanding the Visualization

### For Job Seekers

1. **Identify High-Demand Skills**
   - Look for large, dark green nodes
   - Red-bordered nodes have 50+ job opportunities
   - Use the filter to focus on skills with many jobs

2. **Explore Related Skills**
   - Click parent nodes to see related skill categories
   - Total jobs shown for categories help identify promising areas

3. **Plan Your Learning Path**
   - Start from your current skills
   - Explore adjacent high-demand skills
   - Click leaf nodes to see actual job postings

### For Employers

- See which skills are saturated vs. underserved
- Identify skill combinations in demand
- Understand the skill taxonomy used by job seekers

## Data Structure

The enhanced JSON structure includes job counts:

```json
{
  "Accounting": {
    "children": {
      "Quickbooks": {
        "id": "7",
        "job_count": 336,
        "type": "leaf"
      },
      "Financial Accounting": {
        "children": {...},
        "total_jobs": 245,
        "type": "branch"
      }
    },
    "total_jobs": 734,
    "type": "branch"
  }
}
```

## Output Files

- `skills_with_jobs_current.json` - Latest enhanced tree data
- `skills_with_jobs_[timestamp].json` - Timestamped backups
- `job_scrape_details_[timestamp].csv` - Detailed scraping results

## Tips

- Run the scraper periodically to keep job data current
- The scraper includes a 1.5-second delay between requests to be respectful
- Filter results to focus on skills with actual job opportunities
- Combine with the original visualization for different perspectives

## Mobile Support

The enhanced visualization is fully responsive:
- Touch-friendly controls
- Collapsible menu
- Optimized node sizes for small screens
- Pan and zoom with touch gestures

## Browser Compatibility

Works best in modern browsers that support ES6 and SVG:
- Chrome/Edge (recommended)
- Firefox
- Safari