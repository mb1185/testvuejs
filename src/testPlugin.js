export default {
    install: function (app, options)  {
        console.log ("testPlugin", options)
        app.config.globalProperties.$animation = {}
        app.config.globalProperties.$fcCouleur = function (args){
            //console.log(args)
            if (parseInt(args) > 30){
                return 'red'
            }else{
                return 'green'
            }
            
        }

        app.config.globalProperties.$fcBin = function (valeur, retourOn, retourOff){
            console.log("fcBin :", valeur)
            if (valeur){
                return retourOn
            }else{
                return retourOff
            }
            
        }

        app.config.globalProperties.$fcIf = function (valeur, operateur, valeurTest){
            //console.log("fcIf :", valeur)
            switch(operateur){
                case '==':
                    if (valeur == valeurTest){
                        return true
                    }else{
                        return false
                    }
                case '>':
                    if (valeur > valeurTest){
                        return true
                    }else{
                        return false
                    }
                default:
                    console.log("fcIf operateur non implemente")             
            }


            
        }

        app.config.globalProperties.$animation['fcCouleur'] = app.config.globalProperties.$fcCouleur

      }
  

    
}