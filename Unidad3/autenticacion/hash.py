import bcrypt

#Paso 1. pedir contraseña
incoming_password = input("Ingrese su contraseña:").encode("UTF-8")
#Paso 2. Generar un salt
salt = bcrypt.gensalt(rounds=12)
#Paso 3. Hashear la contraseña con el Salt
hashed_password = bcrypt.hashpw(incoming_password, salt)
print(hashed_password)
#Paso 4. Pedor nuevamente la contraseña
confirm_password = input("Ingrese nuevamente la contraseña:").encode("UTF-8")
#Paso 5. Verificar si la contraseña corresponde
if bcrypt.checkpw(confirm_password,hashed_password):
    print("Contraseña correcta")
else:
    print("Contraseña incorrecta")