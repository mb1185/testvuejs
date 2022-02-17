<template>
 <modelgenerique :proprietes="proprietes" v-if="repr == 'svg'">
  <template v-slot:default="sp">
   <svg :x="x" :y="y" class="svg" height="35" id="svg8" version="1.1" width="300" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<g id="layer1">
<rect class="svg-fond" fill="blue" height="32.71" id="rect843" width="298.16" x=".97589" y="1.32"/>
<text class="svg-text" dominant-baseline="middle" id="text835" style="fill:#000000;font-family:Arial;font-size:21.333px;letter-spacing:0px;line-height:125%;stroke-width:1px;word-spacing:0px" x="2%" xml:space="preserve" y="50%"><tspan id="tspan833" x="49.886322" y="19.498434">{{ sp.proprietes.Nom }}</tspan></text>
<modelboutonon :proprietes="{'Valeur': sp.proprietes.Etat}" :repr="repr" x="219.7" y="-1.7703"/>
<modelboutonoff :proprietes="{'Valeur': sp.proprietes.Etat}" :repr="repr" x="255.38" y="-1.5483"/>
</g>
</svg>
  </template>
 </modelgenerique>
 <modelgenerique :proprietes="proprietes" v-if="repr == 'html'">
  <template v-slot:default="sp">
   <div class="card" style="max-width: 400px;">
    <div class="card-header">
     {{ sp.proprietes.Nom }}
     <span class="badge bg-info text-dark">
      id : {{ sp.proprietes.Etat.id }}
     </span>
    </div>
    <div class="card-body">
     <div class="variable">
      E : {{ sp.pValue.Etat }}
     </div>
     <modelboutonon :proprietes="{'Valeur': sp.proprietes.Etat}" :repr="repr" x="206" y="17">
     </modelboutonon>
     <modelboutonoff :proprietes="{'Valeur': sp.proprietes.Etat}" :repr="repr" x="206" y="17">
     </modelboutonoff>
    </div>
   </div>
  </template>
 </modelgenerique>
</template>
<script>
 export default {
  name: 'ModelLumiere',
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
 svg{
  filter: drop-shadow( 3px 3px 2px rgba(0, 0, 0, .7));
}
.svg-text {
    font-family: 'Courier New', Courier, monospace;
    font-weight: bold;
    pointer-events: none;
  }

.svg-fond{
  fill :url(#gradient_gris);
  stroke-width: 1px;
  stroke: black;
  &:hover{
    stroke-width: 3px;
  }
}
</style>