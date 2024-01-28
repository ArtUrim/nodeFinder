<template>
  <v-card>
    <div class="d-flex flex-row">
      <v-tabs v-model="items" direction="vertical" color="primary">
        <v-tab v-for="item in items" :value="item.name">
			  {{ item.name }}
        </v-tab>
      </v-tabs>
    </div>
  </v-card>
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
       const response = await fetch('http://localhost/api/tests')
       this.items = await response.json();
		 console.log( this.items )
		 console.log( this.items[0] )
		 console.log( this.items.length )
		 this.item_available = true;
     }
  },
	mounted() {
		this.items = this.fetchData();
	   console.log( "Is Billy on the line?" )
  },
};

</script>
