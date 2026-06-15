#!/usr/bin/env python3
"""
NayePankh Foundation — Automated Data Analytics Pipeline
Processes donor metrics, channel analysis, and generates strategic reports.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# Configure paths
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_ROOT, 'data')
OUTPUT_DIR = os.path.join(REPO_ROOT, 'outputs')

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_donor_data():
    """Load donor dataset from CSV."""
    csv_path = os.path.join(DATA_DIR, 'donor_dataset.csv')
    df = pd.read_csv(csv_path)
    df['DonationDate'] = pd.to_datetime(df['DonationDate'])
    return df

def generate_age_distribution_analysis(df):
    """Analyze and visualize age distribution of donors."""
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Age'], bins=8, kde=True, color='teal', edgecolor='black')
    plt.title('NayePankh Donor Base — Age Demographics', fontsize=14, fontweight='bold')
    plt.xlabel('Age (years)', fontsize=12)
    plt.ylabel('Number of Donors', fontsize=12)
    plt.tight_layout()
    
    output_path = os.path.join(OUTPUT_DIR, 'age_distribution.png')
    plt.savefig(output_path, dpi=300)
    print(f"✓ Age distribution analysis saved to {output_path}")
    plt.close()

def generate_donation_channel_analysis(df):
    """Analyze donation channels (Online vs Offline)."""
    plt.figure(figsize=(10, 6))
    channel_data = df.groupby('Channel')['DonationAmount'].agg(['sum', 'mean', 'count'])
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Total donations by channel
    channel_data['sum'].plot(kind='bar', ax=axes[0], color=['#FF6B6B', '#4ECDC4'])
    axes[0].set_title('Total Donations by Channel', fontweight='bold')
    axes[0].set_ylabel('Amount (₹)')
    axes[0].set_xlabel('')
    
    # Count of donors by channel
    channel_data['count'].plot(kind='bar', ax=axes[1], color=['#FF6B6B', '#4ECDC4'])
    axes[1].set_title('Donor Count by Channel', fontweight='bold')
    axes[1].set_ylabel('Count')
    axes[1].set_xlabel('')
    
    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, 'channel_analysis.png')
    plt.savefig(output_path, dpi=300)
    print(f"✓ Channel analysis saved to {output_path}")
    plt.close()

def generate_frequency_analysis(df):
    """Analyze donation frequency patterns."""
    plt.figure(figsize=(10, 6))
    frequency_data = df.groupby('Frequency')['DonationAmount'].agg(['sum', 'count', 'mean'])
    
    frequency_order = ['One-time', 'Quarterly', 'Monthly', 'Yearly']
    frequency_data = frequency_data.reindex(frequency_order)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Total by frequency
    frequency_data['sum'].plot(kind='bar', ax=axes[0], color='#95E1D3')
    axes[0].set_title('Total Donations by Frequency', fontweight='bold')
    axes[0].set_ylabel('Amount (₹)')
    axes[0].set_xlabel('')
    
    # Average by frequency
    frequency_data['mean'].plot(kind='bar', ax=axes[1], color='#F38181')
    axes[1].set_title('Average Donation by Frequency', fontweight='bold')
    axes[1].set_ylabel('Amount (₹)')
    axes[1].set_xlabel('')
    
    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, 'frequency_analysis.png')
    plt.savefig(output_path, dpi=300)
    print(f"✓ Frequency analysis saved to {output_path}")
    plt.close()

def generate_summary_report(df):
    """Generate text-based summary report."""
    report = f"""
================================================================================
        NayePankh Foundation — Donor Analytics Report
        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
================================================================================

📊 KEY METRICS:
  • Total Donors: {len(df)}
  • Total Donations: ₹{df['DonationAmount'].sum():,.0f}
  • Average Donation: ₹{df['DonationAmount'].mean():,.0f}
  • Median Donation: ₹{df['DonationAmount'].median():,.0f}
  • Donation Range: ₹{df['DonationAmount'].min():,} - ₹{df['DonationAmount'].max():,}

👥 DEMOGRAPHIC INSIGHTS:
  • Average Donor Age: {df['Age'].mean():.1f} years
  • Age Range: {df['Age'].min()} - {df['Age'].max()} years

📱 CHANNEL PERFORMANCE:
{df.groupby('Channel').agg({'DonationAmount': ['sum', 'count', 'mean']}).to_string()}

🔄 DONATION FREQUENCY:
{df.groupby('Frequency').agg({'DonationAmount': ['sum', 'count', 'mean']}).to_string()}

🏙️ TOP CITIES BY DONATIONS:
{df.groupby('City')['DonationAmount'].agg(['sum', 'count']).sort_values('sum', ascending=False).to_string()}

================================================================================
    Analysis complete. Visualizations saved to outputs/ directory.
================================================================================
"""
    
    report_path = os.path.join(OUTPUT_DIR, 'donor_analysis_report.txt')
    with open(report_path, 'w') as f:
        f.write(report)
    
    print(report)
    print(f"\n✓ Report saved to {report_path}")

def main():
    """Execute the complete analytics pipeline."""
    print("🚀 Starting NayePankh Donor Analytics Pipeline...")
    print(f"📂 Working directory: {REPO_ROOT}\n")
    
    try:
        # Load data
        df = load_donor_data()
        print(f"✓ Loaded {len(df)} donor records\n")
        
        # Generate analyses
        print("📈 Generating analyses...")
        generate_age_distribution_analysis(df)
        generate_donation_channel_analysis(df)
        generate_frequency_analysis(df)
        generate_summary_report(df)
        
        print("\n✅ Pipeline execution completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during pipeline execution: {e}")
        raise

if __name__ == "__main__":
    main()
