import json
import requests
from bs4 import BeautifulSoup
import time
import os
import re
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from urllib.parse import urljoin, urlparse
import sys


class JobPostingScraper:
    def __init__(self, max_workers: int = None, output_dir: str = "jobs"):
        self.base_url = "https://www.onlinejobs.ph/jobseekers/jobsearch"
        self.job_base_url = "https://www.onlinejobs.ph/jobseekers/job/"
        self.output_dir = output_dir
        self.max_workers = max_workers or os.cpu_count() or 4
        self.results_lock = threading.Lock()
        self.progress_lock = threading.Lock()
        self.completed_count = 0
        self.total_count = 0
        self.scraped_jobs = set()
        self.failed_jobs = []
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
    def _get_session(self):
        """Create a new session for each thread"""
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        return session
    
    def extract_job_urls_from_page(self, html: str, base_url: str) -> List[str]:
        """Extract all job URLs from a search results page"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find all job links - there are usually 2 per job (descriptive + ID-only)
        job_links = soup.select('a[href*="/jobseekers/job/"]')
        
        # Use a dict to track unique job IDs and prefer descriptive URLs
        job_urls_by_id = {}
        
        for link in job_links:
            href = link.get('href')
            if href and '/jobseekers/job/' in href:
                full_url = urljoin(base_url, href)
                job_id = self.extract_job_id_from_url(full_url)
                
                if job_id:
                    # Prefer longer, more descriptive URLs over short ID-only ones
                    if job_id not in job_urls_by_id or len(full_url) > len(job_urls_by_id[job_id]):
                        job_urls_by_id[job_id] = full_url
        
        return list(job_urls_by_id.values())
    
    def extract_job_id_from_url(self, url: str) -> Optional[str]:
        """Extract job ID from job URL"""
        # Pattern: https://www.onlinejobs.ph/jobseekers/job/Facebook-Media-Buyer-Campaign-Launcher-1422402
        # Extract the number at the end
        match = re.search(r'/job/.*?-(\d+)/?$', url)
        if match:
            return match.group(1)
        
        # Alternative pattern: direct job ID
        match = re.search(r'/job/(\d+)/?$', url)
        if match:
            return match.group(1)
        
        return None
    
    def scrape_job_details(self, job_url: str, session: requests.Session = None) -> Dict:
        """Scrape detailed information from a job posting page"""
        if session is None:
            session = self._get_session()
        
        job_id = self.extract_job_id_from_url(job_url)
        if not job_id:
            return {"error": "Could not extract job ID from URL", "url": job_url}
        
        try:
            response = session.get(job_url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Initialize job data
            job_data = {
                "job_id": job_id,
                "url": job_url,
                "scraped_at": datetime.now().isoformat(),
                "title": None,
                "type_of_work": None,
                "salary": None,
                "hours_per_week": None,
                "date_updated": None,
                "job_overview": None,
                "skill_requirements": [],
                "is_active": True,
                "status_history": []
            }
            
            # Extract job title
            title_selectors = ['h1', '.job-title', '#job-title', 'title']
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem:
                    title_text = title_elem.get_text(strip=True)
                    if title_text and len(title_text) > 5:  # Basic validation
                        job_data["title"] = title_text
                        break
            
            # Handle unavailable jobs
            if job_data["title"] == "Job Unavailable":
                job_data["is_active"] = False
                job_data["title"] = "Job Unavailable"
                job_data["status_history"].append({
                    "status": "inactive",
                    "timestamp": datetime.now().isoformat(),
                    "reason": "Job marked as unavailable"
                })
                return job_data
            
            # Extract structured data
            text_content = soup.get_text()
            
            # Type of work
            type_match = re.search(r'TYPE OF WORK\s*([^\n]+)', text_content, re.IGNORECASE)
            if type_match:
                job_data["type_of_work"] = type_match.group(1).strip()
            
            # Salary
            salary_match = re.search(r'SALARY\s*([^\n]+)', text_content, re.IGNORECASE)
            if salary_match:
                job_data["salary"] = salary_match.group(1).strip()
            
            # Hours per week
            hours_match = re.search(r'HOURS PER WEEK\s*([^\n]+)', text_content, re.IGNORECASE)
            if hours_match:
                job_data["hours_per_week"] = hours_match.group(1).strip()
            
            # Date updated
            date_match = re.search(r'DATE UPDATED\s*([^\n]+)', text_content, re.IGNORECASE)
            if date_match:
                job_data["date_updated"] = date_match.group(1).strip()
            
            # Job overview
            overview_match = re.search(r'JOB OVERVIEW\s*(.*?)(?=SKILL REQUIREMENT|ABOUT THE EMPLOYER|$)', text_content, re.IGNORECASE | re.DOTALL)
            if overview_match:
                job_data["job_overview"] = overview_match.group(1).strip()
            
            # Skill requirements - improved parsing
            # Try to find skills in structured HTML first - look for skill links
            skill_links = soup.find_all('a', {'class': 'card-worker-topskill'})
            if skill_links:
                job_data["skill_requirements"] = [link.get_text(strip=True) for link in skill_links]
            else:
                # Fallback: look for SKILL REQUIREMENT section
                skills_section = soup.find(string=re.compile(r'SKILL\s+REQUIREMENT', re.IGNORECASE))
                if skills_section:
                    # Look for the parent element and find skills after it
                    parent = skills_section.parent
                    if parent:
                        # Find the next elements that contain the skills
                        next_elements = parent.find_next_siblings()
                        skills_text = ""
                        for elem in next_elements:
                            elem_text = elem.get_text(strip=True)
                            # Stop if we hit other sections
                            if any(section in elem_text.upper() for section in ['ABOUT THE EMPLOYER', 'SHARE THIS POST', 'VIEW OTHER JOB', 'COPYRIGHT']):
                                break
                            if elem_text and len(elem_text) > 2:
                                skills_text += elem_text + " "
                        
                        if skills_text:
                            # Clean and split skills
                            skills_text = skills_text.strip()
                            # Split by common delimiters and camelCase boundaries
                            skills = re.split(r'[,\n\r]+|(?<=[a-z])(?=[A-Z][a-z])', skills_text)
                            job_data["skill_requirements"] = [
                                skill.strip() 
                                for skill in skills 
                                if skill.strip() and len(skill.strip()) > 2 and 'copyright' not in skill.lower()
                            ]
            
            # Fallback to text-based parsing if HTML parsing didn't work
            if not job_data["skill_requirements"]:
                skills_match = re.search(r'SKILL\s+REQUIREMENT[S]?\s*(.*?)(?=ABOUT\s+THE\s+EMPLOYER|SHARE\s+THIS\s+POST|VIEW\s+OTHER|$)', text_content, re.IGNORECASE | re.DOTALL)
                if skills_match:
                    skills_text = skills_match.group(1).strip()
                    # Clean up the text and split
                    skills_text = re.sub(r'\s+', ' ', skills_text)  # Normalize whitespace
                    # Stop at common footer/section markers
                    skills_text = re.split(r'(?:ABOUT THE EMPLOYER|SHARE THIS POST|VIEW OTHER|Employers|Workers|Copyright)', skills_text, flags=re.IGNORECASE)[0]
                    
                    # Split skills by common delimiters
                    skills = re.split(r'[,\n\r]+', skills_text.strip())
                    job_data["skill_requirements"] = [
                        skill.strip() 
                        for skill in skills 
                        if skill.strip() and len(skill.strip()) > 2 and 'copyright' not in skill.lower()
                    ]
            
            # Clean output - no raw HTML needed
            
            return job_data
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}", "job_id": job_id, "url": job_url}
        except Exception as e:
            return {"error": f"Parsing failed: {str(e)}", "job_id": job_id, "url": job_url}
    
    def extract_total_jobs_from_page(self, html: str) -> int:
        """Extract total number of jobs from page text"""
        # Look for pattern like "Displaying 30 out of 954+ jobs"
        match = re.search(r'Displaying\s+\d+\s+out\s+of\s+(\d+)\+?\s+jobs', html, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return 0
    
    def _fetch_page_worker(self, page_data: Tuple[int, str], delay: float) -> Tuple[int, List[str]]:
        """Worker function for parallel page fetching"""
        page_num, url = page_data
        session = self._get_session()
        
        # Add small delay to avoid overwhelming the server
        time.sleep(delay * (0.5 + 0.5 * threading.current_thread().ident % 10 / 10))
        
        try:
            response = session.get(url, timeout=15)
            response.raise_for_status()
            
            job_urls = self.extract_job_urls_from_page(response.text, self.base_url)
            
            with self.progress_lock:
                print(f"Page {page_num}: Found {len(job_urls)} job URLs")
            
            return page_num, job_urls
            
        except Exception as e:
            with self.progress_lock:
                print(f"Error scraping page {page_num}: {str(e)}")
            return page_num, []
    
    def get_job_urls_from_search_pages(self, max_pages: int = None, delay: float = 1.0) -> List[str]:
        """Get all job URLs by paginating through search results in parallel"""
        print(f"Starting to collect job URLs from search pages...")
        
        # First, get the first page to determine total jobs
        session = self._get_session()
        try:
            print(f"Fetching first page to determine total jobs...")
            response = session.get(self.base_url, timeout=15)
            response.raise_for_status()
            
            # Extract total jobs and calculate pages needed
            total_jobs = self.extract_total_jobs_from_page(response.text)
            if total_jobs > 0:
                # Each page has 30 jobs, so calculate total pages needed
                total_pages = (total_jobs + 29) // 30  # Round up
                print(f"Found {total_jobs} total jobs, will need {total_pages} pages")
            else:
                print("Could not determine total jobs, defaulting to sequential fetching")
                total_pages = 100  # Fallback
            
            # Get job URLs from first page
            first_page_urls = self.extract_job_urls_from_page(response.text, self.base_url)
            print(f"Page 1: Found {len(first_page_urls)} job URLs")
            
        except Exception as e:
            print(f"Error fetching first page: {str(e)}")
            return []
        
        # Limit pages if requested
        if max_pages and max_pages < total_pages:
            total_pages = max_pages
            print(f"Limited to {max_pages} pages")
        
        # Prepare page data for parallel fetching (skip page 1 since we already have it)
        page_data = []
        for page_num in range(2, total_pages + 1):
            offset = (page_num - 1) * 30
            if offset == 0:
                url = self.base_url
            else:
                url = f"{self.base_url}/{offset}"
            page_data.append((page_num, url))
        
        # Fetch remaining pages in parallel
        all_job_urls = set(first_page_urls)
        
        if page_data:
            print(f"Fetching remaining {len(page_data)} pages in parallel...")
            start_time = time.time()
            
            with ThreadPoolExecutor(max_workers=min(self.max_workers, len(page_data))) as executor:
                # Submit all page fetching tasks
                future_to_page = {
                    executor.submit(self._fetch_page_worker, page_info, delay): page_info
                    for page_info in page_data
                }
                
                # Process completed tasks
                for future in as_completed(future_to_page):
                    page_info = future_to_page[future]
                    try:
                        page_num, job_urls = future.result()
                        
                        # Add new URLs
                        new_urls = 0
                        for job_url in job_urls:
                            if job_url not in all_job_urls:
                                all_job_urls.add(job_url)
                                new_urls += 1
                        
                    except Exception as e:
                        page_num, _ = page_info
                        print(f"Error processing page {page_num}: {str(e)}")
            
            elapsed_time = time.time() - start_time
            print(f"Parallel page fetching completed in {elapsed_time:.1f} seconds")
        
        print(f"Collected {len(all_job_urls)} unique job URLs")
        return list(all_job_urls)
    
    def _scrape_job_worker(self, job_url: str, delay: float) -> Dict:
        """Worker function for parallel job scraping"""
        session = self._get_session()
        
        # Add small random delay to avoid thundering herd
        time.sleep(delay * (0.5 + 0.5 * threading.current_thread().ident % 10 / 10))
        
        job_data = self.scrape_job_details(job_url, session)
        job_id = job_data.get("job_id", "unknown")
        
        # Update progress
        with self.progress_lock:
            self.completed_count += 1
            if "error" in job_data:
                print(f"Progress: {self.completed_count}/{self.total_count} - Job {job_id}: ERROR - {job_data['error']}")
            elif not job_data.get("is_active", True):
                print(f"Progress: {self.completed_count}/{self.total_count} - Job {job_id}: UNAVAILABLE")
            else:
                print(f"Progress: {self.completed_count}/{self.total_count} - Job {job_id}: SUCCESS")
        
        return job_data
    
    def check_status_change(self, new_job_data: Dict, existing_filepath: str) -> Dict:
        """Check if job status has changed and update history"""
        try:
            with open(existing_filepath, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
            
            # Check if status changed from active to inactive
            was_active = existing_data.get("is_active", True)
            is_now_active = new_job_data.get("is_active", True)
            
            # Copy existing status history
            new_job_data["status_history"] = existing_data.get("status_history", [])
            
            if was_active and not is_now_active:
                # Job became inactive
                new_job_data["status_history"].append({
                    "status": "inactive",
                    "timestamp": datetime.now().isoformat(),
                    "reason": "Job became unavailable during re-scrape"
                })
                print(f"Job {new_job_data.get('job_id')} changed status: ACTIVE -> INACTIVE")
            elif not was_active and is_now_active:
                # Job became active again
                new_job_data["status_history"].append({
                    "status": "active",
                    "timestamp": datetime.now().isoformat(),
                    "reason": "Job became available again during re-scrape"
                })
                print(f"Job {new_job_data.get('job_id')} changed status: INACTIVE -> ACTIVE")
            
        except Exception as e:
            # If we can't read existing file, just use new data as-is
            pass
        
        return new_job_data

    def save_job_data(self, job_data: Dict) -> bool:
        """Save job data to individual JSON file"""
        job_id = job_data.get("job_id")
        if not job_id:
            return False
        
        filename = f"{job_id}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        # Check for status changes if file already exists
        if os.path.exists(filepath):
            job_data = self.check_status_change(job_data, filepath)
        else:
            # First time scraping this job, add initial status
            if job_data.get("is_active", True):
                job_data["status_history"].append({
                    "status": "active",
                    "timestamp": datetime.now().isoformat(),
                    "reason": "Job first discovered"
                })
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(job_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving job {job_id}: {str(e)}")
            return False
    
    def run(self, max_pages: int = None, delay: float = 1.5, limit_jobs: int = None):
        """Run the complete job scraping process"""
        print(f"Starting job posting scraper...")
        print(f"Output directory: {self.output_dir}")
        print(f"Max workers: {self.max_workers}")
        
        # Step 1: Get all job URLs
        job_urls = self.get_job_urls_from_search_pages(max_pages=max_pages, delay=delay)
        
        if not job_urls:
            print("No job URLs found. Exiting.")
            return
        
        if limit_jobs:
            job_urls = job_urls[:limit_jobs]
            print(f"Limited to {limit_jobs} jobs for testing")
        
        self.total_count = len(job_urls)
        print(f"\nStarting parallel scraping of {self.total_count} jobs...")
        
        # Step 2: Scrape jobs in parallel
        start_time = time.time()
        successful_jobs = 0
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_url = {
                executor.submit(self._scrape_job_worker, job_url, delay): job_url
                for job_url in job_urls
            }
            
            # Process completed tasks
            for future in as_completed(future_to_url):
                job_url = future_to_url[future]
                try:
                    job_data = future.result()
                    
                    # Save job data (including inactive jobs)
                    if "error" not in job_data and self.save_job_data(job_data):
                        successful_jobs += 1
                        with self.results_lock:
                            self.scraped_jobs.add(job_data.get("job_id"))
                    else:
                        with self.results_lock:
                            self.failed_jobs.append({
                                "url": job_url,
                                "error": job_data.get("error", "Unknown error"),
                                "timestamp": datetime.now().isoformat()
                            })
                        
                except Exception as e:
                    print(f"Error processing {job_url}: {str(e)}")
                    with self.results_lock:
                        self.failed_jobs.append({
                            "url": job_url,
                            "error": f"Worker error: {str(e)}",
                            "timestamp": datetime.now().isoformat()
                        })
        
        elapsed_time = time.time() - start_time
        print(f"\nScraping completed in {elapsed_time:.1f} seconds")
        print(f"Successful jobs: {successful_jobs}")
        
        # Count inactive jobs from successful scrapes
        inactive_jobs = 0
        for job_id in self.scraped_jobs:
            job_file = os.path.join(self.output_dir, f"{job_id}.json")
            try:
                with open(job_file, 'r', encoding='utf-8') as f:
                    job_data = json.load(f)
                    if not job_data.get("is_active", True):
                        inactive_jobs += 1
            except:
                pass
        
        active_jobs = successful_jobs - inactive_jobs
        error_jobs = len(self.failed_jobs)
        
        print(f"Active jobs: {active_jobs}")
        print(f"Inactive jobs: {inactive_jobs}")
        print(f"Failed jobs (errors): {error_jobs}")
        print(f"Success rate: {successful_jobs/self.total_count*100:.1f}%")
        
        # Save failed jobs log
        if self.failed_jobs:
            failed_log_path = os.path.join(self.output_dir, "failed_jobs.json")
            with open(failed_log_path, 'w', encoding='utf-8') as f:
                json.dump(self.failed_jobs, f, indent=2, ensure_ascii=False)
            print(f"Failed jobs logged to {failed_log_path}")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Scrape job postings from OnlineJobs.ph')
    parser.add_argument('--workers', type=int, help='Number of parallel workers (default: CPU count)')
    parser.add_argument('--delay', type=float, default=1.5, help='Delay between requests per worker (default: 1.5)')
    parser.add_argument('--max-pages', type=int, help='Maximum number of search pages to scrape')
    parser.add_argument('--limit-jobs', type=int, help='Limit number of jobs to scrape (for testing)')
    parser.add_argument('--output-dir', default='jobs', help='Output directory for job JSON files (default: jobs)')
    parser.add_argument('--test', action='store_true', help='Test mode - scrape only first page and limit to 10 jobs')
    
    args = parser.parse_args()
    
    if args.test:
        print("Running in test mode (first page, max 10 jobs)...")
        max_pages = 1
        limit_jobs = 10
    else:
        max_pages = args.max_pages
        limit_jobs = args.limit_jobs
    
    scraper = JobPostingScraper(max_workers=args.workers, output_dir=args.output_dir)
    scraper.run(max_pages=max_pages, delay=args.delay, limit_jobs=limit_jobs)


if __name__ == "__main__":
    main()