import numpy as np

def generate_signals(df, entry_z=2.0, exit_z=0.5, stop_z=4.0):
    
    df = df.copy()
    z = df["zscore"].values
    position = np.zeros(len(df)) #+1 is long, -1 is short, 0 is flat
    state = 0 # same idea as the position with -1,1,0
    
    for i in range(1, len(df)):
        if state == 0:
            if z[i] > entry_z: 
                state = -1  # short
            elif z[i] < -entry_z: 
                state = 1  # long
        elif state == 1:
            if z[i] > -exit_z: 
                state = 0  # mean reversion toward 0
            elif z[i] < -stop_z: 
                state = 0  # stop loss
        elif state == -1:
            if z[i] < exit_z: 
                state = 0
            elif z[i] > stop_z: 
                state = 0

        
        position[i] = state
    
    df["position"] = position
    
    return df

    