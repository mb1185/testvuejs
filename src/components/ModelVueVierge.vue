<template>
    <modelvue :repr="repr" v-if="repr == 'svg'"   >
    <template v-slot:default="sp">
        <svg>
        </svg>
            

    </template>
    </modelvue>

    <modelvue :repr="repr" v-if="repr == 'html'"   >
    <template v-slot:default="sp">
        <div>
        </div>
            

    </template>
    </modelvue>
</template>
<script>

 export default {
  name: 'ModelVueVierge',
  data(){
      return{

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



}
</script>
<style lang="scss" scoped="">

</style>