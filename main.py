import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import pandas as pd

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)


authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

def owner_dashboard_view():
    st.write(f'Welcome *{name}* to your ProLong dashboard.')
    st.title('Dashboard')
    uploaded_file = st.file_uploader("Choose your data file")
    #smth you want to do with uploaded file (uploaded_file is a subclass of BytesIO)

def marketplace_view():
    st.write(f'Welcome *{name}* to the ProLong marketplace.')
    st.title('Marketplace')
    db = pd.read_csv('db.tsv', sep=',', index_col=0)

    for sell_id, sell in db.iterrows():
        user_id = str(sell['user_id'])
        desc = sell['short_description']
        c1, c2, c3 = st.columns([1, 6, 1])
        with st.container():
            c1.write(f"{user_id}")
            c2.write(f"{desc}")
            buy_button = c3.button(label="Buy", key=user_id+'_user', use_container_width=True)
            if buy_button:
                pass #smth happens here when consumer buys
        st.write('')      
    

#start streamlit form
st.title('ProLong')

name, authentication_status, username = authenticator.login('main') #or sidebar better?

if authentication_status:
    authenticator.logout('LogOut')
    if username == 'web3owner':
        owner_dashboard_view()
    elif username == 'web3consumer':
        marketplace_view()
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')

