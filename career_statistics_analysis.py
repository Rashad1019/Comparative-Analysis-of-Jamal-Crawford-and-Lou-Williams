import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Set style for plots
plt.style.use('fivethirtyeight')
sns.set_palette("deep")

# Create directory for saving visualizations
os.makedirs('/home/ubuntu/nba_comparison/visualizations', exist_ok=True)

# Define player data
crawford_data = {
    'Player': 'Jamal Crawford',
    'Seasons': 20,
    'Games': 1327,
    'PPG': 14.6,
    'RPG': 2.2,
    'APG': 3.4,
    'FG%': 41.0,
    '3P%': 34.8,
    'FT%': 86.2,
    'PER': 15.1,
    'WS': 60.7,
    'Sixth_Man_Awards': 3,
    'Career_High_Points': 52,
    'Total_Points': 19419,
    'Total_Rebounds': 2948,
    'Total_Assists': 4541,
    'Teams': 9
}

williams_data = {
    'Player': 'Lou Williams',
    'Seasons': 17,
    'Games': 1123,
    'PPG': 13.9,
    'RPG': 2.2,
    'APG': 3.4,
    'FG%': 41.9,
    '3P%': 35.1,
    'FT%': 84.2,
    'PER': 18.0,
    'WS': 65.7,
    'Sixth_Man_Awards': 3,
    'Career_High_Points': 50,
    'Total_Points': 15593,
    'Total_Rebounds': 2484,
    'Total_Assists': 3789,
    'Teams': 6
}

# Create DataFrame for comparison
df = pd.DataFrame([crawford_data, williams_data])
df.set_index('Player', inplace=True)

# Calculate additional metrics
df['Points_Per_Season'] = df['Total_Points'] / df['Seasons']
df['Points_Per_Game'] = df['Total_Points'] / df['Games']
df['Games_Per_Season'] = df['Games'] / df['Seasons']

# Save basic comparison to CSV
df.to_csv('/home/ubuntu/nba_comparison/data/career_comparison.csv')

# Create a function to generate comparison bar charts
def create_comparison_bar(metric, title, filename, ylabel=None, higher_is_better=True):
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x=df.index, y=metric, data=df)
    
    # Add values on top of bars
    for i, v in enumerate(df[metric]):
        ax.text(i, v + (max(df[metric]) * 0.02), f"{v:.1f}", ha='center')
    
    # Determine colors based on which value is better
    if higher_is_better:
        colors = ['#1f77b4', '#1f77b4']  # Default blue
        if df[metric].iloc[0] > df[metric].iloc[1]:
            colors[0] = '#2ca02c'  # Green for Crawford if better
        elif df[metric].iloc[1] > df[metric].iloc[0]:
            colors[1] = '#2ca02c'  # Green for Williams if better
    else:
        colors = ['#1f77b4', '#1f77b4']  # Default blue
        if df[metric].iloc[0] < df[metric].iloc[1]:
            colors[0] = '#2ca02c'  # Green for Crawford if better
        elif df[metric].iloc[1] < df[metric].iloc[0]:
            colors[1] = '#2ca02c'  # Green for Williams if better
    
    for i, patch in enumerate(ax.patches):
        patch.set_facecolor(colors[i])
    
    plt.title(title, fontsize=16)
    if ylabel:
        plt.ylabel(ylabel, fontsize=12)
    plt.tight_layout()
    plt.savefig(f'/home/ubuntu/nba_comparison/visualizations/{filename}.png', dpi=300)
    plt.close()

# Generate comparison visualizations
create_comparison_bar('PPG', 'Career Points Per Game', 'ppg_comparison', 'Points Per Game')
create_comparison_bar('RPG', 'Career Rebounds Per Game', 'rpg_comparison', 'Rebounds Per Game')
create_comparison_bar('APG', 'Career Assists Per Game', 'apg_comparison', 'Assists Per Game')
create_comparison_bar('FG%', 'Career Field Goal Percentage', 'fg_pct_comparison', 'FG%')
create_comparison_bar('3P%', 'Career Three-Point Percentage', '3p_pct_comparison', '3P%')
create_comparison_bar('FT%', 'Career Free Throw Percentage', 'ft_pct_comparison', 'FT%')
create_comparison_bar('PER', 'Player Efficiency Rating', 'per_comparison', 'PER')
create_comparison_bar('WS', 'Career Win Shares', 'ws_comparison', 'Win Shares')
create_comparison_bar('Games_Per_Season', 'Games Per Season', 'games_per_season', 'Games')
create_comparison_bar('Points_Per_Season', 'Points Per Season', 'points_per_season', 'Points')

