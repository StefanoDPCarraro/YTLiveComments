import os
import matplotlib
matplotlib.use('Agg')  # Define o backend para salvar figuras
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from nuvem import file_to_json

def format_timedelta(td):
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def format_datetime(dt):
    return dt.strftime('%H:%M')

def get_peaks(comments_json, mnt=10, top=3):
    comments_data = file_to_json(comments_json)

    df = pd.DataFrame(comments_data)

    df['time_elapsed'] = pd.to_datetime(df['time_elapsed'])

    df_resampled = df.resample(f'{mnt}T', on='time_elapsed').size().reset_index(name='Comentários')

    top_peaks = df_resampled.nlargest(top, 'Comentários')

    peaks_array = []

    for _, row in top_peaks.iterrows():
        start_time = row['time_elapsed']
        end_time = row['time_elapsed'] + pd.to_timedelta(f'{mnt}min')

        peak_messages = df[(df['time_elapsed'] >= row['time_elapsed']) & (df['time_elapsed'] < row['time_elapsed'] + pd.to_timedelta(f'{mnt}min'))]

        messages_list = [{'message': msg} for msg in peak_messages['message'].tolist()]

        peak_dict = {
            'start': format_datetime(start_time),
            'end': format_datetime(end_time),
            'comments': len(peak_messages),
            'messages': messages_list
        }

        peaks_array.append(peak_dict)

    plt.figure(figsize=(14, 6))
    plt.plot(df_resampled['time_elapsed'], df_resampled['Comentários'])
    plt.xlabel('Time')
    plt.ylabel('Comments')
    plt.title('Comments per 10 minutes')

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=mnt))

    plt.grid(True)

    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    path = os.path.join(output_dir, 'comentarios_por_minuto.png')

    try:
        plt.savefig(path)
    except Exception as e:
        print(f"Erro ao salvar a figura: {e}")
    finally:
        plt.close()

    return peaks_array, path

if __name__ == '__main__':
    get_peaks('comments.json')
