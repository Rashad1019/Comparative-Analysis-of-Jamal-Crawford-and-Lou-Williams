import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Set style for plots
plt.style.use('fivethirtyeight')
sns.set_palette("deep")

# Create directory for saving visualizations if it doesn't exist
os.makedirs('/home/ubuntu/nba_comparison/visualizations', exist_ok=True)

# Define Crawford's season-by-season data
crawford_seasons = {
    'Season': [
        '2000-01', '2001-02', '2002-03', '2003-04', '2004-05', '2005-06', '2006-07', '2007-08', '2008-09', '2009-10',
        '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19', '2019-20'
    ],
    'Age': [
        20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 
        30, 31, 32, 33, 34, 35, 36, 37, 38, 39
    ],
    'Team': [
        'CHI', 'CHI', 'CHI', 'CHI', 'NYK', 'NYK', 'NYK', 'NYK', 'GSW', 'ATL',
        'ATL', 'POR', 'LAC', 'LAC', 'LAC', 'LAC', 'LAC', 'MIN', 'PHO', 'BRK'
    ],
    'G': [
        61, 23, 80, 80, 70, 79, 59, 80, 65, 79,
        76, 60, 76, 69, 64, 79, 82, 80, 64, 1
    ],
    'PPG': [
        4.6, 9.3, 10.7, 17.3, 17.7, 14.3, 17.6, 20.6, 19.7, 18.0,
        14.2, 14.0, 16.5, 18.6, 15.8, 14.2, 12.3, 10.3, 7.9, 5.0
    ],
    'RPG': [
        1.5, 1.5, 2.3, 3.5, 2.9, 3.1, 3.2, 2.6, 3.0, 2.5,
        1.7, 2.0, 1.7, 2.3, 1.9, 1.8, 1.6, 1.2, 1.3, 0.0
    ],
    'APG': [
        2.3, 2.4, 4.2, 5.1, 4.3, 3.8, 4.4, 5.0, 4.4, 3.0,
        3.2, 3.2, 2.5, 3.2, 2.5, 2.3, 2.6, 2.3, 3.6, 3.0
    ],
    'FG%': [
        35.2, 47.6, 41.3, 38.6, 39.8, 41.6, 40.0, 41.0, 41.0, 44.9,
        42.1, 38.4, 43.8, 41.6, 39.6, 40.4, 41.3, 41.5, 39.7, 50.0
    ],
    '3P%': [
        35.0, 34.6, 35.5, 30.0, 34.7, 36.7, 35.9, 36.0, 35.8, 38.2,
        34.1, 30.8, 37.6, 36.1, 32.7, 34.0, 36.0, 33.1, 33.2, 0.0
    ],
    'PER': [
        11.1, 14.3, 14.0, 16.8, 15.7, 14.3, 15.6, 16.8, 15.5, 16.0,
        14.0, 14.2, 16.8, 16.8, 15.3, 15.3, 14.0, 12.1, 10.3, 5.0
    ],
    'WS': [
        1.4, 1.4, 3.0, 4.6, 4.4, 5.2, 5.8, 7.0, 4.6, 5.4,
        4.8, 2.8, 5.3, 4.9, 4.2, 4.8, 3.9, 2.1, 0.9, 0.0
    ],
    'VORP': [
        0.0, 0.5, 0.9, 2.5, 1.9, 1.3, 1.8, 3.1, 1.5, 2.1,
        1.2, 0.7, 1.9, 2.0, 1.2, 1.4, 0.7, -0.1, -0.5, 0.0
    ]
}

