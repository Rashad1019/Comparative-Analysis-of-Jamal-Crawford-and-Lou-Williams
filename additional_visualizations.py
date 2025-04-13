import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from matplotlib.gridspec import GridSpec

# Set style for plots
plt.style.use('fivethirtyeight')
sns.set_palette("deep")

# Create directory for saving visualizations if it doesn't exist
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
    'Teams': 9,
    'Playoff_Games': 74,
    'Playoff_PPG': 14.3,
    'Playoff_RPG': 1.9,
    'Playoff_APG': 2.2,
    'Playoff_FG%': 40.3,
    'Playoff_3P%': 32.5,
    'Playoff_FT%': 87.2
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
    'Teams': 6,
    'Playoff_Games': 89,
    'Playoff_PPG': 11.4,
    'Playoff_RPG': 2.2,
    'Playoff_APG': 2.8,
    'Playoff_FG%': 39.8,
    'Playoff_3P%': 31.2,
    'Playoff_FT%': 85.6
}

# Create DataFrame for comparison
df = pd.DataFrame([crawford_data, williams_data])
df.set_index('Player', inplace=True)

# Create a function to generate comparison bar charts with a more professional look
def create_enhanced_bar_chart(metric, title, filename, ylabel=None, higher_is_better=True):
    plt.figure(figsize=(12, 8))
    
    # Create bar chart
    ax = sns.barplot(x=df.index, y=metric, data=df, palette=['#1f77b4', '#ff7f0e'])
    
    # Add values on top of bars
    for i, v in enumerate(df[metric]):
        ax.text(i, v + (max(df[metric]) * 0.02), f"{v:.1f}", ha='center', fontsize=12, fontweight='bold')
    
    # Add a horizontal line for the average of both players
    avg_value = df[metric].mean()
    plt.axhline(y=avg_value, color='gray', linestyle='--', alpha=0.7)
    plt.text(0.5, avg_value + (max(df[metric]) * 0.01), f"Avg: {avg_value:.1f}", 
             ha='center', color='gray', fontsize=10)
    
    # Enhance the chart
    plt.title(title, fontsize=18, fontweight='bold', pad=20)
    if ylabel:
        plt.ylabel(ylabel, fontsize=14, fontweight='bold')
    plt.xlabel('', fontsize=14)  # Remove x-label as it's obvious
    
    # Add a subtle grid
    plt.grid(axis='y', alpha=0.3)
    
    # Add annotations to indicate who's better
    if higher_is_better:
        if df[metric].iloc[0] > df[metric].iloc[1]:
            plt.annotate('Crawford leads', xy=(0, df[metric].iloc[0] - (max(df[metric]) * 0.1)),
                        ha='center', fontsize=12, color='#1f77b4', fontweight='bold')
        elif df[metric].iloc[1] > df[metric].iloc[0]:
            plt.annotate('Williams leads', xy=(1, df[metric].iloc[1] - (max(df[metric]) * 0.1)),
                        ha='center', fontsize=12, color='#ff7f0e', fontweight='bold')
    else:
        if df[metric].iloc[0] < df[metric].iloc[1]:
            plt.annotate('Crawford leads', xy=(0, df[metric].iloc[0] + (max(df[metric]) * 0.05)),
                        ha='center', fontsize=12, color='#1f77b4', fontweight='bold')
        elif df[metric].iloc[1] < df[metric].iloc[0]:
            plt.annotate('Williams leads', xy=(1, df[metric].iloc[1] + (max(df[metric]) * 0.05)),
                        ha='center', fontsize=12, color='#ff7f0e', fontweight='bold')
    
    # Add a subtle background color
    ax.set_facecolor('#f8f8f8')
    
    # Add a border
    for spine in ax.spines.values():
        spine.set_edgecolor('#dddddd')
    
    plt.tight_layout()
    plt.savefig(f'/home/ubuntu/nba_comparison/visualizations/{filename}.png', dpi=300, bbox_inches='tight')
    plt.close()

