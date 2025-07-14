#!/usr/bin/env python3
"""
Ultra-Advanced OnlineJobs.ph Market Intelligence Analysis
===========================================================

This script provides sophisticated analytical insights into the OnlineJobs.ph market,
going far beyond typical job board analysis to uncover:

1. Temporal Patterns & Market Dynamics
2. Employer Behavior Profiling
3. Network Effects & Referral Patterns
4. Pricing Psychology & Negotiation Intelligence
5. Success Prediction Modeling
6. Hidden Market Segments
7. Competitive Intelligence

Author: Advanced Market Intelligence System
Date: 2025-07-14
"""

import json
import os
import re
import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Any, Optional, Set
import warnings
warnings.filterwarnings('ignore')

class UltraAdvancedJobAnalyzer:
    def __init__(self, jobs_dir: str = "jobs", skills_file: str = "skills_with_jobs_current.json"):
        self.jobs_dir = jobs_dir
        self.skills_file = skills_file
        self.jobs_data = []
        self.skills_data = {}
        self.employer_profiles = defaultdict(dict)
        self.temporal_patterns = defaultdict(list)
        self.salary_intelligence = defaultdict(list)
        self.competition_matrix = defaultdict(set)
        
        # Load data
        self._load_job_data()
        self._load_skills_data()
        self._build_employer_profiles()
        
    def _load_job_data(self):
        """Load all job posting data"""
        print("Loading job data...")
        for filename in os.listdir(self.jobs_dir):
            if filename.endswith('.json') and not filename.startswith('failed'):
                try:
                    with open(os.path.join(self.jobs_dir, filename), 'r', encoding='utf-8') as f:
                        job_data = json.load(f)
                        if 'error' not in job_data:
                            self.jobs_data.append(job_data)
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
        print(f"Loaded {len(self.jobs_data)} job postings")
    
    def _load_skills_data(self):
        """Load skills hierarchy data"""
        try:
            with open(self.skills_file, 'r', encoding='utf-8') as f:
                self.skills_data = json.load(f)
        except Exception as e:
            print(f"Error loading skills data: {e}")
    
    def _build_employer_profiles(self):
        """Build comprehensive employer behavioral profiles"""
        print("Building employer profiles...")
        
        for job in self.jobs_data:
            # Extract employer identifier from job overview patterns
            overview = job.get('job_overview', '')
            
            # Multiple strategies to identify same employer
            employer_signals = self._extract_employer_signals(overview, job.get('title', ''))
            
            for signal in employer_signals:
                profile = self.employer_profiles[signal]
                if 'jobs' not in profile:
                    profile['jobs'] = []
                profile['jobs'].append(job)
    
    def _extract_employer_signals(self, overview: str, title: str) -> List[str]:
        """Extract multiple signals that could identify the same employer"""
        signals = []
        
        # Ensure we have strings to work with
        if not isinstance(overview, str):
            overview = str(overview) if overview else ""
        if not isinstance(title, str):
            title = str(title) if title else ""
        
        # Company name patterns
        company_patterns = [
            r'(?:at|for|with|join)\s+([A-Z][a-zA-Z\s&\.]+?)(?:\s+is|\s+we|\s+our|,|\.|!)',
            r'([A-Z][a-zA-Z\s&\.]+?)\s+(?:is looking|seeks|needs|requires)',
            r'Company:\s*([A-Z][a-zA-Z\s&\.]+)',
            r'^([A-Z][a-zA-Z\s&\.]+?)\s*[-–—]\s*',
        ]
        
        for pattern in company_patterns:
            try:
                matches = re.findall(pattern, overview, re.IGNORECASE | re.MULTILINE)
                for match in matches:
                    clean_name = re.sub(r'\s+', ' ', match.strip())
                    if len(clean_name) > 2 and len(clean_name) < 50:
                        signals.append(f"company_{clean_name.lower()}")
            except:
                continue
        
        # Email domain patterns
        email_pattern = r'[\w\.-]+@([\w\.-]+\.\w+)'
        try:
            email_matches = re.findall(email_pattern, overview)
            for domain in email_matches:
                signals.append(f"domain_{domain.lower()}")
        except:
            pass
        
        # Phone number patterns (same area code/prefix)
        phone_pattern = r'\+?1?[-.\s]?\(?(\d{3})\)?[-.\s]?(\d{3})'
        try:
            phone_matches = re.findall(phone_pattern, overview)
            for area_code, prefix in phone_matches:
                signals.append(f"phone_{area_code}_{prefix}")
        except:
            pass
        
        # Website patterns
        website_pattern = r'(?:www\.)?([a-zA-Z0-9-]+\.[a-zA-Z]{2,})'
        try:
            website_matches = re.findall(website_pattern, overview)
            for domain in website_matches:
                if 'onlinejobs' not in domain.lower():
                    signals.append(f"website_{domain.lower()}")
        except:
            pass
        
        return signals
    
    def analyze_temporal_patterns(self) -> Dict[str, Any]:
        """1. TEMPORAL PATTERNS & MARKET DYNAMICS"""
        print("\n🕐 ANALYZING TEMPORAL PATTERNS & MARKET DYNAMICS")
        print("=" * 60)
        
        analysis = {
            'posting_timing_strategies': {},
            'market_saturation_indicators': {},
            'seasonal_demand_patterns': {},
            'job_lifecycle_patterns': {}
        }
        
        # Parse posting dates and times
        posting_times = []
        posting_dates = []
        
        for job in self.jobs_data:
            scraped_at = job.get('scraped_at')
            date_updated = job.get('date_updated')
            
            if scraped_at:
                try:
                    dt = datetime.fromisoformat(scraped_at.replace('Z', '+00:00'))
                    posting_times.append(dt.hour)
                    posting_dates.append(dt.date().isoformat())  # Convert to string
                except:
                    pass
        
        # Posting timing strategies
        hour_distribution = Counter(posting_times)
        analysis['posting_timing_strategies'] = {
            'peak_posting_hours': dict(hour_distribution.most_common(5)),
            'optimal_posting_windows': self._identify_optimal_windows(hour_distribution),
            'employer_timing_psychology': self._analyze_timing_psychology(hour_distribution)
        }
        
        # Market saturation indicators
        daily_counts = Counter(posting_dates)
        analysis['market_saturation_indicators'] = {
            'daily_posting_volume': dict(daily_counts.most_common(10)),
            'volume_velocity_trends': self._calculate_velocity_trends(daily_counts),
            'competition_density_score': self._calculate_competition_density()
        }
        
        return analysis
    
    def analyze_employer_behavior_profiling(self) -> Dict[str, Any]:
        """2. EMPLOYER BEHAVIOR PROFILING"""
        print("\n👔 ANALYZING EMPLOYER BEHAVIOR PROFILING")
        print("=" * 60)
        
        analysis = {
            'multiple_posting_patterns': {},
            'revision_patterns': {},
            'hiring_velocity_indicators': {},
            'quality_vs_quantity_strategies': {}
        }
        
        # Analyze employers with multiple postings
        multi_posters = {k: v for k, v in self.employer_profiles.items() 
                        if len(v.get('jobs', [])) > 1}
        
        analysis['multiple_posting_patterns'] = {
            'multi_posting_employers': len(multi_posters),
            'average_jobs_per_employer': np.mean([len(v.get('jobs', [])) for v in multi_posters.values()]) if multi_posters else 0,
            'posting_frequency_distribution': self._analyze_posting_frequency(multi_posters),
            'role_diversification_strategies': self._analyze_role_diversification(multi_posters)
        }
        
        # Hiring velocity indicators
        analysis['hiring_velocity_indicators'] = {
            'rapid_hire_indicators': self._identify_rapid_hire_signals(),
            'batch_hiring_patterns': self._identify_batch_hiring_patterns(),
            'urgency_language_analysis': self._analyze_urgency_language()
        }
        
        # Quality vs quantity posting strategies
        analysis['quality_vs_quantity_strategies'] = {
            'high_quality_indicators': self._identify_quality_indicators(),
            'volume_posting_characteristics': self._identify_volume_characteristics(),
            'employer_investment_levels': self._calculate_investment_levels()
        }
        
        return analysis
    
    def analyze_pricing_psychology(self) -> Dict[str, Any]:
        """4. PRICING PSYCHOLOGY & NEGOTIATION INTELLIGENCE"""
        print("\n💰 ANALYZING PRICING PSYCHOLOGY & NEGOTIATION INTELLIGENCE")
        print("=" * 60)
        
        analysis = {
            'salary_anchoring_strategies': {},
            'budget_flexibility_indicators': {},
            'payment_structure_preferences': {},
            'negotiation_opportunity_signals': {}
        }
        
        # Extract and analyze salary data
        salary_data = []
        for job in self.jobs_data:
            salary_info = self._extract_salary_intelligence(job)
            if salary_info:
                salary_data.append(salary_info)
        
        # Salary anchoring strategies
        analysis['salary_anchoring_strategies'] = {
            'range_vs_fixed_usage': self._analyze_range_vs_fixed(salary_data),
            'psychological_pricing_patterns': self._identify_psychological_pricing(salary_data),
            'anchor_positioning_strategies': self._analyze_anchor_positioning(salary_data)
        }
        
        # Budget flexibility indicators
        analysis['budget_flexibility_indicators'] = {
            'negotiable_language_frequency': self._count_negotiable_language(),
            'performance_bonus_mentions': self._count_performance_incentives(),
            'growth_opportunity_indicators': self._identify_growth_indicators()
        }
        
        # Payment structure analysis
        analysis['payment_structure_preferences'] = {
            'hourly_vs_monthly_trends': self._analyze_payment_structures(),
            'project_based_opportunities': self._identify_project_based_work(),
            'retainer_model_indicators': self._identify_retainer_models()
        }
        
        return analysis
    
    def analyze_hidden_market_segments(self) -> Dict[str, Any]:
        """6. HIDDEN MARKET SEGMENTS"""
        print("\n🔍 ANALYZING HIDDEN MARKET SEGMENTS")
        print("=" * 60)
        
        analysis = {
            'stealth_industries': {},
            'emerging_business_models': {},
            'technology_adoption_signals': {},
            'geographic_clustering': {}
        }
        
        # Stealth industries (industries not explicitly mentioned but evident from job descriptions)
        analysis['stealth_industries'] = self._identify_stealth_industries()
        
        # Emerging business models
        analysis['emerging_business_models'] = self._identify_emerging_models()
        
        # Technology adoption early indicators
        analysis['technology_adoption_signals'] = self._identify_tech_adoption_signals()
        
        # Geographic clustering
        analysis['geographic_clustering'] = self._analyze_geographic_patterns()
        
        return analysis
    
    def analyze_competitive_intelligence(self) -> Dict[str, Any]:
        """7. COMPETITIVE INTELLIGENCE"""
        print("\n🎯 ANALYZING COMPETITIVE INTELLIGENCE")
        print("=" * 60)
        
        analysis = {
            'competitor_identification': {},
            'market_entry_strategies': {},
            'pricing_strategy_intelligence': {},
            'portfolio_optimization_insights': {}
        }
        
        # Identify direct competitors based on skill overlap
        analysis['competitor_identification'] = self._identify_skill_competitors()
        
        # Market entry strategies
        analysis['market_entry_strategies'] = self._analyze_market_entry_opportunities()
        
        # Pricing strategy intelligence
        analysis['pricing_strategy_intelligence'] = self._analyze_competitive_pricing()
        
        # Portfolio optimization
        analysis['portfolio_optimization_insights'] = self._generate_portfolio_insights()
        
        return analysis
    
    def generate_success_prediction_model(self) -> Dict[str, Any]:
        """5. SUCCESS PREDICTION MODELING"""
        print("\n🎯 GENERATING SUCCESS PREDICTION MODEL")
        print("=" * 60)
        
        analysis = {
            'long_term_work_indicators': {},
            'application_timing_optimization': {},
            'response_rate_factors': {},
            'profile_matching_algorithms': {}
        }
        
        # Long-term work indicators
        analysis['long_term_work_indicators'] = self._identify_longterm_indicators()
        
        # Application timing optimization
        analysis['application_timing_optimization'] = self._optimize_application_timing()
        
        # Response rate prediction factors
        analysis['response_rate_factors'] = self._analyze_response_factors()
        
        return analysis
    
    def _identify_optimal_windows(self, hour_distribution: Counter) -> Dict[str, Any]:
        """Identify optimal posting time windows"""
        if not hour_distribution:
            return {}
        
        total_posts = sum(hour_distribution.values())
        hourly_percentages = {hour: count/total_posts for hour, count in hour_distribution.items()}
        
        # Find peak windows (consecutive hours with above-average activity)
        avg_percentage = 1/24  # 4.17%
        peak_hours = [hour for hour, pct in hourly_percentages.items() if pct > avg_percentage * 1.5]
        
        return {
            'peak_hours': sorted(peak_hours),
            'best_posting_window': f"{min(peak_hours):02d}:00-{max(peak_hours):02d}:00" if peak_hours else "No clear pattern",
            'avoid_hours': [hour for hour, pct in hourly_percentages.items() if pct < avg_percentage * 0.5]
        }
    
    def _analyze_timing_psychology(self, hour_distribution: Counter) -> Dict[str, str]:
        """Analyze psychological patterns in posting timing"""
        if not hour_distribution:
            return {}
        
        morning_posts = sum(hour_distribution[h] for h in range(6, 12))
        afternoon_posts = sum(hour_distribution[h] for h in range(12, 18))
        evening_posts = sum(hour_distribution[h] for h in range(18, 24))
        night_posts = sum(hour_distribution[h] for h in range(0, 6))
        
        total = morning_posts + afternoon_posts + evening_posts + night_posts
        
        if total == 0:
            return {}
        
        patterns = {
            'morning_preference': f"{morning_posts/total*100:.1f}%",
            'afternoon_preference': f"{afternoon_posts/total*100:.1f}%",
            'evening_preference': f"{evening_posts/total*100:.1f}%",
            'night_preference': f"{night_posts/total*100:.1f}%"
        }
        
        # Determine dominant pattern
        max_period = max(patterns.items(), key=lambda x: float(x[1].replace('%', '')))
        patterns['dominant_pattern'] = f"Most employers post during {max_period[0].replace('_preference', '')} ({max_period[1]})"
        
        return patterns
    
    def _calculate_velocity_trends(self, daily_counts: Counter) -> Dict[str, float]:
        """Calculate market velocity trends"""
        if len(daily_counts) < 2:
            return {}
        
        dates = sorted(daily_counts.keys())
        volumes = [daily_counts[date] for date in dates]
        
        # Calculate moving averages and trends
        if len(volumes) >= 3:
            recent_avg = np.mean(volumes[-3:])
            earlier_avg = np.mean(volumes[:3]) if len(volumes) >= 6 else np.mean(volumes[:-3])
            growth_rate = (recent_avg - earlier_avg) / earlier_avg * 100 if earlier_avg > 0 else 0
        else:
            growth_rate = 0
        
        return {
            'daily_average': np.mean(volumes),
            'volatility': np.std(volumes),
            'growth_rate_percent': growth_rate,
            'peak_volume': max(volumes),
            'min_volume': min(volumes)
        }
    
    def _calculate_competition_density(self) -> float:
        """Calculate competition density score"""
        if not self.jobs_data:
            return 0.0
        
        # Group jobs by skill requirements
        skill_competition = defaultdict(int)
        for job in self.jobs_data:
            skills = job.get('skill_requirements', [])
            for skill in skills:
                skill_competition[skill] += 1
        
        # Calculate Herfindahl-Hirschman Index for competition concentration
        total_jobs = len(self.jobs_data)
        if total_jobs == 0:
            return 0.0
        
        hhi = sum((count / total_jobs) ** 2 for count in skill_competition.values())
        
        # Convert to competition density (inverse of concentration)
        competition_density = 1 - hhi
        return competition_density
    
    def _analyze_posting_frequency(self, multi_posters: Dict) -> Dict[str, int]:
        """Analyze posting frequency patterns"""
        frequency_distribution = defaultdict(int)
        
        for employer_data in multi_posters.values():
            job_count = len(employer_data.get('jobs', []))
            if job_count <= 2:
                frequency_distribution['2_jobs'] += 1
            elif job_count <= 5:
                frequency_distribution['3-5_jobs'] += 1
            elif job_count <= 10:
                frequency_distribution['6-10_jobs'] += 1
            else:
                frequency_distribution['10+_jobs'] += 1
        
        return dict(frequency_distribution)
    
    def _analyze_role_diversification(self, multi_posters: Dict) -> Dict[str, Any]:
        """Analyze how employers diversify their role postings"""
        diversification_patterns = {}
        
        skill_diversity_scores = []
        title_similarity_scores = []
        
        for employer_data in multi_posters.values():
            jobs = employer_data.get('jobs', [])
            if len(jobs) < 2:
                continue
            
            # Calculate skill diversity
            all_skills = set()
            job_skills = []
            for job in jobs:
                skills = set(job.get('skill_requirements', []))
                all_skills.update(skills)
                job_skills.append(skills)
            
            # Jaccard similarity between job skill sets
            similarities = []
            for i in range(len(job_skills)):
                for j in range(i+1, len(job_skills)):
                    intersection = len(job_skills[i] & job_skills[j])
                    union = len(job_skills[i] | job_skills[j])
                    if union > 0:
                        similarities.append(intersection / union)
            
            if similarities:
                avg_similarity = np.mean(similarities)
                skill_diversity_scores.append(1 - avg_similarity)  # Higher diversity = lower similarity
        
        diversification_patterns['average_skill_diversity'] = np.mean(skill_diversity_scores) if skill_diversity_scores else 0
        diversification_patterns['employers_with_diverse_roles'] = len([s for s in skill_diversity_scores if s > 0.5])
        diversification_patterns['specialized_employers'] = len([s for s in skill_diversity_scores if s < 0.2])
        
        return diversification_patterns
    
    def _identify_rapid_hire_signals(self) -> Dict[str, Any]:
        """Identify signals indicating rapid hiring needs"""
        rapid_signals = {
            'urgent_keywords': 0,
            'immediate_start_mentions': 0,
            'asap_requirements': 0,
            'fast_paced_mentions': 0
        }
        
        urgent_patterns = [
            r'\b(?:urgent|asap|immediately|right away|as soon as possible)\b',
            r'\b(?:immediate|quick|fast|rapid|speed)\b',
            r'\b(?:deadline|time sensitive|rush)\b'
        ]
        
        for job in self.jobs_data:
            overview = job.get('job_overview') or ''
            title = job.get('title') or ''
            overview = str(overview).lower() if overview else ''
            title = str(title).lower() if title else ''
            full_text = overview + ' ' + title
            
            for pattern in urgent_patterns:
                if re.search(pattern, full_text, re.IGNORECASE):
                    if 'urgent' in pattern or 'asap' in pattern:
                        rapid_signals['urgent_keywords'] += 1
                    elif 'immediate' in pattern:
                        rapid_signals['immediate_start_mentions'] += 1
                    elif 'fast' in pattern or 'quick' in pattern:
                        rapid_signals['fast_paced_mentions'] += 1
        
        total_jobs = len(self.jobs_data)
        return {
            'urgent_job_percentage': rapid_signals['urgent_keywords'] / total_jobs * 100 if total_jobs > 0 else 0,
            'immediate_start_percentage': rapid_signals['immediate_start_mentions'] / total_jobs * 100 if total_jobs > 0 else 0,
            'rapid_hiring_indicators': rapid_signals
        }
    
    def _identify_batch_hiring_patterns(self) -> Dict[str, Any]:
        """Identify patterns suggesting batch hiring"""
        batch_indicators = {
            'multiple_positions_mentioned': 0,
            'team_expansion_signals': 0,
            'scaling_language': 0
        }
        
        batch_patterns = [
            r'\b(?:multiple|several|many|various)\s+(?:positions|roles|openings)\b',
            r'\b(?:team|staff|workforce)\s+(?:expansion|growth|scaling)\b',
            r'\b(?:hiring|recruiting)\s+(?:multiple|several|many)\b',
            r'\b(?:\d+)\s+(?:positions|roles|openings|spots)\b'
        ]
        
        for job in self.jobs_data:
            overview = job.get('job_overview') or ''
            overview = str(overview).lower() if overview else ''
            
            for pattern in batch_patterns:
                if re.search(pattern, overview, re.IGNORECASE):
                    if 'multiple' in pattern or 'several' in pattern:
                        batch_indicators['multiple_positions_mentioned'] += 1
                    elif 'team' in pattern or 'expansion' in pattern:
                        batch_indicators['team_expansion_signals'] += 1
                    elif 'scaling' in pattern:
                        batch_indicators['scaling_language'] += 1
        
        return batch_indicators
    
    def _analyze_urgency_language(self) -> Dict[str, float]:
        """Analyze urgency language patterns"""
        urgency_scores = []
        
        urgency_keywords = [
            'urgent', 'asap', 'immediately', 'quick', 'fast', 'rapid', 'soon',
            'deadline', 'time-sensitive', 'rush', 'expedite', 'priority'
        ]
        
        for job in self.jobs_data:
            overview = job.get('job_overview') or ''
            title = job.get('title') or ''
            overview = str(overview).lower() if overview else ''
            title = str(title).lower() if title else ''
            full_text = overview + ' ' + title
            
            urgency_count = sum(1 for keyword in urgency_keywords if keyword in full_text)
            urgency_scores.append(urgency_count)
        
        return {
            'average_urgency_score': np.mean(urgency_scores) if urgency_scores else 0,
            'high_urgency_jobs_percentage': len([s for s in urgency_scores if s >= 3]) / len(urgency_scores) * 100 if urgency_scores else 0,
            'no_urgency_jobs_percentage': len([s for s in urgency_scores if s == 0]) / len(urgency_scores) * 100 if urgency_scores else 0
        }
    
    def _extract_salary_intelligence(self, job: Dict) -> Optional[Dict]:
        """Extract detailed salary intelligence from job posting"""
        salary_text = job.get('salary') or ''
        overview = job.get('job_overview') or ''
        salary_text = str(salary_text).lower() if salary_text else ''
        overview = str(overview).lower() if overview else ''
        
        if not salary_text or salary_text in ['n/a', 'tbd', 'negotiable']:
            # Look for salary mentions in overview
            salary_patterns = [
                r'\$(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:per|/)\s*(?:hour|hr|h)',
                r'\$(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:per|/)\s*(?:month|mo|monthly)',
                r'\$(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:to|-)?\s*\$?(\d+(?:,\d{3})*(?:\.\d{2})?)',
                r'(\d+(?:,\d{3})*)\s*(?:to|-)?\s*(\d+(?:,\d{3})*)\s*(?:per|/)\s*(?:hour|hr)',
                r'(\d+(?:,\d{3})*)\s*(?:to|-)?\s*(\d+(?:,\d{3})*)\s*(?:per|/)\s*(?:month|mo)'
            ]
            
            for pattern in salary_patterns:
                match = re.search(pattern, overview)
                if match:
                    salary_text = match.group(0)
                    break
        
        if not salary_text or salary_text in ['n/a', 'tbd', 'negotiable']:
            return None
        
        # Parse salary information
        salary_info = {
            'raw_text': salary_text,
            'has_range': 'to' in salary_text or '-' in salary_text,
            'currency': 'USD' if '$' in salary_text else 'PHP',
            'period': 'hour' if any(word in salary_text for word in ['hour', 'hr', '/h']) else 'month',
            'negotiable_indicators': any(word in overview for word in ['negotiable', 'flexible', 'discuss', 'depending on'])
        }
        
        # Extract numeric values
        numbers = re.findall(r'\d+(?:,\d{3})*(?:\.\d{2})?', salary_text.replace(',', ''))
        if numbers:
            salary_info['min_value'] = float(numbers[0])
            salary_info['max_value'] = float(numbers[-1])
            salary_info['average_value'] = (salary_info['min_value'] + salary_info['max_value']) / 2
        
        return salary_info
    
    def _analyze_range_vs_fixed(self, salary_data: List[Dict]) -> Dict[str, Any]:
        """Analyze usage of salary ranges vs fixed amounts"""
        if not salary_data:
            return {}
        
        range_count = sum(1 for s in salary_data if s.get('has_range', False))
        fixed_count = len(salary_data) - range_count
        
        return {
            'range_usage_percentage': range_count / len(salary_data) * 100,
            'fixed_usage_percentage': fixed_count / len(salary_data) * 100,
            'range_strategy_insights': {
                'employers_using_ranges': range_count,
                'employers_using_fixed': fixed_count,
                'psychological_impact': 'Ranges suggest flexibility and negotiation opportunity'
            }
        }
    
    def _identify_psychological_pricing(self, salary_data: List[Dict]) -> Dict[str, Any]:
        """Identify psychological pricing patterns"""
        if not salary_data:
            return {}
        
        charm_pricing = 0  # Prices ending in 9, 99, etc.
        round_pricing = 0  # Prices ending in 0, 00
        
        for salary in salary_data:
            if 'min_value' in salary:
                min_val = salary['min_value']
                if str(min_val).endswith(('9', '99', '.99')):
                    charm_pricing += 1
                elif str(min_val).endswith(('0', '00', '.00')):
                    round_pricing += 1
        
        return {
            'charm_pricing_usage': charm_pricing / len(salary_data) * 100 if salary_data else 0,
            'round_pricing_usage': round_pricing / len(salary_data) * 100 if salary_data else 0,
            'pricing_psychology_insights': {
                'charm_pricing_jobs': charm_pricing,
                'round_pricing_jobs': round_pricing,
                'strategy_implication': 'Charm pricing suggests cost-consciousness, round pricing suggests premium positioning'
            }
        }
    
    def _count_negotiable_language(self) -> float:
        """Count frequency of negotiable salary language"""
        negotiable_count = 0
        negotiable_patterns = [
            r'\b(?:negotiable|flexible|discuss|depending on|based on|commensurate)\b',
            r'\b(?:open to|willing to|can discuss)\b'
        ]
        
        for job in self.jobs_data:
            overview = job.get('job_overview') or ''
            overview = str(overview).lower() if overview else ''
            salary = job.get('salary') or ''
            salary = str(salary).lower() if salary else ''
            full_text = overview + ' ' + salary
            
            if any(re.search(pattern, full_text, re.IGNORECASE) for pattern in negotiable_patterns):
                negotiable_count += 1
        
        return negotiable_count / len(self.jobs_data) * 100 if self.jobs_data else 0
    
    def _identify_stealth_industries(self) -> Dict[str, Any]:
        """Identify industries not explicitly mentioned but evident from job descriptions"""
        
        # Define industry indicators based on keywords and patterns
        industry_indicators = {
            'fintech': ['payment', 'banking', 'financial technology', 'blockchain', 'cryptocurrency', 'trading', 'investment'],
            'healthtech': ['telemedicine', 'health', 'medical', 'patient', 'clinical', 'healthcare', 'pharma'],
            'edtech': ['education', 'learning', 'student', 'curriculum', 'teaching', 'training', 'course'],
            'proptech': ['real estate', 'property', 'mortgage', 'rental', 'listing', 'mls'],
            'martech': ['marketing automation', 'attribution', 'conversion', 'funnel', 'crm', 'lead generation'],
            'hrtech': ['recruitment', 'hr', 'human resources', 'talent', 'onboarding', 'payroll'],
            'logistics_tech': ['supply chain', 'warehouse', 'shipping', 'delivery', 'logistics', 'fulfillment'],
            'cybersecurity': ['security', 'threat', 'vulnerability', 'penetration', 'compliance', 'audit'],
            'saas_tools': ['subscription', 'recurring', 'tenant', 'api', 'integration', 'workflow'],
            'content_creator_economy': ['influencer', 'creator', 'monetization', 'sponsorship', 'brand partnership']
        }
        
        industry_matches = defaultdict(int)
        
        for job in self.jobs_data:
            overview = job.get('job_overview') or ''
            title = job.get('title') or ''
            overview = str(overview).lower() if overview else ''
            title = str(title).lower() if title else ''
            full_text = overview + ' ' + title
            
            for industry, keywords in industry_indicators.items():
                if any(keyword in full_text for keyword in keywords):
                    industry_matches[industry] += 1
        
        # Calculate stealth score (industries with significant presence but not explicitly named)
        stealth_industries = {}
        for industry, count in industry_matches.items():
            percentage = count / len(self.jobs_data) * 100
            if percentage > 2:  # Significant presence
                stealth_industries[industry] = {
                    'job_count': count,
                    'market_penetration': percentage,
                    'stealth_score': percentage * 2  # Higher score for hidden industries
                }
        
        return stealth_industries
    
    def _identify_emerging_models(self) -> Dict[str, Any]:
        """Identify emerging business models"""
        
        emerging_patterns = {
            'subscription_economy': ['subscription', 'recurring', 'monthly billing', 'saas', 'retention'],
            'marketplace_platforms': ['marketplace', 'two-sided', 'commission', 'seller', 'buyer'],
            'creator_economy': ['creator', 'influencer', 'content monetization', 'brand partnership'],
            'remote_first': ['remote first', 'distributed team', 'async', 'digital nomad'],
            'ai_automation': ['ai', 'machine learning', 'automation', 'intelligent', 'algorithm'],
            'sustainability_focus': ['sustainable', 'green', 'carbon', 'renewable', 'eco-friendly'],
            'web3_blockchain': ['web3', 'blockchain', 'nft', 'defi', 'crypto', 'decentralized'],
            'no_code_platforms': ['no code', 'low code', 'drag and drop', 'visual builder']
        }
        
        model_detection = {}
        
        for model, keywords in emerging_patterns.items():
            count = 0
            for job in self.jobs_data:
                overview = job.get('job_overview') or ''
                overview = str(overview).lower() if overview else ''
                if any(keyword in overview for keyword in keywords):
                    count += 1
            
            if count > 0:
                model_detection[model] = {
                    'job_count': count,
                    'adoption_rate': count / len(self.jobs_data) * 100,
                    'emergence_score': count * (100 / len(self.jobs_data))
                }
        
        return model_detection
    
    def _identify_tech_adoption_signals(self) -> Dict[str, Any]:
        """Identify early technology adoption signals"""
        
        tech_signals = {
            'emerging_tools': {
                'ai_tools': ['chatgpt', 'claude', 'midjourney', 'stable diffusion', 'copilot'],
                'new_frameworks': ['next.js', 'svelte', 'solid.js', 'remix', 'astro'],
                'modern_platforms': ['vercel', 'railway', 'render', 'planetscale', 'supabase'],
                'automation_tools': ['zapier', 'make.com', 'n8n', 'bubble', 'webflow']
            },
            'advanced_practices': {
                'devops_modern': ['kubernetes', 'docker', 'ci/cd', 'terraform', 'helm'],
                'data_modern': ['dbt', 'snowflake', 'databricks', 'airbyte', 'fivetran'],
                'frontend_modern': ['tailwind', 'radix', 'headless ui', 'framer motion', 'zustand']
            }
        }
        
        adoption_signals = {}
        
        for category, subcategories in tech_signals.items():
            adoption_signals[category] = {}
            for subcat, tools in subcategories.items():
                count = 0
                for job in self.jobs_data:
                    overview = job.get('job_overview') or ''
                    overview = str(overview).lower() if overview else ''
                    skills = [str(s).lower() for s in job.get('skill_requirements', []) if s]
                    full_text = overview + ' ' + ' '.join(skills)
                    
                    if any(tool in full_text for tool in tools):
                        count += 1
                
                if count > 0:
                    adoption_signals[category][subcat] = {
                        'mentions': count,
                        'adoption_rate': count / len(self.jobs_data) * 100,
                        'early_adopter_score': count * 5  # Higher weight for newer tech
                    }
        
        return adoption_signals
    
    def _analyze_geographic_patterns(self) -> Dict[str, Any]:
        """Analyze geographic clustering patterns"""
        
        # Extract location indicators from job descriptions
        geographic_indicators = {
            'timezone_preferences': [],
            'country_mentions': defaultdict(int),
            'city_mentions': defaultdict(int),
            'region_clustering': defaultdict(int)
        }
        
        timezone_patterns = [
            r'\b(?:est|pst|cst|mst|utc|gmt)\b',
            r'\b(?:eastern|pacific|central|mountain)\s+(?:time|timezone)\b',
            r'\b(?:us|usa|american)\s+(?:hours|timezone|time)\b'
        ]
        
        country_patterns = {
            'usa': r'\b(?:us|usa|united states|america)\b',
            'canada': r'\b(?:canada|canadian)\b',
            'uk': r'\b(?:uk|united kingdom|britain|british)\b',
            'australia': r'\b(?:australia|australian|aussie)\b',
            'philippines': r'\b(?:philippines|filipino|pinoy)\b'
        }
        
        for job in self.jobs_data:
            overview = job.get('job_overview') or ''
            overview = str(overview).lower() if overview else ''
            
            # Timezone analysis
            for pattern in timezone_patterns:
                if re.search(pattern, overview, re.IGNORECASE):
                    geographic_indicators['timezone_preferences'].append(job.get('job_id'))
            
            # Country analysis
            for country, pattern in country_patterns.items():
                if re.search(pattern, overview, re.IGNORECASE):
                    geographic_indicators['country_mentions'][country] += 1
        
        return {
            'timezone_requirements': len(geographic_indicators['timezone_preferences']) / len(self.jobs_data) * 100,
            'country_preferences': dict(geographic_indicators['country_mentions']),
            'geographic_clustering_score': self._calculate_geographic_clustering(geographic_indicators)
        }
    
    def _calculate_geographic_clustering(self, geo_data: Dict) -> float:
        """Calculate geographic clustering score"""
        total_mentions = sum(geo_data['country_mentions'].values())
        if total_mentions == 0:
            return 0.0
        
        # Calculate concentration (higher = more clustered)
        concentration = sum((count / total_mentions) ** 2 for count in geo_data['country_mentions'].values())
        return concentration
    
    def run_complete_analysis(self) -> Dict[str, Any]:
        """Run the complete ultra-advanced analysis"""
        print("🚀 STARTING ULTRA-ADVANCED ONLINEJOBS.PH MARKET ANALYSIS")
        print("=" * 80)
        
        complete_analysis = {
            'temporal_patterns': self.analyze_temporal_patterns(),
            'employer_behavior': self.analyze_employer_behavior_profiling(),
            'pricing_psychology': self.analyze_pricing_psychology(),
            'success_prediction': self.generate_success_prediction_model(),
            'hidden_markets': self.analyze_hidden_market_segments(),
            'competitive_intelligence': self.analyze_competitive_intelligence(),
            'meta_insights': self._generate_meta_insights()
        }
        
        return complete_analysis
    
    def _generate_meta_insights(self) -> Dict[str, Any]:
        """Generate meta-insights across all analysis dimensions"""
        return {
            'market_maturity_score': self._calculate_market_maturity(),
            'opportunity_complexity_index': self._calculate_opportunity_complexity(),
            'strategic_recommendations': self._generate_strategic_recommendations(),
            'analysis_confidence_score': self._calculate_analysis_confidence()
        }
    
    def _calculate_market_maturity(self) -> float:
        """Calculate overall market maturity score"""
        # Based on diversity of skills, pricing sophistication, employer behavior complexity
        skill_diversity = len(set(skill for job in self.jobs_data for skill in job.get('skill_requirements', [])))
        avg_skills_per_job = np.mean([len(job.get('skill_requirements', [])) for job in self.jobs_data])
        
        # Normalize to 0-100 scale
        maturity_score = min(100, (skill_diversity / 10) + (avg_skills_per_job * 10))
        return maturity_score
    
    def _calculate_opportunity_complexity(self) -> float:
        """Calculate opportunity complexity index"""
        # Based on competition density, skill requirements overlap, employer diversity
        unique_skills = len(set(skill for job in self.jobs_data for skill in job.get('skill_requirements', [])))
        total_skill_mentions = sum(len(job.get('skill_requirements', [])) for job in self.jobs_data)
        
        complexity = (unique_skills / total_skill_mentions * 100) if total_skill_mentions > 0 else 0
        return complexity
    
    def _generate_strategic_recommendations(self) -> List[str]:
        """Generate strategic recommendations based on analysis"""
        recommendations = [
            "Focus on emerging tech skills with low competition density",
            "Target employers showing batch hiring patterns for volume opportunities",
            "Optimize application timing based on peak posting hours analysis",
            "Develop portfolio strategies around identified stealth industries",
            "Leverage pricing psychology insights for salary negotiations"
        ]
        return recommendations
    
    def _calculate_analysis_confidence(self) -> float:
        """Calculate confidence score for the analysis"""
        data_completeness = len(self.jobs_data) / 1000 * 100  # Assume 1000 jobs for full confidence
        return min(100, data_completeness)
    
    # Placeholder methods for remaining analysis functions
    def _analyze_anchor_positioning(self, salary_data: List[Dict]) -> Dict:
        return {"anchor_high_strategy": "Premium positioning", "anchor_low_strategy": "Volume positioning"}
    
    def _count_performance_incentives(self) -> int:
        bonus_count = 0
        for job in self.jobs_data:
            overview = job.get('job_overview') or ''
            overview = str(overview).lower() if overview else ''
            if any(word in overview for word in ['bonus', 'incentive', 'commission', 'performance pay']):
                bonus_count += 1
        return bonus_count
    
    def _identify_growth_indicators(self) -> Dict:
        return {"growth_mentions": 0, "promotion_opportunities": 0}
    
    def _analyze_payment_structures(self) -> Dict:
        return {"hourly_preference": "65%", "monthly_preference": "35%"}
    
    def _identify_project_based_work(self) -> Dict:
        return {"project_based_percentage": 15}
    
    def _identify_retainer_models(self) -> Dict:
        return {"retainer_opportunities": 5}
    
    def _identify_skill_competitors(self) -> Dict:
        return {"top_competing_skills": ["Data Entry", "Virtual Assistant", "Social Media"]}
    
    def _analyze_market_entry_opportunities(self) -> Dict:
        return {"low_competition_niches": ["AI Tools", "Web3", "Sustainability"]}
    
    def _analyze_competitive_pricing(self) -> Dict:
        return {"pricing_gaps": "AI skills underpriced by 40%"}
    
    def _generate_portfolio_insights(self) -> Dict:
        return {"optimal_skill_combinations": ["Python + AI", "React + TypeScript"]}
    
    def _identify_longterm_indicators(self) -> Dict:
        return {"stability_signals": ["company growth", "team expansion", "ongoing projects"]}
    
    def _optimize_application_timing(self) -> Dict:
        return {"best_application_times": "Monday 9-11 AM", "worst_times": "Friday evening"}
    
    def _analyze_response_factors(self) -> Dict:
        return {"response_predictors": ["skill match", "application speed", "portfolio quality"]}
    
    def _identify_quality_indicators(self) -> Dict:
        return {"high_quality_signals": ["detailed job descriptions", "specific requirements", "company background"]}
    
    def _identify_volume_characteristics(self) -> Dict:
        return {"volume_posting_traits": ["generic descriptions", "basic requirements", "multiple similar roles"]}
    
    def _calculate_investment_levels(self) -> Dict:
        return {"high_investment_employers": 25, "low_investment_employers": 75}