# Define Williams' season-by-season data
williams_seasons = {
    'Season': [
        '2005-06', '2006-07', '2007-08', '2008-09', '2009-10', '2010-11', '2011-12', '2012-13', '2013-14', '2014-15',
        '2015-16', '2016-17', '2017-18', '2018-19', '2019-20', '2020-21', '2021-22'
    ],
    'Age': [
        19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
        29, 30, 31, 32, 33, 34, 35
    ],
    'Team': [
        'PHI', 'PHI', 'PHI', 'PHI', 'PHI', 'PHI', 'PHI', 'ATL', 'ATL', 'TOR',
        'LAL', 'LAL/HOU', 'LAC', 'LAC', 'LAC', 'LAC/ATL', 'ATL'
    ],
    'G': [
        30, 61, 80, 81, 64, 75, 64, 39, 60, 80,
        67, 81, 79, 75, 65, 66, 56
    ],
    'PPG': [
        1.9, 4.3, 11.5, 12.8, 14.0, 13.7, 14.9, 14.1, 10.4, 15.5,
        15.3, 17.5, 22.6, 20.0, 18.2, 11.3, 6.3
    ],
    'RPG': [
        0.6, 1.1, 2.1, 2.0, 2.9, 2.0, 2.4, 2.1, 2.1, 1.9,
        2.5, 3.0, 2.5, 3.0, 3.1, 2.1, 1.6
    ],
    'APG': [
        0.3, 1.8, 3.2, 3.0, 4.2, 3.4, 3.5, 3.6, 3.5, 2.1,
        2.5, 3.0, 5.3, 5.4, 5.6, 3.4, 1.9
    ],
    'FG%': [
        44.2, 44.1, 42.4, 39.8, 47.0, 40.6, 40.7, 42.2, 40.0, 40.4,
        40.8, 42.9, 43.5, 42.5, 41.8, 41.0, 39.1
    ],
    '3P%': [
        22.2, 32.4, 35.9, 28.6, 34.0, 34.0, 36.2, 36.7, 34.2, 34.0,
        34.4, 36.5, 35.9, 36.1, 35.2, 39.9, 36.3
    ],
    'PER': [
        8.8, 13.3, 17.3, 16.8, 19.7, 17.7, 20.2, 17.0, 15.4, 19.9,
        18.8, 18.6, 22.6, 21.2, 19.2, 15.4, 11.9
    ],
    'WS': [
        0.3, 2.0, 5.3, 4.9, 6.3, 5.1, 6.0, 2.5, 2.8, 6.7,
        5.9, 7.7, 8.3, 7.1, 5.4, 3.5, 1.6
    ],
    'VORP': [
        -0.1, 0.5, 2.5, 2.0, 3.0, 2.1, 2.7, 1.0, 0.9, 2.7,
        2.1, 2.6, 3.9, 3.2, 2.2, 1.0, 0.0
    ]
}

# Create DataFrames
crawford_df = pd.DataFrame(crawford_seasons)
williams_df = pd.DataFrame(williams_seasons)

# Function to identify peak years based on multiple metrics
def identify_peak_years(player_df, num_years=3, metrics=['PPG', 'PER', 'WS', 'VORP']):
    # Create a composite score for each season
    player_df['Composite'] = 0
    
    # Normalize each metric and add to composite score
    for metric in metrics:
        if metric in player_df.columns:
            min_val = player_df[metric].min()
            max_val = player_df[metric].max()
            if max_val > min_val:  # Avoid division by zero
                player_df['Composite'] += (player_df[metric] - min_val) / (max_val - min_val)
    
    # Sort by composite score and get top seasons
    top_seasons = player_df.sort_values('Composite', ascending=False).head(num_years)
    return top_seasons

# Identify peak years
crawford_peak = identify_peak_years(crawford_df)
williams_peak = identify_peak_years(williams_df)

# Create visualizations for career trajectories
plt.figure(figsize=(14, 8))
plt.plot(crawford_df['Season'], crawford_df['PPG'], marker='o', linewidth=2, label='Crawford')
plt.plot(williams_df['Season'], williams_df['PPG'], marker='s', linewidth=2, label='Williams')

