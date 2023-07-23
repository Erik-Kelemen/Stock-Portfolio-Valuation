import pandas as pd
import numpy as np
from .Analyzers import nav_analyzer
from .Analyzers import pnl_analyzer
from .Analyzers import alphas_analyzer
from .Analyzers import betas_analyzer
from .Analyzers import sharpes_analyzer
from .Analyzers import volatility_analyzer
from .Analyzers import frontier_analyzer

import streamlit as st

class Controller:
    def __init__(self, trades, prices, analyzers = None):
        st.write(f"Welcome to the analyzer!")
        self.trades = trades
        self.prices = prices
        
        if len(self.prices['currency'].unique()) > 1:
            self.standardize_currency()
        if not analyzers:
            nav_anlyzr = nav_analyzer.NAV_Analyzer(trades, prices)
            pnl_anlyzr = pnl_analyzer.PNL_Analyzer(trades, prices)
            volatility_anlyzr = volatility_analyzer.Volatility_Analyzer(trades, prices, nav_anlyzr, pnl_anlyzr)
            alphas_anlyzr = alphas_analyzer.Alphas_Analyzer(trades, prices)
            betas_anlyzr = betas_analyzer.Betas_Analyzer(trades, prices)
            sharpes_anlyzr = sharpes_analyzer.Sharpes_Analyzer(trades, prices)
            frontier_anlyzr = frontier_analyzer.Frontier_Analyzer(trades, prices)
            analyzers = [nav_anlyzr,
                         pnl_anlyzr,
                         volatility_anlyzr,
                         alphas_anlyzr,
                         betas_anlyzr,
                         sharpes_anlyzr,
                         frontier_anlyzr]
        self.analyzers = analyzers
        
            
    def standardize_currency(self):
        """
        Standardize all stock prices to USD using the appropriate =X conversion rate in prices.
        Will drop the conversion rates from the prices table to eliminate pollution
        """
        st.write("Standarding all stock prices to USD:")
        if len(self.prices['currency'].unique()) > 1:
            date_to_rate = self.prices[(self.prices['ticker'] == 'CAD=X')].set_index(['date'])['price']
            def CAD_to_USD(date, currency, price):
                """
                Utility function for converting USD to CAD for a specific date and time.
                """
                return price if currency == 'USD' else price * (1 / date_to_rate[date])
            self.prices['price_USD'] = self.prices.apply(lambda row: 
                                            CAD_to_USD(row['date'], row['currency'], row['price']), 
                                            axis=1)
        else:
            st.write("All stock prices are already in USD.")
            
    def analyze(self):
        for analyzer in self.analyzers:
            analyzer.analyze()
            analyzer.display()