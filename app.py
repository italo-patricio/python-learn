import streamlit as st

st.title('Cadastro de clientes')

nome = st.text_input('Digite o nome do cliente')
endereco = st.text_input('Digite o endereço')
data_nascimento = st.date_input('Digite a data de nascimento')
tipo_cliente = st.selectbox('Selecione o tipo de cliente', ['Pessoa Física', 'Pessoa Jurídica'])

cadastrar = st.button('Cadastrar cliente')


if cadastrar:
    with open('clientes.txt', 'a', encoding="utf8") as arquivo:
        arquivo.write(f'{nome},{endereco}, {data_nascimento},{tipo_cliente}\n')
        st.success('Cliente cadastrado com sucesso!')