# Create a function for side-by-side comparison of regular season vs playoffs
def create_regular_vs_playoff_chart(reg_metric, playoff_metric, title, filename, ylabel=None):
    plt.figure(figsize=(14, 8))
    
    # Set up the data
    players = df.index.tolist()
    reg_values = df[reg_metric].tolist()
    playoff_values = df[playoff_metric].tolist()
    
    # Set up bar positions
    x = np.arange(len(players))
    width = 0.35
    
    # Create bars
    ax = plt.subplot()
    rects1 = ax.bar(x - width/2, reg_values, width, label='Regular Season', color='#1f77b4')
    rects2 = ax.bar(x + width/2, playoff_values, width, label='Playoffs', color='#ff7f0e')
    
    # Add labels and title
    ax.set_title(title, fontsize=18, fontweight='bold', pad=20)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(players, fontsize=12, fontweight='bold')
    
    # Add value labels on bars
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.1f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    autolabel(rects1)
    autolabel(rects2)
    
    # Add a legend
    ax.legend(fontsize=12)
    
    # Add a subtle grid
    plt.grid(axis='y', alpha=0.3)
    
    # Add a subtle background color
    ax.set_facecolor('#f8f8f8')
    
    # Add a border
    for spine in ax.spines.values():
        spine.set_edgecolor('#dddddd')
    
    # Add annotations for playoff performance drop/improvement
    for i, player in enumerate(players):
        reg = reg_values[i]
        playoff = playoff_values[i]
        diff = playoff - reg
        diff_pct = (diff / reg) * 100
        
        if diff < 0:
            color = '#d62728'  # red for drop
            text = f"{diff_pct:.1f}% drop"
        else:
            color = '#2ca02c'  # green for improvement
            text = f"+{diff_pct:.1f}%"
        
        ax.annotate(text, 
                   xy=(i, min(reg, playoff) - (max(reg_values + playoff_values) * 0.05)),
                   ha='center', fontsize=10, color=color, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'/home/ubuntu/nba_comparison/visualizations/{filename}.png', dpi=300, bbox_inches='tight')
    plt.close()

# Create a function for career timeline visualization
def create_career_timeline():
    plt.figure(figsize=(16, 8))
    
    # Crawford's career span
    crawford_start = 2000
    crawford_end = 2020
    crawford_peak_years = [2003, 2007, 2013]  # Based on peak years analysis
    
    # Williams' career span
    williams_start = 2005
    williams_end = 2022
    williams_peak_years = [2017, 2018, 2019]  # Based on peak years analysis
    
    # Create the timeline
    ax = plt.subplot()
    
    # Draw career spans
    ax.plot([crawford_start, crawford_end], [1, 1], linewidth=8, color='#1f77b4', alpha=0.7, label='Crawford Career')
    ax.plot([williams_start, williams_end], [0, 0], linewidth=8, color='#ff7f0e', alpha=0.7, label='Williams Career')
    
    # Highlight peak years
    for year in crawford_peak_years:
        ax.plot(year, 1, 'o', markersize=15, color='#1f77b4')
        ax.annotate(f"{year}-{year+1}", xy=(year, 1.1), ha='center', fontsize=10, fontweight='bold')
    
    for year in williams_peak_years:
        ax.plot(year, 0, 'o', markersize=15, color='#ff7f0e')
        ax.annotate(f"{year}-{year+1}", xy=(year, -0.1), ha='center', fontsize=10, fontweight='bold')
    
    # Add Sixth Man Award years
    crawford_6moy_years = [2010, 2014, 2016]
    williams_6moy_years = [2015, 2018, 2019]
    
    for year in crawford_6moy_years:
        ax.plot(year, 1, '*', markersize=20, color='gold', markeredgecolor='black')
    
    for year in williams_6moy_years:
        ax.plot(year, 0, '*', markersize=20, color='gold', markeredgecolor='black')
    
    # Add a legend for the stars
    ax.plot([], [], '*', markersize=15, color='gold', markeredgecolor='black', label='Sixth Man Award')
    
    # Set up the axes
    ax.set_yticks([0, 1])
    ax.set_yticklabels(['Lou Williams', 'Jamal Crawford'], fontsize=12, fontweight='bold')
    ax.set_xlim(1999, 2023)
    
    # Add a title
    plt.title('Career Timeline: Crawford vs Williams', fontsize=18, fontweight='bold', pad=20)
    
    # Add x-axis label
    plt.xlabel('NBA Season (Starting Year)', fontsize=14, fontweight='bold')
    
    # Add a legend
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3, fontsize=12)
    
    # Remove y-axis line
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Add a subtle background color
    ax.set_facecolor('#f8f8f8')
    
    # Add a border
    for spine in ['top', 'bottom']:
        ax.spines[spine].set_edgecolor('#dddddd')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/nba_comparison/visualizations/career_timeline.png', dpi=300, bbox_inches='tight')
    plt.close()

