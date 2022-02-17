<template>

    <ul class="nav justify-content-center">
      <img width="50" alt="Vue logo" src="../assets/logo.png">
    <li class="nav-item">
        <a class="nav-link active border border-primary" aria-current="page" href="#" v-on:click="fcSelectVue('VueEtage')">Vue Etage SVG</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="#" v-on:click="fcSelectVue('VueRdc')">Vue RDC SVG</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="#" v-on:click="fcSelectVue('VueEtage', 'html')">Vue Etage Html</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="#" v-on:click="fcSelectVue('VueRdc', 'html')">Vue RDC Html</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="#" v-on:click="fcSelectVue('VueAll', 'html')">Vue All Html</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="#" v-on:click="fcSelectVue('ThreeTest', '3D', 'testthreejs.gltf')">Vue 3D</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="#" v-on:click="fcSelectVue('BabylonTest', '3D', 'testthreejs.gltf')">Babylon3D</a>
    </li>
    </ul>


</template>



<script>




export default {
  name: 'NavigationGauche',
  data(){
      return{

      }
  },
  components:{

      
  },
  emits:{
      ChangementVue: null,
  },
  mounted(){
    //console.log("Mounted Vue etage: " + this.messages["id125"].valeur)

  },
  props: {


  },
  computed:{

    
  },
  methods:{
    fcSelectVue: function(nomVue, type_repr, fichierGltf){
        console.log('Nom vue:',  nomVue)
        this.$emit('ChangementVue', nomVue, type_repr, fichierGltf)
    },
  },
  watch:{

  },

}
</script>

<style scoped lang="scss">
.nav-item{
  :hover{
    color: green,
  }
  :active{
    background-color: hotpink;
    
  }
  
}
.nav-link{
  color:rgb(19, 0, 128);
  :active{
    background-color: hotpink;
    
  }
}
.nav{
  :active{
    background-color: rgb(54, 182, 233);
  }
}
.active{
  background-color: rgb(178, 228, 230);
}
</style>