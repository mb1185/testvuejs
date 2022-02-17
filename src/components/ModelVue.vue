<template>
 <div v-if="repr == 'svg'">
  <button name="bpeTEs" v-on:click="fcZoomMoins">
   Zoom -
  </button>
  <button v-on:click="fcZoomPlus">
   Zoom +
  </button>
 </div>

    <slot :zoom="zoom"/>
</template>
<script>

 export default {
  name: 'ModelVue',
  data(){
      return{
        zoomOb: {x:0,y:0,w:1000,h:1000},
        largeur: "1200"
      }
  },
  components:{
    

      
  },
  mounted(){


  },
  props: {

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

    fcZoomPlus: function(){
     this.zoomOb.w = this.zoomOb.w - 50
     this.zoomOb.h = this.zoomOb.h - 50
    },
    fcZoomMoins: function(){
     this.zoomOb.w = this.zoomOb.w + 50
     this.zoomOb.h = this.zoomOb.h + 50
    },
  },


}
</script>
<style lang="scss" scoped="">

</style>