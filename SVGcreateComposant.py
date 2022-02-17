from bs4 import BeautifulSoup

dossier_svg = 'src/assets/model_svg/'
dossier_html = 'src/assets/model_html/'
dossier_style = 'src/assets/model_style/'
dossier_composants = 'src/components/'


model_composant_vierge = 'ModelGeneriqueVierge'
model_vue_vierge = 'ModelVueVierge'

#models_a_generer = ['ModelTemperature', 'ModelText']
models_a_generer = []
models_a_generer.append({'type_model': model_composant_vierge,'nom':'ModelTemperature'})
models_a_generer.append({'type_model': model_composant_vierge,'nom':'ModelText'})
models_a_generer.append({'type_model': model_vue_vierge,'nom':'VueRdc'})
models_a_generer.append({'type_model': model_composant_vierge,'nom':'ModelBoutonOn'})
models_a_generer.append({'type_model': model_composant_vierge,'nom':'ModelBoutonOff'})
models_a_generer.append({'type_model': model_composant_vierge,'nom':'ModelLumiere'})

for model in models_a_generer:
    
    xml_file_template_vue = dossier_composants + model['type_model'] + '.vue' #ModelGeneriqueVierge.vue' #'src/components/ModelGeneriqueVierge.vue'

    #xml_file_svg = 'src/assets/model_thermostat.svg'
    #xml_file_composant_vue = 'src/components/ModelThermostat.vue'
    #xml_file_svg = 'src/assets/model_svg/ModelText_optimise.svg'
    #xml_file_composant_vue = 'src/components/ModelText2.vue'
    xml_file_svg = dossier_svg + model['nom'] + '_optimise.svg'  #'src/assets/model_svg/ModelTemperature_optimise.svg'
    xml_file_html = dossier_html + model['nom'] + '.html'
    xml_file_style = dossier_style + model['nom'] + '.scss'
    xml_file_composant_vue = dossier_composants + model['nom'] + '.vue' #'src/components/ModelTemperature.vue'

    nom_composant = model['nom']
    nom_a_remplacer = model['type_model']

    compilsvg = ''
    compilhtml = ''
    compilstyle = ''

    #Lecture fichier html a convertir
    with open(xml_file_html, "r", encoding="utf8") as f:
        contents = f.read()
        #soup = BeautifulSoup(contents, "xml")
        soup = BeautifulSoup(contents, "html.parser")
        compilhtml = soup

    #Lecture fichier style a convertir
    with open(xml_file_style, "r", encoding="utf8") as f:
        contents = f.read()
        #soup = BeautifulSoup(contents, "xml")
        soup = BeautifulSoup(contents, "html.parser")
        compilstyle = soup

    #Lecture fichier svg a convertir
    with open(xml_file_svg, "r", encoding="utf8") as f:
        contents = f.read()
        #soup = BeautifulSoup(contents, "xml")
        soup = BeautifulSoup(contents, "xml")

        #Verifie si lien image à remplacer par composant
        
        items = soup.find_all('image')
        print ('Image:', items)
        for image in items:
            #recupere attribut component 
            if 'composant' in image.attrs:
                composant = image['composant']
                print ('composant:', composant)
                #creation tag component (exp : entreenum)
                tag_componant = soup.new_tag(composant)
                #Suppression des attributs non utile
                if 'preserveAspectRatio' in image.attrs:
                    image.attrs.pop('preserveAspectRatio')
                if 'xlink:href' in image.attrs:
                    image.attrs.pop('xlink:href')
                if 'id' in image.attrs:
                    image.attrs.pop('id')
                if 'height' in image.attrs:
                    image.attrs.pop('height')
                if 'width' in image.attrs:
                    image.attrs.pop('width')
                image.attrs.pop('composant')
                #ajout des attributs au tag component
                tag_componant.attrs = image.attrs
                print ("Tag composant:", tag_componant)

                #remplacement du tag image par tag component
                image.replace_with(tag_componant)
    


        items = soup.find_all("svg")
        #nom_composant = items[0].attrs['nom']
        #print ('Svg gg:', items[0])
        compilsvg = str(items[0]).replace("_", ":")
        #print ('Svg Compil:' , compilsvg)


    result_compil = ''
    #Test beautiful
    #Lecture du fichier template Generique .Vue
    with open(xml_file_template_vue, "r", encoding="utf8") as f:
        contents = f.read()
        #soup = BeautifulSoup(contents, "xml")
        soup = BeautifulSoup(contents, "html.parser")

        soup.svg.replace_with(compilsvg)
        soup.div.replace_with(compilhtml)
        #print ("Style-------------------:", soup)
        soup.style.string.replace_with(compilstyle)
        #Remplacement ModelGeneriqueVierge par ModelThermostat
        txt = soup.prettify(formatter=None)
        result_compil = txt.replace(nom_a_remplacer, nom_composant)

        #print ('NomModel -------------------------: ', result_compil)
        #print ("Soup:" ,soup.prettify (formatter=None))

    #Ecriture complet du fichier .vue avec modification du tag svg
    with open(xml_file_composant_vue, "w", encoding="utf8") as f:
        f.write(result_compil)
