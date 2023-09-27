import plotly.express as px
from data.get_data import *


def draw_pie_chart(df: pd.DataFrame):
    recclass_counts = df["recclass"].value_counts()
    print(recclass_counts)
    fig = px.pie(
        recclass_counts,
        values=recclass_counts.values,
        names=recclass_counts.index,
        title="Class Distribution of Asteroids",
    )
    return fig


df = get_df()
draw_pie_chart(df).show()
