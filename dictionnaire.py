dict = [["pierre","rock"],
        ["sur","on"],
        ["sous","under"],
        ["à côté","under"],
        ["aller","to go"],
        ["porte","door"],
        ["eau","water"],
        ["ne pas","to not"],
        ["entre","between"],
        ["statue","statue"],
        ["puis","then"],
        ["devant","before"],
        ["derrière","behind"],
        ["herbe","grass"],
        ["bois","wood"],
        ["sable","sand"],
        ["rouge","red"],
        ["bleu","blue"],
        ["jaune","yellow"],
        ["vert","green"]
        ]

def cherche_fr_ang(mot,dictionnaire): #fonctionne au derniere nouvelles
    l = len(dictionnaire)
    for i in range(0,l):
        if dictionnaire[i][0] == mot:
            return dictionnaire[i][1]
    return -1


#print(cherche_fr_ang("devant",dict))

#print(cherche_fr_ang("erreur",dict))