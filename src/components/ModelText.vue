<template>
 <modelgenerique :proprietes="proprietes" v-if="repr == 'svg'">
  <template v-slot:default="sp">
   <svg :x="x" :y="y" height="30" id="svg8" v-on:click="sp.popup('Valeur')" version="1.1" width="100" xmlns="http://www.w3.org/2000/svg">
<g id="layer1">
<rect class="svg-fond" fill="#008000" height="100%" id="rect843" stroke="#00f" stroke-width="3px" width="100%"/>
<text class="svg-text" dominant-baseline="middle" id="text835" text-anchor="middle" x="50%" xml:space="preserve" y="50%"><tspan id="tspan833" x="50" y="15">{{ sp.pValue.Valeur }}</tspan></text>
</g>
</svg>
  </template>
 </modelgenerique>
 <modelgenerique :proprietes="proprietes" v-if="repr == 'html'">
  <template v-slot:default="sp">
   <input :value="sp.pValue.Valeur" aria-describedby="emailHelp" class="form-control" placeholder="Enter email" type="range" v-if="repr ==='html'" v-on:change="sp.Ecrire($event.target.value, 'Valeur')">
  </template>
 </modelgenerique>
</template>
<script>
 export default {
  name: 'ModelText',
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
 .svg-text {
    color: black;
    font-family:fantasy;
    font-weight: bold;
    font-size: 16px;
    pointer-events: none;
  }
.svg-fond{
  fill :url(#gradient_bleu)  ;
  &:hover{
    stroke-width: 8px;
  }
}
</style>