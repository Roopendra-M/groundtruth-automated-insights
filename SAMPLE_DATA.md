# Sample CSV Data Format

To test the application, you can create a CSV file with marketing/ad-tech data. Here are some example column structures:

## Example 1: Ad Campaign Data

```csv
date,impressions,clicks,conversions,spend,revenue,campaign_name,device_type,city
2024-01-01,10000,250,15,500,750,Campaign A,Mobile,New York
2024-01-02,12000,300,18,600,900,Campaign A,Desktop,Los Angeles
2024-01-03,8000,200,12,400,600,Campaign B,Tablet,Chicago
```

## Example 2: Website Analytics

```csv
date,visitors,page_views,bounce_rate,avg_session_duration,conversion_rate,traffic_source,country
2024-01-01,5000,15000,35.5,180,2.5,Organic,USA
2024-01-02,5500,16500,32.1,195,2.8,Paid,USA
2024-01-03,4800,14400,38.2,165,2.1,Direct,Canada
```

## Example 3: Retail Foot Traffic

```csv
date,foot_traffic,sales,weather,temperature,day_of_week,location
2024-01-01,1200,15000,Sunny,72,Monday,Store A
2024-01-02,1500,18000,Rainy,65,Tuesday,Store A
2024-01-03,1100,14000,Cloudy,68,Wednesday,Store B
```

## Tips for Creating Test Data

1. **Include Date/Time Columns**: The AI can analyze temporal patterns
2. **Mix Numeric and Categorical Data**: Better for correlation analysis
3. **Include Geographic Data**: City, country, region columns enable location-based insights
4. **Add Performance Metrics**: Clicks, conversions, revenue, etc.
5. **Include Contextual Data**: Weather, day of week, device type, etc.

## Quick Test Data Generator

You can use this Python script to generate sample data:

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
data = {
    'date': dates,
    'impressions': np.random.randint(5000, 20000, 30),
    'clicks': np.random.randint(100, 500, 30),
    'conversions': np.random.randint(5, 50, 30),
    'spend': np.random.uniform(200, 1000, 30),
    'campaign': np.random.choice(['Campaign A', 'Campaign B', 'Campaign C'], 30),
    'city': np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston'], 30)
}

df = pd.DataFrame(data)
df['ctr'] = (df['clicks'] / df['impressions'] * 100).round(2)
df['conversion_rate'] = (df['conversions'] / df['clicks'] * 100).round(2)
df.to_csv('sample_data.csv', index=False)
```

Save this as `generate_sample.py` and run it to create a test CSV file.

