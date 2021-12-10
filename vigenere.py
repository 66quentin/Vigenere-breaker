import argparse

alphabet = 'abcdefghijklmnopqrstuvwxyz'
fr_frequences = [0.07636, 0.00901, 0.03260, 0.03669, 0.14715, 0.01066, 0.00866, 0.00737, 0.07529, 0.00613, 0.00074, 0.05456, 0.02968, 0.07095, 0.05796, 0.02521, 0.01362, 0.06693, 0.07948, 0.07244, 0.06311, 0.01838, 0.00049, 0.00427, 0.00128, 0.00326]

def indice_c(txt_crpt):
	N = float(len(txt_crpt))
	freq_somme = 0.0
	for lettre in alphabet:
		freq_somme+= txt_crpt.count(lettre) * (txt_crpt.count(lettre)-1)
	try:
		ic = freq_somme/(N*(N-1))
	except:
		print("Texte chiffré trop court")
		quit()	
	return ic

def longueur_cle(txt_crpt):
	liste_ic=[]
	for longueur_hyp in range(20):#A modifier en fonction de la longueur de cle max
		ic_somme=0.0
		ic_moyen=0.0
		for i in range(longueur_hyp):
			sequence=""
			for j in range(0, len(txt_crpt[i:]), longueur_hyp):
				sequence += txt_crpt[i+j]
			ic_somme+=indice_c(sequence)
		if longueur_hyp!=0:
			ic_moyen=ic_somme/longueur_hyp
		liste_ic.append(ic_moyen)
	
	meilleur = [0,0,0]
	for i in range(0,3):
		meilleur[i] = liste_ic.index(sorted(liste_ic, reverse = True)[i])

	return meilleur

def analyse_freq(sequence):
	khi2_total = [0] * 26
	for i in range(26):
		khi2_somme = 0.0
		sequence_decalage = [chr(((ord(sequence[j])-97-i)%26)+97) for j in range(len(sequence))]
		v = [0] * 26
		for l in sequence_decalage:
			v[ord(l) - ord('a')] += 1
		for j in range(26):
			v[j] *= (1.0/float(len(sequence)))
			khi2_somme+=((v[j] - float(fr_frequences[j]))**2)/float(fr_frequences[j])

		khi2_total[i] = khi2_somme
	decalage = khi2_total.index(min(khi2_total))
	return chr(decalage+97)

def obtenir_cle(txt_crpt, cle_longueur):
	cle = ''
	for i in range(cle_longueur):
		sequence=""
		for j in range(0,len(txt_crpt[i:]), cle_longueur):
			sequence+=txt_crpt[i+j]
		cle+=analyse_freq(sequence)
	return cle

def dechiffrer(txt_crpt, cle):
	encode_ascii = [ord(lettre) for lettre in txt_crpt]
	cle_ascii = [ord(lettre) for lettre in cle]
	clair_ascii = []
	for i in range(len(encode_ascii)):
		clair_ascii.append(((encode_ascii[i]-cle_ascii[i % len(cle)]) % 26) +97)

	texteclair = ''.join(chr(i) for i in clair_ascii)
	return texteclair

def main():
	parser = argparse.ArgumentParser(description='Casse un texte chiffré par Vigenere')
	parser.add_argument('-f','--fichier', help='Fichier contenant le texte chiffré', required=True)
	args = parser.parse_args()

	with open(args.fichier, 'r') as f:
		txt_crpt = ''.join(x.lower() for x in f.read() if x.isalpha())
		
	cle_longueur=longueur_cle(txt_crpt)
	print("Les longueurs de clé sont probablement {}".format(cle_longueur)+"\n")

	for i in range(0,len(cle_longueur)):
		cle = obtenir_cle(txt_crpt, cle_longueur[i])
		texteclair = dechiffrer(txt_crpt, cle)
		print(str(i+1)+" - clé: {}".format(cle))
		print(str(i+1)+" - texte en clair tronqué: {}".format(texteclair)[0:50]+"...\n")
					
	cle_correcte = input("Quelle clé est correcte, 1, 2 ou 3:")
	cle = obtenir_cle(txt_crpt, cle_longueur[int(cle_correcte)-1])
	texteclair = dechiffrer(txt_crpt, cle)
	print("Texte en clair entier:\n{}".format(texteclair))
		
if __name__ == '__main__':
	main()
