import json
import requests
from bs4 import BeautifulSoup
import time
import csv
from datetime import datetime
import re
from typing import Dict, List, Tuple, Any
import copy
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import os
from queue import Queue
import sys

class OnlineJobsScraperEnhanced:
    def __init__(self, json_file: str, max_workers: int = None):
        self.json_file = json_file
        self.base_url = "https://www.onlinejobs.ph/jobseekers/jobsearch?skill_tags="
        self.results = []
        self.enhanced_tree = {}
        self.max_workers = max_workers or os.cpu_count() or 4
        self.results_lock = threading.Lock()
        self.progress_lock = threading.Lock()
        self.completed_count = 0
        self.total_count = 0
        
    def _get_session(self):
        """Create a new session for each thread"""
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        return session
        
    def extract_job_count(self, html: str) -> int:
        """Extract the number of jobs from the HTML page"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Primary pattern: "Displaying X out of Y jobs"
        text = soup.get_text()
        display_pattern = r'Displaying\s*(\d+)\s*out\s*of\s*(\d+)\s*jobs'
        match = re.search(display_pattern, text, re.IGNORECASE)
        if match:
            # Return the total count (second number)
            return int(match.group(2))
        
        # Try to find in data layer if available
        datalayer_pattern = r'"search_result_count":\s*(\d+)'
        match = re.search(datalayer_pattern, html)
        if match:
            return int(match.group(1))
        
        return 0
    
    def scrape_job_count(self, skill_id: str, session: requests.Session = None) -> Tuple[int, str]:
        """Scrape the job count for a specific skill"""
        url = f"{self.base_url}{skill_id}"
        
        if session is None:
            session = self._get_session()
        
        try:
            response = session.get(url, timeout=10)
            response.raise_for_status()
            
            job_count = self.extract_job_count(response.text)
            return job_count, "Success"
            
        except requests.exceptions.RequestException as e:
            return 0, f"Error: {str(e)}"
        except Exception as e:
            return 0, f"Unexpected error: {str(e)}"
    
    def _scrape_worker(self, skill_data: Tuple[str, str, str], delay: float) -> Dict:
        """Worker function for parallel scraping"""
        skill_name, skill_id, path = skill_data
        session = self._get_session()
        
        # Add small random delay to avoid thundering herd
        time.sleep(delay * (0.5 + 0.5 * threading.current_thread().ident % 10 / 10))
        
        job_count, status = self.scrape_job_count(skill_id, session)
        
        result = {
            'skill': skill_name,
            'path': path,
            'skill_id': skill_id,
            'job_count': job_count,
            'status': status,
            'url': f"{self.base_url}{skill_id}",
            'timestamp': datetime.now().isoformat()
        }
        
        # Update progress
        with self.progress_lock:
            self.completed_count += 1
            print(f"Progress: {self.completed_count}/{self.total_count} - {skill_name}: {job_count} jobs ({status})")
        
        return result
    
    def process_tree_with_counts(self, data: Dict, job_counts: Dict[str, int], path: str = "") -> Dict:
        """Process the tree and create an enhanced structure with job counts"""
        result = {}
        
        for key, value in data.items():
            current_path = f"{path} > {key}" if path else key
            
            if isinstance(value, str):
                # Leaf node - add job count information
                job_count = job_counts.get(value, 0)
                result[key] = {
                    "id": value,
                    "job_count": job_count,
                    "type": "leaf"
                }
            elif isinstance(value, dict):
                # Branch node - recurse and calculate total jobs
                child_data = self.process_tree_with_counts(value, job_counts, current_path)
                total_jobs = sum(
                    item.get("job_count", 0) if isinstance(item, dict) else 0
                    for item in child_data.values()
                )
                total_jobs += sum(
                    item.get("total_jobs", 0) if isinstance(item, dict) else 0
                    for item in child_data.values()
                )
                
                result[key] = {
                    "children": child_data,
                    "total_jobs": total_jobs,
                    "type": "branch"
                }
        
        return result
    
    def run(self, delay: float = 1.0, limit: int = None):
        """Run the scraper with parallel workers"""
        # Load JSON data
        print(f"Loading data from {self.json_file}...")
        with open(self.json_file, 'r') as f:
            self.original_data = json.load(f)
        
        # Find all leaf nodes
        leaf_nodes = []
        self._find_leaf_nodes(self.original_data, leaf_nodes)
        
        if limit:
            leaf_nodes = leaf_nodes[:limit]
            print(f"Limiting to {limit} skills for testing")
        
        self.total_count = len(leaf_nodes)
        print(f"Found {self.total_count} leaf nodes to scrape")
        print(f"Using {self.max_workers} parallel workers")
        
        # Scrape job counts in parallel
        job_counts = {}
        print(f"\nStarting parallel scraping with {self.max_workers} workers...")
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_skill = {
                executor.submit(self._scrape_worker, skill_data, delay): skill_data
                for skill_data in leaf_nodes
            }
            
            # Process completed tasks
            for future in as_completed(future_to_skill):
                skill_data = future_to_skill[future]
                try:
                    result = future.result()
                    
                    # Thread-safe append to results
                    with self.results_lock:
                        self.results.append(result)
                        job_counts[result['skill_id']] = result['job_count']
                        
                except Exception as e:
                    skill_name, skill_id, path = skill_data
                    print(f"Error scraping {skill_name}: {str(e)}")
                    
                    with self.results_lock:
                        self.results.append({
                            'skill': skill_name,
                            'path': path,
                            'skill_id': skill_id,
                            'job_count': 0,
                            'status': f"Thread error: {str(e)}",
                            'url': f"{self.base_url}{skill_id}",
                            'timestamp': datetime.now().isoformat()
                        })
        
        elapsed_time = time.time() - start_time
        print(f"\nScraping completed in {elapsed_time:.1f} seconds")
        print(f"Average time per skill: {elapsed_time/self.total_count:.2f} seconds")
        
        # Create enhanced tree structure
        print("\nCreating enhanced tree structure with job counts...")
        self.enhanced_tree = self.process_tree_with_counts(self.original_data, job_counts)
        
        # Calculate statistics
        self._calculate_statistics()
    
    def _find_leaf_nodes(self, data: Dict, result: List, path: str = ""):
        """Recursively find all leaf nodes"""
        for key, value in data.items():
            current_path = f"{path} > {key}" if path else key
            
            if isinstance(value, str):
                result.append((key, value, current_path))
            elif isinstance(value, dict):
                self._find_leaf_nodes(value, result, current_path)
    
    def _calculate_statistics(self):
        """Calculate and display statistics"""
        successful_results = [r for r in self.results if r['job_count'] > 0]
        
        if successful_results:
            total_jobs = sum(r['job_count'] for r in successful_results)
            avg_jobs = total_jobs / len(successful_results)
            max_jobs = max(r['job_count'] for r in successful_results)
            min_jobs = min(r['job_count'] for r in successful_results)
            
            print(f"\nStatistics:")
            print(f"  Total skills scraped: {len(self.results)}")
            print(f"  Successful scrapes: {len(successful_results)}")
            print(f"  Total jobs found: {total_jobs:,}")
            print(f"  Average jobs per skill: {avg_jobs:.1f}")
            print(f"  Max jobs (single skill): {max_jobs:,}")
            print(f"  Min jobs (single skill): {min_jobs:,}")
    
    def save_results(self):
        """Save all results and enhanced tree"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save enhanced tree with job counts
        enhanced_filename = f"skills_with_jobs_{timestamp}.json"
        with open(enhanced_filename, 'w', encoding='utf-8') as f:
            json.dump(self.enhanced_tree, f, indent=2, ensure_ascii=False)
        print(f"\nEnhanced tree saved to {enhanced_filename}")
        
        # Save current enhanced tree for immediate use
        with open("skills_with_jobs_current.json", 'w', encoding='utf-8') as f:
            json.dump(self.enhanced_tree, f, indent=2, ensure_ascii=False)
        print(f"Current enhanced tree saved to skills_with_jobs_current.json")
        
        # Save detailed results CSV (overwrite latest file)
        csv_filename = "job_scrape_details_latest.csv"
        with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.results[0].keys())
            writer.writeheader()
            writer.writerows(self.results)
        print(f"Detailed results saved to {csv_filename}")
        
        # Top skills by job count
        sorted_results = sorted(
            [r for r in self.results if r['job_count'] > 0], 
            key=lambda x: x['job_count'], 
            reverse=True
        )[:20]
        
        print(f"\nTop 20 skills by job count:")
        for r in sorted_results:
            print(f"  {r['skill']}: {r['job_count']:,} jobs")


def main():
    """Main entry point for full scraping"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Scrape job counts from OnlineJobs.ph')
    parser.add_argument('--workers', type=int, help='Number of parallel workers (default: CPU count)')
    parser.add_argument('--delay', type=float, default=1.5, help='Delay between requests per worker (default: 1.5)')
    parser.add_argument('--test', action='store_true', help='Test mode - scrape only 10 skills')
    parser.add_argument('--limit', type=int, help='Limit number of skills to scrape')
    
    args = parser.parse_args()
    
    if args.test:
        print("Running in test mode (10 skills only)...")
        limit = 10
    else:
        limit = args.limit
    
    scraper = OnlineJobsScraperEnhanced("allskills_tree_clean.json", max_workers=args.workers)
    scraper.run(delay=args.delay, limit=limit)
    scraper.save_results()

def test_main():
    """Test entry point for scraping only 10 skills"""
    print("Running in test mode (10 skills only)...")
    scraper = OnlineJobsScraperEnhanced("allskills_tree_clean.json")
    scraper.run(delay=1.5, limit=10)
    scraper.save_results()

if __name__ == "__main__":
    main()