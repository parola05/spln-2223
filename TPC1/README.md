
# TPC1

Extração e estruturação das informações do ficheiro *medicina.pdf* num formato de dados conveniente.
![enter image description here](https://raw.githubusercontent.com/henriqueparola/spln-2223/main/TPC1/banner.png)

### Ficheiros:
* **medicina.pdf**:  pdf sobre o vocabulário de medicina (galego-espanhol-inglés-portugués);
* **medicina.xml**: xml gerado sobre o ficheiro **medicina.pdf** com o comando:
	*  *pdftohtml medicina.pdf -xml -f 20 -l 543*;
* **medicina.text**: representação intermédia do ficheiro **medicina.xml**  construída com base numa linguagem definida por mim para auxiliar o processo de extração de informações;
* **medicina.json**:  JSON gerado a partir da representação intermédia definida por mim, cuja estruturação da informação é o resultado final pretendido;
* **medicina_filter.py**: script em Python que realiza o trabalho pretendido (tanto a passagem do ficheiro **medicina.xml** para o formato intermédio do ficheiro **medicina.text** como a passagem do formato intermédio para o formato final (**medicina.json**).

### Conceitos
* **Entradas completas** possuem a seguinte estrutura:
	* Índice;
	* Denominação;
	* Categoria gramatical;
	* Áreas temáticas (uma ou várias)
	* Sinónimos (zero ou vários);
	* Variantes (zero ou várias);
	* Traduções:
		* Sinónimos em **es** (zero ou vários);
		* Sinónimos em **en** (zero ou vários);
		* Sinónimos em **pt**  (zero ou vários);
		* Sinónimos em **la** (zero ou vários);
	* Nota informativa (campo opcional)
* **Entradas remissivas** possuem a seguinte estrutura:
	* Denomincação;
	* Palavra referênciada como sinónimo ou variante;

Exemplo de **Entrada Completa** com duas áreas temáticas, dois sinónimos, zero variantes  e três palavras por tradução (sem a tradução em *la*) :
![enter image description here](https://raw.githubusercontent.com/henriqueparola/spln-2223/main/TPC1/repInputComplexo.png)

#  TODO
* Corrigir bug de Identificação de EC conter mais de uma linha no XML.