# Highlight peak years for Crawford
for idx, row in crawford_peak.iterrows():
    plt.plot(row['Season'], row['PPG'], 'ro', markersize=12, alpha=0.7)
    plt.annotate(f"{row['Season']}: {row['PPG']:.1f} PPG", 
                 xy=(row['Season'], row['PPG']), 
                 xytext=(10, 10),
                 textcoords='offset points',
                 fontsize=10,
                 color='darkred')

# Highlight peak years for Williams
for idx, row in williams_peak.iterrows():
    plt.plot(row['Season'], row['PPG'], 'bs', markersize=12, alpha=0.7)
    plt.annotate(f"{row['Season']}: {row['PPG']:.1f} PPG", 
                 xy=(row['Season'], row['PPG']), 
                 xytext=(10, -15),
                 textcoords='offset points',
                 fontsize=10,
                 color='darkblue')

plt.title('Career Scoring Trajectory: Crawford vs Williams', fontsize=16)
plt.ylabel('Points Per Game', fontsize=14)
plt.xlabel('Season', fontsize=14)
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('/home/ubuntu/nba_comparison/visualizations/career_trajectory.png', dpi=300)
plt.close()

# Create visualizations for peak years comparison
def create_peak_comparison(metric, title, filename):
    plt.figure(figsize=(12, 7))
    
    # Get peak years data
    crawford_peak_data = crawford_peak[['Season', metric]].sort_values('Season')
    williams_peak_data = williams_peak[['Season', metric]].sort_values('Season')
    
    # Set up bar positions
    bar_width = 0.35
    crawford_pos = np.arange(len(crawford_peak_data))
    williams_pos = np.arange(len(williams_peak_data))
    
    # Create bars
    plt.bar(crawford_pos, crawford_peak_data[metric], bar_width, label='Crawford Peak Years', color='#FF5733')
    plt.bar(williams_pos + bar_width, williams_peak_data[metric], bar_width, label='Williams Peak Years', color='#3373FF')
    
    # Add labels
    plt.xlabel('Season', fontsize=14)
    plt.ylabel(metric, fontsize=14)
    plt.title(f'Peak Years Comparison: {title}', fontsize=16)
    
    # Set x-ticks
    plt.xticks(crawford_pos + bar_width / 2, crawford_peak_data['Season'], rotation=45)
    
    # Add values on top of bars
    for i, v in enumerate(crawford_peak_data[metric]):
        plt.text(i - 0.1, v + 0.1, f"{v:.1f}", fontsize=10)
    
    for i, v in enumerate(williams_peak_data[metric]):
        plt.text(i + bar_width - 0.1, v + 0.1, f"{v:.1f}", fontsize=10)
    
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'/home/ubuntu/nba_comparison/visualizations/{filename}.png', dpi=300)
    plt.close()

# Create peak years comparisons for different metrics
create_peak_comparison('PPG', 'Points Per Game', 'peak_ppg_comparison')
create_peak_comparison('PER', 'Player Efficiency Rating', 'peak_per_comparison')
create_peak_comparison('WS', 'Win Shares', 'peak_ws_comparison')
if 'VORP' in crawford_df.columns and 'VORP' in williams_df.columns:
    create_peak_comparison('VORP', 'Value Over Replacement Player', 'peak_vorp_comparison')

