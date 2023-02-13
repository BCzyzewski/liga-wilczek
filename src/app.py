from csv import writer
import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.no_default_selectbox import selectbox
import pandas as pd




def write_color(color_name: str, text: str):

    return st.markdown(f'<h1 style="color:{color_name};font-size:15px;">{text}</h1>', unsafe_allow_html=True)


def save_result_to_db(player_1: str, result_1: int, result_2: int, player_2: str):
    with open('results.csv', 'a', newline='\n') as f_object:

        writer_object = writer(f_object)
    
        writer_object.writerow([player_1, result_1, result_2, player_2])
    
        f_object.close()

def first_tab(tab: st.tabs):

    with tab:

        colored_header(
        label="Witaj w Wilczkowej Lidze",
        description="Tutaj zapiszesz wyniki meczów i sprawdzisz swoją pozycje w rankingu",
        color_name="violet-70")



def second_tab(tab: st.tabs):

    with tab:

        colored_header(
        label="Wyniki",
        description="Tutaj zapiszesz oraz zobaczysz wyniki meczów",
        color_name="violet-70")

        with st.form("submit_match", clear_on_submit=True):

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                player_1 = selectbox("Gracz 1", ["A", "B", "C"])

            with col2:
                result_1 = st.number_input('Wygrane: G1', step = 1, min_value = 0, max_value = 5)

            with col3:
                result_2 = st.number_input('Wygrane: G2', step = 1, min_value = 0, max_value = 5)

            with col4:        
                player_2 = selectbox("Gracz 2", ["A", "B", "C"])


            submitted = st.form_submit_button("Submit")
            if submitted:
                if result_1 + result_2 > 5:
                    st.write(f'Niepoprawny wynik! Zbyt duża ilość gier. Spróbuj ponownie.')
                    write_color("red", f'Niepoprawny wynik! Zbyt duża ilość gier. Spróbuj ponownie.')
                elif player_1 is None or player_2 is None:
                    write_color("red", f'Niepoprawny wynik! Wybierz graczy. Spróbuj ponownie.')
                elif player_1 == player_2: 
                    write_color("red", f'Niepoprawny wynik! Wybierz różnych graczy. Spróbuj ponownie.')
                elif result_1 + result_2 == 0:
                    write_color("yellow", f'Raczej nie ma sensu dodwać wyniku 0:0. Spróbuj ponownie.') 
                else:
                    write_color("green", f'Wynik dodany! Rezultat: {player_1} {result_1} : {result_2} {player_2}')
                    save_result_to_db(player_1, result_1, result_2, player_2)


        results_df = pd.read_csv('results.csv', header=0)

        st.dataframe(results_df)            


def create_dashboard():

    tab1, tab2 = st.tabs(["Welcome", "Results"])

    first_tab(tab1)

    second_tab(tab2)


create_dashboard()    
