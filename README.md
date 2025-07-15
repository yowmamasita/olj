# OnlineJobs.ph Skills Visualizer

An interactive tool that shows which skills are in demand in the Philippines job market. Perfect for job seekers looking to identify opportunities and plan their career development.

## What is this?

This tool creates a visual map of all the skills listed on OnlineJobs.ph, showing:
- **Which skills have the most job openings** (updated regularly)
- **How skills relate to each other** (skill categories and relationships)
- **Market trends** through color-coded categories

## Who is this for?

- **Job seekers** exploring career opportunities in the Philippines
- **Students** deciding which skills to learn
- **Career changers** looking for in-demand skills
- **Employers** understanding the talent landscape

## How to use it

### Quick Start
1. **Open the tool** in your web browser
2. **Click on skills** to explore - branches expand to show related skills
3. **Look for highlighted skills** - these have the most job opportunities
4. **Click any skill name** to see actual job postings on OnlineJobs.ph

### Key Features

**🔍 Find Opportunities**
- Skills with rainbow borders have 200+ job openings
- Cyan borders mean 100-199 jobs
- Magenta borders indicate 50-99 jobs

**🎨 Skill Categories**
- Blue = Technology & Programming
- Purple = Design & Creative
- Orange = Business & Management
- Green = Marketing & Sales
- Cyan = Writing & Content
- Dark Blue = Data & Analytics
- Pink = Support & Admin

**📱 Works Everywhere**
- Desktop, tablet, and mobile friendly
- Touch gestures supported
- No installation needed

## Project Overview

### What's included

**Core Files:**
- `index.html` - The main visualization (open this in your browser)
- `stats.html` - Market intelligence dashboard with trends and insights

**Data Files:**
- `skills_with_jobs_current.json` - Latest job market data
- `allskills_tree_clean.json` - Backup skill structure

**Tools (for maintainers):**
- `job_scraper_enhanced.py` - Updates job counts from OnlineJobs.ph
- `insights_engine.py` - Generates market intelligence reports
- `job_posting_scraper.py` - Collects detailed job posting data

**Supporting Files:**
- `jobs/` - Folder containing individual job posting data
- `start_server.sh` - Simple web server for local viewing

## Want to help?

We welcome all kinds of contributions! You don't need to be technical to help:

- **Report issues** - Tell us if something doesn't work right
- **Suggest improvements** - Share ideas to make the tool better
- **Test the tool** - Help us find bugs across different devices
- **Share market knowledge** - Suggest missing skills or better categories

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute.

## Getting Started (Simple Version)

### Just want to view it?
1. Download the project files
2. Open `index.html` in any web browser
3. Start exploring!

### Want fresh data?
If you're comfortable with basic computer tasks and want the latest job data, see the setup instructions in [CONTRIBUTING.md](CONTRIBUTING.md).

## Questions?

This tool is community-driven and aims to help job seekers in the Philippines make informed career decisions. If you have questions or suggestions, please open an issue on GitHub.

---

Made with ❤️ for the Philippine job market community