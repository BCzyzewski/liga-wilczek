from csv import writer
import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.no_default_selectbox import selectbox
from streamlit_extras.add_vertical_space import add_vertical_space

from streamlit_extras.badges import badge
import pandas as pd

from datetime import datetime
import pytz


def check_password() -> bool:
    """Returns `True` if the user had the correct password."""

    st.set_page_config(page_title="Liga Wilczek", page_icon=":wolf")

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Hasło", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Hasło", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Hasło niepoprawne")
        return False
    else:
        # Password correct.
        return True


def save_result_to_db(player_1: str, result_1: int, result_2: int, player_2: str, datetime: str):
    with open('results.csv', 'a', newline='\n') as f_object:

        writer_object = writer(f_object)
    
        writer_object.writerow([player_1, result_1, result_2, player_2, datetime])
    
        f_object.close()

def first_tab(tab: st.tabs) -> None:

    with tab:

        colored_header(
        label="Witaj w Aplikacji Wilczkowej Ligi: Phyrexia All Be One!",
        description="Tutaj zapiszesz wyniki meczów i sprawdzisz swoją pozycje w rankingu",
        color_name="orange-70")

        st.image('images/M8rMYriIuVCc.jpg', use_column_width=True)

        st.markdown('Celem apikacji jest usprawnienie procesu zapisywania wyników meczów w ramach ligi. :sunglasses:')

        st.markdown(
            """
            Rozkład apki:
            - **Start** - podstawowe informacje i przydatne linki
            - **Wyniki** - zapisywanie wyników meczów oraz tabela wyników
            - **Leaderboard** - obecny ranking graczy
            - **Statystyki** - statystyki graczy w postaci dashboardu
            """
            ) 

        st.markdown('Aplikacja jest w 100% open source. Kod możesz znaleźć po kliknięciu w link poniżej. :heart:')
        badge(type="github", name="BCzyzewski/liga-wilczek")

        with st.form("my_form"):
            st.write("Masz jakiś pomysł na nową funkcję? Jakiś błąd? Napisz poniżej!")

            text = st.text_input("Napisz", max_chars=5000)

            # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")
            if submitted:
                st.success('Dzięki za sugestię! Postaramy się ją zrealizować. :wink:')



def second_tab(tab: st.tabs) -> None:

    with tab:

        colored_header(
        label="Wyniki",
        description="Tutaj zapiszesz oraz zobaczysz wyniki meczów",
        color_name="violet-70")

        with st.container():

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
                        st.error('Niepoprawny wynik! Zbyt duża ilość gier. Spróbuj ponownie.')
                    elif player_1 is None or player_2 is None:
                        st.error('Niepoprawny wynik! Wybierz graczy. Spróbuj ponownie.')
                    elif player_1 == player_2: 
                        st.error('Niepoprawny wynik! Wybierz różnych graczy. Spróbuj ponownie.')
                    elif result_1 + result_2 == 0:
                        st.error('Raczej nie ma sensu dodawać wyniku 0:0. Spróbuj ponownie.') 
                    else:
                        st.success(f'Wynik dodany! Rezultat: {player_1} {result_1} : {result_2} {player_2}')
                        now = datetime.now(pytz.timezone('Europe/Warsaw')).strftime("%d/%m/%Y %H:%M:%S")
                        save_result_to_db(player_1, result_1, result_2, player_2, now)

            add_vertical_space(1)
            st.markdown('Tabela rezultatów')
            results_df = pd.read_csv('results.csv', header=0).sort_values(by=['Data'], ascending=False)

            st.dataframe(results_df, use_container_width = True)


def third_tab(tab: st.tabs) -> None:

    with tab:

        colored_header(
        label="Leaderboard",
        description="Wyniki na żywo. Wygrana 3 punkty, przegrana 1 punkt.",
        color_name="blue-70")

        df = pd.read_csv('results.csv', header=0)

        players = pd.concat([df['Gracz_1'], df['Gracz_2']]).unique()

        players_dict = {key: [0, 0] for key in players}   



def create_dashboard():

    if check_password():

        tab1, tab2, tab3, tab4 = st.tabs(["Start", "Wyniki", "Leaderboard", "Statystyki"])

        first_tab(tab1)

        second_tab(tab2)

        third_tab(tab3)


create_dashboard()    
