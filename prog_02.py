name=input("Digite o seu nome: ")
age=int(input("Digite a sua idade: "))

if age > 17:
    print("você é maior de idade")
else:
    print("você é menor de idade")

with open("prog_02.txt", "a") as arquivo:
    arquivo.write(f"Seja bem vindo, {name}.\n")