# Create a function for efficiency metrics over time visualization
def create_efficiency_over_time():
    # Define season data for Crawford
    crawford_seasons = list(range(2000, 2020))
    crawford_fg_pct = [35.2, 47.6, 41.3, 38.6, 39.8, 41.6, 40.0, 41.0, 41.0, 44.9,
                      42.1, 38.4, 43.8, 41.6, 39.6, 40.4, 41.3, 41.5, 39.7, 50.0]
    crawford_per = [11.1, 14.3, 14.0, 16.8, 15.7, 14.3, 15.6, 16.8, 15.5, 16.0,
                   14.0, 14.2, 16.8, 16.8, 15.3, 15.3, 14.0, 12.1, 10.3, 5.0]
    
    # Define season data for Williams
    williams_seasons = list(range(2005, 2022))
    williams_fg_pct = [44.2, 44.1, 42.4, 39.8, 47.0, 40.6, 40.7, 42.2, 40.0, 40.4,
                      40.8, 42.9, 43.5, 42.5, 41.8, 41.0, 39.1]
    williams_per = [8.8, 13.3, 17.3, 16.8, 19.7, 17.7, 20.2, 17.0, 15.4, 19.9,
                   18.8, 18.6, 22.6, 21.2, 19.2, 15.4, 11.9]
    
    # Create the figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12), sharex=True)
    
    # Plot FG% over time
    ax1.plot(crawford_seasons, crawford_fg_pct, 'o-', linewidth=2, markersize=8, color='#1f77b4', label='Crawford FG%')
    ax1.plot(williams_seasons, williams_fg_pct, 's-', linewidth=2, markersize=8, color='#ff7f0e', label='Williams FG%')
    
    # Add a horizontal line for league average FG% (approximate)
    ax1.axhline(y=45.0, color='gray', linestyle='--', alpha=0.7)
    ax1.text(2010, 45.5, 'League Average FG%', ha='center', color='gray', fontsize=10)
    
    # Set up the first subplot
    ax1.set_ylabel('Field Goal %', fontsize=14, fontweight='bold')
    ax1.set_title('Shooting Efficiency Over Time', fontsize=18, fontweight='bold', pad=20)
    ax1.legend(fontsize=12)
    ax1.grid(alpha=0.3)
    
    # Plot PER over time
    ax2.plot(crawford_seasons, crawford_per, 'o-', linewidth=2, markersize=8, color='#1f77b4', label='Crawford PER')
    ax2.plot(williams_seasons, williams_per, 's-', linewidth=2, markersize=8, color='#ff7f0e', label='Williams PER')
    
    # Add a horizontal line for league average PER (15.0)
    ax2.axhline(y=15.0, color='gray', linestyle='--', alpha=0.7)
    ax2.text(2010, 15.5, 'League Average PER (15.0)', ha='center', color='gray', fontsize=10)
    
    # Set up the second subplot
    ax2.set_ylabel('Player Efficiency Rating', fontsize=14, fontweight='bold')
    ax2.set_xlabel('NBA Season (Starting Year)', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=12)
    ax2.grid(alpha=0.3)
    
    # Add a subtle background color
    ax1.set_facecolor('#f8f8f8')
    ax2.set_facecolor('#f8f8f8')
    
    # Add borders
    for ax in [ax1, ax2]:
        for spine in ax.spines.values():
            spine.set_edgecolor('#dddddd')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/nba_comparison/visualizations/efficiency_over_time.png', dpi=300, bbox_inches='tight')
    plt.close()