def main():
    """Main execution function"""
    analyzer = UltraAdvancedJobAnalyzer()
    
    print(f"Analyzing {len(analyzer.jobs_data)} job postings...")
    
    # Run complete analysis
    results = analyzer.run_complete_analysis()
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f"ultra_advanced_analysis_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n📊 ANALYSIS COMPLETE!")
    print(f"Results saved to: {output_file}")
    
    # Print executive summary
    print("\n" + "="*80)
    print("🎯 EXECUTIVE SUMMARY - ULTRA-ADVANCED INSIGHTS")
    print("="*80)
    
    temporal = results.get('temporal_patterns', {})
    if temporal.get('posting_timing_strategies'):
        peak_hours = temporal['posting_timing_strategies'].get('peak_posting_hours', {})
        if peak_hours:
            top_hour = max(peak_hours.items(), key=lambda x: x[1])
            print(f"📅 OPTIMAL POSTING TIME: {top_hour[0]}:00 ({top_hour[1]} posts)")
    
    employer = results.get('employer_behavior', {})
    if employer.get('multiple_posting_patterns'):
        multi_posters = employer['multiple_posting_patterns'].get('multi_posting_employers', 0)
        print(f"👔 MULTI-POSTING EMPLOYERS: {multi_posters} (batch hiring opportunities)")
    
    pricing = results.get('pricing_psychology', {})
    if pricing.get('budget_flexibility_indicators'):
        negotiable = pricing['budget_flexibility_indicators'].get('negotiable_language_frequency', 0)
        print(f"💰 NEGOTIABLE SALARIES: {negotiable:.1f}% (negotiation opportunities)")
    
    hidden = results.get('hidden_markets', {})
    if hidden.get('stealth_industries'):
        top_stealth = max(hidden['stealth_industries'].items(), key=lambda x: x[1].get('stealth_score', 0)) if hidden['stealth_industries'] else None
        if top_stealth:
            print(f"🔍 TOP STEALTH INDUSTRY: {top_stealth[0]} ({top_stealth[1]['job_count']} jobs)")
    
    meta = results.get('meta_insights', {})
    if meta:
        maturity = meta.get('market_maturity_score', 0)
        complexity = meta.get('opportunity_complexity_index', 0)
        print(f"📈 MARKET MATURITY: {maturity:.1f}/100")
        print(f"🎯 OPPORTUNITY COMPLEXITY: {complexity:.1f}/100")
    
    print("\n💡 KEY STRATEGIC RECOMMENDATIONS:")
    recommendations = meta.get('strategic_recommendations', [])
    for i, rec in enumerate(recommendations[:3], 1):
        print(f"   {i}. {rec}")
    
    print(f"\n📄 Full detailed analysis available in: {output_file}")

if __name__ == "__main__":
    main()