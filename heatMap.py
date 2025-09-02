# LeBron Shot Chart Heat Map

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import matplotlib.cm as cm
import seaborn as sns

#Read in csv
bron_df = pd.read_csv("/Users/bball/Documents/LeBron Visualization Project/1_lebron_james_shot_chart_1_2023.csv")

#Rename shot types from numbers to readable labels
bron_df['shot_type'] = bron_df['shot_type'].replace({2: '2-point shot', 3: '3-point shot'})

# Rename result from boolean to Made/Missed
bron_df['result'] = bron_df['result'].replace({True: 'Made', False: 'Missed'})

print(bron_df.head())

# Coordinate Conversion

def convert_c(df):
    df['court_x'] = df['left'] - 240 #X coordinate is refering to image pixels, so must be adjusted to center at 0
    df['court_y'] = df['top']

    return df

# Apply shift to LeBron's CSV
bron_df = convert_c(bron_df)

# Court Drawing

def draw_court(axis = None):
    if axis is None:
        fig = plt.figure(figsize = (9,9))
        axis - fig.add_subplot(111, aspect = 'auto')
    else:
        fig = None
    
    # Court Outline
    axis.plot([-250, 250], [-47.5, -47.5], color = 'blue', linestyle = '-') #Baseline
    axis.plot([-250, -250], [-47.5, 422.5], color = 'blue', linestyle = '-') #Left Sideline
    axis.plot([250, 250], [-47.5, 422.5], color = 'blue', linestyle = '-') #Right Sideline
    axis.plot([-250, 250], [422.5, 422.5], color = 'blue', linestyle = '-') #Halfcourt Line

    # Backboard
    axis.plot([-30, 30], [-10, -10], color = 'blue', linestyle = '-', lw = 2)

    # Paint/Lane
    axis.plot([-80, -80], [-47.5, 142.5], color = 'blue', linestyle = '-')
    axis.plot([80, 80], [-47.5, 142.5], color = 'blue', linestyle = '-')
    axis.plot([-60, -60], [-47.5, 142.5], color = 'blue', linestyle = '-')
    axis.plot([60, 60], [-47.5, 142.5], color = 'blue', linestyle = '-')
    axis.plot([-80, 80], [142.5, 142.5], color = 'blue', linestyle = '-')

    # Hoop
    hoop = Arc((0 , 0), 15, 15, theta1=0, theta2=360, lw = 1.5, color = 'blue')
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, lw=1.5, color='blue')
    axis.add_patch(hoop)
    axis.add_patch(restricted)

    # Free Throw Circle
    axis.add_patch(Arc((0, 142.5), 120, 120, theta1 = 0, theta2 = 180, lw = 1.5, color = 'blue')) # Top half
    axis.add_patch(Arc((0, 142.5), 120, 120, theta1 = 180, theta2 = 360, lw = 1.5, linestyle = '--', color = 'blue'))  # Bottom half (dashed)

    # 3-Point Lines 
    axis.plot([-220, -220], [-47.5, 92.5], color = 'blue', linestyle = '-')     # Left corner 3
    axis.plot([220, 220], [-47.5, 92.5], color = 'blue', linestyle = '-')       # Right corner 3
    axis.add_patch(Arc((0, 0), 475, 475, theta1 = 22, theta2 = 158, lw = 1.5, color = 'blue'))   # 3-pt arc

    # Halfcourt Circle
    axis.add_patch(Arc((0, 422.5), 122, 122, theta1 = 180, theta2 = 360, lw = 1.5, color='blue'))

    # Axis Settings
    axis.set_xlim(-250, 250)
    axis.set_ylim(-47.5, 470)
    axis.set_aspect(1)
    axis.axis('off') 

    return fig, axis

# Heat Map

fig, ax = plt.subplots(figsize = (9 , 9))

draw_court(ax)

kde = sns.kdeplot(
    x = bron_df['court_x'],
    y = bron_df['court_y'],
    fill = True,
    cmap = 'turbo',
    bw_adjust = 0.9,
    alpha = 0.5,
    levels = 50,
    thresh = 0.05,
    ax = ax
)

plt.title("LeBron James Shot Chart", fontsize = 16)
plt.show()