# Create a function for a comprehensive dashboard visualization
def create_comprehensive_dashboard():
    # Create a figure with a grid layout
    fig = plt.figure(figsize=(20, 16))
    gs = GridSpec(3, 3, figure=fig)
    
    # Define player colors
    crawford_color = '#1f77b4'
    williams_color = '#ff7f0e'
    
    # 1. Career Summary - Top Left
    ax1 = fig.add_subplot(gs[0, 0])
    summary_data = {
        'Metric': ['Seasons', 'Games', 'Points', 'Sixth Man Awards'],
        'Crawford': [crawford_data['Seasons'], crawford_data['Games'], crawford_data['Total_Points'], crawford_data['Sixth_Man_Awards']],
        'Williams': [williams_data['Seasons'], williams_data['Games'], williams_data['Total_Points'], williams_data['Sixth_Man_Awards']]
    }
    summary_df = pd.DataFrame(summary_data)
    summary_df.set_index('Metric', inplace=True)
    summary_df.plot(kind='bar', ax=ax1, color=[crawford_color, williams_color])
    ax1.set_title('Career Summary', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Value', fontsize=12)
    ax1.legend(fontsize=10)
    
    # 2. Per Game Stats - Top Middle
    ax2 = fig.add_subplot(gs[0, 1])
    per_game_data = {
        'Metric': ['PPG', 'RPG', 'APG'],
        'Crawford': [crawford_data['PPG'], crawford_data['RPG'], crawford_data['APG']],
        'Williams': [williams_data['PPG'], williams_data['RPG'], williams_data['APG']]
    }
    per_game_df = pd.DataFrame(per_game_data)
    per_game_df.set_index('Metric', inplace=True)
    per_game_df.plot(kind='bar', ax=ax2, color=[crawford_color, williams_color])
    ax2.set_title('Per Game Statistics', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Value', fontsize=12)
    ax2.legend(fontsize=10)
    
    # 3. Efficiency Metrics - Top Right
    ax3 = fig.add_subplot(gs[0, 2])
    efficiency_data = {
        'Metric': ['FG%', '3P%', 'FT%', 'PER'],
        'Crawford': [crawford_data['FG%'], crawford_data['3P%'], crawford_data['FT%'], crawford_data['PER']],
        'Williams': [williams_data['FG%'], williams_data['3P%'], williams_data['FT%'], williams_data['PER']]
    }
    efficiency_df = pd.DataFrame(efficiency_data)
    efficiency_df.set_index('Metric', inplace=True)
    efficiency_df.plot(kind='bar', ax=ax3, color=[crawford_color, williams_color])
    ax3.set_title('Efficiency Metrics', fontsize=14, fontweight='bold')
    ax3.set_ylabel('Value', fontsize=12)
    ax3.legend(fontsize=10)
    
    # 4. Regular Season vs Playoffs - Middle Left
    ax4 = fig.add_subplot(gs[1, 0])
    reg_vs_playoff_data = {
        'Context': ['Crawford Reg', 'Crawford Playoff', 'Williams Reg', 'Williams Playoff'],
        'PPG': [crawford_data['PPG'], crawford_data['Playoff_PPG'], williams_data['PPG'], williams_data['Playoff_PPG']],
        'Color': [crawford_color, 'lightblue', williams_color, 'navajowhite']
    }
    sns.barplot(x='Context', y='PPG', data=reg_vs_playoff_data, palette=reg_vs_playoff_data['Color'], ax=ax4)
    ax4.set_title('Regular Season vs Playoffs PPG', fontsize=14, fontweight='bold')
    ax4.set_ylabel('Points Per Game', fontsize=12)
    
    # 5. Win Shares - Middle Middle
    ax5 = fig.add_subplot(gs[1, 1])
    win_shares_data = {
        'Player': ['Crawford', 'Williams'],
        'Win Shares': [crawford_data['WS'], williams_data['WS']],
        'Color': [crawford_color, williams_color]
    }
    sns.barplot(x='Player', y='Win Shares', data=win_shares_data, palette=win_shares_data['Color'], ax=ax5)
    ax5.set_title('Career Win Shares', fontsize=14, fontweight='bold')
    ax5.set_ylabel('Win Shares', fontsize=12)
    
    # 6. Career High Points - Middle Right
    ax6 = fig.add_subplot(gs[1, 2])
    career_high_data = {
        'Player': ['Crawford', 'Williams'],
        'Career High': [crawford_data['Career_High_Points'], williams_data['Career_High_Points']],
        'Color': [crawford_color, w
(Content truncated due to size limit. Use line ranges to read in chunks)