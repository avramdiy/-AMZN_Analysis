from flask import Flask, render_template_string, Response
import pandas as pd
import os
import matplotlib.pyplot as plt
import io
import base64
import calendar

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Flask API to Load Path Data</h1><p>Visit /load to see the dataframe.</p>"

@app.route('/load', methods=['GET'])
def load_file():
    file_path = "C:\\Users\\avram\\OneDrive\\Desktop\\TRG Week 24\\amzn.us.txt"

    if not os.path.exists(file_path):
        return {"error": "File does not exist"}, 404

    try:
        df = pd.read_csv(file_path)

        # Drop the 'OpenInt' column if it exists
        if 'OpenInt' in df.columns:
            df = df.drop(columns=['OpenInt'])

        # Convert date column to datetime (assume the column is named 'Date')
        df['Date'] = pd.to_datetime(df['Date'])

        # Filter rows within either of the two date ranges
        mask = (
            ((df['Date'] >= '1998-01-01') & (df['Date'] <= '1998-11-10')) |
            ((df['Date'] >= '2008-01-01') & (df['Date'] <= '2008-11-10'))
        )
        df_filtered = df.loc[mask]

        html_table = df_filtered.to_html(classes='table table-striped', index=False)

        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Filtered DataFrame Viewer</title>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css">
        </head>
        <body>
            <div class="container mt-4">
                <h2>Filtered Data for $AMZN, Year 1998 & Year 2008</h2>
                {html_table}
            </div>
        </body>
        </html>
        """
        return render_template_string(html_template)

    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/openplot')
def plot_open_prices():
    file_path = "C:\\Users\\avram\\OneDrive\\Desktop\\TRG Week 24\\amzn.us.txt"
    if not os.path.exists(file_path):
        return {"error": "File does not exist"}, 404

    try:
        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Filter for years 1998 and 2008
        df_1998 = df[(df['Date'] >= '1998-01-01') & (df['Date'] <= '1998-12-31')]
        df_2008 = df[(df['Date'] >= '2008-01-01') & (df['Date'] <= '2008-12-31')]

        # Aggregate monthly average of "Open" price
        monthly_1998 = df_1998.resample('M', on='Date')['Open'].mean()
        monthly_2008 = df_2008.resample('M', on='Date')['Open'].mean()

        # Create a month index from 1 to 12 for the X-axis
        months = range(1, 13)
        month_names = [calendar.month_abbr[m] for m in months]

        # Reindex both series to have all months from 1 to 12 (fill missing with NaN)
        monthly_1998.index = monthly_1998.index.month
        monthly_2008.index = monthly_2008.index.month

        monthly_1998 = monthly_1998.reindex(months)
        monthly_2008 = monthly_2008.reindex(months)

        plt.figure(figsize=(10,6))
        plt.plot(months, monthly_1998.values, marker='o', label='1998')
        plt.plot(months, monthly_2008.values, marker='o', label='2008')

        plt.title('Monthly Average "Open" Price for 1998 & 2008')
        plt.xlabel('Month')
        plt.ylabel('Average Open Price')
        plt.xticks(months, month_names)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # Save plot to in-memory buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)

        return Response(buf.getvalue(), mimetype='image/png')

    except Exception as e:
        return {"error": str(e)}, 500
    
@app.route('/closeplot')
def plot_close_prices():
    file_path = "C:\\Users\\avram\\OneDrive\\Desktop\\TRG Week 24\\amzn.us.txt"
    if not os.path.exists(file_path):
        return {"error": "File does not exist"}, 404

    try:
        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Filter for years 1998 and 2008
        df_1998 = df[(df['Date'] >= '1998-01-01') & (df['Date'] <= '1998-12-31')]
        df_2008 = df[(df['Date'] >= '2008-01-01') & (df['Date'] <= '2008-12-31')]

        # Aggregate monthly average of "Open" price
        monthly_1998 = df_1998.resample('M', on='Date')['Close'].mean()
        monthly_2008 = df_2008.resample('M', on='Date')['Close'].mean()

        # Create a month index from 1 to 12 for the X-axis
        months = range(1, 13)
        month_names = [calendar.month_abbr[m] for m in months]

        # Reindex both series to have all months from 1 to 12 (fill missing with NaN)
        monthly_1998.index = monthly_1998.index.month
        monthly_2008.index = monthly_2008.index.month

        monthly_1998 = monthly_1998.reindex(months)
        monthly_2008 = monthly_2008.reindex(months)

        plt.figure(figsize=(10,6))
        plt.plot(months, monthly_1998.values, marker='o', label='1998')
        plt.plot(months, monthly_2008.values, marker='o', label='2008')

        plt.title('Monthly Average "Close" Price for 1998 & 2008')
        plt.xlabel('Month')
        plt.ylabel('Average Close Price')
        plt.xticks(months, month_names)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # Save plot to in-memory buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)

        return Response(buf.getvalue(), mimetype='image/png')

    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/medianplot')
def plot_high_low_prices():
    file_path = "C:\\Users\\avram\\OneDrive\\Desktop\\TRG Week 24\\amzn.us.txt"
    if not os.path.exists(file_path):
        return {"error": "File does not exist"}, 404

    try:
        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['Date'])

        # Filter for years 1998 and 2008
        df_1998 = df[(df['Date'] >= '1998-01-01') & (df['Date'] <= '1998-12-31')]
        df_2008 = df[(df['Date'] >= '2008-01-01') & (df['Date'] <= '2008-12-31')]

        # Aggregate monthly median of "High" and "Low" prices
        monthly_1998 = df_1998.resample('M', on='Date')[['High', 'Low']].median()
        monthly_2008 = df_2008.resample('M', on='Date')[['High', 'Low']].median()

        # Prepare months for x-axis
        months = range(1, 13)
        month_names = [calendar.month_abbr[m] for m in months]

        # Convert index to month numbers and reindex to ensure all months present
        monthly_1998.index = monthly_1998.index.month
        monthly_2008.index = monthly_2008.index.month

        monthly_1998 = monthly_1998.reindex(months)
        monthly_2008 = monthly_2008.reindex(months)

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.plot(months, monthly_1998['High'], marker='o', label='1998 High')
        plt.plot(months, monthly_1998['Low'], marker='o', label='1998 Low')
        plt.plot(months, monthly_2008['High'], marker='o', label='2008 High')
        plt.plot(months, monthly_2008['Low'], marker='o', label='2008 Low')
        plt.title('Monthly Median High and Low Prices for 1998 & 2008')
        plt.xlabel('Month')
        plt.ylabel('Median Price')
        plt.xticks(months, month_names)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # Save plot to in-memory buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)

        return Response(buf.getvalue(), mimetype='image/png')

    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == '__main__':
    app.run(debug=True)
