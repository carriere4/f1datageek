# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import requests

LOGGER = get_logger(__name__)


def get_drivers_in_session(session_id):
    drivers_in_session = requests.get(
        f"https://api.openf1.org/v1/drivers?session_key={session_id}"
    )
    driver_df = pd.DataFrame(drivers_in_session.json(), get_latest_session())[
        ["broadcast_name"], ["team_name"], ["driver_number"]
    ]
    return driver_df


def get_car_data(session_id):
    driver_id = 2
    car_data = requests.get(
        f"https://api.openf1.org/v1/car_data?driver_number={driver_id}&session_key={session_id}"
    )

    return car_data.json()


def get_latest_session():
    latest_meeting = requests.get(
        "https://api.openf1.org/v1/sessions?session_key=latest"
    )
    return latest_meeting.json()[0]["session_key"]


def get_lap_data(session_id, driver_number):
    lap_data = requests.get(
        f"https://api.openf1.org/v1/laps?session_key={session_id}&driver_number={driver_number}"
    )
    return lap_data.json()


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Welcome to Streamlit! 👋")

    st.markdown(
        """
        F1 Data Geeks from around the world, welcome to the OpenF1 API demo.
    """
    )

    st.write("Session Key", get_latest_session())
    # st.write(
    #     "Drivers in session",
    #     get_drivers_in_session(get_latest_session()),
    # )
    st.write("Car Data", get_car_data(get_latest_session()))
    st.write("Lap Data", get_lap_data(get_latest_session(), 1)[-4:])


if __name__ == "__main__":
    run()