# Create radar chart for overall comparison
def create_radar_chart():
    # Select metrics for radar chart
    metrics = ['PPG', 'RPG', 'APG', 'FG%', '3P%', 'FT%', 'PER', 'WS']
    
    # Normalize the data for radar chart
    df_radar = df[metrics].copy()
    for col in df_radar.columns:
        df_radar[col] = (df_radar[col] - df_radar[col].min()) / (df_radar[col].max() - df_radar[col].min())
    
    # Number of variables
    N = len(metrics)
    
    # Create angles for each metric
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Close the loop
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    
    # Add player data
    for idx, player in enumerate(df_radar.index):
        values = df_radar.loc[player].values.tolist()
        values += values[:1]  # Close the loop
        
        # Plot data
        ax.plot(angles, values, linewidth=2, linestyle='solid', label=player)
        ax.fill(angles, values, alpha=0.1)
    
    # Set labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metrics)
    
    # Add legend
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    
    plt.title('Crawford vs Williams: Statistical Comparison', size=20)
    plt.tight_layout()
    plt.savefig('/home/ubuntu/nba_comparison/visualizations/radar_comparison.png', dpi=300)
    plt.close()

create_radar_chart()

# Create a comprehensive comparison table
def create_comprehensive_table():
    # Create a more detailed comparison table
    comparison_data = {
        'Metric': [
            'Seasons Played', 'Games Played', 'Points Per Game', 'Rebounds Per Game',
            'Assists Per Game', 'Field Goal %', '3-Point %', 'Free Throw %',
            'Player Efficiency Rating', 'Win Shares', 'Sixth Man Awards',
            'Career High Points', 'Total Points', 'Total Rebounds', 'Total Assists',
            'Teams Played For', 'Points Per Season', 'Games Per Season'
        ],
        'Jamal Crawford': [
            crawford_data['Seasons'], crawford_data['Games'], crawford_data['PPG'],
            crawford_data['RPG'], crawford_data['APG'], crawford_data['FG%'],
            crawford_data['3P%'], crawford_data['FT%'], crawford_data['PER'],
            crawford_data['WS'], crawford_data['Sixth_Man_Awards'],
            crawford_data['Career_High_Points'], crawford_data['Total_Points'],
            crawford_data['Total_Rebounds'], crawford_data['Total_Assists'],
            crawford_data['Teams'], df.loc['Jamal Crawford', 'Points_Per_Season'],
            df.loc['Jamal Crawford', 'Games_Per_Season']
        ],
        'Lou Williams': [
            williams_data['Seasons'], williams_data['Games'], williams_data['PPG'],
            williams_data['RPG'], williams_data['APG'], williams_data['FG%'],
            williams_data['3P%'], williams_data['FT%'], williams_data['PER'],
            williams_data['WS'], williams_data['Sixth_Man_Awards'],
            williams_data['Career_High_Points'], williams_data['Total_Points'],
            williams_data['Total_Rebounds'], williams_data['Total_Assists'],
            williams_data['Teams'], df.loc['Lou Williams', 'Points_Per_Season'],
            df.loc['Lou Williams', 'Games_Per_Season']
        ]
    }
    
    # Create DataFrame
    comparison_df = pd.DataFrame(comparison_data)
    
    # Add a column to indicate who has the advantage
    def determine_advantage(row):
        # Skip non-numeric comparisons or ties
        if not isinstance(row['Jamal Crawford'], (int, float)) or not isinstance(row['Lou Williams'], (int, float)):
            return 'N/A'
        
        # For most metrics, higher is better
        higher_is_better = True
        
        # For these specific metrics, lower is not necessarily better
        if row['Metric'] in ['Teams Played For']:
            return 'N/A'  # Neutral metric
        
        if higher_is_better:
            if row['Jamal Crawford'] > row['Lou Williams']:
                return 'Crawford'
            elif row['Lou Williams'] > row['Jamal Crawford']:
                return 'Williams'
            else:
                return 'Tie'
        else:
            if row['Jamal Crawford'] < row['Lou Williams']:
                return 'Crawford'
            elif row['Lou Williams'] < row['Jamal Crawford']:
                return 'Williams'
            else:
                return 'Tie'
    
    comparison_df['Advantage'] = comparison_df.apply(determine_advantage, axis=1)
    
    # Save to CSV
    comparison_df.to_csv('/home/ubuntu/nba_comparison/data/detailed_comparison.csv', index=False)
    
    return comparison_df