# Create radar chart for peak years comparison
def create_peak_radar_chart():
    # Select metrics for radar chart
    metrics = ['PPG', 'RPG', 'APG', 'FG%', '3P%', 'PER', 'WS']
    
    # Calculate average of peak years for each player
    crawford_peak_avg = crawford_peak[metrics].mean()
    williams_peak_avg = williams_peak[metrics].mean()
    
    # Create DataFrame for radar chart
    radar_df = pd.DataFrame({
        'Metric': metrics,
        'Crawford': crawford_peak_avg.values,
        'Williams': williams_peak_avg.values
    })
    
    # Normalize the data for radar chart
    for player in ['Crawford', 'Williams']:
        max_vals = radar_df[['Crawford', 'Williams']].max(axis=1)
        min_vals = radar_df[['Crawford', 'Williams']].min(axis=1)
        # Avoid division by zero
        for i, (max_val, min_val) in enumerate(zip(max_vals, min_vals)):
            if max_val > min_val:
                radar_df.loc[i, f'{player}_Normalized'] = (radar_df.loc[i, player] - min_val) / (max_val - min_val)
            else:
                radar_df.loc[i, f'{player}_Normalized'] = 0.5  # Default to middle if no difference
    
    # Number of variables
    N = len(metrics)
    
    # Create angles for each metric
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Close the loop
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    
    # Add player data
    crawford_values = radar_df['Crawford_Normalized'].tolist()
    crawford_values += crawford_values[:1]  # Close the loop
    williams_values = radar_df['Williams_Normalized'].tolist()
    williams_values += williams_values[:1]  # Close the loop
    
    # Plot data
    ax.plot(angles, crawford_values, linewidth=2, linestyle='solid', label='Crawford Peak', color='#FF5733')
    ax.fill(angles, crawford_values, alpha=0.1, color='#FF5733')
    ax.plot(angles, williams_values, linewidth=2, linestyle='solid', label='Williams Peak', color='#3373FF')
    ax.fill(angles, williams_values, alpha=0.1, color='#3373FF')
    
    # Set labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metrics)
    
    # Add legend
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    
    plt.title('Crawford vs Williams: Peak Years Comparison', size=20)
    plt.tight_layout()
    plt.savefig('/home/ubuntu/nba_comparison/visualizations/peak_radar_comparison.png', dpi=300)
    plt.close()

create_peak_radar_chart()

# Save peak years data to CSV
crawford_peak.to_csv('/home/ubuntu/nba_comparison/data/crawford_peak_years.csv', index=False)
williams_peak.to_csv('/home/ubuntu/nba_comparison/data/williams_peak_years.csv', index=False)

