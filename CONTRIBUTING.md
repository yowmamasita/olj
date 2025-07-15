# Contributing to OnlineJobs.ph Skills Visualizer

Welcome! This guide is for anyone who wants to help improve the Skills Visualizer, even if you're not a programmer. There are many ways to contribute!

## Ways You Can Help

### 1. Report Issues
Found something that doesn't work right? Let us know!
- **What to report**: Broken features, confusing interface elements, missing skills, incorrect job counts
- **How to report**: Create an issue on GitHub with:
  - What you were trying to do
  - What happened instead
  - What browser you're using (Chrome, Firefox, Safari, etc.)
  - If possible, a screenshot

### 2. Suggest Improvements
Have ideas to make the tool better?
- **User experience**: Suggest easier ways to navigate or find information
- **New features**: What would make this tool more helpful for job seekers?
- **Visual design**: Ideas for colors, layouts, or animations
- **Documentation**: Help us explain things more clearly

### 3. Test the Tool
Help us find bugs by using the tool regularly
- Try different browsers and devices
- Test all the features (search, filter, zoom, click on skills)
- Check if job counts seem accurate
- Let us know if anything feels slow or unresponsive

### 4. Share Market Knowledge
Know the Philippine job market well?
- Suggest missing skill categories
- Report outdated skill names
- Help group related skills better
- Share insights about which skills are trending

### 5. Help Other Users
- Answer questions from other users
- Share tips on how to use the tool effectively
- Write tutorials or guides
- Create video walkthroughs

## Getting Started (Simple Version)

### Just Want to View the Tool?
1. Download the project files
2. Open `index.html` in your web browser
3. That's it! The tool will load with demo data

### Want Fresh Job Data?
You'll need to run the data scraper. Here's the easiest way:

1. **Install Python** (if you don't have it)
   - Go to python.org and download Python
   - During installation, check "Add Python to PATH"

2. **Open Terminal/Command Prompt**
   - Windows: Press Win+R, type `cmd`, press Enter
   - Mac: Press Cmd+Space, type `terminal`, press Enter

3. **Navigate to the project folder**
   ```
   cd path/to/onlinejobs-visualizer
   ```

4. **Run the setup**
   ```
   pip install uv
   uv venv
   uv pip install -e .
   ```

5. **Get fresh job data**
   ```
   uv run python job_scraper_enhanced.py --test
   ```
   This gets data for 10 skills as a test. Remove `--test` to get all skills (takes 10-15 minutes).

6. **View your updated visualization**
   - Double-click `start_server.sh` (Mac/Linux)
   - Or just open `index.html` in your browser

## Reporting Issues - What We Need to Know

When something goes wrong, help us fix it by providing:

### For Visual Issues
- Screenshot of the problem
- Your screen size (laptop, tablet, phone)
- Browser name and version
- What you clicked before it happened

### For Data Issues
- Which skill has wrong information
- What the correct information should be
- Source of your information (if applicable)

### For Performance Issues
- What action is slow
- How many skills are displayed
- Your device type and browser

## Communication Guidelines

- Be respectful and constructive
- Assume good intentions from others
- Focus on the issue, not the person
- Celebrate contributions of all kinds

## Questions?

Not sure how to contribute? That's okay! 
- Open an issue asking for guidance
- Join discussions in existing issues
- Every contribution helps, no matter how small

Remember: You don't need to be technical to make valuable contributions. User feedback and real-world testing are incredibly important!

Thank you for helping make this tool better for job seekers in the Philippines!