detailed_comparison = create_comprehensive_table()

# Print summary of analysis
print("\nCareer Statistics Analysis Complete")
print("-----------------------------------")
print(f"Visualizations saved to: /home/ubuntu/nba_comparison/visualizations/")
print(f"Data saved to: /home/ubuntu/nba_comparison/data/")

# Count advantages
crawford_advantages = (detailed_comparison['Advantage'] == 'Crawford').sum()
williams_advantages = (detailed_comparison['Advantage'] == 'Williams').sum()
ties = (detailed_comparison['Advantage'] == 'Tie').sum()

print(f"\nStatistical Advantages Summary:")
print(f"Jamal Crawford leads in {crawford_advantages} categories")
print(f"Lou Williams leads in {williams_advantages} categories")
print(f"Tied in {ties} categories")
print(f"N/A in {(detailed_comparison['Advantage'] == 'N/A').sum()} categories")

# Write summary to file
with open('/home/ubuntu/nba_comparison/analysis/career_statistics_summary.md', 'w') as f:
    f.write("# Career Statistics Comparison: Jamal Crawford vs. Lou Williams\n\n")
    
    f.write("## Overview\n")
    f.write("This analysis compares the career statistics of Jamal Crawford and Lou Williams, two of the greatest sixth men in NBA history.\n\n")
    
    f.write("## Statistical Advantages\n")
    f.write(f"- **Jamal Crawford** leads in {crawford_advantages} statistical categories\n")
    f.write(f"- **Lou Williams** leads in {williams_advantages} statistical categories\n")
    f.write(f"- They are tied in {ties} categories\n\n")
    
    f.write("## Key Findings\n")
    
    # Add specific findings based on the data
    if crawford_data['PPG'] > williams_data['PPG']:
        f.write(f"- Crawford averaged more points per game ({crawford_data['PPG']} vs {williams_data['PPG']})\n")
    else:
        f.write(f"- Williams averaged more points per game ({williams_data['PPG']} vs {crawford_data['PPG']})\n")
    
    if crawford_data['PER'] > williams_data['PER']:
        f.write(f"- Crawford had a higher Player Efficiency Rating ({crawford_data['PER']} vs {williams_data['PER']})\n")
    else:
        f.write(f"- Williams had a higher Player Efficiency Rating ({williams_data['PER']} vs {crawford_data['PER']})\n")
    
    if crawford_data['WS'] > williams_data['WS']:
        f.write(f"- Crawford accumulated more Win Shares ({crawford_data['WS']} vs {williams_data['WS']})\n")
    else:
        f.write(f"- Williams accumulated more Win Shares ({williams_data['WS']} vs {crawford_data['WS']})\n")
    
    if crawford_data['FG%'] > williams_data['FG%']:
        f.write(f"- Crawford was more efficient from the field ({crawford_data['FG%']}% vs {williams_data['FG%']}%)\n")
    else:
        f.write(f"- Williams was more efficient from the field ({williams_data['FG%']}% vs {crawford_data['FG%']}%)\n")
    
    f.write(f"- Both players won the Sixth Man of the Year award 3 times\n")
    f.write(f"- Crawford played {crawford_data['Seasons'] - williams_data['Seasons']} more seasons than Williams\n")
    f.write(f"- Crawford played for {crawford_data['Teams']} teams compared to Williams' {williams_data['Teams']} teams\n\n")
    
    f.write("## Conclusion\n")
    if crawford_advantages > williams_advantages:
        f.write("Based on career statistics, Jamal Crawford has a slight edge over Lou Williams in more statistical categories. However, both players were exceptional sixth men who made significant impacts throughout their careers.\n")
    elif williams_advantages > crawford_advantages:
        f.write("Based on career statistics, Lou Williams has a slight edge over Jamal Crawford in more statistical categories. However, both players were exceptional sixth men who made significant impacts throughout their careers.\n")
    else:
        f.write("Based on career statistics, Jamal Crawford and Lou Williams are remarkably similar in their production and efficiency. Both players were exceptional sixth men who made significant impacts throughout their careers.\n")
