<template>
 <div>
  <button name="bpeTEs" v-on:click="fcZoomMoins">
   Zoom -
  </button>
  <button v-on:click="fcZoomPlus">
   Zoom +
  </button>
 </div>
 <svg :viewBox="zoom" height="1e3" style="height:auto;width:auto" v-if="repr ==='svg'" version="1.1" width="1e3" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<rect height="701.68" id="rect871" style="opacity:.98122;paint-order:stroke fill markers;stroke-linecap:square;stroke-linejoin:round;stroke-miterlimit:4.1;stroke-width:3.9987;stroke:#ff0" width="39.564" x="54.692" y="182.69"></rect>
<rect height="38.401" id="rect873" style="opacity:.98122;paint-order:stroke fill markers;stroke-linecap:square;stroke-linejoin:round;stroke-miterlimit:4.1;stroke-width:3.9987;stroke:#ff0" width="708.67" x="98.911" y="845.98"></rect>
<rect height="34.91" id="rect875" style="opacity:.98122;paint-order:stroke fill markers;stroke-linecap:square;stroke-linejoin:round;stroke-miterlimit:4.1;stroke-width:3.9987;stroke:#ff0" width="346.77" x="102.4" y="588.81"></rect>
<rect height="40.728" id="rect877" style="opacity:.98122;paint-order:stroke fill markers;stroke-linecap:square;stroke-linejoin:round;stroke-miterlimit:4.1;stroke-width:3.9987;stroke:#ff0" width="752.88" x="94.256" y="182.69"></rect>
<rect height="660.96" id="rect880" style="opacity:.98122;paint-order:stroke fill markers;stroke-linecap:square;stroke-linejoin:round;stroke-miterlimit:4.1;stroke-width:3.9987;stroke:#ff0" width="39.564" x="807.58" y="223.42"></rect>


<modelgenerique :proprietes="{'Temperature1': {'id' : 'id128', 'attribut': 'T'},'Lum1': {'id' : 'id127', 'attribut': 'E'} }"  >
  <template v-slot:default="sp">

    <svg xmlns="http://www.w3.org/2000/svg"
     width="100px" height="300px" viewBox="0 0 600 600">

  <text v-on:click="sp.popup('Temperature1')"  x="250" y="150"
        font-family="Verdana"
        font-size="55"
        :fill="$fcCouleur(sp.pValue.Temperature1)">
    FF {{ sp.pValue.Temperature1 }}
  </text>
  <text x="250" y="200"
        font-family="Verdana"
        font-size="55">
    FF {{ sp.pValue.Lum1}}
  </text>

</svg>

   
  </template>
</modelgenerique>

<modelboutonon x="150" y="150" :repr="repr" :proprietes="{'Valeur': {'id':'id126', 'attribut': 'E'}}" />
<modelboutonoff x="150" y="190" :repr="repr" :proprietes="{'Valeur': {'id':'id126', 'attribut': 'E'}}" />
<modeltext x="100" y="100" v-on:click="Popup('Valeur')"  :repr="repr" :proprietes="{'Valeur': {'id':'id128', 'attribut': 'T'}, 'Nom':'Toto'}" />
<modeltemperature x="300" y="100"  :repr="repr" :proprietes="{'Temperature': {'id':'id128', 'attribut': 'T'}, 'Nom':'Toto'}" />
<foreignObject x="300" y="200" width="300" height="150">
<modeltemperature x="0" y="0"  repr="html" :proprietes="{'Temperature': {'id':'id128', 'attribut': 'T'}, 'Nom':'Toto'}" />
</foreignObject>
</svg>
 <div v-if="repr === 'html'">
  Html Version

  <modeltemperature x="300" y="100" :repr="repr"  :proprietes="{'Temperature': {'id':'id128', 'attribut': 'T'}, 'Nom':'Toto'}" />
  <div class="card" style="max-width: 400px;">
  <modeltemperature x="20" y="0" repr="svg"  :proprietes="{'Temperature': {'id':'id128', 'attribut': 'T'}, 'Nom':'Toto'}" />
  </div>
 </div>
</template>
<script>
 export default {
  name: 'VueEtageSvg',
  data(){
      return{
        rectangle: Object,
        valeurNum: Object,
        zoomOb: {x:0,y:0,w:1000,h:1000},
        largeur: "800"
      }
  },
  components:{

      
  },
  mounted(){
    

  },
  props: {
      idVue: String,
      repr: {
        type: String,
        default : 'svg'
      },

  },
  computed:{
    zoom(){
      return [this.zoomOb.x, this.zoomOb.y, this.zoomOb.w, this.zoomOb.h].join(' ');
    },
    
  },
  methods:{
 
    fcChangeColor: function(){
        //this.rectangle.setAttributeNS(null, 'fill', 'red')
        this.valeurNum = "555"
        this.zoomOb.w = this.zoomOb.w + 50
        //this.largeur = "500"
        //this.valeurNum.setAttributeNS(null, 'textContent', '99')
    },
    fcZoomPlus: function(){
     this.zoomOb.w = this.zoomOb.w - 50
     this.zoomOb.h = this.zoomOb.h - 50
    },
    fcZoomMoins: function(){
     this.zoomOb.w = this.zoomOb.w + 50
     this.zoomOb.h = this.zoomOb.h + 50
    },
  },
  watch:{

  },

}
</script>
<style lang="scss" scoped="">
 .svg_text {
  font-family: 'Courier New', Courier, monospace;
  font-weight: bold;
}
</style>