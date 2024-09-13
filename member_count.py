from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def convert_time_to_timedelta(time_str):
    try:
        t = datetime.strptime(time_str, '%H:%M:%S')
        return timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
    except ValueError as e:
        print(f"Erro ao converter tempo: {e}")
        return None

def get_new_members(json_data, interval = 20):
    member_messages = []
    for comment in json_data:
        if 'just became a member!' in comment['message']:
            member_messages.append(comment)

    df = pd.DataFrame(member_messages)
    df['timestamp'] = pd.to_datetime(df['time_elapsed'])
    df.set_index('timestamp', inplace=True)
    resampled_df = df.resample(f'{interval}T').size()

    # Plotar grafico
    plt.figure(figsize=(14, 6))
    plt.plot(resampled_df.index, resampled_df.values)
    plt.xlabel('Tempo')
    plt.ylabel('Novos membros')
    plt.title(f'Novos membros a cada {interval} minutos')

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    plt.grid(True)

    path = 'output/novos_membros_por_minuto.png'

    plt.savefig(path)

    return path, member_messages
    
    