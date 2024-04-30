import streamlit as st
import requests

def getRoomSuggestion(objectName):
    if('token' not in st.session_state):
        st.switch_page("Login.py")
    token=st.session_state.token
    headers={'authorization': token}
    url=f'http://localhost:5000/item/{objectName}'
    response = requests.get(url=url,headers=headers)
    # print('Status Code:', response.status_code)
    # print('Response Body:', response.json())
    return response


# Create an input field for the object name
object_name = st.text_input("Enter the object to be found:")
if(st.button('Get Suggestion')):
    response=getRoomSuggestion(object_name)
    if(response.status_code==404):
        st.error("Object not found")
    else:
        response=response.json()
        rooms=response['room']
        st.success(f'{object_name} found!')
        st.write('Please check the following rooms(most likely to least likely): ')
        for i in range(len(rooms)):
            st.write(f'{i+1}- {rooms[i]}')
        # st.success(f'{response['room']}')


# Display the object name
# st.write("Object to be found:", object_name)

