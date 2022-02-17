from bs4 import BeautifulSoup

#xml_file_svg = 'src/assets/model_temperature.svg'
#xml_file_vue = 'src/components/TemperatureSvg.vue' 

#xml_file_svg = 'src/assets/model_entree_num.svg'
#xml_file_vue = 'src/components/EntreeNumSvg.vue'

#xml_file_svg = 'src/assets/model_lumiere.svg'
#xml_file_vue = 'src/components/LumiereSvg.vue'

#xml_file_svg = 'src/assets/model_onoff.svg'
#xml_file_vue = 'src/components/OnOffSvg.vue'

#xml_file_svg = 'src/assets/vue_rdc.svg'
#xml_file_vue = 'src/components/VueRdcSvg.vue'

xml_file_svg = 'src/assets/vue_etage.svg'
xml_file_vue = 'src/components/VueEtageSvg.vue'
#Lecture fichier svg a convertir

with open(xml_file_svg, "r", encoding="utf8") as f:
    contents = f.read()
    #soup = BeautifulSoup(contents, "xml")
    soup = BeautifulSoup(contents, "html.parser")

    #Verifie si lien image à remplacer par composant
    
    items = soup.find_all('image')
    print ('Image:', items)
    for image in items:
        #recupere attribut component 
        composant = image['component']
        print ('Component:', composant)
        #creation tag component (exp : entreenum)
        tag_componant = soup.new_tag(composant)
        #Suppression des attributs non utile
        image.attrs.pop('preserveaspectratio')
        image.attrs.pop('xlink:href')
        if 'id' in image.attrs:
            image.attrs.pop('id')
        if 'height' in image.attrs:
            image.attrs.pop('height')
        if 'width' in image.attrs:
            image.attrs.pop('width')
        image.attrs.pop('component')
        #ajout des attributs au tag component
        tag_componant.attrs = image.attrs
        print ("Tag componant:", tag_componant)

        #remplacement du tag image par tag component
        image.replace_with(tag_componant)
  


    items = soup.find_all("svg")
    #print ('Svg gg:', items[0])
    compilsvg = str(items[0]).replace("_", ":")
    print ('Svg Compil:' , compilsvg)




#Test beautiful
#Lecture du fichier .Vue
with open(xml_file_vue, "r", encoding="utf8") as f:
    contents = f.read()
    #soup = BeautifulSoup(contents, "xml")
    soup = BeautifulSoup(contents, "html.parser")

    items = soup.find_all("svg")
    #print ('Svg:', items)
    #print ("Svg direct:" , soup.svg)
    soup.svg.replace_with(compilsvg)
    #print ("Soup:" ,soup.prettify (formatter=None))

#Ecriture complet du fichier .vue avec modification du tag svg
with open(xml_file_vue, "w", encoding="utf8") as f:
    f.write(soup.prettify(formatter=None))
