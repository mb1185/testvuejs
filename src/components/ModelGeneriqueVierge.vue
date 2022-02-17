<template>


<modelgenerique v-if="repr == 'svg'" :proprietes="proprietes"  >
  <template v-slot:default="sp">
      <svg>
      </svg>
          

  </template>
</modelgenerique>

<modelgenerique v-if="repr == 'html'" :proprietes="proprietes"  >
  <template v-slot:default="sp">
      <div>
      </div>
          

  </template>
</modelgenerique>

</template>


<script>
 export default {
  name: 'ModelGeneriqueVierge',
  data(){
      return{

        
      }
  },
  components:{
    
      
  },
  props: {
      proprietes: Object,
      x:String,
      y:String,
      repr: {
        type: String,
        default : 'svg'
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