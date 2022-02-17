<template>
 <modelgenerique :proprietes="proprietes" v-if="repr == 'svg'">
  <template v-slot:default="sp">
   <svg :x="x" :y="y" height="40" id="svg8" v-on:click="sp.Ecrire('ON', 'Valeur')" version="1.1" width="40" xmlns="http://www.w3.org/2000/svg">
<g id="layer1">
<ellipse :class="$fcBin($fcIf(sp.pValue.Valeur, '==', 'ON'), 'bp On', 'bp Off')" cx="21" cy="19" fill="#f00" id="path3839" rx="13.884" ry="13.884"/>
<text class="svg-text" dominant-baseline="middle" id="text835-7" text-anchor="middle" x="21.092186" xml:space="preserve" y="19.764805"><tspan id="tspan833-2" x="21.092186" y="19.764805">ON</tspan></text>
</g>
</svg>
  </template>
 </modelgenerique>
 <modelgenerique :proprietes="proprietes" v-if="repr == 'html'">
  <template v-slot:default="sp">
   <button class="btn btn-primary" v-on:click="sp.Ecrire('ON', 'Valeur')">
    ON
   </button>
  </template>
 </modelgenerique>
</template>
<script>
 export default {
  name: 'ModelBoutonOn',
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
 @keyframes anim_vert {
  from {fill: brown;}
  to {fill: rgb(38, 255, 0);}
}

.bp{
  filter: drop-shadow( 3px 3px 2px rgba(0, 0, 0, .7));
  stroke-width: 1px;
  stroke: black;
  &.On{
      fill: rgb(0, 255, 0);
      animation-name: anim_vert;
      animation-duration: 2s;

  }
  &.Off{
    fill: brown;
  }
  &:hover{
    stroke-width: 3px;
    }
  &:active{
    filter: drop-shadow( 2px 2px 2px rgba(152, 202, 159, 0.7));
  }
}

.svg-text{
  font-size: 12;
}
</style>