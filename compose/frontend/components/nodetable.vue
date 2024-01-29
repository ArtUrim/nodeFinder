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
       const response = await fetch('/api/nodes')
       this.items = await response.json();
		 // console.log( this.items )
		 this.item_available = true;
     }
  },
	mounted() {
		this.items = this.fetchData();
  },
};

</script>
