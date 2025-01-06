import streamlit as st
import pandas as pd
import os
import uuid
from datetime import date


# Filepath for CSV
CSV_FILE = "clientes.csv"

# Load CSV
def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE, parse_dates=["Birthday"], date_format="%Y-%m-%d")
    else:
        return pd.DataFrame(columns=["ID","Name", "Birthday", "Type"])

# Save data to CSV
def save_data(data):
    data.to_csv(CSV_FILE, index=False)

# Create a new record
def create_record(data, new_record):
    return pd.concat([data, pd.DataFrame([new_record])], ignore_index=True)

# Read records (view data)
def read_records(data):
    st.data_editor(
        data,
        num_rows="dynamic",
        use_container_width=True,
        key="update_editor",
    )

# Update a record
def update_record(data, record_id, updated_record):
    data.loc[data["ID"] == record_id, ["Name", "Birthday", "Type"]] = (
        updated_record["Name"],
        updated_record["Birthday"],
        updated_record["Type"],
    )
    return data

# Delete a record
def delete_record(data, record_id):
    return data[data["ID"] != record_id]

# Generate the next ID
def generate_id():
    return str(uuid.uuid4()) 

def main(): 
    st.title('CRUD de clientes com CSV')

    # Load data
    data = load_data()
    
    # Variável para controlar a edição
    edit_index = st.session_state.get("edit_index", None)
    
    # Exibição da Tabela com Botões
    st.subheader("Registros Existentes")
    if data.empty:
        st.warning("Nenhum registro encontrado.")
    else:
        for i, row in data.iterrows():
            cols = st.columns([3, 3, 3, 2, 2])
            cols[0].write(row["Name"])
            formatted_date = pd.to_datetime(row["Birthday"]).strftime("%d/%m/%Y")
            cols[1].write(formatted_date)
            cols[2].write(row["Type"])
            
            # Botão para Editar
            if cols[3].button("Editar", key=f"edit_{i}"):
                st.session_state.edit_index = i

            # Botão para Remover
            if cols[4].button("Remover", key=f"remove_{i}"):
                data = data.drop(i).reset_index(drop=True)
                save_data(data)
                st.success(f"Registro com ID {row['ID']} removido com sucesso!")
                st.rerun()

    # Formulario unico
    st.subheader("Adicionar novo cliente")
    with st.form("create_form", clear_on_submit=True):
        if edit_index is None:
            # Adicionar Novo Registro
            default_name = ""
            default_birthday = date.today()
            default_type = "Pessoa Física"
        else:
            # Atualizar Registro Selecionado
            selected_row = data.loc[edit_index]
            default_name = selected_row["Name"]
            default_birthday = pd.to_datetime(row["Birthday"]).date()
            default_type = selected_row["Type"]
        
        name_input = st.text_input("Nome do cliente", value=default_name)
        birthday_input = st.date_input("Data de nascimento", value=default_birthday, format="DD/MM/YYYY")
        type_input = st.selectbox("Tipo de cliente", ["Pessoa Física", "Pessoa Jurídica"], index=["Pessoa Física", "Pessoa Jurídica"].index(default_type))
        
        submitted = st.form_submit_button("Salvar")
        
        if submitted:
            if name_input and type_input:
                if edit_index is None:
                    new_id = generate_id()
                    new_record = {"ID": new_id, "Name": name_input, "Birthday": birthday_input, "Type": type_input}
                    data = create_record(data, new_record)
                    st.success("Cliente adicionado com sucesso!")
                    st.session_state.edit_index = None
                else:
                    data.at[edit_index, "Name"] = name_input
                    data.at[edit_index, "Birthday"] = birthday_input
                    data.at[edit_index, "Type"] = type_input
                    st.success("Cliente atualizado com sucesso!")
                    st.session_state.edit_index = None
                save_data(data)
                st.rerun()
            else:
                st.error("Por favor preencha todos os campos.")

if __name__ == "__main__":
    main()