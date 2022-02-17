import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap/scss/bootstrap.scss'

//Style global
import './assets/model_style/StyleGlobal.scss'


// import Vue plugin

//import VueSvgInlinePlugin from "vue-svg-inline-plugin";
const app = createApp(App);



//Import composant global
import onoff from './components/OnOffSvg.vue'
app.component('onoff', onoff)

import shapesvg from './components/ShapeSvg.vue'
app.component('shapesvg', shapesvg)
import modelgenerique from './components/ModelGenerique.vue'
app.component('modelgenerique', modelgenerique)
import modeltext from './components/ModelText.vue'
app.component('modeltext', modeltext)
//import modellumiere from './components/ModelLumiere.vue'
//app.component('modellumiere', modellumiere)
//import modelthermostat from './components/ModelThermostat.vue'
//app.component('modelthermostat', modelthermostat)
import modellumiere from './components/ModelLumiere.vue'
app.component('modellumiere', modellumiere)
import modeltemperature from './components/ModelTemperature.vue'
app.component('modeltemperature', modeltemperature)
import modelboutonon from './components/ModelBoutonOn.vue'
app.component('modelboutonon', modelboutonon)
import modelboutonoff from './components/ModelBoutonOff.vue'
app.component('modelboutonoff', modelboutonoff)
//Model Vue
import modelvue from './components/ModelVue.vue'
app.component('modelvue', modelvue)

//Ajout plugin
import testPlugin from './testPlugin'
app.use(testPlugin)



app.mount('#app')
