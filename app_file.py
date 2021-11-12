import pickle,io
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import pandas as pd
import numpy as  np
import streamlit as st
from PIL import Image
import Equal
import Optimal
import Minimal
import copy

def main():
    st.title("Portfolio Construction of Stocks listed in NSE")
    st.subheader("Enter the tickers of stocks separated by commas")
    st.write("Only enter the tickers of stocks which are listed in NSE")
    stocks = st.text_area(label = "Stocks")
    a=stocks.split(',')
    int_features = [str(x)+".NS" for x in a]
    if st.checkbox("Optimal Risk Portfolio"):
        figs,returns,risks,risklevel,assets=Optimal.figure(int_features)
        buf = io.BytesIO()
        figs.savefig(buf, format='png')
        buf.seek(0)
        pil_img = copy.deepcopy(Image.open(buf))
        st.subheader('Weight Allocation')
        st.image(pil_img)
        st.subheader("Return and Risk of the Portfolio")
        st.error("Volatility of the Portfolio: "+str(np.round(risks,2)))
        st.error("Risk level is "+str(risklevel)) 
        st.success("Expected Return of the Portfolio in Percentage: "+str(np.round(returns,2)))    
        buf.close()
    if st.checkbox("Minimum Variance Portfolio"):
        figs,returns,risks,risklevel,assets=Minimal.figure(int_features)
        buf = io.BytesIO()
        figs.savefig(buf, format='png')
        buf.seek(0)
        pil_img = copy.deepcopy(Image.open(buf))
        st.subheader('Weight Allocation')
        st.image(pil_img)
        st.subheader("Return and Risk of the Portfolio")
        st.error("Volatility of the Portfolio: "+str(np.round(risks,2)))
        st.error("Risk level is "+str(risklevel)) 
        st.success("Expected Return of the Portfolio in Percentage: "+str(np.round(returns,2)))
        buf.close() 
    if st.checkbox("Click here to see the Expected Return and Volatility of Individual Stocks"):
        st.subheader("Expected Return and Volatility of Individual Stocks")
        figs,returns,risks,risklevel,assets=Equal.figure(int_features)
        st.dataframe(assets)      
 

if __name__ == "__main__":
    main()  
    
