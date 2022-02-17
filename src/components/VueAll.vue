<template>

  <div v-if="repr ==='html'">
  Html Version

  <modeltemperature v-for="item in messages" :key="item.id" x="300" y="100"  :repr="repr" :proprietes="{'Temperature': {'id': item.id, 'attribut': 'T'}, 'Nom':'Toto'}" />
 </div>
</template>

<script>

 export default {
  name: 'VueAll',
  data(){
      return{
        rectangle: Object,
        valeurNum: Object,
        zoomOb: {x:0,y:0,w:1000,h:1000},
        largeur: "1200"
      }
  },
  components:{
    

      
  },
  mounted(){
    //console.log("Mounted Vue etage: " + this.messages["id125"].valeur)

  },
  props: {
      idVue: String,
      messages: Object,
      repr: {
        type: String,
        default : 'svg'
      },


  },
  computed:{

    
  },
  methods:{
 
  },
  watch:{
      messages: function(newVal, oldVal ){
          console.log('Prop changed: ', newVal, ' | was: ', oldVal)
          //this.valeurNum.textContent = newVal

      }
  },

}
</script>
<style lang="scss" scoped="">
 .svg_text {
  font-family: 'Courier New', Courier, monospace;
  font-weight: bold;
}
</style>