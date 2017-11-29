

f = open("categorias", 'r')
categorias = {}
while 1:
    line = f.readline()
    if not line:
        break
    entrada = line.rstrip()
    entrada = entrada.split(" ")
    print(">>",entrada)
    categorias[entrada[0]] = float(entrada[1])
f.close()
