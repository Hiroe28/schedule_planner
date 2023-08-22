import streamlit as st
import pandas as pd
from events import create_event, get_event, add_participant, remove_participant
import time

def create_event_page():
    st.title("イベント作成")
    event_name = st.text_input("イベント名")
    memo = st.text_area("メモ")
    dates = st.text_area("候補日程 (例: 8/7(月) 20:00～)")

    if st.button("イベント作成"):
        event_id = create_event(event_name, memo, dates.split("\n"))
        st.success(f"イベントが作成されました。以下のURLをみんなに知らせてあげましょう: http://localhost:8501/?path=event&event_id={event_id}")


def get_event_data(event_id):
    event = get_event(event_id)
    if event is None:
        st.error("イベントが見つかりません")
        return None
    return event


def attendance_input(event):
    name = st.text_input("名前")
    availability = [st.radio(date, ["◯", "△", "×"]) for date in event['dates']]
    comment = st.text_input("コメント")
    return name, availability, comment


def display_dates(event, participants):
    dates_count = {date: [0, 0, 0] for date in event['dates']}

    for participant_availability in participants.values():
        for i, status in enumerate(participant_availability['availability']):
            if status == "◯":
                dates_count[event['dates'][i]][0] += 1
            elif status == "△":
                dates_count[event['dates'][i]][1] += 1
            else:
                dates_count[event['dates'][i]][2] += 1

    # DataFrameを作成
    columns = ["日程", "◯", "△", "×"]
    rows = []
    for participant_name in participants.keys():
        columns.append(participant_name)
    for date, count in dates_count.items():
        row = [date, f"{count[0]}人", f"{count[1]}人", f"{count[2]}人"]
        for participant_availability in participants.values():
            row.append(participant_availability['availability'][event['dates'].index(date)])
        rows.append(row)

    # コメント行の追加
    comment_row = ["コメント", "", "", ""]
    for participant_info in participants.values():
        comment_row.append(participant_info['comment'])
    rows.append(comment_row)

    df = pd.DataFrame(rows, columns=columns)
    st.table(df)


def event_page(event_id):
    event = get_event_data(event_id)
    if event is None:
        return

    st.title(event['name'])
    st.subheader("メモ")
    st.write(event['memo'])

    st.subheader("候補日程")
    display_dates(event, event['participants'])

    st.subheader("出欠入力")
    name, availability, comment = attendance_input(event)

    is_input_clicked = st.button("入力")
    if is_input_clicked:
        add_participant(event_id, name, availability, comment)
        st.success("出欠情報を更新しました。")
        time.sleep(2)  # 2秒待機
        st.experimental_rerun()

    st.subheader("出欠削除")
    name_to_remove = st.selectbox("削除する名前", [""] + list(event['participants'].keys()), key="name_to_remove")
    if name_to_remove and st.button("削除"):
        remove_participant(event_id, name_to_remove)
        st.success(f"{name_to_remove}の出欠情報を削除しました。")
        time.sleep(2)  # 2秒待機
        st.experimental_rerun()

if __name__ == "__main__":
    path = st.experimental_get_query_params().get("path")
    event_id = st.experimental_get_query_params().get("event_id")

    if path and path[0] == "event" and event_id:
        event_page(int(event_id[0]))
    else:
        create_event_page()
