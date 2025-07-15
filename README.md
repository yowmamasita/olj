# OnlineJobs.ph Skills Visualizer

An interactive skill tree visualization that helps identify job opportunities in the Philippines market. This tool displays hierarchical skill categories with real job market data to guide career planning and upskilling decisions.

## Features

### Visual Design System

#### Node Sizing
- **Uniform sizing approach**: Node size indicates hierarchy level, not job count
- **Root node**: 20px radius (OnlineJobs.ph)
- **All other nodes**: 12px radius (consistent across all skill levels)
- **Font sizes**: Scale with hierarchy (24px→18px desktop, 20px→16px mobile)

#### Color System
The visualization uses a sophisticated category-based color scheme with 7 distinct skill categories:

- **🔵 Technology/Programming**: `#0066FF` → `#00BBFF` (blue gradient)
  - Programming, Web Development, Mobile Development, Cloud Services, etc.
- **🟣 Design/Creative**: `#9B59B6` → `#E74C3C` (purple to red)
  - Design, Graphics, UI/UX, Video/Audio Editing
- **🟠 Business/Management**: `#FF6B35` → `#FFB700` (orange gradient)
  - Business, Management, Finance, Accounting, HR
- **🟢 Marketing/Sales**: `#00C896` → `#00E676` (green gradient)
  - Marketing, Sales, SEO, Social Media, E-Commerce
- **🔷 Writing/Content**: `#00ACC1` → `#26C6DA` (cyan gradient)
  - Writing, Content, Copywriting, Blog
- **🔮 Data/Analytics**: `#3F51B5` → `#7986CB` (dark blue gradient)
  - Data, Analytics, Research, Statistics
- **🩷 Support/Admin**: `#E91E63` → `#F06292` (pink gradient)
  - Support, Admin, Customer Service, Virtual Assistant

Color intensity within each category increases with job count (0-200 jobs range with HSL interpolation).

#### Job Demand Indicators
Special border effects highlight high-opportunity skills:

- **High demand (50-99 jobs)**: Magenta border (`#FF00FF`), 3px width, pulsing animation
- **Very high (100-199 jobs)**: Cyan border (`#00FFFF`), 4px width, faster pulsing
- **Ultra high (200+ jobs)**: Rainbow gradient border, 4px width, color-cycling animation

### Layout Modes

#### Radial Layout
- Circular tree radiating from center
- Size: `[2π, min(width,height)/2 - 150]`
- Simple separation: siblings 1x, non-siblings 2x/depth

#### Horizontal Layout (Default)
- Traditional left-to-right tree structure
- Size: `[height × 1.5, width - 200]`
- Sophisticated spacing with depth factors:
  - Level 1: 2x spacing
  - Level 2: 2.5x spacing
  - Level 3+: 3x spacing with additional multipliers
  - Nodes with children get 1.3x extra space

### Interactive Features

#### Navigation
- **Click nodes**: Expand/collapse branches (+ = expandable, − = expanded)
- **Click leaf nodes**: Opens OnlineJobs.ph job search for that skill
- **Zoom/Pan**: Mouse wheel or touch gestures
- **Reset View**: Returns to optimal zoom level for current layout

#### Search & Filtering
- **Text search**: Find specific skills with pink highlighting
- **Job count filter**: Slider to show only skills above minimum threshold
- **High opportunity toggle**: Show/hide special border effects

#### Tooltips
- **Desktop**: Hover to show skill details
- **Mobile**: Long-press (500ms) to display tooltip for 3 seconds
- Shows job count, hierarchy level, and category totals

### Mobile Experience

#### Responsive Design (768px breakpoint)
- **Hamburger menu**: Slide-out controls with overlay
- **Touch optimization**: 44px minimum touch targets
- **Collapsible sections**: Legend and instructions fold away
- **Font scaling**: Reduced sizes for mobile readability

#### Touch Interactions
- **Tap**: Expand/collapse or navigate to jobs
- **Long-press**: Show tooltip
- **Pinch/zoom**: Navigate the visualization
- **Touch feedback**: Visual highlights and animations

## Setup Instructions

### 1. Install uv (if not already installed)

```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using pip
pip install uv
```

### 2. Install Dependencies

```bash
# Create virtual environment and install dependencies
uv venv
uv pip install -e .
```

### 3. Scrape Job Data (Optional)

The scraper supports parallel processing for faster execution:

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

**Performance improvements:**
- With 4 workers: ~4x faster
- With 8 workers: ~6-8x faster
- Test scrape (10 skills): ~7-10 seconds
- Full scrape: ~10-15 minutes

### 4. View the Visualization

Start the local server:
```bash
./start_server.sh
```

Open http://localhost:8000/index.html in your browser. The visualization will:
- Load `skills_with_jobs_current.json` if available (real job data)
- Fall back to `allskills_tree_clean.json` (demo data with mock counts)
- Display data status in the controls panel

## Use Cases

### For Job Seekers

1. **Identify High-Demand Skills**
   - Look for nodes with special border effects (magenta/cyan/rainbow)
   - Use job count filter to focus on opportunities
   - Check job count labels on leaf nodes

2. **Explore Career Paths**
   - Navigate skill categories by color
   - Expand branches to see related skills
   - Click skills to view actual job postings

3. **Plan Learning Routes**
   - Start from current skills
   - Identify adjacent high-demand skills
   - Use category totals to prioritize learning areas

### For Employers

- Identify skills with high/low supply
- Understand skill taxonomy and relationships
- See market demand patterns by category

## Data Structure

The enhanced JSON includes real job counts:

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

## Browser Compatibility

Works best in modern browsers supporting ES6 and SVG:
- Chrome/Edge (recommended)
- Firefox
- Safari

## Tips

- Run scraper periodically to keep job data current
- Use horizontal layout for detailed exploration
- Use radial layout for overview and pattern recognition
- Filter by job count to focus on viable opportunities
- Mobile experience optimized for touch navigation