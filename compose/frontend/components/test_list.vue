<template>
  <v-card>
    <div class="d-flex flex-row">
      <v-tabs direction="vertical" color="primary">
			<v-tab v-show="!is_top" @click="returnUp" >
				...
			</v-tab>
        <v-tab v-for="item in items" :value="item.name"
			  @click="fetchData(item.name)" >
			  {{ item.name }}
        </v-tab>
      </v-tabs>
		{{ text }}
    </div>
  </v-card>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
		 items: [],
		 text: null,
		 is_top: true,
		 project: null,
    };
  },
  methods: {
	  async fetchData(item) {
		  let href = '/api/test';
		  if( this.project === null ) {
			  href += 's/' + item;
		  } else {
			  href += '/' + this.project + '/file/' + item;
		  }
		  const response = await fetch( href );
		  this.is_top = false;
		  const retVal = await response.json();
		  if( this.project === null ) {
			  this.project = item;
			  this.items = retVal;
		  } else {
			  this.text = retVal.content.replaceAll( '\n', '<br>\n' );
		  }
	  },
	  async returnUp() {
		  this.text = null;
		  const response = await fetch( '/api/tests' );
		  this.items = await response.json();
		  this.is_top = true;
		  this.project = null;
	  }
  },
	mounted() {
		this.items = this.returnUp(null);
	   // console.log( "Is Billy on the line?" )
  },
};

</script>
