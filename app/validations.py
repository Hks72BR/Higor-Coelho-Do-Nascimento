def validar_cpf(cpf):
    if len(cpf) != 11 or not cpf.isdigit():
        return False
    # Adicione validação de CPF real aqui
    return True
