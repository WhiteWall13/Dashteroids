from data.get_data import get_df
from dashboard.app.app import run_app

# Get DataFrame
df = get_df()

if __name__ == "__main__":
    # Run App
    run_app(df)
