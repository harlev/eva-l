import streamlit as st

model = st.multiselect("Select models", ["gpt-4o-mini", "gpt-4o"])

prompt = st.text_area("Enter a prompt")
# Initialize session state for columns and data if not exists
if 'columns' not in st.session_state:
    st.session_state.columns = []
if 'data' not in st.session_state:
    st.session_state.data = []



with st.expander("Variable Settings"):
    tab1, tab2 = st.tabs(["Variable Management", "Upload Data"])

    with tab1:
        # Column management section
        col1, col2 = st.columns([3, 1])
        with col1:
            new_column = st.text_input("", placeholder="New variable name", label_visibility="collapsed")
        with col2:
            if st.button("Add Variable"):
                if new_column and new_column not in st.session_state.columns:
                    st.session_state.columns.append(new_column)
                    # Add empty values for new column to existing rows
                    for row in st.session_state.data:
                        row.append("")
                    st.rerun()

    # Display current columns and allow deletion
    if st.session_state.columns:
        cols = st.columns(len(st.session_state.columns))
        for idx, (col, name) in enumerate(zip(cols, st.session_state.columns)):
            with col:
                if st.button(f"❌ {name}", key=f"del_col_{idx}"):
                    # Remove column and its data from all rows
                    for row in st.session_state.data:
                        row.pop(idx)
                    st.session_state.columns.pop(idx)
                    st.rerun()

    with tab2:
        # CSV upload section
        uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
        if uploaded_file is not None:
            import pandas as pd
            try:
                df = pd.read_csv(uploaded_file)
                # Update columns
                st.session_state.columns = list(df.columns)
                # Update data
                st.session_state.data = df.values.tolist()
                st.success("CSV file uploaded successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error reading CSV file: {str(e)}")


    # Data input and display section
    if st.session_state.columns:
        # Convert data to dictionary format for data_editor
        df_data = {col: [row[i] for row in st.session_state.data] 
                for i, col in enumerate(st.session_state.columns)}
        
        # Use data_editor to allow inline editing and row addition
        edited_data = st.data_editor(
            df_data,
            use_container_width=True,
            num_rows="dynamic"
        )

    # Update session state data from edited_data
    if 'edited_data' in locals() and edited_data is not None:
        # Convert edited_data back to list format
        new_data = []
        num_rows = len(next(iter(edited_data.values()), []))
        for row_idx in range(num_rows):
            row_data = []
            for col in st.session_state.columns:
                row_data.append(edited_data[col][row_idx])
            new_data.append(row_data)
        st.session_state.data = new_data

    if st.button("Clear All Data"):
        st.session_state.data = []
        st.rerun()
