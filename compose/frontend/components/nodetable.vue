<template>
  <v-data-table v-if="item_available" :items="items"></v-data-table>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
		 items: [],
		 item_available: false,
    };
  },
  methods: {
     async fetchData() {
       const response = await fetch('http://localhost/api/nodes')
       this.items = await response.json();
		 this.item_available = true;
     }
  },
	mounted() {
		this.items = this.fetchData();
	   console.log( "Is Billy on the line?" )
  },
};

</script>