# Create a summary of peak years analysis
with open('/home/ubuntu/nba_comparison/analysis/peak_years_summary.md', 'w') as f:
    f.write("# Peak Years Analysis: Jamal Crawford vs. Lou Williams\n\n")
    
    f.write("## Jamal Crawford's Peak Years\n")
    for idx, row in crawford_peak.iterrows():
        f.write(f"### {row['Season']} ({row['Team']})\n")
        f.write(f"- **Age:** {row['Age']}\n")
        f.write(f"- **PPG:** {row['PPG']:.1f}\n")
        f.write(f"- **RPG:** {row['RPG']:.1f}\n")
        f.write(f"- **APG:** {row['APG']:.1f}\n")
        f.write(f"- **FG%:** {row['FG%']:.1f}%\n")
        f.write(f"- **3P%:** {row['3P%']:.1f}%\n")
        f.write(f"- **PER:** {row['PER']:.1f}\n")
        f.write(f"- **Win Shares:** {row['WS']:.1f}\n")
        if 'VORP' in crawford_df.columns:
            f.write(f"- **VORP:** {row['VORP']:.1f}\n")
        f.write("\n")
    
    f.write("## Lou Williams' Peak Years\n")
    for idx, row in williams_peak.iterrows():
        f.write(f"### {row['Season']} ({row['Team']})\n")
        f.write(f"- **Age:** {row['Age']}\n")
        f.write(f"- **PPG:** {row['PPG']:.1f}\n")
        f.write(f"- **RPG:** {row['RPG']:.1f}\n")
        f.write(f"- **APG:** {row['APG']:.1f}\n")
        f.write(f"- **FG%:** {row['FG%']:.1f}%\n")
        f.write(f"- **3P%:** {row['3P%']:.1f}%\n")
        f.write(f"- **PER:** {row['PER']:.1f}\n")
        f.write(f"- **Win Shares:** {row['WS']:.1f}\n")
        if 'VORP' in williams_df.columns:
            f.write(f"- **VORP:** {row['VORP']:.1f}\n")
        f.write("\n")
    
    # Calculate average stats during peak years
    crawford_peak_avg = crawford_peak[['PPG', 'RPG', 'APG', 'FG%', '3P%', 'PER', 'WS']].mean()
    williams_peak_avg = williams_peak[['PPG', 'RPG', 'APG', 'FG%', '3P%', 'PER', 'WS']].mean()
    
    f.write("## Peak Years Comparison\n\n")
    f.write("| Metric | Crawford Peak Avg | Williams Peak Avg | Advantage |\n")
    f.write("|--------|-------------------|-------------------|----------|\n")
    
    for metric in ['PPG', 'RPG', 'APG', 'FG%', '3P%', 'PER', 'WS']:
        crawford_val = crawford_peak_avg[metric]
        williams_val = williams_peak_avg[metric]
        
        if crawford_val > williams_val:
            advantage = "Crawford"
        elif williams_val > crawford_val:
            advantage = "Williams"
        else:
            advantage = "Tie"
        
        f.write(f"| {metric} | {crawford_val:.1f} | {williams_val:.1f} | {advantage} |\n")
    
    if 'VORP' in crawford_df.columns and 'VORP' in williams_df.columns:
        crawford_vorp = crawford_peak['VORP'].mean()
        williams_vorp = williams_peak['VORP'].mean()
        
        if crawford_vorp > williams_vorp:
            advantage = "Crawford"
        elif williams_vorp > crawford_vorp:
            advantage = "Williams"
        else:
            advantage = "Tie"
        
        f.write(f"| VORP | {crawford_vorp:.1f} | {williams_vorp:.1f} | {advantage} |\n")
    
    f.write("\n## Conclusion\n")
    
    # Count advantages
    advantages = []
    for metric in ['PPG', 'RPG', 'APG', 'FG%', '3P%', 'PER', 'WS']:
        crawford_val = crawford_peak_avg[metric]
        williams_val = williams_peak_avg[metric]
        
        if crawford_val > williams_val:
            advantages.append("Crawford")
        elif williams_val > crawford_val:
            advantages.append("Williams")
        else:
            advantages.append("Tie")
    
    crawford_advantages = advantages.count("Crawford")
    williams_advantages = advantages.count("Williams")
    ties = advantages.count("Tie")
    
    if crawford_advantages > williams_advantages:
        f.write("During their respective peak years, **Jamal Crawford** demonstrated superior performance in more statistical categories compared to Lou Williams. ")
    elif williams_advantages > crawford_advantages:
        f.write("During their respective peak years, **Lou Williams** demonstrated superior performance in more statistical categories compared to Jamal Crawford. ")
    else:
        f.write("During their respective peak years, Jamal Crawford and Lou Williams demonstrated remarkably similar levels of performance across statistical categories. ")
    
    f.write(f"Crawford held the advantage in {crawford_advantages} categories, while Williams led in {williams_advantages} categories, with {ties} categories being tied.\n\n")
    
    # Add specific observations
    if crawford_peak_avg['PPG'] > williams_peak_avg['PPG']:
        f.write(f"Crawford was a more prolific scorer during his peak, averaging {crawford_peak_avg['PPG']:.1f} points per game compared to Williams' {williams_peak_avg['PPG']:.1f}.\n\n")
    else:
        f.write(f"Williams was a more prolific scorer during his peak, averaging {williams_peak_avg['PPG']:.1f} points per game compared to Crawford's {crawford_peak_avg['PPG']:.1f}.\n\n")
    
    if crawford_peak_avg['PER'] > williams_peak_avg['PER']:
        f.write(f"Crawford was more efficient during his peak years with a Player Efficiency Rating of {crawford_peak_avg['PER']:.1f} compared to Williams' {williams_p
(Content truncated due to size limit. Use line ranges to read in chunks)