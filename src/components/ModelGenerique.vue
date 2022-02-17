<template>
    <slot :pValue="pValue" :proprietes="proprietes" :popup="Popup" :Ecrire="Ecrire"/>
</template>

<script>
 export default {
  name: 'ModelGenerique',
  data(){
      return{
        updateObject: {}

      }
  },
  components:{

      
  },
  props: {
      proprietes: Object,
      x: String,
      y: String,
      repr: {
        type: String,
        default : 'svg'
      },
      
  },
  beforeMount(){
    // abonnemeent de lobject


    if (!(this.proprietes == null)){
        for (const val of Object.values(this.proprietes)){
          //Abonnement aux proprietes contenant un attribut id
          if (typeof(val) == "object"){
            if ('id' in val){
              //console.log('Before Mount Variable:', val['id'])
              this.updateObject[val['id']] = {}
              this.$root.abonnementComposant( val['id'], this.$.uid, this)
            }
          }

        }
    }

    //console.log("Abonnees Onoff:", this.$.uid,  this.$root.abonnees)
  },
  unmounted(){
    // abonnemeent de lobject

    if (!(this.proprietes == null)){
        for (const val of Object.values(this.proprietes)){
          if (typeof(val) == "object"){
            if ('id' in val){
              //console.log('unmounted Mount Variable:', val['id'])
              this.updateObject[val['id']] = {}
              this.$root.desabonnementComposant( val['id'], this.$.uid)
            }
          }
        }
    }
  },
  computed:{
      pValue(){

        var result = {}
        //iteration des proprietes
        for (const [p, val] of Object.entries(this.proprietes)){
          if (val['id'] in this.updateObject){
            result[p] = this.updateObject[val['id']][val['attribut']]
          }
          
        }
        return result

      }

  },
  methods:{
     Popup: function(p){
      var data = {'idObject': this.proprietes[p].id, 'valeur': this.pValue[p], 'attribut': this.proprietes[p].attribut}
      this.fcPopup(data)
    },
    Ecrire: function(value, p ){
      console.log('Ecrire:' + value +" Propriete:" +  p)

      this.fcEmit('update_element',{'id':this.proprietes[p].id, 'attribut':this.proprietes[p].attribut, 'valeur':value});

    },

  },
  inject: ['fcPopup', 'fcEmit'],


}
</script>
<style lang="scss" scoped="">
 .svg_text {
  font-family: 'Courier New', Courier, monospace;
  font-weight: bold;
}
</style>