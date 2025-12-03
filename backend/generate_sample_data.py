"""
Sample data generator for testing the analytics report generator.
Creates a realistic marketing/ad-tech dataset.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_data(output_file='sample_marketing_data.csv', days=30):
    """Generate sample marketing analytics data"""
    
    # Generate date range
    start_date = datetime.now() - timedelta(days=days)
    dates = pd.date_range(start=start_date, periods=days, freq='D')
    
    # Generate realistic marketing data
    np.random.seed(42)  # For reproducibility
    
    data = {
        'date': dates,
        'impressions': np.random.randint(5000, 25000, days),
        'clicks': np.random.randint(100, 800, days),
        'conversions': np.random.randint(5, 80, days),
        'spend': np.random.uniform(200, 1500, days).round(2),
        'revenue': np.random.uniform(500, 3000, days).round(2),
        'campaign_name': np.random.choice(['Summer Sale', 'Back to School', 'Holiday Special', 'New Product Launch'], days),
        'device_type': np.random.choice(['Mobile', 'Desktop', 'Tablet'], days, p=[0.6, 0.3, 0.1]),
        'city': np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia'], days),
        'traffic_source': np.random.choice(['Organic', 'Paid Search', 'Social Media', 'Direct', 'Email'], days),
        'day_of_week': [d.strftime('%A') for d in dates],
        'weather': np.random.choice(['Sunny', 'Cloudy', 'Rainy', 'Clear'], days),
        'temperature': np.random.randint(50, 85, days)
    }
    
    df = pd.DataFrame(data)
    
    # Calculate derived metrics
    df['ctr'] = (df['clicks'] / df['impressions'] * 100).round(2)
    df['conversion_rate'] = (df['conversions'] / df['clicks'] * 100).round(2)
    df['roas'] = (df['revenue'] / df['spend']).round(2)
    df['cpc'] = (df['spend'] / df['clicks']).round(2)
    
    # Add some patterns
    # Weekends have higher traffic
    weekend_mask = df['day_of_week'].isin(['Saturday', 'Sunday'])
    df.loc[weekend_mask, 'impressions'] = (df.loc[weekend_mask, 'impressions'] * 1.3).astype(int)
    df.loc[weekend_mask, 'clicks'] = (df.loc[weekend_mask, 'clicks'] * 1.2).astype(int)
    
    # Rainy days have lower foot traffic (affecting conversions)
    rainy_mask = df['weather'] == 'Rainy'
    df.loc[rainy_mask, 'conversions'] = (df.loc[rainy_mask, 'conversions'] * 0.8).astype(int)
    
    # Save to CSV
    df.to_csv(output_file, index=False)
    print(f"✅ Sample data generated: {output_file}")
    print(f"   Rows: {len(df)}")
    print(f"   Columns: {len(df.columns)}")
    print(f"   Date range: {df['date'].min()} to {df['date'].max()}")
    return df

if __name__ == '__main__':
    generate_sample_data()

