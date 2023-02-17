from ..database import company_db
from ..models.models import Company

# from ..helpers import helper
import yfinance as yf
import datetime
from matplotlib.figure import Figure
import pandas as pd
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
import plotly.graph_objects as go
import plotly.io as pio


def get_company_data(company: Company) -> Company:

    tk = yf.Ticker(company.ticker)
    stockinfo = tk.info

    # Dates
    today = datetime.datetime.today()
    start = datetime.date(today.year - 50, 1, 1)

    companyWithData = Company(
        name=stockinfo.get("longName", "Sin Datos"),
        ticker=company.ticker,
        stock=yf.download(company.ticker, start=start, end=today),
        country=stockinfo.get("country", "Sin Datos"),
        city=stockinfo.get("city", "Sin Datos"),
        industry=stockinfo.get("industry", "Sin Datos"),
        employees=stockinfo.get("fullTimeEmployees", "Sin Datos"),
        business=stockinfo.get("longBusinessSummary", "Sin Datos"),
    )

    return companyWithData


def get_timeline_plot(company: Company) -> Figure:

    # Create the figure using Plotly
    fig = go.Figure()

    # Add the closing price trace
    fig.add_trace(
        go.Scatter(
            x=company.stock.index,
            y=company.stock["Close"],
            name="Closing Price",
            line=dict(color="royalblue", width=2),
        )
    )

    # Set the layout of the figure
    fig.update_layout(
        title=company.ticker + " Stock Price",
        xaxis_title="Date",
        yaxis_title="Price",
        height=500,
        margin=dict(t=50, b=50, l=50, r=50),
    )

    # Convert the figure to an HTML plot
    plot_html = pio.to_html(fig, full_html=False)

    return plot_html


def get_dividends_plot(company: Company) -> Figure:

    # Dates
    today = datetime.datetime.today()
    start = datetime.date(today.year - 50, 1, 1)

    # Retrieve the stock data using yfinance
    stock = yf.Ticker(company.ticker)
    dividends = stock.dividends

    # Create the figure using Plotly
    fig = go.Figure()

    # Add the dividends trace
    fig.add_trace(
        go.Scatter(
            x=dividends.index,
            y=dividends,
            name="Dividends",
            line=dict(color="royalblue", width=2),
        )
    )

    # Set the layout of the figure
    fig.update_layout(
        title=company.ticker + " Dividends",
        xaxis_title="Date",
        yaxis_title="Dividend Amount",
        height=500,
        margin=dict(t=50, b=50, l=50, r=50),
    )

    # Convert the figure to an HTML plot
    plot_html = pio.to_html(fig, full_html=False)

    return plot_html


def get_comparation_plot(company: Company) -> Figure:

    # Fechas
    today = datetime.datetime.today()  # Fecha de hoy
    start = datetime.date(today.year - 50, 1, 1)  # Fecha - 12 años

    # Define the symbols and time range
    symbols = ["AAPL", "MSFT", "AMZN"]

    if company.ticker not in [symbols]:
        symbols.append(company.ticker)

    # Retrieve the stock data using yfinance
    data = yf.download(symbols, start=start, end=today)["Adj Close"]

    # Create the figure using Plotly
    fig = go.Figure()

    # Add the traces for each stock
    for symbol in symbols:
        fig.add_trace(
            go.Scatter(x=data.index, y=data[symbol], name=symbol, line=dict(width=2))
        )

    # Set the layout of the figure
    fig.update_layout(
        title="Stock Comparison",
        xaxis_title="Date",
        yaxis_title="Adjusted Close Price",
        height=500,
        margin=dict(t=50, b=50, l=50, r=50),
    )

    # Convert the figure to an HTML plot
    plot_html = pio.to_html(fig, full_html=False)

    return plot_html


def get_news(company: Company):
    tk = yf.Ticker(company.ticker)

    news = {}
    for i in range(3):
        news[f"title_new_{i+1}"] = tk.news[i].get("title", "No disponible")
        news[f"link_new_{i+1}"] = tk.news[i].get("link")
        try:

            news[f"img_new_{i+1}"] = (
                tk.news[i].get("thumbnail").get("resolutions")[0].get("url")
            )
        except:
            print(f"WARNING: No image in news {i+1}")

    return news
