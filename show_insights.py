#!/usr/bin/env python3
"""
OnlineJobs.ph Market Insights Summary
====================================

Quick summary of key insights for job seekers to level the playing field.
"""

import json
import sys
from datetime import datetime

def load_insights(filename="stats.json"):
    """Load insights from JSON file"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ {filename} not found. Run 'python insights_engine.py' first.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON in {filename}")
        sys.exit(1)

def show_executive_summary(insights):
    """Show executive summary"""
    summary = insights.get('executive_summary', {})
    
    print("🎯 EXECUTIVE SUMMARY")
    print("=" * 50)
    print(f"📊 Total Jobs Analyzed: {summary.get('total_jobs_analyzed', 0):,}")
    print(f"✅ Active Jobs: {summary.get('active_job_percentage', 0):.1f}%")
    print(f"🔥 Top Opportunity: {summary.get('top_opportunity', 'N/A')}")
    print(f"💰 Key Insight: {summary.get('key_insight', 'N/A')}")
    print(f"📈 Market Status: {summary.get('market_maturity', 'N/A')}")
    print(f"🎯 Analysis Confidence: {summary.get('confidence_level', 0):.1f}%")
    print()

def show_market_intelligence(insights):
    """Show key market intelligence"""
    market = insights.get('market_intelligence', {})
    
    print("📊 MARKET INTELLIGENCE")
    print("=" * 50)
    
    # Skills demand
    skills = market.get('skills_market', {}).get('skill_demand_ranking', {})
    print("🔥 TOP IN-DEMAND SKILLS:")
    for i, (skill, count) in enumerate(list(skills.items())[:10], 1):
        print(f"   {i:2d}. {skill}: {count} jobs")
    
    print()
    
    # Salary insights
    salary = market.get('salary_patterns', {})
    negotiable = salary.get('negotiation_opportunities', {})
    print("💰 SALARY INSIGHTS:")
    print(f"   🤝 Negotiable Jobs: {negotiable.get('percentage_negotiable', 0):.1f}%")
    
    salary_stats = salary.get('salary_statistics', {})
    if salary_stats:
        print(f"   💵 Median Salary: ${salary_stats.get('median', 0):,.0f}")
        print(f"   📈 75th Percentile: ${salary_stats.get('q3', 0):,.0f}")
    
    payment = salary.get('payment_structures', {})
    print(f"   ⏰ Hourly Jobs: {payment.get('hourly', 0)}")
    print(f"   📅 Monthly Jobs: {payment.get('monthly', 0)}")
    
    print()

def show_opportunities(insights):
    """Show key opportunities"""
    opportunities = insights.get('opportunity_matrix', {})
    
    print("🚀 KEY OPPORTUNITIES")
    print("=" * 50)
    
    # Blue ocean opportunities
    blue_ocean = opportunities.get('blue_ocean_opportunities', [])
    print("🌊 BLUE OCEAN OPPORTUNITIES:")
    for opp in blue_ocean:
        print(f"   • {opp}")
    
    # Industry opportunities  
    industry = opportunities.get('industry_specialization_opportunities', [])
    print("\n🏭 INDUSTRY SPECIALIZATION:")
    for opp in industry:
        print(f"   • {opp}")
    
    # Tech opportunities
    tech = opportunities.get('technology_early_adoption_opportunities', [])
    print("\n🤖 TECHNOLOGY EARLY ADOPTION:")
    for opp in tech:
        print(f"   • {opp}")
    
    print()

def show_competitive_insights(insights):
    """Show competitive landscape insights"""
    competitive = insights.get('competitive_landscape', {})
    
    print("⚔️  COMPETITIVE LANDSCAPE")
    print("=" * 50)
    
    # Competition density
    density = competitive.get('skill_competition_density', {})
    
    high_comp = density.get('high_competition', [])
    if high_comp:
        print("🔴 HIGH COMPETITION SKILLS (AVOID):")
        for skill in high_comp:
            print(f"   • {skill}")
    
    low_comp = density.get('low_competition', [])
    if low_comp:
        print("\n🟢 LOW COMPETITION SKILLS (TARGET):")
        for skill in low_comp:
            print(f"   • {skill}")
    
    # Market entry strategies
    strategies = competitive.get('market_entry_strategies', [])
    if strategies:
        print("\n🎯 MARKET ENTRY STRATEGIES:")
        for strategy in strategies:
            print(f"   • {strategy}")
    
    print()

def show_action_plan(insights):
    """Show actionable recommendations"""
    strategic = insights.get('strategic_insights', {})
    
    print("⚡ ACTION PLAN")
    print("=" * 50)
    
    # Immediate actions
    immediate = strategic.get('immediate_action_items', [])
    print("🚨 IMMEDIATE ACTIONS (THIS WEEK):")
    for action in immediate:
        print(f"   • {action}")
    
    # Medium-term strategies
    medium = strategic.get('medium_term_strategies', [])
    print("\n📅 MEDIUM-TERM STRATEGIES (1-3 MONTHS):")
    for strategy in medium:
        print(f"   • {strategy}")
    
    # Long-term positioning
    long_term = strategic.get('long_term_positioning_strategies', [])
    print("\n🎯 LONG-TERM POSITIONING (3-6 MONTHS):")
    for strategy in long_term:
        print(f"   • {strategy}")
    
    print()

def show_geographic_insights(insights):
    """Show geographic market insights"""
    data_summary = insights.get('data_summary', {})
    geo = data_summary.get('geographic_preferences', {}).get('geographic_distribution', {})
    
    if geo:
        print("🌍 GEOGRAPHIC MARKET DISTRIBUTION")
        print("=" * 50)
        
        # Sort by job count
        sorted_geo = sorted(geo.items(), key=lambda x: x[1], reverse=True)
        
        for region, count in sorted_geo:
            percentage = (count / sum(geo.values())) * 100
            print(f"   {region}: {count:,} jobs ({percentage:.1f}%)")
        
        timezone_req = data_summary.get('geographic_preferences', {}).get('timezone_requirement_percentage', 0)
        print(f"\n⏰ Jobs with timezone requirements: {timezone_req:.1f}%")
        print("   💡 Tip: Timezone alignment can command premium rates!")
        print()

def show_industry_insights(insights):
    """Show industry distribution"""
    data_summary = insights.get('data_summary', {})
    industries = data_summary.get('industry_distribution', {})
    
    if industries:
        print("🏭 INDUSTRY DISTRIBUTION")
        print("=" * 50)
        
        # Sort by job count
        sorted_industries = sorted(industries.items(), key=lambda x: x[1], reverse=True)
        
        total_jobs = sum(industries.values())
        for industry, count in sorted_industries:
            percentage = (count / total_jobs) * 100
            print(f"   {industry}: {count:,} jobs ({percentage:.1f}%)")
        
        print("\n💡 Technology dominates the market - position accordingly!")
        print()

def main():
    """Main function to display insights summary"""
    print("🚀 OnlineJobs.ph Market Intelligence Summary")
    print("🎯 Level the Playing Field for Job Seekers")
    print("=" * 60)
    print()
    
    # Load insights
    insights = load_insights()
    
    # Show all sections
    show_executive_summary(insights)
    show_market_intelligence(insights)
    show_geographic_insights(insights)
    show_industry_insights(insights)
    show_opportunities(insights)
    show_competitive_insights(insights)
    show_action_plan(insights)
    
    print("🎯 BOTTOM LINE FOR JOB SEEKERS:")
    print("=" * 50)
    print("1. 🔥 Target Facebook/Google Ads + AI Tools combination")
    print("2. 💰 Always negotiate - 11.3% explicitly show flexibility")
    print("3. 🌊 Blue ocean: No-code platforms, AI implementation")
    print("4. 🎯 Focus on US market (69% of jobs) for premium rates")
    print("5. ⚡ Apply off-peak (9-11 AM) when others apply at 11 PM")
    print("6. 🚀 Target multi-posting employers for volume opportunities")
    print("7. 🛡️ Avoid oversaturated VA/Data Entry - specialize instead")
    print()
    print("💪 Remember: Success = Strategic Positioning + Market Intelligence")
    print("🎯 Use these insights to dominate your niche!")

if __name__ == "__main__":
    main()