<template>
 <svg :x="x" :y="y" height="52.126" v-if="repr === 'svg'" version="1.1" viewbox="0 0 113.22 52.126" width="113.22" xmlns="http://www.w3.org/2000/svg">
<ellipse :class="dataValue.classOn" cx="26.031" cy="26.002" fill="#ff0" rx="26.031" ry="26.002" v-on:click="fcOnOff('ON',$event)"></ellipse>
<ellipse :class="dataValue.classOff" cx="81.095" cy="26.063" fill="#f00" rx="26.095" ry="26.063" v-on:click="fcOnOff('OFF',$event)"></ellipse>
<text pointer-events="none" style="fill:#000000;font-family:Sans;font-size:17.13px;font-variant-caps:normal;font-variant-east-asian:normal;font-variant-ligatures:normal;font-variant-numeric:normal;letter-spacing:0px;line-height:125%;opacity:.997;stroke-width:.91768px;word-spacing:0px" transform="scale(1.0006 .99938)" x="65.996544" xml:space="preserve" y="30.724918"><tspan style="stroke-width:.91768px" x="65.996544" y="30.724918">  OFF </tspan></text>
<text pointer-events="none" style="fill:#000000;font-family:Sans;font-size:17.129px;font-variant-caps:normal;font-variant-east-asian:normal;font-variant-ligatures:normal;font-variant-numeric:normal;letter-spacing:0px;line-height:125%;opacity:.997;stroke-width:.91762px;word-spacing:0px" transform="scale(1.0006 .99944)" x="13.030393" xml:space="preserve" y="30.722931"><tspan style="stroke-width:.91762px" x="13.030393" y="30.722931"> ON </tspan></text>
</svg>
 <div v-if="repr ==='html'">
  <div class="container">
   <div class="row align-items-center">
    <div class="col">
     <div>
      Etat:
      <span class="badge bg-info text-dark" id="id999">
       {{ dataValue.valeur }}
      </span>
     </div>
    </div>
    <div class="col">
     <div style="text-align:right;">
      <button class="btn btn-primary button_onoff" type="button" v-on:click="fcOnOff('ON',$event)">
       ON
      </button>
      <button class="btn btn-primary button_onoff" type="button" v-on:click="fcOnOff('OFF',$event)">
       OFF
      </button>
     </div>
    </div>
   </div>
  </div>
 </div>
</template>
<script>

//import { reactive } from 'vue'

 export default {
  name: 'OnOffSvg',
  data(){
      return{
        updateObject: {},
        
      }
  },
  components:{
    
      
  },
  props: {
      idobject: String,
      attribut: String,
      x:String,
      y:String,
      repr: {
        type: String,
        default : 'svg'
      },


  },

  beforeMount(){
    // abonnemeent de lobject
    console.log ("BeforeMount")
    this.updateObject[this.idobject] = {'E': 'OFF'}
    this.$root.abonnementComposant(this.idobject, this.$.uid, this)
    //console.log("Abonnees Onoff:", this.$.uid,  this.$root.abonnees)
  },
  unmounted(){
    // abonnemeent de lobject
    //console.log("Desabonnement Onoff: ", this.idobject, this.$root.abonnees)
    this.$root.desabonnementComposant(this.idobject, this.$.uid)
  },

  methods:{
 
    fcChangeColor: function(data, ev){
      console.log("FcChangeColor" + data)
      console.log("FcChangeColor" + ev.target)
      //this.$emit('fcEmitSocket', 'get_elements');
      this.fcEmit('get_elements')
      
        //this.rectangle.setAttributeNS(null, 'fill', 'red')
        //this.valeurNum = "555"
        //this.valeurNum.setAttributeNS(null, 'textContent', '99')
    },
    fcOnOff: function(val){
      console.log("fcOnOff val:" , val)
      this.fcEmit('update_element',{'id': this.idobject, 'attribut': this.attribut, 'valeur':val})
    }

  

  },
  inject: ['fcEmit'],
  computed:{


    dataValue(){
      console.log("DataValue:",this.$.uid, this.updateObject)
      var classOn = ''
      var classOff = ''
      if (this.updateObject[this.idobject]['E'] == 'ON'){
        classOn = 'svg_button_onoff ON'
        classOff = 'svg_button_onoff OFF'
      }else{
        classOn = 'svg_button_onoff OFF'
        classOff = 'svg_button_onoff ON'
      }
      return {'valeur': this.updateObject[this.idobject]['E'], 'classOn': classOn, 'classOff': classOff}
    }
    
  },

}
</script>
<style lang="scss" scoped="">
 .svg_text {
  font-family: 'Courier New', Courier, monospace;
  font-weight: bold;
}
.svg_button_onoff{
    stroke: rgb(0, 0, 0);
    stroke-width: 2px;
    background-color: rgb(65, 225, 86);
    &:hover{
      stroke-width: 3px;
      stroke:rgb(42, 103, 202);
      //filter: drop-shadow( 6px 6px 6px rgba(29, 4, 61, 0.7));
    }
    &:active{
      filter: drop-shadow( 6px 6px 6px rgba(29, 4, 61, 0.7));
      //stroke-width: 6px;
    }
}

.ON{
    fill: rgb(39, 165, 39);
}
.OFF{
    fill: rgb(187, 87, 21);
}
</style>