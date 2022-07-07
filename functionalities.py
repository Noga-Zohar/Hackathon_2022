import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('default')


def create_graph_per_electrode(df, electrode_name, fig_path):
    plt.figure(figsize=(16, 8), dpi=150)
    df['Delta_' + electrode_name].plot(label='Delta', color='orange')
    df['Theta_' + electrode_name].plot(label='Theta')
    df['Alpha_' + electrode_name].plot(label='Alpha')
    df['Beta_' + electrode_name].plot(label='Beta')
    df['Gamma_' + electrode_name].plot(label='Gamma')

    # adding title to the plot
    plt.title('graph for electrode' + electrode_name)

    # adding Label to the x-axis
    plt.xlabel('time')
    plt.savefig(fig_path)


def create_graph_per_wave(df, wave_length, fig_path):
    plt.figure(figsize=(16, 8), dpi=150)
    df[wave_length + "_AF7"].plot(label='AF7', color='orange')
    df[wave_length + "_AF8"].plot(label='AF8')
    df[wave_length + "_TP9"].plot(label='TP9')
    df[wave_length + "_TP10"].plot(label='TP10')

    # adding title to the plot
    plt.title('graph per wave length' + wave_length)

    # adding Label to the x-axis
    plt.xlabel('time')
    plt.savefig(fig_path)


def clean_and_create_averaged_per_second_df(df):
    irrelevant_col = "Elements"
    df = df.loc[:, df.columns != irrelevant_col]
    df = df.dropna()
    df = df.groupby('TimeStamp').mean()

    return df


def time_correction(df, avg_reindex_df_path=None):
    df = clean_and_create_averaged_per_second_df(df=df)
    df['TimeStamp'] = np.arange(1, df.shape[0] + 1)
    if avg_reindex_df_path:   # if is not "None", save the new csv file
        df.to_csv(avg_reindex_df_path)

    return df


if __name__ == '__main__':
    df_path = r"C:\Users\danie\Downloads\small_sample.csv"
    df = pd.read_csv(df_path)
    fig_path_save = r"C:\Users\danie\Downloads\tmp.png"
    create_graph_per_electrode(df=df, electrode_name='TP9', fig_path=fig_path_save)
