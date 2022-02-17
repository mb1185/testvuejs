<template>
  <!-- Composant gradients contenant les references des gradients pour les svg -->
  <gradients /> 
  <!---------------------------------------------------------------------------->
  <div >
    <div class="row">
      <navigation-gauche @ChangementVue="fcChangementVue" />
    </div>
    <div class="row">
        <h1> Titre </h1>
    </div>
    <div >
        <button class="btn btn-primary" width="100px"  v-on:click="fcRequete('get_elements')">Requete</button>
        <testModalBootstrap  v-if="isModalVisible"  :donnees_popup="donnees_popup"> 
                  <template  v-slot:target="ghhh">
                  <div class="modal" tabindex="-1">
                      <div class="modal-dialog">
                          <div class="modal-content">
                              <div class="modal-header">
                                  <h5 class="modal-title">{{ghhh.donnees.titre}}</h5>
                                  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" v-on:click="closeModal"></button>
                              </div>
                              <div class="modal-body">
                                  <input type="text" :placeholder="ghhh.donnees.valeur" v-model="ghhh.donnees.valeur" />
                                  {{ ghhh.donnees.idObject }}
                              </div>
                              <div class="modal-footer">
                                  <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" v-on:click="closeModal">Fermer</button>
                                  <button type="button" class="btn btn-primary" v-on:click="validerModal(ghhh.donnees.idObject,ghhh.donnees.valeur,ghhh.donnees.attribut )">Valider</button>
                              </div>
                          </div>
                      </div>
                  </div>
                  </template>
        </testModalBootstrap>

        <!--<vueEtage :messages="messages" idVue="idVueEtage" />-->
        <div  class="container overflow-auto" style="max-height: 1200px;max-width: 2000px;" >
          <keep-alive>
          <component :is="vueAffiche" :fichierGltf="fichierGltf"  :messages="messages" :idVue="vueAffiche" :repr="repr" />
          </keep-alive>
        </div>
      
    </div>

  </div>

</template>

<script>

import VueEtage from './components/VueEtageSvg.vue'
import VueRdc from './components/VueRdc.vue'
import VueAll from './components/VueAll.vue'
import NavigationGauche from './components/NavigationGauche.vue'
import Gradients from './components/Gradients.vue'

import testModalBootstrap from './components/ModalBootstrap.vue'
import ThreeTest from './components/ThreeTest.vue'
import BabylonTest from './components/BabylonTest.vue'

const io = require("socket.io-client")


export default {
  name: 'App',
  components: {

    VueEtage,
    VueRdc,
    VueAll,
    testModalBootstrap,
    NavigationGauche,
    Gradients,
    ThreeTest,
    BabylonTest,
  },
  setup(){

  },
  data(){
    return{
      abonnees : {},
      vueAffiche: "VueRdc",
      fichierGltf:'',
      messages: {},
      valeur:"dd",
      valeur_popup: "11",
      valeur_temp_popup : "30",
      donnees_popup : {'titre': "Titre Modal", 'idObject' : "XXX", 'attribut' : 'C', 'valeur': "25.3"},
      isModalVisible: false,
      socket: io('ws://localhost:2345', {
        //transports: ['websocket']
      }),
      repr: 'svg',
    }
  },
  mounted(){
    this.socket.on("MESSAGE", (socket)=>{
      console.log("Message recu")
      for (const [idobject, value] of Object.entries(socket)) {
        this.messages[idobject] = value;
        //Mise a jour des component abonnee
        if (idobject in this.abonnees){
          //console.log("Mise a jour Abonnees id: ", idobject)
          for (const abonnee of Object.values(this.abonnees[idobject])){
            //console.log ("Mise a jour Abonnees:",abonnee, value)
              abonnee.updateObject[idobject] = value
          }
        }
      }

    })
  },
  provide() {
    return {
      fcEmit: this.fcRequete,
      fcPopup: this.fcPopup,
      }
  },

  methods:{
    fcRequete: function(topic, data){
      console.log("fcRequete : topic:" + topic + " data:" +  data)
      if (data == null){
        this.socket.emit(topic);
      }else{
        this.socket.emit(topic, data);
      }
      
      
    },
    fcPopup: function(data){
      this.valeur_popup = data
      this.donnees_popup = {'titre': "Titre Modal", 'idObject' : data['idObject'], 'attribut' : data['attribut'], 'valeur': data['valeur']}
      this.showModal()
    },
    showModal() {
      this.isModalVisible = true;
    },
    closeModal() {
      this.isModalVisible = false;
    },
    validerModal: function(id, value, attribut){
      console.log("Valider Modal id:" + id + " valeur:" + value + ' attruibut:' + attribut);
      this.valeur_temp_popup = value;
      this.socket.emit('update_element',{'id':id, 'attribut':attribut, 'valeur':value});
      
    },
    fcChangementVue: function(nomVue, type_repr="svg", fichierGltf = ''){
      console.log("Changment vue:" , nomVue)
      this.repr = type_repr
      this.fichierGltf = fichierGltf
      this.vueAffiche = nomVue
      console.log("FichierGltf:", this.fichierGltf)
      
    },
    abonnementComposant: function(idobject, uid, composant){
      //console.log('abonnementComposant idobject :%s - uid : %s ', idobject, uid)
      if (idobject in this.abonnees){
        this.abonnees[idobject][uid] = composant
        //mise a jour valeur avec memoire message
        if(idobject in this.messages){
          composant.updateObject[idobject] = this.messages[idobject]
        }
        
      }else{
        this.abonnees[idobject] = {}
        this.abonnees[idobject][uid] = composant
        if(idobject in this.messages){
          composant.updateObject[idobject] = this.messages[idobject]
        }
      }
      //console.log('Liste abonnees:', this.abonnees)
    },
    desabonnementComposant: function(idobject, uid){
      //console.log('desabonnementComposant idobject :%s - uid : %s ', idobject, uid)
      delete this.abonnees[idobject][uid]
      // suppression cle idobject si plus d'abonnee
      if (Object.keys(this.abonnees[idobject]).length < 1){
        delete this.abonnees[idobject]
      }
      //console.log('Liste abonnees:', this.abonnees)
    },

  }
}
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 10px;
  height:100%;
}
body{
  height:100%;
}
html{
  height: 100%;
}
</style>
