<template>
    <svg>
        <ellipse rx="20" ry="20" cx="20" cy="20" :fill='dataValue.Etat'>
        </ellipse>
        <ellipse rx="20" ry="20" cx="60" cy="20" :fill='dataValue.Commande'>
        </ellipse>
    </svg>
</template>

<script>


export default {
  name: 'ShapeSvg',
  data(){
      return{
          updateObject: {},
          couleurResult: 'red',
          

      }
  },
  components:{

      
  },
  props: {
      idobject: Array,
      etat: {
          type: Object,
          default(){
              return {'id': 'idXXX', 'attribut': 'X'}
          } 
      },
      commande: {
          type: Object,
          default(){
              return {'id': 'idXXX', 'attribut': 'X'}
          } 
      },
      nom: String,
      x: String,
      y: String,
      couleur: Object,
      
  },
  beforeMount(){
    console.log("beforeMount")
    this.updateObject[this.etat.id] = {}
    this.updateObject[this.etat.id][this.etat.attribut] = 'XX'
    this.updateObject[this.commande.id] = {}
    this.updateObject[this.commande.id][this.etat.attribut] = 'OFF'
    this.$root.abonnementComposant(this.etat.id, this.$.uid, this)
    this.$root.abonnementComposant(this.commande.id, this.$.uid, this)
  },
  mounted(){
    // abonnemeent de lobject
    // abo a plusieur idobject
    /*
    for (var id of this.idobject){
        //console.log(id)
        this.updateObject[id] = {'E':'OFF'} //init object
        this.$root.abonnementComposant(id, this.$.uid, this)

    }*/
    console.log('Mounted :')


    
    //setInterval(this.fcUpdate, 1000)

  },
  unmounted(){
    // abonnemeent de lobject
    this.$root.desabonnementComposant(this.etat.id, this.$.uid)
    this.$root.desabonnementComposant(this.commande.id, this.$.uid)
  },

  computed:{
      dataValue(){
        console.log('DataValue:', this.updateObject)
        
        var result = {}
        if (this.updateObject[this.etat.id][this.etat.attribut] =='ON'){
            result['Etat'] = 'green'
        }else{
            result['Etat'] = 'red'
        }
        if (this.updateObject[this.commande.id][this.commande.attribut] =='ON'){
            result['Commande'] = 'green'
        }else{
            result['Commande'] = 'red'
        }       
        
        return result
        /*
        for (const value of Object.values(this.updateObject)){
            if (value.E=='ON'){
                result = result && true
            }else{
                result = result && false
            } 
        }
        console.log("RESULT", result)
        if (result){
            return 'green'
        }else{
            return 'red'
        }
        */

      }



  },
  methods:{
 
    fcUpdate: function(){
        //console.log('TEST', val)
        var result = true
        for (var id of this.idobject){
            if (id in this.$root.messages){
                if (this.$root.messages[id].E=='ON'){
                    result = result && true
                }else{
                    result = result && false
                }
            }
        }
        //console.log("RESULT", result)
        if (result){
            this.couleurResult = 'green'
        }else{
            this.couleurResult='red'
        }
    },

  },


}
</script>

<style lang="scss" scoped="">
 .svg_text {
  font-family: 'Courier New', Courier, monospace;
  font-weight: bold;
}
</style>